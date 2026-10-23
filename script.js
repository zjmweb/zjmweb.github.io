document.documentElement.classList.add('js');
// A lightweight heritage scene: pointer parallax and keyboard-accessible chapters.
const heritage=document.querySelector('.heritage-lab');
if(heritage){
  const chapters={objects:['Every object holds a story.','A vessel, a trace, a memory — a starting point for cultural discovery.'],stories:['Stories connect us across time.','Poetry, play and shared memories bring cultural knowledge into the present.'],worlds:['Step into another perspective.','Immersive spaces invite us to explore, question and experience heritage.']};
  heritage.querySelectorAll('[data-story]').forEach(button=>button.addEventListener('click',()=>{const key=button.dataset.story;heritage.dataset.active=key;heritage.querySelectorAll('[data-story]').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));heritage.querySelector('h2').textContent=chapters[key][0];heritage.querySelector('.scene-description').textContent=chapters[key][1];}));
  const motion=matchMedia('(prefers-reduced-motion: reduce)');
  const fine=matchMedia('(hover: hover) and (pointer: fine)');
  const layers=[...heritage.querySelectorAll('[data-depth]')];
  let frame=0,px=0,py=0;
  function renderScene(){layers.forEach(layer=>{const depth=Number(layer.dataset.depth);layer.style.transform=`translate(${px*depth*8}px,${py*depth*6}px)`;});frame=0;}
  heritage.addEventListener('pointermove',event=>{if(motion.matches||!fine.matches)return;const box=heritage.getBoundingClientRect();px=(event.clientX-box.left)/box.width-.5;py=(event.clientY-box.top)/box.height-.5;if(!frame)frame=requestAnimationFrame(renderScene);});
  function resetScene(){px=py=0;if(frame)cancelAnimationFrame(frame);frame=0;layers.forEach(layer=>layer.style.transform='');}
  heritage.addEventListener('pointerleave',resetScene);motion.addEventListener('change',resetScene);
}
const menuButton=document.querySelector('.menu-toggle');
const navigation=document.querySelector('.nav');
function closeMenu(){navigation?.classList.remove('is-open');menuButton?.setAttribute('aria-expanded','false');}
menuButton?.addEventListener('click',()=>{const open=menuButton.getAttribute('aria-expanded')!=='true';menuButton.setAttribute('aria-expanded',String(open));navigation.classList.toggle('is-open',open);});
document.addEventListener('keydown',event=>{if(event.key==='Escape'&&menuButton?.getAttribute('aria-expanded')==='true'){closeMenu();menuButton.focus();}});
document.querySelectorAll('[data-filter]').forEach(button=>button.addEventListener('click',()=>{const filter=button.dataset.filter;document.querySelectorAll('[data-filter]').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));let count=0;document.querySelectorAll('.project[data-category]').forEach(project=>{project.hidden=filter!=='all'&&project.dataset.category!==filter;if(!project.hidden)count++;});document.querySelector('#filter-status').textContent=`${count} project${count===1?'':'s'} shown.`;}));
document.querySelector('.copy-button')?.addEventListener('click',async()=>{const status=document.querySelector('.copy-status');try{if(!navigator.clipboard)throw new Error('Clipboard unavailable');await navigator.clipboard.writeText('Zjmweb0805@163.com');status.textContent='Email address copied.';}catch{status.textContent='Please select and copy the email address above, or choose “Send an email”.';}});
document.querySelectorAll('.video-play').forEach(button=>button.addEventListener('click',()=>{const shell=button.closest('.video-shell');const video=shell.dataset.video;if(!/^[A-Za-z0-9_-]{11}$/.test(video))return;const iframe=document.createElement('iframe');iframe.src=`https://www.youtube-nocookie.com/embed/${video}?autoplay=1`;iframe.title=`${shell.dataset.title} — project film`;iframe.allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';iframe.allowFullscreen=true;iframe.referrerPolicy='strict-origin-when-cross-origin';shell.replaceChildren(iframe);}));
