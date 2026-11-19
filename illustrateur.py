"""Agent 4 — Illustrateur : dessine Mimo, les décors animés et les miniatures."""
import math, random, os, cairosvg

FONT = "Fredoka, sans-serif"

THEMES = {
    "moon":   dict(name="Moonlight",      sky=("#141B47", "#3A3F8F"), prop="moon",  fx="stars",     blanket=("#8FB8E8", "#B9D4F3")),
    "clouds": dict(name="Dreamy Clouds",  sky=("#2B2259", "#8A6FB8"), prop="cloud", fx="stars",     blanket=("#F4A9C0", "#F9CEDB")),
    "ocean":  dict(name="Calm Ocean",     sky=("#0E2A47", "#1F6B8C"), prop="boat",  fx="stars",     blanket=("#F2C46D", "#F8DFA6")),
    "snow":   dict(name="Snowy Night",    sky=("#16244A", "#4E6A9E"), prop="moon",  fx="snow",      blanket=("#E7EEF9", "#FFFFFF")),
    "forest": dict(name="Firefly Forest", sky=("#0F2A24", "#2E5B4A"), prop="moon",  fx="fireflies", blanket=("#A8D5A2", "#CDEBC8")),
    "rain":   dict(name="Rainy Night",    sky=("#1C2433", "#4A5A75"), prop="cloud", fx="rain",      blanket=("#9EC3E6", "#C6DDF2")),
}


def bear(blanket):
    b1, b2 = blanket
    return f'''<ellipse cx="35" cy="58" rx="92" ry="50" fill="#B57D52"/>
<ellipse cx="95" cy="80" rx="30" ry="22" fill="#A06A42"/>
<path d="M-40 55 Q 40 20 125 60 Q 120 105 40 108 Q -20 108 -40 55Z" fill="{b1}"/>
<path d="M-40 55 Q 40 20 125 60" fill="none" stroke="{b2}" stroke-width="10" stroke-linecap="round"/>
<circle cx="-102" cy="-32" r="24" fill="#B57D52"/><circle cx="-102" cy="-32" r="12" fill="#E9B98F"/>
<circle cx="-12" cy="-38" r="24" fill="#B57D52"/><circle cx="-12" cy="-38" r="12" fill="#E9B98F"/>
<circle cx="-57" cy="15" r="64" fill="#C48A5C"/>
<ellipse cx="-57" cy="42" rx="28" ry="20" fill="#F2D6B3"/>
<ellipse cx="-57" cy="33" rx="10" ry="7" fill="#5A3624"/>
<path d="M-64 48 Q -57 54 -50 48" fill="none" stroke="#5A3624" stroke-width="3.5" stroke-linecap="round"/>
<path d="M-90 12 Q -80 22 -70 12" fill="none" stroke="#5A3624" stroke-width="5" stroke-linecap="round"/>
<path d="M-44 12 Q -34 22 -24 12" fill="none" stroke="#5A3624" stroke-width="5" stroke-linecap="round"/>
<circle cx="-98" cy="36" r="10" fill="#F4A3A3" opacity="0.7"/><circle cx="-16" cy="36" r="10" fill="#F4A3A3" opacity="0.7"/>
<path d="M-118 -40 Q -60 -110 0 -45 Q -55 -70 -118 -40Z" fill="{b1}"/>
<circle cx="8" cy="-48" r="13" fill="#FFF4C9"/>'''


def zzz(t=0.0):
    a = 0.65 + 0.25 * math.sin(2 * math.pi * t)
    return (f'<g opacity="{a:.2f}" font-family="{FONT}" font-weight="600" fill="#FFF4C9">'
            '<text x="20" y="-95" font-size="34">z</text><text x="48" y="-128" font-size="44">Z</text>'
            '<text x="84" y="-168" font-size="56">Z</text></g>')


def prop_back(kind):
    if kind == "moon":
        return ('<defs><radialGradient id="mg" cx="0.4" cy="0.7" r="0.8"><stop offset="0" stop-color="#FFF1B8"/>'
                '<stop offset="1" stop-color="#FFD35C"/></radialGradient></defs>'
                '<path d="M-170.98 -56.27 A180 180 0 1 0 170.98 -56.27 A172 172 0 0 1 -170.98 -56.27Z" fill="url(#mg)"/>')
    if kind == "cloud":
        return ('<g fill="#F4F1FF"><circle cx="-130" cy="100" r="62"/><circle cx="-50" cy="80" r="90"/>'
                '<circle cx="60" cy="78" r="88"/><circle cx="150" cy="104" r="60"/>'
                '<rect x="-190" y="100" width="400" height="62" rx="31"/></g>')
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
    return (f'<g transform="translate({x:.1f},{y:.1f}) rotate({rot:.2f}) scale({s})">'
            f'{prop_back(th["prop"])}{bear(th["blanket"])}{prop_front(th["prop"])}{zzz(t)}</g>')


def make_particles(theme, W, H, seed):
    r = random.Random(seed)
    fx = THEMES[theme]["fx"]
    k = W / 1280 if W > H else W / 1080 * 1.2
    n = {"stars": 130, "snow": 110, "fireflies": 40, "rain": 120}[fx]
    parts = []
    for _ in range(n):
        parts.append((fx, r.uniform(0, W), r.uniform(0, H), k, r.choice([1, 2, 3]), r.uniform(0, 6.28), r.random() < 0.22))
    if fx != "stars":
        for _ in range(60):
            parts.append(("stars", r.uniform(0, W), r.uniform(0, H * 0.6), k, r.choice([1, 2]), r.uniform(0, 6.28), False))
    return parts


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
    return (f'<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{a}"/>'
            f'<stop offset="1" stop-color="{b}"/></linearGradient></defs><rect width="{W}" height="{H}" fill="url(#sky)"/>')


def text(x, y, s, size, fill, weight=700, anchor="middle", shadow=True, opacity=1):
    base = f'font-family="{FONT}" font-weight="{weight}" font-size="{size}" text-anchor="{anchor}" opacity="{opacity}"'
    sh = f'<text x="{x+size*0.04:.0f}" y="{y+size*0.05:.0f}" {base} fill="#0B1030">{s}</text>' if shadow else ""
    return sh + f'<text x="{x}" y="{y}" {base} fill="{fill}">{s}</text>'


def scene(theme, W, H, t, parts, overlay=""):
    portrait = H > W
    body = [sky(theme, W, H), draw_particles(parts, W, H, t)]
    if THEMES[theme]["prop"] == "boat":
        cy, sc = (H * 0.56, W / 1080 * 2.3) if portrait else (H * 0.56, H / 720 * 1.55)
        top = (cy + 135 * sc) / H
        body.append(waves(W, H, t, top, layers=(0,)))
    rot = 1.5 * math.sin(2 * math.pi * t + 0.6)
    if portrait:
        s = W / 1080 * 2.3
        body.append(mimo(theme, W / 2 + 30, H * 0.56 + 14 * math.sin(2 * math.pi * t), s, t, rot))
    else:
        s = H / 720 * 1.55
        body.append(mimo(theme, W / 2, H * 0.56 + 10 * math.sin(2 * math.pi * t), s, t, rot))
    if THEMES[theme]["prop"] == "boat":
        body.append(waves(W, H, t, top, layers=(1,)))
    body.append(overlay)
    body.append(text(W - 30, H - 30, "Sleepy Mimo", 40 if portrait else 26, "#FFF4C9", 600, "end", False, 0.55))
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{"".join(body)}</svg>'


def render_loop(theme, W, H, out_dir, seed, overlay="", fps=24, seconds=12):
    """Rend une boucle parfaite (la fin rejoint le début) de `seconds` secondes."""
    os.makedirs(out_dir, exist_ok=True)
    parts = make_particles(theme, W, H, seed)
    n = fps * seconds
    for k in range(n):
        svg = scene(theme, W, H, k / n, parts, overlay)
        cairosvg.svg2png(bytestring=svg.encode(), write_to=os.path.join(out_dir, f"{k:04d}.png"))
    return n


def thumbnail(theme, big, line1, line2, path, seed=0):
    W, H = 1280, 720
    parts = make_particles(theme, W, H, seed)
    body = [sky(theme, W, H), draw_particles(parts, W, H, 0.1)]
    if THEMES[theme]["prop"] == "boat":
        body.append(waves(W, H, 0.1))
    body.append(mimo(theme, 400, 400, 1.5, 0.25))
    bs = 190 if len(big) <= 3 else 150 if len(big) <= 6 else 115
    body.append(text(980, 350, big, bs, "#FFD35C"))
    body.append(text(980, 500, line1, 76 if len(line1) <= 9 else 58, "#FFFFFF"))
    body.append(text(980, 590, line2, 76 if len(line2) <= 9 else 58, "#FFFFFF"))
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">{"".join(body)}</svg>'
    cairosvg.svg2png(bytestring=svg.encode(), write_to=path)
