(function(){
  'use strict';

  const S = {
    tagBtn: '.opblock-tag',
    opBtn: '.opblock .opblock-summary-control',
    modelToggle: '.model-box .model-toggle'
  };

  function expandAll(){
    document.querySelectorAll(S.tagBtn).forEach(btn=>{
      const wrap = btn.closest('.opblock-tag-section') || btn.parentElement;
      if (wrap && !wrap.classList.contains('is-open')) btn.click();
    });
    document.querySelectorAll(S.opBtn).forEach(b=>{
      const op = b.closest('.opblock');
      if (op && !op.classList.contains('is-open')) b.click();
    });
    document.querySelectorAll(S.modelToggle).forEach(t=>{
      if (t.getAttribute('aria-expanded') !== 'true') t.click();
    });
  }

  function collapseAll(){
    document.querySelectorAll(S.opBtn).forEach(b=>{
      const op = b.closest('.opblock');
      if (op && op.classList.contains('is-open')) b.click();
    });
    document.querySelectorAll(S.tagBtn).forEach(btn=>{
      const wrap = btn.closest('.opblock-tag-section') || btn.parentElement;
      if (wrap && wrap.classList.contains('is-open')) btn.click();
    });
    document.querySelectorAll(S.modelToggle).forEach(t=>{
      if (t.getAttribute('aria-expanded') === 'true') t.click();
    });
  }

  // Botón + estilos
  const css = document.createElement('style');
  css.textContent = `
    #qa-expand-toggle{
      position:fixed; right:16px; top:16px; z-index:9999;
      padding:8px 12px; border-radius:10px;
      background:#0ea5e9; color:#0b1220; border:1px solid #1e293b;
      font-weight:600; box-shadow:0 4px 20px rgba(34,211,238,.25);
      cursor:pointer;
    }
    #qa-expand-toggle:hover{ filter:brightness(1.08); }
  `;
  document.head.appendChild(css);

  const btn = document.createElement('button');
  btn.id = 'qa-expand-toggle';
  document.body.appendChild(btn);

  // Estado guardado (por defecto: colapsado)
  const KEY = 'qaExpanded';
  let expanded = (localStorage.getItem(KEY) === '1');

  function apply(){
    btn.textContent = expanded ? 'Colapsar todo' : 'Expandir todo';
    if (expanded) expandAll(); else collapseAll();
  }

  btn.addEventListener('click', ()=>{
    expanded = !expanded;
    localStorage.setItem(KEY, expanded ? '1' : '0');
    apply();
  });

  // Atajos: E (expandir) / C (colapsar)
  window.addEventListener('keydown',(e)=>{
    if (e.target && /INPUT|TEXTAREA|SELECT/.test(e.target.tagName)) return;
    if (e.key.toLowerCase()==='e'){ expanded = true;  localStorage.setItem(KEY,'1'); apply(); }
    if (e.key.toLowerCase()==='c'){ expanded = false; localStorage.setItem(KEY,'0'); apply(); }
  });

  // Aplica una sola vez al cargar
  const boot = ()=> apply();
  if (document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', boot, { once:true });
  } else {
    setTimeout(boot, 0);
  }
})();
