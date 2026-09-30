import base64
W,H=2100,2970
BLUE,RED,GOLD,GREY="#0B2A6F","#B3202A","#B08D3C","#8A93AD"
b64=lambda f:"data:image/png;base64,"+base64.b64encode(open(f,"rb").read()).decode()
LOGO=b64("logo_unacita.png")

# ---------- silhouettes (origine = pieds, hauteur ~1000)
def line(x1,y1,x2,y2,w): return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke-width="{w}" stroke-linecap="round" stroke="{BLUE}"/>'
def legs(): return line(-24,-500,-28,-26,46)+line(24,-500,28,-26,46)+'<path d="M-62,-30 q36,-14 70,0 l2,30 h-74z M-8,-30 q36,-14 70,0 l2,30 h-74z"/>'
def torso(): return '<path d="M-90,-862 Q0,-896 90,-862 L74,-498 Q0,-470 -74,-498Z"/><rect x="-15" y="-884" width="30" height="34"/><path d="M-12,-860 L0,-800 L12,-860Z" fill="#fff" opacity=".5"/>'
def head(t=0): return f'<circle cx="0" cy="-935" r="38"/><ellipse cx="10" cy="-968" rx="58" ry="20" transform="rotate({-8+t} 0 -960)"/><circle cx="-36" cy="-982" r="6"/>'
def arm_down(s): return line(s*94,-846,s*102,-536,30)+f'<circle cx="{s*102}" cy="-522" r="16"/>'
def standing(): return legs()+torso()+arm_down(-1)+arm_down(1)+head()
def saluting(): return legs()+torso()+arm_down(-1)+line(86,-846,156,-748,30)+line(156,-748,60,-930,28)+head(-4)
def bearer(): return legs()+torso()+arm_down(-1)+line(86,-846,120,-716,30)+f'<circle cx="122" cy="-712" r="17"/>'+head(2)+'<rect x="118" y="-1262" width="8" height="1262"/><circle cx="122" cy="-1274" r="13"/>'
def flag():
    shape="M126,-1235 C220,-1262 320,-1200 480,-1235 L480,-985 C320,-950 220,-1010 126,-985Z"
    return f'''<clipPath id="fl"><path d="{shape}"/></clipPath>
<g clip-path="url(#fl)"><rect x="126" y="-1290" width="118" height="340" fill="{BLUE}"/><rect x="244" y="-1290" width="118" height="340" fill="#fff"/><rect x="362" y="-1290" width="122" height="340" fill="{RED}"/>
<image href="{LOGO}" x="232" y="-1180" width="140" height="140" preserveAspectRatio="xMidYMid meet"/></g>
<path d="{shape}" fill="none" stroke="{GOLD}" stroke-width="5"/>'''

def watermark():
    fig=lambda x,s,body:f'<g transform="translate({x} 0) scale({s},1)">{body}</g>'
    g=f'<g fill="{BLUE}" opacity="0.11">{fig(-330,1,standing())}{fig(640,-1,saluting())}{fig(0,1,bearer())}</g>'
    g+=f'<g opacity="0.24">{flag()}</g>'
    return f'<g transform="translate(880 2330) scale(1.3)">{g}</g>'

# ---------- cadre tricolore tout autour
def frame(m=20,w=16):
    s=""
    for i,(c,stroke) in enumerate(((BLUE,None),("#fff",GREY),(RED,None))):
        o=m+i*w; x=o+w/2
        s+=f'<rect x="{x}" y="{x}" width="{W-2*x}" height="{H-2*x}" fill="none" stroke="{c}" stroke-width="{w}"/>'
        if stroke:
            for oo in (o,o+w): s+=f'<rect x="{oo}" y="{oo}" width="{W-2*oo}" height="{H-2*oo}" fill="none" stroke="{stroke}" stroke-width="2"/>'
    o=m+3*w+10
    s+=f'<rect x="{o}" y="{o}" width="{W-2*o}" height="{H-2*o}" fill="none" stroke="{GOLD}" stroke-width="3"/>'
    return s

svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}"><rect width="{W}" height="{H}" fill="#fff"/>{watermark()}{frame()}</svg>'
open("decor_unacita_cadre_A4.svg","w").write(svg)
