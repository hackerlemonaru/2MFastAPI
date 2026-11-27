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


