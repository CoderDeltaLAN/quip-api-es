;(() => {
  const ROOT = document.getElementById('bg') || (() => {
    const d=document.createElement('div'); d.id='bg'; document.body.appendChild(d); return d;
  })();
  const cvs = document.createElement('canvas'); ROOT.appendChild(cvs);
  const ctx = cvs.getContext('2d');
  const DPR = Math.min(window.devicePixelRatio || 1, 2);
  let W=0,H=0;
  function resize(){ W=cvs.width=Math.floor(innerWidth*DPR); H=cvs.height=Math.floor(innerHeight*DPR);
    cvs.style.width=innerWidth+'px'; cvs.style.height=innerHeight+'px'; }
  addEventListener('resize',resize,{passive:true}); resize();

  const CFG={ dots: Math.round((innerWidth*innerHeight)/15000),
    radius: 1.1*DPR, maxDist: 170*DPR, lineWidth: 0.35*DPR,
    lineAlpha:.34, dotAlpha:.52, glow:5,
    color1:'34,211,238', color2:'56,189,248', parallax:.02 };

  const R=(a,b)=>a+Math.random()*(b-a), pts=[];
  for(let i=0;i<CFG.dots;i++) pts.push({x:R(0,W),y:R(0,H),vx:R(-.25,.25)*DPR,vy:R(-.25,.25)*DPR});
  let mx=W/2,my=H/2; addEventListener('mousemove',e=>{mx=(e.clientX||0)*DPR;my=(e.clientY||0)*DPR;},{passive:true});

  function tick(){
    ctx.clearRect(0,0,W,H);
    ctx.fillStyle='rgba(2,6,23,0.86)'; ctx.fillRect(0,0,W,H);

    // puntos brillantes
    ctx.save(); ctx.shadowColor=`rgba(${CFG.color1},.35)`; ctx.shadowBlur=CFG.glow;
    for(const p of pts){
      p.x += p.vx + (mx-W/2)*CFG.parallax*1e-4;
      p.y += p.vy + (my-H/2)*CFG.parallax*1e-4;
      if(p.x<-40||p.x>W+40) p.vx*=-1; if(p.y<-40||p.y>H+40) p.vy*=-1;
      ctx.beginPath(); ctx.globalAlpha=CFG.dotAlpha; ctx.fillStyle=`rgba(${CFG.color1},1)`;
      ctx.arc(p.x,p.y,CFG.radius,0,Math.PI*2); ctx.fill();
    }
    ctx.restore();

    // conexiones ultra finas con degradado y alpha sutil
    ctx.lineWidth=CFG.lineWidth; ctx.globalAlpha=CFG.lineAlpha;
    for(let i=0;i<pts.length;i++){ const a=pts[i];
      for(let j=i+1;j<pts.length;j++){ const b=pts[j];
        const dx=a.x-b.x, dy=a.y-b.y, d=Math.hypot(dx,dy);
        if(d<CFG.maxDist){
          const t=1-d/CFG.maxDist;
          const g=ctx.createLinearGradient(a.x,a.y,b.x,b.y);
          g.addColorStop(0,`rgba(${CFG.color1},${0.18+.45*t})`);
          g.addColorStop(1,`rgba(${CFG.color2},${0.18+.45*t})`);
          ctx.strokeStyle=g; ctx.beginPath(); ctx.moveTo(a.x,a.y); ctx.lineTo(b.x,b.y); ctx.stroke();
        }
      }
    }
    requestAnimationFrame(tick);
  }
  tick();
})();
