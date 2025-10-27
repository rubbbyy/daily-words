# -*- coding: utf-8 -*-
"""
Daily Words by Rubby - Static Site Generator
"""

from pathlib import Path
import json
from vocab_data import CATEGORIES

TITLE = "Daily Words by Rubby"

def esc(s):
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


LOGO_A = r'''<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 96 96"><circle cx="48" cy="48" r="44" fill="#2563EB"/><text x="22" y="57" font-size="30" fill="#fff" font-weight="800">D</text><text x="49" y="57" font-size="30" fill="#fff" font-weight="800">W</text></svg>'''
LOGO_B = LOGO_A
LOGO_C = LOGO_A

ICON_SPK = '''
<svg width="20" height="20" viewBox="0 0 24 24" fill="none"
stroke="currentColor" stroke-width="2"
stroke-linecap="round" stroke-linejoin="round"
xmlns="http://www.w3.org/2000/svg">
<polygon points="5 9 9 9 13 5 13 19 9 15 5 15"></polygon>
<path d="M15 9.354c.776.91.776 2.382 0 3.292"></path>
<path d="M17.657 7.757c1.562 1.562 1.562 4.095 0 5.657"></path>
</svg>
'''


def build():

    site = Path(__file__).parent / "site"
    site.mkdir(exist_ok=True, parents=True)

    # Generate JSON for script.js
    data = []
    for cat, items in CATEGORIES.items():
        for zh, en, br, am, ex in items:
            data.append({
                "category": cat,
                "zh": zh,
                "en": en,
                "ipa_br": br,
                "ipa_am": am,
                "example": ex
            })

    (site / "data.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    # ✅ External JS reference
    html = f"""
<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{esc(TITLE)}</title>

<style>
body {{
    font-family:-apple-system,BlinkMacSystemFont;
    margin:0;
    background:#f0f4ff;
}}
.container {{
    max-width:1000px;
    margin:40px auto;
    padding:0 16px;
}}
.topbar {{
    display:flex;
    justify-content:space-between;
    align-items:center;
    margin-bottom:24px;
}}
.card {{
    background:white;
    border-radius:12px;
    padding:16px;
    margin-top:12px;
}}
.play {{
    display:inline-flex;
    align-items:center;
    gap:4px;
    border:1px solid #ccc;
    border-radius:16px;
    padding:4px 8px;
    cursor:pointer;
    font-size:14px;
}}
.word {{
    font-size:20px;
    font-weight:700;
    margin-bottom:6px;
}}
</style>
</head>

<body>
<div class="container">
    <div class="topbar">
        <div id="logo"></div>
        <select id="logoSel">
            <option value="A">A</option>
            <option value="B">B</option>
            <option value="C" selected>C</option>
        </select>
    </div>

    <h1>{esc(TITLE)}</h1>
    <input id="search" placeholder="Search（中文/English）" style="width:100%;padding:12px;font-size:18px"/>

    <div id="list"></div>
</div>

<script>
window.LOGO_A = `{LOGO_A}`;
window.LOGO_B = `{LOGO_B}`;
window.LOGO_C = `{LOGO_C}`;
window.ICON_SPK = `{ICON_SPK}`;
</script>

<script src="script.js"></script>
</body>
</html>
"""

    (site / "index.html").write_text(html, encoding="utf-8")
    print("✅ Build Success: site/index.html")


if __name__ == "__main__":
    build()
