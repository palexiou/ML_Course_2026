"""Build reviewed Day 2 Sections 5–6 from story and source-bound validation evidence.

No models run during this build or in HTML. Rebuild after the generated notebook
rehearsal refreshes instructor/verification/day2-current.json.
"""
from collections import Counter
import hashlib
import html
import json
import re
from build_day2_section1 import required_match

from build_day2_section1 import ROOT, DECK, BLUE, ORANGE, INK, GRAY, PURPLE, text, line, arrow, circle, svg, dna, helix

E = html.escape
NOTEBOOK = 'https://colab.research.google.com/github/palexiou/ML_Course_2026/blob/main/notebooks/03_representations.ipynb'
METHODS = ['Logistic regression', 'Random forest', 'CNN']


def button(action, label):
    return f'<button type="button" data-eval-action="{action}">{E(label)}</button>'


def live(kind, controls='', caption='', figure='', height=560):
    return (f'<div class="d2-live evaluation-live" data-evaluation="{kind}">'
            + svg('<g data-eval-draw>'+figure+'</g>', 'Day 2: '+kind, height)
            + f'<div class="d2-controls">{controls}</div><p data-eval-readout aria-live="polite">{E(caption)}</p></div>')


def prompt(first, second=''):
    return svg(text(100,210,first,64,BLUE,'start')+(text(100,310,second,64,BLUE,'start') if second else ''),'Audience discussion')


def strand(y, first=True, moved=False, label=True):
    p=line(240,y,1550,y,'#b9cbd7',5)
    starts=[550,1080] if not moved else [760,1310]
    for i,x in enumerate(starts):
        motif,color=(('TATAAATG',BLUE) if (i==0)==first else ('CGGACGTC',ORANGE))
        p+=dna(x-160,y-14,motif,44,size=37,highlights=[(0,8,color)])
        p+=text(x,y+100,(38 if i==0 else 86) if not moved else '?',30,GRAY)
    if label:p+=text(130,y+12,'B' if first else 'A',48,BLUE if first else ORANGE)
    return p


def paired():
    return strand(170)+strand(430,False)+text(864,610,'Shared background · two fixed slots',39,GRAY)


def tally(x,y,values,colors=None):
    p=''
    for i,v in enumerate(values):
        c=(colors or [BLUE]*len(values))[i];xx=x+i*65
        p+=line(xx,y,xx,y-35*v,c,12)
    return p


def stage5(n,data):
    if n==1:return '<div class="evaluation-title-rule"></div>'
    if n==2:
        p=''
        for i,row in enumerate(data['task_examples']):
            yy=110+i*185;p+=text(110,yy+10,'B' if row['label'] else 'A',42,BLUE if row['label'] else ORANGE)
            p+=dna(235,yy,row['sequence'][30:55],49,size=35)
        p+=arrow(400,470,1300,470,BLUE,3)+text(360,485,'0',33,GRAY)+text(1345,485,'1',33,GRAY)+text(864,570,'p(B)',50,BLUE)
        return svg(p,'Actual primary validation DNA examples and the target probability')
    if n==3:
        p=dna(90,300,'ACGTATACGT',44,size=36)+text(285,410,'Same sequences',35,GRAY)
        p+=arrow(600,270,760,150,BLUE)+arrow(600,330,760,470,ORANGE)
        p+=tally(865,205,[2,1,3,2])+text(970,80,'4-mer counts',40,BLUE)+text(1350,135,'Logistic / forest',38,BLUE)
        p+=dna(820,480,'ACGTATACGT',42,size=34)+text(1005,580,'Ordered bases',40,ORANGE)+text(1400,480,'CNN',47,ORANGE)
        return svg(p,'Same training and validation rows; different representations and predictors')
    if n==4:
        return ('<div class="evaluation-notebook"><p>GitHub → Open in Colab</p><a href="'+NOTEBOOK+'" target="_blank" rel="noopener">Open the Day 2 notebook ↗</a><p class="route">Setup → shared definitions → stage 03 → Section 5</p></div>')
    if n==5:
        p=text(410,80,'N × 4 × 160',54,BLUE)
        for i,b in enumerate('ACGT'):
            p+=text(150,190+i*72,b,36,GRAY)
            for j in range(12):p+=circle(240+j*38,177+i*72,9,'',BLUE if j%4==i else '#c3d0d9',12)
        p+=arrow(780,300,990,300)+circle(1120,300,75,'z',BLUE,64)+arrow(1205,300,1405,300)+text(1520,320,'p(B)',62,ORANGE)
        p+=text(864,590,'Adam 0.002 · batch 64 · 24 epochs',45,BLUE)
        return svg(p,'Actual one-hot input, one logit, inference sigmoid and declared training settings')
    if n==6:
        return '<div class="evaluation-notebook"><pre><code>run_representations(\n    seed=2026, epochs=24,\n    show_plot=False\n)</code></pre><p class="route">Run once in the notebook. Then inspect.</p><a href="'+NOTEBOOK+'" target="_blank" rel="noopener">Return to the notebook ↗</a></div>'
    if n in [7,8,9]:
        kind={7:'training',8:'validation',9:'checkpoint'}[n]
        return live(kind,button('checkpoint','Mark selected epoch') if n==9 else '', 'Saved local run · 24 epochs · validation only')
    if n==10:return live('prediction',button('row','Next validation row')+button('label','Reveal observed label'),'Fixed weights · first validation row')
    if n==11:
        return live('response','<label>Row <select data-eval-row aria-label="Validation row">'+''.join(f'<option value="{i}">{i}</option>' for i in range(3))+'</select></label><label>Channel <select data-eval-channel aria-label="Response channel">'+''.join(f'<option value="{i}">{i}</option>' for i in range(16))+'</select></label>','Second convolution · post-ReLU response')
    if n==12:return live('metrics',button('metric','Show average precision'),'Primary PPM · 240 validation records')
    if n==13:
        seconds=data['run']['runs']['simple']['seconds']
        p=tally(280,285,[2,1,3,2])+text(380,400,'Counts',48,BLUE)+dna(960,260,'ACGTATACGT',55,size=42)+text(1220,400,'Ordered sequence',48,ORANGE)
        p+=text(864,595,f'{seconds:.2f} s · CPU · primary workflow, all three methods',40,GRAY)
        return svg(p,'Representation choices and measured aggregate primary-workflow runtime, not per-model timing')
    return prompt('What would help you','understand this result?')


def stage6(n,data):
    if n==1:return '<div class="evaluation-title-rule"></div>'
    if n==2:return live('swap',button('swap','Swap the blocks'), 'B: first order · A: reverse order',paired(),650)
    if n==3:
        p=dna(125,190,'GGGGGGTATAAATGCCCCCC',77,size=41,highlights=[(6,14,BLUE)])
        p+=f'<rect x="{125+4*77-32}" y="125" width="300" height="112" rx="15" stroke="{ORANGE}" stroke-width="4" fill="none"/>'
        p+=dna(125,435,'GGGGGGCGGACGTCCCCCCC',77,size=41,highlights=[(6,14,ORANGE)])
        p+=text(864,610,'Keep boundary-spanning 4-mers too',45,BLUE)
        return svg(p,'Matching six-base flanks preserve motif and outer boundary words')
    if n==4:
        pair=data['control_pairs'][0]['records'];bag=Counter(pair[0]['sequence'][i:i+4] for i in range(157));vals=[v for k,v in sorted(bag.items())[:14]]
        p=text(135,210,'B',44,BLUE)+text(135,470,'A',44,ORANGE)+tally(300,260,vals)+tally(300,520,vals,[ORANGE]*14)
        p+=text(1450,365,'=',115,BLUE)+text(864,660,'All 4-mer counts match · 157 windows per sequence',42,GRAY)
        return svg(p,'A fourteen-feature excerpt of equal profiles; complete Counter equality verified for all words')
    if n==5:
        p=tally(180,365,[2,3,1,2])+arrow(520,300,720,300)+circle(835,300,75,'f(x)',BLUE,50)
        for y,label,c in [(150,'A',ORANGE),(460,'B',BLUE)]:p+=arrow(920,300,1210,y,c)+circle(1340,y,62,'p',c,52)+text(1500,y+18,label,46,c)
        p+=text(864,645,'x₁ = x₂  ⇒  f(x₁) = f(x₂)',58,BLUE)
        return svg(p,'Identical bag inputs force identical deterministic predictor scores')
    if n==6:return live('chance',button('partners','Reveal opposite-label partners'),'Identical score distributions → ROC-AUC 0.5')
    if n==7:
        p=''
        for r,first in enumerate([True,False]):
            yy=130+r*285;p+=text(110,yy+55,'B' if first else 'A',45,BLUE if first else ORANGE)
            seq='TATAAATGCGGACGTC' if first else 'CGGACGTCTATAAATG'
            for i,b in enumerate('ACGT'):
                p+=text(255,yy+i*45,b,28,GRAY)
                for j,nt in enumerate(seq):
                    if b==nt:p+=circle(370+j*66,yy+i*45-10,10,'',BLUE if (j<8)==first else ORANGE,12)
        p+=text(864,690,'Different letters at the same positions',42,BLUE)
        return svg(p,'Excerpts of the positional one-hot inputs retain the swapped motif distinction')
    if n==8:return live('head',button('head','Keep the positions'),'Local receptive field: 11 bases')
    if n==9:return live('paired-metrics',button('variant','Show order control'),'Primary PPM · 240 validation records')
    if n==10:return live('pair',button('pair','Next validation pair')+button('pair-reveal','Reveal model probabilities'),'Check all counts before comparing predictions')
    if n==11:
        p=strand(180,moved=True)+text(864,450,'?',135,ORANGE)+text(864,640,'Unfamiliar positions',46,BLUE)
        return svg(p,'Hypothetical movement to unfamiliar slots; no prediction assigned')
    if n==12:
        p=''
        for i,(label,color) in enumerate([('Counts',BLUE),('Ordered bases',ORANGE),('Learned local features',PURPLE)]):
            x=310+i*560;p+=text(x,100,label,42,color)
            if i==0:p+=tally(x-120,360,[2,1,3,2])
            elif i==1:p+=dna(x-190,300,'ACGTACGT',54,size=38)
            else:
                for j,v in enumerate([20,95,35,10,110,20,60]):p+=line(x-180+j*62,360,x-180+j*62,360-v,color,7)
        p+=text(864,620,'Retain information → learn to use it → evaluate',46,BLUE)
        return svg(p,'Three representations retain different information; fitting and evaluation remain distinct')
    if n==13:return prompt('What information would you','want your model to keep?')
    p=helix(90,245,490,95)+arrow(665,245,850,245)
    for i,v in enumerate([60,120,35,90]):p+=line(980+i*90,310,980+i*90,310-v,PURPLE,14)
    p+=arrow(1370,245,1550,245)+circle(1620,245,46,'p',BLUE,50)+text(864,550,'Day 3 · reuse pretrained features',62,BLUE)
    return svg(p,'Features learned before our task become a representation for Day 3')


CSS='''/* === DAY 2 TRAINING AND REPRESENTATION EVIDENCE === */
.day-two-evaluation .evaluation-live>svg{height:560px}
.day-two-evaluation .evaluation-live:has(svg[viewBox="0 0 1728 650"])>svg{height:650px}
.day-two-evaluation .evaluation-live>p{font-size:31px;line-height:1.3;min-height:42px;margin:20px 0 0;text-align:center;color:#697782}
.day-two-evaluation .d2-controls{min-height:68px}
.day-two-evaluation .d2-controls:empty{display:none}
.day-two-evaluation select{font:inherit;border:2px solid #a6bdcc;border-radius:10px;padding:6px 18px;background:white;color:#0072B2}
.day-two-evaluation .d2-controls label{font-size:30px;display:flex;align-items:center;gap:16px}
.day-two-evaluation:has(.evaluation-title-rule) h1{position:absolute;left:160px;top:350px;max-width:1500px;font-size:108px;line-height:1.12}
.evaluation-title-rule{position:absolute;left:64px;top:410px;width:150px;height:6px;background:#0072B2}
.evaluation-notebook{padding:70px 80px}
.evaluation-notebook p{font-size:57px;line-height:1.35;margin:0 0 55px}
.evaluation-notebook a{font-size:43px;color:#0072B2;display:inline-block;margin-bottom:55px}
.evaluation-notebook .route{font-size:36px;color:#697782}
.evaluation-notebook pre,.evaluation-notebook code{color:#18344b}
.evaluation-notebook pre{font-size:48px;line-height:1.5;border:0;background:none;padding:0;margin:0 0 35px}
/* === END DAY 2 TRAINING AND REPRESENTATION EVIDENCE === */
'''


def build():
    data=json.loads((ROOT/'instructor/verification/day2-current.json').read_text())
    assert not data['test_evaluated']
    for path,sha in data['source_sha256'].items():
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==sha, f'Stale Day 2 evidence: {path}; rehearse/refresh before rebuilding.'
    source=DECK.read_text();m=required_match(r'<script id="day-data" type="application/json">(.*?)</script>',source,re.S);old=json.loads(m[1])
    kept=[s for s in old if not s.get('sectionEvaluation') and s['anchor'] not in {f'day-2-slide-{i}' for i in [9,11,12,13,14,15]}]
    assert len(kept)==58,'Build Sections 1–4 and both breaks first.'
    current=list(kept)
    story=(ROOT/'Slides/Day_2/story.md').read_text()
    for section in [5,6]:
        span=story.split(f'<a id="section-{section}"></a>')[1].split('<a id="section-6"></a>' if section==5 else '<a id="notebook-plan"></a>')[0]
        blocks=re.findall(rf'### S{section}-(\d+) · (.*?)\n(.*?)(?=\n### |\Z)',span,re.S);assert len(blocks)==14
        for number,title,body in blocks:
            def field(name):return E(required_match(r'\*\*'+re.escape(name)+r':\*\* (.*?)(?=\n\n|\Z)',body,re.S)[1]).replace('`','')
            key=required_match(r'\*\*Proposed slide ID:\*\* `([^`]+)`',body)[1]
            provenance=('Local generated Day 2 notebook rehearsal, 2026-11-03; seed2026, CPU2threads, 24epochs; current PPM primary and separate fixed-slot paired control. Validation only. Empirical curves/probabilities/maps/metrics come from instructor/verification/day2-current.json. Constructed conceptual dot distributions and response sketches explain mechanisms, not additional model runs. Counter equality checked for all48 validation pairs; bag scores give ROC-AUC0.5. Model and notebook source hashes gate this builder. Runtime is aggregate per variant, not CNN-only. Map inspection is not attribution or biological proof. Colab, pacing and projector verification remain separate. No model training runs in HTML.')
            current.append(dict(day=2,id=key,anchor=key,sectionEvaluation=True,sectionSequence=True,sectionNumber=section,kind='day-two-opening day-two-evaluation',title=title,time=field('Time'),body=(stage5 if section==5 else stage6)(int(number),data),subtitle='',takeaway='',notes=field('What I want to say'),point=field('Point / reveal'),transition=field('Transition'),sourceNote=E(provenance)))
    source=source[:m.start(1)]+json.dumps(current,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')+source[m.end(1):]
    source=re.sub(r'/\* === DAY 2 TRAINING AND REPRESENTATION EVIDENCE === \*/.*?/\* === END DAY 2 TRAINING AND REPRESENTATION EVIDENCE === \*/\n','',source,flags=re.S)
    source=source.replace('</style>',CSS+'</style>',1)
    for ident in ['day-two-evaluation-data','day-two-evaluation-interactions']:
        source=re.sub(r'<script id="'+ident+'"[^>]*>.*?</script>\n?','',source,flags=re.S)
    payload={k:data[k] for k in ['histories','selected_epochs','metrics','primary_examples','control_pairs']}
    data_tag='<script id="day-two-evaluation-data" type="application/json">'+json.dumps(payload,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')+'</script>\n'
    js='<script id="day-two-evaluation-interactions">\n'+(ROOT/'tools/day2_evaluation_interactions.js').read_text()+'\n</script>\n'
    source=source.replace('<script id="presentation-controller">',data_tag+js+'<script id="presentation-controller">',1)
    if 'bindDayTwoEvaluation();' not in source:source=source.replace('bindDayTwoSequence();','bindDayTwoSequence();\nbindDayTwoEvaluation();')
    aliases=json.loads(required_match(r'const openingAliases = (\{.*?\});',source)[1])
    aliases.update({f'#day-2-slide-{n}':key for n,key in [(9,'day-2-s5-open-notebook'),(11,'day-2-s6-pair'),(12,'day-2-s5-run'),(13,'day-2-s6-paired-results'),(14,'day-2-s6-notebook'),(15,'day-2-s6-synthesis')]})
    source=re.sub(r'const openingAliases = \{.*?\};','const openingAliases = '+json.dumps(aliases)+';',source)
    DECK.write_text(source)
    print('Built Sections 5–6: 28 scenes;',len(current),'total; first58 records preserved.')


if __name__=='__main__':build()
