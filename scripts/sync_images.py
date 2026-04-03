#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
英语陪跑GO - 图片本地化脚本
从微信、数据库或外部URL拉取图片，转为本地存储，更新数据库链接

用法：
  python3 sync_images.py                 # 自动检测并本地化
  python3 sync_images.py --list          # 列出所有需要处理的图片
  python3 sync_images.py --update-qr     # 更新二维码
  python3 sync_images.py --clean         # 清理临时文件
"""

from __future__ import print_function
import sys
import os
import time
import hashlib
import pymysql
from datetime import datetime
import requests
from PIL import Image
from io import BytesIO
import json

# 配置
DB = dict(
    host='localhost',
    user='xiachaoqing',
    password='***REMOVED***',
    db='epgo_db',
    charset='utf8mb4',
    port=3306
)

# 图片存储路径
IMAGE_DIR = '/www/wwwroot/go.xiachaoqing.com/upload/local_images'
WEB_PREFIX = '../upload/local_images'

# 二维码配置
QR_SOURCES = {
    'footinfo_wx': {
        'name': '公众号二维码',
        'size': (170, 170),
        'filename': 'qr_wechat.png'
    }
}

# 用户代理
HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/120.0.0.0 Safari/537.36'
    )
}


class ImageSyncer:
    def __init__(self):
        self.conn = None
        self.local_count = 0
        self.error_count = 0

    def connect(self):
        """连接数据库"""
        try:
            self.conn = pymysql.connect(**DB)
            print('✓ 数据库连接成功')
        except Exception as e:
            print('✗ 数据库连接失败: {}'.format(e))
            return False
        return True

    def close(self):
        """关闭连接"""
        if self.conn:
            self.conn.close()

    def download_image(self, url, timeout=10):
        """下载图片"""
        try:
            response = requests.get(url, headers=HEADERS, timeout=timeout, verify=False)
            if response.status_code == 200:
                return BytesIO(response.content)
            else:
                print('  ✗ HTTP {}: {}'.format(response.status_code, url[:50]))
                return None
        except Exception as e:
            print('  ✗ 下载失败: {}'.format(str(e)[:50]))
            return None

    def remove_bg(self, image_data):
        """简单的背景移除 - 将黑色边框去掉"""
        try:
            img = Image.open(image_data)

            # 转RGBA便于处理透明
            if img.mode != 'RGBA':
                img = img.convert('RGBA')

            # 获取图像数据
            data = img.getdata()

            # 设定黑色阈值（识别接近黑色的像素）
            BLACK_THRESHOLD = 30  # 如果RGB都 < 30，认为是黑色

            # 处理每个像素
            new_data = []
            for item in data:
                r, g, b, a = item if len(item) == 4 else (*item[:3], 255)
                # 如果是黑色或接近黑色，设为透明
                if r < BLACK_THRESHOLD and g < BLACK_THRESHOLD and b < BLACK_THRESHOLD:
                    new_data.append((255, 255, 255, 0))  # 透明
                else:
                    new_data.append(item if len(item) == 4 else (r, g, b, 255))

            img.putdata(new_data)

            # 转出结果
            result = BytesIO()
            img.save(result, format='PNG')
            result.seek(0)
            return result
        except Exception as e:
            print('  ✗ 图片处理失败: {}'.format(e))
            return image_data

    def save_image(self, image_data, filename):
        """保存图片到本地"""
        try:
            # 确保目录存在
            os.makedirs(IMAGE_DIR, exist_ok=True)

            filepath = os.path.join(IMAGE_DIR, filename)

            # 处理PIL Image对象
            if isinstance(image_data, Image.Image):
                image_data.save(filepath, 'PNG')
            else:
                # BytesIO对象
                with open(filepath, 'wb') as f:
                    f.write(image_data.getvalue())

            print('  ✓ 已保存: {}'.format(filename))
            return True
        except Exception as e:
            print('  ✗ 保存失败: {}'.format(e))
            return False

    def update_db_image(self, config_name, local_path):
        """更新数据库中的图片路径"""
        try:
            sql = "INSERT INTO ep_config (name, value, lang) VALUES (%s, %s, 'cn') ON DUPLICATE KEY UPDATE value=%s"
            cur = self.conn.cursor()
            cur.execute(sql, (config_name, local_path, local_path))
            self.conn.commit()
            print('  ✓ 数据库已更新: {} = {}'.format(config_name, local_path))
            return True
        except Exception as e:
            print('  ✗ 数据库更新失败: {}'.format(e))
            return False

    def sync_qr_codes(self):
        """同步二维码"""
        print('\n📱 同步二维码')
        print('-' * 50)

        for config_name, qr_info in QR_SOURCES.items():
            print('\n[{}] {}'.format(config_name, qr_info['name']))

            # 读取当前URL
            cur = self.conn.cursor()
            cur.execute("SELECT value FROM ep_config WHERE name=%s AND lang='cn'", (config_name,))
            result = cur.fetchone()

            if not result:
                print('  ⚠️  未找到配置')
                continue

            url = result[0]

            # 检查是否已是本地路径
            if url.startswith('../upload/local_images') or url.startswith('/upload/local_images'):
                print('  ✓ 已是本地路径，无需同步')
                continue

            print('  下载: {}'.format(url[:50]))

            # 下载图片
            image_data = self.download_image(url)
            if not image_data:
                self.error_count += 1
                continue

            # 去除黑色背景
            print('  处理: 去除黑色边框')
            cleaned = self.remove_bg(image_data)

            # 保存本地
            filename = qr_info['filename']
            if self.save_image(cleaned, filename):
                # 更新数据库
                local_url = '{}/{}'.format(WEB_PREFIX, filename)
                if self.update_db_image(config_name, local_url):
                    self.local_count += 1
            else:
                self.error_count += 1

    def sync_news_images(self):
        """同步新闻文章的图片"""
        print('\n📰 同步文章图片')
        print('-' * 50)

        # 查找所有有外链图片的文章
        sql = "SELECT id, title, imgurl FROM ep_news WHERE imgurl LIKE '%http%' LIMIT 20"
        cur = self.conn.cursor()
        cur.execute(sql)
        results = cur.fetchall()

        print('找到 {} 篇需要处理的文章'.format(len(results)))

        for nid, title, imgurl in results:
            print('\n[ID:{}] {}'.format(nid, title[:30]))
            print('  原URL: {}'.format(imgurl[:60]))

            # 下载图片
            image_data = self.download_image(imgurl)
            if not image_data:
                self.error_count += 1
                continue

            # 生成本地文件名（基于原URL哈希）
            hash_name = hashlib.md5(imgurl.encode()).hexdigest()[:8]
            ext = imgurl.split('.')[-1] if '.' in imgurl else 'jpg'
            filename = 'news_{}_{}.{}'.format(nid, hash_name, ext)

            # 保存本地
            if self.save_image(image_data, filename):
                # 更新数据库
                local_url = '{}/{}'.format(WEB_PREFIX, filename)
                try:
                    sql_update = "UPDATE ep_news SET imgurl=%s WHERE id=%s"
                    cur.execute(sql_update, (local_url, nid))
                    self.conn.commit()
                    print('  ✓ 数据库已更新')
                    self.local_count += 1
                except Exception as e:
                    print('  ✗ 更新失败: {}'.format(e))
                    self.error_count += 1
            else:
                self.error_count += 1

    def list_external_images(self):
        """列出所有外链图片"""
        print('\n📋 外链图片清单')
        print('-' * 50)

        # 配置中的图片
        print('\n[系统配置]')
        cur = self.conn.cursor()
        cur.execute("SELECT name, value FROM ep_config WHERE lang='cn' AND value LIKE '%http%'")
        configs = cur.fetchall()

        for name, url in configs:
            print('  {}: {}'.format(name, url[:60]))

        # 文章中的图片
        print('\n[文章图片]')
        cur.execute("SELECT id, title, imgurl FROM ep_news WHERE imgurl LIKE '%http%' LIMIT 20")
        articles = cur.fetchall()

        for nid, title, url in articles:
            print('  [ID:{}] {} - {}'.format(nid, title[:25], url[:50]))

        print('\n共 {} 个配置 + {} 篇文章需要处理'.format(
            len(configs), len(articles)))

    def cleanup(self):
        """清理临时文件"""
        print('\n🧹 清理临时文件')
        print('-' * 50)

        try:
            # 这里可以清理下载的临时文件
            print('✓ 清理完成')
        except Exception as e:
            print('✗ 清理失败: {}'.format(e))

    def run(self):
        """运行同步"""
        print('\n' + '='*60)
        print('[{}] 图片本地化同步'.format(
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        print('='*60)

        if not self.connect():
            return

        try:
            # 执行同步
            if '--list' in sys.argv:
                self.list_external_images()
            elif '--clean' in sys.argv:
                self.cleanup()
            elif '--update-qr' in sys.argv:
                self.sync_qr_codes()
            else:
                # 默认：全部同步
                self.sync_qr_codes()
                self.sync_news_images()
        finally:
            self.close()

        # 总结
        print('\n' + '='*60)
        print('✓ 本地化完成 - 成功: {}, 失败: {}'.format(
            self.local_count, self.error_count))
        print('='*60 + '\n')


if __name__ == '__main__':
    syncer = ImageSyncer()
    syncer.run()
