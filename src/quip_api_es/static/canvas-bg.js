(() => {
  const c = document.getElementById('bg');
  if (!c) return;
  const ctx = c.getContext('2d');
  const DPR = Math.max(1, window.devicePixelRatio || 1);

  function resize(){
    const { innerWidth:w, innerHeight:h } = window;
    c.width = w * DPR;
    c.height = h * DPR;
    c.style.width = w + 'px';
    c.style.height = h + 'px';
  }
  window.addEventListener('resize', resize); resize();

  const N = 80;
  const rnd = (n=1)=>Math.random()*n;
  const particles = Array.from({length:N}, ()=>({
    x: rnd(c.width), y: rnd(c.height),
    vx: (Math.random()-0.5)*0.25*DPR,
    vy: (Math.random()-0.5)*0.25*DPR
  }));

  function frame(){
    ctx.clearRect(0,0,c.width,c.height);

    // Radial glow suave
    const g = ctx.createRadialGradient(c.width*0.7, c.height*0.3, 0, c.width*0.7, c.height*0.3, Math.max(c.width,c.height)*0.8);
    g.addColorStop(0, 'rgba(34,211,238,0.07)');
    g.addColorStop(1, 'rgba(2,6,23,0.25)');
    ctx.fillStyle = g;
    ctx.fillRect(0,0,c.width,c.height);

    // Actualiza partículas
    for (const p of particles){
      p.x += p.vx; p.y += p.vy;
      if (p.x < 0 || p.x > c.width) p.vx *= -1;
      if (p.y < 0 || p.y > c.height) p.vy *= -1;
    }

    // Conecta cercanas
    for (let i=0;i<N;i++){
      for (let j=i+1;j<N;j++){
        const a=particles[i], b=particles[j];
        const dx=a.x-b.x, dy=a.y-b.y; const d=Math.hypot(dx,dy);
        const R=120*DPR;
        if (d<R){
          ctx.strokeStyle = `rgba(34,211,238,${(1 - d/R)*0.25})`;
          ctx.lineWidth = DPR*0.6;
          ctx.beginPath(); ctx.moveTo(a.x,a.y); ctx.lineTo(b.x,b.y); ctx.stroke();
        }
      }
    }

    // Dots
    ctx.fillStyle='rgba(226,232,240,0.9)';
    for (const p of particles){ ctx.beginPath(); ctx.arc(p.x,p.y,1.2*DPR,0,Math.PI*2); ctx.fill(); }

    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
})();
