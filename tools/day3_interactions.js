/* === DAY 3: TEACHING INTERACTIONS, NO SCIENTIFIC EXECUTION === */
function bindDayThree() {
    const evidence = JSON.parse(document.getElementById('day-three-evidence').textContent);
    const B='#0072B2', O='#D55E00', G='#697782', P='#7B4FA3';
    const methods=[['logistic_regression','Counts + logistic',B],['random_forest','Counts + forest',O],['cnn','CNN',P],['foundation','Frozen NT + logistic',G]];
    const ns='http://www.w3.org/2000/svg';
    function node(parent, tag, attrs, value) {
        const e=document.createElementNS(ns,tag);
        Object.entries(attrs).forEach(([k,v])=>e.setAttribute(k,String(v)));
        if(value!==undefined)e.textContent=value;
        parent.appendChild(e);return e;
    }
    function label(parent,x,y,value,color=G,size=36,anchor='start') {
        return node(parent,'text',{x,y,fill:color,'font-size':size,'text-anchor':anchor},value);
    }
    function stem(parent,x,y,width,color,height=28) {
        return node(parent,'rect',{x,y:y-height/2,width:Math.max(width,0),height,fill:color,rx:2});
    }
    document.querySelectorAll('[data-d3="mask"]').forEach(panel=> {
        panel.querySelector('button').addEventListener('click',()=> {
            const answer=panel.querySelector('[data-mask-answer]');
            const show=!answer.classList.contains('revealed');answer.classList.toggle('revealed',show);
            panel.querySelector('button').textContent=show?'Hide the target':'Reveal the hidden target';
            panel.querySelector('button').setAttribute('aria-pressed',String(show));
        });
    });
    document.querySelectorAll('[data-d3="attention"]').forEach(panel=> {
        const slider=panel.querySelector('[data-weight]');
        function update(){
            const a=Number(slider.value)/100,b=1-a,result=a*2+b*6;
            panel.querySelector('[data-attention-equation]').textContent=`${a.toFixed(2)} × 2 + ${b.toFixed(2)} × 6 = ${result.toFixed(2)}`;
            panel.querySelector('[data-readout]').textContent=`Weights ${a.toFixed(2)} + ${b.toFixed(2)} = 1 · values stay 2 and 6`;
            slider.setAttribute('aria-valuetext',`${a.toFixed(2)} on two; ${b.toFixed(2)} on six; output ${result.toFixed(2)}`);
        }
        slider.addEventListener('input',update);update();
    });
    document.querySelectorAll('[data-d3="alignment"]').forEach(panel=> {
        let aligned=false;
        panel.querySelector('button').addEventListener('click',()=> {
            aligned=!aligned;panel.querySelector('[data-cache-drawing]').innerHTML=evidence[aligned?'aligned':'misaligned'];
            panel.querySelector('button').textContent=aligned?'Show positional failure':'Align by sample ID';
            panel.querySelector('button').setAttribute('aria-pressed',String(aligned));
            panel.querySelector('[data-readout]').textContent=aligned?'Same disk rows, correct correspondence by ID':'Same shape, wrong samples under a positional join';
        });
    });
    document.querySelectorAll('.d3-results').forEach(panel=> {
        let metric='roc_auc';
        panel.querySelector('button').addEventListener('click',()=> {
            metric=metric==='roc_auc'?'average_precision':'roc_auc';
            const plot=panel.querySelector('svg');plot.replaceChildren();
            node(plot,'title',{},`Current validation ${metric==='roc_auc'?'ROC-AUC':'average precision'}`);
            methods.forEach(([key,name,color],i)=> {
                const row=evidence.metrics.find(r=>r.variant===panel.dataset.variant&&r.method===key),v=row[metric],y=100+i*135;
                label(plot,470,y+15,name,color,43,'end');stem(plot,560,y,v*950,color,35);
                label(plot,585+v*950,y+15,v.toFixed(3),color,39);
            });
            [0,.5,1].forEach(v=>label(plot,560+v*950,620,String(v),G,30,'middle'));
            node(plot,'path',{d:'M1035 45 V560',stroke:'#bdcbd6','stroke-width':3,'stroke-dasharray':'10 10',fill:'none'});
            plot.setAttribute('aria-label',`Current validation ${metric==='roc_auc'?'ROC-AUC':'average precision'}`);
            panel.querySelector('button').textContent=metric==='roc_auc'?'Show average precision':'Show ROC-AUC';
        });
    });
    let imported=null,variant='simple';
    const testPanel=document.querySelector('[data-test-comparison]');
    function testChart(){
        const plot=testPanel.querySelector('svg');plot.replaceChildren();
        node(plot,'title',{},'Validation and instructor-imported test ROC-AUC; blank test slots until import');
        methods.forEach(([key,name],i)=> {
            const y=85+i*115,v=evidence.metrics.find(r=>r.variant===variant&&r.method===key).roc_auc;
            label(plot,440,y+10,name,G,39,'end');stem(plot,500,y-15,v*1000,B,22);
            if(imported){
                const t=imported.find(r=>r.variant===variant&&r.method===key).roc_auc;
                stem(plot,500,y+20,t*1000,O,22);label(plot,1515,y+30,t.toFixed(3),O,30);
            } else label(plot,540,y+31,'Test not revealed',G,29);
        });
        label(plot,600,540,'Validation',B,32);label(plot,1000,540,'Test',O,32);
        [0,.5,1].forEach(v=>label(plot,500+v*1000,495,String(v),G,27,'middle'));
        const size=variant==='simple'?240:96;
        testPanel.querySelector('[data-test-status]').textContent=`${variant==='simple'?'Primary':'Order control'} · validation ${size} / test ${size} · ${imported?'classroom file imported':'test not revealed'}`;
    }
    testPanel.querySelector('button').addEventListener('click',()=> {
        variant=variant==='simple'?'interaction':'simple';
        testPanel.querySelector('button').textContent=variant==='simple'?'Show order control':'Show primary PPM';testChart();
    });
    testChart();
    document.querySelector('[data-test-import]').addEventListener('change',async event=> {
        const status=document.querySelector('.d3-test [data-test-status]');
        const file=event.target.files?.[0];if(!file)return;
        try {
            if(file.size>1000000)throw new Error('Result file is too large.');
            const payload=JSON.parse(await file.text());
            if(typeof payload.revealed_utc!=='string'||!/^[a-f0-9]{64}$/.test(payload.frozen_manifest_sha256))throw new Error('Expected a saved test_results.json with a freeze reference.');
            if(!Array.isArray(payload.results)||payload.results.length!==8)throw new Error('Expected eight result rows.');
            const seen=new Set();
            payload.results.forEach(row=> {
                const key=row.variant+'|'+row.method;
                if(!['simple','interaction'].includes(row.variant)||!methods.some(m=>m[0]===row.method)||seen.has(key))throw new Error('Duplicate or unexpected variant/method.');
                seen.add(key);
                if(row.evaluation_split!=='test'||row.sample_count!==(row.variant==='simple'?240:96)||row.decision_threshold!==0.5)throw new Error('Unexpected split, sample count or threshold.');
                ['roc_auc','average_precision'].forEach(k=> {if(typeof row[k]!=='number'||!Number.isFinite(row[k])||row[k]<0||row[k]>1)throw new Error('Invalid metric.');});
            });
            imported=payload.results;
            document.querySelectorAll('[data-test-value]').forEach(cell=> {
                const [v,m,k]=cell.dataset.testValue.split('|');cell.textContent=imported.find(r=>r.variant===v&&r.method===m)[k].toFixed(3);
            });
            status.textContent='Classroom result imported · inspect provenance in the notebook; no model ran in this page.';
            testChart();
        } catch(error){status.textContent='Import refused: '+error.message;}
        event.target.value='';
    });
}
