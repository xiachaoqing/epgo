import paramiko, time

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('39.105.154.244', 22, 'root', 'Xia07090218', timeout=15)

def run(cmd, timeout=30):
    _, o, e = client.exec_command(cmd, timeout=timeout)
    return o.read().decode('utf-8', errors='replace')

# 上传新版jiazhangtong.py
print("=== 上传 jiazhangtong.py ===")
sftp = client.open_sftp()
sftp.put(
    '/Users/xiachaoqing/projects/openclaw_file/wechat_platform_patch/app/api/jiazhangtong.py',
    '/www/wwwroot/wechat_platform/app/api/jiazhangtong.py'
)
sftp.close()
print("上传完成")

# 强杀+重启uvicorn
print("=== 重启 uvicorn ===")
run("kill -9 $(pgrep -f 'uvicorn app.main') 2>/dev/null; sleep 1")
run(
    "cd /www/wwwroot/wechat_platform && "
    "nohup /www/wwwroot/wechat_platform/venv/bin/uvicorn app.main:app "
    "--host 0.0.0.0 --port 8000 --workers 2 --log-level info "
    ">> /www/wwwroot/wechat_platform/logs/app.log 2>&1 &"
)
time.sleep(4)

# 验证
print("=== 验证接口 ===")
print("jsconfig:", run("curl -s 'http://127.0.0.1:8000/api/jzt/wx/jsconfig?url=https://go.xiachaoqing.com/jiazhangtong/' | python3 -c \"import sys,json; d=json.load(sys.stdin); print('OK appId='+d.get('appId',''))\" 2>&1"))

# 测试JSAPI下单（无openid会报错，但至少不是NOAUTH了）
r = run("""curl -s -X POST http://127.0.0.1:8000/api/jzt/order/create \
  -H 'Content-Type: application/json' \
  -d '{"plan_id":"trial","phone":"13500112288","grade":"","openid":"","trade_type":"JSAPI"}'""")
print("order/create(无openid):", r[:200])

# 测试带openid（用测试openid）
r = run("""curl -s -X POST http://127.0.0.1:8000/api/jzt/order/create \
  -H 'Content-Type: application/json' \
  -d '{"plan_id":"trial","phone":"13500112299","grade":"","openid":"oTestOpenID12345","trade_type":"JSAPI"}'""")
print("order/create(有openid):", r[:300])

print("=== 进程确认 ===")
print(run("ps aux | grep 'uvicorn app.main' | grep -v grep"))
client.close()
