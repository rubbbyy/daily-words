// ---- Load data ----
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


// ---- Logo ----
function setLogo(){
  const val = localStorage.getItem("DW_LOGO") || "C";
  logoSel.value = val;
  logoEl.innerHTML = (
    val === "A" ? window.LOGO_A :
    val === "B" ? window.LOGO_B :
                  window.LOGO_C
  );
}

logoSel.addEventListener("change", () => {
  localStorage.setItem("DW_LOGO", logoSel.value);
  setLogo();
});


// ---- Play Pronunciation ----
function play(text, accent){
  if (!text) return;
  const url = `https://dict.youdao.com/dictvoice?audio=${
    encodeURIComponent(text)}&type=${accent==="br"?1:2}`;
  new Audio(url).play();
}


// ---- Render Items ----
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
          ${window.ICON_SPK} BrE
        </div>
        <div class="play" onclick="play('${it.en}','am')">
          ${window.ICON_SPK} AmE
        </div>
      </div>
      <div style="margin-top:10px; font-size:14px;">
        <span style="color:var(--muted);">Example:</span>
        ${it.example || ""}
      </div>
    </div>
  `).join("");

}

searchInput.addEventListener("input", render);

// ---- Init logo ----
setLogo();
// ✅ 显示单词统计
function showCount(total, filtered) {
  let footer = document.getElementById("count");
  if (!footer) {
    footer = document.createElement("div");
    footer.id = "count";
    footer.style.margin = "30px 0";
    footer.style.textAlign = "center";
    footer.style.color = "#555";
    document.body.appendChild(footer);
  }
  footer.textContent = `Showing ${filtered} / ${total} words`;
}

// ✅ 每次加载或筛选后更新计数
let allData = [];
fetch("site/data.json")
  .then(r => r.json())
  .then(data => {
    allData = data;
    renderList(allData);
    showCount(allData.length, allData.length);
  });

function renderList(data) {
  const list = document.getElementById("list");
  list.innerHTML = "";
  data.forEach(w => {
    const card = document.createElement("div");
    card.className = "card";
    card.innerHTML = `
      <div class="word">${w.en} <span style="color:#555;font-size:16px;">${w.zh}</span></div>
      <div>${w.ipaBr} | ${w.ipaAm}</div>
      <div style="color:#555;">${w.example}</div>
    `;
    list.appendChild(card);
  });
  showCount(allData.length, data.length);
}
