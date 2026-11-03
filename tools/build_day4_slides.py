"""Build Day 4 from the reviewed story and source-bound, development-only audit evidence."""
import hashlib
import html
import json
import math
from pathlib import Path
import re

from build_day2_section1 import BLUE, ORANGE, PURPLE, GRAY, INK, text, line, arrow, circle, svg, dna, helix, required_match
from build_day3_slides import CSS as BASE_CSS, lock, statement, pair, list_figure, prompt

ROOT=Path(__file__).resolve().parents[1]
DECK=ROOT/'Slides/Day_4/presentation.html'
E=html.escape
COLAB='https://colab.research.google.com/github/palexiou/ML_Course_2026/blob/main/notebooks/06_scientific_audit.ipynb'


def person(x,y,color=BLUE):
    return circle(x,y-90,40,'',color,0)+f'<path d="M{x-85} {y+150} v-90 q0 -85 85 -85 q85 0 85 85 v90 M{x-85} {y+35} l-70 80 h-50 M{x+85} {y+35} l70 80 h60" fill="none" stroke="{color}" stroke-width="7" stroke-linecap="round"/>'


def page(x,y,label='',color=BLUE,w=230,h=280):
    p=f'<path d="M{x} {y} h{w-50} l50 50 v{h-50} h{-w} Z M{x+w-50} {y} v50 h50" fill="white" stroke="{color}" stroke-width="5"/>'
    for i in range(4):
        yy=y+min(90,h*.43)+i*min(36,h*.12)
        p+=line(x+35,yy,x+w-35-(i%2)*35,yy,color,4)
    return p+text(x+w/2,y+h+65,label,39,color)


def terminal(x,y,w=650,h=260,rows=(),color=BLUE):
    p=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="#f8fafc" stroke="{color}" stroke-width="5"/>'+line(x,y+45,x+w,y+45,color,3)
    for i in range(3):p+=f'<circle cx="{x+27+i*23}" cy="{y+23}" r="6" fill="{color}"/>'
    for i,row in enumerate(rows):p+=text(x+35,y+105+i*62,row,37,INK,'start')
    return p


def link_slide(label,path,sub=''):
    return '<div class="d3-notebook"><p>'+E(label)+'</p><a href="'+path+'">Open the teaching material ↗</a>'+('<p class="route">'+E(sub)+'</p>' if sub else '')+'</div>'


def notebook(label,code='',route='Setup → shared definitions → stage 06 definitions'):
    return '<div class="d3-notebook"><p>'+E(label)+'</p><a href="'+COLAB+'">Open notebook in Colab ↗</a>'+('<pre>'+E(code)+'</pre>' if code else '')+'<p class="route">'+E(route)+'</p></div>'


def code(source,caption=''):
    return '<div class="d3-code"><pre>'+E(source)+'</pre>'+('<p>'+E(caption)+'</p>' if caption else '')+'</div>'


def button(label,attr='data-next'):
    return '<button type="button" '+attr+'>'+E(label)+'</button>'


def live(p,mode,controls,caption=''):
    return '<div class="d2-live d3-live" data-d4="'+mode+'">'+svg(p,mode.replace('-',' '),560)+'<div class="d3-controls">'+controls+'</div><p data-readout aria-live="polite">'+E(caption)+'</p></div>'


def loop():
    points=[(864,75,'Inspect'),(1440,260,'Act'),(864,465,'Observe'),(290,260,'Revise')]
    p=''
    for i,(x,y,label) in enumerate(points):
        nx,ny,_=points[(i+1)%4];a=math.atan2(ny-y,nx-x)
        p+=arrow(x+100*math.cos(a),y+45*math.sin(a),nx-120*math.cos(a),ny-50*math.sin(a),'#b7c8d5',4)
    for i,(x,y,label) in enumerate(points):p+=f'<g data-loop-step="{i}" class="current">'+circle(x,y,53,str(i+1),BLUE if i%2==0 else ORANGE,44)+text(x,y+95,label,44,INK)+'</g>'
    return p


def group_figure():
    p=text(460,90,'Training',51,BLUE)+text(1280,90,'Validation',51,ORANGE)
    for x,y,sid,group,c in [(460,240,'train-01','group-a',BLUE),(460,440,'train-02','group-b',BLUE),(1280,240,'validation-01','group-a',ORANGE),(1280,440,'validation-02','group-c',ORANGE)]:
        p+=circle(x-165,y,30,'',c,0)+text(x,y+10,sid,38,c)+text(x,y+75,group,42,INK)
    p+=line(660,310,1080,310,ORANGE,7)+text(864,620,'Unique samples ≠ independent groups',51,ORANGE)
    return p


def alignment(aligned=False):
    p=text(330,70,'Validation labels',46,BLUE)+text(1260,70,'Probability rows',46,ORANGE)
    for i,(sid,label) in enumerate([('validation-01','0'),('validation-02','1')]):
        y=190+i*160;p+=text(180,y,sid,38,BLUE)+circle(495,y-12,35,label,BLUE,38)
    for i,(sid,probability) in enumerate([('validation-02','0.1'),('validation-01','0.9')]):
        y=190+i*160;p+=circle(1090,y-12,45,probability,ORANGE,37)+text(1400,y,sid,38,ORANGE)
    for i,j in enumerate([1,0] if aligned else [0,1]):p+=arrow(555,178+i*160,1025,178+j*160,BLUE if aligned else ORANGE,5)
    p+=text(864,530,'ID-aligned accuracy = 0%' if aligned else 'Positional “accuracy” = 100%',58,BLUE if aligned else ORANGE)
    return p


def claims():
    return svg(text(864,130,'“Learned promoter biology”',64,ORANGE)+text(864,235,'No biological validation',47,GRAY)+line(220,315,1510,315,'#dce5eb',3)+text(864,435,'“Choose using the Day 3 test”',60,ORANGE)+text(864,540,'Proposed misuse ≠ observed test access',43,GRAY),'Authored unsupported biological claim and proposed post-reveal selection, without evidence of an actual test read')


def scoreboard(data,metric='roc_auc'):
    p=text(1030,55,'Validation ROC-AUC' if metric=='roc_auc' else 'Validation average precision',42,GRAY)
    for i,(arm,label,c) in enumerate([('vague','Vague request',ORANGE),('specified','Specified baseline',BLUE)]):
        y=170+i*210;v=data['historical_actual_runs'][arm]['metrics'][metric]
        p+=text(440,y+16,label,48,c,'end')+line(530,y,530+v*1000,y,c,42)+text(565+v*1000,y+16,f'{v:.3f}',46,c,'start')
    p+=text(530,505,'0',31,GRAY)+text(1030,505,'0.5',31,GRAY)+text(1530,505,'1',31,GRAY)
    return p


def s1(n,data):
    if n==1:
        p=person(400,240)+page(150,455,'Your question',BLUE,w=180,h=140)+arrow(650,260,960,260)+text(800,200,'Delegate',42,GRAY)+terminal(1060,120,560,300,['Read files','Write code','Run checks'],ORANGE)
        p+=text(864,690,'1 · Count     2 · Learn     3 · Reuse     4 · Delegate',41,BLUE)
        return svg(p,'Day 4: researcher delegates implementation while retaining scientific responsibility')
    if n==2:
        p=terminal(100,90,630,275,['Read · edit · execute','Inspect errors · report'])+person(1290,220,ORANGE)+text(410,515,'Implementation',57,BLUE)+text(1290,515,'Scientific responsibility',51,ORANGE)
        return svg(p,'An agent can help implement and check; the researcher owns the question, design and claim')
    if n==3:
        p=terminal(100,170,620,240,['Train + validation only'])+arrow(770,280,990,280)+line(1030,100,1030,530,ORANGE,10)+lock(1300,200,GRAY)+text(1300,400,'Protected evidence',44,GRAY)
        p+=text(864,680,'No Day 4 selection against the Day 3 test',49,BLUE)
        return svg(p,'Day 4 development cannot use protected test files or any revealed scores to select new models')
    if n==4:
        p=''
        for i,(word,c) in enumerate([('Read',BLUE),('this',BLUE),('sequence',BLUE),('…',ORANGE)]):p+=text(200+i*230,175,word,56,c)
        p+=arrow(910,160,1090,160)
        for i,(word,v) in enumerate([('file',.55),('table',.30),('result',.15)]):
            y=90+i*100;p+=text(1130,y,word,40,GRAY,'start')+line(1300,y-15,1300+v*450,y-15,ORANGE,22)
        p+=page(320,360,'Files / history',BLUE,w=160,h=160)+arrow(590,450,850,450)+text(1230,470,'Application supplies context',45,BLUE)
        return svg(p,'Constructed next-token distribution and application-supplied context, not a statement about universal memory behavior')
    if n==5:
        p=circle(360,250,90,'LLM',BLUE,57)+arrow(510,250,700,250)
        for i,label in enumerate(['Read','Edit','Run']):
            y=100+i*190;p+=circle(930,y,48,str(i+1),ORANGE,38)+text(1120,y+15,label,55,ORANGE)+line(740,250,875,y,ORANGE,4)
        p+=text(864,665,'A model uses tools and observes their results',54,BLUE)
        return svg(p,'Tools let a language model read files, edit code and run commands within an application')
    if n==6:return live(loop(),'loop',button('Trace the next step'),'Inspect the current task and available files')
    if n==7:
        p=terminal(100,100,670,270,['Exit code: 0','Accuracy: 100%'])
        p+='<g data-exit-defects>'+page(1160,70,'Inspect the analysis',ORANGE,w=250,h=220)+text(1250,430,'Group overlap',45,ORANGE)+text(1250,510,'Wrong row pairing',45,ORANGE)+'</g>'
        return live(p,'exit',button('Inspect what ran'),'What does this output actually establish?')
    if n==8:
        p=page(255,90,'Observe saved evidence',BLUE)+terminal(1020,100,580,250,['Use existing access'],ORANGE)+text(1300,500,'Optional operator route',45,ORANGE)
        p+=text(864,680,'Same evidence questions · no agent account required',46,BLUE)
        return svg(p,'Observation route and optional existing-access operation have the same ungraded evidence questions')
    if n==9:return prompt('What would you need to see','before putting your name on the result?')
    return prompt('The agent executes. You defend.','What did the request leave unsaid?')


def s2(n,data):
    if n==1:return '<div class="d3-prompt d4-quote"><p>“Can you build the best model to predict promoters from these DNA sequences and explain the biology?”</p></div>'
    if n==2:
        return live('', 'decisions', button('Next set of decisions'),'Task and data · 1 of 3')
    if n==3:
        p=text(864,70,'One vague request',58,INK)
        for x,label,sub,c in [(330,'Split?','Rows / groups',BLUE),(864,'Success?','Accuracy / ROC-AUC',ORANGE),(1400,'Search?','Baseline / candidates',PURPLE)]:
            p+=arrow(864,140,x,260,c)+circle(x,300,50,'?',c,50)+text(x,435,label,52,c)+text(x,540,sub,39,GRAY)
        return svg(p,'Missing decisions create different possible experiments; failure is not inevitable')
    if n==4:
        p=page(280,90,'Four authored rows',ORANGE)+text(1180,200,'Invented probabilities',60,ORANGE)+text(1180,320,'Not an agent transcript',49,BLUE)+text(1180,450,'Read → predict → audit',47,GRAY)
        return svg(p,'An authored teaching fixture with invented probabilities, distinct from genuine previous agent runs')
    if n==5:return svg(group_figure(),'group-a crosses training and validation despite distinct sample IDs')
    if n==6:
        return code('vectorizer.fit(samples["sequence"])','Training + validation informed the vocabulary')
    if n==7:return live('<g data-alignment>'+alignment()+'</g>','alignment',button('Join by sample ID'),'Authored probabilities · fixing alignment does not fix leakage')
    if n==8:return claims()
    return prompt('The script runs.','Which evidence would you inspect first?')


def s3(n,data):
    if n==1:
        p=person(230,210)+arrow(410,260,650,260)+page(760,100,'Experiment spec',BLUE)+arrow(1070,260,1230,260)+terminal(1270,160,350,215,['Implement'],ORANGE)
        return svg(p,'A checkable scientific specification connects the research question to implementation')
    if n==2:return list_figure(['Question and scope','Allowed data and partitions','Fixed model and fitting protocol','Metrics and decision threshold','Outputs, provenance and limitations'])
    if n==3:
        p=page(200,80,'train.csv',BLUE)+page(750,80,'validation.csv',ORANGE)+line(1190,40,1190,540,GRAY,7)+lock(1460,160,GRAY)+text(1460,400,'Test stays out',42,GRAY)
        return svg(p,'Explicit development files and protected test exclusion, with fixed split identities')
    if n==4:
        return code('4-mer counts\nLogisticRegression(\n    C=1.0, max_iter=2000,\n    random_state=2026\n)','Vocabulary + classifier fit on training only')
    if n==5:
        p=text(440,150,'Rank probabilities',52,BLUE)+text(440,280,'ROC-AUC',78,BLUE)+text(440,420,'Average precision supports',41,GRAY)
        p+=line(864,75,864,560,'#dce5eb',3)+text(1300,150,'Make class calls',52,ORANGE)+text(1300,290,'p ≥ 0.5',80,ORANGE)+text(1300,430,'Declare before evaluation',43,GRAY)
        return svg(p,'ROC-AUC primary and AP supporting; class decisions use fixed threshold 0.5')
    if n==6:
        return '<div class="d2-live d4-schema"><table><thead><tr><th>sample_id</th><th>probability</th></tr></thead><tbody><tr><td>validation-01</td><td>0.9</td></tr><tr><td>validation-02</td><td>0.1</td></tr></tbody></table><p>Unique IDs · exact coverage · finite p in [0, 1]</p></div>'
    if n==7:
        p=page(240,70,'Run record',BLUE,w=270,h=350)
        for i,label in enumerate(['Input + source hashes','Settings + seed','Versions + commands','Timing + limitations']):p+=text(880,130+i*130,label,49,[BLUE,ORANGE,BLUE,ORANGE][i],'start')
        return svg(p,'Record input/source identities, settings, versions, commands, timing and limitations')
    return prompt('Fewer hidden choices.','More checkable commitments.')


def s4(n,data):
    if n==1:
        p=''
        for x,label,job,c in [(220,'Specification','This experiment',BLUE),(760,'AGENTS.md','Project guidance',ORANGE),(1300,'SKILL.md','Reusable procedure',PURPLE)]:
            p+=page(x,90,label,c,w=200,h=250)+text(x+100,535,job,40,c)
        return svg(p,'Specification, project guidance and reusable procedure are different jobs, not a universal precedence hierarchy')
    if n==2:return link_slide('Read the example project rules','../../agent_workshop/example-project/AGENTS.md','Development only · fixed identities · supported claims')
    if n==3:
        p=page(150,110,'SKILL.md',PURPLE,w=230,h=300)+arrow(480,260,700,260)
        for i,label in enumerate(['Read the spec','Trace fitting + IDs','Check predictions','Report evidence + limits']):p+=text(850,110+i*145,label,50,BLUE,'start')
        return svg(p,'The supplied audit skill is a reusable evidence procedure; course audit code is separate')
    if n==4:
        p=page(150,80,'Same development files',BLUE,w=230,h=270)+arrow(460,200,760,130)+arrow(460,280,760,430)
        p+=terminal(820,40,720,200,['Vague request'],ORANGE)+terminal(820,350,720,200,['Specified baseline'],BLUE)+text(864,675,'October 26 · genuine saved runs · historical fixed motif',42,GRAY)
        return svg(p,'Two actual previous agent contexts with identical historical development inputs and operational restrictions')
    if n==5:return live(scoreboard(data),'scores',button('Show average precision','data-metric'),'October 26 · fixed-motif data · not a prompt-quality experiment')
    if n==6:
        p=text(420,90,'Specified baseline',53,BLUE)+text(1300,90,'Vague request',53,ORANGE)
        p+=page(300,190,'Fixed 4-mers + LR',BLUE,w=200,h=230)
        for i in range(6):p+=circle(1100+(i%3)*200,210+(i//3)*150,37,str(i+1),ORANGE,35)
        p+=text(1300,500,'Six candidates · training-only CV',39,ORANGE)+text(864,665,'The motif prior was disclosed, not discovered',49,INK)
        return svg(p,'Fixed count baseline versus six candidates selected by training-only group CV using a supplied fixed-motif prior')
    if n==7:return statement('Different features. Different search.','Prompt quality was not isolated.')
    return prompt('Instructions clarify the task.','Now audit what actually happened.')


def s5(n,data):
    if n==1:
        p=text(285,145,'Claim',67,ORANGE)+arrow(430,130,650,130)+text(850,145,'Artifacts',67,BLUE)+arrow(1070,130,1290,130)+text(1460,145,'Checks',67,BLUE)
        p+=page(250,280,'What is asserted?',ORANGE,w=180,h=210)+page(750,280,'What supports it?',BLUE,w=180,h=210)+page(1250,280,'What is unresolved?',GRAY,w=180,h=210)
        return svg(p,'Scientific audit traces each claim through supporting artifacts, checks and unresolved evidence')
    if n==2:return list_figure(['Required columns and identities','Exact evaluation-ID coverage','Finite probabilities in [0, 1]','One-to-one ID join and metrics','Cross-split groups and duplicate sequences'])
    if n==3:return notebook('Run the fixture audit','Day 4 · fixture audit\nThen: negative prediction probes','Section 5 · output reports defects; preprocessing needs source inspection')
    if n==4:
        return '<div class="d2-live d4-audit-activity"><div class="d4-themes"><span>Splits</span><span>Fitting scope</span><span>ID joins</span><span>Metrics</span><span>Claims</span></div><a href="../../instructor/audit-checklist.html">Open the audit handout ↗</a><p>PASS · FAIL · UNVERIFIED</p><div class="d4-timer" data-timer><output aria-live="off">05:00</output><div class="d3-controls">'+button('Start','data-timer-start')+button('Reset','data-timer-reset')+'</div></div></div>'
    if n==5:
        return live('','findings',button('Reveal the next finding'),'Observed defects and missing evidence are different findings')
    if n==6:
        p=''
        for i,(x,title,sub,c) in enumerate([(290,'Evidence','group-a crosses splits',ORANGE),(864,'Consequence','New-group claim unsupported',BLUE),(1440,'Repair','Group-respecting split + refit',BLUE)]):
            p+=circle(x,170,55,str(i+1),c,44)+text(x,320,title,57,c)+text(x,455,sub,33,INK)
            if i<2:p+=arrow(x+110,170,x+440,170,GRAY,4)
        return svg(p,'Evidence: cross-split group; consequence: unsupported independent-group claim; repair: separate exercise split and refit')
    if n==7:
        p=''
        for i,(arm,label,c) in enumerate([('vague','Vague',ORANGE),('specified','Specified',BLUE)]):
            y=100+i*260;r=data['historical_actual_runs'][arm]
            p+=text(180,y,label,53,c,'start')+text(850,y,'240 matching validation IDs',45,c)+text(850,y+95,'0 cross-split groups · 0 duplicate sequences',39,GRAY)+text(850,y+175,f"ROC-AUC {r['metrics']['roc_auc']:.7f}",46,c)
        return svg(p,'Current local audit of historical saved predictions; automated identity and metric checks pass for both genuine runs')
    if n==8:return prompt('The tables pass the checks.','Is the scientific question still sound?')
    if n==9:
        p=loop()+text(864,670,'Repair → refit → validation · keep the old test out',46,BLUE)
        return svg(p,'Repair the separate exercise entirely within development; preserve the main-course frozen evaluation')
    if n==10:return prompt('Defend one sentence.','Name the artifact that supports it.')
    return prompt('What would you like to revisit?','Splits · fitting scope · identity · claim limits')


def s6(n,data):
    if n==1:
        p=''
        for i,(label,c) in enumerate([('Question',BLUE),('Data',ORANGE),('Execution',BLUE),('Artifacts',ORANGE),('Claim',BLUE)]):
            x=150+i*350;p+=circle(x,200,38,str(i+1),c,36)+text(x,360,label,43,c)
            if i<4:p+=arrow(x+60,200,x+280,200,GRAY,4)
        p+=text(864,610,'Platform inspection plan',54,BLUE)
        return svg(p,'Generic workflow inspection plan; no observed Agentomics product behavior is claimed')
    if n==2:return list_figure(['Where are the split identities?','Where is the execution record?','Where are the raw predictions?'])
    if n==3:return prompt('Agentomics demonstration pending','Discussion: what evidence would you need?')
    if n==4:
        return '<div class="d4-canvas"><div><h2>Evidence needed</h2><p>Which artifact?</p></div><div><h2>Why it matters</h2><p>Which claim?</p></div><div><h2>Still unverified</h2><p>What remains open?</p></div></div>'
    if n==5:
        p=''
        for i,(lab,c) in enumerate([('Count',BLUE),('Learn',ORANGE),('Reuse',PURPLE),('Delegate',BLUE)]):
            x=220+i*425;p+=text(x,65,f'Day {i+1}',38,GRAY)+text(x,480,lab,58,c)
            if i==0:
                for j,v in enumerate([80,150,110]):p+=line(x-80+j*80,330,x-80+j*80,330-v,c,24)
            elif i==1:
                for j in range(3):
                    for k in range(2):p+=line(x-90,210+j*60,x+90,225+k*100,c,3)
                for xx,ys in [(x-90,[210,270,330]),(x+90,[225,325])]:
                    for y in ys:p+=circle(xx,y,17,'',c,0)
            elif i==2:p+=helix(x-150,260,300,65)
            else:p+=terminal(x-150,160,300,195,['Read · act'],c)
        p+=text(864,675,'Where do the features come from? What evidence supports the claim?',43,INK)
        return svg(p,'Four-day synthesis: count features, learn detectors, reuse embeddings, delegate implementation')
    if n==6:
        p=person(864,210,BLUE)+text(365,210,'The question',51,BLUE)+text(1370,210,'The evaluation',51,ORANGE)+text(370,460,'The evidence',51,ORANGE)+text(1370,460,'The final claim',51,BLUE)
        return svg(p,'Human scientific responsibility for the question, evaluation, evidence and final claim')
    return '<div class="d3-notebook"><p>One claim you can defend.<br>One check you will keep.</p><a href="../index.html">All four days ↗</a><br><a href="../../notebooks/README.md">Completed notebooks ↗</a><br><a href="../../instructor/audit-checklist.html">Audit checklist ↗</a></div>'


CSS=BASE_CSS.replace('DAY 3 ILLUSTRATED STORY','DAY 4 ILLUSTRATED STORY').replace('.day-three','.day-four')+'''
/* === DAY 4 WORKSHOP CONTROLS === */
.day-four h1{font-size:72px}.day-four .d4-quote{padding:55px 70px}.day-four .d4-quote p{font-size:67px;color:#18344b}
.day-four .d4-schema{padding:100px 150px}.day-four .d4-schema table{width:100%;font-size:55px;border-collapse:collapse}
.day-four .d4-schema th,.day-four .d4-schema td{background:none;text-align:left;padding:20px 40px;border-bottom:2px solid #d7e1e8}
.day-four .d4-schema th{color:#0072B2}.day-four .d4-schema p{text-align:center;font-size:42px;margin-top:65px}
.day-four [data-loop-step]{opacity:.2;transition:opacity .2s}.day-four [data-loop-step].current{opacity:1}
.day-four [data-exit-defects]{opacity:0;transition:opacity .2s}.day-four [data-exit-defects].revealed{opacity:1}
.day-four .d4-audit-activity{padding:25px 100px;text-align:center}.day-four .d4-themes{display:flex;justify-content:space-around;gap:24px;flex-wrap:wrap;font-size:41px;margin:30px 0 65px;color:#0072B2}
.day-four .d4-audit-activity a{font-size:43px;color:#0072B2}.day-four .d4-audit-activity p{font-size:42px;color:#697782;margin:40px 0 0}
.day-four .d4-timer output{display:block;font-size:135px;font-variant-numeric:tabular-nums;color:#18344b;margin:12px auto 10px}
.day-four .d4-canvas{display:grid;grid-template-columns:1fr 1fr 1fr;gap:55px;padding:90px 20px}
.day-four .d4-canvas>div{min-height:400px;border-bottom:3px solid #a8bdcc}.day-four .d4-canvas h2{font:600 46px "Source Sans 3",sans-serif;color:#0072B2;margin:0 0 70px}
.day-four .d4-canvas p{font-size:40px;color:#697782;line-height:1.4}
@media(prefers-reduced-motion:reduce){.day-four [data-loop-step],.day-four [data-exit-defects]{transition:none}}
@media print{.day-four [data-exit-defects]{opacity:1!important}.day-four [data-loop-step]{opacity:1!important}}
/* === END DAY 4 WORKSHOP CONTROLS === */
'''


def build():
    data=json.loads((ROOT/'instructor/verification/day4-current.json').read_text())
    assert not data['test_evaluated'] and not data['new_agent_run'] and not data['agentomics_demo_delivered']
    for path,sha in data['source_sha256'].items():
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==sha,f'Stale Day 4 evidence: {path}'
    source=(ROOT/'Slides/Day_3/presentation.html').read_text()
    start=source.index('/* === DAY 3 ILLUSTRATED STORY === */');end=source.index('</style>',start)
    source=source[:start]+CSS+source[end:]
    source=re.sub(r'<script id="day-three-[^"]+"[^>]*>.*?</script>\s*','',source,flags=re.S)
    source=source.replace('Day 3 · Machine learning','Day 4 · Machine learning').replace('ml-course-2026-day-3-edits-v2','ml-course-2026-day-4-edits-v2')
    source=source.replace("key.startsWith('day-3-')","key.startsWith('day-4-')").replace('Number(localMatch[1]) !== 3','Number(localMatch[1]) !== 4').replace('if (day === 3)','if (day === 4)')
    source=source.replace('day-3-edited','day-4-edited').replace('bindDayThree();','bindDayFour();')
    aliases={f'#day-4-slide-{i}':key for i,key in enumerate(['day-4-s1-welcome','day-4-s1-llm-basics','day-4-s2-vague-prompt','day-4-s2-fixture-intro','day-4-break-1','day-4-s3-spec-concept','day-4-s4-three-tiers','day-4-s4-actual-runs-intro','day-4-break-2','day-4-s5-checklist-activity','day-4-s5-repair-framework','day-4-s6-agentomics-demo','day-4-s6-human-responsibility','day-4-s6-final-discussion'],1)}
    source=re.sub(r'const openingAliases = \{.*?\};','const openingAliases = '+json.dumps(aliases)+';',source)
    story=(ROOT/'Slides/Day_4/story.md').read_text();records=[]
    for sec,count in [(1,10),(2,9),(3,8),(4,8),(5,11),(6,7)]:
        span=story.split(f'<a id="section-{sec}"></a>')[1].split('<a id="')[0]
        blocks=re.findall(rf'### S{sec}-(\d+) · (.*?)\n(.*?)(?=\n### |\Z)',span,re.S);assert len(blocks)==count
        for number,title,body in blocks:
            def field(name):return E(required_match(r'\*\*'+re.escape(name)+r':\*\* (.*?)(?=\n\n\*\*|\Z)',body,re.S)[1].strip().removesuffix('---').strip()).replace('`','')
            key=required_match(r'\*\*Proposed slide ID:\*\* `([^`]+)`',body)[1]
            provenance='Figures are native teaching constructions. Fixture probabilities 0.1/0.9 are deliberately authored, not fitted model output or observed agent failure. The local notebook audit checks identity and saved validation metrics; it cannot infer correct fitting or test-access history from prediction tables. Historical actual runs: October 26, 2026, Codex/gpt-6.1-sol, fixed-string motif input, 720 training / 240 validation rows; not current PPM scores. Vague arm used a disclosed TATAAATG prior and six-candidate training-only group CV, not motif discovery. Specified arm is fixed 4-mer/logistic baseline, max_iter=2000, no scaler. Both received technical tool corrections. Current Git files have LF line endings; reconstructed CRLF matches original Windows input hashes. Source-bound evidence: instructor/verification/day4-current.json. No new agent call, classifier fitting, protected test access or reveal. Instructor selected Agentomics audit-discussion fallback; no product demo or capability claim is verified. Colab, pacing and projector readability unverified.'
            records.append(dict(day=4,id=key,anchor=key,sectionSequence=True,sectionNumber=sec,kind='day-four',title=E(title.replace('`','')),time=field('Time'),body=globals()[f's{sec}'](int(number),data),subtitle='',takeaway='',notes=field('What I want to say'),point=field('Point / reveal'),transition=field('Transition'),sourceNote=E(provenance)))
        if sec in [2,4]:
            num=1 if sec==2 else 2;key=f'day-4-break-{num}'
            records.append(dict(day=4,id=key,anchor=key,sectionSequence=True,sectionNumber=sec,kind='day-four',title='Ten-minute break',time='50:00–60:00 (10:00)' if num==1 else '100:00–110:00 (10:00)',body=statement('Ten-minute break','Next: specify the experiment' if num==1 else 'Next: your scientific audit'),subtitle='',takeaway='',notes='Return at minute '+('60' if num==1 else '110')+'.',point='Leave this slide up.',transition='Continue with the next section.',sourceNote='Suggested classroom timing.'))
    assert len(records)==55 and len({r['id'] for r in records})==55
    last=0
    for record in records:
        timing=required_match(r'^(\d+):(\d+)–(\d+):(\d+) \((\d+):(\d+)\)$',record['time'])
        a,b,c,d,e,f=map(int,timing.groups())
        start,finish,duration=60*a+b,60*c+d,60*e+f
        assert start==last and finish-start==duration,record['id']
        last=finish
    assert last==180*60
    m=required_match(r'<script id="day-data" type="application/json">(.*?)</script>',source,re.S)
    source=source[:m.start(1)]+json.dumps(records,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')+source[m.end(1):]
    payload={'historical':data['historical_actual_runs'],'aligned':alignment(True),'positional':alignment(False)}
    tags='<script id="day-four-evidence" type="application/json">'+json.dumps(payload,separators=(',',':')).replace('<','\\u003c')+'</script>\n<script id="day-four-interactions">\n'+(ROOT/'tools/day4_interactions.js').read_text()+'\n</script>\n'
    source=source.replace('<script id="presentation-controller">',tags+'<script id="presentation-controller">',1)
    DECK.write_text(source)
    print('Built Day 4: 53 content slides + two breaks; Agentomics discussion fallback; no test access.')


if __name__=='__main__':build()
