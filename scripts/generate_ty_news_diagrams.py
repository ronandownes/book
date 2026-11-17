#!/usr/bin/env python3
"""Reproduce the original, labelled diagrams used in the TY classroom story."""
from pathlib import Path
from html import escape
from math import sqrt, sin, cos, pi
import re

OUT = Path('assets/ty-news')
OUT.mkdir(parents=True, exist_ok=True)
INK, PURPLE, BLUE, GREEN, RED = '#202b3d', '#51458c', '#146f9a', '#20794d', '#bd343c'

def label(x,y,s,size=28,fill=INK,anchor='middle',weight=500):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" font-weight="{weight}" fill="{fill}">{escape(str(s))}</text>'

def rect(x,y,w,h,fill='#eef0f7',stroke='none',r=16):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}"/>'

def line(x,y,X,Y,color=BLUE,width=5,dash=''):
    return f'<line x1="{x}" y1="{y}" x2="{X}" y2="{Y}" stroke="{color}" stroke-width="{width}" stroke-dasharray="{dash}" stroke-linecap="round"/>'

def dot(x,y,r=10,fill=INK):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}"/>'

def save(name,title,body,w=1000,h=620):
    text=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title"><title id="title">{escape(title)}</title><rect width="100%" height="100%" rx="22" fill="#f7f6fb"/><g font-family="Arial, sans-serif">{body}</g></svg>'
    (OUT/name).write_text(text,encoding='utf-8')

# A concise visual route through the story.
b=label(500,72,'CAN A COMPUTER SURPRISE US?',38,PURPLE,weight=700)
for x,year,name,symbol in [(170,'1997','Chess','♞'),(500,'2016','Go','●'),(830,'2026','Mathematics','?')]:
    b+=rect(x-130,120,260,320,'white','#d7d2e7')
    b+=label(x,255,symbol,110,PURPLE)+label(x,335,year,42,BLUE,weight=700)+label(x,395,name,28)
b+=label(500,525,'A win. A surprising move. A new proof.',30)
save('story-route.svg','Chess, Go and mathematics: three stages of the story',b)

# Scores are points, not numbers of games won.
b=label(500,65,'THE 1997 REMATCH',38,PURPLE,weight=700)
for i,(top,bottom) in enumerate(zip(['1','0','½','½','½','0'],['0','1','½','½','½','1'])):
    x=260+i*105
    b+=label(x,150,i+1,24)+rect(x-40,178,80,88,'#e3eaf6')+rect(x-40,295,80,88,'#e8e3f4')
    b+=label(x,238,top,42,BLUE,weight=700)+label(x,356,bottom,42,PURPLE,weight=700)
b+=label(70,150,'Game',25,anchor='start')+label(60,235,'Kasparov',28,anchor='start')+label(60,352,'Deep Blue',28,anchor='start')
b+=label(500,455,'Kasparov 2½ — Deep Blue 3½',38,PURPLE,weight=700)
b+=label(500,520,'A win = 1 point. A draw = ½ point each.',27)
save('chess-rematch.svg','The six games of the 1997 match: Deep Blue wins by three and a half points to two and a half',b)

# Capture lesson, deliberately separate from the historical match positions.
b=label(500,65,'STONES GO ON INTERSECTIONS',35,PURPLE,weight=700)
for origin,after in [(80,False),(565,True)]:
    b+=rect(origin,115,355,355,'#e9c997')
    for k in range(7):
        q=origin+35+k*47.5;y=150+k*47.5
        b+=line(q,150,q,435,INK,1.4)+line(origin+35,y,origin+320,y,INK,1.4)
    cx,cy=origin+177.5,292.5
    for dx,dy in [(-1,0),(1,0),(0,-1)]+([(0,1)] if after else []):b+=dot(cx+dx*47.5,cy+dy*47.5,19)
    if not after:
        b+=f'<circle cx="{cx}" cy="{cy}" r="19" fill="white" stroke="{INK}" stroke-width="2"/>'
        b+=f'<circle cx="{cx}" cy="{cy+47.5}" r="20" fill="none" stroke="{RED}" stroke-width="4"/>'
    b+=label(origin+177.5,525,'White has one liberty' if not after else 'Black fills it: white is captured',24)
b+=label(500,590,'Teaching diagram on a small board; the match used 19 × 19 lines.',21)
save('go-capture.svg','A Go capture: fill the last liberty and remove the surrounded white stone',b)

def moves_from_sgf(path):
    content=path.read_text()
    assert content.count('(')==content.count(')')==1, 'Only a single main line is accepted'
    return [(c,(ord(p[0])-97,ord(p[1])-97) if p else None) for c,p in re.findall(r';([BW])\[([a-s]{2})?\]',content)]

def position(moves,through):
    board={}
    def neighbors(p):
        x,y=p
        return [(X,Y) for X,Y in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)] if 0<=X<19 and 0<=Y<19]
    def group(p):
        color=board[p]; seen={p};todo=[p]
        while todo:
            for q in neighbors(todo.pop()):
                if q not in seen and board.get(q)==color:seen.add(q);todo.append(q)
        return seen
    for color,p in moves[:through]:
        if p is None:continue
        assert p not in board
        board[p]=color
        for q in neighbors(p):
            if q in board and board[q]!=color:
                g=group(q)
                if not any(t not in board for s in g for t in neighbors(s)):
                    for t in g:del board[t]
    return board

for game,move,name in [(2,37,'AlphaGo'),(4,78,'Lee Sedol')]:
    moves=moves_from_sgf(OUT/f'game-{game}.sgf');board=position(moves,move);color,p=moves[move-1]
    cols='ABCDEFGHJKLMNOPQRST';coord=cols[p[0]]+str(19-p[1])
    assert (game,coord,color) in [(2,'P10','B'),(4,'L11','W')]
    b=label(325,42,f'{name} · move {move} · {coord}',25,PURPLE,weight=700)
    b+=rect(35,65,580,555,'#e9c997')
    for k in range(19):
        q=70+k*28
        b+=line(q,90,q,594,INK,1)+line(70,q+20,574,q+20,INK,1)
        b+=label(q,80,cols[k],12)+label(50,q+25,19-k,12)
    for x in [3,9,15]:
        for y in [3,9,15]:b+=dot(70+x*28,90+y*28,3.2)
    for (x,y),c in board.items():
        b+=f'<circle cx="{70+x*28}" cy="{90+y*28}" r="12.5" fill="{INK if c=="B" else "white"}" stroke="{INK}" stroke-width="1.1"/>'
    x,y=70+p[0]*28,90+p[1]*28
    b+=f'<circle cx="{x}" cy="{y}" r="18" fill="none" stroke="{RED}" stroke-width="4"/>'
    b+=label(x,y+4,move,10,'white' if color=='B' else INK,weight=700)
    save(f'go-move-{move}.svg',f'Actual game {game} position after move {move}, highlighted at {coord}',b,650,650)
    print(f'Game {game}: move {move} is {color} at {coord}; {len(board)} stones on the board.')

b=label(500,65,'SEOUL, MARCH 2016',38,PURPLE,weight=700)
for i,winner in enumerate(['AlphaGo','AlphaGo','AlphaGo','Lee Sedol','AlphaGo']):
    x=100+i*195;b+=rect(x-80,150,160,235,'#e7e3f4' if winner=='AlphaGo' else '#dff0e4')
    b+=label(x,210,f'Game {i+1}',24)+label(x,292,'●' if winner=='AlphaGo' else '○',65,PURPLE if winner=='AlphaGo' else GREEN)+label(x,355,winner,25)
b+=label(500,485,'AlphaGo 4 — Lee Sedol 1',44,PURPLE,weight=700)+label(500,555,'Game 4 is the human response at the heart of the story.',25)
save('go-match.svg','The five match winners, with Lee Sedol winning game four',b)

b=label(500,62,'ALPHAZERO AGAINST STOCKFISH',35,PURPLE,weight=700)
b+=label(500,115,'The 1,000-game evaluation reported in 2018',26)
start=60;width=880
for count,color in [(155,BLUE),(839,'#bfc9d9'),(6,RED)]:
    extent=width*count/1000;b+=rect(start,165,extent,85,color,r=0);start+=extent
for x,n,s,c in [(190,'155','AlphaZero wins',BLUE),(505,'839','Draws',INK),(810,'6','Stockfish wins',RED)]:
    b+=label(x,330,n,62,c,weight=700)+label(x,375,s,24,c)
for x,s in [(175,'Play itself'),(500,'Learn from results'),(825,'Test against a rival')]:
    b+=rect(x-145,450,290,80,'#e8e3f4')+label(x,500,s,23,PURPLE)
b+=label(500,585,'Historical test conditions; this is not a ranking of today’s engines.',20)
save('alphazero-stockfish.svg','An exact proportional bar: 155 AlphaZero wins, 839 draws and 6 Stockfish wins',b)

# Four points: a square gives four unit pairs; two equilateral triangles give five.
b=label(500,62,'FOUR POINTS. CAN WE MAKE MORE UNIT PAIRS?',31,PURPLE,weight=700)
for pts,offset in [([(0,0),(1,0),(0,1),(1,1)],70), ([(0,0),(1,0),(.5,sqrt(3)/2),(1.5,sqrt(3)/2)],550)]:
    xy=[(offset+180*x,420-180*y) for x,y in pts];count=0
    for i in range(4):
        for j in range(i):
            a,c=pts[i],pts[j]
            if abs((a[0]-c[0])**2+(a[1]-c[1])**2-1)<1e-9:
                b+=line(*xy[i],*xy[j],BLUE,6);count+=1
    for x,y in xy:b+=dot(x,y,12)
    b+=label(offset+145,180,f'{count} unit pairs',38,BLUE,weight=700)
b+=label(500,535,'Only blue links are exactly one unit long.',27)
b+=label(500,583,'All four points stay on the same flat plane.',25)
save('unit-pairs.svg','A unit square has four unit-distance pairs; a rhombus of two equilateral triangles has five',b)

b=label(500,62,'THE CUBE: WHICH DISTANCES ARE 1?',34,PURPLE,weight=700)
front=[(235,220),(495,220),(495,480),(235,480)];back=[(x+150,y-100) for x,y in front]
for v in [front,back]:
    for i in range(4):b+=line(*v[i],*v[(i+1)%4],BLUE,6)
for a,c in zip(front,back):b+=line(*a,*c,BLUE,6)
b+=line(*front[3],*front[1],'#d28a19',5,'9 7')+line(*front[3],*back[1],RED,5,'5 7')
for x,y in front+back:b+=dot(x,y,9)
b+=label(500,540,'12 edges: 1     face diagonal: √2     body diagonal: √3',25)
b+=label(500,590,'A 3D example. The Erdős question keeps every point in a plane.',24,PURPLE)
save('cube-distances.svg','A cube has twelve unit edges, face diagonals of square root two, and body diagonals of square root three',b)

b=label(500,65,'WHAT FAILED WAS A CONJECTURE',36,PURPLE,weight=700)
for x,y,title,detail,fill in [(60,130,'The expectation','Grid-based arrangements were essentially best.','#eeeaf6'),(520,130,'A new construction','A different family beats the predicted growth.','#dfeefa'),(60,345,'Human checking','Mathematicians checked and explained the proof.','#e2f0e7'),(520,345,'The conclusion','The old conjecture is false.','#fde9e7')]:
    b+=rect(x,y,420,170,fill)+label(x+210,y+55,title,29,PURPLE,weight=700)
    words=detail.split();half=len(words)//2
    b+=label(x+210,y+103,' '.join(words[:half]),21)+label(x+210,y+134,' '.join(words[half:]),21)
b+=label(500,583,'20 May 2026 · this is not the cube construction',23)
save('unit-distance-result.svg','The expectation, construction, independent checking and counterexample of May 2026',b)

b=label(500,68,'A MODEL CAN BREAK DOWN',36,PURPLE,weight=700)
for k in range(6):b+=line(70,175+k*45,360,175+k*45,BLUE,4)
for k in range(5):
    points=[]
    for i in range(220):
        t=i/219*4*pi;r=160*(1-i/240);points.append((700+r*cos(t+k*.12),315+r*sin(t+k*.12)))
    b+='<polyline points="'+' '.join(f'{x:.1f},{y:.1f}' for x,y in points)+'" fill="none" stroke="'+BLUE+'" stroke-width="3"/>'
b+=label(210,510,'Smooth starting flow',28)+label(715,510,'Could the equations break down?',27)
b+=label(500,584,'Illustration, not a fluid simulation or the claimed proof.',22)
save('fluid-question.svg','A schematic flow and a spiral illustrate the question about mathematical breakdown',b)

b=label(500,65,'722 MANUSCRIPTS',46,PURPLE,weight=700)
for row in range(19):
    for col in range(38):b+=rect(64+col*23,110+row*20,17,15,'#627ca9',r=2)
b+=label(500,545,'38 columns × 19 rows = 722 papers',29,BLUE,weight=700)
b+=label(500,592,'The original release, 6 October 2026',24)
save('722-manuscripts.svg','Exactly 722 small manuscript symbols in 38 columns and 19 rows',b)

b=label(500,65,'A MISTAKE CAN AFFECT OTHER PAPERS',33,PURPLE,weight=700)
b+=rect(300,120,400,125,'#fde9e7')+label(500,175,'One paper contains a sign error',27,RED)+label(500,215,'Its argument fails',23)
for x in [250,750]:
    b+=line(500,250,x,335,RED,5)+rect(x-180,345,360,120,'#eeeaf6')
    b+=label(x,395,'Another paper uses it',25,PURPLE)+label(x,435,'This must be rechecked',23)
b+=label(500,550,'7 October: three manuscripts withdrawn',30,RED,weight=700)
save('proof-dependencies.svg','A sign error in one paper affects two papers depending on it; all three are withdrawn',b)

b=label(500,70,'OUR INVESTIGATION',40,PURPLE,weight=700)
for x,y,s,detail in [(60,140,'1. Ask','What exactly is the claim?'),(520,140,'2. Test','Can another student repeat my checks?'),(60,350,'3. Explain','Why does the pattern happen?'),(520,350,'4. Be precise','What have I actually established?')]:
    b+=rect(x,y,420,165,'white','#d7d2e7')+label(x+210,y+60,s,34,PURPLE,weight=700)
    words=detail.split();half=len(words)//2
    b+=label(x+210,y+108,' '.join(words[:half]),23)+label(x+210,y+139,' '.join(words[half:]),23)
save('our-investigation.svg','Ask, test, explain and state a precise conclusion',b)
print('Original diagrams regenerated. Unit-pair counts, Go coordinates and 722 symbols checked.')
