/* Constructed detector/readout examples; inlined in the offline deck. */
function bindDayTwoSequence() {
    const BLUE='#0072B2',ORANGE='#D55E00',GRAY='#697782',INK='#18344b',PURPLE='#7B4FA3';
    const colors=[ORANGE,BLUE,PURPLE],names=['CCG','GTC','TCC'],sequence='ACCGTCCG';
    const maps=[[0,1,0,0,0,1],[0,0,0,1,0,0],[0,0,0,0,1,0]];
    const q=(p,s)=>p.querySelector(s),qa=(p,s)=>[...p.querySelectorAll(s)];
    const read=(p,s)=>{const el=q(p,'[data-sequence-readout]');if(el)el.textContent=s;};
    const txt=(x,y,value,size=40,color=INK,anchor='middle')=>`<text x="${x}" y="${y}" font-size="${size}" fill="${color}" text-anchor="${anchor}">${value}</text>`;
    const line=(x,y,x2,y2,color=GRAY,width=3)=>`<path d="M${x} ${y} L${x2} ${y2}" stroke="${color}" stroke-width="${width}" fill="none"/>`;
    const detector=(seq,target='CCG',padding=0)=>Array.from({length:seq.length-2+2*padding},(_,i)=>[...target].reduce((score,b,j)=>score+Number(seq[i-padding+j]===b),-2));
    function matrix(seq,x=330,y=150,step=140,row=65) {
        let s='';[...'ACGT'].forEach((b,c)=>{const yy=y+c*row;s+=txt(x-80,yy+10,b,35,GRAY,'end');[...seq].forEach((v,j)=>{const on=v===b,xx=x+j*step;if(on)s+=`<circle cx="${xx}" cy="${yy}" r="22" fill="${ORANGE}" fill-opacity=".12" stroke="${ORANGE}" stroke-width="2"/>`;s+=txt(xx,yy+10,Number(on),30,on?INK:'#a3b1ba');});});return s;
    }
    function track(values,x=440,y=310,step=140,label='',color=BLUE,upto=999) {
        let s=line(x-25,y,x+(values.length-1)*step+25,y,'#bccbd5');if(label)s+=txt(x-70,y-35,label,38,color,'end');
        values.forEach((v,i)=>{const xx=x+i*step;s+=`<g opacity="${i<=upto?1:.12}">`+(v?line(xx,y,xx,y-80*v,color,8):'')+`<circle cx="${xx}" cy="${y-80*v}" r="${v?11:5}" fill="${color}"/></g>`+txt(xx,y+45,i,27,GRAY);});return s;
    }
    function inspect(seq,padded=false) {
        const shown=padded?[null,...seq,null]:[...seq],x=padded?300:400,step=padded?125:130;
        let s=shown.map((b,i)=>txt(x+i*step,65,b||'zeros',b?44:25,b?INK:GRAY)).join('')+matrix(shown,x,145,step,60);
        const vals=detector(seq,'CCG',Number(padded)).map(z=>Math.max(0,z));s+=track(vals,padded?300:530,480,padded?125:130,'',ORANGE);return s;
    }
    function baseView(base) {
        let s=txt(430,330,base,170,BLUE)+line(610,275,820,275);[...'ACGT'].forEach((b,i)=>{const y=130+i*100;s+=txt(1000,y+15,b,46,GRAY)+`<circle cx="1160" cy="${y}" r="32" fill="white" stroke="${b===base?ORANGE:'#a9bac6'}" stroke-width="5"/>`+txt(1160,y+13,Number(b===base),40,b===base?ORANGE:GRAY);});return s;
    }
    const printStates=[];
    document.querySelectorAll('[data-scene]').forEach(panel=>{
        const kind=panel.dataset.scene;
        if(kind==='base')qa(panel,'[data-base]').forEach(button=>button.addEventListener('click',()=>{const b=button.dataset.base;q(panel,'[data-draw="base"]').innerHTML=baseView(b);qa(panel,'[data-base]').forEach(el=>el.setAttribute('aria-pressed',String(el===button)));read(panel,`${b} → (${[...'ACGT'].map(x=>Number(x===b)).join(', ')})`);}));
        if(kind==='matrix') {
            let i=0;const show=()=>{q(panel,'[data-column]').setAttribute('x',355+i*130);read(panel,`Position ${i} · ${sequence[i]} → (${[...'ACGT'].map(x=>Number(x===sequence[i])).join(', ')}) · 4 channels × 8 positions`);};
            q(panel,'[data-next-column]').addEventListener('click',()=>{i=(i+1)%8;show();});q(panel,'[data-reset-column]').addEventListener('click',()=>{i=0;show();});
        }
        if(kind==='score') {
            let stage=0;const show=()=>{qa(panel,'[data-calculation]').forEach((g,i)=>g.style.opacity=stage>i?1:.12);q(panel,'[data-score-next]').disabled=stage===2;q(panel,'[data-score-next]').textContent=['Reveal the sum','Apply ReLU','Activation computed'][stage];read(panel,['Multiply corresponding entries, then add the bias.','1 + 1 + 1 − 2 = 1','ReLU(1) = 1 · a feature value, not a class probability'][stage]);};
            q(panel,'[data-score-next]').addEventListener('click',()=>{stage=Math.min(2,stage+1);show();});q(panel,'[data-score-reset]').addEventListener('click',()=>{stage=0;show();});printStates.push({get:()=>stage,set:v=>{stage=v;show();},end:2});
        }
        if(kind==='scan') {
            let start=0;const scores=detector(sequence),values=scores.map(z=>Math.max(0,z));
            const show=()=>{q(panel,'[data-window]').setAttribute('x',260+start*140);q(panel,'[data-draw="scan-map"]').innerHTML=track(values,460,420,140,'',BLUE,start);q(panel,'[data-scan-next]').disabled=start===5;read(panel,`Start ${start} · ${sequence.slice(start,start+3)} · score ${scores[start]} → activation ${values[start]}`);};
            q(panel,'[data-scan-next]').addEventListener('click',()=>{start=Math.min(5,start+1);show();});q(panel,'[data-scan-reset]').addEventListener('click',()=>{start=0;show();});printStates.push({get:()=>start,set:v=>{start=v;show();},end:5});
        }
        if(kind==='padding') {
            let padded=false;const show=()=>{q(panel,'[data-draw="inspection"]').innerHTML=inspect(sequence,padded);q(panel,'[data-padding-toggle]').textContent=padded?'Remove zero padding':'Add zero padding';read(panel,padded?'Zero padding · 8 bases → 8 outputs aligned to position centers':'No padding · 8 bases → 6 valid-window outputs');};
            q(panel,'[data-padding-toggle]').addEventListener('click',()=>{padded=!padded;show();});
        }
        if(kind==='inspection') {
            let changed=false;const show=()=>{const seq=changed?'ACTGTCCG':sequence,values=detector(seq).map(z=>Math.max(0,z));q(panel,'[data-draw="inspection"]').innerHTML=inspect(seq);q(panel,'[data-mutate]').disabled=changed;read(panel,`${seq} → (${values.join(', ')})`);};
            q(panel,'[data-mutate]').addEventListener('click',()=>{changed=true;show();});q(panel,'[data-mutation-reset]').addEventListener('click',()=>{changed=false;show();});
        }
        if(kind==='global-max') {
            let shown=false;const show=()=>{q(panel,'[data-pool-result]').style.opacity=shown?1:.12;q(panel,'[data-pool-reveal]').disabled=shown;read(panel,shown?'max(0, 1, 0, 0, 0, 1) = 1 · no coordinate or count returned':'Two tied peaks; one maximum value.');};
            q(panel,'[data-pool-reveal]').addEventListener('click',()=>{shown=true;show();});printStates.push({get:()=>shown,set:v=>{shown=v;show();},end:true});
        }
        if(kind==='pool-channels') {
            let count=1;const show=()=>{qa(panel,'[data-channel]').forEach(g=>g.style.opacity=Number(g.dataset.channel)<count?1:.12);q(panel,'[data-next-channel]').disabled=count===3;read(panel,`One maximum per channel → (${Array(count).fill(1).join(', ')})`);};
            q(panel,'[data-next-channel]').addEventListener('click',()=>{count=Math.min(3,count+1);show();});q(panel,'[data-reset-channels]').addEventListener('click',()=>{count=1;show();});printStates.push({get:()=>count,set:v=>{count=v;show();},end:3});
        }
        if(kind==='pool-limit') {
            let step=0;const cases=[maps[0],[0,0,1,0,0,1],[0,0,1,0,0,0]],show=()=>{const values=cases[step];q(panel,'[data-draw="moving-map"]').innerHTML=track(values,300,300,160,'CCG',ORANGE);q(panel,'[data-move-peak]').textContent=['Move first peak','Remove tied peak','Summary still unchanged'][step];q(panel,'[data-move-peak]').disabled=step===2;read(panel,`CCG map (${values.join(', ')}) · pooled vector stays (1, 1, 1)`);};
            q(panel,'[data-move-peak]').addEventListener('click',()=>{step=Math.min(2,step+1);show();});q(panel,'[data-map-reset]').addEventListener('click',()=>{step=0;show();});
        }
        if(kind==='flatten') {
            let count=0;const show=()=>{qa(panel,'[data-flat-channel]').forEach(g=>g.style.opacity=Number(g.dataset.flatChannel)<count?1:.12);q(panel,'[data-flatten-next]').disabled=count===3;read(panel,count?`${count*6} ordered entries · ${names.slice(0,count).join(' → ')} · channel-major order`:'Preserve each channel-position slot in the ordered ribbon.');};
            q(panel,'[data-flatten-next]').addEventListener('click',()=>{count=Math.min(3,count+1);show();});q(panel,'[data-flatten-reset]').addEventListener('click',()=>{count=0;show();});printStates.push({get:()=>count,set:v=>{count=v;show();},end:3});
        }
        if(kind==='position') {
            let moved=false;const show=()=>{const values=moved?[0,0,1,0,0,1]:maps[0],weights=[0,1.2,-.4,0,0,.3],z=values.reduce((s,v,i)=>s+v*weights[i],-.5);q(panel,'[data-draw="position-map"]').innerHTML=track(values,260,200,160,'',ORANGE);q(panel,'[data-position-score]').textContent=`score = ${z.toFixed(1)}`;q(panel,'[data-position-feature]').textContent=`ReLU → ${Math.max(0,z).toFixed(1)}`;q(panel,'[data-position-toggle]').textContent=moved?'Restore peak to position 1':'Move peak to position 2';read(panel,`Pooled maximum = 1 · positional hidden feature = ${Math.max(0,z).toFixed(1)} · bias −0.5`);};
            q(panel,'[data-position-toggle]').addEventListener('click',()=>{moved=!moved;show();});
        }
        if(kind==='branches') {
            let step=0;const show=()=>{['flat','pool','join'].forEach((key,i)=>q(panel,`[data-branch="${key}"]`).style.opacity=step>=i?1:.12);q(panel,'[data-branch-next]').disabled=step===2;q(panel,'[data-branch-next]').textContent=['Reveal global max branch','Join the features','Branches joined'][step];read(panel,['18 ordered values from the same maps','3 strongest-response values, one per channel','18 + 3 = 21 features · actual model: 2560 + 16 = 2576'][step]);};
            q(panel,'[data-branch-next]').addEventListener('click',()=>{step=Math.min(2,step+1);show();});q(panel,'[data-branch-reset]').addEventListener('click',()=>{step=0;show();});printStates.push({get:()=>step,set:v=>{step=v;show();},end:2});
        }
        if(kind==='probability') {
            let shown=false;const show=()=>{q(panel,'[data-class-result]').style.opacity=shown?1:.12;q(panel,'[data-class-reveal]').disabled=shown;read(panel,shown?'z = 0.3 → P(B) ≈ 0.574 → class B at cutoff 0.5':'A logit becomes a probability; a cutoff then gives a class.');};
            q(panel,'[data-class-reveal]').addEventListener('click',()=>{shown=true;show();});printStates.push({get:()=>shown,set:v=>{shown=v;show();},end:true});
        }
        if(kind==='architecture') {
            let step=0;const descriptions=['Follow one sequence through the actual model.','Input: batch × 4 × 160','Conv7/ReLU → Conv5/ReLU: batch × 16 × 160','Flatten 2560 + global max 16 → 2576 features','Dense + ReLU → 32 hidden features','Final linear → one logit; inference sigmoid → P(B)'];
            const show=()=>{qa(panel,'[data-route]').forEach(g=>g.style.opacity=!step||Number(g.dataset.route)===step?1:.15);q(panel,'[data-route-next]').disabled=step===5;read(panel,descriptions[step]);};
            q(panel,'[data-route-next]').addEventListener('click',()=>{step=Math.min(5,step+1);show();});q(panel,'[data-route-reset]').addEventListener('click',()=>{step=0;show();});printStates.push({get:()=>step,set:v=>{step=v;show();},end:0});
        }
        if(kind==='learned') {
            let step=0;const descriptions=['First convolution: fitted local weights and biases','Second convolution: fitted weights combine local feature channels','Dense hidden and output layers have fitted weights and biases','Convolution and dense parameters are fitted; encoding, activations, max, flatten and join follow fixed rules'];
            const show=()=>{qa(panel,'[data-route]').forEach(g=>g.style.opacity=.2);qa(panel,'[data-module]').forEach(g=>{const m=g.dataset.module,on=step===3||(step===0&&m==='conv7')||(step===1&&m==='conv5')||(step===2&&['dense','output'].includes(m));g.style.opacity=on?1:.2;q(g,'[data-theta]').style.opacity=on?1:.12;});q(panel,'[data-learned-next]').disabled=step===3;read(panel,descriptions[step]);};
            q(panel,'[data-learned-next]').addEventListener('click',()=>{step=Math.min(3,step+1);show();});q(panel,'[data-learned-reset]').addEventListener('click',()=>{step=0;show();});show();printStates.push({get:()=>step,set:v=>{step=v;show();},end:3});
        }
        if(kind==='discussion') {
            let moved=false;q(panel,'[data-discussion-move]').addEventListener('click',()=>{moved=!moved;const values=moved?[0,0,1,0,0,1]:maps[0];q(panel,'[data-draw="discussion-map"]').innerHTML=track(values,440,460,140,'',ORANGE);read(panel,`Maximum = 1 · ordered values = (${values.join(', ')})`);});
        }
    });
    let saved=[];
    addEventListener('beforeprint',()=>{saved=printStates.map(s=>s.get());printStates.forEach(s=>s.set(s.end));});
    addEventListener('afterprint',()=>printStates.forEach((s,i)=>s.set(saved[i])));
}
