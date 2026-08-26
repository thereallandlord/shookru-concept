#!/usr/bin/env python3
"""Собирает полноценный статический сайт для GitHub Pages."""
import os, re, base64, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build import img, S

SITE = f"{S}/site"
BASE = "https://thereallandlord.github.io/shookru-concept"

PAGES = [
    ("index.html", "v6-quiet.html", None),   # заглушка, перезапишем ниже
]
VARIANTS = [
    # две страницы сайта — у каждой свой адрес, заголовок и превью
    ("index.html", "v6-quiet.html", "Шукру — халяльные платёжные решения",
     "Рассрочка без процентов и садака с открытой сметой. Один сервис — от покупки до пожертвования."),
    ("sadaka.html", "v6-quiet.html", "Садака — просто и прозрачно · Шукру",
     "112 сборов вместе с 39 фондами. У каждого сбора есть фонд, смета и срок. Комиссия сервиса — ноль."),
]

FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 40 40'%3E"
           "%3Cpath fill='%2307BC8E' fill-rule='evenodd' d='M20 40C8.954 40 0 31.046 0 20S8.954 0 20 0c2.02 0 3.97.3 "
           "5.808.858A16.5 16.5 0 0 0 23.5 20a16.5 16.5 0 0 0 2.308 8.39A19.94 19.94 0 0 1 20 40Z'/%3E%3C/svg%3E")

def wrap(body, title, desc, url, og="og-index.jpg"):
    """Оборачивает контент в полноценную страницу: кодировка, вьюпорт, превью для мессенджеров."""
    body = re.sub(r'<title>.*?</title>\s*', '', body, count=1, flags=re.S)
    return f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex,nofollow">
<link rel="icon" href="{FAVICON}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{BASE}/{og}">
<meta property="og:url" content="{url}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
</head>
<body>
{body}
</body>
</html>
"""

def build_one(src, out, title, desc):
    html = open(f"{S}/src/{src}", encoding='utf-8').read()
    html = re.sub(r'\{\{IMG:([a-z0-9_]+)\}\}', lambda m: img(m.group(1)), html)
    og = "og-sadaka.jpg" if "sadaka" in out else "og-index.jpg"
    page = wrap(html, title, desc, f"{BASE}/{out}", og)
    open(f"{SITE}/{out}", 'w', encoding='utf-8').write(page)
    return os.path.getsize(f"{SITE}/{out}") / 1024

if __name__ == '__main__':
    os.makedirs(SITE, exist_ok=True)
    total = 0
    for out, src, title, desc in VARIANTS:
        kb = build_one(src, out, title, desc); total += kb
        print(f"  {out:<11} {kb:6.0f} KB  {title}")

    open(f"{SITE}/robots.txt",'w').write("User-agent: *\nDisallow: /\n")
    open(f"{SITE}/.nojekyll",'w').write("")
    print(f"\nитого {total/1024:.1f} МБ в {SITE}")
