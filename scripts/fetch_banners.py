#!/usr/bin/env python3
"""
爬取英语学习相关的高质量图片作为首页轮播banner
图片来源：Unsplash (免费商用)
直接下载到服务器 upload 目录并插入 MetInfo ep_flash 表
"""
import urllib.request, json, os, time, subprocess

# Unsplash 不需要API key 可直接访问source URL
# 格式: https://source.unsplash.com/1440x600/?关键词
# 或用直接的图片URL（稳定）

BANNERS = [
    {
        "title":   "KET备考 · 高效冲刺",
        "desc":    "系统备考，轻松拿证",
        "link":    "/ket/",
        "url":     "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=1440&h=600&fit=crop&q=80",
        # 学生在图书馆看书学习
    },
    {
        "title":   "PET备考 · 中级突破",
        "desc":    "听说读写，全面提升",
        "link":    "/pet/",
        "url":     "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=1440&h=600&fit=crop&q=80",
        # 英语书本和笔记
    },
    {
        "title":   "每日打卡 · 坚持就是胜利",
        "desc":    "10000+学员陪你一起备考",
        "link":    "/ket-exam/",
        "url":     "https://images.unsplash.com/photo-1427504494785-3a9ca7044f45?w=1440&h=600&fit=crop&q=80",
        # 教室场景
    },
    {
        "title":   "真题解析 · 掌握出题规律",
        "desc":    "历年真题逐题精讲",
        "link":    "/ket-exam/",
        "url":     "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=1440&h=600&fit=crop&q=80",
        # 学生做题
    },
    {
        "title":   "英语阅读 · 拓展视野",
        "desc":    "从阅读开始，爱上英语",
        "link":    "/reading/",
        "url":     "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=1440&h=600&fit=crop&q=80",
        # 阅读场景
    },
]

UPLOAD_DIR  = "/www/wwwroot/go.xiachaoqing.com/upload/banner"
DB_CMD      = "mysql -h 127.0.0.1 -u xiachaoqing -p***REMOVED*** epgo_db"
SERVER      = "epgo"
YEAR_MONTH  = time.strftime("%Y%m")

def run_remote(cmd):
    result = subprocess.run(
        ["ssh", SERVER, cmd],
        capture_output=True, text=True
    )
    return result.stdout.strip(), result.returncode

def download_and_upload(banner, idx):
    filename = f"banner_{idx+1}_{int(time.time())}.jpg"
    remote_path = f"{UPLOAD_DIR}/{filename}"
    web_path    = f"upload/banner/{filename}"

    print(f"  下载: {banner['url'][:60]}...")
    # 先下载到本地临时文件
    local_tmp = f"/tmp/{filename}"
    try:
        req = urllib.request.Request(
            banner["url"],
            headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=20) as r:
            data = r.read()
        with open(local_tmp, "wb") as f:
            f.write(data)
        print(f"  已下载 {len(data)//1024}KB")
    except Exception as e:
        print(f"  下载失败: {e}")
        return None

    # 确保远端目录存在
    run_remote(f"mkdir -p {UPLOAD_DIR}")

    # 上传到服务器
    result = subprocess.run(
        ["scp", local_tmp, f"{SERVER}:{remote_path}"],
        capture_output=True, text=True
    )
    os.remove(local_tmp)

    if result.returncode != 0:
        print(f"  上传失败: {result.stderr}")
        return None

    print(f"  已上传到: {remote_path}")
    return web_path


def insert_banner(title, desc, link, img_path, order):
    sql = (
        f"INSERT INTO ep_flash "
        f"(img_title, img_des, img_link, img_path, no_order, lang, target, width, height) "
        f"VALUES ('{title}', '{desc}', '{link}', '{img_path}', {order}, 'cn', 0, 1440, 600);"
    )
    out, rc = run_remote(f'{DB_CMD} -e "{sql}" 2>/dev/null')
    if rc == 0:
        print(f"  插入DB成功")
    else:
        print(f"  插入DB失败: {out}")


if __name__ == "__main__":
    print("=" * 55)
    print("  首页轮播图爬取与配置")
    print("=" * 55)

    # 先清空已有banner
    run_remote(f'{DB_CMD} -e "DELETE FROM ep_flash;" 2>/dev/null')
    print("已清空旧banner\n")

    for i, banner in enumerate(BANNERS):
        print(f"[{i+1}/{len(BANNERS)}] {banner['title']}")
        img_path = download_and_upload(banner, i)
        if img_path:
            insert_banner(
                title    = banner["title"],
                desc     = banner["desc"],
                link     = banner["link"],
                img_path = img_path,
                order    = i + 1
            )
        print()
        time.sleep(1)  # 避免请求过快

    print("✅ 完成！共配置了", len(BANNERS), "张轮播图")
    print("👉 刷新 https://xiachaoqing.com 查看效果（需要在index.php添加banner标签）")
