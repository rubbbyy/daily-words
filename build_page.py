# -*- coding: utf-8 -*-
from pathlib import Path
import json
from vocab_data import CATEGORIES

TITLE = "Daily Words"

def esc(s):
    return (s or "").replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

def build():
    site = Path(__file__).parent / "site"
    site.mkdir(exist_ok=True, parents=True)
    data = []
    for cat, items in CATEGORIES.items():
        for zh, en, br, am, ex in items:
            data.append({"category": cat, "zh": zh, "en": en, "ipa_br": br, "ipa_am": am, "example": ex})
    # prepare checks
    checks = "".join([f'<label class="pill"><input type="checkbox" class="cat-filter" value="{esc(c)}" checked>{esc(c)}</label>' for c in sorted(CATEGORIES.keys())])
    html = TEMPLATE.replace("%%TITLE%%", esc(TITLE)).replace("%%CHECKS%%", checks).replace("%%DATA%%", json.dumps(data, ensure_ascii=False))
    (site/"index.html").write_text(html, encoding="utf-8")
    print("✅ Built site/index.html")

TEMPLATE = r"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>%%TITLE%%</title>
<style>
:root{--bg:#f6f9ff;--card:#fff;--text:#111;--muted:#6b7280;--brand:#2563eb;}
*{box-sizing:border-box}
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,"PingFang SC","Hiragino Sans GB","Noto Sans CJK SC","Microsoft YaHei",sans-serif;background:linear-gradient(180deg,#eaf2ff,#ffffff 60%)}
.container{max-width:1000px;margin:40px auto;padding:0 16px}
.card{background:var(--card);border-radius:16px;padding:24px;box-shadow:0 10px 30px rgba(0,0,0,.08)}
h1{margin:0 0 8px;font-size:28px}
.sub{color:var(--muted);margin-bottom:16px}
.toolbar{display:grid;grid-template-columns:1fr auto;gap:12px;align-items:center;margin-bottom:12px}
.search{width:100%;height:42px;padding:0 12px;font-size:16px;border:1px solid #e5e7eb;border-radius:10px;outline:none}
.filters{display:flex;gap:10px;flex-wrap:wrap;justify-content:flex-end;align-items:center}
.pill input{margin-right:6px}
.pill{display:flex;align-items:center;padding:6px 10px;border-radius:999px;background:#eff6ff;color:#1d4ed8;border:1px solid #bfdbfe;font-size:14px}
.btn{height:40px;padding:0 14px;border:none;border-radius:10px;background:var(--brand);color:#fff;cursor:pointer}
.count{margin:8px 0 0;color:#64748b;font-size:14px}
.list{margin:8px 0 0;padding:0;list-style:none}
.item{border-bottom:1px solid #f1f5f9;padding:10px 0}
.summary{display:flex;gap:8px;align-items:center;justify-content:space-between;cursor:pointer}
.badge{font-size:12px;background:#e2e8f0;color:#334155;border-radius:6px;padding:2px 6px;margin-right:8px;white-space:nowrap}
.word{font-weight:700}
.small{color:#64748b;font-size:13px}
.details{margin-top:8px;color:#111;line-height:1.6}
.ipa{
  font-family: "Helvetica Neue", Arial, sans-serif;
  background:#f8fafc;border-radius:8px;padding:8px;display:flex;gap:12px;flex-wrap:wrap;
  border:1px solid #eef2f7
}
.ipa span{white-space:nowrap}
.controls{display:flex;gap:8px;align-items:center;flex-wrap:wrap}
@media (max-width:600px){
  .summary{flex-direction:column;align-items:flex-start;gap:4px}
}
</style>
</head>
<body>
  <div class="container">
    <div class="card">
      <h1>📘 %%TITLE%%</h1>
      <div class="sub">Fruits · Vegetables · Daily — Click a word to see IPA (BrE/AmE) and an example sentence. Search supports Chinese and English.</div>
      <div class="toolbar">
        <input id="search" class="search" type="search" placeholder="Search（中文/English，如 apple / 苹果 / towel）" />
        <div class="filters">
          %%CHECKS%%
          <button id="export" class="btn">Export CSV</button>
        </div>
      </div>
      <div class="count" id="count"></div>
      <ul id="list" class="list"></ul>
    </div>
  </div>

<script>
const RAW = %%DATA%%;
const list = document.getElementById('list');
const search = document.getElementById('search');
const checks = Array.from(document.querySelectorAll('.cat-filter'));
const countEl = document.getElementById('count');
const exportBtn = document.getElementById('export');

function norm(s){return (s||'').toLowerCase().trim();}

function render(items){
  list.innerHTML = items.map(it => `
    <li class="item">
      <details>
        <summary class="summary">
          <span class="controls">
            <span class="badge">${it.category}</span>
            <span class="word">${escapeHtml(it.en)}</span>
            <span class="small">— ${escapeHtml(it.zh)}</span>
          </span>
          <span class="small">▶ click to expand</span>
        </summary>
        <div class="details">
          <div class="ipa"><span><b>BrE</b> ${escapeHtml(it.ipa_br)}</span><span><b>AmE</b> ${escapeHtml(it.ipa_am)}</span></div>
          <div style="margin-top:8px;"><b>Example:</b> ${escapeHtml(it.example)}</div>
        </div>
      </details>
    </li>
  `).join('');
  countEl.textContent = `Showing ${items.length} / ${RAW.length} words`;
}

function escapeHtml(s){
  return String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;');
}

function apply(){
  const kw = norm(search.value);
  const chosen = new Set(checks.filter(c=>c.checked).map(c=>c.value));
  const filtered = RAW.filter(it => chosen.has(it.category) && (
      !kw || norm(it.en).includes(kw) || norm(it.zh).includes(kw)
  ));
  render(filtered);
}

function exportCSV(){
  const kw = norm(search.value);
  const chosen = new Set(checks.filter(c=>c.checked).map(c=>c.value));
  const filtered = RAW.filter(it => chosen.has(it.category) && (
      !kw || norm(it.en).includes(kw) || norm(it.zh).includes(kw)
  ));
  const header = ['Category','Chinese','English','IPA_BrE','IPA_AmE','Example'];
  const lines = [header].concat(filtered.map(it => [it.category,it.zh,it.en,it.ipa_br,it.ipa_am,it.example]));
  const csv = lines.map(row => row.map(v => `"${String(v).replaceAll('"','""')}"`).join(',')).join('\n');
  const blob = new Blob([csv], {type:'text/csv;charset=utf-8'});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url; a.download = 'daily_words.csv';
  document.body.appendChild(a); a.click();
  URL.revokeObjectURL(url); a.remove();
}

search.addEventListener('input', apply);
checks.forEach(c => c.addEventListener('change', apply));
exportBtn.addEventListener('click', exportCSV);
apply();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    build()
