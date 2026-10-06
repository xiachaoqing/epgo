#!/usr/bin/env python3
"""Apply an editorial manifest to the static sitemap without touching other URLs."""
import json
import re
import sys
from datetime import date
from pathlib import Path

if len(sys.argv) != 3:
    raise SystemExit("usage: update_editorial_sitemap.py MANIFEST SITEMAP")
manifest = json.loads(Path(sys.argv[1]).read_text())
path = Path(sys.argv[2])
text = path.read_text()
actions = {int(item["id"]): item["action"] for item in manifest["items"]}
seen = set()


def update(match):
    block = match.group(0)
    article_id = int(match.group(1))
    if article_id not in actions:
        return block
    seen.add(article_id)
    if actions[article_id] == "hide":
        return ""
    return re.sub(r"<lastmod>[^<]*</lastmod>",
                  "<lastmod>" + date.today().isoformat() + "</lastmod>",
                  block, count=1)


new_text = re.sub(
    r"  <url>\s*<loc>https://xiachaoqing\.com/[^<]*/(\d+)\.html</loc>.*?</url>\n",
    update, text, flags=re.S,
)
missing = set(actions) - seen
if missing:
    raise SystemExit("Sitemap entries missing: " + ", ".join(map(str, sorted(missing))))
path.write_text(new_text)
print(f"Updated {sum(a == 'rewrite' for a in actions.values())} and removed "
      f"{sum(a == 'hide' for a in actions.values())} article URLs")
