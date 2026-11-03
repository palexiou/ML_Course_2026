/* === DAY 2: SAVED VALIDATION RESULTS AND REPRESENTATION CONTROL === */
function bindDayTwoEvaluation() {
    const data=JSON.parse(document.getElementById('day-two-evaluation-data').textContent);
    const B='#0072B2',O='#D55E00',P='#7B4FA3',G='#697782',I='#18344b';
    const colors=[B,O,P],methods=['logistic_regression','random_forest','cnn'],labels=['Logistic regression','Random forest','CNN'];
    const escape=v=>String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
    const text=(x,y,v,size=40,c=I,anchor='middle')=>`<text x="${x}" y="${y}" font-size="${size}" fill="${c}" text-anchor="${anchor}">${escape(v)}</text>`;
    const line=(x,y,x2,y2,c=G,w=3,extra='')=>`<path d="M${x} ${y} L${x2} ${y2}" stroke="${c}" stroke-width="${w}" fill="none" ${extra}/>`;
    const dot=(x,y,c,r=13)=>`<circle cx="${x}" cy="${y}" r="${r}" fill="${c}"/>`;
    const marker=(x,y,i)=>i===0?dot(x,y,colors[i]):i===1?`<rect x="${x-13}" y="${y-13}" width="26" height="26" fill="${colors[i]}"/>`:`<path d="M${x} ${y-17} L${x+17} ${y+13} L${x-17} ${y+13} Z" fill="${colors[i]}"/>`;
    const dna=(seq,x,y,step=43,color=I)=>line(x-20,y+25,x+(seq.length-1)*step+20,y+25,'#c3d0da')+[...seq].map((b,i)=>text(x+i*step,y,b,34,color)).join('');
    const checkpoints=[];
    document.querySelectorAll('[data-evaluation]').forEach(panel=>{
        const kind=panel.dataset.evaluation,draw=panel.querySelector('[data-eval-draw]'),read=panel.querySelector('[data-eval-readout]');
        const initial=draw.innerHTML;
        let state={row:0,channel:0,revealed:false,metric:'roc_auc',variant:'simple',swapped:false,keep:false};
        function chart() {
            const key=kind==='training'?'training_loss':'validation_roc_auc',history=data.histories.simple;
            const ymax=key==='training_loss'?Math.ceil(Math.max(...history.map(h=>h[key]))*10)/10:1;
            const x=v=>260+(v-1)/23*1260,y=v=>415-v/ymax*330;
            let s=line(260,415,1550,415,'#afc1ce')+line(260,415,260,65,'#afc1ce');
            for(const e of [1,8,16,24])s+=text(x(e),465,e,30,G);
            for(const v of [0,ymax/2,ymax])s+=text(225,y(v)+10,v.toFixed(2),29,G,'end');
            s+=text(880,535,'Epoch',34,G)+text(270,35,key==='training_loss'?'Training loss':'Validation ROC-AUC',37,G,'start');
            s+=`<polyline points="${history.map(h=>`${x(h.epoch)},${y(h[key])}`).join(' ')}" stroke="${key==='training_loss'?B:O}" stroke-width="6" fill="none"/>`;
            for(const h of history)s+=dot(x(h.epoch),y(h[key]),key==='training_loss'?B:O,5);
            if(state.revealed){
                const best=data.selected_epochs.simple,h=history[best-1];s+=line(x(best),70,x(best),415,B,3,'stroke-dasharray="9 9"')+`<circle cx="${x(best)}" cy="${y(h[key])}" r="14" stroke="${B}" stroke-width="4" fill="white"/>`;
                s+=text(1100,35,`Selected epoch ${best} · final epoch 24`,34,B);
            }
            draw.innerHTML=s;
            read.textContent=kind==='checkpoint'?(state.revealed?`Earliest highest validation ROC-AUC: epoch ${data.selected_epochs.simple}. All 24 epochs ran.`:'Final weights and selected weights need not be the same.'): 'Saved local run · 24 epochs · validation only';
        }
        function metrics() {
            const variant=kind==='paired-metrics'?state.variant:'simple',key=kind==='paired-metrics'?'roc_auc':state.metric;
            let s=line(600,460,1510,460,'#afc1ce')+text(1050,545,key==='roc_auc'?'Validation ROC-AUC':'Validation average precision',36,G);
            for(const v of [0,.5,1])s+=text(600+v*900,490,v.toFixed(1),28,G);
            if(key==='roc_auc')s+=line(1050,70,1050,450,'#b3c3ce',2,'stroke-dasharray="9 9"');
            methods.forEach((method,i)=>{const value=data.metrics.find(r=>r.variant===variant&&r.method===method)[key],yy=120+i*130,xx=600+900*value;s+=text(540,yy+13,labels[i],38,colors[i],'end')+marker(xx,yy,i)+text(xx+35,yy+13,value.toFixed(3),34,colors[i],'start');});
            draw.innerHTML=s;
            read.textContent=variant==='simple'?'Primary PPM · 240 validation records · saved local run':'Fixed-slot order control · 96 validation records · bag ROC-AUC limit 0.5';
            const btn=panel.querySelector('button');if(btn)btn.textContent=kind==='paired-metrics'?(variant==='simple'?'Show order control':'Show primary PPM'):(key==='roc_auc'?'Show average precision':'Show ROC-AUC');
        }
        function prediction() {
            const row=data.primary_examples[state.row],px=340+1060*row.probability;
            let s=dna(row.sequence.slice(0,28),240,80,46)+text(864,175,row.sample_id+' · bases 0–27',32,G);
            s+=line(340,340,1400,340,'#a9bdca',4)+line(870,320,870,360,G,3,'stroke-dasharray="8 7"');
            s+=text(340,410,'0',33,G)+text(870,410,'0.5',33,G)+text(1400,410,'1',33,G)+dot(px,340,B,18)+text(px,275,`p(B) = ${row.probability.toFixed(3)}`,50,B);
            if(state.revealed)s+=text(864,515,`Observed ${row.label?'B':'A'} · predicted ${row.probability>=.5?'B':'A'} at 0.5`,45,O);
            draw.innerHTML=s;read.textContent=`Validation row ${state.row} · selected checkpoint · no refitting`;
        }
        function response() {
            const row=data.primary_examples[state.row],vals=row.responses[state.channel],max=Math.max(...vals,.001),baseline=410;
            let s=text(864,28,row.sample_id+` · channel ${state.channel}`,34,G);
            [...row.sequence].forEach((b,i)=>{const c={A:B,C:P,G:G,T:O}[b],x=200+i*8.4;s+=line(x,65,x,87,c,6);});
            vals.forEach((v,i)=>s+=line(200+i*8.4,baseline,200+i*8.4,baseline-v/max*260,B,4));
            s+=line(200,baseline,1550,baseline,'#b4c4ce');
            for(const v of [0,40,80,120,159])s+=text(200+v*8.4,460,v,28,G);
            s+=text(165,baseline,'0',28,G,'end')+text(165,150,max.toFixed(2),28,G,'end')+text(864,535,'Position (zero-based)',34,G);
            draw.innerHTML=s;read.textContent='Second convolution · post-ReLU · response, not attribution';
        }
        function chance() {
            let s=line(320,370,1440,370,'#b4c4ce');
            for(const v of [.2,.4,.5,.6,.8]){
                const x=320+1120*v;s+=dot(x,250,O,17);
                if(state.revealed)s+=`<rect x="${x-16}" y="294" width="32" height="32" fill="${B}"/>`;
            }
            s+=text(220,265,'A',40,O)+text(220,325,'B',40,B)+text(320,430,'0',32,G)+text(1440,430,'1',32,G)+text(864,490,'Prediction score',38,G);
            if(state.revealed)s+=text(864,80,'Identical distributions → ROC-AUC 0.5',51,B);
            draw.innerHTML=s;read.textContent=state.revealed?'Every score has one A partner and one B partner.':'Reveal the opposite-label partners at the same scores.';
        }
        function head() {
            let s='';
            for(let i=0;i<2;i++){
                const yy=250+i*210,xs=i?[1120,600]:[600,1120];
                s+=line(290,yy,1320,yy,'#bdccd6')+text(180,yy,i?'A':'B',44,i?O:B);
                xs.forEach((x,j)=>{s+=line(x,yy,x,yy-100,colors[j],9)+text(x,yy-130,j?'CGGACGTC':'TATAAATG',32,colors[j]);});
                s+=text(1500,yy,state.keep?(i?'different':'slots kept'):'same max',37,state.keep?B:G);
            }
            s+=text(864,55,state.keep?'Position-indexed features remain available':'A strongest-response summary discards the swap',43,B);
            draw.innerHTML=s;read.textContent=state.keep?'Actual model: flattened positions + per-channel maxima.':'This local stack cannot span the distant motifs; its maxima lose this fixed-slot cue.';
        }
        function pair() {
            const pair=data.control_pairs[state.row],records=[...pair.records].sort((a,b)=>b.label-a.label);
            let s=text(864,30,pair.group_id,32,G);
            for(let i=0;i<2;i++){
                const r=records[i],yy=125+i*140;s+=text(160,yy,r.label?'B':'A',43,r.label?B:O);
                s+=dna(r.sequence.slice(38,46),350,yy,45,r.label?B:O)+dna(r.sequence.slice(86,94),1030,yy,45,r.label?O:B);
            }
            if(state.revealed){
                methods.forEach((method,i)=>{let yy=365+i*70;const a=records[0][method+'_probability'],b=records[1][method+'_probability'];s+=text(680,yy,labels[i],33,colors[i],'end')+text(925,yy,'B '+a.toFixed(4),35,B)+text(1270,yy,'A '+b.toFixed(4),35,O);});
            } else s+=text(864,430,'Complete 4-mer Counters: equal',48,B)+text(864,510,'157 overlapping windows per sequence',36,G);
            draw.innerHTML=s;read.textContent=state.revealed?'Same bag scores within each pair; CNN probabilities are observed local results.':'Shared background · opposite labels · complete count equality verified';
        }
        function swap() {
            // Reuse the authored paired ribbons; swap only the two displayed class labels.
            draw.innerHTML=initial;
            if(state.swapped){const texts=[...draw.querySelectorAll('text')];for(const t of texts){if(Number(t.getAttribute('x'))!==130)continue;if(t.textContent==='B')t.textContent='A';else if(t.textContent==='A')t.textContent='B';}}
            read.textContent=state.swapped?'Reverse the arrangement, reverse the construction label.':'B: first order · A: reverse order';
            // Actual motif movement is handled as a transform of each letter group below.
            if(state.swapped){
                [...draw.querySelectorAll('text')].filter(t=>['A','C','G','T'].includes(t.textContent)&&Number(t.getAttribute('x'))>250).forEach(t=>{const x=Number(t.getAttribute('x'));t.setAttribute('x',x<900?x+530:x-530);});
                [...draw.querySelectorAll('circle')].forEach(c=>{const x=Number(c.getAttribute('cx'));c.setAttribute('cx',x<900?x+530:x-530);});
            }
        }
        function render(){
            if(['training','validation','checkpoint'].includes(kind))chart();
            else if(['metrics','paired-metrics'].includes(kind))metrics();
            else if(kind==='prediction')prediction();else if(kind==='response')response();else if(kind==='chance')chance();else if(kind==='head')head();else if(kind==='pair')pair();else if(kind==='swap')swap();
        }
        panel.querySelectorAll('[data-eval-action]').forEach(btn=>btn.addEventListener('click',()=>{
            const action=btn.dataset.evalAction;
            if(['label','checkpoint','partners','pair-reveal'].includes(action))state.revealed=!state.revealed;
            if(action==='row'||action==='pair'){state.row=(state.row+1)%3;state.revealed=false;}
            if(action==='metric')state.metric=state.metric==='roc_auc'?'average_precision':'roc_auc';
            if(action==='variant')state.variant=state.variant==='simple'?'interaction':'simple';
            if(action==='head'){state.keep=!state.keep;btn.textContent=state.keep?'Summarize maxima':'Keep the positions';}
            if(action==='swap')state.swapped=!state.swapped;
            render();
        }));
        panel.querySelector('[data-eval-row]')?.addEventListener('change',e=>{state.row=Number(e.target.value);render();});
        panel.querySelector('[data-eval-channel]')?.addEventListener('change',e=>{state.channel=Number(e.target.value);render();});
        checkpoints.push({get:()=>({...state}),set:s=>{state={...s};render();},end:()=>({...state,revealed:true,variant:kind==='paired-metrics'?'interaction':state.variant,keep:true})});
        render();
    });
    let saved;
    addEventListener('beforeprint',()=>{saved=checkpoints.map(p=>p.get());checkpoints.forEach(p=>p.set(p.end()));});
    addEventListener('afterprint',()=>{if(saved)checkpoints.forEach((p,i)=>p.set(saved[i]));saved=null;});
}
