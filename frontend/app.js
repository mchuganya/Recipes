const rows = document.getElementById('rows');
const drawer = document.getElementById('drawer');
const searchBtn = document.getElementById('searchBtn');
const qtitle = document.getElementById('qtitle');
const qcuisine = document.getElementById('qcuisine');
const qcal = document.getElementById('qcal');
const limitSel = document.getElementById('limit');

let page = 1;

async function fetchRecipes(){
  const limit = limitSel.value || 15;
  const title = qtitle.value;
  const cuisine = qcuisine.value;
  const cal = qcal.value;
  let url = `/api/recipes?page=${page}&limit=${limit}`;
  // if search fields used, call search instead
  if (title || cuisine || cal) {
    let q = [];
    if (title) q.push(`title=${encodeURIComponent(title)}`);
    if (cuisine) q.push(`cuisine=${encodeURIComponent(cuisine)}`);
    if (cal) q.push(`calories=<=${encodeURIComponent(cal)}`);
    url = `/api/recipes/search?${q.join('&')}`;
  }
  const res = await fetch(url);
  const data = await res.json();
  let list = data.data || data.data || data.data;
  if (!list && data.data===undefined){
    // /api/recipes returns page/limit/total/data
    list = data.data || [];
  }
  if (!list && data) list = data;
  if (!Array.isArray(list)) list = data.data || [];
  renderRows(list);
}

function renderRows(list){
  rows.innerHTML = '';
  if (!list || list.length===0){
    rows.innerHTML = '<tr><td colspan="5">No results found</td></tr>';
    return;
  }
  for(const r of list){
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${truncate(r.title,40)}</td>
      <td>${r.cuisine||''}</td>
      <td><span class="stars">${renderStars(r.rating)}</span> ${r.rating||''}</td>
      <td>${r.total_time||''}</td>
      <td>${r.serves||''}</td>
    `;
    tr.onclick = ()=> openDrawer(r);
    rows.appendChild(tr);
  }
}

function truncate(s,n){ if(!s) return ''; return s.length>n? s.slice(0,n-1)+'…': s }
function renderStars(v){ if(!v) return ''; const n=Math.round(v); return '★'.repeat(n)+'☆'.repeat(Math.max(0,5-n)); }

function openDrawer(r){
  drawer.innerHTML = '';
  const h = document.createElement('h2');
  h.textContent = `${r.title} — ${r.cuisine || ''}`;
  drawer.appendChild(h);
  const desc = document.createElement('div');
  desc.innerHTML = `<strong>Description:</strong><div>${r.description||''}</div>`;
  drawer.appendChild(desc);
  const tot = document.createElement('div');
  tot.innerHTML = `<strong>Total Time:</strong> ${r.total_time||''} <button id="exp">Expand</button><div id="times" style="display:none;margin-top:8px">Prep: ${r.prep_time||''} | Cook: ${r.cook_time||''}</div>`;
  drawer.appendChild(tot);
  tot.querySelector('#exp').onclick = ()=>{
    const t = tot.querySelector('#times'); t.style.display = t.style.display==='none'?'block':'none';
  }
  const nut = document.createElement('div');
  const n = r.nutrients||{};
  nut.innerHTML = `<h3>Nutrition</h3><table>${renderNutr(n)}</table>`;
  drawer.appendChild(nut);
  drawer.classList.add('open');
}

function renderNutr(n){ if(!n) return '<tr><td>No data</td></tr>';
  const keys = ['calories','carbohydrateContent','cholesterolContent','fiberContent','proteinContent','saturatedFatContent','sodiumContent','sugarContent','fatContent'];
  return keys.map(k=>`<tr><td>${k}</td><td>${n[k]||''}</td></tr>`).join('');
}

searchBtn.onclick = ()=>{ page=1; fetchRecipes(); }

// initial load
fetchRecipes();
