# -*- coding: utf-8 -*-
"""
Daily Words by Rubby - Build Script
Generates static HTML page with vocabulary & pronunciation support
"""

from pathlib import Path
import json
from vocab_data import CATEGORIES

TITLE = "Daily Words by Rubby"

def esc(s):
    """Basic HTML escape"""
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# === Logos (A/B/C) ===
LOGO_A = r'''<svg xmlns="http://www.w3.org/2000/svg" width="96" height="96" viewBox="0 0 96 96"><defs><linearGradient id="gA" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3b82f6"/><stop offset="1" stop-color="#2563EB"/></linearGradient></defs><circle cx="48" cy="48" r="44" fill="url(#gA)"/><g fill="#fff" font-family="Inter, Arial, sans-serif" font-weight="800"><text x="22" y="57" font-size="30">D</text><text x="49" y="57" font-size="30">W</text></g></svg>'''

LOGO_B = r'''<svg xmlns="http://www.w3.org/2000/svg" width="96" height="96" viewBox="0 0 96 96"><defs><radialGradient id="gB" cx="30%" cy="20%" r="80%"><stop offset="0" stop-color="#60a5fa"/><stop offset="1" stop-color="#2563EB"/></radialGradient></defs><circle cx="48" cy="48" r="44" fill="url(#gB)"/><g fill="#fff" font-family="Nunito, Arial, sans-serif" font-weight="900"><text x="22" y="57" font-size="30">D</text><text x="49" y="57" font-size="30">W</text></g><path d="M20 32c8-6 18-9 28-9 10 0 20 3 28 9" fill="none" stroke="#ffffff" stroke-opacity=".25" stroke-width="4" stroke-linecap="round"/></svg>'''

LOGO_C = r'''<svg xmlns="http://www.w3.org/2000/svg" width="96" height="96" viewBox="0 0 96 96"><defs><linearGradient id="gC" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#60a5fa"/><stop offset="1" stop-color="#2563EB"/></linearGradient></defs><circle cx="48" cy="48" r="44" fill="url(#gC)"/><g fill="#fff" font-family="Nunito, Arial, sans-serif" font-weight="900"><text x="20" y="56" font-size="30">D</text><text x="44" y="56" font-size="30">W</text></g><circle cx="66" cy="62" r="8" fill="none" stroke="#fff" stroke-width="3"/><rect x="73" y="68" width="10" height="4" rx="2" fill="#fff" transform="rotate(35 78 70)"/></svg>'''
# ==== Speaker SVG ====
ICON_SPK = '''
<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
 stroke-linecap="round" stroke-linejoin="round" xmlns="http://www.w3.org/2000/svg">
<polygon points="5 9 9 9 13 5 13 19 9 15 5 15"></polygon>
<path d="M15 9.354c.776.91.776 2.382 0 3.292"></path>
<path d="M17.657 7.757c1.562 1.562 1.562 4.095 0 5.657"></path>
</svg>
'''

def build():
    site = Path(__file__).parent / "site"
    site.mkdir(exist_ok=True, parents=True)

    # flatten items for JS consumption
    data = []
    for cat, items in CATEGORIES.items():
        for zh, en, br, am, ex in items:
            data.append({
                "category": cat, "zh": zh, "en": en,
                "ipa_br": br, "ipa_am": am, "example": ex
            })

    # write JSON for JS
    (site / "data.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    html = f"""
<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>{esc(TITLE)}</title>
<style>
:root {{
  --brand:#2563EB;
  --bg:#f5f8ff;
  --card:#fff;
  --text:#111;
  --muted:#6b7280;
}}
body {{
  font-family:-apple-system,BlinkMacSystemFont,"SF Pro","Segoe UI",Arial;
  margin:0;background:var(--bg);color:var(--text);
}}
.container {{ max-width:1000px; margin:40px auto; padding:0 16px; }}
.topbar {{ display:flex; justify-content:space-between; align-items:center; margin-bottom:24px; }}
.logo-btn {{ width:48px; height:48px; cursor:pointer; }}
h1 {{ font-size:30px; margin:0; line-height:1.1; font-weight:800; }}
.search-box input {{
  width:100%; padding:14px 18px; font-size:18px;
  border:1px solid #e5e7eb; border-radius:12px;
  outline:none;
}}
.pill {{
  background:#e5edff; color:#1e3a8a; border-radius:16px;
  padding:6px 12px; font-size:14px;
  margin-right:4px;
}}
.card {{
  background:var(--card);
  border-radius:12px;
  padding:16px;
  margin-top:12px;
  box-shadow:0 2px 8px rgba(0,0,0,0.05);
}}
.word {{
  display:flex;
  justify-content:space-between;
  font-size:20px; font-weight:700;
  margin-bottom:6px;
}}
.play {{
  cursor:pointer; display:flex; align-items:center;
  border:1px solid #d1d5db;
  border-radius:16px;
  padding:4px 10px;
  font-size:14px;
  gap:3px;
}}
</style>
</head>
<body>
<div class="container">
  <div class="topbar">
    <div id="logo"></div>
    <div style="display:flex;align-items:center;gap:8px;">
      <label>Logo:</label>
      <select id="logoSel">
        <option value="A">A · DW Geo(默认)</option>
        <option value="B">B · DW Glass</option>
        <option value="C" selected>C · Focus</option>
      </select>
    </div>
  </div>
  <h1>{esc(TITLE)}</h1>
  <div class="search-box">
    <input id="search" placeholder="Search（中文/English，如 apple / 苹果 / towel）"/>
  </div>
"""
  <div id="list"></div>
</div>

<script>
// Load data
let DATA = [];
fetch("data.json")
  .then(r => r.json())
  .then(arr => {
    DATA = arr;
    render();
  });

const list = document.getElementById("list");
const searchInput = document.getElementById("search");
const logoSel = document.getElementById("logoSel");
const logoEl = document.getElementById("logo");

// Load logo from localStorage
function setLogo(){
  const val = localStorage.getItem("DW_LOGO") || "C";
  logoSel.value = val;
  logoEl.innerHTML = (val==="A"? `{{LOGO_A}}` :
                      val==="B"? `{{LOGO_B}}` :
                                 `{{LOGO_C}}`);
}
setLogo();

// Play pronunciation
function play(text, accent){
  if (!text) return;
  const url = `https://dict.youdao.com/dictvoice?audio=${encodeURIComponent(text)}&type=${accent==="br"?1:2}`;
  new Audio(url).play();
}

// Render list
function render(){
  const q = searchInput.value.trim().toLowerCase();
  const res = DATA.filter(it =>
    it.en.toLowerCase().includes(q) ||
    it.zh.includes(q)
  );
  list.innerHTML = res.map(it => `
    <div class="card">
      <div class="word">
        <span>${it.en} — ${it.zh}</span>
      </div>
      <div style="display:flex;gap:10px;margin-top:4px;">
        <div class="play" onclick="play('${it.en}','br')">
          ${`{{ICON_SPK}}`} BrE
        </div>
        <div class="play" onclick="play('${it.en}','am')">
          ${`{{ICON_SPK}}`} AmE
        </div>
      </div>
      <div style="margin-top:10px; font-size:14px;">
        <span style="color:var(--muted);">Example:
        </span> ${it.example || ""}
      </div>
    </div>
  `).join("");
}

// Bind events
searchInput.addEventListener("input", render);
logoSel.addEventListener("change", () => {
  localStorage.setItem("DW_LOGO", logoSel.value);
  setLogo();
});
</script>

"""
    # —— 结束 HTML，补齐闭合标签 ——
    html += """
</body>
</html>
"""

    # —— 将占位符替换成真正的 SVG ——
    html = (html
            .replace("{{LOGO_A}}", LOGO_A)
            .replace("{{LOGO_B}}", LOGO_B)
            .replace("{{LOGO_C}}", LOGO_C)
            .replace("{{ICON_SPK}}", ICON_SPK))

    # —— 写入构建产物 ——
    site = Path(__file__).parent / "site"
    site.mkdir(exist_ok=True, parents=True)
    (site / "index.html").write_text(html, encoding="utf-8")
    print("✅ Built site/index.html")


if __name__ == "__main__":
    build()
