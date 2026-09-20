# EPGO 多平台媒体服务

这里的 compose 配置复用 [Cobalt](https://github.com/imputnet/cobalt) 的自托管 API，用于处理用户主动提交的公开媒体链接。当前站点通过 `/epgo/media-api.php` 代理调用，Cobalt 只监听网站服务器本机的 `127.0.0.1:9000`。

部署前在服务器生成 `keys.json`，不要把真实密钥提交到 Git：

```bash
mkdir -p /opt/epgo-cobalt
cd /opt/epgo-cobalt
python3 - <<'PY'
import secrets
from pathlib import Path
Path('media-api-key.txt').write_text(secrets.token_urlsafe(32) + '\n')
PY
python3 - <<'PY'
import json, pathlib
key = pathlib.Path('media-api-key.txt').read_text().strip()
pathlib.Path('keys.json').write_text(json.dumps({key: {'name': 'epgo-web', 'limit': 6}}, ensure_ascii=False))
PY
```

实际部署还要把同一把 API key 写入站点目录的 `.media-api-key`（权限 600），并为该精确路径配置 Nginx 404；PHP 7.2 受 `open_basedir` 限制，不能从站点目录外读取。媒体只处理用户拥有或已获授权的内容；临时下载地址和缓存时长由 Cobalt 配置控制。Compose 不启用根文件系统只读模式，因为 Cobalt 的 node 用户需要监听密钥文件变化；密钥文件仍以只读挂载、600 权限和本机端口隔离保护。

Cobalt API 采用 AGPL-3.0。若后续修改并对外提供网络服务，需要保留原项目署名、许可证和对应源码提供方式。
