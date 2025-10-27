# -*- coding: utf-8 -*-
from pathlib import Path
import json
from vocab_data import CATEGORIES

TITLE = "Daily Words by Rubby"

def esc(s):
    return (s or "").replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

# === Logos (A/B/C) ===
LOGO_A = r'''<svg xmlns="http://www.w3.org/2000/svg" width="96" height="96" viewBox="0 0 96 96"><defs><linearGradient id="gA" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3b82f6"/><stop offset="1" stop-color="#2563EB"/></linearGradient></defs><circle cx="48" cy="48" r="44" fill="url(#gA)"/><g fill="#fff" font-family="Inter, Arial, sans-serif" font-weight="800"><text x="22" y="57" font-size="30">D</text><text x="49" y="57" font-size="30">W</text></g></svg>'''
LOGO_B = r'''<svg xmlns="http://www.w3.org/2000/svg" width="96" height="96" viewBox="0 0 96 96"><defs><radialGradient id="gB" cx="30%" cy="20%" r="80%"><stop offset="0" stop-color="#60a5fa"/><stop offset="1" stop-color="#2563EB"/></radialGradient></defs><circle cx="48" cy="48" r="44" fill="url(#gB)"/><g fill="#fff" font-family="Nunito, Arial, sans-serif" font-weight="900"><text x="22" y="57" font-size="30">D</text><text x="49" y="57" font-size="30">W</text></g><path d="M20 32c8-6 18-9 28-9 10 0 20 3 28 9" fill="none" stroke="#ffffff" stroke-opacity=".25" stroke-width="4" stroke-linecap="round"/></svg>'''
LOGO_C = r'''<svg xmlns="http://www.w3.org/2000/svg" width="96" height="96" viewBox="0 0 96 96"><defs><linearGradient id="gC" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#60a5fa"/><stop offset="1" stop-color="#2563EB"/></linearGradient></defs><circle cx="48" cy="48" r="44" fill="url(#gC)"/><g fill="#fff" font-family="Nunito, Arial, sans-serif" font-weight="900"><text x="20" y="56" font-size="30">D</text><text id="w" x="44" y="56" font-size="30">W</text></g><circle cx="66" cy="62" r="8" fill="none" stroke="#fff" stroke-width="3"/><rect x="73" y="68" width="10" height="4" rx="2" fill="#fff" transform="rotate(35 78 70)"/></svg>'''

# === Speaker icons (SVG) ===
ICON_BRE = r'''<svg class="spk" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M4 10v4h3l4 3V7L7 10H4z" fill="currentColor"/><path d="M14 10a2 2 0 0 1 0 4" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><text x="18" y="20" font-size="6" fill="currentColor">Br</text></svg>'''
ICON_AME = r'''<svg class="spk" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M4 10v4h3l4 3V7L7 10H4z" fill="currentColor"/><path d="M14 8a4 4 0 0 1 0 8" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><text x="18" y="20" font-size="6" fill="currentColor">Am</text></svg>'''

def build():
    site = Path(__file__).parent / "site"
    site.mkdir(exist_ok=True, parents=True)

    data = []
    cats = []
    for cat, items in CATEGORIES.items():
        cats.append(cat)
        for zh, en, br, am, ex in items:
            data.append({"category": cat, "zh": zh, "en": en, "ipa_br": br, "ipa_am": am, "example": ex})

    html = generate_html(TITLE, data, cats)
    (site / "index.html").write_text(html, encoding="utf-8")
    print("✅ Built site/index.html")

def generate_html(title, data, cats):
    checks = "".join([f'<label class="pill"><input type="checkbox" class="cat-filter" value="{esc(c)}" checked>{esc(c)}</label>' for c in cats])

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{esc(title)}</title>
<link id="favicon" rel="icon" type="image/svg+xml" href="">
<style>
:root{{--bg:#f6f9ff;--card:#fff;--text:#111;--muted:#6b7280;--brand:#2563EB;--accent:#2563EB}}
*{{box-sizing:border-box}}
body{{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,"PingFang SC","Hiragino Sans GB","Noto Sans CJK SC","Microsoft YaHei",sans-serif;background:linear-gradient(180deg,#eaf2ff,#ffffff 60%)}}
.container{{max-width:1000px;margin:40px auto;padding:0 16px}}
.card{{background:var(--card);border-radius:16px;padding:24px;box-shadow:0 10px 30px rgba(0,0,0,.08)}}
.topbar{{display:flex;gap:12px;align-items:center;justify-content:space-between;margin-bottom:14px}}
.brand{{display:flex;gap:10px;align-items:center}}
.brand svg{{width:32px;height:32px;display:block}}
.brand-title{{font-weight:800;letter-spacing:.2px;font-size:20px}}
.logo-chooser{{display:flex;gap:8px;align-items:center}}
.small{{font-size:13px;color:var(--muted)}}
.search{{width:100%;height:42px;padding:0 12px;font-size:16px;border:1px solid #e5e7eb;border-radius:10px}}
.filters{{display:flex;gap:10px;flex-wrap:wrap;justify-content:flex-end}}
.pill{{display:flex;align-items:center;padding:6px 10px;border-radius:999px;background:#eff6ff;color:#1d4ed8;border:1px solid #bfdbfe;font-size:14px}}
.list{{margin:8px 0 0;padding:0;list-style:none}}
.item{{border-bottom:1px solid #f1f5f9;padding:10px 0}}
.summary{{display:flex;gap:8px;align-items:center;justify-content:space-between;cursor:pointer}}
.controls{{display:flex;gap:10px;align-items:center;flex-wrap:wrap}}
.word{{font-weight:700}}
.count{{margin-top:6px;color:#64748b;font-size:14px}}
.details{{margin-top:8px;color:#111;line-height:1.6}}
.ipa{{background:#f8fafc;border-radius:8px;padding:8px;border:1px solid #eef2f7;margin-bottom:6px;display:flex;gap:12px;align-items:center;flex-wrap:wrap}}
.btn{{height:40px;padding:0 14px;border:none;border-radius:10px;background:var(--brand);color:#fff}}
.badge{{font-size:12px;background:#e2e8f0;color:#334155;border-radius:6px;padding:2px 6px;white-space:nowrap}}

.spk-btn{{display:inline-flex;align-items:center;gap:4px;border:1px solid #e5e7eb;border-radius:10px;padding:4px 8px;font-size:13px;color:#334155;background:#fff;cursor:pointer}}
.spk-btn .spk{{width:16px;height:16px}}
.spk-btn:hover{{border-color:#cbd5e1}}
.spk-btn.playing{{background:#e0ebff;border-color:var(--accent);color:#1d4ed8}}
.spk-pair{{display:flex;gap:8px;align-items:center;flex-wrap:wrap}}

.hint{{color:#64748b;font-size:12px;margin-top:4px}}
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
            <option value="C">C · Focus（默认）</option>
            <option value="B">B · Glass</option>
            <option value="A">A · Geo</option>
          </select>
          <button id="export" class="btn">Export CSV</button>
        </div>
      </div>

      <input id="search" class="search" type="search" placeholder="Search（中文/English，如 apple / 苹果 / towel）">
      <div class="filters">{checks}</div>
      <div class="count" id="count"></div>
      <ul id="list" class="list"></ul>

      <div class="hint">提示：点击英文单词可用默认口音朗读；展开后可分别播放英式🔉 / 美式🔊。如无声音，尝试点一下页面以允许音频。</div>
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

const LOGOS = {{ A:`{LOGO_A}`, B:`{LOGO_B}`, C:`{LOGO_C}` }};
const ICON_BRE = `{ICON_BRE}`;
const ICON_AME = `{ICON_AME}`;

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

function escapeHtml(s){{return String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;');}}

function norm(s){{return (s||'').toLowerCase().trim();}}

function render(items){{
  list.innerHTML = items.map(it => {{
    const titleBtns = `
      <button class="spk-btn" data-acc="BrE" data-en="${{escapeHtml(it.en)}}">${{ICON_BRE}} BrE</button>
      <button class="spk-btn" data-acc="AmE" data-en="${{escapeHtml(it.en)}}">${{ICON_AME}} AmE</button>
    `;
    return `
      <li class="item">
        <details>
          <summary class="summary">
            <span class="controls">
              <span class="badge">\${{it.category}}</span>
              <span class="word speak-title" data-en="\${{escapeHtml(it.en)}}">\${{escapeHtml(it.en)}}</span>
              <span class="small">— \${{escapeHtml(it.zh)}}</span>
            </span>
            <span class="spk-pair" data-en="\${{escapeHtml(it.en)}}">${{titleBtns}}</span>
          </summary>
          <div class="details">
            <div class="ipa">
              <span><b>BrE</b> \${{escapeHtml(it.ipa_br)}} <button class="spk-btn" data-acc="BrE" data-en="\${{escapeHtml(it.en)}}">${{ICON_BRE}} Play</button></span>
              <span><b>AmE</b> \${{escapeHtml(it.ipa_am)}} <button class="spk-btn" data-acc="AmE" data-en="\${{escapeHtml(it.en)}}">${{ICON_AME}} Play</button></span>
            </div>
            <div><b>Example:</b> \${{escapeHtml(it.example)}}</div>
          </div>
        </details>
      </li>`;
  }}).join('');
  countEl.textContent = `Showing ${{items.length}} / ${{RAW.length}} words`;
}}

function apply(){{
  const kw = norm(search.value);
  const chosen = new Set(checks.filter(c=>c.checked).map(c=>c.value));
  const filtered = RAW.filter(it => chosen.has(it.category) && (!kw || norm(it.en).includes(kw) || norm(it.zh).includes(kw)));
  render(filtered);
}}

// ===== CSV Export =====
function exportCSV(){{
  const kw = norm(search.value);
  const chosen = new Set(checks.filter(c=>c.checked).map(c=>c.value));
  const filtered = RAW.filter(it => chosen.has(it.category) && (!kw || norm(it.en).includes(kw) || norm(it.zh).includes(kw)));
  const header = ['Category','Chinese','English','IPA_BrE','IPA_AmE','Example'];
  const lines = [header].concat(filtered.map(it => [it.category,it.zh,it.en,it.ipa_br,it.ipa_am,it.example]));
  const csv = lines.map(row => row.map(v => `"${{String(v).replaceAll('"','""')}}"`).join(',')).join('\\n');
  const blob = new Blob([csv], {{type:'text/csv;charset=utf-8'}});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url; a.download = 'daily_words.csv';
  document.body.appendChild(a); a.click();
  URL.revokeObjectURL(url); a.remove();
}}

// ===== Speech Synth (Web Speech API) =====
let voices = [];
let voicesReady = false;
const ACCENT_KEY = 'dw_accent'; // default accent for title click
const defaultAccent = localStorage.getItem(ACCENT_KEY) || 'AmE';

function refreshVoices() {{
  if (!('speechSynthesis' in window)) return;
  voices = window.speechSynthesis.getVoices() || [];
  voicesReady = voices.length > 0;
}}

refreshVoices();
if ('speechSynthesis' in window) {{
  window.speechSynthesis.onvoiceschanged = () => {{
    refreshVoices();
  }};
}}

function pickVoice(tagPref) {{
  if (!voicesReady) return null;
  // exact match first
  let exact = voices.find(v => v.lang === tagPref);
  if (exact) return exact;
  // region-weighted
  if (tagPref === 'en-GB') {{
    const gb = voices.filter(v => /en-GB|British|UK/i.test(v.lang + ' ' + v.name));
    if (gb.length) return gb[0];
  }}
  if (tagPref === 'en-US') {{
    const us = voices.filter(v => /en-US|United States|US English/i.test(v.lang + ' ' + v.name));
    if (us.length) return us[0];
  }}
  // any English
  const en = voices.filter(v => /^en(-|_)?/i.test(v.lang));
  return en[0] || voices[0] || null;
}}

function speak(text, accent, btn) {{
  if (!('speechSynthesis' in window)) {{
    alert('当前浏览器不支持语音朗读。可更换 Chrome / Safari 尝试。');
    return;
  }}
  // On some mobile browsers, need a user gesture first; clicking button/word counts.
  const utter = new SpeechSynthesisUtterance(text);
  utter.rate = 0.95;
  utter.pitch = 1.0;
  utter.lang = (accent === 'BrE') ? 'en-GB' : 'en-US';
  const v = pickVoice(utter.lang);
  if (v) utter.voice = v;

  if (btn) btn.classList.add('playing');
  utter.onend = () => {{ if (btn) btn.classList.remove('playing'); }};
  try {{ window.speechSynthesis.cancel(); }} catch(e) {{}}
  window.speechSynthesis.speak(utter);
}}

// delegation for clicks
document.addEventListener('click', (e) => {{
  // speaker buttons
  const spk = e.target.closest('.spk-btn');
  if (spk && spk.dataset.en) {{
    e.stopPropagation();
    const acc = spk.dataset.acc || 'AmE';
    const en = spk.dataset.en;
    // if user explicitly clicked an accent button, remember it for title-click default
    localStorage.setItem(ACCENT_KEY, acc);
    speak(en, acc, spk);
    return;
  }}
  // clicking the English word (title) -> speak with default accent
  const title = e.target.closest('.speak-title');
  if (title && title.dataset.en) {{
    const en = title.dataset.en;
    const acc = localStorage.getItem(ACCENT_KEY) || defaultAccent || 'AmE';
    speak(en, acc, title);
    return;
  }}
}});

// events
search.addEventListener('input', apply);
checks.forEach(c => c.addEventListener('change', apply));
exportBtn.addEventListener('click', exportCSV);
logoSelect.addEventListener('change', e => setLogo(e.target.value));

// init
setLogo(localStorage.getItem('dw_logo') || 'C'); // default main logo
apply();
</script>
</body>
</html>"""

if __name__ == "__main__":
    build()
