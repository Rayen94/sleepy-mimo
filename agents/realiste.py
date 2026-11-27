"""Saison 2 — style « 2.5D réaliste » : animaux de profil, sur quatre pattes, avec relief, pelage et lumière de la lune.
Même interface que personnages.py : fonction(mouth, blink, walk, wave, look) -> groupe SVG centré (pieds vers y=+130).
Les animaux regardent vers la droite ; draw() inverse l'image avec facing=-1."""
import math, random

LIGHT = "#CFE2FF"  # lumière de lune (reflet sur le dessus du pelage)


def _fur(seed, cx, cy, rx, ry, n, light, dark, ang=0.0):
    """Poils : deux chemins (clairs / sombres) faits de petits traits courbes, toujours les mêmes d'une image à l'autre."""
    r = random.Random(seed)
    a, b = [], []
    for i in range(n):
        t = r.uniform(0, 6.283); k = math.sqrt(r.uniform(0.05, 1))
        x, y = cx + rx * k * math.cos(t), cy + ry * k * math.sin(t)
        L = r.uniform(7, 14)
        dx, dy = math.cos(ang + r.uniform(-0.5, 0.5)) * L, math.sin(ang + r.uniform(-0.5, 0.5)) * L
        seg = f"M{x:.1f} {y:.1f} q{dx*0.3 + r.uniform(-2, 2):.1f} {dy*0.3 + 2:.1f} {dx:.1f} {dy:.1f}"
        (a if i % 2 else b).append(seg)
    return (f'<path d="{"".join(a)}" stroke="{light}" stroke-width="1.6" fill="none" opacity="0.38" stroke-linecap="round"/>'
            f'<path d="{"".join(b)}" stroke="{dark}" stroke-width="1.6" fill="none" opacity="0.42" stroke-linecap="round"/>')


def _eye(x, y, r, blink, look, lid="#2A1A12", iris="#6B3F1D"):
    if blink:
        return f'<path d="M{x-r} {y} Q{x} {y+r*0.9} {x+r} {y}" stroke="{lid}" stroke-width="{r*0.45:.1f}" fill="none" stroke-linecap="round"/>'
    px = x + look * r * 0.25
    return (f'<ellipse cx="{x}" cy="{y}" rx="{r*1.15:.1f}" ry="{r:.1f}" fill="#F3E9DA"/>'
            f'<circle cx="{px:.1f}" cy="{y}" r="{r*0.92:.1f}" fill="{iris}"/>'
            f'<circle cx="{px:.1f}" cy="{y}" r="{r*0.55:.1f}" fill="#120A06"/>'
            f'<circle cx="{px + r*0.3:.1f}" cy="{y - r*0.35:.1f}" r="{r*0.3:.1f}" fill="#FFFFFF"/>'
            f'<circle cx="{px - r*0.25:.1f}" cy="{y + r*0.3:.1f}" r="{r*0.14:.1f}" fill="#FFFFFF" opacity="0.7"/>'
            f'<path d="M{x-r*1.2:.1f} {y-r*0.15:.1f} Q{x} {y-r*1.5:.1f} {x+r*1.2:.1f} {y-r*0.1:.1f}" stroke="{lid}" stroke-width="{r*0.38:.1f}" fill="none" stroke-linecap="round"/>')


# ------------------------------------------------------------------ fiches des espèces
SP = {
    "bear": dict(base="#7B4A2A", hi="#B07845", lo="#3E2212", belly="#A9774C", muzzle="#CFA57C", nose="#1B120D", leg="#6A3E22", paw="#2F1A0E",
                 brx=74, bry=50, bx=-8, by=66, hx=82, hy=18, hr=40, snout=30, snr=22, ear=("round", 15), ear_in="#C48C66", leg_w=30, tail=("stub", 14),
                 tail_col="#7B4A2A", eye=7.5, iris="#5A3418", fur=70),
    "fox": dict(base="#D9661F", hi="#FF9B4A", lo="#7A2F0C", belly="#FFF1DF", muzzle="#FFF1DF", nose="#120C0A", leg="#2A1710", paw="#1A0F0A",
                brx=68, bry=36, bx=-12, by=72, hx=84, hy=24, hr=30, snout=46, snr=15, ear=("tall", 36), ear_in="#2A1710", leg_w=15, tail=("bush", 80),
                tail_col="#D9661F", eye=6.5, iris="#B8741A", fur=60),
    "hedgehog": dict(base="#8B6B4E", hi="#C09A74", lo="#3F2C1D", belly="#E3C9A6", muzzle="#E8D2B2", nose="#1A100B", leg="#B58E69", paw="#6A4A33",
                     brx=70, bry=48, bx=-10, by=74, hx=76, hy=64, hr=28, snout=36, snr=14, ear=("round", 8), ear_in="#D9B995", leg_w=16, tail=("none", 0),
                     tail_col="#8B6B4E", eye=5.5, iris="#241812", fur=30, spines=True),
    "bunny": dict(base="#9C8570", hi="#D0BBA0", lo="#4F4034", belly="#EADFCF", muzzle="#EADFCF", nose="#B86B66", leg="#8A7360", paw="#5A4A3C",
                  brx=52, bry=44, bx=-16, by=74, hx=62, hy=34, hr=30, snout=14, snr=13, ear=("long", 58), ear_in="#E3B3AC", leg_w=21, tail=("pom", 15),
                  tail_col="#F2EADC", eye=7.5, iris="#4A2A14", fur=55),
    "otter": dict(base="#6A4630", hi="#9C7250", lo="#2F1C0E", belly="#D2B591", muzzle="#DCC5A5", nose="#1A100B", leg="#5A3A26", paw="#2A180C",
                  brx=88, bry=30, bx=-16, by=92, hx=96, hy=62, hr=27, snout=17, snr=14, ear=("round", 8), ear_in="#C9A683", leg_w=17, tail=("taper", 100),
                  tail_col="#5A3A26", eye=6.2, iris="#2A180C", fur=60, whisk=True),
    "fawn": dict(base="#C07A3E", hi="#E8A862", lo="#6E3A16", belly="#F3E3CB", muzzle="#EBD3B0", nose="#2A1710", leg="#B06D38", paw="#3A2415",
                 brx=56, bry=28, bx=-12, by=46, hx=76, hy=-16, hr=25, snout=32, snr=12, ear=("leaf", 30), ear_in="#F0C9A4", leg_w=11, tail=("stub", 9),
                 tail_col="#F6EAD6", eye=7.5, iris="#2A1710", fur=40, spots=True),
    "beaver": dict(base="#7A5236", hi="#AE7C53", lo="#3A2415", belly="#B38A60", muzzle="#B38A60", nose="#1A100B", leg="#6A4630", paw="#2F1B0E",
                   brx=64, bry=40, bx=-12, by=80, hx=80, hy=44, hr=31, snout=15, snr=15, ear=("round", 9), ear_in="#4A2E1C", leg_w=21, tail=("paddle", 74),
                   tail_col="#3E2A1B", eye=6.5, iris="#2A180C", fur=55, teeth=True),
}


def _leg(hx, hip_y, fx, fy, w, col, paw, pcol, far=False):
    kx = (hx + fx) / 2 + (6 if not far else 4)
    d = f"M{hx:.1f} {hip_y} Q{kx:.1f} {(hip_y + fy)/2 - 2:.1f} {fx:.1f} {fy:.1f}"
    op = "" if not far else ' opacity="0.78"'
    return (f'<g{op}><path d="{d}" stroke="{col}" stroke-width="{w}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<ellipse cx="{fx + w*0.18:.1f}" cy="{fy + w*0.05:.1f}" rx="{w*0.72:.1f}" ry="{w*0.42:.1f}" fill="{pcol}"/></g>')


def _tail(S, wave, t):
    kind, ln = S["tail"]
    if kind == "none":
        return ""
    wag = 9 * math.sin(2 * math.pi * 1.4 * t) * (0.4 + wave) if kind == "bush" else 0
    bx, by = S["bx"] - S["brx"] + 8, S["by"] - 8
    if kind in ("stub", "pom"):
        return f'<ellipse cx="{bx:.1f}" cy="{by:.1f}" rx="{ln}" ry="{ln*0.8:.1f}" fill="{S["tail_col"]}"/>'
    if kind == "taper":
        sw = 5 * math.sin(2 * math.pi * 0.7 * t)
        return (f'<path d="M{bx+6:.1f} {by-8:.1f} Q{bx-ln*0.55:.1f} {by+16+sw:.1f} {bx-ln:.1f} {by+34+sw*2:.1f} Q{bx-ln*0.5:.1f} {by+26+sw:.1f} {bx+6:.1f} {by+14:.1f}Z" fill="url(#g_{S["id"]}_tail)"/>')
    if kind == "paddle":
        return (f'<g transform="rotate({-4 * math.sin(2 * math.pi * 0.5 * t):.1f} {bx:.1f} {by+14:.1f})"><ellipse cx="{bx-ln*0.6:.1f}" cy="{by+22:.1f}" rx="{ln*0.62:.1f}" ry="20" fill="{S["tail_col"]}"/>'
                f'<path d="M{bx-ln*1.0:.1f} {by+22:.1f} H{bx-ln*0.2:.1f} M{bx-ln*0.6:.1f} {by+6:.1f} V{by+38:.1f}" stroke="#241608" stroke-width="2" opacity="0.6"/></g>')
    return (f'<g transform="rotate({wag - 14:.1f} {bx:.1f} {by:.1f})">'
            f'<path d="M{bx:.1f} {by+10:.1f} Q{bx-ln*0.75:.1f} {by+34:.1f} {bx-ln:.1f} {by-4:.1f} Q{bx-ln*0.7:.1f} {by-36:.1f} {bx+6:.1f} {by-14:.1f}Z" fill="url(#g_{S["id"]}_tail)"/>'
            f'<path d="M{bx-ln*0.78:.1f} {by-28:.1f} Q{bx-ln*0.98:.1f} {by-14:.1f} {bx-ln:.1f} {by-4:.1f} Q{bx-ln*0.9:.1f} {by+14:.1f} {bx-ln*0.62:.1f} {by+20:.1f} Q{bx-ln*0.7:.1f} {by-4:.1f} {bx-ln*0.78:.1f} {by-28:.1f}Z" fill="#FFF1DF"/></g>')


def _ear(S, k):
    kind, sz = S["ear"]
    hr = S["hr"]
    if kind == "round":
        return (f'<circle cx="{-hr*0.15 + k*16:.1f}" cy="{-hr*0.85:.1f}" r="{sz}" fill="{S["lo"] if k else S["base"]}"/>'
                f'<circle cx="{-hr*0.15 + k*16:.1f}" cy="{-hr*0.8:.1f}" r="{sz*0.58:.1f}" fill="{S["ear_in"]}"/>')
    if kind == "long":
        x0 = -hr * 0.30 + k * 14
        return (f'<g transform="rotate({-12 + k * 10} {x0:.1f} {-hr*0.7:.1f})"><ellipse cx="{x0:.1f}" cy="{-hr*0.7 - sz*0.5:.1f}" rx="12" ry="{sz*0.55:.1f}" fill="{S["lo"] if k else S["base"]}"/>'
                f'<ellipse cx="{x0:.1f}" cy="{-hr*0.7 - sz*0.5:.1f}" rx="6.5" ry="{sz*0.42:.1f}" fill="{S["ear_in"]}"/></g>')
    if kind == "leaf":
        x0 = -hr * 0.2 + k * 16
        return (f'<g transform="rotate({-38 + k * 12} {x0:.1f} {-hr*0.6:.1f})"><path d="M{x0-8:.1f} {-hr*0.6:.1f} Q{x0-16:.1f} {-hr*0.6-sz:.1f} {x0:.1f} {-hr*0.6-sz*1.3:.1f} Q{x0+16:.1f} {-hr*0.6-sz:.1f} {x0+8:.1f} {-hr*0.6:.1f}Z" fill="{S["lo"] if k else S["base"]}"/>'
                f'<path d="M{x0-4:.1f} {-hr*0.64:.1f} Q{x0-8:.1f} {-hr*0.6-sz*0.9:.1f} {x0:.1f} {-hr*0.6-sz*1.1:.1f} Q{x0+8:.1f} {-hr*0.6-sz*0.9:.1f} {x0+4:.1f} {-hr*0.64:.1f}Z" fill="{S["ear_in"]}"/></g>')
    x0 = -hr * 0.35 + k * 20
    return (f'<path d="M{x0-14:.1f} {-hr*0.62:.1f} L{x0+2:.1f} {-hr-sz:.1f} L{x0+22:.1f} {-hr*0.55:.1f}Z" fill="{S["lo"] if k else S["base"]}"/>'
            f'<path d="M{x0-6:.1f} {-hr*0.66:.1f} L{x0+3:.1f} {-hr-sz*0.55:.1f} L{x0+15:.1f} {-hr*0.6:.1f}Z" fill="{S["ear_in"]}"/>')


def animal(name, mouth=0.0, blink=False, walk=0.0, wave=0.0, look=0.0, t=0.0, cap=None, pose=None):
    S = dict(SP[name]); S["id"] = name
    asleep = pose == "sleep"
    if asleep:
        blink, mouth, walk = True, 0.0, 0.0
        S = dict(S, by=S["by"] + 34, bry=S["bry"] * 0.82, hx=S["hx"] - 8, hy=S["hy"] + 62)
    sw = math.sin(2 * math.pi * walk)
    moving = walk > 0
    breath = 1 + 0.018 * math.sin(2 * math.pi * 0.45 * t)
    bob = -abs(sw) * 4 if moving else 0
    brx, bry, bx, by = S["brx"], S["bry"], S["bx"], S["by"]
    id_ = name
    defs = (f'<defs>'
            f'<radialGradient id="g_{id_}_body" cx="0.32" cy="0.18" r="0.95"><stop offset="0" stop-color="{S["hi"]}"/><stop offset="0.5" stop-color="{S["base"]}"/><stop offset="1" stop-color="{S["lo"]}"/></radialGradient>'
            f'<radialGradient id="g_{id_}_tail" cx="0.3" cy="0.3" r="1"><stop offset="0" stop-color="{S["hi"]}"/><stop offset="0.6" stop-color="{S["base"]}"/><stop offset="1" stop-color="{S["lo"]}"/></radialGradient>'
            f'<linearGradient id="g_{id_}_neck" gradientUnits="userSpaceOnUse" x1="0" y1="{by-bry}" x2="0" y2="{by+bry}"><stop offset="0" stop-color="{S["hi"]}"/><stop offset="0.45" stop-color="{S["base"]}"/><stop offset="1" stop-color="{S["lo"]}"/></linearGradient>'
            f'<linearGradient id="g_{id_}_muz" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{S["muzzle"]}" stop-opacity="0"/><stop offset="0.38" stop-color="{S["muzzle"]}"/><stop offset="1" stop-color="{S["muzzle"]}"/></linearGradient>'
            f'<linearGradient id="g_{id_}_belly" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{S["belly"]}" stop-opacity="0"/><stop offset="1" stop-color="{S["belly"]}" stop-opacity="0.9"/></linearGradient>'
            f'</defs>')
    # pattes : deux proches (devant/derrière), deux lointaines plus sombres
    fx, bxx = 52, -58
    if asleep:
        legs_far = ""
        legs_near = (f'<ellipse cx="{bxx + 20}" cy="{by + bry*0.85:.1f}" rx="{S["leg_w"]*0.9:.1f}" ry="{S["leg_w"]*0.5:.1f}" fill="{S["leg"]}"/>'
                     f'<ellipse cx="{S["hx"] + 8}" cy="{S["hy"] + 40:.1f}" rx="{S["leg_w"]*0.95:.1f}" ry="{S["leg_w"]*0.5:.1f}" fill="{S["paw"]}"/>')
    else:
        legs_far = (_leg(fx - 18, by + 18, fx - 18 - 20 * sw, 128 - max(0, -sw) * 10, S["leg_w"] * 0.92, S["lo"], 0, S["paw"], True)
                    + _leg(bxx + 18, by + 18, bxx + 18 + 20 * sw, 128 - max(0, sw) * 10, S["leg_w"] * 0.92, S["lo"], 0, S["paw"], True))
        legs_near = (_leg(bxx, by + 18, bxx - 20 * sw, 128 - max(0, -sw) * 10, S["leg_w"], S["leg"], 0, S["paw"])
                     + _leg(fx, by + 18, fx + 20 * sw, 128 - max(0, sw) * 10, S["leg_w"], S["leg"], 0, S["paw"]))
    hx0, hy0 = S["hx"], S["hy"]
    neck_svg = (f'<path d="M{bx + brx*0.35:.1f} {by - bry*0.95:.1f} Q{hx0 - S["hr"]*0.2:.1f} {hy0 - S["hr"]*0.9:.1f} {hx0 + S["hr"]*0.2:.1f} {hy0 - S["hr"]*0.2:.1f} '
             f'L{hx0 + S["hr"]*0.1:.1f} {hy0 + S["hr"]*0.85:.1f} Q{bx + brx*0.9:.1f} {by + bry*0.55:.1f} {bx + brx*0.55:.1f} {by + bry*0.8:.1f}Z" fill="url(#g_{id_}_neck)"/>'
             f'{_fur(hash(name) % 977 + 11, (bx + brx*0.6 + hx0)/2, (by + hy0)/2, 24, 30, 14, S["hi"], S["lo"], 0.4)}')
    body = (f'<g transform="translate(0 {bob:.1f})">{_tail(S, wave, t)}{legs_far}{neck_svg}'
            f'<ellipse cx="{bx}" cy="{by}" rx="{brx}" ry="{bry*breath:.1f}" fill="url(#g_{id_}_body)"/>'
            f'<ellipse cx="{bx + 4}" cy="{by + bry*0.45:.1f}" rx="{brx*0.82:.1f}" ry="{bry*0.55:.1f}" fill="url(#g_{id_}_belly)"/>'
            f'{_fur(hash(name) % 997, bx, by, brx * 0.92, bry * 0.9, S["fur"], S["hi"], S["lo"], 0.5)}')
    if S.get("spines"):
        r = random.Random(7); sp = []
        for i in range(320):
            a = r.uniform(3.2, 6.05); k = r.uniform(0.35, 1.0)
            x, y = bx + brx * 1.02 * k * math.cos(a), by + bry * 1.05 * k * math.sin(a)
            L = r.uniform(13, 24) * (0.5 + 0.5 * k)
            sp.append(f"M{x:.1f} {y:.1f} l{math.cos(a) * L:.1f} {math.sin(a) * L:.1f}")
        body += (f'<path d="{"".join(sp)}" stroke="#2B1D12" stroke-width="2.4" stroke-linecap="round" fill="none"/>'
                 f'<path d="{"".join(sp[::3])}" stroke="#D9B98E" stroke-width="1.6" stroke-linecap="round" fill="none" opacity="0.8"/>')
    if S.get("spots"):
        r2 = random.Random(11)
        body += "".join(f'<ellipse cx="{bx + r2.uniform(-brx*0.8, brx*0.8):.1f}" cy="{by - r2.uniform(0, bry*0.8):.1f}" rx="{r2.uniform(2.5, 4.5):.1f}" ry="{r2.uniform(2, 3.5):.1f}" fill="#FFF3DD" opacity="0.9"/>' for _ in range(26))
    # lumière de contour sur le dos
    body += (f'<path d="M{bx - brx*0.85:.1f} {by - bry*0.45:.1f} Q{bx} {by - bry*1.12:.1f} {bx + brx*0.8:.1f} {by - bry*0.55:.1f}" '
             f'stroke="{LIGHT}" stroke-width="3" fill="none" opacity="0.5" stroke-linecap="round"/>')
    body += legs_near
    # ---- tête
    hx, hy, hr, sn, snr = S["hx"], S["hy"], S["hr"], S["snout"], S["snr"]
    tilt = -4 * wave + 2 * math.sin(2 * math.pi * 0.35 * t) + (2 if moving else 0)
    jaw = 22 * mouth
    head = (f'<g transform="translate({hx} {hy + bob:.1f}) rotate({tilt:.1f})">'
            f'{_ear(S, 1)}'
            f'<ellipse cx="0" cy="0" rx="{hr}" ry="{hr*0.92:.1f}" fill="url(#g_{id_}_body)"/>'
            f'<path d="M{hr*0.3:.1f} {-snr*0.9:.1f} Q{hr + sn*0.8:.1f} {-snr*0.7:.1f} {hr + sn:.1f} {snr*0.15:.1f} Q{hr + sn*0.7:.1f} {snr*1.1:.1f} {hr*0.3:.1f} {snr*1.15:.1f}Z" fill="url(#g_{id_}_muz)"/>'
            f'<ellipse cx="{hr*0.1:.1f}" cy="{hr*0.25:.1f}" rx="{hr*0.62:.1f}" ry="{hr*0.5:.1f}" fill="{S["muzzle"]}" opacity="0.55"/>'
            f'{_ear(S, 0)}')
    if not S.get("spines"):
        head += _fur(hash(name) % 991 + 3, 0, 0, hr * 0.9, hr * 0.8, 22, S["hi"], S["lo"], 0.2)
    head += (f'<ellipse cx="{hr + sn - 3:.1f}" cy="{-snr*0.05:.1f}" rx="{snr*0.55:.1f}" ry="{snr*0.42:.1f}" fill="{S["nose"]}"/>'
             f'<ellipse cx="{hr + sn - 6:.1f}" cy="{-snr*0.28:.1f}" rx="{snr*0.2:.1f}" ry="{snr*0.1:.1f}" fill="#FFFFFF" opacity="0.55"/>')
    # bouche : trait fin, ou mâchoire qui s'ouvre
    jx, jy = hr * 0.55, snr * 1.1
    if mouth < 0.12:
        head += f'<path d="M{jx:.1f} {jy:.1f} Q{hr + sn*0.5:.1f} {jy + 3:.1f} {hr + sn - 4:.1f} {snr*0.45:.1f}" stroke="#2A1710" stroke-width="2.2" fill="none" stroke-linecap="round"/>'
    else:
        head += (f'<g transform="rotate({jaw:.1f} {jx:.1f} {jy:.1f})"><path d="M{jx:.1f} {jy:.1f} Q{hr + sn*0.5:.1f} {jy + 12:.1f} {hr + sn - 6:.1f} {snr*0.5:.1f} L{hr + sn - 6:.1f} {snr*0.2:.1f} Z" fill="{S["muzzle"]}"/>'
                 f'<path d="M{jx + 6:.1f} {jy - 1:.1f} Q{hr + sn*0.5:.1f} {jy + 8:.1f} {hr + sn - 10:.1f} {snr*0.4:.1f}" stroke="#7A2A2A" stroke-width="5" fill="none"/>'
                 f'<ellipse cx="{hr + sn*0.35:.1f}" cy="{jy + 5:.1f}" rx="{sn*0.22:.1f}" ry="3.5" fill="#E8838A"/></g>')
    if S.get("whisk"):
        wx, wy = hr + sn - 10, snr * 0.5
        head += "".join(f'<path d="M{wx:.1f} {wy + k*2:.1f} q{18:.0f} {k*5 - 2:.0f} {34:.0f} {k*9:.0f}" stroke="#F4EBDD" stroke-width="1.4" fill="none" opacity="0.8"/>' for k in (-1, 0, 1))
    if S.get("teeth") and mouth < 0.12:
        head += f'<rect x="{hr + sn*0.35:.1f}" y="{snr*0.75:.1f}" width="9" height="12" rx="2" fill="#F2B15A"/>'
    head += _eye(hr * 0.42, -hr * 0.18, S["eye"], blink, look, "#1A0F0A", S["iris"])
    head += (f'<path d="M{-hr*0.8:.1f} {-hr*0.55:.1f} Q{0} {-hr*1.02:.1f} {hr*0.7:.1f} {-hr*0.58:.1f}" stroke="{LIGHT}" stroke-width="2.6" fill="none" opacity="0.45" stroke-linecap="round"/>')
    if cap:
        head += (f'<g transform="rotate(-8 0 {-hr*0.8:.1f})"><path d="M{-hr*0.78:.1f} {-hr*0.55:.1f} Q{-hr*0.1:.1f} {-hr*1.75:.1f} {hr*0.7:.1f} {-hr*0.6:.1f} Q{-hr*0.05:.1f} {-hr*0.88:.1f} {-hr*0.78:.1f} {-hr*0.55:.1f}Z" fill="{cap}"/>'
                 f'<path d="M{-hr*0.7:.1f} {-hr*0.62:.1f} Q{-hr*0.05:.1f} {-hr*0.95:.1f} {hr*0.62:.1f} {-hr*0.64:.1f}" stroke="#FFFFFF" stroke-width="3" fill="none" opacity="0.55"/>'
                 f'<circle cx="{-hr*0.15:.1f}" cy="{-hr*1.62:.1f}" r="{hr*0.2:.1f}" fill="#FFF4C9"/></g>')
    head += "</g>"
    return defs + body + head + "</g>"


def mimo(mouth=0.0, blink=False, walk=0.0, wave=0.0, look=0.0, t=0.0, pose=None):
    return animal("bear", mouth, blink, walk, wave, look, t, cap="#8FB8E8", pose=pose)


def _std(name):
    def f(mouth=0.0, blink=False, walk=0.0, wave=0.0, look=0.0, t=0.0, pose=None):
        return animal(name, mouth, blink, walk, wave, look, t, pose=pose)
    return f


# ------------------------------------------------------------------ animaux qui ne sont pas des quadrupèdes de profil
def _feathers(seed, cx, cy, rx, ry, n, col, op=0.35):
    r = random.Random(seed); d = []
    for _ in range(n):
        a = r.uniform(0, 6.283); k = math.sqrt(r.uniform(0.1, 1))
        x, y = cx + rx * k * math.cos(a), cy + ry * k * math.sin(a)
        d.append(f"M{x-6:.1f} {y:.1f} q6 8 12 0")
    return f'<path d="{"".join(d)}" stroke="{col}" stroke-width="1.7" fill="none" opacity="{op}" stroke-linecap="round"/>'


def owl(mouth=0.0, blink=False, walk=0.0, wave=0.0, look=0.0, t=0.0, pose=None):
    """Luna, la chouette effraie : de face, pattes sur le sol, disque facial clair, grands yeux sombres."""
    asleep = pose == "sleep"
    if asleep:
        blink, mouth = True, 0.0
    br = 1 + 0.02 * math.sin(2 * math.pi * 0.45 * t)
    dy = 14 if asleep else 0
    bob = -abs(math.sin(2 * math.pi * walk)) * 4
    wing = -34 * wave
    beak_open = 9 * mouth
    return f'''<g transform="translate(0 {bob + dy:.1f})"><defs>
<radialGradient id="g_owl_b" cx="0.35" cy="0.2" r="1"><stop offset="0" stop-color="#C9A06C"/><stop offset="0.55" stop-color="#8E6A44"/><stop offset="1" stop-color="#4A3220"/></radialGradient>
<radialGradient id="g_owl_f" cx="0.5" cy="0.45" r="0.6"><stop offset="0" stop-color="#FFF4DE"/><stop offset="1" stop-color="#E5CFA6"/></radialGradient>
<linearGradient id="g_owl_w" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#7A5636"/><stop offset="1" stop-color="#3C281A"/></linearGradient></defs>
<path d="M-26 128 l-8 10 m8 -10 l0 12 m0 -12 l10 10 M26 128 l-10 10 m10 -10 l0 12 m0 -12 l8 10" stroke="#D9A24A" stroke-width="5" stroke-linecap="round" fill="none"/>
<g transform="translate(0 {(1 - br) * 80:.1f}) scale(1 {br:.3f})">
<path d="M-58 20 Q-72 100 -36 126 Q0 140 36 126 Q72 100 58 20 Q40 -16 0 -18 Q-40 -16 -58 20Z" fill="url(#g_owl_b)"/>
<path d="M-34 38 Q-40 104 -18 124 Q0 130 18 124 Q40 104 34 38 Q0 18 -34 38Z" fill="#F0DDB8"/>
{_feathers(5, 0, 84, 28, 38, 26, "#8E6A44", 0.55)}{_feathers(9, 0, 60, 54, 40, 30, "#3C281A", 0.35)}
<g transform="rotate({-wing:.1f} -56 40)"><path d="M-56 30 Q-80 80 -56 124 Q-40 90 -44 36Z" fill="url(#g_owl_w)"/></g>
<g transform="rotate({wing:.1f} 56 40)"><path d="M56 30 Q80 80 56 124 Q40 90 44 36Z" fill="url(#g_owl_w)"/></g>
</g>
<path d="M-52 -40 L-60 -88 L-22 -62Z" fill="#7A5636"/><path d="M52 -40 L60 -88 L22 -62Z" fill="#7A5636"/>
<ellipse cx="0" cy="-34" rx="58" ry="52" fill="url(#g_owl_b)"/>
<path d="M0 -70 Q-56 -64 -50 -26 Q-40 14 0 8 Q40 14 50 -26 Q56 -64 0 -70Z" fill="url(#g_owl_f)"/>
<path d="M0 -62 Q-30 -66 -42 -40 M0 -62 Q30 -66 42 -40" stroke="#B88F5E" stroke-width="2.5" fill="none" opacity="0.7"/>
{"".join(_owl_eye(x, blink, look) for x in (-24, 24))}
<path d="M-7 -20 Q0 -34 7 -20 Q0 -4 -7 -20Z" fill="#E0A04A"/><path d="M-5 -18 Q0 -28 5 -18Z" fill="#F7C877" opacity="0.8"/>
{f'<path d="M-6 -12 Q0 {-10 + beak_open:.1f} 6 -12 Q0 {-4 + beak_open:.1f} -6 -12Z" fill="#B8742E"/>' if mouth > 0.12 else ""}
<path d="M-58 -52 Q0 -96 58 -52" stroke="{LIGHT}" stroke-width="2.6" fill="none" opacity="0.4" stroke-linecap="round"/>
</g>'''


def _owl_eye(x, blink, look):
    if blink:
        return f'<path d="M{x-14} -38 Q{x} -28 {x+14} -38" stroke="#2A1A10" stroke-width="3.4" fill="none" stroke-linecap="round"/>'
    px = x + look * 3
    return (f'<circle cx="{x}" cy="-38" r="17" fill="#2A1A10"/><circle cx="{x}" cy="-38" r="14" fill="#E9A92A"/>'
            f'<circle cx="{px:.1f}" cy="-38" r="9" fill="#0B0705"/><circle cx="{px + 4:.1f}" cy="-43" r="3.6" fill="#FFFFFF"/>'
            f'<circle cx="{px - 3:.1f}" cy="-33" r="1.6" fill="#FFFFFF" opacity="0.7"/>'
            f'<path d="M{x-17} -44 Q{x} -58 {x+17} -44" stroke="#7A5636" stroke-width="4" fill="none" stroke-linecap="round"/>')


def bat(mouth=0.0, blink=False, walk=0.0, wave=0.0, look=0.0, t=0.0, pose=None):
    """Echo, la petite chauve-souris : ailes en membrane qui battent, grandes oreilles."""
    f = math.sin(2 * math.pi * 1.1 * t)
    lift = 38 * f
    mo = 5 + 7 * mouth
    return f'''<g transform="translate(0 20)"><defs><radialGradient id="g_bat_b" cx="0.4" cy="0.25" r="1"><stop offset="0" stop-color="#6E5A74"/><stop offset="1" stop-color="#241A2B"/></radialGradient>
<linearGradient id="g_bat_w" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4B3A55"/><stop offset="1" stop-color="#1D1424"/></linearGradient></defs>
<path d="M-14 -4 Q-60 {-60 - lift:.0f} -120 {-30 - lift:.0f} Q-100 {-10 - lift*0.5:.0f} -92 {10 - lift*0.4:.0f} Q-70 {0 - lift*0.2:.0f} -58 {18:.0f} Q-40 8 -14 22Z" fill="url(#g_bat_w)"/>
<path d="M14 -4 Q60 {-60 - lift:.0f} 120 {-30 - lift:.0f} Q100 {-10 - lift*0.5:.0f} 92 {10 - lift*0.4:.0f} Q70 {0 - lift*0.2:.0f} 58 18 Q40 8 14 22Z" fill="url(#g_bat_w)"/>
<path d="M-14 -2 L-112 {-26 - lift:.0f} M14 -2 L112 {-26 - lift:.0f}" stroke="#14101A" stroke-width="2" opacity="0.7"/>
<ellipse cx="0" cy="14" rx="22" ry="30" fill="url(#g_bat_b)"/>
{_fur(31, 0, 14, 18, 24, 18, "#9C86A6", "#150E1A", 1.4)}
<path d="M-16 -26 L-22 -60 L-4 -38Z" fill="#3A2B42"/><path d="M16 -26 L22 -60 L4 -38Z" fill="#3A2B42"/>
<path d="M-12 -34 L-18 -54 L-6 -40Z" fill="#D8A0B0" opacity="0.8"/><path d="M12 -34 L18 -54 L6 -40Z" fill="#D8A0B0" opacity="0.8"/>
<ellipse cx="0" cy="-20" rx="20" ry="19" fill="url(#g_bat_b)"/><ellipse cx="0" cy="-12" rx="11" ry="8" fill="#7F6A86"/>
<ellipse cx="0" cy="-15" rx="4" ry="3" fill="#1A1020"/>
{"".join(f'<circle cx="{x}" cy="-24" r="4.2" fill="#0B0710"/><circle cx="{x + 1.3}" cy="-25.4" r="1.4" fill="#FFFFFF"/>' if not blink else f'<path d="M{x-4} -24 q4 3 8 0" stroke="#0B0710" stroke-width="1.8" fill="none"/>' for x in (-8, 8))}
<path d="M-5 -7 Q0 {-7 + mo*0.5:.1f} 5 -7" stroke="#2A1020" stroke-width="{1.6 + mouth*2:.1f}" fill="none"/>
</g>'''


def turtle(mouth=0.0, blink=False, walk=0.0, wave=0.0, look=0.0, t=0.0, pose=None):
    """Shelly la tortue : grosse carapace à écailles, tête qui sort, pattes courtes."""
    asleep = pose == "sleep"
    sw = math.sin(2 * math.pi * walk)
    head_x = 66 if not asleep else 36
    hy_ = 56 if not asleep else 78
    shell = "".join(f'<path d="M{x} {y} l16 -9 l16 9 l0 18 l-16 9 l-16 -9Z" fill="#2F5B3A" stroke="#173222" stroke-width="2" opacity="0.55"/>' for x, y in ((-26, 22), (6, 22), (-42, 52), (-10, 52), (22, 52), (-26, 80), (6, 80)))
    return f'''<g><defs><radialGradient id="g_tur_s" cx="0.35" cy="0.2" r="1"><stop offset="0" stop-color="#7FB06C"/><stop offset="0.5" stop-color="#4C8450"/><stop offset="1" stop-color="#1F3F2A"/></radialGradient>
<radialGradient id="g_tur_b" cx="0.4" cy="0.3" r="1"><stop offset="0" stop-color="#C2B37A"/><stop offset="1" stop-color="#6E6238"/></radialGradient></defs>
<ellipse cx="-44" cy="{120 + 4*sw:.1f}" rx="18" ry="11" fill="#7C7A44"/><ellipse cx="34" cy="{120 - 4*sw:.1f}" rx="18" ry="11" fill="#7C7A44"/>
<path d="M-82 96 Q-86 4 0 0 Q86 4 82 96Z" fill="url(#g_tur_s)"/>{shell}
<path d="M-70 24 Q0 -10 70 24" stroke="{LIGHT}" stroke-width="3" fill="none" opacity="0.45" stroke-linecap="round"/>
<path d="M-84 96 H84 Q84 110 60 112 H-60 Q-84 110 -84 96Z" fill="url(#g_tur_b)"/>
<ellipse cx="-62" cy="{116 - 4*sw:.1f}" rx="18" ry="12" fill="#8C8A52"/><ellipse cx="52" cy="{116 + 4*sw:.1f}" rx="18" ry="12" fill="#8C8A52"/>
<g transform="translate({head_x} {hy_})"><path d="M-30 30 Q-20 -12 4 -20 Q34 -22 40 4 Q44 26 12 34Z" fill="#8C8A52"/>
<ellipse cx="10" cy="2" rx="26" ry="22" fill="#9C9A5C"/>
{_eye(14, -6, 5.2, blink or asleep, look, "#2A2410", "#3A2A10")}
{'<path d="M16 14 Q30 22 38 12" stroke="#4A2A1A" stroke-width="2.6" fill="none"/>' if mouth < 0.12 else f'<path d="M16 12 Q30 {18 + 10*mouth:.0f} 40 8" stroke="#6A2A2A" stroke-width="5" fill="none"/>'}
</g></g>'''


DRAW2 = {"mimo": mimo, "fox": _std("fox"), "hedgehog": _std("hedgehog"), "bunny": _std("bunny"), "otter": _std("otter"), "fawn": _std("fawn"), "beaver": _std("beaver"), "owl": owl, "bat": bat, "turtle": turtle}
FIT = {"owl": 0.95, "bat": 0.9, "turtle": 0.8}          # échelle de chaque animal dans le repère des personnages (0.8 par défaut)
