document.querySelectorAll('form[data-confirm]').forEach(form=>form.addEventListener('submit',e=>{if(!confirm(form.dataset.confirm))e.preventDefault();}));
setTimeout(()=>document.querySelectorAll('.alerta').forEach(a=>a.classList.add('sumir')),3500);
document.querySelectorAll('.barra span').forEach(bar=>{const width=bar.style.width;bar.style.width='0';requestAnimationFrame(()=>setTimeout(()=>bar.style.width=width,100));});
