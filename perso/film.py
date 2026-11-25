"""Montage d'un épisode de « رايان و يقين » : minutage, caméra, jeu des acteurs, son, sous-titres arabes, encodage Full HD."""
import math, os, random, subprocess
import numpy as np, soundfile as sf
from multiprocessing import Pool
from . import humains as H, decors_tn as D, musique_tn as M

W, HH, FPS, SR = 1920, 1080, 30, 44100
TARGET = 605.0
G = {}  # plans partagés avec les processus de rendu


# ------------------------------------------------------------------ minutage
def _mood(sh):
    emos = [ln[1] for ln in sh.get("lines", [])]
    if emos and sum(e in ("sad", "worried") for e in emos) / len(emos) >= 0.45:
        return "sad"
    return "light"


def plan(ep, voices):
    """voices[(i_plan, i_réplique)] = (signal 44.1k, enveloppe bouche 100 Hz)."""
    shots, t = [], 0.0
    for si, sh in enumerate(ep["shots"]):
        sh = dict(sh)
        if sh.get("title"):
            sh.update(kind="title", decor="sidibou_soir", cast=[("rayen", 700, 700, 1), ("yakin", 1220, 1220, -1)], dur=7.0, lines_t=[])
        elif sh.get("montage"):
            sh.update(kind="montage", dur=float(sh.get("min", 15)), lines_t=[])
        else:
            sh["kind"] = "teaser" if sh.get("teaser") else "dialogue"
            moves = [abs(c[2] - c[1]) for c in sh["cast"]]
            move_t = min(3.2, max(moves) / 520.0) if max(moves) > 0 else 0.0
            sh["move_t"] = move_t
            lt = max(0.9, move_t * 0.8) + (2.4 if sh["kind"] == "teaser" else 0)
            lines = []
            for li, ln in enumerate(sh["lines"]):
                who, emo, gest, text = ln[:4]
                act = ln[4] if len(ln) > 4 else ""
                y, mouth = voices[(si, li)]
                d = len(y) / SR
                lines.append(dict(who=who, emo=emo, gest=gest, text=text, act=act, start=lt, dur=d, mouth=mouth, key=(si, li)))
                lt += d + 0.42 + (0.9 if act in ("slip", "jump") else 0) + (0.25 if text.endswith(("؟", "!", "?")) else 0)
            sh["lines_t"] = lines
            sh["dur"] = lt + (1.0 if sh["kind"] == "dialogue" else 2.6)
        sh["mood"] = _mood(sh)
        shots.append(sh)
    # allonger les montages musicaux pour atteindre ~10 min
    total = sum(s["dur"] for s in shots)
    mont = [s for s in shots if s["kind"] == "montage"]
    if total < TARGET and mont:
        extra = TARGET - total
        for s in mont:
            s["dur"] += min(extra / len(mont), 30.0)
    t = 0.0
    for s in shots:
        s["start"] = t; t += s["dur"]
    if t < TARGET:  # générique de fin si encore trop court
        shots.append(dict(kind="credits", decor="toit_nuit", cast=[("rayen", 700, 700, 1), ("yakin", 1000, 1000, -1),
                                                                  ("hamma", 1320, 1320, -1), ("sarra", 1580, 1580, -1)],
                          dur=max(12.0, TARGET - t), lines_t=[], start=t, mood="theme"))
        t += shots[-1]["dur"]
    return shots, math.ceil(t * FPS) / FPS


# ------------------------------------------------------------------ jeu des acteurs
def _speaking(sh, ts):
    for ln in sh["lines_t"]:
        if ln["start"] <= ts < ln["start"] + ln["dur"]:
            return ln
    return None


def actors(sh, ts):
    sp = _speaking(sh, ts)
    kind = sh["kind"]
    out = []
    xs = {}
    for c in sh["cast"]:
        who, x0, x1, facing = c[:4]
        if kind == "montage":
            u = min(1.0, ts / 6.0)
            u = u * u * (3 - 2 * u)
            mv = x0 != x1 and u < 1.0
        else:
            mt = sh.get("move_t", 0.0)
            u = min(1.0, ts / mt) if mt > 0 and x0 != x1 else 1.0
            mv = x0 != x1 and u < 1.0
            u = u * u * (3 - 2 * u)
        xs[who] = x0 + (x1 - x0) * u
    for c in sh["cast"]:
        who, x0, x1, facing = c[:4]
        prop = c[4] if len(c) > 4 else None
        x = xs[who]
        moving = (x0 != x1) and ((kind == "montage" and ts < 6.0) or (kind != "montage" and ts < sh.get("move_t", 0)))
        f = facing
        if moving:
            f = 1 if x1 > x0 else -1
        elif sp and sp["who"] != who and sp["who"] in xs:
            f = 1 if xs[sp["who"]] > x else -1
        st = dict(who=who, x=x, facing=f, walk=(ts * 1.7 if moving else 0.0), prop=prop, emo="neutral",
                  gesture="idle", mouth=0.0, talk=False, jump=0.0, fall=0.0, fx=None, look=0.0)
        # dernière émotion du personnage
        last = [ln for ln in sh["lines_t"] if ln["who"] == who and ln["start"] <= ts]
        if last:
            st["emo"] = last[-1]["emo"] if ts < last[-1]["start"] + last[-1]["dur"] + 2.5 else ("happy" if last[-1]["emo"] in ("happy", "laugh", "love") else "neutral")
        if kind in ("montage", "title", "credits"):
            st["emo"] = ["happy", "laugh", "love", "happy"][int(ts / 3 + len(who)) % 4]
            if who in ("rayen", "yakin") and kind != "montage":
                st["emo"] = "love"
        if sp and sp["who"] == who:
            k = int((ts - sp["start"]) * 100)
            m = sp["mouth"]
            st["mouth"] = float(m[min(k, len(m) - 1)]) if len(m) else 0.0
            st["gesture"], st["emo"], st["talk"] = sp["gest"], sp["emo"], True
            u = ts - sp["start"]
            if sp["act"] == "jump" and u < 0.55:
                st["jump"] = math.sin(math.pi * u / 0.55)
            if sp["act"] in ("hearts", "sweat", "anger"):
                st["fx"] = (sp["act"], u)
        elif sp and sp["who"] in xs:
            st["look"] = 1.0 if xs[sp["who"]] > x else -1.0
        # chute (glissade) : pendant la réplique et un peu après
        for ln in sh["lines_t"]:
            if ln["who"] == who and ln["act"] == "slip":
                u = ts - (ln["start"] + 0.25)
                end = ln["dur"] + 0.6
                if 0 <= u < end + 0.4:
                    st["fall"] = min(1.0, u / 0.25) if u < end else max(0.0, 1 - (u - end) / 0.4)
                    if u < end:
                        st["fx"] = ("stars", u)
        if kind == "montage" and who in ("rayen", "yakin") and int(ts / 4) % 3 == 1:
            st["fx"] = ("hearts", ts % 4)
        st["blink"] = ((ts + len(who) * 0.37) % 3.9) < 0.12
        out.append(st)
    return out, sp


def _fx(kind, x, y, u, s):
    if kind == "hearts":
        g = ""
        for i in range(4):
            v = (u * 0.6 + i * 0.25) % 1.0
            hx, hy = x + (i - 1.5) * 50 * s + 14 * math.sin(6 * v + i), y - 80 * s - v * 220 * s
            a = 1 - v
            g += (f'<path transform="translate({hx:.0f} {hy:.0f}) scale({s*1.4:.2f})" d="M0 10 C-22 -4 -10 -22 0 -8 C10 -22 22 -4 0 10Z" '
                  f'fill="#FF4D7A" opacity="{a:.2f}"/>')
        return g
    if kind == "sweat":
        dy = (u * 40) % 50
        return f'<path transform="translate({x + 95*s:.0f} {y - 520*s + dy:.0f}) scale({s:.2f})" d="M0 -22 Q16 4 0 14 Q-16 4 0 -22Z" fill="#9ED8FF" stroke="#3A8ACF" stroke-width="3"/>'
    if kind == "anger":
        p = 1 + 0.15 * math.sin(u * 20)
        return (f'<g transform="translate({x + 90*s:.0f} {y - 600*s:.0f}) scale({s*p:.2f})" stroke="#E8243C" stroke-width="7" fill="none" stroke-linecap="round">'
                '<path d="M-20 -6 Q-8 -8 -6 -20 M6 -20 Q8 -8 20 -6 M20 6 Q8 8 6 20 M-6 20 Q-8 8 -20 6"/></g>')
    if kind == "stars":
        g = ""
        for i in range(4):
            a = u * 4 + i * math.pi / 2
            g += f'<path transform="translate({x + math.cos(a)*70*s:.0f} {y - 120*s + math.sin(a)*22*s:.0f}) scale({s:.2f})" d="M0 -14 L4 -4 L14 -4 L6 3 L9 13 L0 7 L-9 13 L-6 3 L-14 -4 L-4 -4Z" fill="#FFE066"/>'
        return g
    return ""


def _draw_actor(st, t, s=1.0):
    x, y = st["x"], D.GROUND
    body = H.draw(st["who"], 0, 0, s, mouth=st["mouth"], blink=st["blink"], walk=st["walk"], facing=st["facing"],
                  look=st["look"], emo=st["emo"], gesture=st["gesture"], t=t, talk=st["talk"], jump=st["jump"], prop=st["prop"])
    fall = st["fall"]
    if fall > 0:
        ang = -82 * fall * st["facing"]
        g = f'<g transform="translate({x:.1f} {y:.1f}) rotate({ang:.1f})">{body}</g>'
        hx, hy = x - 380 * s * fall * st["facing"] * 0.9, y - 60 * s
    else:
        g = f'<g transform="translate({x:.1f} {y:.1f})">{body}</g>'
        hx, hy = x, y - st["jump"] * 60 * s
    if st["fx"]:
        k, u = st["fx"]
        if k == "stars":
            g += _fx(k, hx, hy + 40 * s, u, s)
        else:
            g += _fx(k, x, hy, u, s)
    return g


# ------------------------------------------------------------------ caméra
def _clamp(cx, cy, z):
    hw, hh = W / 2 / z, HH / 2 / z
    return min(max(cx, hw), W - hw), min(max(cy, hh), HH - hh), z


def _cam_target(sh, li, acts):
    if sh["kind"] != "dialogue" or li is None or li < 0:
        return (W / 2, HH / 2, 1.0)
    ln = sh["lines_t"][li]
    xs = {a["who"]: a["x"] for a in acts}
    if ln["act"] in ("slip", "jump") or len(xs) == 1 and li % 3 == 0:
        return _clamp(sum(xs.values()) / len(xs), 600, 1.1)
    x = xs.get(ln["who"], W / 2)
    mode = li % 4
    if li == 0:
        return (W / 2, HH / 2, 1.0)
    if mode in (1, 3):
        return _clamp(x, 470, 1.65)
    others = [v for k, v in xs.items() if k != ln["who"]]
    if others:
        o = min(others, key=lambda v: abs(v - x))
        return _clamp((x + o) / 2, 560, 1.3)
    return _clamp(x, 520, 1.4)


def camera(sh, ts, acts):
    if sh["kind"] == "montage":
        xs = [a["x"] for a in acts]
        return _clamp(sum(xs) / len(xs), 560, 1.25)
    if sh["kind"] in ("title", "credits"):
        return (W / 2, HH / 2, 1.0 + 0.05 * ts / sh["dur"])
    lis = [i for i, ln in enumerate(sh["lines_t"]) if ln["start"] - 0.15 <= ts]
    li = lis[-1] if lis else None
    cur = _cam_target(sh, li, acts)
    if li is None:
        return cur
    prev = _cam_target(sh, li - 1, acts)
    u = min(1.0, (ts - sh["lines_t"][li]["start"] + 0.15) / 0.55)
    u = u * u * (3 - 2 * u)
    return tuple(p + (c - p) * u for p, c in zip(prev, cur))


VIG = ('<defs><radialGradient id="vig" cx="0.5" cy="0.5" r="0.75"><stop offset="0.6" stop-color="#000" stop-opacity="0"/>'
       '<stop offset="1" stop-color="#000" stop-opacity="0.38"/></radialGradient></defs>')


def shot_svg(sh, ts):
    acts, sp = actors(sh, ts)
    cx, cy, z = camera(sh, ts, acts)
    z *= 1.0 + 0.015 * ts / max(sh["dur"], 1)
    cx, cy, z = _clamp(cx, cy, z)
    deco = D.DECORS[sh["decor"]](ts + sh["start"] * 0.0)
    people = "".join(_draw_actor(a, ts) for a in sorted(acts, key=lambda a: a["who"] in ("rayen", "yakin")))
    tint = '<rect width="1920" height="1080" fill="#14104A" opacity="0.22"/>' if sh["decor"] in D.NIGHT else ""
    extra = ""
    if sh["kind"] in ("title", "credits"):
        extra = '<rect width="1920" height="1080" fill="#1A0A2A" opacity="0.45"/>' + "".join(
            _fx("hearts", 200 + i * 380, 1100, ts * 0.5 + i * 0.3, 1.6) for i in range(5))
    return (VIG + f'<g transform="translate({W/2} {HH/2}) scale({z:.4f}) translate({-cx:.1f} {-cy:.1f})">{deco}{people}{tint}</g>'
            + extra + f'<rect width="{W}" height="{HH}" fill="url(#vig)"/>')


def _svg(body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{HH}" viewBox="0 0 {W} {HH}">{body}</svg>'


def _frame(k):
    import cairosvg
    shots, total = G["shots"], G["total"]
    t = k / FPS
    si = max(i for i, s in enumerate(shots) if s["start"] <= t + 1e-6)
    sh = shots[si]
    ts = t - sh["start"]
    body = shot_svg(sh, ts)
    fade = 0.45
    if si > 0 and ts < fade:
        pv = shots[si - 1]
        body = f'<g>{shot_svg(pv, pv["dur"] - 1 / FPS)}</g><g opacity="{ts / fade:.3f}">{body}</g>'
    if t < 0.6:
        body += f'<rect width="{W}" height="{HH}" fill="#000" opacity="{1 - t / 0.6:.3f}"/>'
    if t > total - 1.2:
        body += f'<rect width="{W}" height="{HH}" fill="#000" opacity="{min(1, (t - total + 1.2) / 1.2):.3f}"/>'
    return cairosvg.svg2png(bytestring=_svg(body).encode())


# ------------------------------------------------------------------ son
def _noise(n, seed):
    return np.random.default_rng(seed).standard_normal(n)


def _lowpass(x, a):
    from scipy.signal import lfilter
    return lfilter([1 - a], [1, -a], x)


def ambience(decor, n, seed=1):
    t = np.arange(n) / SR
    if decor in ("plage", "cafe", "sidibou", "sidibou_soir"):
        w = _lowpass(_noise(n, seed), 0.985) * 6
        lvl = (0.5 + 0.5 * np.sin(2 * np.pi * t / 7.5)) ** 2 * (0.04 if decor == "plage" else 0.02)
        return w * lvl
    if decor == "medina":
        x = _lowpass(_noise(n, seed), 0.94) * 2
        return x * 0.012 * (0.7 + 0.3 * np.sin(2 * np.pi * t / 3.1))
    if decor == "toit_nuit":
        chirp = np.sin(2 * np.pi * 4300 * t) * (np.sin(2 * np.pi * 28 * t) > 0.6) * ((t % 1.7) < 0.35)
        return chirp * 0.006
    if decor == "fac":
        return _lowpass(_noise(n, seed), 0.95) * 0.01
    return np.zeros(n)


def sfx(kind):
    if kind == "jump":
        d = 0.35; t = np.arange(int(d * SR)) / SR
        f = 300 + 900 * t / d
        return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 6) * 0.25
    if kind == "slip":
        d = 0.7; t = np.arange(int(d * SR)) / SR
        f = 900 - 800 * t / d
        y = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.18 * (t < 0.45)
        th = np.zeros_like(t); i = int(0.45 * SR)
        th[i:] = _lowpass(_noise(len(t) - i, 3), 0.9)[: len(t) - i] * np.exp(-(t[i:] - 0.45) * 18) * 0.9
        return y + th
    if kind == "hearts":
        out = []
        for f in (1318, 1568, 2093):
            t = np.arange(int(0.18 * SR)) / SR
            out.append(np.sin(2 * np.pi * f * t) * np.exp(-t * 14) * 0.12)
        return np.concatenate(out)
    return np.zeros(1)


def build_audio(shots, total, voices):
    n = int(total * SR) + SR
    voice = np.zeros(n)
    fx = np.zeros(n)
    music = np.zeros((n, 2))
    amb = np.zeros(n)
    for s in shots:
        a = int(s["start"] * SR)
        for ln in s["lines_t"]:
            y = voices[ln["key"]][0]
            i = int((s["start"] + ln["start"]) * SR)
            voice[i:i + len(y)] += y[: n - i]
            if ln["act"] in ("jump", "slip", "hearts"):
                e = sfx(ln["act"]); j = i + int(0.2 * SR)
                fx[j:j + len(e)] += e[: n - j]
        mood = {"title": "theme", "montage": "theme", "credits": "theme"}.get(s["kind"], s.get("mood", "light"))
        vol = {"title": 1.0, "montage": 0.95, "credits": 0.9, "teaser": 0.55}.get(s["kind"], 0.32 if mood == "light" else 0.42)
        L = s["dur"] + 1.2
        b = M.bed(mood, L, fade=0.9) * vol
        music[a:a + len(b)] += b[: n - a]
        am = ambience(s["decor"], int(s["dur"] * SR), seed=hash(s["decor"]) % 1000)
        amb[a:a + len(am)] += am[: n - a]
    env = np.convolve(np.abs(voice), np.ones(4410) / 4410, mode="same")
    duck = 1 - 0.45 * np.clip(env / 0.02, 0, 1)
    duck = np.convolve(duck, np.ones(2205) / 2205, mode="same")
    mix = music * duck[:, None] + (voice + fx + amb)[:, None] * np.array([1.0, 1.0])
    mix = np.tanh(mix * 1.4) / 1.4
    peak = np.abs(mix).max()
    mix *= 0.89 / max(peak, 1e-6)
    return mix[: int(total * SR)]


# ------------------------------------------------------------------ sous-titres (ASS, arabe)
def _ts(t):
    t = max(0.0, t)
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def _col(hexrgb):
    r, g, b = hexrgb[1:3], hexrgb[3:5], hexrgb[5:7]
    return f"&H00{b}{g}{r}&".upper()


ASS_HEAD = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Dial,Tajawal ExtraBold,62,&H00FFFFFF,&H00FFFFFF,&H00201020,&H90000000,-1,0,0,0,100,100,0,0,1,5,2,2,140,140,48,1
Style: Big,Lalezar,190,&H007AC8FF,&H00FFFFFF,&H00401040,&H90000000,0,0,0,0,100,100,0,0,1,8,4,5,80,80,0,1
Style: Sub,Tajawal ExtraBold,76,&H00FFFFFF,&H00FFFFFF,&H00401040,&H90000000,-1,0,0,0,100,100,0,0,1,6,3,5,80,80,0,1
Style: Cap,Lalezar,92,&H0066E0FF,&H00FFFFFF,&H00301030,&H90000000,0,0,0,0,100,100,0,0,1,7,3,8,80,80,70,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def build_ass(ep, shots, path):
    ev = []
    for s in shots:
        a = s["start"]
        if s["kind"] == "title":
            ev.append(f"Dialogue: 1,{_ts(a+0.4)},{_ts(a+s['dur']-0.2)},Big,,0,0,0,,{{\\fad(500,400)\\pos(960,210)}}رايان و يقين")
            ev.append(f"Dialogue: 1,{_ts(a+1.0)},{_ts(a+s['dur']-0.2)},Sub,,0,0,0,,{{\\fad(500,400)\\pos(960,980)}}الحلقة {ep['num']}: {ep['title']}")
        if s.get("caption"):
            d = 5.0 if s["kind"] == "montage" and not s.get("end") else s["dur"] - 0.5
            ev.append(f"Dialogue: 1,{_ts(a+0.6)},{_ts(a+0.6+d)},Cap,,0,0,0,,{{\\fad(400,400)}}{s['caption']}")
        if s["kind"] == "credits":
            ev.append(f"Dialogue: 1,{_ts(a+0.5)},{_ts(a+s['dur']-0.3)},Big,,0,0,0,,{{\\fad(600,600)\\pos(960,210)}}رايان و يقين")
            ev.append(f"Dialogue: 1,{_ts(a+1.2)},{_ts(a+s['dur']-0.3)},Sub,,0,0,0,,{{\\fad(600,600)\\pos(960,980)}}"
                      + ("تابعونا في الحلقة الجاية" if ep["num"] < 3 else "النهاية... والحكاية مازالت"))
        for ln in s["lines_t"]:
            t0, t1 = a + ln["start"] - 0.05, a + ln["start"] + ln["dur"] + 0.3
            name = H.NAMES.get(ln["who"], "")
            col = _col(H.COLORS.get(ln["who"], "#FFFFFF"))
            ev.append(f"Dialogue: 0,{_ts(t0)},{_ts(t1)},Dial,,0,0,0,,{{\\c{col}\\fs50}}{name}\\N{{\\c&H00FFFFFF&\\fs62}}{ln['text']}")
    with open(path, "w", encoding="utf-8") as f:
        f.write(ASS_HEAD + "\n".join(ev) + "\n")


# ------------------------------------------------------------------ rendu
def render(ep, voices, out, workdir, fonts="perso/fonts", preset="medium", crf=19, scale=1.0, log=print):
    shots, total = plan(ep, voices)
    log(f"Épisode {ep['num']} : {len(shots)} plans, {total/60:.1f} min")
    wav = os.path.join(workdir, f"ep{ep['num']}.wav")
    sf.write(wav, build_audio(shots, total, voices), SR, subtype="PCM_16")
    ass = os.path.join(workdir, f"ep{ep['num']}.ass")
    build_ass(ep, shots, ass)
    G["shots"], G["total"] = shots, total
    n = int(round(total * FPS))
    vf = f"ass={ass}:fontsdir={fonts}"
    if scale != 1.0:
        vf = f"scale={int(W*scale)}:{int(HH*scale)}," + vf.replace("ass=", "ass=")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "png", "-i", "-",
           "-i", wav, "-vf", vf, "-c:v", "libx264", "-preset", preset, "-tune", "animation", "-crf", str(crf),
           "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    with Pool(os.cpu_count() or 2) as pool:
        for i, png in enumerate(pool.imap(_frame, range(n), chunksize=6)):
            p.stdin.write(png)
            if i % 1800 == 0:
                log(f"  image {i}/{n}")
    p.stdin.close()
    if p.wait() != 0:
        raise RuntimeError("ffmpeg a échoué")
    return shots, total
