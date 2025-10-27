# -*- coding: utf-8 -*-
from pathlib import Path
import json
from vocab_data import CATEGORIES

TITLE = "Daily Words by Rubby"

def esc(s):
    return (s or "").replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

# ✅ Logo A/B/C（三套 DW 圆形科技 Logo，均为 SVG 矢量）
LOGO_A = r'''<svg xmlns="http://www.w3.org/2000/svg" width="96" height="96" viewBox="0 0 96 96"><defs><linearGradient id="gA" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3b82f6"/><stop offset="1" stop-color="#2563EB"/></linearGradient></defs><circle cx="48" cy="48" r="44" fill="url(#gA)"/><g fill="#fff" font-family="Inter, Arial, sans-serif" font-weight="800"><text x="22" y="57" font-size="30">D</text><text x="49" y="57" font-size="30">W</text></g></svg>'''

LOGO_B = r'''<svg xmlns="http://www.w3.org/2000/svg" width="96" height="96" viewBox="0 0 96 96"><defs><radialGradient id="gB" cx="30%" cy="20%" r="80%"><stop offset="0" stop-color="#60a5fa"/><stop offset="1" stop-color="#2563EB"/></radialGradient></defs><circle cx="48" cy="48" r="44" fill="url(#gB)"/><g fill="#fff" font-family="Nunito, Arial, sans-serif" font-weight="900"><text x="22" y="57" font-size="30">D</text><text x="49" y="57" font-size="30">W</text></g><path d="M20 32c8-6 18-9 28-9 10 0 20 3 28 9" fill="none" stroke="#ffffff" stroke-opacity=".25" stroke-width="4" stroke-linecap="round"/></svg>'''

LOGO_C = r'''<svg xmlns="http://www.w3.org/2000/svg" width="96" height="96" viewBox="0 0 96 96"><defs><linearGradient id="gC" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#60a5fa"/><stop offset="1" stop-color="#2563EB"/></linearGradient></defs><circle cx="48" cy="48" r="44" fill="url(#gC)"/><g fill="#fff" font-family="Nunito, Arial, sans-serif" font-weight="900"><text x="20" y="56" font-size="30">D</text><text id="w" x="44" y="56" font-size="30">W</text></g><circle cx="66" cy="62" r="8" fill="none" stroke="#fff" stroke-width="3"/><rect x="73" y="68" width="10" height="4" rx="2" fill="#fff" transform="rotate(35 78 70)"/></svg>'''

def build():
    site = Path(__file__).parent / "site"
    site.mkdir(exist_ok=True, parents=True)

    data = []
    for cat, items in CATEGORIES.items():
        for zh, en, br, am, ex in items:
            data.append({"category": cat, "zh": zh, "en": en, "ipa_br": br, "ipa_am": am, "example": ex})

    html = generate_html(TITLE, data, list(CATEGORIES.keys()))
    (site / "index.html").write_text(html, encoding="utf-8")
    print("✅ Built site/index.html")

def generate_html(title, data, cats):
    checks = "".join([
        f'<label class="pill"><input type="checkbox" class="cat-filter" value="{esc(c)}" checked>{esc(c)}</label>'
        for c in cats
    ])

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{esc(title)}</title>
<link id="favicon" rel="icon" type="image/svg+xml" href="">

<style>
:root{{--bg:#f6f9ff;--card:#fff;--text:#111;--muted:#6b7280;--brand:#2563EB}}
*{{box-sizing:border-box}} body{{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Arial; 
background:linear-gradient(180deg,#eaf2ff,#ffffff 60%)}}
.container{{max-width:1000px;margin:40px auto;padding:0 16px}}
.card{{background:var(--card);border-radius:16px;padding:24px;
box-shadow:0 10px 30px rgba(0,0,0,.08)}}
.topbar{{display:flex;gap:12px;align-items:center;justify-content:space-between;margin-bottom:14px}}
.brand{{display:flex;gap:10px;align-items:center}}
.brand svg{{width:32px;height:32px;display:block}}
.brand-title{{font-weight:800;letter-spacing:.2px;font-size:20px}}
.logo-chooser{{display:flex;gap:8px;align-items:center}}
.small{{font-size:13px;color:#64748b}}
.search{{width:100%;height:42px;padding:0 12px;font-size:16px;border:1px solid #e5e7eb;border-radius:10px}}
.filters{{display:flex;gap:10px;flex-wrap:wrap;justify-content:flex-end}}
.pill{{display:flex;align-items:center;padding:6px 10px;border-radius:999px;background:#eff6ff;color:#1d4ed8;
border:1px solid #bfdbfe;font-size:14px}}
.list{{margin:8px 0 0;padding:0;list-style:none}} .item{{border-bottom:1px solid #f1f5f9;padding:10px 0}}
.summary{{display:flex;gap:8px;align-items:center;justify-content:space-between;cursor:pointer}}
.word{{font-weight:700}} .count{{margin-top:6px;color:#64748b;font-size:14px}}
.details{{margin-top:8px;color:#111;line-height:1.6}}
.ipa{{background:#f8fafc;border-radius:8px;padding:8px;border:1px solid #eef2f7;margin-bottom:6px}}
.btn{{height:40px;padding:0 14px;border:none;border-radius:10px;background:var(--brand);color:#fff}}
</style>

</head>
<body>

<div class="container">
<div class="card">

  <div class="topbar">
    <div class="brand">
      <span id="logo-slot"></span>
      <div class="brand-title">{esc(title)}</div>
    </div>

    <div class="logo-chooser">
      <span class="small">Logo：</span>
      <select id="logoSelect">
        <option value="C">C · Focus(默认)</option>
        <option value="B">B · Glass</option>
        <option value="A">A · Geo</option>
      </select>
      <button id="export" class="btn">Export</button>
    </div>
  </div>

  <input id="search" class="search" type="search" placeholder="Search（中文/English）">
  <div class="filters">{checks}</div>
  <div class="count" id="count"></div>
  <ul id="list" class="list"></ul>

</div>
</div>

<script>
const RAW = {json.dumps(data, ensure_ascii=False)};
const list = document.getElementById('list');
const search = document.getElementById('search');
const checks = [...document.querySelectorAll('.cat-filter')];
const countEl = document.getElementById('count');
const exportBtn = document.getElementById('export');
const logoSlot = document.getElementById('logo-slot');
const logoSelect = document.getElementById('logoSelect');
const favicon = document.getElementById('favicon');

const LOGOS = {{
  A:`{LOGO_A}`, B:`{LOGO_B}`, C:`{LOGO_C}`
}};

function svgToDataUrl(svg) {{
  return "data:image/svg+xml;charset=utf-8," +
    encodeURIComponent(svg).replace(/'/g,"%27").replace(/"/g,"%22");
}}

function setLogo(which) {{
  const svg = LOGOS[which] || LOGOS.C;
  logoSlot.innerHTML = svg;
  favicon.href = svgToDataUrl(svg);
  localStorage.setItem('dw_logo', which);
  logoSelect.value = which;
}}

function escapeHtml(s){{return String(s).replaceAll('&','&amp;')
.replaceAll('<','&lt;').replaceAll('>','&gt;');}}

function apply(){{
  const kw = search.value.trim().toLowerCase();
  const chosen = new Set(checks.filter(c=>c.checked).map(c=>c.value));
  const filtered = RAW.filter(it =>
    chosen.has(it.category) &&
    (!kw || it.en.toLowerCase().includes(kw) || it.zh.includes(kw))
  );
  render(filtered);
}}

function render(items){{
  list.innerHTML = items.map(it => `
    <li class="item">
      <details>
        <summary class="summary">
          <span><span class="word">${{escapeHtml(it.en)}}</span> — ${{escapeHtml(it.zh)}}</span>
          <span class="small">click to expand</span>
        </summary>
        <div class="details">
          <div class="ipa"><b>BrE</b> ${{escapeHtml(it.ipa_br)}} | <b>AmE</b> ${{escapeHtml(it.ipa_am)}}</div>
          <b>Example:</b> ${{escapeHtml(it.example)}}
        </div>
      </details>
    </li>`).join('');
  countEl.textContent = `Showing ${{items.length}} / ${{RAW.length}} words`;
}}

exportBtn.onclick = () => {{
  let lines = ["Category,Chinese,English,IPA_BrE,IPA_AmE,Example"];
  list.querySelectorAll('details').forEach(det => {{
    const en = det.querySelector('.word').innerText;
    const zh = det.querySelector('summary span').innerText.split('—')[1].trim();
    const details = det.querySelector('.details');
    const ipa = details.querySelector('.ipa').innerText.replace(/\s+/g,' ');
    const example = details.innerText.split('Example:')[1].trim();
    lines.push(`"daily","${{zh}}","${{en}}","${{ipa}}","${{example}}"`);
  }});
  const blob = new Blob([lines.join('\\n')], {{type:"text/csv"}});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a'); a.href = url; a.download = "daily_words.csv";
  a.click(); URL.revokeObjectURL(url);
}};

search.oninput = apply;
checks.forEach(c => c.onchange = apply);

setLogo(localStorage.getItem('dw_logo') || 'C'); // ✅ 默认：C放大镜版
apply();
</script>

</body>
</html>"""

if __name__ == "__main__":
    build()
