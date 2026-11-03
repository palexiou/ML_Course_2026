/* === DETERMINISTIC TEACHING INTERACTIONS: NO MODEL OR NETWORK CALLS === */
const lessonColors={blue:'#0072B2',orange:'#D55E00',ink:'#18344b',gray:'#697782'};
const lessonGroups=[[.95,8,2],[.85,8,2],[.75,7,3],[.65,7,3],[.45,6,4],[.35,5,5],[.25,4,6],[.15,3,7],[.08,1,9],[.02,1,9]];
const lessonScores=lessonGroups.flatMap(([p,b,a])=>Array.from({length:b+a},(_,i)=>({p,y:i<b?1:0})));
function lessonText(x,y,s,size=35,color=lessonColors.ink,anchor='middle'){return `<text x="${x}" y="${y}" font-size="${size}" fill="${color}" text-anchor="${anchor}">${s}</text>`;}
function lessonSVG(s,label){return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1728 540" role="img" aria-label="${label}"><title>${label}</title>${s}</svg>`;}
function lessonLine(x1,y1,x2,y2,color=lessonColors.gray,width=3){return `<path d="M${x1} ${y1}L${x2} ${y2}" fill="none" stroke="${color}" stroke-width="${width}"/>`;}
function dayOneMetrics(t){let tp=0,fp=0,tn=0,fn=0;lessonScores.forEach(({p,y})=>{if(p>=t){if(y)tp++;else fp++;}else if(y)fn++;else tn++;});return{tp,fp,tn,fn,accuracy:(tp+tn)/100,precision:tp+fp?tp/(tp+fp):null,recall:tp/(tp+fn),f1:2*tp+fp+fn?2*tp/(2*tp+fp+fn):0};}
const lessonPercent=x=>x===null?'undefined':(100*x).toFixed(1)+'%';
function lessonGradientLoss(w){return [-2,-1,1,2].reduce((s,x,i)=>{const z=w*x,y=[0,1,0,1][i];return s+Math.max(z,0)+Math.log1p(Math.exp(-Math.abs(z)))-y*z;},0)/4;}
function lessonGradient(w){return [-2,-1,1,2].reduce((s,x,i)=>s+x*(1/(1+Math.exp(-w*x))-[0,1,0,1][i]),0)/4;}
function updateLesson(root){
 const mode=root.dataset.live,plot=root.querySelector('[data-live-plot]'),read=root.querySelector('[data-live-readout]');let s='';
 if(mode==='sigmoid'){
  const z=Number(root.querySelector('input').value),p=1/(1+Math.exp(-z)),X=z=>300+(z+6)/12*1100,Y=p=>450-380*p;
  s=lessonLine(300,50,300,450)+lessonLine(300,450,1400,450);
  const pts=Array.from({length:121},(_,i)=>{let z=-6+i/10;return `${X(z)},${Y(1/(1+Math.exp(-z)))}`;}).join(' ');
  s+=`<polyline points="${pts}" fill="none" stroke="${lessonColors.blue}" stroke-width="7"/><circle cx="${X(z)}" cy="${Y(p)}" r="15" fill="${lessonColors.orange}"/>`;
  s+=lessonText(850,530,'Score z',32)+lessonText(160,90,'P(B)',38)+lessonText(265,85,'1',30)+lessonText(265,455,'0',30)+lessonText(300,480,'−6',28)+lessonText(850,480,'0',28)+lessonText(1400,480,'6',28);
  plot.innerHTML=lessonSVG(s,'Sigmoid maps score to class probability');read.textContent=`z = ${z.toFixed(1)} → P(B) = ${p.toFixed(3)}; P(A) = ${(1-p).toFixed(3)}`;
 }else if(mode==='gradient'){
  const k=Number(root.dataset.step||0);let w=-2;for(let i=0;i<k;i++)w-=.8*lessonGradient(w);
  const X=w=>300+(w+3)/6*1100,Y=l=>450-l*145;
  const pts=Array.from({length:121},(_,i)=>{let w=-3+i/20;return `${X(w)},${Y(lessonGradientLoss(w))}`;}).join(' ');
  s=lessonLine(300,50,300,450)+lessonLine(300,450,1400,450)+`<polyline points="${pts}" fill="none" stroke="${lessonColors.blue}" stroke-width="7"/><circle cx="${X(w)}" cy="${Y(lessonGradientLoss(w))}" r="16" fill="${lessonColors.orange}"/>`;
  s+=lessonText(850,530,'One weight w · other parameters held fixed',32)+lessonText(800,45,'Mean training loss',38)+lessonText(300,480,'−3',28)+lessonText(850,480,'0',28)+lessonText(1400,480,'3',28);
  plot.innerHTML=lessonSVG(s,'One-weight logistic training-loss gradient descent');read.textContent=`Step ${k} · w = ${w.toFixed(3)} · Mean loss = ${lessonGradientLoss(w).toFixed(3)}`;root.querySelector('[data-step]').disabled=k>=8;
 }else if(mode==='threshold'){
  const t=Number(root.querySelector('input').value),m=dayOneMetrics(t),X=p=>260+p*1150;
  lessonScores.forEach(({p,y},i)=>{const yy=90+(i%10)*29;s+=`<${y?'circle':'rect'} ${y?`cx="${X(p)}" cy="${yy}" r="10"`:`x="${X(p)-9}" y="${yy-9}" width="18" height="18"`} fill="${y?lessonColors.orange:lessonColors.blue}"/>`;});
  s+=lessonLine(260,410,1410,410)+lessonLine(X(t),50,X(t),410,lessonColors.orange,5)+lessonText(260,455,'0',30)+lessonText(835,455,'0.5',30)+lessonText(1410,455,'1',30)+lessonText(835,510,'P(B) · square A / circle B',38);
  plot.innerHTML=lessonSVG(s,'Fixed class probabilities with a movable decision cutoff');read.textContent=`TP ${m.tp} · FP ${m.fp} · FN ${m.fn} · TN ${m.tn} · Precision ${lessonPercent(m.precision)} · Recall ${lessonPercent(m.recall)}`;
 }else if(mode==='curve'){
  const t=Number(root.querySelector('input').value),m=dayOneMetrics(t),pr=root.dataset.curve==='pr',X=x=>390+x*950,Y=y=>440-y*360;
  const states=[{recall:0,precision:1,fp:0},...lessonGroups.map(([p])=>dayOneMetrics(p))];
  const xy=states.map(m=>[X(pr?m.recall:m.fp/50),Y(pr?m.precision:m.recall)]);
  const d=xy.map(([x,y],i)=>`${i?'L':'M'}${x} ${y}`).join(' ');
  s=lessonLine(390,60,390,440)+lessonLine(390,440,1340,440);
  if(!pr)s+=`<path d="M390 440 L1340 80" stroke="#a9b7c1" stroke-width="3" stroke-dasharray="10 8"/>`;
  else s+=`<path d="M390 ${Y(.5)} L1340 ${Y(.5)}" stroke="#a9b7c1" stroke-width="3" stroke-dasharray="10 8"/>`;
  if(root.dataset.area==='1')s+=`<path d="${d}L1340 440Z" fill="${lessonColors.blue}" opacity=".12"/>`;
  s+=`<path d="${d}" fill="none" stroke="${lessonColors.blue}" stroke-width="6"/>`;
  if(!pr||m.precision!==null)s+=`<circle cx="${X(pr?m.recall:m.fp/50)}" cy="${Y(pr?m.precision:m.recall)}" r="15" fill="${lessonColors.orange}"/>`;
  s+=lessonText(865,515,pr?'Recall':'False-positive rate = FP / actual A',37)+lessonText(865,40,pr?'Precision':'True-positive rate (recall)',37);
  s+=lessonText(355,445,'0',28)+lessonText(355,90,'1',28)+lessonText(390,480,'0',28)+lessonText(1340,480,'1',28);
  plot.innerHTML=lessonSVG(s,pr?'Precision–recall curve of the constructed batch':'ROC curve of the constructed batch');
  read.textContent=pr?`Precision ${lessonPercent(m.precision)} · Recall ${lessonPercent(m.recall)} · AP = 0.731`:`FPR = ${(m.fp/50).toFixed(2)} · TPR = ${m.recall.toFixed(2)} · ROC-AUC = 0.784`;
 }else if(mode==='tree'){
  const a=Number(root.querySelector('[data-tree-a]').value),b=Number(root.querySelector('[data-tree-b]').value),p=a>=2?(b<2?.8:.25):.2;
  const box=(x,y,w,label,active)=>`<rect x="${x}" y="${y}" width="${w}" height="82" rx="17" fill="${active?'#FBE9D9':'#f2f6f9'}" stroke="${active?lessonColors.orange:'#c3d0d8'}" stroke-width="4"/>`+lessonText(x+w/2,y+53,label,36);
  s=lessonLine(864,118,450,225)+lessonLine(864,118,1190,225)+lessonLine(1190,307,970,425)+lessonLine(1190,307,1480,425);
  s+=box(624,36,480,'TATA ≥ 2?',true)+box(210,225,480,'P(B) = 0.20',a<2)+box(950,225,480,'CGCG < 2?',a>=2)+box(750,425,440,'P(B) = 0.80',a>=2&&b<2)+box(1260,425,440,'P(B) = 0.25',a>=2&&b>=2);
  s+=lessonText(540,180,'No',30)+lessonText(1090,180,'Yes',30)+lessonText(990,365,'Yes',30)+lessonText(1430,365,'No',30);
  plot.innerHTML=lessonSVG(s,'Interactive constructed classification tree');read.textContent=`TATA ${a} · CGCG ${b} → P(B) = ${p.toFixed(2)} → class ${p>=.5?'B':'A'}`;
 }
}
function bindDayOneInteractions(){document.querySelectorAll('[data-live]').forEach(root=>{updateLesson(root);root.querySelectorAll('input').forEach(el=>el.addEventListener('input',()=>updateLesson(root)));root.querySelector('[data-step]')?.addEventListener('click',()=>{root.dataset.step=String(Number(root.dataset.step||0)+1);updateLesson(root);});root.querySelector('[data-reset]')?.addEventListener('click',()=>{root.dataset.step='0';if(root.dataset.live==='tree'){root.querySelector('[data-tree-a]').value=2;root.querySelector('[data-tree-b]').value=3;}updateLesson(root);});});}
