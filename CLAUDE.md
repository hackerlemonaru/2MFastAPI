# 2MFastAPI 開発方針 / Development notes

**日本語**: 共通ルールは [`open-raid-z/CLAUDE.md`](https://github.com/aon-co-jp/open-raid-z) と [`runo`](https://github.com/aon-co-jp/runo) の `CLAUDE.md` を参照。チャットは日本語のみ。確認なしで開発・TEST・DEBUG・commit・push。heredocでバックスラッシュ・三連引用符を含むコードを書かない(Writeツールを使う)。REST を新設しない方針は本ツールの変換結果には関係しない(変換先は元のアプリの API をそのまま保つ)。
**English**: shared rules live in `open-raid-z/CLAUDE.md` and `runo/CLAUDE.md`. Chat in Japanese only. Develop, test, debug, commit and push without asking. Do not write code with backslashes or triple quotes through bash heredocs (use the Write tool). The "no new REST" policy does not apply to converted output (the converted app keeps its original API).

## 状態 / Status
- 日本語: v0.1.0。Flask / Django / DRF は 2FastAPI(`tofastapi`)で変換し、FastAPI は無変更+`run_mfastapi.py`。差分試験5件(FastAPI+SQLAlchemy+Pydantic、Flask+SQLAlchemy+marshmallow+JWT、DRF ModelViewSet、CLI)を WSL(MFastAPI 0.2.6 の Rust 版を入れて)で確認。毎晩のCI(最新の2FastAPI/MFastAPI/上流で再試験、新版があればパッチ版を自動リリース)あり。
- English: v0.1.0. Flask / Django / DRF go through 2FastAPI (`tofastapi`); FastAPI projects are kept as-is plus `run_mfastapi.py`. 5 differential tests pass in WSL with the MFastAPI 0.2.6 Rust backend. Nightly CI re-tests against the latest 2FastAPI / MFastAPI / upstream and auto-releases a patch version when upstream has a new release.

## 構成 / Layout
`src/tomfastapi/{scan,convert,cli}.py`、`examples/`(試験用サンプル)、`scripts/nightly_bump.py`(毎晩の版上げ)・`scripts/make_pages.py`(紹介ページ生成)、`webpage/`(easy-web.tokyo の `/2MFastAPI` と `/demo`)、`upstream.json`。

## 未了 / Open
- 日本語: PyPI 公開(所有者の認証が必要。2FastAPI・MFastAPI も未公開のため依存は GitHub 参照)、FastAPI 側の「組み合わせ」ごとの個別変換(現状は無変更で動かす)、macOS/Windows の CI。
- English: PyPI publication (needs the owner's credentials; the dependency is a GitHub reference because 2FastAPI/MFastAPI are not on PyPI either), per-combination rewrites on the FastAPI side (today they run unchanged), macOS/Windows CI.
