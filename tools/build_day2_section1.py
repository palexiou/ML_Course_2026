"""Build the approved Day 2 opening; retain the later section records.

The self-contained HTML is the delivery artifact. Figures are native SVG;
all numerical examples are teaching constructions, not fitted model results.
"""
from collections import Counter
import html
import json
import math
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
DECK = ROOT / 'Slides/Day_2/presentation.html'
BLUE, ORANGE, INK, GRAY, PURPLE = '#0072B2', '#D55E00', '#18344b', '#697782', '#7B4FA3'
COLORS = [ORANGE, BLUE, PURPLE]
SEQ = 'TATACCGCGCGCGTATAAATG'
E = html.escape


def required_match(pattern: str, value: str, flags: int = 0) -> re.Match[str]:
    result = re.search(pattern, value, flags)
    assert result is not None, f"Required deck/story pattern missing: {pattern}"
    return result


def text(x, y, value, size=44, color=INK, anchor='middle', weight=400, attrs=''):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" text-anchor="{anchor}" font-weight="{weight}" {attrs}>{E(str(value))}</text>'


def line(x1, y1, x2, y2, color=GRAY, width=4, attrs=''):
    return f'<path d="M{x1} {y1} L{x2} {y2}" fill="none" stroke="{color}" stroke-width="{width}" {attrs}/>'


def arrow(x1, y1, x2, y2, color=GRAY, width=4):
    a = math.atan2(y2-y1, x2-x1)
    return line(x1,y1,x2,y2,color,width)+''.join(line(x2,y2,x2-18*math.cos(a+d),y2-18*math.sin(a+d),color,width) for d in [-.5,.5])


def circle(x,y,r,label='',color=BLUE,size=44,attrs=''):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="white" stroke="{color}" stroke-width="5" {attrs}/>'+text(x,y+size*.32,label,size,color)


def svg(p,label,height=720):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1728 {height}" role="img" aria-label="{E(label,quote=True)}"><title>{E(label)}</title>{p}</svg>'


def dna(x,y,seq=SEQ,step=66,highlights=(),size=46):
    p=line(x-20,y+30,x+(len(seq)-1)*step+20,y+30,'#c4d0d9',3)
    for i,b in enumerate(seq):
        color=next((c for start,end,c in highlights if start<=i<end),INK)
        if color!=INK:p+=f'<circle cx="{x+i*step}" cy="{y-15}" r="32" fill="{color}" fill-opacity=".09"/>'
        p+=text(x+i*step,y,b,size,color,weight=600)
    return p


def helix(x,y,w=700,h=150):
    p=''
    for phase,c in [(0,BLUE),(math.pi,ORANGE)]:
        points=[(x+w*i/120,y+h*math.sin(i/120*math.pi*3+phase)) for i in range(121)]
        p+=f'<polyline points="{" ".join(f"{a:.1f},{b:.1f}" for a,b in points)}" fill="none" stroke="{c}" stroke-width="10" stroke-linecap="round"/>'
    for i in range(2,25):
        xx=x+w*i/26;dy=h*math.sin(i/26*math.pi*3)
        p+=line(xx,y-dy,xx,y+dy,'#a8bccb',4)
    return p


def plot(x,y,w,h,kind='sigmoid',labels=True):
    xmin,xmax=-3,3;ymin,ymax=(0,1) if kind=='sigmoid' else (0,3)
    px=lambda z:x+(z-xmin)/(xmax-xmin)*w
    py=lambda v:y+h-v/ymax*h
    p=arrow(x-20,y+h,x+w+32,y+h,'#a8bac6',3)+arrow(px(0),y+h+12,px(0),y-22,'#a8bac6',3)
    pts=[]
    for i in range(181):
        z=xmin+(xmax-xmin)*i/180;v=1/(1+math.exp(-z)) if kind=='sigmoid' else max(0,z)
        pts.append(f'{px(z):.2f},{py(v):.2f}')
    p+=f'<polyline points="{" ".join(pts)}" fill="none" stroke="{ORANGE}" stroke-width="8" stroke-linejoin="round"/>'
    if labels:
        for z in [-3,0,3]:p+=text(px(z),y+h+46,z,30,GRAY)
        p+=text(px(0)-24,y+10,ymax,30,GRAY,'end')+text(x+w+45,y+h+12,'z',34,GRAY)
    return p


def inputs(x=230,ys=(180,350,520)):
    return ''.join(text(x-85,y+14,k,36,c,'end')+circle(x,y,48,n,c,44) for y,k,n,c in zip(ys,['TATA','AATG','CGCG'],[2,1,3],COLORS))


def network(output=False,deep=False,focus=False):
    ys=[180,350,520];hx=720
    p=''
    for j,yh in enumerate(ys):
        edges=''.join(line(278,yi,hx-58,yh,COLORS[i],3) for i,yi in enumerate(ys))
        p+=f'<g data-unit-path="{j}" opacity="{1 if j==0 or not focus else .16}">{edges}</g>'
    p+=inputs()
    for j,y in enumerate(ys):p+=circle(hx,y,58,f'h{["₁","₂","₃"][j]}',BLUE,44,attrs=f'data-hidden-node="{j}"')
    p+=text(230,85,'Counts',36,GRAY)+text(hx,85,'Hidden features',36,GRAY)
    if output:
        if deep:
            for y in ys:
                for y2 in [265,435]:p+=line(hx+58,y,1100-50,y2,'#a8bccb',3)
            for y in [265,435]:p+=line(1150,y,1460,350,'#a8bccb',3)+circle(1100,y,50,'',ORANGE)
            p+=circle(1515,350,55,'z',BLUE)+text(1100,85,'Combine again',36,GRAY)+text(1515,85,'Output',36,GRAY)
            p+=text(864,670,'Later layers use the features made by earlier layers',44,GRAY)
        else:
            p+='<g data-forward-part="output">'
            for j,y in enumerate(ys):
                p+=line(hx+58,y,1155,350,'#9bb4c5',4)+text(hx+115,y+15,[1,1,0][j],40,ORANGE,'start')
            p+=circle(1210,350,55,'Σ',BLUE,48)+text(1210,480,'z = 0.3',42,BLUE)
            p+='</g><g data-forward-part="probability">'+arrow(1265,350,1375,350)+plot(1400,200,230,180)
            p+=text(1520,550,'P(B) ≈ 0.574',43,ORANGE)+'</g>'
    elif not focus:
        p+=arrow(778,350,1150,350,BLUE,5)+text(1170,325,'h₁ = 1',66,ORANGE,'start')+text(1170,395,'a new feature',42,GRAY,'start')
    return p


def figure(n):
    p=''
    if n==1:
        p=helix(80,240,650,120)+arrow(800,240,980,240,BLUE)
        for x,ys in [(1080,[150,330]),(1310,[100,240,380]),(1530,[240])]:
            for yy in ys:
                if x<1530:
                    targets=[100,240,380] if x==1080 else [240]
                    for ty in targets:p+=line(x,yy,x+230,ty,'#b6c8d5',4)
        for x,ys in [(1080,[150,330]),(1310,[100,240,380]),(1540,[240])]:
            for yy in ys:p+=circle(x,yy,24,'',ORANGE if x==1310 else BLUE)
        p+=text(864,510,'Day 2',52,BLUE)
        labels=['Define & evaluate','Learn the features','Reuse pretrained features','Specify & audit']
        p+=line(145,600,1585,600,'#d6e0e7',4)
        for i,label in enumerate(labels):
            x=195+i*445;c=BLUE if i==1 else '#7b8993'
            p+=f'<circle cx="{x}" cy="600" r="{15 if i==1 else 8}" fill="{c}"/>'+text(x,650,f'{i+1}. {label}',30,c)
    elif n==2:
        p=dna(170,145,step=68,highlights=[(0,4,ORANGE),(5,13,PURPLE),(13,17,ORANGE),(17,21,BLUE)])
        for i,(k,count,c) in enumerate(zip(['TATA','AATG','CGCG'],[2,1,3],COLORS)):
            x=400+i*465
            p+=arrow(x,220,x,310,'#b7c7d3')+text(x,380,k,52,c)
            for j in range(count):p+=f'<circle cx="{x+(j-(count-1)/2)*54}" cy="465" r="19" fill="{c}"/>'
            p+=text(x,560,count,65,c)
        p+=text(864,680,'Which words? How many? Their positions are gone.',43,GRAY)
    elif n==3:
        for y,label in [(170,'Choose features'),(480,'Learn features')]:p+=text(85,y-80,label,38,GRAY,'start')
        for i,(k,v,c) in enumerate(zip(['TATA','AATG','CGCG'],[2,1,3],COLORS)):
            y=140+i*57;p+=text(120,y+13,k,28,c,'start')+line(220,y,220+v*45,y,c,17)
        p+=arrow(420,205,600,205)+circle(810,205,75,'f(x)',BLUE,43)+arrow(900,205,1220,205)+text(1450,220,'P(B)',65,BLUE)
        p+=dna(95,510,'ACGTATACGT',step=42,size=33)+arrow(530,495,650,495)
        for i,h in enumerate([90,130,55]):
            x=745+i*120;p+=line(x,550,x,550-h,ORANGE,30)
        p+=text(865,620,'Fitted intermediate features',33,ORANGE)+arrow(1080,495,1220,495)+text(1450,510,'P(B)',65,BLUE)
    elif n==4:
        p=inputs(270,[170,340,510])
        for i,(y,c,w,contribution) in enumerate(zip([170,340,510],COLORS,['× 0.6','× 0.8','× −0.2'],['+1.2','+0.8','−0.6'])):
            p+=text(460,y+14,w,43,c)+arrow(565,y,790,340,c,4)+text(670,y-22,contribution,36,c)
        p+=circle(850,340,60,'Σ',BLUE,54)+text(850,485,'bias −0.4',36,GRAY)
        p+=arrow(910,340,1085,340)+text(1000,295,'z = 1',42,BLUE)
        p+=plot(1130,170,420,320)+text(1375,660,'P(B) ≈ 0.731',67,ORANGE)
    elif n==5:
        p=circle(410,315,110,'Σ',BLUE,90)+text(410,530,'Combine the inputs',46,BLUE)+arrow(545,315,790,315)
        p+=text(665,260,'score z',42,GRAY)+plot(900,140,535,330)+text(1160,590,'Transform the score',46,ORANGE)
        p+=text(864,680,'Sigmoid is one possible activation',46,GRAY)
    elif n==6:
        p=plot(440,55,900,365,'relu')+text(1470,160,'h = max(0, z)',43,ORANGE)
        p+='<g data-relu-point>'+line(1040,420,1040,298.333,BLUE,3,attrs='stroke-dasharray="8 9"')+f'<circle cx="1040" cy="298.333" r="17" fill="{BLUE}"/>'+'</g>'
        return '<div class="d2-live" data-relu>'+svg(p,'Interactive ReLU curve: negative scores become zero; positive scores pass through',540)+'''<div class="d2-controls"><label for="d2-cgcg">CGCG count <input id="d2-cgcg" type="range" min="0" max="12" step="1" value="3"></label><button type="button" data-count="3">Count 3</button><button type="button" data-count="9">Count 9</button></div><p data-relu-readout aria-live="polite">CGCG = 3 → z = 1.0 → h = 1.0</p></div>'''
    elif n==7:
        p=inputs()+''.join(line(278,y,662,350,c,4) for y,c in zip([180,350,520],COLORS))
        p+=circle(720,350,58,'Σ',BLUE,48)+arrow(778,350,920,350)
        p+=plot(960,230,250,200,'relu')+arrow(1265,350,1420,350)+text(1515,370,'h₁',88,ORANGE)
        p+=text(1050,575,'ReLU',43,ORANGE)+text(1515,575,'Feature value',40,GRAY)+text(864,680,'The output becomes an input to the next calculation',43,GRAY)
    elif n==8:
        p=network(focus=True)+text(1260,160,'Own weights',36,GRAY)
        p+=text(1260,255,'0.6, 0.8, −0.2',55,BLUE,attrs='data-unit-weights')
        p+=text(1260,365,'bias −0.4',43,GRAY,attrs='data-unit-bias')
        p+=text(1260,495,'h₁ = ReLU(1.0) = 1.0',45,ORANGE,attrs='data-unit-activation')
        return '<div class="d2-live" data-hidden-layer>'+svg(p,'Three hidden neurons receive the same counts, each through its own weights',600)+'''<div class="d2-controls" role="group" aria-label="Highlight a hidden unit"><button type="button" data-unit="0" aria-pressed="true">h₁</button><button type="button" data-unit="1" aria-pressed="false">h₂</button><button type="button" data-unit="2" aria-pressed="false">h₃</button></div><p data-unit-readout aria-live="polite">h₁: own weights + own bias → ReLU → 1.0</p></div>'''
    elif n==9:
        return '<div class="d2-live" data-forward>'+svg(network(output=True),'Forward pass: counts 2, 1, 3 produce hidden features 1, 1, 0, a logit of 0.3 and probability 0.574',600)+'''<div class="d2-controls"><button type="button" data-forward-next>Trace the prediction</button><button type="button" data-forward-reset>Reset</button><span data-forward-readout aria-live="polite">Start with one sequence’s counts.</span></div></div>'''
    elif n==10:
        p=text(100,120,'Only linear / affine steps',38,GRAY,'start')+text(100,235,'2x + 1 → 3u − 4',62,BLUE,'start')+text(100,330,'= 6x − 1',62,BLUE,'start')
        p+=text(100,455,'Insert a nonlinear activation',38,GRAY,'start')+text(100,565,'3 max(0, 2x + 1) − 4',58,ORANGE,'start')
        for yy,nonlinear,c in [(60,False,BLUE),(390,True,ORANGE)]:
            p+=arrow(1100,yy+220,1600,yy+220,'#b7c7d3',3)+arrow(1330,yy+250,1330,yy,'#b7c7d3',3)
            points=[]
            for i in range(100):
                xx=-2+4*i/99;val=(3*max(0,2*xx+1)-4) if nonlinear else 6*xx-1
                points.append(f'{1100+i*5},{yy+230-(val+13)*9}')
            p+=f'<polyline points="{" ".join(points)}" stroke="{c}" stroke-width="7" fill="none"/>'
        p+=text(864,710,'More linear layers still collapse into one linear score',40,GRAY)
    elif n==11:p=network(output=True,deep=True)
    else:
        p=text(100,145,'A recurring pattern?',64,BLUE,'start')+text(100,250,'Its location? A combination?',57,INK,'start')
        p+=dna(150,440,step=68,highlights=[(0,4,ORANGE),(13,17,ORANGE)])
        p+=text(864,650,'How could the weights learn to notice it?',54,GRAY)
    return svg(p,['','Learning useful features from DNA','DNA words become counts, without their original positions','Choose features or learn intermediate features','Familiar weighted contributions become a score and sigmoid probability','A neuron combines inputs and transforms the score','','One hidden activation becomes a new feature','','','Affine composition stays affine; ReLU introduces a bend','Two hidden layers compose learned features','Discuss useful sequence features'][n])


CSS='''/* DAY 2 SECTION 1 — ILLUSTRATED TEACHING */
.day-two-opening{display:block;padding:80px 96px;border:0;background:#fff;color:#18344b;font-family:"Source Sans 3",sans-serif}
.day-two-opening h1{font-family:inherit;font-size:76px;line-height:1.16;letter-spacing:-1px;margin:0;max-width:1728px;color:#18344b}
.day-two-opening>.slide-top,.day-two-opening>.subtitle,.day-two-opening>.takeaway{display:none}
.day-two-opening>.content{position:absolute;left:96px;top:230px;width:1728px;height:740px;display:block;margin:0;padding:0;overflow:hidden}
.day-two-opening .content svg{display:block;width:1728px;height:720px;font-family:inherit}
.day-two-opening .d2-live{height:740px}
.day-two-opening [data-relu] svg{height:540px}
.day-two-opening [data-hidden-layer] svg,.day-two-opening [data-forward] svg{height:600px}
.day-two-opening .d2-controls{display:flex;align-items:center;justify-content:center;gap:25px;min-height:65px;font-size:31px}
.day-two-opening .d2-controls label{display:flex;align-items:center;gap:25px}
.day-two-opening input[type=range]{width:550px;accent-color:#0072B2}
.day-two-opening button{font:inherit;font-size:30px;border:2px solid #0072B2;padding:10px 25px;color:#0072B2;background:#fff}
.day-two-opening button[aria-pressed=true]{background:#e5f1f8}
.day-two-opening button:disabled{opacity:.5;cursor:default}
.day-two-opening .d2-live>p{font-size:34px;text-align:center;margin:16px 0 0;color:#18344b}
.day-two-opening [data-forward-readout]{font-size:30px;min-width:770px}
.day-two-opening [data-unit-path],.day-two-opening [data-forward-part]{transition:opacity .25s ease}
.day-two-opening .notes{font-family:inherit}
.day-two-opening.active .notes.show,.day-two-opening.active .notes.show *{visibility:visible}
.day-two-opening .notes p{font-size:32px;line-height:1.45}
.day-two-opening .notes .small{font-size:25px}
@media print{.day-two-opening .d2-controls{display:none}.day-two-opening .notes{display:none!important}}
/* END DAY 2 SECTION 1 */
'''


def records():
    story=(ROOT/'Slides/Day_2/story.md').read_text().split('<a id="section-2">')[0]
    blocks=re.findall(r'### S1-(\d+) · (.*?)\n(.*?)(?=\n### |\Z)',story,re.S)
    assert len(blocks)==12
    points=[
        'Trace the DNA ribbon into the network; point out Day 2 on the journey.',
        'Point to repeated TATA occurrences, then the two tally dots. Show the three CGCG windows, which overlap.',
        'Compare the chosen count bars with the fitted intermediate features. We first use counts to build a network; positional DNA comes later.',
        'Follow each count times its weight. Add 1.2 + 0.8 − 0.6 and the bias −0.4 to get 1. Follow that score onto sigmoid.',
        'Point to the sum symbol, then the function curve. The two operations are separate even when drawn as one neuron.',
        'Move the CGCG count from 3 to 9 and back. Watch the score cross zero, while ReLU stays at zero on its negative side.',
        'Follow counts through the weighted sum and ReLU to h₁. The arrow continues: this number is an input for the next stage.',
        'Select h₁, h₂, then h₃. Inputs stay fixed; the highlighted incoming connections belong to the selected neuron.',
        'Press Trace the prediction three times: hidden features, output score, sigmoid probability. Reset to repeat the explanation.',
        'Read the upper composition and its straight line; then compare the lower curve where the intermediate ReLU introduces a kink.',
        'Follow one feature into the next hidden layer. The second layer combines features of the first; depth counts composed learned stages.',
        'Invite several suggestions, then point to the weights as the next unanswered question. There is no expected-answer checklist.',
    ]
    transitions=[
        'Start with what yesterday’s counts retained.', 'Can a model learn useful intermediate features?',
        'Begin with a calculation we already know.', 'Separate the two operations in that familiar predictor.',
        'Use a simpler hidden activation to make its behavior visible.', 'Now use that activation as a feature.',
        'One new feature is useful; several can capture different combinations.', 'Combine the hidden features into the final output.',
        'Why add nonlinear activations between these stages?', 'We can compose another learned feature layer.',
        'What useful sequence features might we want these layers to learn?', 'Next: how do labeled examples change all these weights?',
    ]
    result=[]
    for number,title,body in blocks:
        n=int(number);key=required_match(r'\*\*Proposed slide ID:\*\* `([^`]+)`',body)[1]
        time=required_match(r'\*\*Time:\*\* (.*)',body)[1]
        say=required_match(r'\*\*What I want to say:\*\* (.*?)(?=\n\n|\Z)',body,re.S)[1]
        source='Constructed teaching example, not a fitted model or empirical result. The 21-base Day 1 sequence has 18 overlapping four-base windows; only TATA=2, AATG=1 and CGCG=3 are displayed. Suggested Section 1 pacing totals 25 minutes; not rehearsed.'
        if n in [8,9]:source+=' Hidden weights: h₁=ReLU(0.6×2+0.8×1−0.2×3−0.4)=1; h₂=ReLU(−0.3×2+0.2×1+0.5×3−0.1)=1; h₃=ReLU(0.2×2−0.5×1+0.1×3−0.4)=0. Output weights 1.2, −0.7, 0.5, bias −0.2 give z=0.3 and sigmoid(z)=0.574443. Independent invented weights for illustration; not a fitted biological explanation.'
        if n==10:source+=' Affine example: f(x)=2x+1, g(u)=3u−4; g(f(x))=6x−1. Replacing f by ReLU(f) gives 3max(0,2x+1)−4. These scalar response sketches are not DNA measurements.'
        result.append(dict(day=2,id=key,anchor=key,sectionOne=True,kind='day-two-opening',time=time,title=title,subtitle='',takeaway='',body=figure(n),notes=say,point=points[n-1],transition=transitions[n-1],sourceNote=source))
    return result


def build():
    counts=Counter(SEQ[i:i+4] for i in range(len(SEQ)-3))
    assert [counts[k] for k in ['TATA','AATG','CGCG']]==[2,1,3]
    source=DECK.read_text();m=required_match(r'<script id="day-data" type="application/json">(.*?)</script>',source,re.S)
    old=json.loads(m[1]);later=[x for x in old if not x.get('sectionOne')]
    if not any(x.get('sectionOne') for x in old):
        assert len(later)==15
        later=later[2:]
    assert later and later[0]['anchor'] in ['day-2-slide-3','day-2-s2-section']
    current=records()+later
    payload=json.dumps(current,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
    source=source[:m.start(1)]+payload+source[m.end(1):]
    source=re.sub(r'/\* DAY 2 SECTION 1 — ILLUSTRATED TEACHING \*/.*?/\* END DAY 2 SECTION 1 \*/\n','',source,flags=re.S)
    # Reuse the approved, embedded Source Sans font; no network requests.
    day1=(ROOT/'Slides/Day_1/presentation.html').read_text()
    if '@font-face{font-family:"Source Sans 3"' not in source:
        fonts='\n'.join(x for x in re.findall(r'@font-face\{.*?\}',day1,re.S) if 'Source Sans 3' in x)
        assert fonts
        source=source.replace('</style>',fonts+'\n</style>',1)
    source=source.replace('</style>',CSS+'</style>',1)
    source=source.replace('slide.anchor = `day-${slide.day}-slide-${slide.local}`;', 'slide.anchor = slide.id || slide.anchor || `day-${slide.day}-slide-${slide.local}`;')
    # Keep old scene/edit anchors stable; new opening keys cannot inherit old wording.
    source=source.replace("    readHash() {\n        const localMatch", "    readHash() {\n        const openingAliases = {'#day-2-slide-1':'day-2-s1-welcome','#day-2-slide-2':'day-2-s1-weighted-sum'};\n        const target = openingAliases[location.hash] || location.hash.slice(1);\n        const exact = slides.findIndex(slide => slide.anchor === target);\n        if (exact >= 0) { this.go(exact, false); return; }\n        const localMatch")
    if '<strong>SAY:</strong>' not in source:
        source=source.replace('<p>${slide.notes}</p>', '''${slide.sectionOne ? `<p><strong>SAY:</strong> ${slide.notes}</p><p><strong>POINT:</strong> ${slide.point}</p><p><strong>TRANSITION:</strong> ${slide.transition}</p><p class="small"><strong>Timing:</strong> ${slide.time}</p><p class="small">${slide.sourceNote}</p><p><a href="story.md#section-1">Section 1 story</a></p>` : `<p>${slide.notes}</p>`}''')
    source=source.replace("closest('.d1-demo')", "closest('.d1-demo, .d2-live')")
    source=source.replace("closest('.deck-controls, .d1-demo')", "closest('.deck-controls, .d1-demo, .d2-live')")
    source=source.replace("closest('a, button, input, select, .d1-demo, [contenteditable]')", "closest('a, button, input, select, .d1-demo, .d2-live, [contenteditable]')")
    source=re.sub(r'<script id="day-two-opening-interactions">.*?</script>\n?','',source,flags=re.S)
    js=(ROOT/'tools/day2_section1_interactions.js').read_text()
    source=source.replace('<script id="presentation-controller">','<script id="day-two-opening-interactions">\n'+js+'\n</script>\n<script id="presentation-controller">',1)
    source=source.replace('window.presentation = new SlidePresentation();\n</script>','window.presentation = new SlidePresentation();\nbindDayTwoOpening();\n</script>')
    DECK.write_text(source)
    print(f'Built 12 illustrated opening slides; retained {len(later)} later records ({len(current)} total).')


if __name__=='__main__':build()
