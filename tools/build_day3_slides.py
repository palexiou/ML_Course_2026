"""Build Day 3's reviewed story as a self-contained illustrated HTML deck.

Native figures use source-bound local validation evidence. Test panels start empty;
only an instructor-imported result file may fill them. No scientific code runs here.
"""
import hashlib
import html
import json
import math
from pathlib import Path
import re

from build_day2_section1 import BLUE, ORANGE, INK, GRAY, PURPLE, text, line, arrow, circle, svg, dna, helix, required_match

ROOT = Path(__file__).resolve().parents[1]
DECK = ROOT / 'Slides/Day_3/presentation.html'
E = html.escape
MODEL = 'InstaDeepAI/nucleotide-transformer-v2-50m-multi-species'
REVISION = '81b29e5786726d891dbf929404ef20adca5b36f1'
NOTEBOOK = 'https://colab.research.google.com/github/palexiou/ML_Course_2026/blob/main/notebooks/03_representations.ipynb'
METHODS = [('logistic_regression','Counts + logistic',BLUE),('random_forest','Counts + forest',ORANGE),('cnn','CNN',PURPLE),('foundation','Frozen NT + logistic',GRAY)]


def strip(x,y,values=None,w=450,h=75):
    values = values if values is not None else [.2,-.5,.8,.4,-.2,.6,-.1,.4]
    p=''
    for i,v in enumerate(values):
        c=BLUE if v>=0 else ORANGE
        p+=f'<rect x="{x+i*w/len(values):.2f}" y="{y}" width="{w/len(values)-4:.2f}" height="{h}" rx="3" fill="{c}" fill-opacity="{.15+.75*min(1,abs(v)):.2f}"/>'
    return p


def lock(x,y,color=BLUE,opened=False):
    return f'<path d="M{x-24} {y} v-24 a24 24 0 0 1 48 0 v{8 if opened else 24}" fill="none" stroke="{color}" stroke-width="7"/><rect x="{x-37}" y="{y}" width="74" height="59" rx="7" fill="white" stroke="{color}" stroke-width="6"/>'+circle(x,y+27,5,'',color,0)


def tiles(words,y=230,x=95,step=305,size=46):
    p=''
    for i,word in enumerate(words):
        xx=x+i*step;c=ORANGE if word in {'ATG','[MASK]'} else BLUE
        p+=line(xx-50,y+35,xx+step-80,y+35,c,5)+text(xx+(step-130)/2,y,word,size,c,weight=600)
    return p


def statement(a,b='',color=BLUE):
    return svg(text(864,270,a,72,color)+text(864,410,b,55,GRAY),' '.join([a,b]))


def pair(a,b,c='',d=''):
    return svg(text(405,160,a,52,BLUE)+text(1310,160,b,52,ORANGE)+line(864,80,864,565,'#dce5eb',3)+text(405,390,c,48,INK)+text(1310,390,d,48,INK),a+'; '+b)


def list_figure(labels,colors=None):
    p='';colors=colors or [BLUE,ORANGE,PURPLE,GRAY,BLUE]
    step=min(128,560/max(1,len(labels)-1))
    for i,label in enumerate(labels):
        y=70+i*step
        p+=circle(160,y,27,str(i+1),colors[i%len(colors)],28)+text(225,y+14,label,45,INK,'start')
    return svg(p,'; '.join(labels))


def network(x,y,w=360,h=230,color=BLUE):
    ys=[[y+40,y+h-40],[y,y+h/2,y+h],[y+h/2]];xs=[x,x+w*.52,x+w]
    p=''
    for k in range(2):
        for a in ys[k]:
            for b in ys[k+1]:p+=line(xs[k]+18,a,xs[k+1]-18,b,'#aebfcd',3)
    for xx,yy in zip(xs,ys):
        for v in yy:p+=circle(xx,v,18,'',color,0)
    return p


def envelope():
    return '<rect x="464" y="100" width="800" height="430" rx="20" fill="#f6f9fc" stroke="'+BLUE+'" stroke-width="7"/><path d="M464 110 L864 370 L1264 110 M464 525 L720 335 M1264 525 L1008 335" fill="none" stroke="'+BLUE+'" stroke-width="5"/>'+lock(864,310,ORANGE)


def prompt(a,b=''):
    return '<div class="d3-prompt"><p>'+E(a)+'</p>'+('<p class="secondary">'+E(b)+'</p>' if b else '')+'</div>'


def notebook(label,code='',route='Stage 04 · same notebook, same runtime'):
    return '<div class="d3-notebook"><p>'+E(label)+'</p><a href="'+NOTEBOOK+'">Open notebook in Colab ↗</a>'+('<pre>'+E(code)+'</pre>' if code else '')+'<p class="route">'+E(route)+'</p></div>'


def live(p,mode,controls,caption=''):
    return '<div class="d2-live d3-live" data-d3="'+mode+'">'+svg(p,mode.replace('-',' '),560)+'<div class="d3-controls">'+controls+'</div><p data-readout aria-live="polite">'+E(caption)+'</p></div>'


def button(label,attr='data-next'):
    return '<button type="button" '+attr+'>'+E(label)+'</button>'


def critter(x,y,kind,color):
    # Deliberately simple native line drawings, rather than image dependencies.
    if kind=='Bird':
        return f'<ellipse cx="{x}" cy="{y}" rx="70" ry="45" fill="{color}" fill-opacity=".1" stroke="{color}" stroke-width="5"/><path d="M{x+65} {y-5} l45 12 l-45 12 M{x-65} {y} l-40 -30 l5 55 Z M{x-25} {y+43} v35 m40 -35 v35" fill="none" stroke="{color}" stroke-width="5"/>'+circle(x+30,y-10,4,'',color,0)
    ear=f'M{x-65} {y-45} l-20 -65 l65 40 M{x+65} {y-45} l20 -65 l-65 40' if kind=='Cat' else f'M{x-65} {y-40} q-80 -25 -50 65 M{x+65} {y-40} q80 -25 50 65'
    return f'<path d="{ear}" fill="none" stroke="{color}" stroke-width="7"/><ellipse cx="{x}" cy="{y}" rx="76" ry="67" fill="white" stroke="{color}" stroke-width="5"/>'+circle(x-25,y-10,5,'',color,0)+circle(x+25,y-10,5,'',color,0)+text(x,y+30,'⌣',40,color)


def s1(n,data):
    if n==1:
        p=helix(80,235,420,85)
        for i,(label,color) in enumerate([('Count',BLUE),('Train detectors',ORANGE),('Borrow features',PURPLE)]):
            x=780+i*340;p+=arrow(540,235,x,235,color)+text(x,380,label,42,color)
            for j,v in enumerate([50,110,70]):p+=line(x-65+j*65,230,x-65+j*65,230-v,color,12)
        p+=text(864,560,'Day 3',56,PURPLE)+text(864,660,'1 · Define     2 · Learn     3 · Reuse     4 · Audit',39,GRAY)
        return svg(p,'Day 3 moves from designed counts and trained detectors to borrowed representations')
    if n==2:
        p=''
        for y,label,c in [(170,'Count words',BLUE),(470,'Learn filters',ORANGE)]:
            p+=text(160,y-65,label,39,c,'start')+dna(130,y+20,'ACGTAC',55,size=36)+arrow(540,y,680,y)+network(760,y-70,290,140,c)+arrow(1110,y,1300,y)+text(1450,y+20,'P(B)',65,c)
        p+=text(864,690,'Both fitted using our training labels',46,GRAY)
        return svg(p,'Recap: counts and CNN weights are fitted on the training task')
    if n==3:
        p=''
        for i,(animal,c) in enumerate([('Dog',BLUE),('Cat',ORANGE),('Bird',PURPLE)]):
            y=120+i*190;p+=critter(160,y,animal,c)+text(310,y+15,animal,42,c,'start')+arrow(460,y,600,y)+strip(640,y-30,w=330,h=60,values=[math.sin(i+j) for j in range(6)])
            cx,cy=[(1190,170),(1400,410),(1530,155)][i]
            for j in range(7):p+=circle(cx+48*math.sin(j*2),cy+40*math.cos(j*3),8,'',c,0)
            p+=text(cx,cy+95,animal,34,c)
        p+=arrow(1060,540,1640,540,GRAY,3)+arrow(1060,540,1060,55,GRAY,3)+text(1360,620,'Learned relationships',42,BLUE)
        return svg(p,'Schematic animal drawings, learned vectors and a two-dimensional projection; proximity depends on training')
    if n==4:
        p=helix(90,160,360,65)+arrow(510,160,650,160)+network(730,60,300,200,ORANGE)+text(1370,170,'Predict hidden DNA',48,ORANGE)
        p+=arrow(880,300,880,420,ORANGE)+dna(110,540,'ACGTAT',55,size=36)+arrow(500,510,650,510)+network(730,420,300,180,ORANGE)+arrow(1100,510,1280,510)+circle(1440,510,65,'A/B',BLUE,47)
        return svg(p,'Broad pretraining transfers a backbone to our small classification task')
    if n==5:return pair('Supervised','Self-supervised','Sequence + external label','Input supplies its own target')
    if n==6:
        p=tiles(['ACG','TCC','[MASK]','GCT','GAA'],120)
        p+='<g data-mask-answer>'+text(864,320,'True hidden token: ATG',58,ORANGE)
        for i,(word,probability) in enumerate([('ATG',.55),('GGA',.25),('CCC',.15),('TAA',.05)]):
            x=410+i*300;p+=line(x,475,x,475-probability*210,BLUE if i else ORANGE,65)+text(x,530,word,34,GRAY)
        p+='</g>'
        return live(p,'mask',button('Reveal the hidden target'),'Targets come from the input itself')
    if n==7:
        p=''
        for i,(label,width) in enumerate([('Composition',4),('Patterns and neighbours',8),('Distant regularities',15)]):
            y=100+i*210;p+=text(110,y,label,42,[BLUE,ORANGE,PURPLE][i],'start')+dna(680,y+20,'ACGTATGCTAGTCATG',57,[(0,width,[BLUE,ORANGE,PURPLE][i])],35)
        return svg(p,'Potential cues for masked prediction at widening sequence scales; not proven learned mechanisms')
    if n==8:return pair('Predict a missing token','Separate class A from B','Natural genomes','Our simulated sequences')
    if n==9:
        p=''
        for y,label,opened,c in [(140,'Frozen',False,BLUE),(440,'Fine-tuned',True,ORANGE)]:
            p+=network(300,y-70,290,140,c)+lock(450,y-100,c,opened)+arrow(660,y,940,y)+strip(980,y-35,w=300,h=70)+circle(1510,y,58,'A/B',c,40)+text(155,y+12,label,41,c)
            p+=arrow(1410,y+100,700 if not opened else 250,y+100,c)+text(1050,y+170,'Task loss updates head only' if not opened else 'Task loss can update backbone',37,c)
        return svg(p,'Frozen encoder stops task gradients; fine-tuning can update the backbone')
    if n==10:
        p=network(240,125,370,230)+text(425,520,'~50 million weights',48,BLUE)+circle(1200,230,100,'720',ORANGE,70)+text(1200,520,'Labelled training rows',48,ORANGE)
        p+=text(864,665,'Frozen features · small fitted head · local CPU',45,GRAY)
        return svg(p,'Why this course freezes the encoder: compute, few labels and an interpretable comparison')
    return prompt('What does pretraining change?','Which evaluation responsibilities stay with us?')


def s2(n,data):
    if n==1:
        p=dna(120,330,'ACGTATGCATGCTACGTACG',76,[(7,10,ORANGE)],44)
        p+='<rect x="610" y="263" width="242" height="110" rx="15" fill="none" stroke="'+ORANGE+'" stroke-width="6"/>'
        for i in [0,2,4,8,11,14,17,19]:
            x=120+i*76;p+=f'<path d="M728 250 Q{(728+x)/2} {70+abs(i-8)*3} {x} 250" fill="none" stroke="{BLUE}" stroke-width="{3+i%3}"/>'
        p+=text(864,570,'Local window → information across tokens',50,BLUE)
        return svg(p,'A local convolution window contrasted with a token attending across the sequence')
    if n==2:
        seq='ATGCTAAGCT';p=''
        for y,words,label in [(90,list(seq),'Bases · 10'),(300,['ATG','CTA','AGC','T'],'Tiled 3-mers + remainder · 4'),(510,['ATGC','TAA','GCT'],'Learned-token sketch · 3')]:
            p+=text(85,y,label,38,GRAY,'start')+tiles(words,y+85,500,(1120/len(words)),36)
        return svg(p,'All three tokenizations reconstruct ATGCTAAGCT exactly; token choices change sequence length')
    if n==3:
        p=text(200,125,'[CLS]',45,GRAY)+text(960,125,'160 DNA bases',58,BLUE)
        for i in range(26):
            x=340+(i%13)*97;y=230+(i//13)*140
            p+=line(x-28,y+22,x+28,y+22,BLUE,30)+text(x,y-20,'6',32,BLUE)
        for i,b in enumerate('ACGT'):p+=circle(700+i*110,550,32,b,ORANGE,32)
        p+=text(864,690,'1 special + 26 six-mers + 4 bases = 31 tokens',45,INK)
        return svg(p,'Exactly 31 tokens at 160 bases: CLS, 26 six-mers, four bases; no truncation')
    if n==4:
        p=tiles(['CCA','ATG','GCT','TAA'],100,220,360)+strip(610,240,w=470)
        for x in [300,1000,1350]:p+=f'<path d="M700 175 Q{(700+x)/2} 320 {x} 175" fill="none" stroke="{ORANGE}" stroke-width="5"/>'
        p+=strip(610,430,values=[-.3,.8,.1,-.7,.2,.5,.4,-.2],w=470)+text(1310,280,'Input vector',43,GRAY)+text(1310,480,'Contextual vector',43,BLUE)
        p+=text(864,650,'Same letters · different context · different representation',43,BLUE)
        return svg(p,'Conceptual codon-sized token example; context changes a representation without proving start-codon recognition')
    if n==5:
        p=circle(420,130,60,'2',BLUE,65)+circle(1300,130,60,'6',ORANGE,65)+arrow(450,225,790,340,BLUE)+arrow(1270,225,940,340,ORANGE)
        p+=text(864,415,'0.75 × 2 + 0.25 × 6 = 3',65,INK,attrs='data-attention-equation')
        return live(p,'attention','<label>Weight on 2 <input type="range" min="0" max="100" value="75" data-weight aria-label="Weight on the value two"></label>','Weights sum to 1; real attention combines vectors')
    if n==6:
        p=circle(255,280,70,'Token',BLUE,40)
        for i,(label,meaning,c) in enumerate([('Query','What matches?',BLUE),('Key','What can match me?',ORANGE),('Value','What gets passed on?',PURPLE)]):
            y=100+i*210;p+=arrow(340,280,640,y,c)+text(850,y+15,label,62,c)+text(1330,y+15,meaning,41,c)
        p+=text(864,690,'Query · key → scores → softmax → weights · values',42,INK)
        return svg(p,'Queries and keys determine normalized weights; values provide the mixed information')
    if n==7:
        p=''
        for i in range(7):
            for j in range(7):p+=f'<rect x="{210+j*65}" y="{70+i*65}" width="58" height="58" fill="{ORANGE if i==2 and j==5 else BLUE}" fill-opacity="{.15+((i*3+j*7)%11)/16}"/>'
        p+=text(1180,200,'High attention',62,BLUE)+text(1180,350,'≠',92,ORANGE)+text(1180,490,'Biological cause',62,BLUE)
        return svg(p,'Schematic attention heatmap; high attention does not establish causation')
    if n==8:
        p=tiles(['ACGTAC','TTAGGC','…'],590,170,430,40)
        for i in range(4):
            y=415-i*90;p+=line(210,y,1460,y,BLUE,9)+text(1500,y+12,['1','2','⋮','12'][i],32,GRAY)
        p+=text(864,100,'12 layers · 16 heads · 512 coordinates',52,BLUE)+text(864,680,'Attention + feed-forward transformations',42,GRAY)
        return svg(p,'Pinned NT-v2 config: 12 encoder layers, 16 attention heads, hidden width 512; diagram is schematic')
    if n==9:
        p=''
        for i in range(7):
            p+=strip(280+i*170,70,values=[math.sin(i+j) for j in range(8)],w=125,h=250) if i else '<rect x="280" y="70" width="125" height="250" fill="#dce3e8"/>'
        p+=text(340,380,'CLS ×',34,GRAY)+text(1000,380,'30 DNA token vectors',43,BLUE)+arrow(864,430,864,490)+strip(590,525,w=550,h=90)+text(864,690,'Mean → one vector of 512 numbers',47,BLUE)
        return svg(p,'Exclude special tokens and padding, then mean-pool the 30 last-layer DNA vectors')
    if n==10:return list_figure(['Pinned model + revision','Last hidden layer','Mean of DNA tokens only','512 numbers per sequence'])
    if n==11:
        p=helix(70,200,300,65)+arrow(420,200,560,200)+network(610,110,230,180)+lock(725,30)
        p+=arrow(900,200,1030,200)+strip(1080,170,w=260,h=60)+arrow(1400,200,1510,200)+circle(1605,200,55,'p',ORANGE,50)
        p+=text(725,390,'Frozen encoder',44,BLUE)+text(1210,390,'512 features',42,BLUE)
        p+=text(864,560,'Standardise → logistic regression → P(B)',54,ORANGE)+text(864,680,'Scaler: training inputs · classifier: training inputs + labels',40,GRAY)
        return svg(p,'Frozen encoder, 512 features, training-only scaling and logistic regression, class probability')
    return prompt('What might averaging lose?','What could contextual vectors still preserve?')


def s3(n,data):
    if n==1:
        p=''
        for i,(label,c) in enumerate([('Watch two training sequences',ORANGE),('Check every stored vector',BLUE)]):
            y=170+i*330;p+=text(90,y-90,label,49,c,'start')+helix(110,y,390,65)+arrow(550,y,770,y,c)+strip(900,y-35,w=550,h=70)
        return svg(p,'Two real training vectors first; provenance-checked full-data extraction or cache next')
    if n==2:return notebook('Continue where Day 2 stopped','Stage 04 definitions\nDay 3 · identity → live checkpoint','Fresh runtime? Complete the Day 2 cells first.')
    if n==3:return '<div class="d3-code"><pre>revision=PINNED_REVISION\ncode_revision=PINNED_REVISION\ntrust_remote_code=True\nuse_safetensors=True</pre><p>Custom Python runs here.</p></div>'
    if n==4:return svg(text(864,165,'CC BY–NC–SA 4.0',82,BLUE)+text(864,330,'Attribution · Non-commercial · Share-alike',48,ORANGE)+text(864,520,'Custom code has separate Apache-2.0 notices',40,GRAY),'Weight licence and custom-code notices are distinct; check terms for your use')
    if n==5:
        p=helix(100,220,440,80)+arrow(620,220,810,220)+strip(950,140,w=600)+strip(950,270,w=600,values=[-.4,.7,.3,-.2,.6,-.1,.5,.2])+text(1250,450,'(2, 512)',90,BLUE)
        return svg(p+text(864,640,'Read shape + timing from the notebook',46,GRAY),'Two actual training sequences yield two 512-dimensional vectors; classroom timings come from execution')
    if n==6:
        p=''
        for i,values in enumerate(data['live_components']['simple']):
            p+=strip(160,100+i*190,values[:8],w=1400,h=110)
            for j,v in enumerate(values[:8]):p+=text(248+j*175,270+i*190,f'{v:+.3f}',32,GRAY)
        p+=text(864,625,'First 8 coordinates · two real training vectors',46,BLUE)
        return svg(p,'Actual local current primary training-vector components; values and source identity recorded in Day 3 evidence')
    if n==7:
        p=''
        times=[(v,data['run']['runs'][v]['cache_load_or_extraction_seconds'],data['run']['runs'][v]['classifier_fit_seconds']) for v in ['simple','interaction']]
        maximum=max(x[1] for x in times)
        for i,(v,extract,fit) in enumerate(times):
            y=150+i*270;p+=text(100,y-50,'Primary PPM' if v=='simple' else 'Order control',43,INK,'start')
            p+=line(420,y,420+extract/maximum*1000,y,ORANGE,35)+text(1460,y+13,f'{extract:.2f}s',42,ORANGE,'start')
            p+=line(420,y+90,420+max(3,fit/maximum*1000),y+90,BLUE,22)+text(600,y+103,f'Head fit {fit:.3f}s',38,BLUE,'start')
        p+=text(864,680,'Local CPU · extraction/cache checks vs classifier fitting',39,GRAY)
        return svg(p,'Current local extraction/cache-check and classifier fit wall times; setup/network not measured as classroom cost')
    if n==8:return list_figure(['Sample IDs + per-sequence hashes','Embedding matrix','Model + revision + layer/pooling','Dataset generation identity'])
    return prompt('The vectors are real.','What happens if they meet the wrong labels?')


def cache_diagram(aligned=False):
    p=text(400,65,'Requested samples',46,BLUE)+text(1300,65,'Cache on disk',46,ORANGE)
    for i,(sid,val) in enumerate([('A','A'),('B','B'),('C','C')]):
        y=160+i*140;p+=circle(400,y,35,sid,BLUE,36)
    for i,sid in enumerate(['C','A','B']):
        y=160+i*140;p+=circle(1300,y,35,sid,ORANGE,36)+strip(1390,y-23,w=220,h=46,values=[.3,-.2,.8])
    mapping=[1,2,0] if aligned else [0,1,2]
    for i,j in enumerate(mapping):p+=arrow(450,160+i*140,1240,160+j*140,BLUE if aligned else ORANGE,5)
    p+=text(864,550,'Join by ID' if aligned else 'Join by position',55,BLUE if aligned else ORANGE)
    return p


def s4(n,data):
    if n==1:return svg(cache_diagram(),'Same matrix dimensions, wrong sample correspondence under a positional join')
    if n==2:return live('<g data-cache-drawing>'+cache_diagram()+'</g>','alignment',button('Align by sample ID'),'Shape alone cannot verify correspondence')
    if n==3:return list_figure(['Same generated dataset','Unique IDs · exact coverage','Same model + revision + pooling','Per-ID sequence hash matches','Finite matrix · n × 512'])
    if n==4:return '<div class="d3-code"><pre>positions = pd.Index(ids).get_indexer(\n    samples["sample_id"]\n)\nfeatures = embeddings[positions]</pre><p>Verify identity and sequence hashes first.</p></div>'
    if n==5:return notebook('Repair the join','Day 3 · synthetic alignment\nReorder → align → reject missing IDs','Section 4 · completed code; optional follow-along')
    if n==6:
        p=''
        for x,w,c,label in [(100,900,BLUE,'Train · 720'),(1000,300,ORANGE,'Validation · 240'),(1300,300,GRAY,'Test · 240')]:
            p+=line(x,250,x+w,250,c,85)+text(x+w/2,385,label,40,c)
        p+=text(550,120,'Fit scaler + classifier',47,BLUE)+text(1150,120,'Predict',42,ORANGE)+lock(1450,80,GRAY)
        p+=text(864,600,'Read current validation ROC-AUC + AP in the notebook',42,GRAY)
        return svg(p,'Training fits preprocessing and classifier; validation scored; primary protected test remains masked')
    return statement('Missing or ambiguous identity?','Stop and repair upstream.',ORANGE)


def chart(data,variant,metric='roc_auc'):
    p='';start=560;width=950
    for i,(key,label,c) in enumerate(METHODS):
        y=100+i*135;row=next(x for x in data['metrics'] if x['variant']==variant and x['method']==key);v=row[metric]
        p+=text(470,y+15,label,43,c,'end')+line(start,y,start+v*width,y,c,35)+text(start+v*width+25,y+15,f'{v:.3f}',39,c,'start')
    p+=line(start+width*.5,45,start+width*.5,560,'#bdcbd6',3,attrs='stroke-dasharray="10 10"')
    p+=text(start,620,'0',30,GRAY)+text(start+width*.5,620,'0.5',30,GRAY)+text(start+width,620,'1',30,GRAY)
    return p


def s5(n,data):
    if n==1:return prompt('Where would you place the four models?','Primary motif task · paired order control')
    if n==2:
        p=''
        for i,(_,label,c) in enumerate(METHODS):
            x=240+i*410;p+=circle(x,200,55,str(i+1),c,50)+text(x,345,label.replace(' + ',' +\u00a0'),35,c)
        p+=line(180,500,1540,500,BLUE,12)+text(864,630,'Same split IDs · same metrics · same threshold policy',44,BLUE)
        return svg(p,'Four workflows share split identities and evaluation policy within each variant')
    if n in [3,4]:
        v='simple' if n==3 else 'interaction'
        return '<div class="d2-live d3-results" data-variant="'+v+'"><div data-validation-chart>'+svg(chart(data,v),'Current matched validation ROC-AUC for four workflows',650)+'</div><div class="d3-controls">'+button('Show average precision','data-metric')+'</div></div>'
    if n==5:
        p=''
        for i,(a,b,c) in enumerate([('Counts','Words without positions',BLUE),('CNN','Ordered input + fitted detectors',ORANGE),('Frozen encoder','Context + external dependencies',PURPLE)]):
            y=110+i*205;p+=text(100,y,a,55,c,'start')+text(760,y,b,44,INK,'start')
        p+=text(864,680,'Also compare cost, inspectability and reproducibility',42,GRAY)
        return svg(p,'Representation tradeoffs beyond a single validation score')
    if n==6:return list_figure(['Pretraining asks a different question','Mean pooling compresses token vectors','A linear head uses frozen features','Simulated DNA differs from natural genomes'])
    if n==7:
        p=f'<ellipse cx="460" cy="260" rx="350" ry="220" fill="{BLUE}" fill-opacity=".06" stroke="{BLUE}" stroke-width="5"/><ellipse cx="1340" cy="330" rx="280" ry="170" fill="{ORANGE}" fill-opacity=".06" stroke="{ORANGE}" stroke-width="5"/>'
        p+=helix(220,230,470,75)+text(460,90,'Pretraining genomes',47,BLUE)+text(1340,330,'Simulated DNA',47,ORANGE)
        p+=text(460,565,'Plants + viruses excluded',41,GRAY)+text(460,630,'according to this model card',33,GRAY)+text(1340,580,'Different distribution',43,ORANGE)
        return svg(p,'Model-card domain excludes plants and viruses; course simulation is a different distribution')
    if n==8:
        p=f'<circle cx="690" cy="260" r="225" fill="{BLUE}" fill-opacity=".08" stroke="{BLUE}" stroke-width="5"/><circle cx="1040" cy="260" r="225" fill="{ORANGE}" fill-opacity=".08" stroke="{ORANGE}" stroke-width="5"/>'
        p+=text(590,270,'Pretraining',44,BLUE)+text(1150,270,'Evaluation',44,ORANGE)+text(866,285,'?',74,INK)+text(864,620,'Overlap has not been audited',52,GRAY)
        return svg(p,'Potential pretraining and evaluation overlap; no claim that it has been excluded')
    if n==9:
        p=helix(100,200,650,85)+text(425,70,'~1 million input bases',51,BLUE)+arrow(820,200,1000,200)
        for i,(lab,c) in enumerate([('RNA expression',BLUE),('Accessibility',ORANGE),('TF binding',PURPLE),('Splicing',GRAY)]):
            y=65+i*130;p+=text(1100,y,lab,36,c,'start')
            points=' '.join(f'{1110+j*20},{y+75-45*abs(math.sin(j*.7+i))**6}' for j in range(25))
            p+=f'<polyline points="{points}" fill="none" stroke="{c}" stroke-width="4"/>'
        p+=text(864,630,'Variant effect: compare alternate and reference predictions',43,INK)+text(864,700,'AlphaGenome · Avsec et al. · official model documentation',30,GRAY)
        return svg(p,'Native schematic of AlphaGenome sequence-to-functional-track and variant comparison; not reproduced course results')
    if n==10:return prompt('What changes with real promoters?','Which independent measurements would you need?')
    if n==11:return list_figure(['Cheap, readable baseline → counts','Position-aware learning → a CNN','Plausible transfer → borrowed features'])
    return list_figure(['Four workflows · two variants','Validation predictions saved by ID','Test labels unscored','Development decisions complete'])


def blank_test_table():
    rows=''.join('<tr><td>'+variant+'</td><td>'+E(label)+'</td><td data-test-value="'+v+'|'+key+'|roc_auc">—</td><td data-test-value="'+v+'|'+key+'|average_precision">—</td></tr>' for v,variant in [('simple','Primary'),('interaction','Order')] for key,label,_ in METHODS)
    return '<div class="d2-live d3-test"><table><thead><tr><th>Variant</th><th>Workflow</th><th>ROC-AUC</th><th>AP</th></tr></thead><tbody>'+rows+'</tbody></table><div class="d3-controls"><label class="d3-import">Load classroom result <input type="file" accept=".json,application/json" data-test-import></label></div><p data-test-status aria-live="polite">Not revealed · import the saved result after the authorised classroom action</p></div>'


def s6(n,data):
    if n==1:return svg(envelope()+text(864,660,'240 primary + 96 order-control rows · one opening',44,BLUE),'Protected test envelope remains closed until the planned authorized reveal')
    if n==2:return pair('A recollection','A checkable record','“I changed nothing”','Hashes · settings · timestamp')
    if n==3:
        labels=['Dataset, split IDs and source identity','Models, representation and metric policy','Validation predictions saved by ID','Instructor name, time and authorisation','All prerequisites satisfied']
        return '<div class="d2-live d3-checklist">'+''.join('<label><input type="checkbox">'+E(l)+'</label>' for l in labels)+'<p>Teaching checklist · the notebook performs the actual freeze</p></div>'
    if n==4:return notebook('Write a manifest; leave test labels closed','freeze_workflows()','Stage 05 · freeze only; never overwrites an existing freeze')
    if n==5:return prompt('Commit to your prediction.','Then run the instructor-approved freeze cell.')
    if n==6:return '<div class="d3-code"><pre>reveal_test(\n    confirmation=\n    "REVEAL THE FROZEN TEST RESULTS"\n)</pre><p>Separate instructor action · guards must pass</p></div>'
    if n==7:return blank_test_table()
    if n==8:
        return '<div class="d2-live d3-live" data-test-comparison>'+svg('', 'Validation versus test; test values await instructor import',560)+'<div class="d3-controls">'+button('Show order control','data-test-variant')+'</div><p data-test-status>Primary · validation 240 / test 240 · test not revealed</p></div>'
    if n==9:return pair('Observation','Possible explanation','What happened?','What could account for it?')
    if n==10:
        p=arrow(864,160,420,365,ORANGE,6)+arrow(864,160,1300,365,BLUE,6)+text(420,465,'Tune on the test',49,ORANGE)+text(1300,465,'Report the fixed result',49,BLUE)
        p+=line(180,400,650,510,ORANGE,6)+text(864,650,'Follow-up ideas need fresh independent evidence',48,GRAY)
        return svg(p,'After reveal, report fixed results; do not tune settings against the same test')
    if n==11:
        p=text(300,285,'Develop',62,BLUE)+arrow(470,265,720,265)+line(830,90,830,470,ORANGE,12)+circle(830,265,42,'',ORANGE,0)+arrow(920,265,1160,265)+text(1430,285,'Historical evidence',54,GRAY)
        p+=text(864,650,'The same boundary applies to tomorrow’s coding agent',45,BLUE)
        return svg(p,'A one-way evaluation boundary also constrains Day 4 agent work')
    if n==12:return pair('Supported','Beyond this experiment','These fixed simulations','Biological mechanism')
    if n==13:
        p=''
        for i,(lab,c) in enumerate([('Learn elsewhere',BLUE),('Mix context',ORANGE),('Record provenance',PURPLE),('Align by ID',BLUE),('Freeze → reveal',ORANGE)]):
            x=185+i*340;p+=circle(x,220,45,str(i+1),c,42)+text(x,380,lab,34,c)
        p+=text(864,625,'Tomorrow: who owns the claim when an agent writes the code?',44,INK)
        return svg(p,'Day 3 recap: transfer, attention, provenance, alignment and evaluation boundary')
    return '<div class="d3-notebook"><p>What would you like to revisit?</p><a href="../../notebooks/README.md">Notebook guide ↗</a><br><a href="../../course_code/04_foundation_embeddings.py">Encoder workflow ↗</a><br><a href="../../instructor/guide.md">Instructor guide ↗</a></div>'


CSS='''/* === DAY 3 ILLUSTRATED STORY === */
.day-three{display:block;padding:80px 96px;border:0;background:#fff;color:#18344b;font-family:"Source Sans 3",sans-serif}
.day-three h1{font-family:inherit;font-size:72px;line-height:1.16;letter-spacing:-1px;margin:0;max-width:1728px;color:#18344b}
.day-three>.slide-top,.day-three>.subtitle,.day-three>.takeaway{display:none}
.day-three>.content{position:absolute;left:96px;top:230px;width:1728px;height:740px;display:block;margin:0;padding:0;overflow:hidden}
.day-three .content svg{display:block;width:1728px;height:720px;font-family:inherit}
.day-three .d3-live>svg{height:560px}.day-three .d3-results svg{height:650px}
.day-three .d3-controls{display:flex;align-items:center;justify-content:center;gap:25px;min-height:68px;font-size:31px}
.day-three .d3-controls label{display:flex;align-items:center;gap:25px}
.day-three input[type=range]{width:550px;accent-color:#0072B2}
.day-three button,.day-three .d3-import{font:inherit;font-size:30px;border:2px solid #0072B2;padding:10px 25px;color:#0072B2;background:white;border-radius:6px}
.day-three button[aria-pressed=true]{background:#e5f1f8}.day-three button:disabled{opacity:.5}
.day-three .d3-live>p,.day-three .d3-test>p{font-size:32px;text-align:center;margin:14px 0 0;color:#697782;line-height:1.3}
.day-three .d3-prompt{padding:95px 50px}.day-three .d3-prompt p{font-size:76px;line-height:1.3;margin:0 0 80px;color:#0072B2}
.day-three .d3-prompt .secondary{font-size:54px;color:#697782}
.day-three .d3-notebook{padding:35px 50px}.day-three .d3-notebook p{font-size:61px;line-height:1.3;margin:0 0 50px}
.day-three .d3-notebook a{font-size:43px;color:#0072B2;display:inline-block;margin-bottom:30px}
.day-three .d3-notebook .route{font-size:37px;color:#697782;margin-top:35px}
.day-three pre{border:0;background:none;font-family:inherit;font-size:48px;line-height:1.55;padding:0;margin:0 0 45px;color:#18344b;white-space:pre-wrap}
.day-three .d3-code{padding:40px 80px}.day-three .d3-code p{font-size:43px;color:#D55E00}
.day-three .d3-checklist{padding:20px 60px}.day-three .d3-checklist label{display:flex;gap:35px;align-items:center;font-size:45px;margin-bottom:45px}
.day-three .d3-checklist input{width:36px;height:36px;accent-color:#0072B2}.day-three .d3-checklist p{font-size:32px;color:#697782}
.day-three .d3-test table{width:100%;border-collapse:collapse;font-size:34px;line-height:1.15}
.day-three .d3-test th,.day-three .d3-test td{padding:14px 30px;text-align:left;border-bottom:1px solid #d7e1e8;background:none}
.day-three .d3-test th{color:#0072B2;font-weight:600}.day-three .d3-test th:nth-child(n+3),.day-three .d3-test td:nth-child(n+3){text-align:right}
.day-three .d3-import{cursor:pointer;position:relative;overflow:hidden}.day-three .d3-import input{position:absolute;inset:0;opacity:0;width:100%;cursor:pointer}
.day-three .d3-import:focus-within{outline:4px solid #D55E00;outline-offset:4px}
.day-three .notes{font-family:inherit}.day-three.active .notes.show,.day-three.active .notes.show *{visibility:visible}
.day-three .notes p{font-size:32px;line-height:1.45}.day-three .notes .small{font-size:25px}
[data-mask-answer]{opacity:0;transition:opacity .2s}[data-mask-answer].revealed{opacity:1}
@media print{.day-three .d3-controls{display:none}.day-three .notes{display:none!important}[data-mask-answer]{opacity:1!important}.day-three{display:block!important}}
/* === END DAY 3 ILLUSTRATED STORY === */
'''


def build():
    evidence=ROOT/'instructor/verification/day3-current.json'
    data=json.loads(evidence.read_text())
    assert not data['test_evaluated']
    for path,sha in data['source_sha256'].items():
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==sha, f'Stale Day 3 evidence: {path}'
    assert data['weight_sha256']=='17e75af297556ea56828716d8aa539e8f12b8b625547204b74171ab91aa33569'
    # Reuse the established self-contained presentation shell, not its Day 2 content or controls.
    source=(ROOT/'Slides/Day_2/presentation.html').read_text()
    start=source.index('.day-two-opening{')
    end=source.index('</style>',start)
    source=source[:start]+CSS+source[end:]
    source=re.sub(r'<script id="day-two-[^"]+"[^>]*>.*?</script>\s*','',source,flags=re.S)
    source=source.replace('Day 2 · Machine learning','Day 3 · Machine learning').replace('ml-course-2026-day-2-edits-v1','ml-course-2026-day-3-edits-v2')
    source=source.replace("key.startsWith('day-2-')","key.startsWith('day-3-')")
    source=source.replace('Number(localMatch[1]) !== 2','Number(localMatch[1]) !== 3').replace('if (day === 2)','if (day === 3)')
    source=re.sub(r'bindDayTwo\w+\(\);\n?','',source)
    # The delivery filename identifies this day for exported copies too.
    source=source.replace('day-2-edited','day-3-edited')
    aliases={f'#day-3-slide-{i}':key for i,key in enumerate(['day-3-s1-welcome','day-3-s2-borrowing-context','day-3-s1-masked-lm','day-3-s2-mean-pooling','day-3-s3-roadmap','day-3-break-1','day-3-s3-notebook-open','day-3-s4-silent-failure','day-3-s4-alignment-practical','day-3-break-2','day-3-s5-primary-results','day-3-s5-why-not-crush','day-3-s6-checklist-aloud','day-3-s6-test-results-table','day-3-s6-synthesis'],1)}
    source=re.sub(r'const openingAliases = \{.*?\};','const openingAliases = '+json.dumps(aliases)+';',source)
    story=(ROOT/'Slides/Day_3/story.md').read_text()
    records=[]
    for sec,count in [(1,11),(2,12),(3,9),(4,7),(5,12),(6,14)]:
        span=story.split(f'<a id="section-{sec}"></a>')[1].split('<a id="')[0]
        blocks=re.findall(rf'### S{sec}-(\d+) · (.*?)\n(.*?)(?=\n### |\Z)',span,re.S)
        assert len(blocks)==count
        for number,title,body in blocks:
            def field(name):
                return E(required_match(r'\*\*'+re.escape(name)+r':\*\* (.*?)(?=\n\n|\Z)',body,re.S)[1]).replace('`','')
            key=required_match(r'\*\*Proposed slide ID:\*\* `([^`]+)`',body)[1]
            provenance='Native SVG conceptual figures and small attention/masking numbers are constructions, not fitted outputs. Actual live components, configuration, timings and current matched validation results: instructor/verification/day3-current.json, local CPU2threads, 2026-11-03. Stage03 seed2026/24epochs, current 15-position PPM and separate paired order control; no retuning. Model '+MODEL+'; revision '+REVISION+'; last-layer mean excluding special/padding tokens; 512 dimensions. StandardScaler uses training inputs, logistic regression uses training labels. Test labels unscored. Test panels start empty and accept only instructor-imported classroom results; importing does not execute a reveal or independently verify the manifest. Colab, classroom timing and projector readability unverified.'
            if sec==5 and int(number)==9:provenance+=' AlphaGenome: official https://www.alphagenomedocs.com/ and https://www.alphagenomedocs.com/faqs.html ; Avsec et al., Advancing regulatory variant effect prediction with AlphaGenome, Nature649(2026), doi:10.1038/s41586-025-10014-0; https://github.com/google-deepmind/alphagenome . Native schematic only, not reproduced results.'
            if sec==2 and int(number)==8:provenance+=' Architecture recipe: Ji et al., DNABERT, Bioinformatics 2021, doi:10.1093/bioinformatics/btab083; pinned NT-v2 config has 12layers, 16heads, width512, rotary positions.'
            record=dict(day=3,id=key,anchor=key,sectionSequence=True,sectionNumber=sec,kind='day-three',title=E(title),time=field('Time'),body=globals()[f's{sec}'](int(number),data),subtitle='',takeaway='',notes=field('What I want to say'),point=field('Point / reveal'),transition=field('Transition'),sourceNote=E(provenance))
            records.append(record)
        if sec in [2,4]:
            num=1 if sec==2 else 2;key=f'day-3-break-{num}'
            records.append(dict(day=3,id=key,anchor=key,sectionSequence=True,sectionNumber=sec,kind='day-three',title='Ten-minute break',time='50:00–60:00 (10:00)' if num==1 else '100:00–110:00 (10:00)',body=statement('Ten-minute break','Next: real vectors' if num==1 else 'Next: compare the workflows'),subtitle='',takeaway='',notes='Return at minute '+('60' if num==1 else '110')+'.',point='Leave this slide up.',transition='Continue with the next section.',sourceNote='Suggested classroom timing.'))
    assert len(records)==67 and len({s['id'] for s in records})==67
    m=required_match(r'<script id="day-data" type="application/json">(.*?)</script>',source,re.S)
    source=source[:m.start(1)]+json.dumps(records,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')+source[m.end(1):]
    payload={'metrics':data['metrics'],'aligned':cache_diagram(True),'misaligned':cache_diagram(False)}
    tags='<script id="day-three-evidence" type="application/json">'+json.dumps(payload,separators=(',',':')).replace('<','\\u003c')+'</script>\n<script id="day-three-interactions">\n'+(ROOT/'tools/day3_interactions.js').read_text()+'\n</script>\n'
    source=source.replace('<script id="presentation-controller">',tags+'<script id="presentation-controller">',1)
    source=source.replace('window.presentation = new SlidePresentation();','window.presentation = new SlidePresentation();\nbindDayThree();')
    DECK.write_text(source)
    print('Built Day 3: 65 content scenes + two breaks; native illustrations; no prefilled test scores.')


if __name__=='__main__':build()
