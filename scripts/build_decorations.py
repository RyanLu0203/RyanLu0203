"""Build self-contained SVG decorations. No runtime services or JavaScript."""
from pathlib import Path
from html import escape
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
FONT = '-apple-system,BlinkMacSystemFont,Segoe UI,PingFang SC,Microsoft YaHei,sans-serif'
MONO = 'ui-monospace,SFMono-Regular,Consolas,monospace'
THEMES = {
    'light': dict(bg='#f8fbf9', ink='#102d43', muted='#526c7b', border='#cfe5e2', panel='#ffffff', dot='#0f766e'),
    'dark': dict(bg='#0d1827', ink='#e5f2f7', muted='#98b5c4', border='#254551', panel='#142537', dot='#5eead4'),
}
ICONS = {
    'agri': '<path d="M12 25C10 10 20 4 32 5C33 17 26 28 12 25ZM12 25L27 11M12 25L9 32"/>',
    'risk': '<path d="M20 4L33 10V20C33 28 26 32 20 36C14 32 7 28 7 20V10Z"/><path d="M13 19L18 24L27 14"/>',
    'quant': '<path d="M6 5V33H35M11 26L18 18L25 22L34 9M27 9H34V16"/>',
    'workflow': '<rect x="4" y="4" width="10" height="10" rx="3"/><rect x="26" y="4" width="10" height="10" rx="3"/><rect x="15" y="27" width="10" height="10" rx="3"/><path d="M14 9H26M31 14V20H20V27M9 14V20H20"/>',
}
ACCENTS = {'agri':'#2f9472', 'risk':'#398ad7', 'quant':'#b17a25', 'workflow':'#9270cc'}

def icon(kind, x, y, scale=1, color=None):
    return f'<g transform="translate({x} {y}) scale({scale})" fill="none" stroke="{color or ACCENTS[kind]}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{ICONS[kind]}</g>'

def svg(w, h, title, body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img"><title>{escape(title)}</title>{body}</svg>\n'

def write(name, content):
    ET.fromstring(content)
    (ASSETS/name).write_text(content, encoding='utf-8')

def hero(theme):
    t=THEMES[theme]
    body=f'''<defs>
      <linearGradient id="wash" x2="1" y2="1"><stop stop-color="{t['bg']}"/><stop offset=".6" stop-color="{t['bg']}"/><stop offset="1" stop-color="{'#e3f7f0' if theme=='light' else '#113c42'}"/></linearGradient>
      <linearGradient id="line"><stop stop-color="#64b3bc"/><stop offset=".55" stop-color="#6e83d1"/><stop offset="1" stop-color="#41bea8"/></linearGradient>
      <radialGradient id="glow"><stop stop-color="#6ac7be" stop-opacity=".22"/><stop offset="1" stop-color="#6ac7be" stop-opacity="0"/></radialGradient>
      <pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1" fill="{t['dot']}" opacity=".12"/></pattern>
    </defs>
    <style>
      .orbit{{transform-box:fill-box;transform-origin:center;animation:orbit 30s linear infinite}}
      .float{{animation:float 6s ease-in-out infinite}}.dash{{animation:dash 18s linear infinite}}
      @keyframes orbit{{to{{transform:rotate(360deg)}}}}@keyframes float{{50%{{transform:translateY(-8px)}}}}@keyframes dash{{to{{stroke-dashoffset:-600}}}}
      @media(prefers-reduced-motion:reduce){{.orbit,.float,.dash{{animation:none}}.moving{{display:none}}}}
    </style>
    <rect x="1" y="1" width="1198" height="388" rx="28" fill="url(#wash)" stroke="{t['border']}"/>
    <rect x="630" y="18" width="550" height="354" rx="24" fill="url(#grid)"/>
    <circle cx="940" cy="190" r="280" fill="url(#glow)"/>
    <path d="M28 1H1172Q1199 1 1199 28V362Q1199 389 1172 389H28Q1 389 1 362V28Q1 1 28 1Z" fill="none" stroke="url(#line)" stroke-width="2" stroke-dasharray="120 480" opacity=".8" class="dash"/>
    <g font-family="{FONT}">
      <text x="58" y="57" fill="{t['muted']}" font-size="14" letter-spacing="3">@RYANLU0203 / BUILD &amp; RESEARCH</text>
      <text x="53" y="164" fill="{t['ink']}" font-size="88" font-weight="800" letter-spacing="-4">LU XINYU</text>
      <text x="60" y="208" fill="{t['muted']}" font-size="19" letter-spacing="1.2">From business questions to working systems.</text>
    </g>'''
    for kind,label,x,y in [('agri','AGRICULTURE',60,241),('risk','RISK & SECURITY',326,241),('quant','QUANT SYSTEMS',60,299),('workflow','WORKFLOW RESEARCH',326,299)]:
        body+=f'<rect x="{x}" y="{y}" width="246" height="43" rx="13" fill="{t["panel"]}" stroke="{t["border"]}"/>'
        body+=icon(kind,x+12,y+8,.66)
        body+=f'<text x="{x+46}" y="{y+27}" font-family="{MONO}" font-size="13" font-weight="600" fill="{t["ink"]}">{escape(label)}</text>'
    body+=f'''<g stroke="url(#line)" fill="none">
      <ellipse cx="930" cy="205" rx="213" ry="119" transform="rotate(-29 930 205)" opacity=".5"/>
      <ellipse cx="930" cy="205" rx="205" ry="146" transform="rotate(30 930 205)" stroke-dasharray="4 8" opacity=".5"/>
      <circle cx="930" cy="205" r="102" opacity=".23"/><circle cx="930" cy="205" r="157" opacity=".13"/>
      <path d="M674 310C760 310 740 110 838 112S1006 338 1060 290S1120 102 1172 91" stroke-width="2" opacity=".5"/>
      <path d="M674 336C770 336 830 275 862 199S967 78 1040 107S1122 264 1176 273" opacity=".35"/>
    </g>
    <g class="orbit"><circle cx="930" cy="48" r="4" fill="#6e83d1"/><circle cx="930" cy="362" r="3" fill="#41bea8"/></g>
    <circle cx="930" cy="205" r="68" fill="{t['panel']}" stroke="{t['border']}" stroke-width="2"/>
    <text x="930" y="218" text-anchor="middle" font-family="{MONO}" font-size="42" font-weight="700" fill="{t['dot']}">&lt;/&gt;</text>'''
    for i,(kind,x,y) in enumerate([('agri',830,102),('risk',1090,155),('quant',1043,306),('workflow',775,282)]):
        body+=f'<g class="float" style="animation-delay:-{i*1.4}s"><circle cx="{x}" cy="{y}" r="29" fill="{t["panel"]}" stroke="{t["border"]}" stroke-width="1.5"/>{icon(kind,x-17,y-17,.85)}</g>'
    for i in range(3):
        body+=f'<circle class="moving" r="{4-i*.6}" fill="{["#0f9d92","#7190df","#4ec4a4"][i]}" opacity=".85"><animateMotion dur="{7+i*2}s" repeatCount="indefinite" path="M674 310C760 310 740 110 838 112S1006 338 1060 290S1120 102 1172 91" begin="-{i*3}s"/></circle>'
    body+=f'<text x="1170" y="365" text-anchor="end" font-family="{MONO}" font-size="11" letter-spacing="2" fill="{t["muted"]}">DESIGN / CODE / VALIDATE / ITERATE</text>'
    return svg(1200,390,'Lu Xinyu — agricultural software, financial risk and security, quant systems, workflow research',body)

def typing():
    lines=['Exploring agricultural software & decision tools', 'Building financial risk & security platforms', 'Developing quant research & equity systems', 'Connecting tools, knowledge & reusable workflows']
    body=f'''<defs><clipPath id="type"><rect x="0" y="0" width="1000" height="52"><animate attributeName="width" values="0;1000;1000;0" keyTimes="0;.52;.9;1" dur="5s" repeatCount="indefinite"/></rect></clipPath></defs>
    <rect x="1" y="1" width="1198" height="126" rx="18" fill="#112c3c" stroke="#285163"/>
    <circle cx="27" cy="24" r="5" fill="#ff8b86"/><circle cx="46" cy="24" r="5" fill="#f4cb6a"/><circle cx="65" cy="24" r="5" fill="#70d5b5"/>
    <text x="95" y="29" font-family="{MONO}" font-size="13" fill="#91b3c6">ryan@lab:~ / focus</text>
    <text x="32" y="87" font-family="{MONO}" font-size="28" fill="#6ee7cc">❯</text>
    <g transform="translate(66 51)"><g clip-path="url(#type)">'''
    for i,line in enumerate(lines):
        if i==0: times='0;.24;.25;1'; vals='1;1;0;0'
        elif i==3: times='0;.75;.751;.999;1'; vals='0;0;1;1;0'
        else:
            s=i/4;e=(i+1)/4
            times=f'0;{s};{s+.001};{e-.01};{e};1'; vals='0;0;1;1;0;0'
        body+=f'<text x="0" y="36" opacity="{1 if i==0 else 0}" font-family="{MONO}" font-size="27" fill="#d9f6f1">{escape(line)}<animate attributeName="opacity" values="{vals}" keyTimes="{times}" dur="20s" repeatCount="indefinite"/></text>'
    body+='</g><rect x="0" y="8" width="3" height="34" fill="#6ee7cc"><animate attributeName="x" values="0;1000;1000;0" keyTimes="0;.52;.9;1" dur="5s" repeatCount="indefinite"/><animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/></rect></g>'
    return svg(1200,128,'Rotating typed introduction for four research and development interests',body)

def divider():
    body='<defs><linearGradient id="d"><stop stop-color="#54bfad" stop-opacity="0"/><stop offset=".35" stop-color="#54bfad"/><stop offset=".65" stop-color="#7889d1"/><stop offset="1" stop-color="#7889d1" stop-opacity="0"/></linearGradient></defs>'
    for i in range(3):
        body+=f'<path d="M0 {22+i*4}Q150 {i*2} 300 {22+i*4}T600 {22+i*4}T900 {22+i*4}T1200 {22+i*4}" fill="none" stroke="url(#d)" stroke-width="{2-i*.5}" opacity="{.8-i*.22}"><animate attributeName="d" values="M0 {22+i*4}Q150 {i*2} 300 {22+i*4}T600 {22+i*4}T900 {22+i*4}T1200 {22+i*4};M0 {22+i*4}Q150 {44-i*2} 300 {22+i*4}T600 {22+i*4}T900 {22+i*4}T1200 {22+i*4};M0 {22+i*4}Q150 {i*2} 300 {22+i*4}T600 {22+i*4}T900 {22+i*4}T1200 {22+i*4}" dur="{7+i}s" repeatCount="indefinite"/></path>'
    return svg(1200,50,'Flowing teal and lavender divider',body)

def card(kind,index,title,subtitle,status,theme):
    t=THEMES[theme];a=ACCENTS[kind]
    body=f'''<defs><linearGradient id="card"><stop stop-color="{a}" stop-opacity=".14"/><stop offset="1" stop-color="{a}" stop-opacity=".02"/></linearGradient></defs>
    <rect x="1" y="1" width="558" height="188" rx="20" fill="{t['panel']}" stroke="{t['border']}"/>
    <rect x="1" y="1" width="558" height="188" rx="20" fill="url(#card)"/>
    <text x="529" y="51" text-anchor="end" font-family="{MONO}" font-size="36" font-weight="700" fill="{a}" opacity=".18">{index:02}</text>
    <rect x="25" y="24" width="48" height="48" rx="14" fill="{a}" opacity=".12"/>{icon(kind,29,28,1)}
    <g font-family="{FONT}"><text x="89" y="52" font-size="21" font-weight="700" fill="{t['ink']}">{escape(title)}</text>
    <text x="27" y="107" font-size="20" font-weight="600" fill="{t['ink']}">{escape(subtitle)}</text>
    <text x="27" y="155" font-size="12" letter-spacing="1.2" fill="{a}">{escape(status)}</text>
    <text x="527" y="157" text-anchor="end" font-size="23" fill="{a}">↗</text></g>'''
    return svg(560,190,f'{title} — {subtitle} — {status}',body)

def main():
    ASSETS.mkdir(exist_ok=True)
    for theme in THEMES:
        write(f'hero-{theme}.svg',hero(theme))
        for item in [('agri',1,'农业软件需求开发','作物排序与土地配置研究','SCIENTIFIC DRAFT / OPTIMIZATION'),('risk',2,'金融风控与安全平台','A 股盘前研究工作台','READ-ONLY RESEARCH / GOVERNANCE'),('quant',3,'量化与股票系统','金融新闻 × DQN 交易研究','COURSE TEAM PROJECT / EXPERIMENTS'),('workflow',4,'工作流研究','Obsidian / Codex 笔记流程','REUSABLE SKILL / KNOWLEDGE')]:
            write(f'project-{item[0]}-{theme}.svg',card(*item,theme))
    write('typing.svg',typing())
    write('divider.svg',divider())
    for kind,label in [('agri','AGRI SOFTWARE'),('risk','RISK & SECURITY'),('quant','QUANT SYSTEMS'),('workflow','WORKFLOW RESEARCH')]:
        color=ACCENTS[kind]
        body=f'<rect x="1" y="1" width="228" height="40" rx="20" fill="{color}"/>{icon(kind,12,8,.64,"#ffffff")}<text x="45" y="26" fill="#ffffff" font-family="{MONO}" font-size="12" font-weight="600">{escape(label)}</text>'
        write(f'badge-{kind}.svg',svg(230,42,label,body))
    print('Built 16 SVG decorations.')

if __name__=='__main__': main()
