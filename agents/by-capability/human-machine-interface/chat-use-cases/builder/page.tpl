<title>Chat Agent Spec Builder</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700&family=JetBrains+Mono:wght@400;500&family=Source+Sans+3:wght@400;500;600&display=swap">
<style>
/* Layout: a two-column workbench. Left builds the spec (use case, goals, rules); right shows what follows from it (failures, rules, code, ledger). */
:root{
  --bg:#F5F7F6; --surface:#FFFFFF; --surface2:#ECF0EF; --fg:#16201F; --muted:#50605D; --line:#D3DBD9;
  --accent:#0B6B63; --accent-fg:#FFFFFF; --accent-soft:#DAEFEC;
  --good:#1D7539; --good-soft:#DAF0E1; --warn:#8F5600; --warn-soft:#FAEBCF; --bad:#9F2727; --bad-soft:#F7DADA;
  --code-bg:#101716; --code-fg:#DCEAE7; --code-mute:#8FA7A2;
  --font-display:"Bricolage Grotesque","Segoe UI",system-ui,sans-serif; --font-body:"Source Sans 3","Segoe UI",system-ui,sans-serif; --font-mono:"JetBrains Mono",ui-monospace,Consolas,monospace;
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --bg:#0C1413; --surface:#131D1C; --surface2:#1A2625; --fg:#E5EEEC; --muted:#9BB0AC; --line:#293937;
  --accent:#5CC9BE; --accent-fg:#06201D; --accent-soft:#16312E;
  --good:#7CD49B; --good-soft:#15301F; --warn:#E5AA4C; --warn-soft:#33290F; --bad:#EF8E8E; --bad-soft:#3A1D1D;
  --code-bg:#0A100F; --code-fg:#D5E6E2; --code-mute:#7F9893; color-scheme:dark}}
:root[data-theme="dark"]{
  --bg:#0C1413; --surface:#131D1C; --surface2:#1A2625; --fg:#E5EEEC; --muted:#9BB0AC; --line:#293937;
  --accent:#5CC9BE; --accent-fg:#06201D; --accent-soft:#16312E;
  --good:#7CD49B; --good-soft:#15301F; --warn:#E5AA4C; --warn-soft:#33290F; --bad:#EF8E8E; --bad-soft:#3A1D1D;
  --code-bg:#0A100F; --code-fg:#D5E6E2; --code-mute:#7F9893; color-scheme:dark}
*{box-sizing:border-box}
body{background:var(--bg);color:var(--fg);font-family:var(--font-body);font-size:16px;line-height:1.5;margin:0;
  padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:20px 56px}
.wrap{max-width:1240px;margin:0 auto}
h1,h2,h3{font-family:var(--font-display);line-height:1.15;margin:0;text-wrap:balance}
h1{font-size:clamp(1.7rem,3.2vw,2.5rem);font-weight:700;letter-spacing:-.01em}
h2{font-size:1.05rem;font-weight:600}
h3{font-size:1rem;font-weight:600}
p{margin:0}
a{color:var(--accent)}
.eyebrow{font-size:.78rem;letter-spacing:.09em;text-transform:uppercase;color:var(--muted);font-weight:600}
header{display:grid;gap:10px;padding-bottom:18px}
.lede{color:var(--muted);max-width:68ch}
.badges{display:flex;flex-wrap:wrap;gap:8px;margin-top:4px}
.chip{display:inline-flex;align-items:center;gap:4px;font-size:.78rem;font-weight:600;padding:2px 9px;border-radius:999px;background:var(--surface2);color:var(--muted);border:1px solid var(--line);white-space:nowrap}
.chip.good{background:var(--good-soft);color:var(--good);border-color:transparent}
.chip.warn{background:var(--warn-soft);color:var(--warn);border-color:transparent}
.chip.bad{background:var(--bad-soft);color:var(--bad);border-color:transparent}
.chip.acc{background:var(--accent-soft);color:var(--accent);border-color:transparent}
.grid{display:grid;grid-template-columns:minmax(0,420px) minmax(0,1fr);gap:20px;align-items:start}
@media(max-width:900px){.grid{grid-template-columns:minmax(0,1fr)}}
.panel{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:16px;display:grid;gap:14px;min-width:0}
.step{display:grid;gap:10px}
.step-head{display:flex;align-items:baseline;justify-content:space-between;gap:10px}
.step-head .n{font-family:var(--font-mono);font-size:.78rem;color:var(--muted)}
label.field{display:grid;gap:6px;font-size:.9rem;font-weight:600}
select{font:inherit;color:var(--fg);background:var(--surface2);border:1px solid var(--line);border-radius:8px;padding:9px 10px;width:100%}
:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.uc-card{background:var(--surface2);border-radius:8px;padding:12px;display:grid;gap:8px;font-size:.92rem}
.kv{display:grid;grid-template-columns:auto 1fr;gap:2px 10px}
.kv dt{color:var(--muted)} .kv dd{margin:0}
.gate{background:var(--warn-soft);color:var(--warn);border-radius:8px;padding:10px 12px;font-size:.9rem}
.list{display:grid;gap:8px;margin:0;padding:0;list-style:none}
.opt{display:grid;grid-template-columns:auto 1fr;gap:10px;align-items:start;padding:10px;border:1px solid var(--line);border-radius:8px;background:var(--surface);cursor:pointer}
.opt:hover{border-color:var(--accent)}
.opt input{margin-top:4px;accent-color:var(--accent);width:16px;height:16px}
.opt.on{border-color:var(--accent);background:var(--accent-soft)}
.opt .t{font-weight:600;font-size:.95rem}
.opt .m{font-size:.82rem;color:var(--muted)}
.opt .tags{display:flex;flex-wrap:wrap;gap:6px;margin-top:4px}
.group-title{font-size:.78rem;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);font-weight:600;margin-top:4px}
button{font:inherit;cursor:pointer}
.btn{background:var(--surface2);color:var(--fg);border:1px solid var(--line);border-radius:8px;padding:6px 12px;font-size:.88rem;font-weight:600}
.btn:hover{border-color:var(--accent)}
.btn.pri{background:var(--accent);color:var(--accent-fg);border-color:var(--accent)}
.out{display:grid;gap:14px;min-width:0}
.stats{display:flex;flex-wrap:wrap;gap:10px}
.stat{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:10px 14px;min-width:120px}
.stat b{display:block;font-family:var(--font-display);font-size:1.5rem;line-height:1.1;font-variant-numeric:tabular-nums}
.stat span{font-size:.8rem;color:var(--muted)}
.tabs{display:flex;gap:4px;border-bottom:1px solid var(--line);overflow-x:auto}
.tab{background:none;border:0;border-bottom:3px solid transparent;padding:10px 14px;font-weight:600;color:var(--muted);white-space:nowrap}
.tab[aria-selected="true"]{color:var(--fg);border-bottom-color:var(--accent)}
.tabpanel{display:grid;gap:14px;min-width:0}
.card{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:14px;display:grid;gap:8px;min-width:0}
.card .row{display:flex;flex-wrap:wrap;gap:8px;align-items:center;justify-content:space-between}
.goalhead{display:grid;gap:2px}
.goalhead .sub{font-size:.85rem;color:var(--muted)}
.fail{display:grid;gap:2px;padding:8px 0;border-top:1px solid var(--line)}
.fail:first-of-type{border-top:0}
.fail .ft{font-weight:600}
.fail .fi{font-size:.88rem;color:var(--muted)}
.note{font-size:.88rem;color:var(--muted)}
.metricgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:8px;font-size:.86rem}
.metricgrid div{background:var(--surface2);border-radius:8px;padding:8px 10px}
.metricgrid b{display:block;font-size:.72rem;letter-spacing:.07em;text-transform:uppercase;color:var(--muted);margin-bottom:2px}
pre{margin:0;background:var(--code-bg);color:var(--code-fg);border-radius:8px;padding:12px;overflow-x:auto;font-family:var(--font-mono);font-size:.82rem;line-height:1.55}
.codehead{display:flex;flex-wrap:wrap;gap:8px;align-items:center;justify-content:space-between}
.lang{font-family:var(--font-mono);font-size:.74rem;color:var(--code-mute);background:var(--code-bg);padding:2px 8px;border-radius:6px}
.tablewrap{overflow-x:auto;background:var(--surface);border:1px solid var(--line);border-radius:10px}
table{border-collapse:collapse;width:100%;font-size:.86rem;min-width:760px}
th,td{text-align:left;vertical-align:top;padding:8px 10px;border-bottom:1px solid var(--line)}
th{font-size:.74rem;letter-spacing:.07em;text-transform:uppercase;color:var(--muted);position:sticky;top:0;background:var(--surface)}
td.id{font-family:var(--font-mono);white-space:nowrap}
.foot{margin-top:28px;display:grid;gap:8px;font-size:.88rem;color:var(--muted);max-width:90ch}
.empty{color:var(--muted);padding:20px;text-align:center}
@media(prefers-reduced-motion:reduce){*{scroll-behavior:auto!important;transition:none!important}}
</style>

<div class="wrap">
<header>
  <div class="eyebrow">Chat agent spec builder</div>
  <h1>Pick a narrow chat use case. See what it must defend against.</h1>
  <p class="lede">Choose the use case, then the goals and rules. The page lists the failures to defend against, the rules to add, code to start from, and the metric behind every item.</p>
  <div class="badges">
    <span class="chip warn">Code and prompts are untested drafts</span>
    <span class="chip acc">Every rule has a metric and a counter-metric</span>
    <span class="chip">Thresholds come from your own baseline</span>
  </div>
</header>

<div class="grid">
  <section class="panel" aria-label="Build the spec">
    <div class="step">
      <div class="step-head"><h2>Use case</h2><span class="n">1 of 3</span></div>
      <label class="field" for="uc">Narrow chat use case
        <select id="uc"></select>
      </label>
      <div id="ucCard" class="uc-card"></div>
      <div><button class="btn" id="reset" type="button">Reset to this use case's defaults</button></div>
    </div>
    <div class="step">
      <div class="step-head"><h2>Goals</h2><span class="n">2 of 3</span></div>
      <p class="note">Each goal brings its failures, rules, and metric.</p>
      <ul class="list" id="goals"></ul>
    </div>
    <div class="step">
      <div class="step-head"><h2>Rules</h2><span class="n">3 of 3</span></div>
      <p class="note">Goals switch rules on. You can add or remove any.</p>
      <div id="rules"></div>
    </div>
  </section>

  <section class="out" aria-label="What to incorporate">
    <div class="stats" id="stats"></div>
    <div class="tabs" role="tablist" id="tabs"></div>
    <div class="tabpanel" id="panel" role="tabpanel"></div>
  </section>
</div>

<div class="foot">
  <p><b>How to read this.</b> Failures come from the failure library and catalog, linked where a page exists. "Candidate" means catalogued but not yet written. Goals, rule text, and snippets are illustrative drafts written for this page: none has been run against a model, and the code is shaped to show the idea, not to ship.</p>
  <p><b>Usage evidence grades.</b> A: a primary study or report, but from one platform. B: a survey or company-reported figure. C: a vendor claim, or a list built from online posts rather than usage logs. "-": none found in this pass. Write order (waves) weighs usage evidence together with stakes. Usage is not the same as risk.</p>
  <p><b>Thresholds.</b> The page names the metric and how to measure it. The number comes from your baseline, or from a law or published benchmark you cite.</p>
  <p><b>High-stakes use cases.</b> For emotional, companion, kids, older-adult, grief, and role-play chat (tier C), instruction text is withheld until qualified reviewers have checked it. Flags L and E mean legal or expert review is needed.</p>
</div>
</div>

<script>
const DATA = __DATA__;
const $ = s => document.querySelector(s);
const esc = s => String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const TYPES=[['instruction','Instructions'],['guardrail','Guardrails'],['eval','Evals']];
const TIERNAME={A:'Tier A: public evidence, lower stakes',B:'Tier B: regulated or sensitive',C:'Tier C: high-stakes relational'};
let V={goals:DATA.goals,rules:DATA.rules};
function buildView(){const seg=ucById(state.uc).segment;const m=(base,vs)=>{const o={};for(const k in base){o[k]=Object.assign({},base[k],((vs||{})[k]||{})[seg]||{})}return o};V={goals:m(DATA.goals,DATA.variants.goals),rules:m(DATA.rules,DATA.variants.rules)}}
const state={uc:'CU-05',goals:new Set(),over:{},tab:'failures'};
const ucById=id=>DATA.usecases.find(u=>u.id===id);
const GRADE_CLS={A:'good',B:'warn',C:'bad','-':''};

function load(){try{const s=JSON.parse(localStorage.getItem('chatbuilder')||'null');if(s&&ucById(s.uc)){state.uc=s.uc;state.goals=new Set(s.goals);state.over=s.over||{};state.tab=s.tab||'failures';return true}}catch(e){}return false}
function save(){try{localStorage.setItem('chatbuilder',JSON.stringify({uc:state.uc,goals:[...state.goals],over:state.over,tab:state.tab}))}catch(e){}}
function defaults(){state.goals=new Set(ucById(state.uc).goals);state.over={}}
function derived(){const s=new Set();state.goals.forEach(g=>V.goals[g].rules.forEach(r=>s.add(r)));return s}
function selectedRules(){const d=derived();return Object.keys(V.rules).filter(r=>(r in state.over)?state.over[r]:d.has(r))}
function ordered(ids){const o={instruction:0,guardrail:1,eval:2};return ids.slice().sort((a,b)=>o[V.rules[a].type]-o[V.rules[b].type])}
function withheld(r){return ucById(state.uc).tier==='C'&&V.rules[r].type==='instruction'}
function failuresFor(){const out=[];state.goals.forEach(g=>{out.push([g,V.goals[g].failures])});return out}
function uniqFailures(){const s=new Set();state.goals.forEach(g=>V.goals[g].failures.forEach(f=>s.add(f)));return s}

function renderUC(){
  const sel=$('#uc');
  if(!sel.options.length){
    [['general','General-purpose assistants'],['business','Business-deployed chat'],['relational','Relational and high-stakes']].forEach(([seg,label])=>{
      const og=document.createElement('optgroup');og.label=label;
      DATA.usecases.filter(u=>u.segment===seg).sort((a,b)=>a.wave-b.wave||a.id.localeCompare(b.id)).forEach(u=>{const o=document.createElement('option');o.value=u.id;o.textContent='Wave '+u.wave+' · '+u.name;og.appendChild(o)});sel.appendChild(og)});
  }
  sel.value=state.uc;
  const u=ucById(state.uc);
  const tierCls=u.tier==='A'?'good':u.tier==='B'?'warn':'bad';
  $('#ucCard').innerHTML=`<div style="display:flex;flex-wrap:wrap;gap:6px"><span class="chip ${tierCls}">${esc(TIERNAME[u.tier])}</span>${u.flags?`<span class="chip bad">Review needed: ${esc(u.flags)}</span>`:''}<span class="chip">${esc(u.id)}</span><span class="chip acc">Write order: wave ${u.wave}</span></div>
  <dl class="kv" style="margin:0"><dt>Primary metric</dt><dd>${esc(u.primary)}</dd><dt>Counter-metric</dt><dd>${esc(u.counter)}</dd></dl>
  ${u.note?`<p class="note">${esc(u.note)}</p>`:''}
  <div><div class="group-title">Market usage evidence <span class="chip ${GRADE_CLS[u.evidence.grade]||''}">Grade ${esc(u.evidence.grade)}</span></div>
  <p class="note">${esc(u.evidence.text)}</p>${u.evidence.sources.length?`<p class="note">${u.evidence.sources.map(x=>`<a href="${esc(x.url)}" target="_blank" rel="noopener">${esc(x.name)}</a>`).join(' · ')}</p>`:''}</div>
  ${u.tier==='C'?'<div class="gate">Instruction text is withheld for this use case until qualified reviewers have checked it. Goals, metrics, guardrail rules, and evals are shown.</div>':''}`;
}
function renderGoals(){
  $('#goals').innerHTML=Object.entries(V.goals).map(([id,g])=>{const on=state.goals.has(id);
    return `<li><label class="opt ${on?'on':''}"><input type="checkbox" data-goal="${id}" ${on?'checked':''}><span><span class="t">${esc(g.name)}</span><span class="m" style="display:block">Metric: ${esc(g.metric)}</span></span></label></li>`}).join('');
}
function renderRules(){
  const d=derived();
  $('#rules').innerHTML=TYPES.map(([t,label])=>{
    const ids=Object.keys(V.rules).filter(r=>V.rules[r].type===t);
    return `<div class="group-title">${label}</div><ul class="list">`+ids.map(r=>{const R=V.rules[r];const on=selectedRules().includes(r);const rec=d.has(r);
      return `<li><label class="opt ${on?'on':''}"><input type="checkbox" data-rule="${r}" ${on?'checked':''}><span><span class="t">${esc(R.title)}</span><span class="m" style="display:block">${esc(R.metric)}</span><span class="tags">${rec?'<span class="chip acc">From your goals</span>':''}${R.flag?`<span class="chip bad">${esc(R.flag)}</span>`:''}</span></span></label></li>`}).join('')+'</ul>';
  }).join('');
}
function failItem(k){const f=DATA.failures[k];
  const kind=f.kind==='library'?['Library pattern','good']:f.kind==='written'?['Written HMI pattern','good']:['Candidate, not yet written','warn'];
  const title=f.path?`<a href="${esc(DATA.linkBase+f.path)}" target="_blank" rel="noopener">${esc(f.title)}</a>`:esc(f.title);
  return `<div class="fail"><div style="display:flex;flex-wrap:wrap;gap:8px;align-items:center"><span class="ft">${title}</span><span class="chip ${kind[1]}">${kind[0]}</span></div><div class="fi">${esc(f.issue)}</div></div>`}
function tabFailures(){
  if(!state.goals.size)return '<div class="empty">Pick at least one goal to see its failures.</div>';
  return failuresFor().map(([g,fs])=>{const G=V.goals[g];const real=fs.filter(k=>DATA.failures[k].kind!=='candidate').length;
    return `<div class="card"><div class="goalhead"><h3>${esc(G.name)}</h3><span class="sub">Metric: ${esc(G.metric)}. Counter-metric: ${esc(G.counter)}.</span></div>
    ${real===0?'<div class="gate">No written pattern covers this goal yet. The items below are catalogued candidates.</div>':''}
    <div>${fs.map(failItem).join('')}</div></div>`}).join('');
}
function ruleCard(r){const R=V.rules[r];const w=withheld(r);
  const prev=R.prevents.map(k=>esc(DATA.failures[k].title)).join('; ');
  return `<div class="card"><div class="row"><h3>${esc(R.title)}</h3><span style="display:flex;gap:6px;flex-wrap:wrap"><span class="chip acc">${esc(R.type)}</span>${R.flag?`<span class="chip bad">Review: ${esc(R.flag)}</span>`:''}</span></div>
  ${w?'<div class="gate">Instruction text withheld for this use case pending expert review.</div>':`<p>${esc(R.text)}</p>`}
  <div class="metricgrid"><div><b>Metric</b>${esc(R.metric)}</div><div><b>How measured</b>${esc(R.how)}</div><div><b>Counter-metric</b>${esc(R.counter)}</div><div><b>Threshold</b>${esc(R.basis)}</div></div>
  <p class="note"><b>Prevents:</b> ${prev}</p></div>`}
function tabRules(){const ids=ordered(selectedRules());if(!ids.length)return '<div class="empty">No rules selected. Pick goals or add rules on the left.</div>';
  return TYPES.map(([t,label])=>{const x=ids.filter(r=>V.rules[r].type===t);return x.length?`<h2>${label} (${x.length})</h2>`+x.map(ruleCard).join(''):''}).join('')}
function tabCode(){const ids=ordered(selectedRules());if(!ids.length)return '<div class="empty">No rules selected.</div>';
  const note='<div class="gate">Illustrative drafts. None of this has been run against a model, and none is production code. Placeholders and example values are marked in comments.</div>';
  return note+ids.map(r=>{const R=V.rules[r];const w=withheld(r);
    return `<div class="card"><div class="codehead"><h3>${esc(R.title)}</h3><span style="display:flex;gap:8px;align-items:center"><span class="lang">${esc(R.lang)}</span>${w?'':`<button class="btn" type="button" data-copy="${r}">Copy</button>`}</span></div>${w?'<div class="gate">Instruction text withheld for this use case pending expert review.</div>':`<pre id="code-${r}"><code>${esc(R.code)}</code></pre>`}</div>`}).join('')}
function ledgerRows(){return ordered(selectedRules()).map((r,i)=>{const R=V.rules[r];return {id:'L-'+String(i+1).padStart(2,'0'),item:R.title,type:R.type,metric:R.metric,how:R.how,counter:R.counter,basis:R.basis}})}
function tabLedger(){const rows=ledgerRows();if(!rows.length)return '<div class="empty">No rules selected.</div>';
  return `<div class="row" style="display:flex;gap:8px;flex-wrap:wrap"><button class="btn pri" type="button" data-copy-ledger="md">Copy as Markdown</button><button class="btn" type="button" data-copy-ledger="json">Copy as JSON</button></div>
  <div class="tablewrap"><table><thead><tr><th>ID</th><th>Item</th><th>Type</th><th>Metric</th><th>How measured</th><th>Counter-metric</th><th>Threshold basis</th></tr></thead><tbody>`+
  rows.map(r=>`<tr><td class="id">${r.id}</td><td>${esc(r.item)}</td><td>${esc(r.type)}</td><td>${esc(r.metric)}</td><td>${esc(r.how)}</td><td>${esc(r.counter)}</td><td>${esc(r.basis)}</td></tr>`).join('')+'</tbody></table></div>'}
function renderOut(){
  const rules=selectedRules();const fs=uniqFailures();
  const written=[...fs].filter(k=>DATA.failures[k].kind!=='candidate').length;
  $('#stats').innerHTML=`<div class="stat"><b>${state.goals.size}</b><span>goals</span></div><div class="stat"><b>${rules.length}</b><span>rules, each with a metric</span></div><div class="stat"><b>${written}</b><span>failure patterns (${fs.size-written} more are candidates)</span></div>`;
  const tabs=[['failures','Failures'],['rules','Rules'],['code','Code'],['ledger','Metric ledger']];
  $('#tabs').innerHTML=tabs.map(([k,l])=>`<button class="tab" role="tab" type="button" data-tab="${k}" aria-selected="${state.tab===k}">${l}</button>`).join('');
  const fn={failures:tabFailures,rules:tabRules,code:tabCode,ledger:tabLedger}[state.tab];
  $('#panel').innerHTML=fn();
}
function renderAll(){buildView();renderUC();renderGoals();renderRules();renderOut();save()}
async function copyText(text,btn){
  let ok=false;
  try{await navigator.clipboard.writeText(text);ok=true}catch(e){
    const ta=document.createElement('textarea');ta.value=text;ta.style.position='fixed';ta.style.opacity='0';document.body.appendChild(ta);ta.select();try{ok=document.execCommand('copy')}catch(_){}document.body.removeChild(ta)}
  if(btn){const o=btn.textContent;btn.textContent=ok?'Copied':'Select and copy manually';setTimeout(()=>btn.textContent=o,1400)}
}
document.addEventListener('change',e=>{
  const t=e.target;
  if(t.id==='uc'){state.uc=t.value;defaults();renderAll();return}
  if(t.dataset.goal){t.checked?state.goals.add(t.dataset.goal):state.goals.delete(t.dataset.goal);state.over={};renderAll();return}
  if(t.dataset.rule){state.over[t.dataset.rule]=t.checked;renderAll()}
});
document.addEventListener('click',e=>{
  const b=e.target.closest('button');if(!b)return;
  if(b.id==='reset'){defaults();renderAll();return}
  if(b.dataset.tab){state.tab=b.dataset.tab;renderAll();return}
  if(b.dataset.copy){copyText(V.rules[b.dataset.copy].code,b);return}
  if(b.dataset.copyLedger){const rows=ledgerRows();
    const text=b.dataset.copyLedger==='json'?JSON.stringify(rows,null,2):'| ID | Item | Type | Metric | How measured | Counter-metric | Threshold basis |\n|---|---|---|---|---|---|---|\n'+rows.map(r=>`| ${r.id} | ${r.item} | ${r.type} | ${r.metric} | ${r.how} | ${r.counter} | ${r.basis} |`).join('\n');
    copyText(text,b)}
});
if(!load())defaults();
renderAll();
</script>
