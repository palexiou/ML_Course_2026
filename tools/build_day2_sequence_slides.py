"""Build reviewed Day 2 Section 3 or 4, in that order; figures work offline.

Usage: python tools/build_day2_sequence_slides.py 3 (then 4).
Readout values and filter maps are teaching constructions, not fitted results.
"""
import html
import json
import re
from build_day2_section1 import required_match
import sys

from build_day2_section1 import ROOT, DECK, BLUE, ORANGE, INK, GRAY, PURPLE, text, line, arrow, circle, svg, dna, plot

E=html.escape
SEQ='ACCGTCCG'
COLORS=[ORANGE,BLUE,PURPLE]
MAPS=[[0,1,0,0,0,1],[0,0,0,1,0,0],[0,0,0,0,1,0]]
NAMES=['CCG','GTC','TCC']
SOURCE3='''Constructed demonstration, not fitted filters or empirical results. Input ACCGTCCG, A/C/G/T channel order, shape 4×8. CCG filter rows (0,0,0)/(1,1,0)/(0,0,1)/(0,0,0); bias −2; ReLU. Valid-window scores −1,1,−1,−2,−1,1 give map 0,1,0,0,0,1 at starts 0–5. ACTGTCCG scores −1,0,−2,−2,−1,1 give map 0,0,0,0,0,1. Changed position 2 affects windows 0/1/2 but only activation 1 changes. GTC and TCC filters use the same designed rule, giving maps 0,0,0,1,0,0 and 0,0,0,0,1,0. Extended ACCGTCCGAAAA / AACCGTCCGAAA have peaks 1/5 and 2/6. A one-position zero pad gives eight outputs aligned to centers, peaks 2/6. Actual SequenceCNN: A/C/G/T batch×4×160 input, Conv1d 4→16 width7/pad3, ReLU, Conv1d16→16 width5/pad2, ReLU, stride1/no dilation. Both maps retain length160; nominal interior receptive field is 7+5−1=11. This is controlled simulated sequence classification; the designed CCG detector is not the primary PPM. The notebook has canonical definitions but no new guided detector/mutation cells; the slide inspection is complete without running it. Suggested section pacing 30 minutes, not rehearsed.'''
SOURCE4='''Constructed feature maps, not fitted CNN outputs. CCG=(0,1,0,0,0,1), GTC=(0,0,0,1,0,0), TCC=(0,0,0,0,1,0). Global maxima=(1,1,1). Channel-major flatten preserves all18 entries; append3 maxima to get21. Move CCG activation 1→2 at map level, keeping other maps fixed; this is not a claimed DNA-edit experiment. Positional neuron weights (0,1.2,−0.4,0,0,0.3), bias−0.5, all other coefficients zero: original score1/ReLU1; moved score−0.6/ReLU0. Independent familiar output conversion z=0.3 gives sigmoid0.5744425 and class B at threshold0.5; it is not derived from that positional neuron. Actual SequenceCNN.forward: N×4×160 → N×16×160; flatten(1) N×2560 and amax(dim=2) N×16, concatenated dim1 to N×2576; Linear2576→32, ReLU, Linear32→1, squeeze(1). predict_cnn uses eval/inference_mode then sigmoid. The maximum summary is derivable from flattened maps; the branch provides an explicit summary, not new information. Convolution and dense layers have fitted weights/biases; encoding, activations, flatten, max and concat have no fitted parameters here. PPM and filter weights have different meanings; no biological discovery or empirical comparison is claimed. Validation supports development; test results never guide decisions. Suggested section pacing25 minutes, not rehearsed.'''


def detector(seq,target='CCG',padding=0):
    scores=[sum(0<=i+j<len(seq) and seq[i+j]==base for j,base in enumerate(target))-2 for i in range(-padding,len(seq)-2+padding)]
    return scores,[max(0,v) for v in scores]


def matrix(seq=SEQ,x=330,y=150,step=140,row=65,weights=False):
    p=''
    for c,base in enumerate('ACGT'):
        yy=y+c*row;p+=text(x-80,yy+10,base,35,GRAY,'end')
        for j,value in enumerate(seq):
            active=value==base;xx=x+j*step
            if active:p+=f'<circle cx="{xx}" cy="{yy}" r="22" fill="{ORANGE}" fill-opacity=".12" stroke="{ORANGE}" stroke-width="2"/>'
            p+=text(xx,yy+10,int(active),30,INK if active else '#a3b1ba')
    return p


def sequence_matrix(seq=SEQ,padding=False):
    shown=[None,*seq,None] if padding else list(seq)
    x=300 if padding else 400;step=125 if padding else 130
    p=''
    for j,b in enumerate(shown):p+=text(x+j*step,65,b if b else 'zeros',44 if b else 25,INK if b else GRAY)
    p+=matrix(shown,x,145,step,60)
    return p


def track(values,x=440,y=310,step=140,label='',color=BLUE,indices=True,upto=999):
    p=line(x-25,y,x+(len(values)-1)*step+25,y,'#bccbd5',3)
    if label:p+=text(x-70,y-35,label,38,color,'end')
    for i,v in enumerate(values):
        xx=x+i*step;p+=f'<g opacity="{1 if i<=upto else .12}">'
        if v:p+=line(xx,y,xx,y-80*v,color,8)
        p+=f'<circle cx="{xx}" cy="{y-80*v}" r="{11 if v else 5}" fill="{color}"/>'+'</g>'
        if indices:p+=text(xx,y+45,i,27,GRAY)
    return p


def maps_view(maps=MAPS,x=420,y=145,step=155,gap=175,maxima=False):
    p=''
    for i,values in enumerate(maps):
        yy=y+i*gap;p+=track(values,x,yy,step,NAMES[i],COLORS[i])
        if maxima:p+=arrow(x+step*5+45,yy-30,1440,yy-30,'#a6bdcc',3)+circle(1530,yy-30,40,max(values),COLORS[i],42)
    return p


def ribbon(values,x=210,y=360,step=65,channel_offset=0,per_value=False):
    p=line(x-22,y+25,x+(len(values)-1)*step+22,y+25,'#bdccd6',3)
    for i,v in enumerate(values):
        color=COLORS[i%3] if per_value else COLORS[(i//6+channel_offset)%3] if i<18 else COLORS[(i-18)%3]
        p+=text(x+i*step,y,v,39,color)
    return p


def button(attr,label,extra=''):
    return f'<button type="button" {attr} {extra}>{E(label)}</button>'


def live(kind,p,controls='',readout='',height=560):
    return f'<div class="d2-live sequence-live" data-scene="{kind}" data-height="{height}">'+svg(p,kind.replace('-',' '),height)+f'<div class="d2-controls">{controls}</div><p data-sequence-readout aria-live="polite">{E(readout)}</p></div>'


def base_view(base='C'):
    p=text(430,330,base,170,BLUE)+arrow(610,275,820,275)
    for i,b in enumerate('ACGT'):
        yy=130+i*100;p+=text(1000,yy+15,b,46,GRAY)+circle(1160,yy,32,int(b==base),ORANGE if b==base else '#a9bac6',40)
    return p


def score_view(window):
    p=text(400,55,f'{window} input',43,BLUE)+text(1050,55,'CCG weights',43,ORANGE)
    p+=matrix(window,280,155,115,75)+text(710,285,'×',75,GRAY)+matrix('CCG',930,155,115,75)
    contributions=[int(a==b) for a,b in zip(window,'CCG')];z=sum(contributions)-2
    p+='<g data-calculation="sum" opacity=".12">'+text(540,515,' + '.join(map(str,contributions))+f' − 2 = {z}',54,BLUE)+'</g>'
    p+='<g data-calculation="activation" opacity=".12">'+text(1290,515,f'ReLU({z}) = {max(0,z)}',54,ORANGE)+'</g>'
    return p


def scan_view(start=0):
    scores,values=detector(SEQ);p=dna(320,105,SEQ,140,size=52)
    p+=f'<rect data-window x="{260+start*140}" y="35" width="400" height="130" rx="18" fill="{BLUE}" fill-opacity=".05" stroke="{BLUE}" stroke-width="4"/>'
    p+=text(864,245,'C / C / G weights · same bias −2',40,ORANGE)
    p+='<g data-draw="scan-map">'+track(values,460,420,140,upto=start)+'</g>'
    return p


def inspection_view(seq=SEQ,padding=False):
    p=sequence_matrix(seq,padding)
    _,values=detector(seq,padding=int(padding))
    x=300 if padding else 530;step=125 if padding else 130
    p+=track(values,x,480,step,color=ORANGE)
    return p


def section3(n):
    if n==1:return '<div class="sequence-title-rule"></div>'
    if n==2:
        p=line(350,300,1450,300,'#bbcad4',4)
        for i,b in enumerate('ACGT'):p+=circle(420+i*300,300,14,'',BLUE)+text(420+i*300,210,b,70,BLUE)+text(420+i*300,380,i,42,GRAY)
        p+=arrow(420,450,720,450,ORANGE)+text(570,525,'Distance 1',40,ORANGE)+arrow(420,570,1320,570,BLUE)+text(870,650,'Distance 3',40,BLUE)
        return svg(p,'Scalar base IDs impose arbitrary ordering and distances')
    if n==3:return live('base',f'<g data-draw="base">{base_view()}</g>',''.join(button(f'data-base="{b}"',b,f'aria-pressed="{str(b=="C").lower()}"') for b in 'ACGT'),'C → (0, 1, 0, 0)')
    if n==4:
        p=sequence_matrix()+f'<rect data-column x="355" y="110" width="90" height="265" rx="15" fill="{BLUE}" fill-opacity=".06" stroke="{BLUE}" stroke-width="3"/>'
        for i in range(8):p+=text(400+i*130,455,i,29,GRAY)
        return live('matrix',p,button('data-next-column','Next position')+button('data-reset-column','Reset'),'Position 0 · A → (1, 0, 0, 0) · 4 channels × 8 positions')
    if n==5:
        p=sequence_matrix()+f'<rect x="345" y="15" width="375" height="360" rx="18" fill="{BLUE}" fill-opacity=".05" stroke="{BLUE}" stroke-width="4"/>'
        p+=text(520,530,'4 channels × 3 positions',43,BLUE)+arrow(770,470,1070,520)+circle(1160,520,60,'Σ',BLUE,50)+arrow(1225,520,1360,520)+text(1490,540,'ReLU',48,ORANGE)
        return svg(p,'A local neuron reads every base channel across three adjacent positions')
    if n==6:
        p=text(600,90,'Three filter positions',48,ORANGE)+matrix('CCG',420,220,180,90)
        for i in range(3):p+=text(420+i*180,155,i+1,30,GRAY)
        p+=arrow(950,350,1100,350)+circle(1200,350,65,'Σ',BLUE,54)+text(1200,520,'bias −2',43,BLUE)+arrow(1270,350,1370,350)+text(1480,368,'ReLU',48,ORANGE)
        return svg(p,'A four-channel by three-position CCG scoring filter, bias minus two and ReLU')
    if n==7:return live('score',score_view('CCG'),button('data-score-next','Reveal the sum')+button('data-score-reset','Reset'),'Multiply corresponding entries, then add the bias.')
    if n==8:
        p=score_view('ACC').replace(' opacity=".12"',' opacity="1"')
        return svg(p,'ACC scores minus one; ReLU returns zero',560)
    if n==9:return live('scan',scan_view(),button('data-scan-next','Next window')+button('data-scan-reset','Reset'),'Start 0 · ACC · score −1 → activation 0')
    if n==10:
        p=dna(320,170,SEQ,140,size=55)+track(MAPS[0],460,460,140,color=ORANGE)
        p+=text(864,660,'Six windows → six feature values',48,BLUE)
        return svg(p,'The CCG activation map has peaks at window starts one and five')
    if n==11:
        p=''
        for i,seq in enumerate(['ACCGTCCGAAAA','AACCGTCCGAAA']):
            yy=80+i*310;p+=dna(270,yy,seq,95,size=36)+track(detector(seq)[1],365,yy+175,95,color=COLORS[i])
        return svg(p,'Moving both interior CCG sites shifts their responses from starts one/five to two/six')
    if n==12:return svg(maps_view(y=160,gap=210),'Three designed filters produce distinct position-wise feature maps')
    if n==13:
        p=text(420,75,'Filter parameters',43,BLUE)
        for i,b in enumerate('ACGT'):
            p+=text(150,180+i*90,b,36,GRAY)
            for j in range(3):p+=circle(280+j*130,165+i*90,29,'w',BLUE,30)
        p+=arrow(680,300,900,300)+text(1050,315,'Feature map',45,BLUE)+arrow(1240,300,1360,300)+circle(1460,300,65,'Loss',ORANGE,38)
        p+=text(1460,155,'Sequence label',40,ORANGE)
        p+=f'<path d="M1420 405 Q900 730 500 500" fill="none" stroke="{ORANGE}" stroke-width="5" stroke-dasharray="13 10"/>'+arrow(540,520,500,500,ORANGE)
        p+=text(910,660,'Gradients combine uses across positions',42,ORANGE)
        return svg(p,'Sequence labels determine loss; backward sensitivities reach shared filter weights')
    if n==14:
        p=dna(300,90,SEQ+'AAA',110,size=38)
        for i in range(5):p+=line(245+i*110,230+i*45,1015+i*110,230+i*45,COLORS[i%3],12)
        p+=text(1535,345,'7 bases',35,GRAY)
        for i in range(5):p+=circle(630+i*110,540,20,'',BLUE)
        p+=f'<rect x="580" y="490" width="540" height="100" rx="15" fill="{ORANGE}" fill-opacity=".05" stroke="{ORANGE}" stroke-width="4"/>'
        p+=text(864,465,'5 positions · all 16 feature channels',37,ORANGE)+line(245,625,1455,625,BLUE,5)+text(850,695,'11 DNA positions',47,BLUE)
        return svg(p,'Five overlapping seven-base windows span eleven DNA positions')
    if n==15:return live('padding',f'<g data-draw="inspection">{inspection_view()}</g>',button('data-padding-toggle','Add zero padding'),'No padding · 8 bases → 6 valid-window outputs')
    return live('inspection',f'<g data-draw="inspection">{inspection_view()}</g>',button('data-mutate','Change third base C → T')+button('data-mutation-reset','Reset'),'ACCGTCCG → (0, 1, 0, 0, 0, 1)')


def section4(n):
    return section4_figure(n)


def feature_glyph(x,y,color=BLUE):
    return ''.join(line(x+j*28,y+i*28,x+j*28,y+i*28-12,color,4) for i in range(3) for j in range(5))


def architecture():
    p=''
    p+='<g data-route="1">'+text(160,110,'DNA / one-hot',32,BLUE)+dna(115,255,'ACGT',35,size=30)
    for i,base in enumerate('ACGT'):
        p+=text(70,335+i*45,base,24,GRAY)
        for j in range(4):p+=f'<circle cx="{115+j*35}" cy="{325+i*45}" r="{6 if i==j else 2}" fill="{ORANGE if i==j else GRAY}"/>'
    p+='</g>'
    p+=arrow(285,300,370,300,'#b4c5d1',3)
    for x,k in [(470,7),(740,5)]:
        p+=f'<g data-route="2" data-module="conv{k}">'+text(x,110,f'Conv {k}',34,BLUE)+text(x,160,'ReLU',30,GRAY)+feature_glyph(x-55,245)+text(x,430,'θ',40,ORANGE,attrs='data-theta opacity=".12"')+'</g>'
    p+=arrow(565,300,635,300,'#b4c5d1',3)
    p+='<g data-route="3">'
    p+=f'<path d="M830 300 Q890 150 965 175 M830 300 Q890 450 965 425" fill="none" stroke="{BLUE}" stroke-width="4"/>'
    p+=text(1050,175,'Flatten',36,BLUE)+text(1050,440,'Global max',36,ORANGE)
    p+=f'<path d="M1140 175 Q1210 175 1250 300 M1150 425 Q1210 425 1250 300" fill="none" stroke="{GRAY}" stroke-width="4"/>'
    for j in range(7):p+=line(1260,230+j*24,1310,230+j*24,COLORS[j%3],5)
    p+=text(1285,110,'Join',36,BLUE)+'</g>'
    p+='<g data-route="4" data-module="dense">'+text(1460,110,'Dense / ReLU',31,BLUE)
    for yy in [235,300,365]:p+=line(1325,300,1425,yy,'#b5c8d5',3)+circle(1460,yy,23,'',BLUE)
    p+=text(1460,460,'32 units',31,GRAY)+text(1460,530,'θ',40,ORANGE,attrs='data-theta opacity=".12"')+'</g>'
    p+='<g data-route="5" data-module="output">'
    for yy in [235,300,365]:p+=line(1485,yy,1600,300,'#b5c8d5',3)
    p+=circle(1640,300,33,'z',BLUE,35)+text(1620,460,'z → P(B)',30,ORANGE)+text(1640,530,'θ',40,ORANGE,attrs='data-theta opacity=".12"')+'</g>'
    return p


def section4_figure(n):
    if n==1:return '<div class="sequence-title-rule"></div>'
    if n==2:
        p=dna(320,130,SEQ,140,size=52)+track(MAPS[0],460,460,140,color=ORANGE)
        p+=arrow(1240,410,1390,350)+text(1330,325,'?',65,GRAY)+circle(1510,350,76,'P(B)',BLUE,42)
        return svg(p,'Position-wise detector responses need a sequence-level readout')
    if n==3:
        p=track(MAPS[0],300,300,160,'CCG',ORANGE)+arrow(1170,260,1380,260)
        p+='<g data-pool-result opacity=".12">'+circle(1510,260,56,'1',ORANGE,60)+text(1510,440,'Global max',39,ORANGE)+'</g>'
        return live('global-max',p,button('data-pool-reveal','Keep the strongest response'),'Two tied peaks; one maximum value.')
    if n==4:
        p=''
        for i in range(3):p+=f'<g data-channel="{i}" opacity="{1 if i==0 else .12}">'+maps_view([MAPS[i]],x=350,y=130+i*180,step=150,maxima=True).replace('CCG',NAMES[i]).replace(COLORS[0],COLORS[i])+'</g>'
        return live('pool-channels',p,button('data-next-channel','Next channel')+button('data-reset-channels','Reset'),'Pool over positions · keep one value per channel')
    if n==5:
        p='<g data-draw="moving-map">'+track(MAPS[0],300,300,160,'CCG',ORANGE)+'</g>'
        p+=arrow(1190,260,1370,260)+circle(1510,260,55,'1',ORANGE,56)+text(1460,430,'Pooled vector: (1, 1, 1)',37,BLUE)+text(350,500,'Other channels stay fixed',33,GRAY)
        return live('pool-limit',p,button('data-move-peak','Move first peak')+button('data-map-reset','Reset'),'The maximum retains strength; location is absent.')
    if n==6:
        p=text(864,30,'Feature values',37,GRAY)
        for i,values in enumerate(MAPS):
            p+=text(300,110+i*110,NAMES[i],38,COLORS[i],'end')
            for j,v in enumerate(values):p+=text(450+j*145,110+i*110,v,42,COLORS[i])
        p+=arrow(864,365,864,420)
        for i in range(3):p+=f'<g data-flat-channel="{i}" opacity=".12">'+ribbon(MAPS[i],x=210+i*6*65,y=490,step=65,channel_offset=i)+text(210+(i*6+2.5)*65,565,NAMES[i],29,COLORS[i])+'</g>'
        return live('flatten',p,button('data-flatten-next','Unroll next channel')+button('data-flatten-reset','Reset'),'Preserve each channel-position slot in the ordered ribbon.',600)
    if n==7:
        p='<g data-draw="position-map">'+track(MAPS[0],260,200,160,color=ORANGE)+'</g>'
        for i,w in enumerate([0,1.2,-.4,0,0,.3]):p+=text(260+i*160,325,w,35,BLUE)+line(260+i*160,355,1300,395,'#b4c7d4',3)
        p+=circle(1370,395,58,'Σ',BLUE,52)+text(1390,220,'score = 1.0',44,BLUE,attrs='data-position-score')+text(1390,530,'ReLU → 1.0',45,ORANGE,attrs='data-position-feature')
        return live('position',p,button('data-position-toggle','Move peak to position 2'),'Location-specific weights can give a different hidden feature.',600)
    if n==8:
        p=feature_glyph(170,210)+text(240,380,'Same maps',35,BLUE)
        p+=f'<path d="M350 260 Q480 140 610 140 M350 260 Q550 330 790 330" fill="none" stroke="{BLUE}" stroke-width="4"/>'
        flat=[v for row in MAPS for v in row]
        p+='<g data-branch="flat">'+ribbon(flat,660,145,45)+text(1040,65,'18 ordered values',38,BLUE)+'</g>'
        p+='<g data-branch="pool" opacity=".12">'+ribbon([1,1,1],900,335,140,per_value=True)+text(1050,420,'3 maxima',38,ORANGE)+'</g>'
        p+='<g data-branch="join" opacity=".12">'+f'<path d="M1490 145 Q1630 260 1570 430 M1250 335 Q1510 335 1570 430" fill="none" stroke="{GRAY}" stroke-width="4"/>'+ribbon(flat+[1,1,1],220,510,65)+text(864,580,'Append the values → 21 features',36,BLUE)+'</g>'
        return live('branches',p,button('data-branch-next','Reveal global max branch')+button('data-branch-reset','Reset'),'One model · shared feature maps · two readout branches',600)
    if n==9:
        p=text(270,75,'Joined features',43,BLUE)+text(950,75,'32 hidden units',43,BLUE)+text(1490,75,'One logit',43,BLUE)
        for y in [190,270,350,430,510]:
            p+=circle(270,y,16,'',GRAY)
            for y2 in [160,290,420,550]:p+=line(290,y,915,y2,'#c4d3dc',2)
        for y in [160,290,420,550]:p+=circle(950,y,32,'',BLUE)+line(985,y,1430,350,'#b5c8d5',3)
        p+=circle(1490,350,56,'z',BLUE,52)+text(900,690,'Weighted sums + biases + ReLU',44,ORANGE)
        return svg(p,'A dense hidden layer combines joined sequence features and a final weighted sum produces one logit')
    if n==10:
        p=text(250,280,'z = 0.3',52,BLUE)+arrow(380,280,550,280)+plot(600,105,780,340)
        p+=f'<circle cx="1029" cy="249.69" r="14" fill="{BLUE}"/>'+text(1490,250,'P(B) ≈ 0.574',43,ORANGE)
        p+='<g data-class-result opacity=".12">'+line(600,275,1380,275,GRAY,3,attrs='stroke-dasharray="10 10"')+text(1490,390,'cutoff 0.5',37,GRAY)+text(1550,515,'Class B',48,ORANGE)+'</g>'
        return live('probability',p,button('data-class-reveal','Apply the 0.5 cutoff'),'A logit becomes a probability; a cutoff then gives a class.')
    if n==11:return live('architecture',architecture(),button('data-route-next','Trace the route')+button('data-route-reset','Reset'),'Follow one sequence through the actual model.',600)
    if n==12:return live('learned',architecture(),button('data-learned-next','Next trainable stage')+button('data-learned-reset','Reset'),'Which operations have fitted weights and biases?',600)
    if n==13:
        p=text(450,90,'Base probabilities',48,BLUE)+text(1320,90,'Scoring weights',48,ORANGE)+text(864,320,'?',100,GRAY)
        for i,(b,probability) in enumerate(zip('ACGT',[.5,.4,.05,.05])):
            x=270+i*110;p+=line(x,420,x,420-probability*440,BLUE,35)+text(x,420-probability*440-35,probability,33,BLUE)+text(x,485,b,37,GRAY)
        p+=text(435,595,'One PPM position: sum = 1',35,BLUE)
        for i,weight in enumerate([-.4,.8,.1]):
            x=1160+i*150;p+=line(x,310,x,310-weight*160,ORANGE,35)+text(x,310-weight*160+(-35 if weight>0 else 55),weight,35,ORANGE)
        p+=line(1090,310,1550,310,GRAY,3)+text(1320,595,'A filter column need not sum to 1',34,ORANGE)+text(864,705,'What evidence would connect them?',44,GRAY)
        return svg(p,'Probability-motif entries and scoring-filter entries have different meanings; response alone does not establish biology')
    p=text(100,100,'When might location matter?',63,BLUE,'start')+text(100,195,'When should we ignore it?',63,BLUE,'start')
    p+='<g data-draw="discussion-map">'+track(MAPS[0],440,460,140,color=ORANGE)+'</g>'+circle(1510,420,50,'1',ORANGE,55)
    return live('discussion',p,button('data-discussion-move','Move the response'),'The maximum can stay the same while the ordered values change.')


CSS='''/* DAY 2 SEQUENCE SECTIONS */
.day-two-sequence .sequence-live>svg{height:560px}
.day-two-sequence .sequence-live[data-height="600"]>svg{height:600px}
.day-two-sequence .sequence-live>p{font-size:32px;line-height:1.25;min-height:45px;margin:20px 0 0;text-align:center}
.day-two-sequence .d2-controls{min-height:68px}
.day-two-sequence:has(.sequence-title-rule) h1{position:absolute;left:160px;top:370px;max-width:1540px;font-size:108px;line-height:1.12}
.sequence-title-rule{position:absolute;left:64px;top:415px;width:150px;height:6px;background:#0072B2}
.day-two-sequence [data-fade],.day-two-sequence [data-calculation]{transition:opacity .2s ease}
/* END DAY 2 SEQUENCE SECTIONS */
'''


def records(section):
    story=(ROOT/'Slides/Day_2/story.md').read_text().split(f'<a id="section-{section}"></a>')[1].split(f'<a id="section-{section+1}"></a>')[0]
    blocks=re.findall(rf'### S{section}-(\d+) · (.*?)\n(.*?)(?=\n### |\n\*\*Construction|\Z)',story,re.S)
    assert len(blocks)=={3:16,4:14}[section]
    records=[]
    for num,title,body in blocks:
        def field(name):return E(required_match(r'\*\*'+re.escape(name)+r':\*\* (.*?)(?=\n\n|\Z)',body,re.S)[1]).replace('`','')
        key=required_match(r'\*\*Proposed slide ID:\*\* `([^`]+)`',body)[1]
        records.append(dict(day=2,id=key,anchor=key,sectionSequence=True,sectionNumber=section,kind='day-two-opening day-two-sequence',title=title,time=field('Time'),body=(section3 if section==3 else section4)(int(num)),subtitle='',takeaway='',notes=field('What I want to say'),point=field('Point / reveal'),transition=field('Transition'),sourceNote=E(SOURCE3 if section==3 else SOURCE4)))
    if section==4:
        key='day-2-s4-break';records.append(dict(day=2,id=key,anchor=key,sectionSequence=True,sectionNumber=4,kind='day-two-opening day-two-sequence',title='Break',time='115–125 · 10 minutes',body=svg(text(864,350,'10 minutes',120,BLUE),'Ten-minute break'),subtitle='',takeaway='',notes='Take the full ten minutes. Return to run and inspect the actual training workflow.',point='The break is separate from teaching time.',transition='Section 5: train, inspect and compare.',sourceNote='The revised second break is 115–125, following the reviewed story.'))
    return records


def build(section):
    source=DECK.read_text();m=required_match(r'<script id="day-data" type="application/json">(.*?)</script>',source,re.S);old=json.loads(m[1])
    removed={3:['day-2-slide-5','day-2-slide-7'],4:['day-2-slide-8','day-2-slide-10']}[section]
    remaining=[s for s in old if s.get('sectionNumber')!=section and s['anchor'] not in removed]
    if section==3:
        insertion=next(i for i,s in enumerate(remaining) if s.get('sectionNumber')==4 or s['anchor'] in ['day-2-slide-8','day-2-slide-9'])
    else:
        assert any(s.get('sectionNumber')==3 for s in old),'Build Section 3 first.'
        insertion=next(i for i,s in enumerate(remaining) if s['anchor']=='day-2-slide-9' or s.get('sectionNumber')==5)
    current=remaining[:insertion]+records(section)+remaining[insertion:]
    source=source[:m.start(1)]+json.dumps(current,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')+source[m.end(1):]
    source=re.sub(r'/\* DAY 2 SEQUENCE SECTIONS \*/.*?/\* END DAY 2 SEQUENCE SECTIONS \*/\n','',source,flags=re.S)
    source=source.replace('</style>',CSS+'</style>',1)
    source=source.replace('${slide.sectionOne || slide.sectionLearning ?', '${slide.sectionOne || slide.sectionLearning || slide.sectionSequence ?')
    source=source.replace('${slide.sectionLearning ? 2 : 1}', '${slide.sectionNumber || (slide.sectionLearning ? 2 : 1)}')
    aliases=json.loads(required_match(r'const openingAliases = (\{.*?\});',source)[1])
    if any(s.get('sectionNumber')==3 for s in current):aliases.update({'#day-2-slide-5':'day-2-s3-sequence-matrix','#day-2-slide-7':'day-2-s3-move-window'})
    if any(s.get('sectionNumber')==4 for s in current):aliases.update({'#day-2-slide-8':'day-2-s4-architecture','#day-2-slide-10':'day-2-s4-break'})
    source=re.sub(r'const openingAliases = \{.*?\};','const openingAliases = '+json.dumps(aliases)+';',source)
    source=re.sub(r'<script id="day-two-sequence-interactions">.*?</script>\n?','',source,flags=re.S)
    js=(ROOT/'tools/day2_sequence_interactions.js').read_text()
    source=source.replace('<script id="presentation-controller">','<script id="day-two-sequence-interactions">\n'+js+'\n</script>\n<script id="presentation-controller">',1)
    if 'bindDayTwoSequence();' not in source:source=source.replace('bindDayTwoLearning();','bindDayTwoLearning();\nbindDayTwoSequence();')
    DECK.write_text(source);print(f'Built Section {section}: {len(records(section))} scenes; {len(current)} total.')


if __name__=='__main__':build(int(sys.argv[1]))
