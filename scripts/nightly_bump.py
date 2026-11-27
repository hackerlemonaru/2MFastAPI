#!/usr/bin/env python3
"""毎晩の自動追従: 2FastAPI / MFastAPI の最新リリースを調べ、前回(upstream.json)と違えば記録を更新してパッチ版を1つ上げる。

標準ライブラリのみ。GH_TOKEN があれば使う。取得に失敗した項目は前回の値を残す(版は上げない)。
"""
import json
import os
import re
import urllib.request

ORG = "aon-co-jp"
REPOS = ["2FastAPI", "MFastAPI"]
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def latest(repo):
    h = {"User-Agent": "2mfastapi-nightly", "Accept": "application/vnd.github+json"}
    if os.environ.get("GH_TOKEN"):
        h["Authorization"] = "Bearer " + os.environ["GH_TOKEN"]
    with urllib.request.urlopen(urllib.request.Request("https://api.github.com/repos/%s/%s/releases/latest" % (ORG, repo), headers=h), timeout=20) as r:
        return json.loads(r.read().decode("utf-8"))["tag_name"]


def main():
    path = os.path.join(ROOT, "upstream.json")
    old = json.load(open(path)) if os.path.exists(path) else {}
    new = dict(old)
    for r in REPOS:
        try:
            new[r] = latest(r)
        except Exception as e:  # noqa: BLE001
            print("warn: %s: %s" % (r, e))
    if new == old:
        print("unchanged")
        return
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(new, fh, indent=1, sort_keys=True)
        fh.write("\n")
    if not old:  # first run only records the baseline
        print("baseline recorded")
        return
    for rel, pat in (("pyproject.toml", r'(?m)^version = "(\d+)\.(\d+)\.(\d+)"'), ("src/tomfastapi/__init__.py", r'__version__ = "(\d+)\.(\d+)\.(\d+)"')):
        p = os.path.join(ROOT, rel)
        s = open(p, encoding="utf-8").read()
        s = re.sub(pat, lambda m: m.group(0).replace("%s.%s.%s" % m.groups(), "%s.%s.%d" % (m.group(1), m.group(2), int(m.group(3)) + 1)), s, count=1)
        open(p, "w", encoding="utf-8", newline="\n").write(s)
    print("bumped:", old, "->", new)

