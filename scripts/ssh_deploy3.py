import paramiko, time

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('39.105.154.244', 22, 'root', 'Xia07090218', timeout=15)

def run(cmd, timeout=30):
    _, o, e = client.exec_command(cmd, timeout=timeout)
    return o.read().decode('utf-8', errors='replace')

# 上传新jiazhangtong.py
sftp = client.open_sftp()
sftp.put(
    '/Users/xiachaoqing/projects/openclaw_file/wechat_platform_patch/app/api/jiazhangtong.py',
    '/www/wwwroot/wechat_platform/app/api/jiazhangtong.py'
)
sftp.close()
print("后端上传完成")

# 重启
run("kill -9 $(pgrep -f 'uvicorn app.main') 2>/dev/null; sleep 1")
run("cd /www/wwwroot/wechat_platform && nohup /www/wwwroot/wechat_platform/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 2 --log-level info >> /www/wwwroot/wechat_platform/logs/app.log 2>&1 &")
time.sleep(4)
print("服务重启完成")

# 验证
r = run("curl -s 'http://127.0.0.1:8000/api/jzt/wx/jsconfig?url=https://go.xiachaoqing.com/jiazhangtong/'")
print("jsconfig:", "OK" if '"code":0' in r else "FAIL: "+r[:100])
client.close()
