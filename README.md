# -*- coding: utf-8 -*-
from pathlib import Path
import json
from vocab_data import CATEGORIES

TITLE = "Daily Words by Rubby"

def esc(s):
    return (s or "").replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

# 三套 Logo（圆形 + 科技蓝 #2563EB），均为纯 SVG 矢量，可任意缩放
# A: DW Geo（几何切割感）
LOGO_A = r'''<svg xmlns="http://www.w3.org/2000/svg" width="96" height="96" viewBox="0 0 96 96">
  <defs>
    <linearGradient id="gA" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#3b82f6"/><stop offset="1" stop-color="#2563EB"/>
    </linearGradient>
  </defs>
  <circle cx="48" cy="48" r="44" fill="url(#gA)"/>
  <g fill="#fff" font-family="Inter, Arial, sans-serif" font-weight="800">
    <path d="M22 31h17c10 0 17 7 17 17s-7 17-17 17H22V31zm12 10v14h5c4 0 7-3 7-7s-3-7-7-7h-5z"/>
    <path d="M52 31h12l8 28 8-28h12l-12 34H64L52 31z" transform="scale(.7) translate(40 26)" />
  </g>
</svg>'''

# B: DW Glass（圆润拟物、扁平高光） ※你选的“方向B”的现代扁平款
LOGO_B = r'''<svg xmlns="http://www.w3.org/2000/svg" width="96" height="96" viewBox="0 0 96 96">
  <defs>
    <radialGradient id="gB" cx="30%" cy="20%" r="80%">
      <stop offset="0" stop-color="#60a5fa"/><stop offset="1" stop-color="#2563EB"/>
    </radialGradient>
  </defs>
  <circle cx="48" cy="48" r="44" fill="url(#gB)"/>
  <g fill="#fff" font-family="Nunito, Arial, sans-serif" font-weight="900">
    <text x="22" y="57" font-size="30" letter-spacing="1">D</text>
    <text x="49" y="57" font-size="30" letter-spacing="1">W</text>
  </g>
  <path d="M20 32c8-6 18-9 28-9 10 0 20 3 28 9" fill="none" stroke="#ffffff" stroke-opacity=".25" stroke-width="4" stroke-linecap="round"/>
</svg>'''

# C: DW Focus（放大镜融合：W 右下角延伸镜柄，强调“查词”寓意）— 默认
LOGO_C = r'''<svg xmlns="http://www.w3.org/2000/svg" width="96" height="96" viewBox="0 0 96 96">
  <defs>
    <linearGradient id="gC" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#60a5fa"/><stop offset="1" stop-color="#2563EB"/>
    </linearGradient>
  </defs>
  <circle cx="48" cy="48" r="44" fill="url(#gC)"/>
  <g fill="#fff" font-family="Nunito, Arial, sans-serif" font-weight="900">
    <text x="20" y="56" font-size="30">D</text>
    <text id="w" x="44" y="56" font-size="30">W</text>
  </g>
  <!-- 放大镜与 W 融合 -->
  <circle cx="66" cy="62" r="8" fill="none" stroke="#fff" stroke-width="3"/>
  <rect x="73" y="68" width="10" height="4" rx="2" fill="#fff" transform="rotate(35 78 70)"/>
</svg>'''

def build():
    site = Path(__file__).parent / "site"
    site.mkdir(exist_ok=True, parents=True)

    # 数据打平
    data = []
    for cat, items in CATEGORIES.items():
        for zh, en, br, am, ex in items:
            data.append({"category": cat, "zh": zh, "en": en, "ipa_br": br, "ipa_am": am, "example": ex})

    cats = sorted(CATEGORIES.keys())

    html = generate_html(TITLE, data, cats)
    (site / "index.html").write_text(html, encoding="utf-8")
    print("✅ Built site/index.html")

def generate_html(title, data, cats):
    # 顶部导航 + Logo 切换 + 自动 favicon
    checks = "".join([f'<label class="pill"><input type="checkbox" class="cat-filter" value="{esc(c)}" checked>{esc(c)}</label>' for c in cats])
    TEMPLATE = f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{esc(title)}</title>
<link id="favicon" rel="icon" type="image/svg+xml" href="">
<style>
:root{{--bg:#f6f9ff;--card:#fff;--text:#111;--muted:#6b7280;--brand:#2563eb}}
*{{box-sizing:border-box}} body{{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,"PingFang SC","Hiragino Sans GB","Noto Sans CJK SC","Microsoft YaHei",sans-serif;background:linear-gradient(180deg,#eaf2ff,#ffffff 60%)}}
.container{{max-width:1000px;margin:40px auto;padding:0 16px}}
.card{{background:var(--card);border-radius:16px;padding:24px;box-shadow:0 10px 30px rgba(0,0,0,.08)}}
h1{{margin:0 0 8px;font-size:26px}}
.sub{{color:var(--muted);margin:6px 0 16px}}
.toolbar{{display:grid;grid-template-columns:1fr auto;gap:12px;align-items:center;margin-bottom:12px}}
.search{{width:100%;height:42px;padding:0 12px;font-size:16px;border:1px solid #e5e7eb;border-radius:10px;outline:none}}
.filters{{display:flex;gap:10px;flex-wrap:wrap;justify-content:flex-end;align-items:center}}
.pill input{{margin-right:6px}} .pill{{display:flex;align-items:center;padding:6px 10px;border-radius:999px;background:#eff6ff;color:#1d4ed8;border:1px solid #bfdbfe;font-size:14px}}
.btn{{height:40px;padding:0 14px;border:none;border-radius:10px;background:var(--brand);color:#fff;cursor:pointer}}
.count{{margin:8px 0 0;color:#64748b;font-size:14px}}
.list{{margin:8px 0 0;padding:0;list-style:none}} .item{{border-bottom:1px solid #f1f5f9;padding:10px 0}}
.summary{{display:flex;gap:8px;align-items:center;justify-content:space-between;cursor:pointer}}
.badge{{font-size:12px;background:#e2e8f0;color:#334155;border-radius:6px;padding:2px 6px;margin-right:8px;white-space:nowrap}}
.word{{font-weight:700}} .small{{color:#64748b;font-size:13px}}
.details{{margin-top:8px;color:#111;line-height:1.6}}
.ipa{{background:#f8fafc;border-radius:8px;padding:8px;display:flex;gap:12px;flex-wrap:wrap;border:1px solid #eef2f7}}
.ipa span{{white-space:nowrap}}
.topbar{{display:flex;gap:12px;align-items:center;margin-bottom:14px;justify-content:space-between}}
.brand{{display:flex;gap:10px;align-items:center}}
.brand svg{{width:32px;height:32px;display:block}}
.brand-title{{font-weight:800;letter-spacing:.2px}}
.logo-chooser{{display:flex;gap:8px;align-items:center}}
select{{height:36px;border:1px solid #e5e7eb;border-radius:8px;padding:0 10px;outline:none}}
@media (max-width:600px){{.summary{{flex-direction:column;align-items:flex-start;gap:4px}} .brand-title{{font-size:16px}}}}
</style>
</head>
<body>
  <div class="container">
    <div class="card">

      <div class="topbar">
        <div class="brand">
          <span id="logo-slot" aria-label="logo"></span>
          <div class="brand-title">{esc(title)}</div>
        </div>
        <div class="logo-chooser">
          <span class="small">Logo：</span>
          <select id="logoSelect" title="Switch logo">
            <option value="C">C · Focus (默认, 放大镜)</option>
            <option value="B">B · Glass（扁平圆润）</option>
            <option value="A">A · Geo（几何切割）</option>
          </select>
          <button id="export" class="btn">Export CSV</button>
        </div>
      </div>

      <div class="sub">Fruits · Vegetables · Daily — 点击单词可展开英/美音标与例句。右上角可切换 Logo（会同步替换 favicon）。</div>

      <div class="toolbar">
        <input id="search" class="search" type="search" placeholder="Search（中文/English，如 apple / 苹果 / towel）" />
        <div class="filters">{checks}</div>
      </div>

      <div class="count" id="count"></div>
      <ul id="list" class="list"></ul>
    </div>
  </div>

<script>
const RAW = {json.dumps(data, ensure_ascii=False)};
const list = document.getElementById('list');
const search = document.getElementById('search');
const checks = Array.from(document.querySelectorAll('.cat-filter'));
const countEl = document.getElementById('count');
const exportBtn = document.getElementById('export');
const logoSlot = document.getElementById('logo-slot');
const logoSelect = document.getElementById('logoSelect');
const favicon = document.getElementById('favicon');

// 内联 SVG 方案（A/B/C）
const LOGOS = {{
  A: `{LOGO_A}`,
  B: `{LOGO_B}`,
  C: `{LOGO_C}`
}};

function svgToDataUrl(svg) {{
  const enc = encodeURIComponent(svg).replace(/'/g, "%27").replace(/"/g, "%22");
  return "data:image/svg+xml;charset=utf-8," + enc;
}}

function setLogo(which) {{
  const svg = LOGOS[which] || LOGOS.C;
  logoSlot.innerHTML = svg;
  favicon.href = svgToDataUrl(svg);
  localStorage.setItem('dw_logo', which);
  logoSelect.value = which;
}}

function norm(s){{return (s||'').toLowerCase().trim();}}

function render(items){{
  list.innerHTML = items.map(it => `
    <li class="item">
      <details>
        <summary class="summary">
          <span class="controls">
            <span class="badge">\${it.category}</span>
            <span class="word">\${escapeHtml(it.en)}</span>
            <span class="small">— \${escapeHtml(it.zh)}</span>
          </span>
          <span class="small">▶ click to expand</span>
        </summary>
        <div class="details">
          <div class="ipa"><span><b>BrE</b> \${escapeHtml(it.ipa_br)}</span><span><b>AmE</b> \${escapeHtml(it.ipa_am)}</span></div>
          <div style="margin-top:8px;"><b>Example:</b> \${escapeHtml(it.example)}</div>
        </div>
      </details>
    </li>
  `).join('');
  countEl.textContent = `Showing \${items.length} / \${RAW.length} words`;
}}

function escapeHtml(s){{
  return String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;');
}}

function apply(){{
  const kw = norm(search.value);
  const chosen = new Set(checks.filter(c=>c.checked).map(c=>c.value));
  const filtered = RAW.filter(it => chosen.has(it.category) && (
    !kw || norm(it.en).includes(kw) || norm(it.zh).includes(kw)
  ));
  render(filtered);
}}

function exportCSV(){{
  const kw = norm(search.value);
  const chosen = new Set(checks.filter(c=>c.checked).map(c=>c.value));
  const filtered = RAW.filter(it => chosen.has(it.category) && (
    !kw || norm(it.en).includes(kw) || norm(it.zh).includes(kw)
  ));
  const header = ['Category','Chinese','English','IPA_BrE','IPA_AmE','Example'];
  const lines = [header].concat(filtered.map(it => [it.category,it.zh,it.en,it.ipa_br,it.ipa_am,it.example]));
  const csv = lines.map(row => row.map(v => `"${String(v).replaceAll('"','""')}"`).join(',')).join('\\n');
  const blob = new Blob([csv], {{type:'text/csv;charset=utf-8'}});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url; a.download = 'daily_words.csv';
  document.body.appendChild(a); a.click();
  URL.revokeObjectURL(url); a.remove();
}}

search.addEventListener('input', apply);
checks.forEach(c => c.addEventListener('change', apply));
exportBtn.addEventListener('click', exportCSV);
logoSelect.addEventListener('change', e => setLogo(e.target.value));

// 初始：默认使用 C（放大镜融合），若本地存储有选择，用之
setLogo(localStorage.getItem('dw_logo') || 'C');
apply();
</script>
</body>
</html>"""
    return TEMPLATE

if __name__ == "__main__":
    build()

