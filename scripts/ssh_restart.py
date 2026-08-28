import paramiko, time

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('39.105.154.244', 22, 'root', 'Xia07090218', timeout=15)

def run(cmd, timeout=30):
    _, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    return stdout.read().decode('utf-8', errors='replace'), stderr.read().decode('utf-8', errors='replace')

# 强杀所有uvicorn
print("=== 强杀 uvicorn ===")
o, e = run("kill -9 $(pgrep -f 'uvicorn app.main') 2>/dev/null; sleep 1; pgrep -f 'uvicorn app.main' || echo 'all killed'")
print(o)

# 重新启动
print("=== 重新启动 ===")
o, e = run(
    "cd /www/wwwroot/wechat_platform && "
    "source .env 2>/dev/null; "
    "nohup /www/wwwroot/wechat_platform/venv/bin/uvicorn app.main:app "
    "--host 0.0.0.0 --port 8000 --workers 2 --log-level info "
    ">> /www/wwwroot/wechat_platform/logs/app.log 2>&1 & echo $!"
)
print("新PID:", o.strip())

time.sleep(4)

# 验证进程
o, e = run("ps aux | grep 'uvicorn app.main' | grep -v grep")
print("进程:", o[:400])

# 测试新接口
print("=== 测试 wx/jsconfig ===")
o, e = run("curl -s 'http://127.0.0.1:8000/api/jzt/wx/jsconfig?url=https://go.xiachaoqing.com/jiazhangtong/'")
print("响应:", o[:300])

# 测试创建订单
print("=== 测试 order/create ===")
o, e = run("""curl -s -X POST http://127.0.0.1:8000/api/jzt/order/create \
  -H 'Content-Type: application/json' \
  -d '{"plan_id":"trial","phone":"13500998877","grade":"","trade_type":"MWEB"}'""")
print("响应:", o[:500])

client.close()
