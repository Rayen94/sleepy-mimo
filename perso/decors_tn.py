"""Décors tunisiens (repère 1920x1080, sol des personnages à y = 930).
sidibou, sidibou_soir, cafe, plage, fac, medina, toit_nuit, maison."""
import math, random
from functools import lru_cache

GROUND = 930


def _g(gid, stops, x2=0, y2=1):
    s = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
    return f'<linearGradient id="{gid}" x1="0" y1="0" x2="{x2}" y2="{y2}">{s}</linearGradient>'


def _cloud(x, y, s, op=0.9, col="#FFFFFF"):
    return (f'<g transform="translate({x:.0f} {y:.0f}) scale({s:.2f})" fill="{col}" opacity="{op}">'
            '<circle cx="-60" cy="0" r="40"/><circle cx="0" cy="-22" r="55"/><circle cx="60" cy="0" r="42"/>'
            '<rect x="-100" y="0" width="200" height="40" rx="20"/></g>')


def _door(x, y, w, h, col="#1E6FB8"):
    """Porte bleue de Sidi Bou Saïd, en arc, avec clous noirs."""
    r = w / 2
    studs = "".join(f'<circle cx="{x + w*0.25 + (i%2)*w*0.5:.0f}" cy="{y + r + 30 + (i//2)*40:.0f}" r="5" fill="#0D2A4A"/>' for i in range(int((h - r - 40) // 40) * 2))
    return (f'<path d="M{x-12} {y+h} L{x-12} {y+r} A{r+12} {r+12} 0 0 1 {x+w+12} {y+r} L{x+w+12} {y+h}Z" fill="#F2D49A"/>'
            f'<path d="M{x} {y+h} L{x} {y+r} A{r} {r} 0 0 1 {x+w} {y+r} L{x+w} {y+h}Z" fill="{col}"/>'
            f'<path d="M{x+w/2} {y+6} L{x+w/2} {y+h}" stroke="#14548E" stroke-width="5"/>' + studs)


def _window(x, y, w, h):
    bars = "".join(f'<path d="M{x+i*w/5:.0f} {y+10} L{x+i*w/5:.0f} {y+h}" stroke="#1E6FB8" stroke-width="5"/>' for i in range(1, 5))
    return (f'<path d="M{x-8} {y+h+10} L{x-8} {y+w/2} A{w/2+8} {w/2+8} 0 0 1 {x+w+8} {y+w/2} L{x+w+8} {y+h+10}Z" fill="#1E6FB8"/>'
            f'<path d="M{x} {y+h} L{x} {y+w/2} A{w/2} {w/2} 0 0 1 {x+w} {y+w/2} L{x+w} {y+h}Z" fill="#14548E"/>' + bars +
            f'<path d="M{x} {y+h*0.45} L{x+w} {y+h*0.45}" stroke="#1E6FB8" stroke-width="5"/>')


def _bougain(x, y, n, r_, seed):
    r = random.Random(seed)
    out = [f'<path d="M{x} {y} q{r.uniform(-40,40):.0f} {-60} {r.uniform(-30,30):.0f} {-120}" stroke="#6B4A2A" stroke-width="7" fill="none"/>']
    for _ in range(n):
        cx, cy = x + r.gauss(0, r_), y - 60 + r.gauss(0, r_ * 0.7)
        out.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r.uniform(10,20):.0f}" fill="{r.choice(["#E0418A", "#F25AA0", "#C92D78", "#FF7AB8", "#4E9A4A"])}"/>')
    return "".join(out)


def _palm(x, y, h, t, s=1.0):
    sw = 4 * math.sin(2 * math.pi * t * 0.3 + x)
    fr = "".join(f'<path d="M{x+sw:.0f} {y-h} q{60*math.cos(a)*s:.0f} {-40*s+70*math.sin(a)*s:.0f} {150*math.cos(a)*s:.0f} {60*s+90*math.sin(a)*s:.0f}" stroke="#3E8E4A" stroke-width="{16*s:.0f}" fill="none" stroke-linecap="round"/>'
                 for a in [-2.8, -2.2, -1.6, -1.0, -0.4, 0.2])
    return (f'<path d="M{x} {y} Q{x-10} {y-h/2} {x+sw:.0f} {y-h}" stroke="#8A6A44" stroke-width="{26*s:.0f}" fill="none"/>' + fr)


def _sea(y, t, w=1920, cols=("#2F9BD8", "#1F7DBF"), amp=6):
    out = [f'<rect x="0" y="{y}" width="{w}" height="400" fill="{cols[0]}"/>']
    for k in range(4):
        yy = y + 20 + k * 26
        ph = 2 * math.pi * (t * 0.25 + k * 0.3)
        d = f"M0 {yy}" + "".join(f" Q{x+40} {yy + amp*math.sin(ph + x/90):.1f} {x+80} {yy}" for x in range(0, w, 80))
        out.append(f'<path d="{d}" stroke="#FFFFFF" stroke-width="3" fill="none" opacity="{0.25 + 0.1*k:.2f}"/>')
    return "".join(out)


def _sparkles(x0, x1, y0, y1, t, n, seed):
    r = random.Random(seed)
    out = []
    for i in range(n):
        x, y = r.uniform(x0, x1), r.uniform(y0, y1)
        a = max(0.0, math.sin(2 * math.pi * (t * r.uniform(0.3, 0.8) + r.random())))
        out.append(f'<path d="M{x-10*a:.0f} {y} L{x+10*a:.0f} {y} M{x} {y-6*a:.0f} L{x} {y+6*a:.0f}" stroke="#FFFFFF" stroke-width="3" opacity="{a:.2f}"/>')
    return "".join(out)


def _gull(x, y, t, s=1.0):
    f = 14 * math.sin(2 * math.pi * t * 2.5)
    return f'<path d="M{x-28*s:.0f} {y+f*s:.0f} Q{x-12*s:.0f} {y-10*s:.0f} {x} {y} Q{x+12*s:.0f} {y-10*s:.0f} {x+28*s:.0f} {y+f*s:.0f}" stroke="#2A2A3A" stroke-width="{4*s:.1f}" fill="none"/>'


def _stars(t, n, seed, ymax=600):
    r = random.Random(seed)
    out = []
    for i in range(n):
        x, y, s = r.uniform(0, 1920), r.uniform(0, ymax), r.uniform(1.5, 4)
        a = 0.5 + 0.5 * math.sin(2 * math.pi * (t * r.uniform(0.2, 0.6)) + r.random() * 6)
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{s:.1f}" fill="#FFFFFF" opacity="{0.3 + 0.7*a:.2f}"/>')
    return "".join(out)


# ------------------------------------------------------------------ Sidi Bou Saïd
@lru_cache(None)
def _sidibou_static(soir):
    sky = _g("sky_sbs", [(0, "#FF9A76"), (0.5, "#FFC48A"), (1, "#FFE2B0")]) if soir else _g("sky_sbs", [(0, "#5DB8F2"), (1, "#BFE6FF")])
    out = [f'<defs>{sky}</defs><rect width="1920" height="1080" fill="url(#sky_sbs)"/>']
    if soir:
        out.append('<circle cx="1500" cy="520" r="130" fill="#FFD27A" opacity="0.5"/><circle cx="1500" cy="520" r="90" fill="#FFB347"/>')
    else:
        out.append('<circle cx="1650" cy="160" r="80" fill="#FFF2A8" opacity="0.7"/><circle cx="1650" cy="160" r="58" fill="#FFE066"/>')
    # mer au loin
    out.append(f'<rect x="1100" y="560" width="820" height="160" fill="{"#E9906A" if soir else "#2F9BD8"}"/>')
    # maisons de fond
    house = "#FFF6EC" if not soir else "#FFE3CC"
    shade = "#E8DCCF" if not soir else "#F0C4A8"
    for x, y, w in [(0, 380, 300), (260, 300, 260), (500, 420, 280), (760, 340, 300), (1020, 460, 180)]:
        out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{930-y}" fill="{house}"/><rect x="{x+w-24}" y="{y}" width="24" height="{930-y}" fill="{shade}"/>'
                   f'<rect x="{x-6}" y="{y-10}" width="{w+12}" height="16" fill="{shade}"/>')
    out.append('<path d="M330 300 A70 70 0 0 1 470 300Z" fill="#FFFFFF"/><rect x="392" y="200" width="16" height="40" fill="#FFFFFF"/>')
    out.append(_window(100, 470, 110, 160) + _window(560, 520, 100, 140) + _window(820, 430, 120, 170))
    out.append(_door(300, 610, 150, 320) + _door(1040, 650, 130, 280, "#2580C8"))
    out.append(_bougain(250, 560, 70, 70, 3) + _bougain(980, 600, 60, 60, 4) + _bougain(720, 520, 55, 60, 5))
    # escalier/rue pavée
    out.append(f'<rect y="900" width="1920" height="180" fill="{"#E9C9A6" if soir else "#E8DCC8"}"/>')
    for i in range(18):
        out.append(f'<path d="M{i*110} 900 L{i*110-60} 1080" stroke="#D4C2A6" stroke-width="3"/>')
    out.append('<path d="M0 960 L1920 960 M0 1020 L1920 1020" stroke="#D4C2A6" stroke-width="3"/>')
    # lampadaire
    out.append('<rect x="1600" y="560" width="14" height="370" fill="#2A2A3A"/><path d="M1580 560 L1634 560 L1622 520 L1592 520Z" fill="#2A2A3A"/>'
               f'<rect x="1594" y="526" width="26" height="30" fill="{"#FFD27A" if soir else "#F2F2F2"}"/>')
    return "".join(out)


def sidibou(t, soir=False):
    out = [_sidibou_static(soir)]
    out.append(_sparkles(1100, 1920, 570, 710, t, 14, 2))
    for i, (x, y) in enumerate([(300, 160), (900, 110)]):
        out.append(_cloud((x + 25 * t) % 2200 - 140, y, 0.8 + 0.2 * i, 0.85 if not soir else 0.6, "#FFFFFF" if not soir else "#FFD9C2"))
    out.append(_gull((1400 + 60 * t) % 2100 - 90, 260, t, 0.9) + _gull((1200 + 50 * t) % 2100 - 90, 320, t + 0.3, 0.7))
    if soir:
        out.append('<rect width="1920" height="1080" fill="#FF7A3A" opacity="0.08"/>')
    return "".join(out)


# ------------------------------------------------------------------ Café en terrasse
@lru_cache(None)
def _cafe_static():
    out = [f'<defs>{_g("sky_cafe", [(0, "#6CC3F5"), (1, "#D6F0FF")])}</defs><rect width="1920" height="1080" fill="url(#sky_cafe)"/>']
    out.append('<path d="M0 560 Q300 520 600 560 L600 600 L0 600Z" fill="#7FA9C8"/>')
    out.append('<path d="M1300 600 Q1500 500 1920 540 L1920 600Z" fill="#6E98B8"/>')
    # store rayé
    for i in range(13):
        col = "#1E6FB8" if i % 2 == 0 else "#FFFFFF"
        out.append(f'<path d="M{i*150} 0 L{i*150+150} 0 L{i*150+150} 130 Q{i*150+75} 170 {i*150} 130Z" fill="{col}"/>')
    out.append('<rect width="1920" height="12" y="0" fill="#14548E"/>')
    # sol carrelé
    out.append('<rect y="760" width="1920" height="320" fill="#F2EADF"/>')
    for i in range(0, 1920, 120):
        out.append(f'<path d="M{i} 760 L{i - 200} 1080" stroke="#DCCFBF" stroke-width="3"/>')
    for y in (820, 900, 1000):
        out.append(f'<path d="M0 {y} L1920 {y}" stroke="#DCCFBF" stroke-width="3"/>')
    # balustrade bleue
    out.append('<rect x="0" y="640" width="1920" height="14" fill="#1E6FB8"/>')
    for x in range(10, 1920, 46):
        out.append(f'<rect x="{x}" y="654" width="12" height="106" fill="#1E6FB8"/>')
    out.append('<rect x="0" y="752" width="1920" height="12" fill="#1E6FB8"/>')
    # tables de fond
    for x in (220, 1660):
        out.append(f'<ellipse cx="{x}" cy="800" rx="110" ry="22" fill="#FFFFFF"/><rect x="{x-8}" y="800" width="16" height="110" fill="#8A8A9A"/>'
                   f'<rect x="{x-40}" y="760" width="18" height="34" rx="3" fill="#E9F7EE" opacity="0.9"/><rect x="{x-38}" y="770" width="14" height="22" fill="#C9862A" opacity="0.8"/>'
                   f'<rect x="{x+20}" y="764" width="16" height="30" rx="3" fill="#FFFFFF"/>')
    # pots de plantes
    for x in (80, 1840):
        out.append(f'<path d="M{x-50} 930 L{x+50} 930 L{x+38} 1010 L{x-38} 1010Z" fill="#C96A3A"/>'
                   + "".join(f'<ellipse cx="{x + dx}" cy="{900 - abs(dx)*0.6}" rx="18" ry="60" transform="rotate({dx*0.8} {x+dx} 930)" fill="#3E8E4A"/>' for dx in (-40, -20, 0, 20, 40)))
    return "".join(out)


def cafe(t):
    return (_cafe_static()[:0] + _cafe_static().replace('<path d="M0 560', _sea(560, t, amp=3) + '<path d="M0 560', 1)
            + _sparkles(0, 1920, 590, 640, t, 18, 7) + _gull((300 + 70 * t) % 2100 - 90, 300, t))


# ------------------------------------------------------------------ Plage de La Marsa
@lru_cache(None)
def _plage_static():
    out = [f'<defs>{_g("sky_pl", [(0, "#49B2F0"), (1, "#C8ECFF")])}{_g("sand", [(0, "#F6DDA8"), (1, "#E8C27E")])}</defs>',
           '<rect width="1920" height="1080" fill="url(#sky_pl)"/>',
           '<circle cx="300" cy="170" r="90" fill="#FFF3A0" opacity="0.6"/><circle cx="300" cy="170" r="64" fill="#FFE45A"/>']
    return "".join(out)


def plage(t):
    out = [_plage_static()]
    for i, (x, y) in enumerate([(700, 140), (1300, 220), (1750, 120)]):
        out.append(_cloud((x + 20 * t * (1 + i * 0.2)) % 2200 - 140, y, 0.7 + 0.15 * i))
    out.append(_sea(560, t, amp=7))
    # bateau
    bx = (1300 + 18 * t) % 2100 - 90
    out.append(f'<g transform="translate({bx:.0f} {600 + 3*math.sin(t):.1f})"><path d="M-50 0 L50 0 L36 22 L-36 22Z" fill="#FFFFFF"/>'
               '<path d="M0 0 L0 -70 L40 -6Z" fill="#FFFFFF"/><path d="M-2 0 L-2 -64 L-34 -6Z" fill="#F25A5A"/></g>')
    # vagues sur le sable
    wv = 18 * math.sin(2 * math.pi * t * 0.25)
    out.append(f'<path d="M0 {770+wv:.0f} Q480 {740+wv:.0f} 960 {770+wv:.0f} T1920 {765+wv:.0f} L1920 1080 L0 1080Z" fill="#FFFFFF" opacity="0.8"/>')
    out.append(f'<path d="M0 {786+wv:.0f} Q480 {760+wv:.0f} 960 {786+wv:.0f} T1920 {780+wv:.0f} L1920 1080 L0 1080Z" fill="url(#sand)"/>')
    # parasols
    for x, c1, c2 in [(180, "#F25A5A", "#FFFFFF"), (1720, "#1E9BD8", "#FFE45A")]:
        segs = "".join(f'<path d="M{x} 640 L{x-130+k*52} 700 L{x-130+(k+1)*52} 700Z" fill="{c1 if k % 2 == 0 else c2}"/>' for k in range(5))
        out.append(f'<rect x="{x-5}" y="640" width="10" height="290" fill="#8A6A44"/>' + segs)
        out.append(f'<rect x="{x-90}" y="905" width="150" height="20" rx="8" fill="{c1}"/>')
    out.append(_sparkles(0, 1920, 570, 730, t, 24, 9))
    out.append(_gull((200 + 80 * t) % 2100 - 90, 300, t) + _gull((900 + 65 * t) % 2100 - 90, 250, t + 0.4, 0.8))
    for x in (520, 1400):
        out.append(f'<path d="M{x} 1000 q20 -30 40 0 q-20 10 -40 0z" fill="#F2A07A"/>')
    return "".join(out)


# ------------------------------------------------------------------ La fac
@lru_cache(None)
def _fac_static():
    out = [f'<defs>{_g("sky_fac", [(0, "#62BDF5"), (1, "#D8F1FF")])}</defs><rect width="1920" height="1080" fill="url(#sky_fac)"/>']
    out.append('<rect x="160" y="250" width="1600" height="680" fill="#F0DDB8"/><rect x="140" y="230" width="1640" height="40" fill="#D9BE8E"/>')
    for i in range(8):
        x = 230 + i * 190
        out.append(f'<path d="M{x} 930 L{x} 640 A70 70 0 0 1 {x+140} 640 L{x+140} 930Z" fill="#C79A5E" opacity="0.35"/>'
                   f'<path d="M{x+10} 520 L{x+10} 410 A60 60 0 0 1 {x+130} 410 L{x+130} 520Z" fill="#7CA8C8"/>'
                   f'<path d="M{x+70} 350 L{x+70} 520 M{x+10} 450 L{x+130} 450" stroke="#F0DDB8" stroke-width="6"/>')
    out.append('<rect x="760" y="150" width="400" height="100" fill="#F0DDB8"/><text x="960" y="222" font-family="Fredoka" font-weight="700" font-size="56" text-anchor="middle" fill="#8A5A2A">UNIVERSITÉ</text>')
    # drapeau tunisien
    out.append('<rect x="1240" y="40" width="8" height="200" fill="#6A6A7A"/><rect x="1248" y="44" width="150" height="100" fill="#E70013"/>'
               '<circle cx="1323" cy="94" r="32" fill="#FFFFFF"/><circle cx="1330" cy="94" r="24" fill="#E70013"/><circle cx="1338" cy="94" r="20" fill="#FFFFFF"/>'
               '<path d="M1322 94 l20 -7 l-12 17 l0 -21 l12 17z" fill="#E70013"/>')
    out.append('<rect y="900" width="1920" height="180" fill="#DCCBAA"/>')
    for i in range(0, 1920, 96):
        out.append(f'<rect x="{i}" y="900" width="94" height="180" fill="#E6D6B6" opacity="{0.5 if (i//96)%2 else 0}"/>')
    out.append('<rect x="1380" y="860" width="260" height="20" rx="6" fill="#8A5A2A"/><rect x="1395" y="880" width="12" height="50" fill="#5A3A22"/><rect x="1613" y="880" width="12" height="50" fill="#5A3A22"/>')
    return "".join(out)


def fac(t):
    out = [_fac_static(), _palm(90, 930, 520, t, 1.1), _palm(1830, 930, 480, t, 1.0)]
    out.append(_cloud((500 + 22 * t) % 2200 - 140, 110, 0.8) + _cloud((1500 + 18 * t) % 2200 - 140, 80, 0.6))
    # étudiants au fond qui passent
    for k, (sp, col) in enumerate([(60, "#7A6AB8"), (-45, "#D88A4A"), (38, "#4AA88A")]):
        x = (400 + k * 600 + sp * t) % 2100 - 90
        out.append(f'<g opacity="0.45" transform="translate({x:.0f} 900) scale(0.35)"><rect x="-40" y="-360" width="80" height="170" rx="30" fill="{col}"/>'
                   f'<circle cx="0" cy="-420" r="55" fill="#C99A72"/><rect x="-30" y="-200" width="22" height="200" fill="#3A3A4A"/><rect x="8" y="-200" width="22" height="200" fill="#3A3A4A"/></g>')
    return "".join(out)


# ------------------------------------------------------------------ Médina / souk
@lru_cache(None)
def _medina_static():
    out = ['<rect width="1920" height="1080" fill="#7A4A2A"/>',
           f'<defs>{_g("medina_l", [(0, "#F2C27A"), (1, "#C98A4A")])}</defs>',
           '<rect x="0" y="0" width="1920" height="930" fill="url(#medina_l)"/>']
    for i, x in enumerate(range(-100, 2000, 420)):
        out.append(f'<path d="M{x} 930 L{x} 420 Q{x+150} 220 {x+300} 420 L{x+300} 930Z" fill="#8A4A24" opacity="0.55"/>'
                   f'<path d="M{x+20} 930 L{x+20} 430 Q{x+150} 260 {x+280} 430 L{x+280} 930Z" fill="#F7D9A6"/>')
        # marchandises : tapis, assiettes, chéchias
        cols = ["#C8323C", "#1E6FB8", "#2FA36B", "#F2B23A"]
        out.append(f'<rect x="{x+50}" y="520" width="90" height="260" fill="{cols[i%4]}"/><path d="M{x+60} 540 L{x+130} 540 M{x+60} 760 L{x+130} 760" stroke="#FFFFFF" stroke-width="5" stroke-dasharray="8 6"/>'
                   f'<path d="M{x+95} 580 L{x+125} 650 L{x+95} 720 L{x+65} 650Z" fill="#FFFFFF" opacity="0.7"/>')
        for k in range(3):
            out.append(f'<circle cx="{x+200}" cy="{520 + k*90}" r="36" fill="#FFFFFF"/><circle cx="{x+200}" cy="{520 + k*90}" r="26" fill="{cols[(i+k+1)%4]}"/>'
                       f'<circle cx="{x+200}" cy="{520 + k*90}" r="10" fill="#FFFFFF"/>')
        out.append("".join(f'<path d="M{x+170+j*36} 800 L{x+176+j*36} 760 L{x+196+j*36} 760 L{x+202+j*36} 800Z" fill="#C8202C"/><rect x="{x+184+j*36}" y="752" width="4" height="10" fill="#222"/>' for j in range(3)))
    out.append('<rect y="900" width="1920" height="180" fill="#B88A5A"/>')
    for i in range(0, 1920, 80):
        out.append(f'<path d="M{i} 900 L{i-40} 1080" stroke="#9A7048" stroke-width="3"/>')
    return "".join(out)


def medina(t):
    out = [_medina_static()]
    for k, x in enumerate(range(110, 2000, 420)):
        sw = 6 * math.sin(2 * math.pi * t * 0.5 + k)
        out.append(f'<g transform="rotate({sw:.1f} {x+150} 300)"><path d="M{x+150} 300 L{x+150} 380" stroke="#3A2A1A" stroke-width="3"/>'
                   f'<path d="M{x+125} 380 L{x+175} 380 L{x+185} 430 L{x+150} 470 L{x+115} 430Z" fill="#F2B23A"/>'
                   f'<circle cx="{x+150}" cy="425" r="{50 + 6*math.sin(2*math.pi*t + k):.0f}" fill="#FFD27A" opacity="0.25"/></g>')
    return "".join(out)


# ------------------------------------------------------------------ Toit la nuit
@lru_cache(None)
def _toit_static():
    out = [f'<defs>{_g("sky_n", [(0, "#0E1440"), (0.7, "#2A2C6A"), (1, "#5A4A8A")])}</defs><rect width="1920" height="1080" fill="url(#sky_n)"/>',
           '<circle cx="1500" cy="200" r="120" fill="#FFF6D0" opacity="0.15"/><circle cx="1500" cy="200" r="74" fill="#FFF2C0"/><circle cx="1530" cy="180" r="66" fill="#2A2C6A" opacity="0.0"/>']
    # ville au loin
    r = random.Random(3)
    x = 0
    while x < 1920:
        w, h = r.randint(60, 160), r.randint(60, 220)
        out.append(f'<rect x="{x}" y="{700-h}" width="{w}" height="{h+60}" fill="#1E1A44"/>')
        for _ in range(r.randint(1, 5)):
            out.append(f'<rect x="{x + r.randint(8, max(9, w-20))}" y="{700-h + r.randint(10, max(11, h-20))}" width="10" height="14" fill="#FFD27A" opacity="0.8"/>')
        x += w
    out.append('<path d="M700 640 A110 110 0 0 1 920 640Z" fill="#E8E4F4"/><rect x="700" y="640" width="220" height="80" fill="#E8E4F4"/>')
    # toit
    out.append('<rect y="740" width="1920" height="340" fill="#D8D0E6"/><rect y="740" width="1920" height="22" fill="#F2EEF8"/>'
               '<rect y="700" width="1920" height="48" fill="#EDE8F6"/>')
    for x in (60, 1860):
        out.append(f'<path d="M{x-46} 930 L{x+46} 930 L{x+34} 1000 L{x-34} 1000Z" fill="#3E7AC8"/>'
                   + "".join(f'<circle cx="{x + 30*math.cos(a):.0f}" cy="{880 + 30*math.sin(a):.0f}" r="22" fill="#2E6A3A"/>' for a in [i*1.1 for i in range(6)])
                   + "".join(f'<circle cx="{x + 34*math.cos(a):.0f}" cy="{874 + 30*math.sin(a):.0f}" r="6" fill="#FFFFFF"/>' for a in [i*0.9 for i in range(7)]))
    return "".join(out)


def toit_nuit(t):
    out = [_toit_static().replace('<circle cx="1500" cy="200" r="120"', _stars(t, 120, 5, 560) + '<circle cx="1500" cy="200" r="120"', 1)]
    # guirlande
    d = "M0 120 Q480 260 960 140 T1920 130"
    out.append(f'<path d="{d}" stroke="#2A2030" stroke-width="3" fill="none"/>')
    for i in range(24):
        u = i / 23
        x = u * 1920
        y = 120 + 110 * math.sin(math.pi * min(1, u * 2)) if u < 0.5 else 140 + 90 * math.sin(math.pi * (u - 0.5) * 2)
        a = 0.6 + 0.4 * math.sin(2 * math.pi * t * 0.8 + i)
        out.append(f'<circle cx="{x:.0f}" cy="{y+12:.0f}" r="22" fill="#FFD27A" opacity="{0.25*a:.2f}"/><circle cx="{x:.0f}" cy="{y+12:.0f}" r="9" fill="#FFE8A0" opacity="{a:.2f}"/>')
    sx = (1920 - (t * 300) % 6000)
    if 0 < sx < 1920:
        out.append(f'<path d="M{sx:.0f} {80 + (1920-sx)*0.15:.0f} l120 -40" stroke="#FFFFFF" stroke-width="3" opacity="0.8"/>')
    return "".join(out)


# ------------------------------------------------------------------ La maison
@lru_cache(None)
def _maison_static():
    out = ['<rect width="1920" height="1080" fill="#F6E8D4"/>']
    # bande de zellige
    out.append('<rect y="600" width="1920" height="330" fill="#FFFFFF"/>')
    for x in range(0, 1920, 60):
        for y in range(610, 920, 60):
            c = ["#1E6FB8", "#2FA36B", "#F2B23A", "#C8323C"][((x // 60) + (y // 60)) % 4]
            out.append(f'<path d="M{x+30} {y} L{x+60} {y+30} L{x+30} {y+60} L{x} {y+30}Z" fill="{c}" opacity="0.75"/>')
    out.append('<rect y="590" width="1920" height="14" fill="#C98A4A"/>')
    # fenêtre
    out.append(_window(1300, 180, 260, 340).replace("#1E6FB8", "#2580C8"))
    out.append('<rect x="1310" y="320" width="240" height="190" fill="#9ED8F5" opacity="0.4"/>')
    # cadre
    out.append('<rect x="360" y="200" width="300" height="220" fill="#8A5A2A"/><rect x="380" y="220" width="260" height="180" fill="#F2C27A"/>'
               '<path d="M380 400 L470 300 L540 360 L590 320 L640 400Z" fill="#2FA36B"/><circle cx="590" cy="270" r="22" fill="#FFE066"/>')
    # canapé
    out.append('<rect x="160" y="760" width="760" height="170" rx="30" fill="#B8434E"/><rect x="160" y="680" width="760" height="110" rx="30" fill="#C8545E"/>'
               '<rect x="130" y="720" width="70" height="210" rx="26" fill="#A8343E"/><rect x="880" y="720" width="70" height="210" rx="26" fill="#A8343E"/>')
    out.append('<rect y="930" width="1920" height="150" fill="#C9A276"/>')
    # table basse, théière
    out.append('<rect x="1100" y="860" width="320" height="22" rx="8" fill="#8A5A2A"/><rect x="1120" y="882" width="14" height="48" fill="#6A4022"/><rect x="1386" y="882" width="14" height="48" fill="#6A4022"/>'
               '<path d="M1220 860 Q1210 800 1260 796 Q1310 800 1300 860Z" fill="#D9D9E0"/><path d="M1300 830 L1340 806" stroke="#D9D9E0" stroke-width="8"/>'
               '<rect x="1350" y="830" width="20" height="30" rx="3" fill="#E9F7EE"/><rect x="1352" y="840" width="16" height="18" fill="#C9862A"/>')
    return "".join(out)


def maison(t):
    return _maison_static()


DECORS = {"sidibou": sidibou, "sidibou_soir": lambda t: sidibou(t, True), "cafe": cafe, "plage": plage,
          "fac": fac, "medina": medina, "toit_nuit": toit_nuit, "maison": maison}
NIGHT = {"toit_nuit"}
