/* === DAY 4: LOCAL TEACHING CONTROLS, NO AGENT OR MODEL EXECUTION === */
function bindDayFour() {
    const evidence=JSON.parse(document.getElementById('day-four-evidence').textContent);
    const B='#0072B2',O='#D55E00',G='#697782',ns='http://www.w3.org/2000/svg';
    function node(parent,tag,attrs,value){
        const el=document.createElementNS(ns,tag);
        Object.entries(attrs).forEach(([key,val])=>el.setAttribute(key,String(val)));
        if(value!==undefined)el.textContent=value;
        parent.appendChild(el);return el;
    }
    function label(parent,x,y,value,color=B,size=46,anchor='middle'){
        return node(parent,'text',{x,y,fill:color,'font-size':size,'text-anchor':anchor},value);
    }
    function clear(panel,title){
        const plot=panel.querySelector('svg');plot.replaceChildren();
        node(plot,'title',{},title);plot.setAttribute('aria-label',title);return plot;
    }
    document.querySelectorAll('[data-d4="loop"]').forEach(panel=>{
        let current=0;
        const phrases=['Inspect the current task and available files','Act with an appropriate tool','Observe the tool result and inspect its evidence','Revise the plan or report the result and its limits'];
        function update(){
            panel.querySelectorAll('[data-loop-step]').forEach(el=>el.classList.toggle('current',Number(el.dataset.loopStep)===current));
            panel.querySelector('[data-readout]').textContent=phrases[current];
        }
        panel.querySelector('button').addEventListener('click',()=>{current=(current+1)%4;update();});update();
    });
    document.querySelectorAll('[data-d4="exit"]').forEach(panel=>{
        const button=panel.querySelector('button'),defects=panel.querySelector('[data-exit-defects]');
        button.setAttribute('aria-pressed','false');
        button.addEventListener('click',()=>{
            const revealed=defects.classList.toggle('revealed');button.setAttribute('aria-pressed',String(revealed));
            button.textContent=revealed?'Hide the findings':'Inspect what ran';
            panel.querySelector('[data-readout]').textContent=revealed?'Authored fixture: a clean exit coexists with an invalid analysis':'What does this output actually establish?';
        });
    });
    document.querySelectorAll('[data-d4="decisions"]').forEach(panel=>{
        let group=0;
        const sets=[
            ['Task and data','What does the label mean?','Which files are allowed?','Which samples belong together?','How are splits assigned?'],
            ['Model and success','Which representation?','Which model or search?','Which primary metric?','Which decision threshold?'],
            ['Evaluation and provenance','Where may selection happen?','What stays protected?','Which outputs are required?','Which claims can we defend?']
        ];
        function update(){
            const [name,...questions]=sets[group],plot=clear(panel,'Missing experiment decisions: '+name);
            questions.forEach((question,i)=>{
                const x=i%2===0?430:1290,y=i<2?140:400;
                label(plot,x,y-65,String(group*4+i+1),G,33);label(plot,x,y,question,i%2?O:B,43);
            });
            panel.querySelector('[data-readout]').textContent=`${name} · ${group+1} of 3`;
        }
        panel.querySelector('button').addEventListener('click',()=>{group=(group+1)%3;update();});update();
    });
    document.querySelectorAll('[data-d4="alignment"]').forEach(panel=>{
        let aligned=false;const button=panel.querySelector('button');button.setAttribute('aria-pressed','false');
        button.addEventListener('click',()=>{
            aligned=!aligned;panel.querySelector('[data-alignment]').innerHTML=evidence[aligned?'aligned':'positional'];
            button.textContent=aligned?'Show positional pairing':'Join by sample ID';button.setAttribute('aria-pressed',String(aligned));
        });
    });
    document.querySelectorAll('[data-d4="scores"]').forEach(panel=>{
        let metric='roc_auc';const button=panel.querySelector('button');
        function update(){
            const plot=clear(panel,'Historical validation '+(metric==='roc_auc'?'ROC-AUC':'average precision'));
            label(plot,1030,55,metric==='roc_auc'?'Validation ROC-AUC':'Validation average precision',G,42);
            [['vague','Vague request',O],['specified','Specified baseline',B]].forEach(([key,name,color],i)=>{
                const value=evidence.historical[key].metrics[metric],y=170+i*210;
                label(plot,440,y+16,name,color,48,'end');
                node(plot,'rect',{x:530,y:y-21,width:1000*value,height:42,fill:color});
                label(plot,565+1000*value,y+16,value.toFixed(3),color,46,'start');
            });
            [0,.5,1].forEach(value=>label(plot,530+1000*value,505,String(value),G,31));
            button.textContent=metric==='roc_auc'?'Show average precision':'Show ROC-AUC';
        }
        button.addEventListener('click',()=>{metric=metric==='roc_auc'?'average_precision':'roc_auc';update();});update();
    });
    document.querySelectorAll('[data-d4="findings"]').forEach(panel=>{
        let current=0;
        const findings=[
            ['FAIL','Group separation','group-a occurs in training and validation',O],
            ['FAIL','Training-only vocabulary','Source: fit(samples["sequence"]) includes validation',O],
            ['FAIL','Metric correspondence','ID join changes accuracy from 100% to 0%',O],
            ['FAIL','Biological claim scope','An authored simulation does not validate promoter biology',O],
            ['UNVERIFIED','A fitted predictor','Probabilities were authored; no training evidence',G],
            ['UNVERIFIED','Actual test-access history','A proposed misuse does not establish a file read',G]
        ];
        function update(){
            const [status,title,detail,color]=findings[current],plot=clear(panel,`${status}: ${title}`);
            label(plot,864,105,status,color,48);label(plot,864,270,title,color,70);label(plot,864,430,detail,G,42);
            panel.querySelector('[data-readout]').textContent=`Finding ${current+1} of ${findings.length} · observed defects and missing evidence differ`;
        }
        panel.querySelector('button').addEventListener('click',()=>{current=(current+1)%findings.length;update();});update();
    });
    // Optional discussion timer. It never advances slides; leaving pauses it.
    // Kept local and transient: no storage, imports, network or scientific work.
    document.querySelectorAll('[data-timer]').forEach(panel=>{
        const output=panel.querySelector('output'),start=panel.querySelector('[data-timer-start]'),reset=panel.querySelector('[data-timer-reset]');
        let remaining=300000,deadline=0,interval=null;
        function paint(){const seconds=Math.ceil(remaining/1000);output.textContent=`${String(Math.floor(seconds/60)).padStart(2,'0')}:${String(seconds%60).padStart(2,'0')}`;}
        function pause(){
            if(interval!==null){remaining=Math.max(0,deadline-Date.now());clearInterval(interval);interval=null;}
            start.textContent=remaining===0?'Restart':remaining===300000?'Start':'Resume';paint();
        }
        function tick(){remaining=Math.max(0,deadline-Date.now());paint();if(remaining===0){pause();start.textContent='Restart';}}
        start.addEventListener('click',()=>{
            if(interval!==null){pause();return;}
            if(remaining===0)remaining=300000;
            deadline=Date.now()+remaining;interval=setInterval(tick,200);start.textContent='Pause';tick();
        });
        reset.addEventListener('click',()=>{pause();remaining=300000;start.textContent='Start';paint();});
        new MutationObserver(()=>{if(!panel.closest('.slide').classList.contains('active'))pause();}).observe(panel.closest('.slide'),{attributes:true,attributeFilter:['class']});
        document.addEventListener('visibilitychange',()=>{if(document.hidden)pause();});
        window.addEventListener('beforeprint',pause);paint();
    });
}
