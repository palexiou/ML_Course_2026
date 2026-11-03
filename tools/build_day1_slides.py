"""Build the remaining Day 1 figures from story.md, preserving approved Sections 1–2.

Run after the generated Day 1 notebook rehearsal updates day1-current.json.
The HTML remains the standalone delivery artifact; no server or runtime imports.
"""
import hashlib
import html
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
DECK = ROOT / 'Slides/Day_1/presentation.html'
BLUE, ORANGE, INK, GRAY, PURPLE = '#0072B2', '#D55E00', '#18344b', '#697782', '#7B4FA3'
E = html.escape


def text(x, y, value, size=44, color=INK, anchor='middle', weight=400):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" text-anchor="{anchor}" font-weight="{weight}">{E(str(value))}</text>'


def line(x1, y1, x2, y2, color=GRAY, width=4, dash=''):
    return f'<path d="M{x1} {y1} L{x2} {y2}" fill="none" stroke="{color}" stroke-width="{width}" stroke-dasharray="{dash}"/>'


def box(x, y, w, h, label, color=BLUE, small=''):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="22" fill="{color}" fill-opacity=".08" stroke="{color}" stroke-width="3"/>'
            + text(x+w/2, y+h/2+(12 if not small else -5), label, 40, color)
            + (text(x+w/2, y+h/2+52, small, 30, GRAY) if small else ''))


def svg(contents, label):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1728 720" role="img" aria-label="{E(label, quote=True)}"><title>{E(label)}</title>{contents}</svg>'


def flow(labels, colors=None):
    n=len(labels);w=min(400,1350/n);step=1500/n;parts=''
    for i,label in enumerate(labels):
        x=114+i*step+(step-w)/2
        parts+=box(x,250,w,155,label,(colors or [BLUE,ORANGE,BLUE,ORANGE,BLUE])[i%5])
        if i<n-1: parts+=line(x+w+8,327,x+step-18,327)+text(x+step-18,340,'›',48,GRAY)
    return parts


def forest_diagram():
    p=box(560,15,600,95,'Same training pool',BLUE)
    for i,x in enumerate([140,650,1160]):
        p+=line(860,110,x+215,220)
        p+=text(x+215,205,f'Tree {i+1}',36,GRAY)
        p+=line(x+215,255,x+110,355)+line(x+215,255,x+320,355)
        p+=line(x+320,355,x+255,420)+line(x+320,355,x+385,420)
        for xx,yy in [(x+215,255),(x+110,355),(x+320,355),(x+255,420),(x+385,420)]:
            p+=f'<circle cx="{xx}" cy="{yy}" r="14" fill="{BLUE if i%2==0 else ORANGE}"/>'
        p+=line(x+215,450,860,560,GRAY,3)
    return p+box(590,560,540,110,'Average probabilities',ORANGE)


def words(items, colors=None, y=345, size=62):
    return ''.join(text(864+(i-(len(items)-1)/2)*(1450/max(len(items),1)),y,v,size,(colors or [INK]*len(items))[i]) for i,v in enumerate(items))


def bars(labels, values, signed=False, value_format='.2f', colors=None):
    n=len(labels);h=min(82,460/max(n,1));zero=950 if signed else 450;scale=500/max(max(abs(v) for v in values),1e-6);parts=line(zero,85,zero,85+n*h,GRAY,2)
    for i,(label,v) in enumerate(zip(labels,values)):
        y=105+i*h;end=zero+v*scale;color=colors[i] if colors else (ORANGE if v>=0 else BLUE)
        parts+=text(320,y+28,label,40,INK,'end')
        parts+=f'<rect x="{min(zero,end)}" y="{y}" width="{max(abs(v)*scale,2)}" height="40" rx="5" fill="{color}"/>'
        parts+=text(end+(18 if v>=0 else -18),y+29,format(v,value_format),34,color,'start' if v>=0 else 'end')
    return parts


def matrix(focus='',suffix=''):
    parts=text(900,85,'Predicted',36,GRAY)+text(720,150,'A / 0',38,BLUE)+text(1040,150,'B / 1',38,ORANGE)
    parts+=text(285,350,'Observed',36,GRAY)+text(450,280,'A / 0',38,BLUE)+text(450,470,'B / 1',38,ORANGE)
    for idx,(x,y,n,label) in enumerate([(560,195,40,'TN'),(880,195,10,'FP'),(560,385,20,'FN'),(880,385,30,'TP')]):
        on=not focus or label in focus.split(',');col=ORANGE if idx in [1,3] else BLUE
        parts+=f'<g opacity="{1 if on else .22}"><rect x="{x}" y="{y}" width="290" height="165" rx="18" fill="{col}" fill-opacity=".10" stroke="{col}" stroke-width="3"/>'+text(x+145,y+77,n,68,col)+text(x+145,y+144,label,33,GRAY)+'</g>'
    return parts+text(864,650,suffix,48,INK)


def tree(stage='all', interactive=False):
    parts=line(864,145,440,310)+line(864,145,1200,310)+text(570,205,'No',30,GRAY)+text(1110,205,'Yes',30,GRAY)
    parts+=box(600,45,528,100,'TATA ≥ 2?')
    if stage!='root':
        parts+=box(180,310,480,110,'P(B) = 0.20',BLUE,'1 B / 4 A')
        parts+=box(960,270,500,100,'CGCG < 2?')
        parts+=line(1210,370,1000,510)+line(1210,370,1490,510)+text(1020,425,'Yes',30,GRAY)+text(1420,425,'No',30,GRAY)
        parts+=box(780,510,420,120,'P(B) = 0.80',ORANGE,'4 B / 1 A')+box(1270,510,420,120,'P(B) = 0.25',BLUE,'1 B / 3 A')
    else:parts+=text(440,345,'…',70,GRAY)+text(1200,345,'…',70,GRAY)
    return parts


TOY_ROWS=[(0,0,0,0),(0,0,1,0),(1,0,2,0),(1,1,3,0),(1,0,4,1),(2,0,0,1),(2,0,1,1),(3,1,0,1),(3,1,1,1),(4,0,1,0),(2,1,2,1),(2,1,3,0),(3,1,3,0),(4,1,4,0)]


def separation():
    p=line(350,560,1450,560)+line(350,560,350,70)
    for i in range(5):p+=text(450+i*210,610,i,34,GRAY)+text(300,540-i*105,i,34,GRAY)
    for a,_,c,y in TOY_ROWS:
        x=450+a*210;yy=530-c*105
        p+=(f'<circle cx="{x}" cy="{yy}" r="17" fill="{ORANGE}"/>' if y else f'<rect x="{x-15}" y="{yy-15}" width="30" height="30" fill="{BLUE}"/>')
    p+=line(765,80,765,560,ORANGE,4,'12 8')+text(900,685,'TATA count',38)+text(180,315,'CGCG',36)
    p+=text(550,45,'1 B / 4 A',36,BLUE)+text(1140,45,'5 B / 4 A',36,ORANGE)
    return p


def motif(ppm):
    p='';bases='ACGT';cols=[BLUE,ORANGE,PURPLE,GRAY]
    for i,row in enumerate(ppm):
        for j,v in enumerate(row):
            x=230+i*88;y=125+j*110
            p+=f'<rect x="{x}" y="{y}" width="80" height="100" rx="5" fill="{cols[j]}" fill-opacity="{.08+.82*v}"/>'+text(x+40,y+60,f'{v:.2f}',28,INK)
        p+=text(270+i*88,610,i+1,26,GRAY)
    for j,b in enumerate(bases):p+=text(150,185+j*110,b,44,cols[j])
    return p


def practical(section, labels):
    steps=''.join(f'<p>{E(label)}</p>' for label in labels)
    url='https://colab.research.google.com/github/palexiou/ML_Course_2026/blob/main/notebooks/01_simple_signal.ipynb'
    return f'<div class="lesson-practical">{steps}<a href="{url}">Open Day 1 in Colab ↗</a></div>'


def specs():
    story=(ROOT/'Slides/Day_1/story.md').read_text();result=[]
    pattern=r'### S([3-6])-(\d{2}) · ([^\n]+)\n\n\*\*(?:Proposed slide ID|Slide ID):\*\* `([^`]+)` · \*\*Time:\*\* ([^\n]+)\n\n\*\*What is on slide:\*\* (.*?)\n\n\*\*What I want to say:\*\* (.*?)\n\n\*\*Point / transition:\*\* (.*?)(?=\n\n|\n###|\Z)'
    for m in re.finditer(pattern,story,re.S):
        sec,num,title,key,time,visible,say,point=m.groups()
        result.append(dict(sectionNumber=int(sec),number=int(num),title=title,id=key,time=time,visible=visible,notes=say,point=point))
    assert len(result)==68,len(result)
    return result


def figure(s, data):
    sec,n=s['sectionNumber'],s['number'];p='';special=None
    if sec==3:
        if n==1:p=flow(['k-mer counts','Predictor','P(B), 1 − P(B)'])
        elif n==2:p=flow(['Counts','Weighted sum','Probability'])
        elif n==3:p=words(['2 × 0.6','1 × 0.8','3 × (−0.2)'],[ORANGE,BLUE,PURPLE],250,60)+words(['+1.2','+0.8','−0.6'],[ORANGE,BLUE,PURPLE],435,82)
        elif n==4:p=text(864,250,'1.2 + 0.8 − 0.6 − 0.4',80)+text(864,450,'z = 1.0',110,ORANGE)
        elif n==5:special='<div class="lesson-live" data-live="sigmoid"><div data-live-plot></div><label>Score z <input type="range" min="-6" max="6" step="0.1" value="1" aria-label="Logistic score"></label><p data-live-readout></p></div>'
        elif n==6:p=text(864,200,'P(B) = 0.731',90,ORANGE)+line(240,380,1490,380)+line(865,340,865,420,BLUE,6)+f'<circle cx="1154" cy="380" r="18" fill="{ORANGE}"/>'+text(865,480,'Cutoff 0.5',42)+text(240,480,'A',52,BLUE)+text(1490,480,'B',52,ORANGE)
        elif n==7:p=flow(['New counts','Fitted model','Probability'])+text(864,530,'Parameters stay fixed',46,GRAY)
        elif n==8:p=flow(['Training counts','Probabilities','Compare labels'])+text(864,535,'Feedback adjusts the parameters',48,ORANGE)
        elif n==9:p=text(864,200,'Observed B: loss = −log P(B)',60)+words(['P(B) = 0.9','P(B) = 0.1'],[BLUE,ORANGE],365,64)+words(['Loss ≈ 0.105','Loss ≈ 2.303'],[BLUE,ORANGE],510,64)
        elif n==10:
            pts=' '.join(f'{260+i*12},{560-(-__import__("math").log(max(.01,i/100)))*92}' for i in range(1,100))
            p=line(240,560,1500,560)+line(240,560,240,80)+f'<polyline points="{pts}" fill="none" stroke="{ORANGE}" stroke-width="7"/>'+text(900,650,'P(B) when observed class is B',42)+text(140,180,'Loss',42)
        elif n==11:p=flow(['0.105','2.303','Mean ≈ 1.204'])+text(864,540,'Average over the training examples',48,GRAY)
        elif n==12:special='<div class="lesson-live" data-live="gradient" data-step="0"><div data-live-plot></div><div class="live-buttons"><button data-step>Step downhill</button><button data-reset>Reset</button></div><p data-live-readout></p></div>'
        elif n==13:p=flow(['Train + labels','Fit','Fitted parameters'])+text(864,535,'New counts → fixed model → probability',49,GRAY)
        elif n==14:special=practical(sec,['Inspect counts → fit on TRAIN','Reproduce the score, probability and loss'])
        elif n==15:p=flow(['Validation rows','Fixed model','Compare labels'])+text(864,540,'Test: final frozen comparison only',42,GRAY)
        else:p=flow(['One probability','Many predictions','Which mistakes matter?'])
    elif sec==4:
        if n==1:return '<div class="s2-title-rule"></div>'
        if n==2:
            p=text(430,130,'Observed',40,GRAY)+text(860,130,'P(B)',40,GRAY)+text(1290,130,'Predicted',40,GRAY)
            for i,(y,q,call) in enumerate([('B / 1','0.95','B / 1'),('A / 0','0.85','B / 1'),('B / 1','0.35','A / 0')]):p+=text(430,270+i*150,y,55)+text(860,270+i*150,q,55,ORANGE)+text(1290,270+i*150,call,55)
        elif n in [3,4,6,7]:p=matrix({3:'',4:'TP,TN',6:'TP,FP',7:'TP,FN'}[n],{3:'100 examples',4:'Accuracy = 70 / 100 = 70%',6:'Precision = 30 / 40 = 75%',7:'Recall = 30 / 50 = 60%'}[n])
        elif n==5:
            for i in range(100):p+=f'<circle cx="{360+i%20*54}" cy="{150+i//20*65}" r="17" fill="{ORANGE if i>=95 else BLUE}"/>'
            p+=text(864,585,'Always A: 95% accuracy, no B recovered',58)
        elif n==8:p=flow(['False positive','Unnecessary follow-up'])+text(864,570,'False negative → missed candidate',58,ORANGE)
        elif n==9:p=words(['Precision 0.75','Recall 0.60'],[BLUE,ORANGE],220,62)+text(864,430,'F1 = 2PR / (P + R) ≈ 0.667',70)+text(864,590,'True negatives are outside this summary',40,GRAY)
        elif n==10:special='<div class="lesson-live" data-live="threshold"><div data-live-plot></div><label>Cutoff <input type="range" min="0" max="1" step="0.01" value="0.5" aria-label="Decision threshold"></label><p data-live-readout></p></div>'
        elif n==11:
            for i,(score,b,a) in enumerate([(0.95,8,2),(.85,8,2),(.75,7,3),(.65,7,3),(.45,6,4),(.35,5,5),(.25,4,6),(.15,3,7),(.08,1,9),(.02,1,9)]):
                for j in range(10):p+=f'<circle cx="{190+i*145}" cy="{130+j*42}" r="13" fill="{ORANGE if j<b else BLUE}"/>'
            p+=text(850,640,'Higher P(B) ← ranking → lower P(B)',50)
        elif n in [12,13,14]:special=f'<div class="lesson-live" data-live="curve" data-curve="{"pr" if n==14 else "roc"}" data-area="{1 if n==13 else 0}"><div data-live-plot></div><label>Cutoff <input type="range" min="0" max="1" step="0.01" value="0.5" aria-label="Curve decision threshold"></label><p data-live-readout></p></div>'
        elif n==15:special=practical(sec,['Read TP, FP, FN and TN','Calculate precision / recall → change the cutoff'])
        else:special='<div class="lesson-prompt"><p>If you could follow up only a few predictions,<br>what would matter to you?</p></div>'
    elif sec==5:
        if n==1:return '<div class="s2-title-rule"></div>'
        if n==2:p=flow(['Counts 2, 1, 3','Tree','P(B)'])
        elif n==3:p=tree('root')
        elif n in [4,9]:p=tree()
        elif n==5:p=words(['A','A','B','A'],[BLUE,BLUE,ORANGE,BLUE],240,100)+text(864,440,'P(B) = 1 / 4 = 0.25',86)+text(864,590,'Training class proportions in this leaf',42,GRAY)
        elif n==6:special='<div class="lesson-live tree-live" data-live="tree"><div data-live-plot></div><div class="live-buttons"><label>TATA <input data-tree-a type="number" min="0" max="20" value="2"></label><label>CGCG <input data-tree-b type="number" min="0" max="20" value="3"></label><button data-reset>Reset</button></div><p data-live-readout></p></div>'
        elif n==7:p=separation()
        elif n==8:p=words(['AATG ≥ 1?','TATA ≥ 2?'],[BLUE,ORANGE],160,62)+words(['3B/4A · 3B/4A','1B/4A · 5B/4A'],[BLUE,ORANGE],345,48)+words(['Same mixture','Less mixed children'],[BLUE,ORANGE],530,48)
        elif n==10:
            p=box(550,30,620,100,'Mixed training group')
            p+=line(860,130,525,245)+line(860,130,1185,245)
            for x in [525,1185]:p+=f'<circle cx="{x}" cy="245" r="25" fill="{BLUE}"/>'
            for i,x in enumerate([360,690,1020,1350]):
                p+=line(525 if i<2 else 1185,270,x,430)+box(x-125,430,250,130,'1 example',ORANGE if i==2 else BLUE)
                p+=f'<circle cx="{x}" cy="370" r="18" fill="{ORANGE if i==2 else BLUE}"/>'
            p+=text(864,645,'A pure leaf can rest on one accidental detail',50,GRAY)
        elif n==11:
            p=tree('root')+line(180,265,1580,265,ORANGE,5)+text(864,625,'Stop at a depth limit; retain enough rows per leaf',48,GRAY)
            p+=text(864,240,'Maximum depth',42,ORANGE)+box(240,390,500,100,'Keep a larger leaf',BLUE)+box(1010,390,500,100,'Minimum leaf size',ORANGE)
        elif n==12:
            for x,label,c in [(450,'TATA split',BLUE),(1260,'CGCG split',ORANGE)]:
                p+=box(x-230,120,460,100,label,c)+line(x,220,x-180,400,c)+line(x,220,x+180,400,c)
                p+=f'<circle cx="{x-180}" cy="400" r="25" fill="{c}"/><circle cx="{x+180}" cy="400" r="25" fill="{c}"/>'
            p+=text(864,590,'Small training changes can alter early questions',48,GRAY)
        elif n==13:p=forest_diagram()
        elif n==14:p=text(864,140,'Training pool: 1  2  3  4  5  6',58)+text(864,330,'Bag 1: 1  1  3  4  4  6',70,BLUE)+text(864,510,'Bag 2: 2  2  3  5  6  6',70,ORANGE)
        elif n==15:
            p=text(180,220,'Node 1',40,GRAY)+text(180,410,'Node 2',40,GRAY)
            p+=''.join(text(480+i*300,220,label,58,[ORANGE,GRAY,BLUE,GRAY][i])+text(480+i*300,410,label,58,[GRAY,ORANGE,GRAY,BLUE][i]) for i,label in enumerate(['TATA','CGCG','AATG','ACTG']))
            p+=text(864,600,'A fresh candidate subset; then select a useful split',46,GRAY)
        elif n==16:p=words(['0.25','0.60','0.80'],[BLUE,ORANGE,BLUE],230,90)+text(864,435,'Average P(B) = 0.55',90)+text(864,595,'Apply the separate 0.5 decision cutoff',43,GRAY)
        elif n==17:p=line(230,355,1500,355)+''.join(f'<circle cx="{230+1270*v}" cy="355" r="20" fill="{BLUE}" opacity=".5"/>' for v in [.25,.6,.8])+line(230+1270*.55,300,230+1270*.55,410,ORANGE,9)+text(864,555,'Averaging can reduce instability',58)
        elif n==18:
            p=box(80,265,410,150,'Same counts')+box(680,100,510,130,'Logistic regression',BLUE)+box(680,440,510,130,'Random forest',ORANGE)+box(1360,265,320,150,'Compare',BLUE)
            p+=line(490,340,680,165)+line(490,340,680,505)+line(1190,165,1360,340)+line(1190,505,1360,340)+text(864,680,'Same validation rows · same metrics · cutoff 0.5',43,GRAY)
        elif n==19:special=practical(sec,['Run the paired workflow once','Read the actual comparison → inspect a disagreement'])
        else:
            rows=data['comparison'];p=text(420,140,'Validation ROC-AUC',43,GRAY)+text(1230,140,'Validation AP',43,GRAY)
            for i,r in enumerate(rows):p+=text(310,300+i*190,'Logistic' if i==0 else 'Forest',43,INK)+text(680,300+i*190,f"{r['roc_auc']:.3f}",82,BLUE if i==0 else ORANGE)+text(1230,300+i*190,f"{r['average_precision']:.3f}",82,BLUE if i==0 else ORANGE)
            p+=text(864,650,'Which sequence clues are the models using?',46,GRAY)
    elif sec==6:
        if n==1:return '<div class="s2-title-rule"></div>'
        if n==2:p=box(200,220,580,180,'One prediction',BLUE)+box(950,220,580,180,'The fitted model',ORANGE)+words(['Local contributions','Global summaries'],[BLUE,ORANGE],540,49)
        elif n==3:p=bars(['TATA','AATG','CGCG'],[1.2,.8,-.6],True,colors=[ORANGE,BLUE,PURPLE])+text(864,650,'Count × coefficient → score contribution',46)
        elif n==4:p=text(864,230,'−0.4 + 1.2 + 0.8 − 0.6 = 1',78)+text(864,440,'P(B) ≈ 0.731',98,ORANGE)
        elif n==5:
            rows=data['coefficients'];p=bars([r['kmer'] for r in rows],[r['coefficient'] for r in rows],True)+text(864,680,'Signed coefficients · actual fitted logistic model',35,GRAY)
        elif n==6:p=flow(['Same coefficient','Count = 0','Contribution = 0'])+text(864,560,'A coefficient needs the feature value',53,GRAY)
        elif n==7:
            rows=data['forest_importance'];p=bars([r['kmer'] for r in rows],[r['importance'] for r in rows],False,'.3f')+text(864,680,'Global impurity importance · no positive/negative direction',35,GRAY)
        elif n==8:p=flow(['Feature use','Shared credit','No causal conclusion'])
        elif n==9:p=motif(data['motif_ppm'])
        elif n==10:
            r=data['forest_importance'][0];word=r['kmer'];ppm=data['motif_ppm'];best=max(range(12),key=lambda start:__import__('math').prod(ppm[start+j]['ACGT'.index(b)] for j,b in enumerate(word)))
            for j,b in enumerate(word):
                v=ppm[best+j]['ACGT'.index(b)];p+=box(260+j*325,80,265,150,b,ORANGE,f'p = {v:.2f}')
                if j<3:p+=text(550+j*325,175,'×',42,GRAY)
            p+=text(864,345,f'One internal window: positions {best+1}–{best+4}',43,GRAY)
            p+=text(864,465,'Average the word probabilities over 12 starts',48)
            p+=text(864,620,f"Enrichment vs 1/256: {r['motif_vs_background_enrichment']:.2f}×",65,BLUE)
        elif n==11:
            rows=data['forest_importance'][:3];p=text(450,130,'k-mer',40,GRAY)+text(870,130,'Forest importance',40,GRAY)+text(1310,130,'PPM enrichment',40,GRAY)
            for i,r in enumerate(rows):p+=text(450,280+i*145,r['kmer'],62)+text(870,280+i*145,f"{r['importance']:.4f}",55,ORANGE)+text(1310,280+i*145,f"{r['motif_vs_background_enrichment']:.2f}×",55,BLUE)
        elif n==12:p=text(864,180,'… A C G T A C …',80)+text(650,365,'ACGT',80,BLUE)+text(1000,500,'CGTA',80,ORANGE)+text(864,650,'Shared bases → correlated features',48,GRAY)
        elif n==13:
            p=text(480,120,'Training',48,GRAY)+text(1240,120,'Validation',48,GRAY)+line(860,150,860,510,GRAY,3)
            p+=box(220,240,520,140,'Family A · row 1',BLUE)+box(980,240,520,140,'Family A · row 2',BLUE)
            p+=text(864,620,'A new ID need not mean a new family',53,ORANGE)
        elif n==14:special=practical(sec,['Select one validation row → verify the full sum','Explain contributions → compare global features'])
        elif n==15:special='<div class="lesson-prompt"><p>Which clue mattered here,<br>and what would you still want to check?</p></div>'
        else:p=flow(['DNA','Counts','Prediction','Evaluation','Explanation'])+text(864,575,'Tomorrow: retain position and learn features',52,ORANGE)
    if special:return special
    if not p:raise ValueError(s)
    return svg(p,s['title'])


CSS='''/* === SECTIONS 3–6: ONE TITLE, ONE VISUAL === */
.section-teaching h1{font-size:70px;line-height:1.2;max-width:1728px}
.section-teaching>.content{top:240px;height:720px}
.section-teaching .lesson-live{height:720px;width:1728px;overflow:hidden}
.section-teaching [data-live-plot]{height:540px;width:1728px}
.section-teaching [data-live-plot]>svg{height:540px;width:1728px;display:block}
.section-teaching .lesson-live>label{display:flex;align-items:center;justify-content:center;gap:30px;font-size:34px;height:55px}
.section-teaching input[type=range]{width:720px;accent-color:#D55E00}
.section-teaching [data-live-readout]{font-size:34px;text-align:center;margin:20px 0 0;line-height:1.25;color:#18344b;min-height:45px}
.section-teaching .live-buttons{display:flex;align-items:center;justify-content:center;gap:28px;height:65px}
.section-teaching button{font:inherit;font-size:30px;border:2px solid #0072B2;border-radius:12px;padding:10px 24px;background:#fff;color:#0072B2}
.section-teaching button:disabled{opacity:.4}
.section-teaching .live-buttons label{font-size:32px;display:flex;align-items:center;gap:15px}
.section-teaching input[type=number]{font:inherit;width:95px;border:2px solid #becbd4;padding:8px;border-radius:8px}
.section-teaching .lesson-practical{padding:100px 65px}
.section-teaching .lesson-practical p{font-size:54px;line-height:1.35;margin:0 0 50px;color:#18344b}
.section-teaching .lesson-practical a{display:inline-block;font-size:42px;color:#0072B2;margin-top:20px}
.section-teaching .lesson-prompt{padding:120px 70px}
.section-teaching .lesson-prompt p{font-size:64px;line-height:1.45;margin:0;color:#0072B2}
.section-teaching:has(.s2-title-rule) h1{font-size:112px;max-width:1550px}
@media print{.section-teaching button,.section-teaching input{display:none!important}}
'''


def build():
    data=json.loads((ROOT/'instructor/verification/day1-current.json').read_text())
    for path,sha in data['source_sha256'].items():
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==sha, f'Rehearse updated notebook first: {path}'
    source=DECK.read_text();m=re.search(r'<script id="day-data" type="application/json">(.*?)</script>',source,re.S)
    assert m is not None
    current=json.loads(m[1]);records=current[:42]
    assert records[-1]['id']=='day-1-dna-ready-for-model'
    def br(key,time,nextsec):
        return dict(day=1,id=key,kind='section-two section-teaching',sectionTeaching=True,sectionNumber=nextsec,time=time,title='Break',body=svg(text(864,340,'10 minutes',120,BLUE),'Ten-minute break'),notes=f'Take the full {time} break. Return for Section {nextsec}.',point='The break duration.',transition=f'Resume with Section {nextsec}.',sourceNote='Break time is separate from teaching allocations.')
    records.append(br('day-1-break-1','50–60',3))
    for s in specs():
        if s['sectionNumber']==5 and s['number']==1:records.append(br('day-1-break-2','115–125',5))
        body=figure(s,data);sec=s['sectionNumber']
        s.update(day=1,kind='section-two section-teaching',sectionTeaching=True,body=body,transition=s['point'],sourceNote=f'Section {sec} story and source notes govern this slide. Teaching constructions and current paired-run values are distinguished there. Validation only; no test-guided decisions.')
        if sec==3 and s['number'] in [9,10,11,12]:
            s['sourceNote']+=' The plotted loss is the data-loss term. The real LogisticRegression(max_iter=2000) fit uses L-BFGS and its default L2 penalty; it does not execute the toy one-weight gradient-descent steps. Regularization/complexity is not an extra Section 3 teaching beat.'
        if sec in [5,6] and s['number'] in ([20] if sec==5 else [5,7,10,11]):
            s['sourceNote']+=' Empirical values: generated Day 1 notebook, local seed-2026 primary PPM run, 2026-11-03; 240 validation rows, threshold 0.5; instructor/verification/day1-current.json. No tuning followed.'
        records.append(s)
    assert len(records)==112
    payload=json.dumps(records,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
    source=source[:m.start(1)]+payload+source[m.end(1):]
    source=re.sub(r'/\* === SECTIONS 3–6: ONE TITLE, ONE VISUAL === \*/.*?(?=</style>)','',source,flags=re.S)
    source=source.replace('</style>',CSS+'</style>',1)
    # Reuse the established controller; new records have fresh edit keys.
    source=source.replace('${slide.sectionTwo ?','${slide.sectionTwo || slide.sectionTeaching ?')
    source=source.replace('Section 2 total 25 minutes (not rehearsed).','Section ${slide.sectionNumber || 2} total ${[0,25,25,30,25,30,25][slide.sectionNumber || 2]} minutes (not rehearsed).')
    source=source.replace('href="story.md#section-2">Section 2 story and scientific notes','href="story.md#section-${slide.sectionNumber || 2}">Section ${slide.sectionNumber || 2} story and scientific notes')
    source=source.replace("closest('.d1-demo')", "closest('.d1-demo, .lesson-live')")
    source=source.replace("closest('.deck-controls, .d1-demo')", "closest('.deck-controls, .d1-demo, .lesson-live')")
    source=source.replace("closest('a, button, input, select, .d1-demo, [contenteditable]')", "closest('a, button, input, select, .d1-demo, .lesson-live, [contenteditable]')")
    js=(ROOT/'tools/day1_interactions.js').read_text()
    source=re.sub(r'<script id="day-one-interactions">.*?</script>',lambda _: '<script id="day-one-interactions">\n'+js+'\n</script>',source,flags=re.S)
    marker='        const sectionTwoAliases = '
    alias={'23':'day-1-break-1','24':'day-1-lr-section','25':'day-1-lr-supervised-fit','26':'day-1-lr-validation','27':'day-1-dna-test-boundary','28':'day-1-lr-signed-contributions','29':'day-1-lr-sigmoid','30':'day-1-lr-threshold','31':'day-1-lr-optimization','32':'day-1-metrics-confusion','33':'day-1-metrics-accuracy','34':'day-1-metrics-precision','35':'day-1-metrics-recall','36':'day-1-metrics-f1','37':'day-1-metrics-roc','38':'day-1-metrics-pr','39':'day-1-metrics-threshold','40':'day-1-lr-notebook-checkpoint','41':'day-1-explain-notebook','42':'day-1-break-2','43':'day-1-trees-root','44':'day-1-trees-paths','45':'day-1-trees-overfit','46':'day-1-trees-average','47':'day-1-trees-fair-comparison','48':'day-1-trees-handoff','49':'day-1-explain-forest-importance','50':'day-1-explain-probability-pattern','51':'day-1-explain-discussion','61':'day-1-explain-tomorrow','62':'day-1-explain-tomorrow'}
    alias.update({str(i):'day-1-explain-shortcut' for i in range(52,61)})
    source=re.sub(r'        /\* Legacy later-slide aliases \*/.*?/\* End later aliases \*/\n','',source,flags=re.S)
    inject='        /* Legacy later-slide aliases */\n        const laterAliases='+json.dumps(alias)+';\n        const later=location.hash.match(/^#day-1-slide-(\\d+)$/);\n        if(later && laterAliases[later[1]]) { this.go(slides.findIndex(s=>s.id===laterAliases[later[1]]),false); return; }\n        /* End later aliases */\n'
    source=source.replace(marker,inject+marker)
    DECK.write_text(source)
    print(f'Built {len(records)} Day 1 slides; preserved 42 approved opening records.')


if __name__=='__main__':build()
