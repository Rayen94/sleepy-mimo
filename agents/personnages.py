"""Agent 17 — Character designer : les personnages éveillés, qui parlent, clignent des yeux et marchent.
Mimo l'ourson, Luna la chouette, Pip le lapin, Twinkle l'étoile et Wooly l'agneau.
Chaque fonction dessine le personnage centré en (0, 0) (les pieds vers y=+130), à placer avec translate/scale.
mouth : ouverture de la bouche (0 à 1), blink : yeux fermés, walk : phase de marche (0 à 1), wave : bras levé."""
import math

NAMES = {"fish": "Bubbles", "mimo": "Mimo", "owl": "Luna", "bunny": "Pip", "star": "Twinkle", "lamb": "Wooly", "kitten": "Mia", "duck": "Dot", "fox": "Finn"}
SPECIES = {"fish": "big fish", "mimo": "little bear", "owl": "owl", "bunny": "bunny", "star": "little star", "lamb": "little lamb", "kitten": "kitten", "duck": "duckling", "fox": "fox"}


def _eyes(xl, xr, y, r, blink, look=0.0, col="#2B1A12"):
    if blink:
        return (f'<path d="M{xl-r} {y} Q{xl} {y+r*0.8} {xl+r} {y}" stroke="{col}" stroke-width="{r*0.6:.1f}" fill="none" stroke-linecap="round"/>'
                f'<path d="M{xr-r} {y} Q{xr} {y+r*0.8} {xr+r} {y}" stroke="{col}" stroke-width="{r*0.6:.1f}" fill="none" stroke-linecap="round"/>')
    out = ""
    for x in (xl, xr):
        out += (f'<ellipse cx="{x + look*r*0.3:.1f}" cy="{y}" rx="{r*0.85:.1f}" ry="{r:.1f}" fill="{col}"/>'
                f'<circle cx="{x + look*r*0.3 + r*0.3:.1f}" cy="{y - r*0.35:.1f}" r="{r*0.32:.1f}" fill="#FFFFFF"/>')
    return out


def _mouth(x, y, w, mouth, col="#7A2E2E"):
    if mouth < 0.12:
        return f'<path d="M{x-w} {y} Q{x} {y+w*0.9} {x+w} {y}" stroke="#4A2A1A" stroke-width="{w*0.35:.1f}" fill="none" stroke-linecap="round"/>'
    h = w * (0.35 + 0.9 * mouth)
    return (f'<path d="M{x-w} {y} Q{x} {y+h*2} {x+w} {y} Q{x} {y+h*0.4} {x-w} {y}Z" fill="{col}"/>'
            f'<ellipse cx="{x}" cy="{y + h*0.95:.1f}" rx="{w*0.45:.1f}" ry="{h*0.35:.1f}" fill="#F28A8A"/>')


def mimo(mouth=0.0, blink=False, walk=0.0, wave=0.0, cap="#8FB8E8", look=0.0):
    sw = math.sin(2 * math.pi * walk)
    bob = -abs(sw) * 6
    la, ra = 20 * sw, -20 * sw - 120 * wave
    return f'''<g transform="translate(0 {bob:.1f})">
<ellipse cx="-26" cy="{118 + 6*sw:.1f}" rx="22" ry="14" fill="#9C6A44"/><ellipse cx="26" cy="{118 - 6*sw:.1f}" rx="22" ry="14" fill="#9C6A44"/>
<g transform="rotate({la:.1f} -50 30)"><ellipse cx="-60" cy="60" rx="18" ry="34" fill="#B57D52"/></g>
<g transform="rotate({ra:.1f} 50 30)"><ellipse cx="60" cy="60" rx="18" ry="34" fill="#B57D52"/></g>
<ellipse cx="0" cy="60" rx="56" ry="64" fill="#C48A5C"/><ellipse cx="0" cy="70" rx="36" ry="42" fill="#F2D6B3"/>
<circle cx="-48" cy="-92" r="22" fill="#B57D52"/><circle cx="-48" cy="-92" r="11" fill="#E9B98F"/>
<circle cx="48" cy="-92" r="22" fill="#B57D52"/><circle cx="48" cy="-92" r="11" fill="#E9B98F"/>
<circle cx="0" cy="-45" r="62" fill="#C48A5C"/>
<ellipse cx="0" cy="-20" rx="30" ry="22" fill="#F2D6B3"/><ellipse cx="0" cy="-30" rx="11" ry="8" fill="#5A3624"/>
{_eyes(-23, 23, -55, 8, blink, look)}
{_mouth(0, -14, 10, mouth)}
<circle cx="-40" cy="-25" r="10" fill="#F4A3A3" opacity="0.7"/><circle cx="40" cy="-25" r="10" fill="#F4A3A3" opacity="0.7"/>
<path d="M-58 -78 Q0 -150 60 -88 Q0 -108 -58 -78Z" fill="{cap}"/><circle cx="66" cy="-92" r="13" fill="#FFF4C9"/>
</g>'''


def owl(mouth=0.0, blink=False, walk=0.0, wave=0.0, look=0.0):
    flap = math.sin(2 * math.pi * walk) * 12 + 50 * wave
    bob = -abs(math.sin(2 * math.pi * walk)) * 5
    lid = "" if not blink else ('<path d="M-56 -40 A24 24 0 0 1 -8 -40Z" fill="#7E5FC4"/><path d="M8 -40 A24 24 0 0 1 56 -40Z" fill="#7E5FC4"/>'
                                '<path d="M-56 -40 L-8 -40 M8 -40 L56 -40" stroke="#3E2A6E" stroke-width="4"/>')
    if blink:
        lid = ('<rect x="-58" y="-66" width="52" height="28" fill="#9A7BDB"/><rect x="6" y="-66" width="52" height="28" fill="#9A7BDB"/>'
               '<path d="M-54 -40 Q-32 -30 -10 -40 M10 -40 Q32 -30 54 -40" stroke="#3E2A6E" stroke-width="4" fill="none"/>')
    beak_open = 4 + 14 * mouth
    return f'''<g transform="translate(0 {bob:.1f})">
<ellipse cx="-20" cy="124" rx="16" ry="8" fill="#F2A33A"/><ellipse cx="20" cy="124" rx="16" ry="8" fill="#F2A33A"/>
<g transform="rotate({-flap:.1f} -55 10)"><ellipse cx="-70" cy="45" rx="22" ry="52" fill="#6A4BAE"/></g>
<g transform="rotate({flap:.1f} 55 10)"><ellipse cx="70" cy="45" rx="22" ry="52" fill="#6A4BAE"/></g>
<ellipse cx="0" cy="25" rx="68" ry="98" fill="#9A7BDB"/>
<ellipse cx="0" cy="55" rx="44" ry="58" fill="#D9CBF6"/>
<g fill="#B8A6E8">{"".join(f'<path d="M{x-8} {y} Q{x} {y+10} {x+8} {y}" stroke="#B8A6E8" stroke-width="3" fill="none"/>' for x in (-16, 0, 16) for y in (40, 60, 80))}</g>
<path d="M-52 -82 L-36 -112 L-22 -78Z" fill="#7E5FC4"/><path d="M52 -82 L36 -112 L22 -78Z" fill="#7E5FC4"/>
<circle cx="-32" cy="-40" r="26" fill="#FFFFFF"/><circle cx="32" cy="-40" r="26" fill="#FFFFFF"/>
<circle cx="{-32 + look*6:.1f}" cy="-38" r="13" fill="#2B1A12"/><circle cx="{32 + look*6:.1f}" cy="-38" r="13" fill="#2B1A12"/>
<circle cx="{-27 + look*6:.1f}" cy="-43" r="4.5" fill="#FFFFFF"/><circle cx="{37 + look*6:.1f}" cy="-43" r="4.5" fill="#FFFFFF"/>
{lid}
<path d="M-11 -14 L11 -14 L0 2Z" fill="#F2A33A"/><path d="M-9 {-12 + beak_open:.1f} L9 {-12 + beak_open:.1f} L0 {2 + beak_open:.1f}Z" fill="#E08A20"/>
<circle cx="-52" cy="-12" r="9" fill="#F4A3C6" opacity="0.6"/><circle cx="52" cy="-12" r="9" fill="#F4A3C6" opacity="0.6"/>
</g>'''


def bunny(mouth=0.0, blink=False, walk=0.0, wave=0.0, look=0.0):
    hop = abs(math.sin(2 * math.pi * walk)) * 22
    ear = 6 * math.sin(2 * math.pi * walk * 2) + 4 * mouth
    teeth = f'<rect x="-6" y="-6" width="5" height="{6+6*mouth:.1f}" fill="#FFFFFF"/><rect x="1" y="-6" width="5" height="{6+6*mouth:.1f}" fill="#FFFFFF"/>' if mouth > 0.12 else ""
    return f'''<g transform="translate(0 {-hop:.1f})">
<g transform="rotate({-8 - ear:.1f} -22 -80)"><ellipse cx="-24" cy="-150" rx="17" ry="62" fill="#FFFFFF"/><ellipse cx="-24" cy="-146" rx="8" ry="44" fill="#F7B7C9"/></g>
<g transform="rotate({8 + ear:.1f} 22 -80)"><ellipse cx="24" cy="-150" rx="17" ry="62" fill="#FFFFFF"/><ellipse cx="24" cy="-146" rx="8" ry="44" fill="#F7B7C9"/></g>
<ellipse cx="-24" cy="120" rx="24" ry="12" fill="#F1ECF6"/><ellipse cx="24" cy="120" rx="24" ry="12" fill="#F1ECF6"/>
<ellipse cx="0" cy="62" rx="52" ry="60" fill="#FFFFFF"/><ellipse cx="0" cy="70" rx="30" ry="36" fill="#FDEFF4"/>
<g transform="rotate({-15 - 110*wave:.1f} 40 40)"><ellipse cx="52" cy="62" rx="13" ry="26" fill="#FFFFFF"/></g>
<ellipse cx="-50" cy="62" rx="13" ry="26" fill="#FFFFFF"/>
<circle cx="0" cy="-35" r="55" fill="#FFFFFF"/>
{_eyes(-20, 20, -45, 7.5, blink, look, "#3A2A4A")}
<path d="M-7 -22 L7 -22 L0 -14Z" fill="#F28AA8"/>
{_mouth(0, -10, 9, mouth, "#B44A6A")}{teeth}
<circle cx="-36" cy="-20" r="10" fill="#F7B7C9" opacity="0.8"/><circle cx="36" cy="-20" r="10" fill="#F7B7C9" opacity="0.8"/>
</g>'''


def star(mouth=0.0, blink=False, walk=0.0, wave=0.0, look=0.0):
    rot = 6 * math.sin(2 * math.pi * walk)
    pts = []
    for i in range(10):
        a = math.pi / 5 * i - math.pi / 2
        r = 120 if i % 2 == 0 else 58
        pts.append(f"{r*math.cos(a):.1f},{r*math.sin(a) + 10:.1f}")
    return f'''<g transform="rotate({rot:.1f})"><circle cx="0" cy="10" r="160" fill="#FFE9A0" opacity="0.22"/>
<path d="M{" L".join(pts)}Z" fill="#FFD95A" stroke="#F2B53A" stroke-width="6" stroke-linejoin="round"/>
{_eyes(-22, 22, 0, 8, blink, look, "#6A3A12")}
{_mouth(0, 26, 11, mouth, "#B5532A")}
<circle cx="-42" cy="20" r="10" fill="#F59A8A" opacity="0.6"/><circle cx="42" cy="20" r="10" fill="#F59A8A" opacity="0.6"/></g>'''


def lamb(mouth=0.0, blink=False, walk=0.0, wave=0.0, look=0.0):
    sw = math.sin(2 * math.pi * walk)
    body = "".join(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#FFFFFF"/>' for cx, cy, r in
                   [(-40, 50, 34), (0, 36, 40), (40, 50, 34), (-30, 80, 32), (30, 80, 32), (0, 86, 36)])
    legs = "".join(f'<rect x="{x}" y="100" width="14" height="{30 + 5*sw*(1 if i%2 else -1):.1f}" rx="7" fill="#4A3F5C"/>' for i, x in enumerate((-40, -14, 2, 28)))
    return f'''<g transform="translate(0 {-abs(sw)*5:.1f})">{legs}{body}
<ellipse cx="-46" cy="-30" rx="22" ry="11" fill="#4A3F5C" transform="rotate(-25 -46 -30)"/><ellipse cx="46" cy="-30" rx="22" ry="11" fill="#4A3F5C" transform="rotate(25 46 -30)"/>
<ellipse cx="0" cy="-20" rx="38" ry="44" fill="#4A3F5C"/>
<g fill="#FFFFFF"><circle cx="-18" cy="-62" r="15"/><circle cx="0" cy="-68" r="17"/><circle cx="18" cy="-62" r="15"/></g>
{_eyes(-14, 14, -26, 6.5, blink, look, "#FFFFFF")}
{_mouth(0, -2, 8, mouth, "#B44A6A")}
<circle cx="-24" cy="-8" r="7" fill="#F4A3A3" opacity="0.6"/><circle cx="24" cy="-8" r="7" fill="#F4A3A3" opacity="0.6"/>
</g>'''


def kitten(mouth=0.0, blink=False, walk=0.0, wave=0.0, look=0.0):
    sw = math.sin(2 * math.pi * walk)
    tail = 18 * math.sin(2 * math.pi * walk * 0.5 + 1) + 10
    return f'''<g transform="translate(0 {-abs(sw)*5:.1f})">
<path d="M40 90 Q{95 + tail:.1f} 60 {80 + tail:.1f} 0" stroke="#F2A65A" stroke-width="16" fill="none" stroke-linecap="round"/>
<ellipse cx="-22" cy="{122 + 5*sw:.1f}" rx="18" ry="11" fill="#FFF1E0"/><ellipse cx="22" cy="{122 - 5*sw:.1f}" rx="18" ry="11" fill="#FFF1E0"/>
<ellipse cx="0" cy="68" rx="48" ry="56" fill="#F2A65A"/><ellipse cx="0" cy="78" rx="28" ry="36" fill="#FFF1E0"/>
<g transform="rotate({-110*wave:.1f} 40 40)"><ellipse cx="48" cy="66" rx="12" ry="26" fill="#F2A65A"/></g><ellipse cx="-48" cy="66" rx="12" ry="26" fill="#F2A65A"/>
<path d="M-56 -60 L-46 -118 L-12 -86Z" fill="#F2A65A"/><path d="M-48 -70 L-42 -104 L-22 -84Z" fill="#FFC2D1"/>
<path d="M56 -60 L46 -118 L12 -86Z" fill="#F2A65A"/><path d="M48 -70 L42 -104 L22 -84Z" fill="#FFC2D1"/>
<circle cx="0" cy="-42" r="58" fill="#F2A65A"/>
<path d="M-20 -96 Q-14 -80 -8 -96 M8 -96 Q14 -80 20 -96" stroke="#D9833A" stroke-width="5" fill="none"/>
<ellipse cx="0" cy="-18" rx="30" ry="20" fill="#FFF1E0"/>
{_eyes(-22, 22, -50, 8.5, blink, look, "#2E4A2E")}
<path d="M-6 -26 L6 -26 L0 -19Z" fill="#F28AA8"/>
{_mouth(0, -12, 9, mouth, "#B44A6A")}
<g stroke="#8A5A3A" stroke-width="2.5"><line x1="-30" y1="-22" x2="-62" y2="-28"/><line x1="-30" y1="-16" x2="-62" y2="-12"/>
<line x1="30" y1="-22" x2="62" y2="-28"/><line x1="30" y1="-16" x2="62" y2="-12"/></g>
<circle cx="-38" cy="-26" r="9" fill="#FF9EB0" opacity="0.6"/><circle cx="38" cy="-26" r="9" fill="#FF9EB0" opacity="0.6"/>
<path d="M-30 -96 Q0 -112 30 -96 L24 -88 Q0 -100 -24 -88Z" fill="#FF6F91"/><circle cx="34" cy="-98" r="9" fill="#FF6F91"/>
</g>'''


def duck(mouth=0.0, blink=False, walk=0.0, wave=0.0, look=0.0):
    sw = math.sin(2 * math.pi * walk)
    flap = 25 * wave + 6 * sw
    beak = 4 + 12 * mouth
    return f'''<g transform="translate(0 {-abs(sw)*4:.1f}) rotate({4*sw:.1f} 0 120)">
<path d="M-30 118 L-12 118 L-20 104Z M12 118 L30 118 L20 104Z" fill="#FF9F3A"/><ellipse cx="-20" cy="122" rx="16" ry="6" fill="#FF9F3A"/><ellipse cx="20" cy="122" rx="16" ry="6" fill="#FF9F3A"/>
<ellipse cx="0" cy="62" rx="60" ry="52" fill="#FFE066"/>
<g transform="rotate({-flap:.1f} -40 50)"><ellipse cx="-56" cy="62" rx="16" ry="30" fill="#FFD23F"/></g>
<g transform="rotate({flap:.1f} 40 50)"><ellipse cx="56" cy="62" rx="16" ry="30" fill="#FFD23F"/></g>
<circle cx="0" cy="-30" r="54" fill="#FFE066"/><path d="M-6 -86 Q0 -110 10 -92 Q16 -108 18 -84" fill="#FFD23F"/>
{_eyes(-20, 20, -40, 8, blink, look)}
<ellipse cx="0" cy="-10" rx="26" ry="9" fill="#FF9F3A"/><ellipse cx="0" cy="{-4 + beak:.1f}" rx="22" ry="7" fill="#F28A1E"/>
<circle cx="-36" cy="-18" r="9" fill="#FFAA8A" opacity="0.6"/><circle cx="36" cy="-18" r="9" fill="#FFAA8A" opacity="0.6"/>
<path d="M-40 18 Q0 34 40 18 L40 30 Q0 46 -40 30Z" fill="#7EC8F2"/>
</g>'''


def fox(mouth=0.0, blink=False, walk=0.0, wave=0.0, look=0.0):
    sw = math.sin(2 * math.pi * walk)
    tail = 10 * math.sin(2 * math.pi * walk * 0.5)
    return f'''<g transform="translate(0 {-abs(sw)*5:.1f})">
<g transform="rotate({tail - 20:.1f} 40 90)"><path d="M40 90 Q120 80 130 20 Q110 40 80 40 Q60 60 40 90Z" fill="#F07A2A"/><path d="M118 34 Q126 22 130 20 Q122 36 108 40Z" fill="#FFFFFF"/></g>
<ellipse cx="-22" cy="{122 + 5*sw:.1f}" rx="18" ry="11" fill="#5A3A2A"/><ellipse cx="22" cy="{122 - 5*sw:.1f}" rx="18" ry="11" fill="#5A3A2A"/>
<ellipse cx="0" cy="66" rx="48" ry="58" fill="#F07A2A"/><ellipse cx="0" cy="78" rx="26" ry="36" fill="#FFF4E6"/>
<g transform="rotate({-110*wave:.1f} 40 40)"><ellipse cx="48" cy="64" rx="12" ry="26" fill="#E0661A"/></g><ellipse cx="-48" cy="64" rx="12" ry="26" fill="#E0661A"/>
<path d="M-60 -50 L-44 -124 L-10 -82Z" fill="#F07A2A"/><path d="M-50 -64 L-42 -108 L-22 -84Z" fill="#3A2A2A"/>
<path d="M60 -50 L44 -124 L10 -82Z" fill="#F07A2A"/><path d="M50 -64 L42 -108 L22 -84Z" fill="#3A2A2A"/>
<path d="M-62 -40 Q-60 -100 0 -100 Q60 -100 62 -40 Q40 10 0 12 Q-40 10 -62 -40Z" fill="#F07A2A"/>
<path d="M-50 -24 Q-26 -36 0 -6 Q26 -36 50 -24 Q34 12 0 14 Q-34 12 -50 -24Z" fill="#FFF4E6"/>
{_eyes(-24, 24, -50, 8, blink, look)}
<ellipse cx="0" cy="-14" rx="9" ry="7" fill="#2A1A1A"/>
{_mouth(0, 0, 9, mouth, "#8A2E2E")}
<circle cx="-40" cy="-20" r="8" fill="#FF9E8A" opacity="0.5"/><circle cx="40" cy="-20" r="8" fill="#FF9E8A" opacity="0.5"/>
<path d="M-40 18 L40 18 L30 34 L-30 34Z" fill="#5EC8F2"/>
</g>'''


def fish(mouth=0.0, blink=False, walk=0.0, wave=0.0, look=0.0):
    """Bubbles regarde vers la droite par défaut (sens = -1 pour regarder à gauche)."""
    fin = 10 * math.sin(2 * math.pi * walk + 1) + 20 * wave
    return f'''<g>
<path d="M-60 40 L-130 {0 - fin*0.3:.1f} L-130 {90 + fin*0.3:.1f}Z" fill="#3FA7D6"/>
<ellipse cx="0" cy="45" rx="90" ry="70" fill="#5EC8F2"/>
<ellipse cx="10" cy="70" rx="60" ry="34" fill="#BFEFFF"/>
<path d="M10 -20 Q-20 {-60 - fin:.1f} -50 -18Z" fill="#3FA7D6"/>
<g fill="#FFFFFF" opacity="0.5"><circle cx="-20" cy="30" r="10"/><circle cx="-44" cy="52" r="8"/><circle cx="-24" cy="70" r="7"/></g>
{_eyes(18, 52, 20, 11, blink, look)}
{_mouth(58, 58, 12, mouth, "#2E6F9E")}
<circle cx="70" cy="44" r="10" fill="#FF9EB0" opacity="0.6"/>
</g>'''


DRAW = {"fish": fish, "mimo": mimo, "owl": owl, "bunny": bunny, "star": star, "lamb": lamb, "kitten": kitten, "duck": duck, "fox": fox}


def draw(name, x, y, s, mouth=0.0, blink=False, walk=0.0, wave=0.0, facing=1, look=0.0, **kw):
    return (f'<g transform="translate({x:.1f} {y:.1f}) scale({s*facing:.3f} {s:.3f})">'
            f'<ellipse cx="0" cy="134" rx="62" ry="10" fill="#000000" opacity="0.12"/>'
            f'{DRAW[name](mouth=mouth, blink=blink, walk=walk, wave=wave, look=look, **kw)}</g>')
