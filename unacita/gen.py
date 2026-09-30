import math
W,H=2100,2970
BLUE,RED,GOLD,GREEN="#0B2A6F","#B3202A","#B08D3C","#3E5B2E"
def branch(x,y,ang,n=9,L=34,flip=1):
    s=""
    for i in range(n):
        t=i/ (n-1)
        a=math.radians(ang+flip*(i*9))
        cx=x+math.cos(a)*i*L; cy=y+math.sin(a)*i*L
        for side in (-1,1):
            la=math.degrees(a)+side*55
            s+=f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{20-6*t:.1f}" ry="{7-2*t:.1f}" transform="rotate({la:.1f} {cx:.1f} {cy:.1f}) translate({14:.0f} 0)" fill="{GREEN}"/>'
    s+=f'<path d="M{x},{y} '+" ".join(f"L{x+math.cos(math.radians(ang+flip*i*9))*i*34:.1f},{y+math.sin(math.radians(ang+flip*i*9))*i*34:.1f}" for i in range(n))+f'" stroke="{GREEN}" stroke-width="4" fill="none"/>'
    return s
def laurier(cx,cy,ang_l,ang_r):
    return branch(cx,cy,ang_l,flip=-1)+branch(cx,cy,ang_r,flip=1)

def wreath(cx,cy,r=170,up=True):
    out=""
    for side in (-1,1):
        for i in range(14):
            t=i/13
            a=math.radians(90+side*(15+t*150)) if up else math.radians(-90-side*(15+t*150))
            x=cx+r*math.cos(a); y=cy+r*math.sin(a)
            tang=math.degrees(a)+90*side*(-1 if up else 1)
            for k,off in ((0,-28),(1,28)):
                out+=f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="26" ry="9" transform="rotate({tang+off:.1f} {x:.1f} {y:.1f}) translate(18 0)" fill="{GREEN}"/>'
    return out
def corner(x,y,r):
    return f'<g transform="translate({x} {y}) rotate({r})"><path d="M0,0 H230 M0,0 V230" stroke="{GOLD}" stroke-width="10"/><path d="M40,40 H190 M40,40 V190" stroke="{GOLD}" stroke-width="4"/><circle cx="40" cy="40" r="16" fill="{BLUE}" stroke="{GOLD}" stroke-width="5"/><path d="M40,28 L44,38 L55,38 L46,44 L50,55 L40,48 L30,55 L34,44 L25,38 L36,38Z" fill="#fff"/></g>'
m=90
svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="2100" height="2970"><rect width="{W}" height="{H}" fill="#fff"/>'
svg+=f'<rect x="{m}" y="{m}" width="{W-2*m}" height="{H-2*m}" fill="none" stroke="{GOLD}" stroke-width="10"/>'
svg+=f'<rect x="{m+30}" y="{m+30}" width="{W-2*m-60}" height="{H-2*m-60}" fill="none" stroke="{GOLD}" stroke-width="3"/>'
# bande tricolore haut et bas
bw=(W-2*m-120)/3
for yy in (m+60,H-m-80):
    for i,c in enumerate((BLUE,"#fff",RED)):
        svg+=f'<rect x="{m+60+i*bw:.0f}" y="{yy}" width="{bw:.0f}" height="20" fill="{c}" stroke="{BLUE if c=="#fff" else c}" stroke-width="1"/>'
svg+=corner(m+10,m+10,0)+corner(W-m-10,m+10,90)+corner(W-m-10,H-m-10,180)+corner(m+10,H-m-10,270)
# lauriers haut (zone logo) et bas
svg+=wreath(W/2,430,170,True)
svg+=f''
svg+='</svg>'
open("decor_unacita_cadre_A4.svg","w").write(svg)
