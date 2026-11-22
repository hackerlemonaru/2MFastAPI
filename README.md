# 2MFastAPI

**日本語**: Flask・Django(DRF を含む)・FastAPI で組まれたプロジェクトを、使っているライブラリの組み合わせ(SQLAlchemy・marshmallow・JWT・DRF・Flask-Login など)ごと **MFastAPI**(FastAPI 互換・Rust 高速化、`mfastapi.accelerate(app)`)へ自動変換するツール。Flask / Django の変換は [2FastAPI](https://github.com/aon-co-jp/2FastAPI) を土台にし、FastAPI のプロジェクトはコードを変えずに `run_mfastapi.py`(MFastAPI が無ければ素の FastAPI として動く)を足します。
**English**: Converts Flask, Django (incl. DRF) and FastAPI projects, in many library combinations (SQLAlchemy, marshmallow, JWT, DRF, Flask-Login ...), to **MFastAPI** (FastAPI-compatible, Rust-accelerated, `mfastapi.accelerate(app)`). Flask / Django conversion builds on [2FastAPI](https://github.com/aon-co-jp/2FastAPI); FastAPI projects keep their code and get a `run_mfastapi.py` launcher (plain FastAPI behaviour when MFastAPI is absent).

- 紹介・ダウンロード: https://easy-web.tokyo/2MFastAPI ・ デモ: https://easy-web.tokyo/2MFastAPI/demo/
- ライセンス / License: MIT

## 使い方 / Usage
```bash
pip install "tofastapi @ git+https://github.com/aon-co-jp/2FastAPI.git" .
2mfastapi scan  ./my-projects                  # Flask / Django / FastAPI を探す(ライブラリも表示) / list projects and libraries
2mfastapi convert ./proj -o ./proj-mfastapi    # 1つ変換 / convert one
2mfastapi auto  ./my-projects -o ./out         # 見つかった全部を変換 / convert everything found
uvicorn run_mfastapi:app --reload              # 変換後 / after conversion
```
MFastAPI は GitHub リリースのホイールで配布(PyPI 未公開): https://github.com/aon-co-jp/MFastAPI/releases 。未導入でも変換後のアプリは素の FastAPI として動きます。
MFastAPI ships as GitHub release wheels (not on PyPI). The converted app also runs as plain FastAPI without it.

## 対応する組み合わせ / Supported combinations (差分試験あり / differentially tested)
| 元 / Source | 変換 / Conversion |
|---|---|
| FastAPI + SQLAlchemy + Pydantic(+ JWT/passlib 等) | コードは無変更、`run_mfastapi.py` を追加。応答が元と一致することを試験 / unchanged code + launcher; responses verified identical |
| Flask + Flask-SQLAlchemy + marshmallow + Flask-JWT-Extended | 2FastAPI の互換層で変換(Flask が発行したトークンを変換後が受理) / via 2FastAPI shims |
| Django REST framework(`ModelViewSet`・`ModelSerializer`・`ViewSet`・router) | SQLAlchemy + pydantic の CRUD に変換 / converted to SQLAlchemy + pydantic CRUD |
| Flask(Login・Session・Blueprint ほか)、Django(View・TemplateView・render) | 2FastAPI の全機能 / everything 2FastAPI converts |

## 毎晩の自動バージョンアップ / Nightly auto-update
**日本語**: GitHub Actions が毎晩 02:47 JST に、最新の 2FastAPI(main)・MFastAPI(最新ホイール)・上流(Python / Flask / Django / FastAPI / Starlette)で全試験を実行します。失敗したら日付つきの issue を1件起こします。通って、かつ 2FastAPI か MFastAPI に新しいリリースが出ていれば、パッチ版を上げてリリースします(`upstream.json` に前回の版を記録、`scripts/nightly_bump.py`)。また `version-control` が本リポジトリのクローンの鮮度を見張り、easy-web.tokyo の紹介ページは `refresh_versions.py`(1時間ごと)で最新版を表示します。
**English**: GitHub Actions runs the full suite every night (02:47 JST) against the latest 2FastAPI (main), MFastAPI (latest wheel) and upstream (Python / Flask / Django / FastAPI / Starlette), opening one dated issue on failure. When it passes and 2FastAPI or MFastAPI has a new release, it bumps the patch version and publishes a release (`upstream.json`, `scripts/nightly_bump.py`). `version-control` watches the clone's freshness and the easy-web.tokyo page shows the latest versions via `refresh_versions.py` (hourly).

## 開発 / Development
WSL: `bash run-tests.sh`(`2FastAPI` を隣に置く / keep 2FastAPI checked out next to this repo)。Windows ネイティブでは libcst が無いためテストは WSL / Linux CI。
