#!/usr/bin/env python3
"""webpage/index.html と webpage/demo/index.html を、2FastAPI の紹介ページ(テンプレート)から作る。

使い方: make_pages.py <2FastAPI の webpage ディレクトリ> <出力 webpage ディレクトリ>
ページはダウンロード専用(ブラウザ上で動かす・入力する・アップロードする機能は置かない)。
"""
import os
import re
import sys

DESC = {
    "ja": "Flask・Django・FastAPI で組まれたプロジェクトを、使っているライブラリの組み合わせ(SQLAlchemy・marshmallow・JWT・DRF など)ごと、MFastAPI(FastAPI互換・Rust高速化)へ自動変換するツール。毎晩、最新の 2FastAPI と MFastAPI に追従します。",
    "en": "A tool that converts Flask, Django and FastAPI projects, in many library combinations (SQLAlchemy, marshmallow, JWT, DRF and more), to MFastAPI (FastAPI-compatible, Rust-accelerated). It follows the latest 2FastAPI and MFastAPI every night.",
    "zh-CN": "将 Flask、Django 和 FastAPI 项目(包括 SQLAlchemy、marshmallow、JWT、DRF 等多种库组合)自动转换为 MFastAPI(兼容 FastAPI,Rust 加速)的工具。每晚自动跟进最新的 2FastAPI 和 MFastAPI。",
    "zh-TW": "將 Flask、Django 與 FastAPI 專案(含 SQLAlchemy、marshmallow、JWT、DRF 等多種函式庫組合)自動轉換為 MFastAPI(相容 FastAPI,以 Rust 加速)的工具。每晚自動跟進最新的 2FastAPI 與 MFastAPI。",
    "ko": "Flask, Django, FastAPI로 만든 프로젝트를 SQLAlchemy·marshmallow·JWT·DRF 등 다양한 라이브러리 조합 그대로 MFastAPI(FastAPI 호환, Rust 가속)로 자동 변환하는 도구입니다. 매일 밤 최신 2FastAPI와 MFastAPI를 따라갑니다.",
    "it": "Uno strumento che converte automaticamente progetti Flask, Django e FastAPI, in molte combinazioni di librerie (SQLAlchemy, marshmallow, JWT, DRF e altre), in MFastAPI (compatibile con FastAPI, accelerato in Rust). Ogni notte segue le ultime versioni di 2FastAPI e MFastAPI.",
    "fr": "Un outil qui convertit automatiquement des projets Flask, Django et FastAPI, dans de nombreuses combinaisons de bibliothèques (SQLAlchemy, marshmallow, JWT, DRF et d&#x27;autres), en MFastAPI (compatible FastAPI, accéléré en Rust). Chaque nuit, il suit les dernières versions de 2FastAPI et de MFastAPI.",
    "de": "Ein Werkzeug, das Flask-, Django- und FastAPI-Projekte in vielen Bibliothekskombinationen (SQLAlchemy, marshmallow, JWT, DRF und mehr) automatisch in MFastAPI (FastAPI-kompatibel, mit Rust beschleunigt) umwandelt. Jede Nacht folgt es den neuesten Versionen von 2FastAPI und MFastAPI.",
    "ru": "Инструмент, автоматически преобразующий проекты Flask, Django и FastAPI, в разных сочетаниях библиотек (SQLAlchemy, marshmallow, JWT, DRF и других), в MFastAPI (совместим с FastAPI, ускорен на Rust). Каждую ночь он следует за последними версиями 2FastAPI и MFastAPI.",
    "uk": "Інструмент, що автоматично перетворює проєкти Flask, Django і FastAPI, у різних поєднаннях бібліотек (SQLAlchemy, marshmallow, JWT, DRF та інших), на MFastAPI (сумісний із FastAPI, прискорений на Rust). Щоночі він слідує за найновішими версіями 2FastAPI і MFastAPI.",
    "fa": "ابزاری که پروژه‌های Flask و Django و FastAPI را با ترکیب‌های گوناگون کتابخانه‌ها (SQLAlchemy، marshmallow، JWT، DRF و جز آن) به‌طور خودکار به MFastAPI (سازگار با FastAPI و شتاب‌گرفته با Rust) تبدیل می‌کند. هر شب آخرین نسخه‌های 2FastAPI و MFastAPI را دنبال می‌کند.",
    "ar": "أداة تحوّل تلقائيًا مشاريع Flask وDjango وFastAPI، بتوليفات متعددة من المكتبات (SQLAlchemy وmarshmallow وJWT وDRF وغيرها)، إلى MFastAPI (متوافق مع FastAPI ومسرَّع بـ Rust). تتبع كل ليلة أحدث إصدارات 2FastAPI وMFastAPI.",
    "he": "כלי שממיר אוטומטית פרויקטים של Flask, Django ו-FastAPI, בשילובי ספריות רבים (SQLAlchemy, marshmallow, JWT, DRF ועוד), ל-MFastAPI (תואם FastAPI, מואץ ב-Rust). בכל לילה הוא עוקב אחר הגרסאות האחרונות של 2FastAPI ושל MFastAPI.",
}


def build(src: str) -> str:
    s = src
    s = s.replace("https://github.com/aon-co-jp/2FastAPI-VSC/releases/latest", "https://github.com/aon-co-jp/2FastAPI/releases/latest")
    s = re.sub(r'<a class="btn alt" href="https://github.com/aon-co-jp/2FastAPI/releases/latest" rel="noopener">2FastAPI-VSC</a>', '<a class="btn alt" href="https://github.com/aon-co-jp/2FastAPI/releases/latest" rel="noopener">2FastAPI</a>', s)
    s = s.replace("https://github.com/aon-co-jp/2FastAPI\"", "https://github.com/aon-co-jp/2MFastAPI\"")
    # the main button points to the 2MFastAPI release; the 2FastAPI button stays as a second link
    s = s.replace('<a class="btn" href="https://github.com/aon-co-jp/2FastAPI/releases/latest"', '<a class="btn" href="https://github.com/aon-co-jp/2MFastAPI/releases/latest"')
    s = s.replace("<h1>2FastAPI</h1>", "<h1>2MFastAPI</h1>").replace("<title>2FastAPI -", "<title>2MFastAPI -")

    def sec(m):
        lang = m.group(1)
        body = re.sub(r"<p>.*?</p>", "<p>" + DESC[lang] + "</p>", m.group(0), count=1, flags=re.S)
        return body

    s = re.sub(r'<section id="([\w-]+)" lang="[\w-]+" dir="\w+">.*?</section>', sec, s, flags=re.S)
    s = re.sub(r'(<meta name="description" content=")[^"]*"', lambda m: m.group(1) + DESC["en"] + '"', s, count=1)
    return s


def main():
    tpl, out = sys.argv[1], sys.argv[2]
    for rel in ("index.html", os.path.join("demo", "index.html")):
        with open(os.path.join(tpl, rel), encoding="utf-8") as fh:
            new = build(fh.read())
        dest = os.path.join(out, rel)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(new)
        print("wrote", dest, len(new))


if __name__ == "__main__":
    main()
