(function () {
  'use strict';
  const params = new URLSearchParams(location.search);
  const ordinals = [...document.querySelectorAll('.value')];
  const metrics = [...document.querySelectorAll('.metric')];
  const records = [], mutations = [];
  const observer = new MutationObserver((changes) => {
    mutations.push({at:performance.now(),changes:changes.length,values:ordinals.map(e=>e.textContent)});
  });
  ordinals.forEach(element=>observer.observe(element,{childList:true,characterData:true,subtree:true}));
  const started = performance.now();
  function record(now) {
    const values = ordinals.map(e=>e.textContent);
    records.push({at:Math.round(now-started),ordinals:values,metrics:metrics.map(e=>e.textContent)});
    if(now-started < 15000)requestAnimationFrame(record);
  }
  requestAnimationFrame(record);
  function result() {
    const evidence = {
      mode:params.get('mode')||'scroll',delay:Number(params.get('delay')||0),
      visibleFrames:records.length,badFrames:records.filter(r=>r.ordinals.some(v=>!/^\d{2}$/.test(v))),
      frames:records,mutations,
      final:ordinals.map(e=>e.textContent),metrics:metrics.map(e=>e.textContent)
    };
    document.querySelector('#evidence').textContent=JSON.stringify(evidence);
    document.querySelector('#result').textContent=evidence.badFrames.length?'FAIL: unpadded paint sample':'PASS: all animation-frame samples contain two digits';
  }
  setInterval(result,250);
  document.querySelector('#start').addEventListener('click',()=>document.querySelector('#numbers').scrollIntoView());
  document.querySelector('#return').addEventListener('click',()=>window.scrollTo(0,0));
  document.querySelector('#repeat').addEventListener('click',()=>{
    const script=document.createElement('script');script.src='/formatter.js';document.body.append(script);
  });
  if(params.get('mode')==='in-view')document.querySelector('#numbers').scrollIntoView();
  if(params.get('mode')==='missing')return;
  setTimeout(()=>{
    const script=document.createElement('script');
    script.src='https://cdn.jsdelivr.net/npm/@finsweet/attributes-numbercount@1.2.1/numbercount.js';
    script.onload=()=>{
      for(const init of window.Webflow||[])init();
      document.querySelector('#result').textContent='Library loaded; waiting for scrolling / animation';
    };
    script.onerror=()=>{document.querySelector('#result').textContent='Library unavailable; source fallback remains';};
    document.body.append(script);
  },Number(params.get('delay')||0));
})();
