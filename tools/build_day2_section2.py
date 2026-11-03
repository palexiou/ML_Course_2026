"""Build Day 2 learning slides from story.md, preserving the illustrated opening.

Native SVG and local JS are inlined in the standalone deck. No fitting or
empirical results are produced; all plotted numbers are teaching constructions.
"""
import html
import json
import math
from pathlib import Path
import re

from build_day2_section1 import (ROOT, DECK, BLUE, ORANGE, INK, GRAY, PURPLE,
                                  text, line, arrow, circle, svg, dna, network)

E=html.escape
PROVENANCE='''Constructed teaching figures, not fitted-model results. Carry forward counts (2,1,3), hidden features (1,1,0), output weights (1.2,−0.7,0.5), bias −0.2. Thus z=0.3, sigmoid(z)=0.5744425, and positive-label loss=0.5543552. Holding other parameters fixed gives z=v₁−0.9. At v₁=1.1/1.2/1.3, losses are 0.598139/0.554355/0.513015. Its derivative at 1.2 is (p−1)h₁=−0.4255575. A plain descent step with rate 0.1 gives v₁=1.2425557, p=0.5848112, loss=0.5364662. This is one example and one weight, not Adam training. The separate bowl uses L(w)=(w−1)², start w=3, rates 0.2 and 1.1. Checkpoint curves use epochs 1/8/16/24, losses 0.66/0.61/0.54/0.48, validation ROC-AUC 0.62/0.66/0.64/0.63; choose epoch 8. These are synthetic curves, not an executed course run. Actual code: course_code/03_representations.py fit_cnn; Adam lr=0.002, mean logits-based binary cross-entropy, batch size 64, shuffled epochs, 24 default epochs, earliest highest validation ROC-AUC checkpoint restored after training. Shared predict_cnn uses eval plus inference_mode then sigmoid. Test results never guide development. Suggested Section 2 pacing is 25 minutes, not rehearsed.'''


def curve(fn,domain,count=181):
    a,b=domain
    return [(a+(b-a)*i/(count-1),fn(a+(b-a)*i/(count-1))) for i in range(count)]


def chart(key,x,y,w,h,xmin,xmax,ymin,ymax,points=(),color=ORANGE,xticks=(),yticks=(),xlabel=''):
    def px(v):return x+(v-xmin)/(xmax-xmin)*w
    def py(v):return y+h-(v-ymin)/(ymax-ymin)*h
    attrs=' '.join(f'data-{k}="{v}"' for k,v in dict(x=x,y=y,w=w,h=h,xmin=xmin,xmax=xmax,ymin=ymin,ymax=ymax).items())
    p=f'<g data-chart="{key}" {attrs}>'
    p+=arrow(x,y+h,x+w+25,y+h,'#a9bdca',3)+arrow(x,y+h,x,y-20,'#a9bdca',3)
    for v in xticks:p+=line(px(v),y+h,px(v),y+h+10,'#a9bdca',2)+text(px(v),y+h+51,f'{v:g}',29,GRAY)
    for v in yticks:p+=text(x-25,py(v)+10,f'{v:g}',29,GRAY,'end')
    if points:
        pts=' '.join(f'{px(a):.2f},{py(b):.2f}' for a,b in points)
        p+=f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="7" stroke-linejoin="round"/>'
    if xlabel:p+=text(x+w/2,y+h+105,xlabel,35,GRAY)
    return p+'<g data-chart-overlay></g></g>'


def controls(content,readout=''):
    return f'<div class="d2-controls">{content}</div>'+(f'<p data-learning-readout aria-live="polite">{E(readout)}</p>' if readout else '')


def button(key,label,extra=''):
    return f'<button type="button" {key} {extra}>{E(label)}</button>'


def live(kind,p,ctl='',readout='',height=560):
    return f'<div class="d2-live learning-live" data-learning="{kind}">'+svg(p,f'Day 2 learning: {kind}',height)+controls(ctl,readout)+'</div>'


def weight_chart(key='weight',xmin=.8,xmax=1.6,ymin=.35,ymax=.8):
    return chart(key,720,70,830,355,xmin,xmax,ymin,ymax,
                 curve(lambda v:math.log1p(math.exp(.9-v)),(xmin,xmax)),xticks=[xmin,(xmin+xmax)/2,xmax],yticks=[ymin,ymax],xlabel='Output weight v₁')+text(685,35,'Loss',34,GRAY)


def miniature(x,y):
    p=''
    for a in [y-90,y,y+90]:
        for b in [y-55,y+55]:p+=line(x,a,x+230,b,'#b4c7d4',4)
    for b in [y-55,y+55]:p+=line(x+230,b,x+460,y,'#b4c7d4',4)
    for xx,ys in [(x,[y-90,y,y+90]),(x+230,[y-55,y+55]),(x+460,[y])]:
        for yy in ys:p+=circle(xx,yy,27,'',ORANGE if xx==x+230 else BLUE)
    return p


def figure(n):
    if n==1:return '<div class="learning-section-title"></div>'
    if n==2:
        p=network(output=True)
        p+='<g data-parameter="weight">'+line(778,180,1155,350,ORANGE,9)+text(1040,150,'weight v₁ = 1.2',40,ORANGE)+'</g>'
        p+='<g data-parameter="bias" opacity=".12">'+arrow(1210,605,1210,420,ORANGE,6)+text(1210,685,'bias −0.2',42,ORANGE)+'</g>'
        return live('parameters',p,button('data-parameter-select="weight"','Connection weight','aria-pressed="true"')+button('data-parameter-select="bias"','Neuron bias','aria-pressed="false"'),height=720)
    if n==3:
        p=network(output=True)+f'<g data-observed-label opacity="0">'+text(1450,90,'Observed B / y = 1',42,ORANGE)+'</g>'
        return live('forward',p,button('data-label-reveal','Reveal the training label'),height=600)
    if n==4:
        p=chart('loss',300,65,1150,365,.02,.98,0,4,curve(lambda q:-math.log(q),(.02,.98)),xticks=[.2,.5,.8],yticks=[0,2,4],xlabel='Predicted P(B)')
        p+=text(250,30,'Loss',34,GRAY)+text(1440,40,'Observed B / y = 1',36,BLUE)
        ctl=button('data-probability="0.8"','P(B) = 0.8')+button('data-probability="0.2"','P(B) = 0.2')+button('data-probability="current"','Our prediction')
        return live('loss',p,ctl,'P(B) ≈ 0.574 → loss ≈ 0.554')
    if n==5:
        p=circle(140,270,48,'h₁',BLUE,43)+arrow(190,270,460,270,ORANGE,7)+circle(510,270,48,'Σ',BLUE,43)
        p+=text(140,370,'1',44,BLUE)+text(335,195,'v₁',58,ORANGE)+text(335,440,'Other weights stay fixed',31,GRAY)
        p+=weight_chart()
        return live('gradient',p,'<label for="learning-weight">v₁ <input id="learning-weight" type="range" min="0.8" max="1.6" step="0.01" value="1.2"></label>'+button('data-weight="1.1"','1.1')+button('data-weight="1.2"','1.2')+button('data-weight="1.3"','1.3'),'v₁ = 1.20 → loss ≈ 0.554 · local gradient ≈ −0.426')
    if n==6:
        p=network(output=True)
        p+='<g data-backward="output" opacity=".08">'+arrow(1430,590,1265,420,ORANGE,6)+text(1480,680,'Loss ≈ 0.554',40,ORANGE)+'</g>'
        p+='<g data-backward="hidden" opacity=".08">'
        for yy in [180,350,520]:
            p+=f'<path d="M1150 335 Q1000 {yy-90} 795 {yy-30}" fill="none" stroke="{ORANGE}" stroke-width="5" stroke-dasharray="12 9"/>'+arrow(825,yy-30,790,yy-30,ORANGE,5)
        p+='</g><g data-backward="earlier" opacity=".08">'
        for yy in [180,350,520]:p+=arrow(650,yy-45,305,yy-45,ORANGE,4)
        p+='</g>'
        return live('backprop',p,button('data-backward-next','Trace loss sensitivity')+button('data-backward-reset','Reset'),height=720)
    if n==7:
        p=text(320,175,'v₁ ← v₁ − ηg',61,BLUE)+text(320,300,'g ≈ −0.426',48,ORANGE)+text(320,400,'η = 0.1',46,GRAY)
        p+=weight_chart('update',1.18,1.28,.52,.57)
        return live('update',p,button('data-weight-step','Take one step')+button('data-weight-reset','Reset'),'v₁ = 1.200 → P(B) ≈ 0.574 → loss ≈ 0.554')
    if n==8:
        p=''
        for key,x,rate in [('small',140,.2),('large',965,1.1)]:
            p+=text(x+280,35,f'Learning rate {rate}',40,BLUE if key=='small' else ORANGE)
            p+=chart(key,x,85,580,345,-4.4,7.4,0,45,curve(lambda w:(w-1)**2,(-4.4,7.4)),color='#b3c7d4',xticks=[-4,1,7],yticks=[0,20,40],xlabel='Weight w')
        return live('rate',p,button('data-rate-next','Next step')+button('data-rate-reset','Reset'),'Same starting weight, different step sizes · step 0 of 6')
    if n==9:
        p=''
        for i,seq in enumerate(['ACGTAC','TATACG','CCGTTA','GATACC']):p+=dna(90,125+i*105,seq,step=45,size=35)
        p+=text(245,560,'One minibatch: up to 64 examples',35,BLUE)
        p+=arrow(435,300,620,300)+circle(765,300,100,'Mean loss',BLUE,35)
        p+=arrow(880,300,1030,300)+circle(1150,300,90,'∇L',ORANGE,65)
        p+=arrow(1255,300,1405,300)+circle(1510,300,82,'Step',BLUE,42)
        p+=text(1150,485,'Combined gradient',35,ORANGE)+text(1510,485,'One update',35,BLUE)
        return svg(p,'A minibatch combines examples into a mean loss, a gradient and one optimizer update')
    if n==10:
        p=text(864,35,'720 training examples',45,BLUE)
        for i in range(12):
            x=180+(i%6)*270;y=190+(i//6)*230
            p+=f'<g data-epoch-batch="{i}">'+circle(x,y,65,'64' if i<11 else '16',BLUE,45)+text(x,y+110,f'Batch {i+1}',29,GRAY)
            p+=text(x,y+155,f'Rows {i*64+1}–{min(720,(i+1)*64)}',25,GRAY,attrs='data-epoch-rows')+'</g>'
        return live('epoch',p,button('data-epoch-next','Next update')+button('data-epoch-reset','Reset'),'Epoch 1 · 0 / 12 updates · 0 / 720 examples',height=600)
    if n==11:
        lines=['optimizer.zero_grad()','logits = model(inputs[indices])','loss = nn.functional.binary_cross_entropy_with_logits(logits, labels[indices])','loss.backward()','optimizer.step()']
        code=''.join(f'<div data-code-line="{i}" class="{"current" if i==0 else ""}">{E(v)}</div>' for i,v in enumerate(lines))
        return '<div class="d2-live learning-live learning-code" data-learning="code"><pre aria-label="One minibatch training step"><code>'+code+'</code></pre>'+controls(button('data-code-next','Next operation')+button('data-code-reset','Reset'),'Clear old gradients before the next minibatch.')+'</div>'
    if n==12:
        p=''
        for key,x,values,lo,hi,title,c in [('train',140,[.66,.61,.54,.48],.4,.7,'Training loss',BLUE),('validation',965,[.62,.66,.64,.63],.5,.7,'Validation ROC-AUC',ORANGE)]:
            p+=text(x+280,35,title,43,c)
            p+=chart(key,x,90,580,335,1,24,lo,hi,list(zip([1,8,16,24],values)),color=c,xticks=[1,8,16,24],yticks=[lo,hi],xlabel='Epoch')
        return live('validation',p,button('data-select-checkpoint','Select the checkpoint'),'Training improves; validation does not keep improving.')
    if n==13:
        p=text(445,60,'Training',55,BLUE)+text(1280,60,'Inference',55,ORANGE)
        p+=miniature(170,300)+miniature(1005,300)
        p+=text(400,570,'Weights change with updates',38,BLUE)+text(1250,570,'Selected weights stay fixed',38,ORANGE)
        p+=f'<path d="M630 350 Q700 500 400 480 Q190 480 170 390" stroke="{BLUE}" stroke-width="5" stroke-dasharray="12 10" fill="none"/>'+arrow(200,410,170,390,BLUE)
        p+=text(1290,670,'New input → P(B)',49,ORANGE)
        return svg(p,'Training updates parameters using labels; inference applies the selected weights without updates')
    p=text(100,120,'What would you want to watch',62,BLUE,'start')+text(100,210,'while this model learns?',62,BLUE,'start')
    p+=chart('discussion',1000,330,540,220,0,1,0,1,curve(lambda x:.1+.8*math.exp(-4*x),(0,1)),color='#adc4d2')
    p+=text(100,540,'Then: how should we give it DNA?',44,GRAY,'start')
    return svg(p,'Open discussion about what to inspect during learning, then transition to positional DNA')


CSS='''/* DAY 2 SECTION 2 — LEARNING */
.day-two-learning>.content{height:740px}
.day-two-learning .learning-live>svg{height:560px}
.day-two-learning [data-learning=parameters]>svg,.day-two-learning [data-learning=backprop]>svg{height:650px}
.day-two-learning [data-learning=forward]>svg,.day-two-learning [data-learning=epoch]>svg{height:600px}
.day-two-learning .d2-controls{min-height:68px}
.day-two-learning input[type=range]{width:530px}
.day-two-learning:has(.learning-section-title) h1{position:absolute;left:160px;top:380px;font-size:112px;line-height:1.1;max-width:1540px}
.learning-section-title{position:absolute;left:64px;top:400px;width:150px;height:6px;background:#0072B2}
.learning-code pre{position:absolute;top:35px;left:50px;width:1628px;background:white;padding:0;border:0;border-radius:0;color:#697782;font:32px/1.5 monospace;white-space:pre}
.learning-code pre code{font:inherit;color:inherit;background:none;padding:0}
.learning-code [data-code-line]{padding:20px 12px;border-left:6px solid transparent;transition:color .2s}
.learning-code [data-code-line].current{color:#0072B2;background:#edf5fa;border-left-color:#0072B2}
.learning-code>.d2-controls{position:absolute;top:560px;width:1728px}
.learning-code>[data-learning-readout]{position:absolute;top:650px;width:1728px}
.day-two-learning [data-epoch-batch] circle{transition:fill .2s}
.day-two-learning [data-epoch-batch].done circle{fill:#e9f3f9;stroke:#0072B2}
.day-two-learning [data-epoch-batch].current circle{fill:#fff0e6;stroke:#D55E00;stroke-width:8}
.day-two-learning [data-learning-readout]{min-height:46px}
.day-two-learning [data-parameter],.day-two-learning [data-observed-label],.day-two-learning [data-backward]{transition:opacity .25s}
@media print{.learning-code [data-code-line]{color:#18344b!important;background:none!important;border-color:transparent!important}}
/* END DAY 2 SECTION 2 */
'''


def records():
    story=(ROOT/'Slides/Day_2/story.md').read_text().split('<a id="section-2"></a>')[1].split('<a id="section-3"></a>')[0]
    blocks=re.findall(r'### S2-(\d+) · (.*?)\n(.*?)(?=\n### |\n\*\*Construction|\Z)',story,re.S)
    assert len(blocks)==14
    records=[]
    for num,title,body in blocks:
        def field(name):
            value=re.search(r'\*\*'+re.escape(name)+r':\*\* (.*?)(?=\n\n|\Z)',body,re.S)[1]
            return E(value).replace('`','')
        key=re.search(r'\*\*Proposed slide ID:\*\* `([^`]+)`',body)[1]
        provenance=PROVENANCE
        if int(num)==10:provenance+=' Epoch row labels illustrate positions within a training set, not real sample IDs. Subsequent passes show a deterministic permutation for visual explanation rather than Torch\'s actual shuffled order.'
        records.append(dict(day=2,id=key,anchor=key,sectionLearning=True,kind='day-two-opening day-two-learning',title=title,time=field('Time'),body=figure(int(num)),subtitle='',takeaway='',notes=field('What I want to say'),point=field('Point / reveal'),transition=field('Transition'),sourceNote=E(provenance)))
    key='day-2-s2-break'
    records.append(dict(day=2,id=key,anchor=key,sectionLearning=True,kind='day-two-opening day-two-learning',title='Break',time='50–60 · 10 minutes',body=svg(text(864,350,'10 minutes',120,BLUE),'Ten-minute break'),subtitle='',takeaway='',notes='Return in ten minutes. Next: encode DNA while preserving sequence order.',point='Take the full break.',transition='From learning weights to reading DNA in position.',sourceNote='The break is separate from the 25-minute Section 2 teaching allocation.'))
    return records


def build():
    source=DECK.read_text();m=re.search(r'<script id="day-data" type="application/json">(.*?)</script>',source,re.S)
    old=json.loads(m[1]);opening=[s for s in old if s.get('sectionOne')];assert len(opening)==12
    later=[s for s in old if not s.get('sectionOne') and not s.get('sectionLearning') and s['anchor'] not in ['day-2-slide-3','day-2-slide-4','day-2-slide-6']]
    assert len(later)==10 and later[0]['anchor']=='day-2-slide-5'
    current=opening+records()+later
    source=source[:m.start(1)]+json.dumps(current,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')+source[m.end(1):]
    source=re.sub(r'/\* DAY 2 SECTION 2 — LEARNING \*/.*?/\* END DAY 2 SECTION 2 \*/\n','',source,flags=re.S)
    source=source.replace('</style>',CSS+'</style>',1)
    source=source.replace('${slide.sectionOne ?', '${slide.sectionOne || slide.sectionLearning ?')
    source=source.replace('href="story.md#section-1">Section 1 story','href="story.md#section-${slide.sectionLearning ? 2 : 1}">Section ${slide.sectionLearning ? 2 : 1} story')
    aliases={'#day-2-slide-1':'day-2-s1-welcome','#day-2-slide-2':'day-2-s1-weighted-sum','#day-2-slide-3':'day-2-s2-loss','#day-2-slide-4':'day-2-s2-update','#day-2-slide-6':'day-2-s2-break'}
    source=re.sub(r'const openingAliases = \{.*?\};','const openingAliases = '+json.dumps(aliases)+';',source)
    source=re.sub(r'<script id="day-two-learning-interactions">.*?</script>\n?','',source,flags=re.S)
    js=(ROOT/'tools/day2_section2_interactions.js').read_text()
    source=source.replace('<script id="presentation-controller">','<script id="day-two-learning-interactions">\n'+js+'\n</script>\n<script id="presentation-controller">',1)
    if 'bindDayTwoLearning();' not in source:source=source.replace('bindDayTwoOpening();','bindDayTwoOpening();\nbindDayTwoLearning();')
    DECK.write_text(source)
    print(f'Built 14 learning slides + break; preserved 12 opening and 10 later records ({len(current)} total).')


if __name__=='__main__':build()
