#!/usr/bin/env python3
"""Собирает самодостаточный HTML: подставляет data-URI картинок и реальные данные сборов."""
import json, base64, re, sys, os
S = os.path.dirname(os.path.abspath(__file__))

def datauri(path):
    ext = os.path.splitext(path)[1].lower()
    mime = {'.webp':'image/webp','.jpg':'image/jpeg','.jpeg':'image/jpeg','.png':'image/png','.svg':'image/svg+xml'}[ext]
    with open(path,'rb') as f:
        return f"data:{mime};base64,{base64.b64encode(f.read()).decode()}"

CACHE = {}
def img(token):                      # token: "f01_c" / "f01_h"
    if token not in CACHE:
        CACHE[token] = datauri(f"{S}/assets/web/{token}.webp")
    return CACHE[token]

def build(src, out):
    html = open(f"{S}/src/{src}", encoding='utf-8').read()
    html = re.sub(r'\{\{IMG:([a-z0-9_]+)\}\}', lambda m: img(m.group(1)), html)
    with open(f"{S}/dist/{out}", 'w', encoding='utf-8') as f:
        f.write(html)                                    # для артефакта — без head-тегов
    with open(f"{S}/dist/local-{out}", 'w', encoding='utf-8') as f:
        f.write('<!doctype html><meta charset="utf-8">'
                '<meta name="viewport" content="width=device-width,initial-scale=1">\n' + html)
    kb = os.path.getsize(f"{S}/dist/{out}")/1024
    n = len(re.findall(r'data:image', html))
    print(f"✓ {out}  {kb:,.0f} KB  ({n} картинок встроено)".replace(',',' '))
    if kb > 15000: print("  ⚠ близко к лимиту артефакта 16 МБ")

if __name__ == '__main__':
    for a in sys.argv[1:]:
        build(a, a)
