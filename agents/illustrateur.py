"""Agent 4 — Illustrateur : dessine Mimo, les décors animés, les Shorts et les miniatures.
Animation : Mimo respire, ses « Zzz » s'envolent, la lune brille, les nuages dérivent,
des étoiles filantes passent, la caméra bouge doucement. Toutes les boucles sont parfaites
(la dernière image rejoint la première)."""
import math, random

FONT = "Fredoka, sans-serif"

THEMES = {
    "moon":   dict(name="Moonlight",      sky=("#141B47", "#3A3F8F"), prop="moon",  fx="stars",     blanket=("#8FB8E8", "#B9D4F3"), clouds=True),
    "clouds": dict(name="Dreamy Clouds",  sky=("#2B2259", "#8A6FB8"), prop="cloud", fx="stars",     blanket=("#F4A9C0", "#F9CEDB"), clouds=True),
    "ocean":  dict(name="Calm Ocean",     sky=("#0E2A47", "#1F6B8C"), prop="boat",  fx="stars",     blanket=("#F2C46D", "#F8DFA6"), clouds=False),
    "snow":   dict(name="Snowy Night",    sky=("#16244A", "#4E6A9E"), prop="moon",  fx="snow",      blanket=("#E7EEF9", "#FFFFFF"), clouds=True),
    "forest": dict(name="Firefly Forest", sky=("#0F2A24", "#2E5B4A"), prop="moon",  fx="fireflies", blanket=("#A8D5A2", "#CDEBC8"), clouds=False),
    "rain":   dict(name="Rainy Night",    sky=("#1C2433", "#4A5A75"), prop="cloud", fx="rain",      blanket=("#9EC3E6", "#C6DDF2"), clouds=True),
}

BREATHS = 4  # respirations par boucle


def ease_out_back(x):
    x = min(max(x, 0.0), 1.0)
    c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2


def smooth(x):
    x = min(max(x, 0.0), 1.0)
    return x * x * (3 - 2 * x)


# ---------------------------------------------------------------- Mimo
def bear(blanket, t=0.0):
    b1, b2 = blanket
    br = math.sin(2 * math.pi * BREATHS * t)
    sy, sx = 1 + 0.035 * br, 1 + 0.012 * br
    dy = -2.2 * br
    body = f'''<g transform="translate(35 108) scale({sx:.4f} {sy:.4f}) translate(-35 -108)">
<ellipse cx="35" cy="58" rx="92" ry="50" fill="#B57D52"/>
<ellipse cx="95" cy="80" rx="30" ry="22" fill="#A06A42"/>
<path d="M-40 55 Q 40 20 125 60 Q 120 105 40 108 Q -20 108 -40 55Z" fill="{b1}"/>
<path d="M-40 55 Q 40 20 125 60" fill="none" stroke="{b2}" stroke-width="10" stroke-linecap="round"/>
<g fill="{b2}" opacity="0.55"><circle cx="10" cy="80" r="5"/><circle cx="45" cy="72" r="5"/><circle cx="80" cy="82" r="5"/><circle cx="30" cy="96" r="4"/><circle cx="68" cy="99" r="4"/></g>
</g>'''
    head = f'''<g transform="translate(0 {dy:.2f})">
<circle cx="-102" cy="-32" r="24" fill="#B57D52"/><circle cx="-102" cy="-32" r="12" fill="#E9B98F"/>
<circle cx="-12" cy="-38" r="24" fill="#B57D52"/><circle cx="-12" cy="-38" r="12" fill="#E9B98F"/>
<circle cx="-57" cy="15" r="64" fill="#C48A5C"/>
<ellipse cx="-57" cy="42" rx="28" ry="20" fill="#F2D6B3"/>
<ellipse cx="-57" cy="33" rx="10" ry="7" fill="#5A3624"/>
<ellipse cx="-60" cy="30" rx="3" ry="2" fill="#8A5A40"/>
<path d="M-64 48 Q -57 54 -50 48" fill="none" stroke="#5A3624" stroke-width="3.5" stroke-linecap="round"/>
<path d="M-90 12 Q -80 22 -70 12" fill="none" stroke="#5A3624" stroke-width="5" stroke-linecap="round"/>
<path d="M-44 12 Q -34 22 -24 12" fill="none" stroke="#5A3624" stroke-width="5" stroke-linecap="round"/>
<circle cx="-98" cy="36" r="10" fill="#F4A3A3" opacity="0.7"/><circle cx="-16" cy="36" r="10" fill="#F4A3A3" opacity="0.7"/>
<path d="M-118 -40 Q -60 -110 0 -45 Q -55 -70 -118 -40Z" fill="{b1}"/>
<path d="M-112 -42 Q -60 -96 -6 -47" fill="none" stroke="{b2}" stroke-width="6" stroke-linecap="round" opacity="0.8"/>
<circle cx="8" cy="-48" r="13" fill="#FFF4C9"/>
</g>'''
    return body + head


def zzz(t=0.0):
    """Trois « Z » qui montent en grandissant puis disparaissent, en boucle."""
    out = [f'<g font-family="{FONT}" font-weight="600" fill="#FFF4C9">']
    for i in range(3):
        p = (t * BREATHS / 2 + i / 3) % 1.0
        x = 18 + 95 * p + 10 * math.sin(2 * math.pi * p * 1.5)
        y = -90 - 120 * p
        size = 26 + 34 * p
        a = math.sin(math.pi * p) ** 1.3 * 0.9
        out.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size:.1f}" opacity="{a:.2f}">Z</text>')
    out.append("</g>")
    return "".join(out)


def prop_back(kind, theme, t=0.0):
    if kind == "moon":
        glow = 0.16 + 0.07 * math.sin(2 * math.pi * t)
        return (f'<defs><radialGradient id="mg_{theme}" cx="0.4" cy="0.7" r="0.8"><stop offset="0" stop-color="#FFF1B8"/>'
                f'<stop offset="1" stop-color="#FFD35C"/></radialGradient>'
                f'<radialGradient id="glow_{theme}"><stop offset="0.55" stop-color="#FFE9A0" stop-opacity="0.9"/>'
                f'<stop offset="1" stop-color="#FFE9A0" stop-opacity="0"/></radialGradient></defs>'
                f'<circle cx="0" cy="20" r="270" fill="url(#glow_{theme})" opacity="{glow:.3f}"/>'
                f'<path d="M-170.98 -56.27 A180 180 0 1 0 170.98 -56.27 A172 172 0 0 1 -170.98 -56.27Z" fill="url(#mg_{theme})"/>'
                '<g fill="#F2C24A" opacity="0.35"><circle cx="-120" cy="90" r="12"/><circle cx="60" cy="150" r="9"/><circle cx="130" cy="60" r="7"/></g>')
    if kind == "cloud":
        return ('<g fill="#F4F1FF"><circle cx="-130" cy="100" r="62"/><circle cx="-50" cy="80" r="90"/>'
                '<circle cx="60" cy="78" r="88"/><circle cx="150" cy="104" r="60"/>'
                '<rect x="-190" y="100" width="400" height="62" rx="31"/></g>'
                '<g fill="#D9D2F2" opacity="0.6"><rect x="-180" y="140" width="380" height="22" rx="11"/></g>')
    return ""


def prop_front(kind):
    if kind == "cloud":
        return '<g fill="#FFFFFF"><circle cx="-150" cy="128" r="40"/><circle cx="170" cy="130" r="38"/></g>'
    if kind == "boat":
        return ('<path d="M-185 75 L185 75 Q150 170 0 170 Q-150 170 -185 75Z" fill="#E8896B"/>'
                '<path d="M-178 95 L178 95" stroke="#F6C2A8" stroke-width="10"/>'
                '<circle cx="-90" cy="130" r="11" fill="#F6C2A8"/><circle cx="0" cy="135" r="11" fill="#F6C2A8"/>'
                '<circle cx="90" cy="130" r="11" fill="#F6C2A8"/>')
    return ""


def mimo(theme, x, y, s, t=0.0, rot=0.0):
    th = THEMES[theme]
    return (f'<g transform="translate({x:.1f},{y:.1f}) rotate({rot:.2f}) scale({s:.4f})">'
            f'{prop_back(th["prop"], theme, t)}{bear(th["blanket"], t)}{prop_front(th["prop"])}{zzz(t)}</g>')


# ---------------------------------------------------------------- Décor
def make_particles(theme, W, H, seed):
    r = random.Random(seed)
    fx = THEMES[theme]["fx"]
    k = W / 1280 if W > H else W / 1080 * 1.2
    n = {"stars": 150, "snow": 130, "fireflies": 45, "rain": 140}[fx]
    parts = []
    for _ in range(n):
        parts.append((fx, r.uniform(0, W), r.uniform(0, H), k, r.choice([1, 2, 3]), r.uniform(0, 6.28), r.random() < 0.22))
    if fx != "stars":
        for _ in range(70):
            parts.append(("stars", r.uniform(0, W), r.uniform(0, H * 0.6), k, r.choice([1, 2]), r.uniform(0, 6.28), False))
    extras = dict(
        shooting=[(r.uniform(0.05, 0.85), r.uniform(0.15, 0.95) * W, r.uniform(0.02, 0.3) * H) for _ in range(2)],
        clouds=[(r.uniform(-0.1, 1.0) * W, r.uniform(0.05, 0.45) * H, r.uniform(0.7, 1.4) * k, r.uniform(0, 6.28),
                 r.uniform(0.06, 0.12)) for _ in range(4)],
    )
    return parts, extras


def draw_particles(parts, W, H, t):
    out = []
    for fx, x, y, k, fr, ph, big in parts:
        if fx == "stars":
            a = 0.45 + 0.5 * (0.5 + 0.5 * math.sin(2 * math.pi * fr * t + ph))
            if big:
                s = 13 * k * (0.85 + 0.15 * math.sin(2 * math.pi * fr * t + ph))
                out.append(f'<path d="M{x:.1f} {y-s:.1f} Q{x:.1f} {y:.1f} {x+s:.1f} {y:.1f} Q{x:.1f} {y:.1f} {x:.1f} {y+s:.1f} '
                           f'Q{x:.1f} {y:.1f} {x-s:.1f} {y:.1f} Q{x:.1f} {y:.1f} {x:.1f} {y-s:.1f}Z" fill="#FFF4C9" opacity="{a:.2f}"/>')
            else:
                out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{2.2*k:.1f}" fill="#FFFFFF" opacity="{a*0.8:.2f}"/>')
        elif fx == "snow":
            yy = (y + t * H * fr) % H
            xx = x + 14 * k * math.sin(2 * math.pi * t * 2 + ph)
            out.append(f'<circle cx="{xx:.1f}" cy="{yy:.1f}" r="{3.5*k:.1f}" fill="#FFFFFF" opacity="0.85"/>')
        elif fx == "rain":
            yy = (y + t * H * (fr + 2)) % H
            out.append(f'<line x1="{x:.1f}" y1="{yy:.1f}" x2="{x-4*k:.1f}" y2="{yy+22*k:.1f}" stroke="#BFD3EE" '
                       f'stroke-width="{2*k:.1f}" opacity="0.45" stroke-linecap="round"/>')
        elif fx == "fireflies":
            xx = x + 40 * k * math.sin(2 * math.pi * fr * t + ph)
            yy = y + 30 * k * math.cos(2 * math.pi * t + ph)
            a = 0.3 + 0.7 * (0.5 + 0.5 * math.sin(2 * math.pi * fr * t * 2 + ph))
            out.append(f'<circle cx="{xx:.1f}" cy="{yy:.1f}" r="{15*k:.1f}" fill="#F7F3A1" opacity="{a*0.25:.2f}"/>'
                       f'<circle cx="{xx:.1f}" cy="{yy:.1f}" r="{5*k:.1f}" fill="#FDFBC8" opacity="{a:.2f}"/>')
    return "".join(out)


def shooting_stars(theme, extras, W, H, t):
    if THEMES[theme]["fx"] != "stars":
        return ""
    out = []
    k = W / 1280 if W > H else W / 1080 * 1.2
    for i, (start, x0, y0) in enumerate(extras["shooting"]):
        dur = 0.07
        u = (t - start) / dur
        if not 0 <= u <= 1:
            continue
        L = 260 * k
        hx, hy = x0 - L * 1.6 * u, y0 + L * 0.8 * u
        tx, ty = hx + L * 0.55, hy - L * 0.28
        a = math.sin(math.pi * u)
        gid = f"ss_{theme}_{i}"
        out.append(f'<defs><linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="{tx:.1f}" y1="{ty:.1f}" x2="{hx:.1f}" y2="{hy:.1f}">'
                   f'<stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/><stop offset="1" stop-color="#FFF8DC" stop-opacity="{a:.2f}"/></linearGradient></defs>'
                   f'<line x1="{tx:.1f}" y1="{ty:.1f}" x2="{hx:.1f}" y2="{hy:.1f}" stroke="url(#{gid})" stroke-width="{3*k:.1f}" stroke-linecap="round"/>'
                   f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="{3.2*k:.1f}" fill="#FFFFFF" opacity="{a:.2f}"/>')
    return "".join(out)


def drifting_clouds(theme, extras, W, H, t):
    if not THEMES[theme]["clouds"]:
        return ""
    out = []
    for x, y, s, ph, op in extras["clouds"]:
        xx = x + 70 * s * math.sin(2 * math.pi * t + ph)
        out.append(f'<g transform="translate({xx:.1f} {y:.1f}) scale({s:.3f})" fill="#FFFFFF" opacity="{op:.3f}">'
                   '<ellipse cx="0" cy="0" rx="120" ry="34"/><ellipse cx="-50" cy="-14" rx="60" ry="34"/>'
                   '<ellipse cx="40" cy="-22" rx="70" ry="40"/></g>')
    return "".join(out)


def waves(W, H, t, top=0.86, layers=(0, 1)):
    out = []
    for i, (col, base, amp) in enumerate([("#1A5577", top, 14), ("#14476A", top + 0.035, 10)]):
        if i not in layers:
            continue
        y0 = H * base
        pts = []
        for j in range(41):
            x = W * j / 40
            y = y0 + amp * (W / 1280) * math.sin(2 * math.pi * (j / 10 + t + i * 0.3))
            pts.append(f"{x:.1f},{y:.1f}")
        out.append(f'<path d="M0,{H} L{" L".join(pts)} L{W},{H}Z" fill="{col}"/>')
    return "".join(out)


def sky(theme, W, H):
    a, b = THEMES[theme]["sky"]
    return (f'<defs><linearGradient id="sky_{theme}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{a}"/>'
            f'<stop offset="1" stop-color="{b}"/></linearGradient>'
            f'<radialGradient id="vig_{theme}" cx="0.5" cy="0.5" r="0.75"><stop offset="0.6" stop-color="#000" stop-opacity="0"/>'
            f'<stop offset="1" stop-color="#000" stop-opacity="0.35"/></radialGradient></defs>'
            f'<rect width="{W}" height="{H}" fill="url(#sky_{theme})"/>')


def vignette(theme, W, H):
    return f'<rect width="{W}" height="{H}" fill="url(#vig_{theme})"/>'


def text(x, y, s, size, fill, weight=700, anchor="middle", shadow=True, opacity=1):
    base = f'font-family="{FONT}" font-weight="{weight}" font-size="{size}" text-anchor="{anchor}" opacity="{opacity:.3f}"'
    sh = f'<text x="{x+size*0.04:.0f}" y="{y+size*0.05:.0f}" {base} fill="#0B1030">{s}</text>' if shadow else ""
    return sh + f'<text x="{x:.0f}" y="{y:.0f}" {base} fill="{fill}">{s}</text>'


def scene_body(theme, W, H, t, pe, cam=1.0, watermark=True, mimo_dy=0.0, mimo_scale=1.0):
    """Contenu SVG d'une image du décor (sans la balise <svg>)."""
    parts, extras = pe
    portrait = H > W
    th = THEMES[theme]
    zoom = cam * (1 + 0.025 * (0.5 - 0.5 * math.cos(2 * math.pi * t)))
    body = [sky(theme, W, H), f'<g transform="translate({W/2:.1f} {H/2:.1f}) scale({zoom:.4f}) translate({-W/2:.1f} {-H/2:.1f})">',
            draw_particles(parts, W, H, t), shooting_stars(theme, extras, W, H, t), drifting_clouds(theme, extras, W, H, t)]
    if portrait:
        cy, sc, cx = H * 0.56, W / 1080 * 2.3, W / 2 + 30
    else:
        cy, sc, cx = H * 0.56 + mimo_dy * H / 720, H / 720 * 1.55 * mimo_scale, W / 2
    top = (cy + 135 * sc) / H
    if th["prop"] == "boat":
        body.append(waves(W, H, t, top, layers=(0,)))
    rot = 1.5 * math.sin(2 * math.pi * t + 0.6)
    bob = (14 if portrait else 10 * H / 720) * math.sin(2 * math.pi * t)
    body.append(mimo(theme, cx, cy + bob, sc, t, rot))
    if th["prop"] == "boat":
        body.append(waves(W, H, t, top, layers=(1,)))
    body.append("</g>")
    body.append(vignette(theme, W, H))
    if watermark:
        if portrait:
            body.append(text(40, 130, "Sleepy Mimo", 40, "#FFF4C9", 600, "start", False, 0.6))
        else:
            body.append(text(W - 30 * W / 1280, 50 * W / 1280, "Sleepy Mimo", int(26 * W / 1280), "#FFF4C9", 600, "end", False, 0.55))
    return "".join(body)


def svg(W, H, body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{body}</svg>'


# ---------------------------------------------------------------- Générateurs d'images
def loop_frames(theme, W, H, pe, n):
    """n images d'une boucle parfaite du décor."""
    for k in range(n):
        yield svg(W, H, scene_body(theme, W, H, k / n, pe))


def transition_frames(theme_a, pe_a, theme_b, pe_b, W, H, n_loop, n_trans):
    """Fondu enchaîné entre deux décors. A continue après la fin de sa boucle,
    B arrive juste avant le début de la sienne : aucune saute à la jonction."""
    for k in range(n_trans):
        a = scene_body(theme_a, W, H, k / n_loop, pe_a, watermark=False)
        b = scene_body(theme_b, W, H, (n_loop - n_trans + k) / n_loop, pe_b)
        o = smooth((k + 0.5) / n_trans)
        yield svg(W, H, f'<g>{a}</g><g opacity="{o:.3f}">{b}</g>')


def short_frames(theme, pe, hook, caption, fps, seconds, n_loop, W=1080, H=1920):
    """Short vertical : zoom d'ouverture + accroche qui « pop », légende, puis appel final."""
    total = int(fps * seconds)
    for k in range(total):
        ts = k / fps
        t = (k % n_loop) / n_loop
        cam = 1.0 + 0.18 * (1 - smooth(ts / 1.6))
        parts = [scene_body(theme, W, H, t, pe, cam=cam)]
        cx, y1 = W / 2, H * 0.17
        hs = min(112, int(980 / (0.56 * max(len(hook[0]), len(hook[1])))))
        cs = min(84, int(980 / (0.56 * max(len(caption[0]), len(caption[1])))))
        # Accroche (0 à 3,7 s)
        if ts < 3.7:
            pop = ease_out_back(ts / 0.45) if ts < 0.45 else 1.0
            op = 1.0 if ts < 3.2 else 1 - smooth((ts - 3.2) / 0.5)
            s = 0.55 + 0.45 * pop
            parts.append(f'<g opacity="{op:.3f}" transform="translate({cx} {y1+60}) scale({s:.3f}) translate({-cx} {-(y1+60)})">'
                         + text(cx, y1, hook[0], hs, "#FFFFFF") + text(cx, y1 + hs * 1.12, hook[1], hs, "#FFD35C") + "</g>")
        # Légende (après l'accroche, jusqu'à la fin - 4,5 s)
        end_cta = seconds - 4.5
        if 3.7 <= ts < end_cta + 0.5:
            op = smooth((ts - 3.7) / 0.5) * (1 - smooth((ts - end_cta) / 0.5))
            parts.append(f'<g opacity="{op:.3f}">' + text(cx, y1, caption[0], cs, "#FFF4C9") + text(cx, y1 + cs * 1.2, caption[1], cs, "#FFD35C") + "</g>")
        # Appel final
        if ts >= end_cta:
            u = (ts - end_cta) / 0.5
            op = smooth(u)
            pulse = 1 + 0.04 * math.sin(2 * math.pi * (ts - end_cta) * 1.2)
            parts.append(f'<g opacity="{op:.3f}" transform="translate({cx} {y1+50}) scale({pulse:.3f}) translate({-cx} {-(y1+50)})">'
                         + text(cx, y1, "More lullabies", 92, "#FFFFFF") + text(cx, y1 + 110, "with Mimo", 92, "#FFD35C") + "</g>")
        yield svg(W, H, "".join(parts))


# ---------------------------------------------------------------- Miniature
def thumbnail(theme, big, line1, line2, path, seed=0):
    import cairosvg
    W, H = 1280, 720
    pe = make_particles(theme, W, H, seed)
    parts, extras = pe
    body = [sky(theme, W, H), draw_particles(parts, W, H, 0.1), drifting_clouds(theme, extras, W, H, 0.1)]
    if THEMES[theme]["prop"] == "boat":
        body.append(waves(W, H, 0.1, (400 + 135 * 1.5) / H, layers=(0,)))
    body.append(mimo(theme, 400, 400, 1.5, 0.0))
    if THEMES[theme]["prop"] == "boat":
        body.append(waves(W, H, 0.1, (400 + 135 * 1.5) / H, layers=(1,)))
    body.append(vignette(theme, W, H))
    bs = 190 if len(big) <= 3 else 150 if len(big) <= 6 else 115
    body.append(text(980, 350, big, bs, "#FFD35C"))
    body.append(text(980, 500, line1, 76 if len(line1) <= 9 else 58, "#FFFFFF"))
    body.append(text(980, 590, line2, 76 if len(line2) <= 9 else 58, "#FFFFFF"))
    cairosvg.svg2png(bytestring=svg(W, H, "".join(body)).encode(), write_to=path)
