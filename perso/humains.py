"""Les personnages humains de « Rayen & Yakin » (style dessin animé, vue de face).
Chaque personnage est dessiné les pieds en (0, 0) ; hauteur ~560 px à l'échelle 1."""
import math

CAST = {
    "rayen": dict(name="رايان", skin="#D9A57B", skin2="#C48E66", hair="#1E1612", style="fade", eyes="#4A2C1A",
                  top="#D63A3A", top2="#B02A2E", pants="#2F4E7A", shoes="#F4F4F4", beard=True, girl=False, h=1.0),
    "yakin": dict(name="يقين", skin="#6E4128", skin2="#57311D", hair="#120A06", style="long", eyes="#3A2416",
                  top="#F2C14E", top2="#DFA92E", pants="#F2C14E", shoes="#C8434E", girl=True, clip="#FFFFFF", h=0.95),
    "yassmine": dict(name="ياسمين", skin="#EBBE9A", skin2="#D6A57F", hair="#9A4E1E", style="bob", eyes="#4A2C1A",
                     top="#E8559A", top2="#C93F80", pants="#2F3550", shoes="#FFFFFF", girl=True, earrings=True, h=0.94),
    "salah": dict(name="عم صالح", skin="#D9A57B", skin2="#C48E66", hair="#D8D8D8", style="chechia", eyes="#3A2416",
                  top="#8A7350", top2="#6E5A3C", pants="#5A4A34", shoes="#3A2A1A", mustache=True, girl=False, h=0.93, wide=1.16),
    "hamma": dict(name="حمّة", skin="#C99168", skin2="#B27C55", hair="#15100D", style="curly", eyes="#3A2416",
                  top="#2FA36B", top2="#24865A", pants="#3B3B46", shoes="#E9E2D0", cap="#F2F2F2", girl=False, h=0.97, wide=1.18),
    "sarra": dict(name="سارة", skin="#E2B08A", skin2="#CC9670", hair="#5B2E1E", style="bob", eyes="#5A3A22",
                  top="#8D5BD6", top2="#7446BC", pants="#33405E", shoes="#FFFFFF", glasses=True, girl=True, h=0.93),
    "skander": dict(name="سكندر", skin="#E6B992", skin2="#D0A07A", hair="#2A1C10", style="gel", eyes="#3B2A1A",
                    top="#2E7DD1", top2="#2266B0", pants="#E8E1D2", shoes="#6B4A32", sunglasses=True, girl=False, h=1.06),
    "mama": dict(name="ماما", skin="#D9A57B", skin2="#C48E66", hair="#2A1A12", style="scarf", eyes="#4A2C1A",
                 top="#3E9C9C", top2="#2F8080", pants="#3E9C9C", shoes="#6B4A32", girl=True, h=0.92, wide=1.12),
}
NAMES = {k: v["name"] for k, v in CAST.items()}
NAMES["narrator"] = ""
COLORS = {"yassmine": "#FF9AD0", "salah": "#E8C890", "rayen": "#FF8A7A", "yakin": "#FFD27A", "hamma": "#8CF0B0", "sarra": "#D2B0FF", "skander": "#9EC3FF", "mama": "#7FE0D8", "narrator": "#FFFFFF"}

# angles des bras (épaule, coude) en degrés : 0 = bras le long du corps, + = vers l'extérieur / le haut
GEST = {
    "idle": ((8, 6), (8, 6)), "wave": ((8, 6), (150, 25)), "point": ((8, 6), (92, 4)),
    "hips": ((38, -115), (38, -115)), "fist": ((10, 6), (125, 70)), "shy": ((10, 8), (150, 125)),
    "up": ((150, 15), (150, 15)), "open": ((42, 32), (42, 32)), "heart": ((22, 140), (22, 140)),
    "hold": ((8, 6), (35, 95)), "facepalm": ((10, 6), (55, 150)), "shrug": ((60, -90), (60, -90)),
    "think": ((22, 140), (60, 150)), "phone": ((8, 6), (40, 150)),
}


def _rot(x, y, a):
    c, s = math.cos(a), math.sin(a)
    return x * c - y * s, x * s + y * c


def _arm(side, sh, el, col, skin, t, wob=0.0, L1=95, L2=92):
    """side : -1 (gauche de l'écran) / +1 ; renvoie (svg, position de la main)."""
    sx, sy = side * 74, -352
    ex = sx + math.sin(math.radians(sh + wob)) * L1 * side
    ey = sy + math.cos(math.radians(sh + wob)) * L1
    a2 = sh + wob + el
    hx = ex + math.sin(math.radians(a2)) * L2 * side
    hy = ey + math.cos(math.radians(a2)) * L2
    g = (f'<path d="M{sx:.1f} {sy:.1f} L{ex:.1f} {ey:.1f}" stroke="{col}" stroke-width="40" stroke-linecap="round"/>'
         f'<path d="M{ex:.1f} {ey:.1f} L{hx:.1f} {hy:.1f}" stroke="{skin}" stroke-width="30" stroke-linecap="round"/>'
         f'<path d="M{ex:.1f} {ey:.1f} L{(ex*0.7+hx*0.3):.1f} {(ey*0.7+hy*0.3):.1f}" stroke="{col}" stroke-width="38" stroke-linecap="round"/>'
         f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="19" fill="{skin}"/>')
    return g, (hx, hy)


def _hair_back(c):
    h, st = c["hair"], c["style"]
    if st == "long":
        return (f'<path d="M-98 -500 Q-120 -330 -112 -250 Q-60 -230 0 -236 Q60 -230 112 -250 Q120 -330 98 -500 Z" fill="{h}"/>')
    if st == "scarf":
        return f'<path d="M-104 -470 Q-110 -330 -80 -300 L80 -300 Q110 -330 104 -470 Z" fill="#C8546E"/>'
    return ""


def _hair_front(c, t):
    h, st = c["hair"], c["style"]
    if st == "fade":
        return (f'<path d="M-82 -500 Q-88 -590 -20 -604 Q40 -618 78 -582 Q96 -556 84 -500 Q70 -540 30 -548 Q-20 -556 -60 -530 Q-74 -520 -82 -500Z" fill="{h}"/>'
                f'<path d="M-84 -500 Q-90 -470 -86 -446 L-78 -446 Q-80 -480 -74 -505Z" fill="{h}" opacity="0.55"/>'
                f'<path d="M84 -500 Q90 -470 86 -446 L78 -446 Q80 -480 74 -505Z" fill="{h}" opacity="0.55"/>')
    if st == "long":
        sw = 4 * math.sin(2 * math.pi * t * 0.4)
        clip = f'<g transform="translate(62 -552)"><circle r="13" fill="{c.get("clip","#fff")}"/><circle r="5" fill="#FFD84A"/>' + \
            "".join(f'<circle cx="{11*math.cos(a):.1f}" cy="{11*math.sin(a):.1f}" r="7" fill="#FFFFFF"/>' for a in [i*2*math.pi/5 for i in range(5)]) + \
            '<circle r="5" fill="#FFD84A"/></g>'
        return (f'<path d="M-92 -470 Q-100 -600 0 -606 Q100 -600 92 -470 Q84 -540 30 -556 Q-10 -520 -60 -540 Q-84 -520 -92 -470Z" fill="{h}"/>'
                f'<path d="M-92 -480 Q{-112+sw:.1f} -380 {-104+sw:.1f} -300 L-84 -300 Q-90 -400 -78 -470Z" fill="{h}"/>'
                f'<path d="M92 -480 Q{112+sw:.1f} -380 {104+sw:.1f} -300 L84 -300 Q90 -400 78 -470Z" fill="{h}"/>' + clip)
    if st == "curly":
        bumps = "".join(f'<circle cx="{x}" cy="{y}" r="26" fill="{h}"/>' for x, y in
                        [(-70, -530), (-42, -566), (-6, -580), (32, -572), (66, -546), (80, -512), (-82, -500)])
        cap = c.get("cap")
        if cap:
            return (bumps + f'<path d="M-86 -536 Q-80 -616 0 -620 Q80 -616 86 -536 Z" fill="{cap}"/>'
                    f'<path d="M-86 -538 L86 -538" stroke="#D9D9D9" stroke-width="8"/>'
                    f'<path d="M-60 -540 Q-110 -560 -140 -534 Q-100 -526 -60 -530Z" fill="{cap}"/>')
        return bumps
    if st == "bob":
        return (f'<path d="M-96 -470 Q-108 -604 0 -608 Q108 -604 96 -470 L96 -420 Q100 -400 84 -404 L80 -500 Q40 -540 -10 -536 Q-60 -540 -80 -500 L-84 -404 Q-100 -400 -96 -420Z" fill="{h}"/>')
    if st == "gel":
        return (f'<path d="M-82 -505 Q-90 -600 0 -612 Q60 -618 96 -590 Q70 -600 50 -592 Q90 -570 84 -505 Q60 -560 0 -560 Q-50 -556 -82 -505Z" fill="{h}"/>')
    if st == "chechia":
        return (f'<path d="M-86 -470 Q-92 -420 -80 -400 L-70 -404 Q-80 -440 -76 -480Z" fill="{h}"/>'
                f'<path d="M86 -470 Q92 -420 80 -400 L70 -404 Q80 -440 76 -480Z" fill="{h}"/>'
                '<path d="M-74 -520 Q-80 -600 0 -604 Q80 -600 74 -520 Q0 -540 -74 -520Z" fill="#C21E2E"/>'
                '<path d="M-74 -522 Q0 -540 74 -522" stroke="#9A1422" stroke-width="6" fill="none"/>'
                '<path d="M0 -602 Q30 -610 46 -580 L52 -540" stroke="#111" stroke-width="7" fill="none"/>'
                '<path d="M46 -548 L40 -520 M52 -546 L54 -518 M58 -548 L66 -522" stroke="#111" stroke-width="5"/>')
    if st == "scarf":
        return ('<path d="M-96 -480 Q-100 -620 0 -620 Q100 -620 96 -480 Q90 -560 0 -566 Q-90 -560 -96 -480Z" fill="#C8546E"/>'
                '<path d="M-96 -480 Q-96 -430 -80 -400 L-70 -404 Q-84 -440 -84 -480Z" fill="#C8546E"/>'
                '<path d="M96 -480 Q96 -430 80 -400 L70 -404 Q84 -440 84 -480Z" fill="#C8546E"/>'
                '<path d="M-90 -540 Q0 -580 90 -540" stroke="#F2C14E" stroke-width="6" fill="none"/>')
    return ""


def _face(c, mouth, blink, look, emo, t):
    lx = 9 * look
    eye_y, ex = -462, 33
    out = []
    skin = c["skin"]
    # sourcils
    brow = {"angry": (14, -10), "sad": (-12, 6), "surprised": (0, -14), "shy": (-6, 2), "love": (-4, -6),
            "laugh": (0, -6), "happy": (0, -4), "worried": (-12, 4), "smug": (8, -4)}.get(emo, (0, 0))
    ang, dy = brow
    for s in (-1, 1):
        bx = s * ex + lx
        out.append(f'<path d="M{bx - 20:.1f} {eye_y - 34 + dy + (ang if s < 0 else -ang) * 0.5 * -1:.1f} '
                   f'L{bx + 20:.1f} {eye_y - 34 + dy + (-ang if s < 0 else ang) * 0.5 * -1:.1f}" '
                   f'stroke="{c["hair"]}" stroke-width="8" stroke-linecap="round"/>')
    # yeux
    closed = blink or emo == "laugh"
    for s in (-1, 1):
        x = s * ex + lx
        if closed:
            if emo == "laugh":
                out.append(f'<path d="M{x-15} {eye_y+4} Q{x} {eye_y-14} {x+15} {eye_y+4}" stroke="#2A1A12" stroke-width="6" fill="none" stroke-linecap="round"/>')
            else:
                out.append(f'<path d="M{x-15} {eye_y} Q{x} {eye_y+9} {x+15} {eye_y}" stroke="#2A1A12" stroke-width="6" fill="none" stroke-linecap="round"/>')
            continue
        r = 17 if emo == "surprised" else 15
        out.append(f'<ellipse cx="{x:.1f}" cy="{eye_y}" rx="{r}" ry="{r+4}" fill="#FFFFFF"/>')
        if emo == "love":
            hx, hy = x + look * 3, eye_y
            out.append(f'<path d="M{hx:.1f} {hy+9:.1f} C{hx-20:.1f} {hy-4:.1f} {hx-8:.1f} {hy-18:.1f} {hx:.1f} {hy-6:.1f} C{hx+8:.1f} {hy-18:.1f} {hx+20:.1f} {hy-4:.1f} {hx:.1f} {hy+9:.1f}Z" fill="#FF4D7A"/>')
        else:
            px = x + look * 4
            out.append(f'<circle cx="{px:.1f}" cy="{eye_y+2}" r="10.5" fill="{c["eyes"]}"/><circle cx="{px:.1f}" cy="{eye_y+2}" r="5.5" fill="#120A06"/>'
                       f'<circle cx="{px+4:.1f}" cy="{eye_y-3}" r="3.6" fill="#FFFFFF"/>')
        if c.get("girl"):
            out.append(f'<path d="M{x-17:.1f} {eye_y-12} Q{x:.1f} {eye_y-24} {x+18:.1f} {eye_y-12}" stroke="#1A100A" stroke-width="4" fill="none"/>')
    if c.get("glasses"):
        out.append(f'<g fill="none" stroke="#3A2A40" stroke-width="5"><circle cx="{-ex+lx:.1f}" cy="{eye_y}" r="25"/><circle cx="{ex+lx:.1f}" cy="{eye_y}" r="25"/>'
                   f'<path d="M{-ex+25+lx:.1f} {eye_y} L{ex-25+lx:.1f} {eye_y}"/></g>')
    if c.get("sunglasses"):
        out.append(f'<g fill="#1A1A22"><rect x="{-ex-26+lx:.1f}" y="{eye_y-18}" width="52" height="34" rx="12"/><rect x="{ex-26+lx:.1f}" y="{eye_y-18}" width="52" height="34" rx="12"/></g>'
                   f'<path d="M{-ex+26+lx:.1f} {eye_y-6} L{ex-26+lx:.1f} {eye_y-6}" stroke="#1A1A22" stroke-width="6"/>'
                   f'<path d="M{-ex-14+lx:.1f} {eye_y-10} L{-ex-2+lx:.1f} {eye_y-10}" stroke="#FFFFFF" stroke-width="4" opacity="0.6"/>')
    # nez
    out.append(f'<path d="M{lx*1.2-4:.1f} -446 Q{lx*1.2+6:.1f} -428 {lx*1.2-6:.1f} -424" stroke="{c["skin2"]}" stroke-width="5" fill="none" stroke-linecap="round"/>')
    # joues
    blush = 0.85 if emo in ("shy", "love") else 0.35
    out.append(f'<ellipse cx="{-52+lx:.1f}" cy="-424" rx="17" ry="10" fill="#FF7A8A" opacity="{blush}"/>'
               f'<ellipse cx="{52+lx:.1f}" cy="-424" rx="17" ry="10" fill="#FF7A8A" opacity="{blush}"/>')
    if c.get("mustache"):
        out.append(f'<path d="M{-40+lx:.1f} -414 Q{-20+lx:.1f} -432 {lx:.1f} -420 Q{20+lx:.1f} -432 {40+lx:.1f} -414 Q{20+lx:.1f} -410 {lx:.1f} -412 Q{-20+lx:.1f} -410 {-40+lx:.1f} -414Z" fill="{c["hair"]}"/>')
    if c.get("earrings"):
        out.append('<circle cx="-86" cy="-424" r="8" fill="#FFD84A"/><circle cx="86" cy="-424" r="8" fill="#FFD84A"/>')
    if c.get("beard"):
        out.append(f'<path d="M-74 -440 Q-70 -370 0 -362 Q70 -370 74 -440 Q66 -392 0 -386 Q-66 -392 -74 -440Z" fill="{c["hair"]}" opacity="0.32"/>')
    # bouche
    mx, my = lx * 1.1, -400
    m = max(0.0, min(1.0, mouth))
    if m > 0.1:
        h = 6 + 22 * m
        w = 22 if emo != "surprised" else 14
        out.append(f'<path d="M{mx-w:.1f} {my:.1f} Q{mx:.1f} {my+h*1.6:.1f} {mx+w:.1f} {my:.1f} Q{mx:.1f} {my+3:.1f} {mx-w:.1f} {my:.1f}Z" fill="#6E2430"/>'
                   f'<ellipse cx="{mx:.1f}" cy="{my+h*0.95:.1f}" rx="{w*0.5:.1f}" ry="{h*0.32:.1f}" fill="#F07A86"/>'
                   f'<path d="M{mx-w*0.7:.1f} {my+1:.1f} L{mx+w*0.7:.1f} {my+1:.1f}" stroke="#FFFFFF" stroke-width="5"/>')
    elif emo in ("angry", "sad", "worried"):
        out.append(f'<path d="M{mx-18:.1f} {my+8:.1f} Q{mx:.1f} {my-6:.1f} {mx+18:.1f} {my+8:.1f}" stroke="#6E2430" stroke-width="6" fill="none" stroke-linecap="round"/>')
    elif emo == "surprised":
        out.append(f'<ellipse cx="{mx:.1f}" cy="{my+4:.1f}" rx="9" ry="12" fill="#6E2430"/>')
    elif emo == "smug":
        out.append(f'<path d="M{mx-16:.1f} {my+2:.1f} Q{mx+4:.1f} {my+10:.1f} {mx+20:.1f} {my-6:.1f}" stroke="#6E2430" stroke-width="6" fill="none" stroke-linecap="round"/>')
    else:
        w = 22 if emo in ("happy", "laugh", "love") else 15
        out.append(f'<path d="M{mx-w:.1f} {my:.1f} Q{mx:.1f} {my+16:.1f} {mx+w:.1f} {my:.1f}" stroke="#6E2430" stroke-width="6" fill="none" stroke-linecap="round"/>')
    return "".join(out)


def draw(who, x, y, s=1.0, mouth=0.0, blink=False, walk=0.0, facing=1, look=0.0, emo="neutral",
         gesture="idle", t=0.0, talk=False, jump=0.0, prop=None, sit=False):
    c = CAST[who]
    s *= c.get("h", 1.0)
    wide = c.get("wide", 1.0)
    sw = math.sin(2 * math.pi * walk) if walk else 0.0
    bob = -abs(sw) * 10 - jump * 60 + (2.5 * math.sin(2 * math.pi * t * 0.5))
    breath = 1 + 0.008 * math.sin(2 * math.pi * t * 0.35)
    g_l, g_r = GEST.get(gesture, GEST["idle"])
    wob = 0.0
    if gesture == "wave":
        wob = 22 * math.sin(2 * math.pi * t * 2.2)
    elif gesture == "fist":
        wob = 10 * math.sin(2 * math.pi * t * 5)
    elif gesture == "open":
        wob = 10 * math.sin(2 * math.pi * t * 1.3)
    elif talk and gesture == "idle":
        wob = 6 * math.sin(2 * math.pi * t * 1.1)
    if walk:
        g_l, g_r = (g_l[0] + 18 * sw, g_l[1]), (g_r[0] - 18 * sw, g_r[1]) if gesture == "idle" else g_r
    skin, top, top2 = c["skin"], c["top"], c["top2"]
    parts = []
    parts.append(_hair_back(c))
    # jambes
    if sit:
        parts.append(f'<path d="M-40 -200 L-40 -120 L-46 -20" stroke="{c["pants"]}" stroke-width="44" stroke-linecap="round" fill="none"/>'
                     f'<path d="M40 -200 L40 -120 L46 -20" stroke="{c["pants"]}" stroke-width="44" stroke-linecap="round" fill="none"/>')
    elif c.get("girl") and c["style"] in ("long", "scarf"):
        for side in (-1, 1):
            a = side * 12 * sw
            fx, fy = _rot(0, 190, math.radians(a))
            parts.append(f'<path d="M{side*30} -190 L{side*30 - fx:.1f} {-190 + fy:.1f}" stroke="{skin if c["style"]=="long" else c["pants"]}" stroke-width="30" stroke-linecap="round"/>')
    else:
        for side in (-1, 1):
            a = side * 14 * sw
            fx, fy = _rot(0, 190, math.radians(a))
            parts.append(f'<path d="M{side*36} -205 L{side*36 - fx:.1f} {-200 + fy:.1f}" stroke="{c["pants"]}" stroke-width="46" stroke-linecap="round"/>')
    for side in (-1, 1):
        a = side * 14 * sw
        fx, _ = _rot(0, 190, math.radians(a))
        parts.append(f'<ellipse cx="{side*36 - fx + side*8:.1f}" cy="-8" rx="34" ry="17" fill="{c["shoes"]}"/>'
                     f'<ellipse cx="{side*36 - fx + side*8:.1f}" cy="0" rx="34" ry="6" fill="#00000030"/>')
    # bras arrière (derrière le torse) : aucun ; torse
    if c.get("girl") and c["style"] in ("long", "scarf"):
        parts.append(f'<path d="M-76 -360 Q-84 -260 -112 -170 L112 -170 Q84 -260 76 -360 Q0 -384 -76 -360Z" fill="{top}"/>'
                     f'<path d="M-112 -170 L112 -170 L106 -186 L-106 -186Z" fill="{top2}"/>'
                     + (f'<path d="M-50 -364 Q0 -330 50 -364" stroke="{top2}" stroke-width="8" fill="none"/>' if c["style"] == "long" else ""))
    else:
        parts.append(f'<path d="M{-80*wide:.0f} -362 Q{-90*wide:.0f} -280 {-74*wide:.0f} -196 L{74*wide:.0f} -196 Q{90*wide:.0f} -280 {80*wide:.0f} -362 Q0 -386 {-80*wide:.0f} -362Z" fill="{top}"/>'
                     f'<path d="M{-74*wide:.0f} -196 L{74*wide:.0f} -196 L{72*wide:.0f} -214 L{-72*wide:.0f} -214Z" fill="{top2}"/>')
        if who == "rayen":
            parts.append('<path d="M-30 -368 L0 -330 L30 -368" stroke="#B02A2E" stroke-width="7" fill="none"/>'
                         '<path d="M-20 -320 L-20 -250 M20 -320 L20 -250" stroke="#F4F4F4" stroke-width="5"/>')
        elif who == "hamma":
            parts.append('<path d="M-60 -330 L60 -330 M-70 -290 L70 -290 M-72 -250 L72 -250" stroke="#F2D24A" stroke-width="10" opacity="0.9"/>'
                         '<circle cx="0" cy="-310" r="14" fill="#F2D24A"/>')
        elif who == "skander":
            parts.append('<path d="M-26 -370 L0 -340 L26 -370" stroke="#FFFFFF" stroke-width="8" fill="none"/>')
    # cou + tête
    parts.append(f'<rect x="-22" y="-392" width="44" height="40" rx="12" fill="{c["skin2"]}"/>')
    parts.append(f'<ellipse cx="-84" cy="-450" rx="14" ry="20" fill="{c["skin2"]}"/><ellipse cx="84" cy="-450" rx="14" ry="20" fill="{c["skin2"]}"/>')
    parts.append(f'<ellipse cx="0" cy="-466" rx="84" ry="96" fill="{skin}"/>')
    parts.append(_face(c, mouth, blink, look * facing, emo, t))
    parts.append(_hair_front(c, t))
    # bras
    hands = {}
    for side, (sh, el) in ((-1, g_l), (1, g_r)):
        wb = wob if (side == 1 or gesture in ("open",)) else 0.0
        if gesture in ("up",) and talk:
            wb = 8 * math.sin(2 * math.pi * t * 2 + side)
        g, hp = _arm(side, sh, el, top, skin, t, wb)
        hands[side] = hp
        parts.append(g)
    if prop:
        hx, hy = hands[1]
        parts.append(PROPS[prop](hx, hy, t))
    tr = f'translate({x:.1f} {y + bob * s:.1f}) scale({s * facing:.3f} {s * breath:.3f})'
    return f'<g transform="{tr}">{"".join(parts)}</g>'


# ------------------------------------------------------------------ accessoires
def _jasmine(x, y, t):
    """Un « mechmoum » de jasmin : petit bouquet blanc sur une tige."""
    fl = "".join(f'<g transform="translate({x + dx:.1f} {y - 60 + dy:.1f})">' +
                 "".join(f'<ellipse cx="{6*math.cos(a):.1f}" cy="{6*math.sin(a):.1f}" rx="6" ry="4" transform="rotate({math.degrees(a):.0f} {6*math.cos(a):.1f} {6*math.sin(a):.1f})" fill="#FFFFFF"/>' for a in [i*2*math.pi/5 for i in range(5)]) +
                 '<circle r="3" fill="#F6E39A"/></g>' for dx, dy in [(0, 0), (-12, 8), (12, 8), (-6, -12), (7, -12), (0, 16)])
    return f'<path d="M{x} {y} L{x} {y-50}" stroke="#7FA65A" stroke-width="4"/>' + fl


def _phone(x, y, t):
    return f'<rect x="{x-14}" y="{y-34}" width="28" height="50" rx="6" fill="#20202A"/><rect x="{x-10}" y="{y-29}" width="20" height="38" rx="3" fill="#7CC8FF"/>'


def _coffee(x, y, t):
    st = "".join(f'<path d="M{x-6+i*8} {y-42} q-6 -12 0 -24 q6 -12 0 -24" stroke="#FFFFFF" stroke-width="3" fill="none" opacity="{0.4+0.3*math.sin(2*math.pi*t+i):.2f}"/>' for i in range(2))
    return st + f'<path d="M{x-16} {y-36} L{x+16} {y-36} L{x+12} {y} L{x-12} {y}Z" fill="#FFFFFF"/><rect x="{x-16}" y="{y-40}" width="32" height="6" fill="#5A3A22"/>'


def _bambalouni(x, y, t):
    return (f'<circle cx="{x}" cy="{y-18}" r="30" fill="#E8A54A"/><circle cx="{x}" cy="{y-18}" r="10" fill="#C77A2A"/>'
            + "".join(f'<circle cx="{x + 20*math.cos(a):.1f}" cy="{y - 18 + 20*math.sin(a):.1f}" r="2.5" fill="#FFFFFF"/>' for a in [i*0.7 for i in range(9)]))


def _letter(x, y, t):
    return (f'<rect x="{x-30}" y="{y-44}" width="60" height="42" rx="4" fill="#FFF7E6"/>'
            f'<path d="M{x-30} {y-44} L{x} {y-20} L{x+30} {y-44}" stroke="#E0C9A0" stroke-width="3" fill="none"/>'
            f'<path d="M{x} {y-14} c-8 -8 -2 -16 0 -10 c2 -6 8 2 0 10z" fill="#FF4D7A"/>')


def _ball(x, y, t):
    return f'<circle cx="{x}" cy="{y-24}" r="26" fill="#FFFFFF" stroke="#222" stroke-width="3"/><path d="M{x-10} {y-34} l10 -6 l10 6 l-4 12 l-12 0z" fill="#222"/>'


PROPS = {"jasmine": _jasmine, "phone": _phone, "coffee": _coffee, "bambalouni": _bambalouni, "letter": _letter, "ball": _ball}
