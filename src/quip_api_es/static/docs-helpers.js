;(() => {
  function ready(fn){
    if (document.readyState !== 'loading') fn();
    else document.addEventListener('DOMContentLoaded', fn);
  }

  ready(() => {
    const root = document.querySelector('#swagger-ui');
    if (!root) return;

    const btn = document.createElement('button');
    btn.className = 'btn';
    btn.type = 'button';
    btn.textContent = 'Expandir todo';
    btn.setAttribute('aria-expanded', 'false');
    document.body.appendChild(btn);

    let expanded = false;
    function setState(){
      btn.textContent = expanded ? 'Colapsar todo' : 'Expandir todo';
      btn.setAttribute('aria-expanded', String(expanded));
    }

    function toggle(){
      const details = root.querySelectorAll('.opblock.is-open .opblock-summary-control, .opblock .opblock-summary-control');
      details.forEach(el => {
        const open = el.closest('.opblock')?.classList.contains('is-open');
        if (expanded && !open) el.click();
        if (!expanded && open) el.click();
      });
      expanded = !expanded;
      setState();
    }

    btn.addEventListener('click', toggle);
    document.addEventListener('keydown', (e) => {
      if (['INPUT','TEXTAREA','SELECT'].includes(e.target.tagName)) return;
      if (e.key.toLowerCase() === 'e') { expanded = false; setState(); toggle(); }
      if (e.key.toLowerCase() === 'c') { expanded = true;  setState(); toggle(); }
    }, {passive:true});
  });
})();
