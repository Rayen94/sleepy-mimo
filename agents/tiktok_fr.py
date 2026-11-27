"""Série TikTok en français : des vidéos verticales de 62 à 90 s, 100 % séparées de YouTube (autres histoires, autre langue,
autre montage). Ce qui a fait ses preuves chez les petits comptes francophones (vidIQ, novembre 2026) :
  - la phrase d'accroche écrite à l'écran dès la première image, et la voix qui démarre tout de suite ;
  - des sous-titres dynamiques (le mot dit est surligné) ;
  - une histoire animée racontée en voix off, avec un suspense qui donne envie de voir la partie 2 ;
  - plus d'une minute (seuil du programme de récompenses TikTok).
Rien n'est repris d'un autre créateur : scénarios, dessins, voix et musique sont produits ici."""
import os
import io, os, math, wave, datetime
import numpy as np
from . import histoires as H, comediens as V, voixia, illustrateur as I, style, monteur, decors as D, compositeur
from .tiktok_fr_scripts import BANK

SR = V.SR
FPS = monteur.FPS
W, HT = 1080, 1920
START = datetime.date(2026, 11, 28)          # jour 0 de la série
MIN_SECONDS = 62.0                           # TikTok : au moins 1 minute pour être éligible aux récompenses

# (voix Kokoro, vitesse, décalage des formants, facteur de hauteur) — une seule voix française, déclinée en timbres différents
FR_VOICES = {
    "narrator": ("ff_siwis", 0.98, 1.00, 0.95),
    "fox":      ("ff_siwis", 1.02, 0.90, 0.78),
    "owl":      ("ff_siwis", 0.90, 0.98, 0.86),
    "hedgehog": ("ff_siwis", 1.04, 1.12, 1.22),
    "bunny":    ("ff_siwis", 1.08, 1.18, 1.55),
    "otter":    ("ff_siwis", 1.04, 0.94, 0.95),
    "fawn":     ("ff_siwis", 1.00, 1.14, 1.40),
    "beaver":   ("ff_siwis", 0.95, 0.88, 0.76),
    "turtle":   ("ff_siwis", 0.88, 0.90, 0.72),
    "mimo":     ("ff_siwis", 1.00, 1.12, 1.35),
    "bat":      ("ff_siwis", 1.10, 1.18, 1.60),
}
SPEAKER_COLOR = {"narrator": "#FFFFFF"}


def pick(date, n):
    """Les n vidéos du jour (déterministe : relancer la même journée redonne les mêmes vidéos)."""
    d = (date if isinstance(date, datetime.date) else datetime.date.fromisoformat(date)) - START
    out = []
    for i in range(n):
        k = d.days * n + i
        if 0 <= k < len(BANK):
            out.append(BANK[k])
    return out


# ------------------------------------------------------------------ voix et minutage
_CACHE = {}


def _speak(who, text, mult):
    key = (who, text, round(mult, 3))
    if key in _CACHE:
        return _CACHE[key]
    import parselmouth
    from parselmouth.praat import call
    voice, speed, formant, pf = FR_VOICES[who]
    y, sr = voixia.synth(text, voice, speed * mult, lang="fr-fr")
    snd = parselmouth.Sound(y, sampling_frequency=sr)
    if abs(pf - 1) > 0.01 or abs(formant - 1) > 0.01:
        f0 = snd.to_pitch().selected_array["frequency"]
        med = float(np.median(f0[f0 > 0])) if (f0 > 0).any() else 190.0
        snd = call(snd, "Change gender", 75, 600, formant, med * pf, 1.1, 1.0)
    y = call(snd, "Resample", SR, 50).values[0]
    _CACHE[key] = V._finish(y)
    return _CACHE[key]


def _cta(vid):
    if vid["parts"] > 1 and vid["part"] < vid["parts"]:
        return ("narrator", "La suite arrive très vite. Suis-moi pour ne pas la rater !"), ("La suite", "très vite !")
    if vid["parts"] > 1:
        return ("narrator", "Suis-moi pour une nouvelle histoire."), ("Une nouvelle", "histoire bientôt !")
    return ("narrator", "Suis-moi pour d'autres secrets d'animaux !"), ("Suis-moi pour", "d'autres secrets !")


def timeline(vid, mult, lead=0.2, gap=0.28, shot_gap=0.22):
    shots, t, clips = [], lead, []
    cta_line, _ = _cta(vid)
    n = len(vid["shots"])
    for si, sh in enumerate(vid["shots"]):
        st, lines = t, []
        raw = list(sh["lines"]) + ([cta_line] if si == n - 1 else [])
        for who, text in raw:
            y, mouth = _speak(who, text, mult)
            lines.append(dict(who=who, text=text, start=t - st, dur=len(y) / SR, mouth=mouth))
            clips.append((t, y))
            t += len(y) / SR + gap
        t += shot_gap
        shots.append(dict(sh, start=st, dur=t - st, lines_t=lines))
    total = math.ceil((t + 0.3) * FPS) / FPS
    return shots, clips, total


def build(vid, rng):
    """Calcule les plans, la voix et la musique. La vitesse de la voix est ajustée pour dépasser 62 s."""
    mult = 1.0
    shots, clips, total = timeline(vid, mult)
    if total < MIN_SECONDS + 1.0:
        talk = sum(len(y) / SR for _, y in clips)
        need = (MIN_SECONDS + 1.0) - total
        mult = max(0.80, talk / (talk + need))
        shots, clips, total = timeline(vid, mult)
    n = int(total * SR)
    voice = np.zeros(n)
    for t0, y in clips:
        i = int(t0 * SR); voice[i:i + len(y)] += y[:n - i]
    bpm, mel, ch = compositeur.track_spec(("orig", "story"), rng)
    inst = ["soft", "box", "harp"][int(rng.integers(3))]
    m = compositeur.reverb(compositeur.render(bpm * 0.95, mel, ch, inst, 12, 0, total + 1, seed=int(rng.integers(1000))))[:n]
    bg = np.zeros((n, 2)); bg[:len(m)] += m * 0.20
    voice_st = compositeur.reverb(voice) * 0.18 + np.stack([voice, voice], 1) * 0.82
    audio = voice_st + bg
    k = int(SR * 0.4); audio[:k] *= np.linspace(0, 1, k)[:, None]
    k = int(SR * 1.2); audio[-k:] *= np.linspace(1, 0, k)[:, None]
    return shots, total, audio, mult


# ------------------------------------------------------------------ sous-titres dynamiques
def _esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _chunks(words, max_chars=15, max_words=3):
    out, cur = [], []
    for w in words:
        if cur and (len(" ".join(cur + [w])) > max_chars or len(cur) >= max_words):
            out.append(cur); cur = []
        cur.append(w)
        if w[-1] in ".!?":
            out.append(cur); cur = []
    if cur:
        out.append(cur)
    return out


def caption_events(shots):
    """Une liste (début, fin, mots du groupe, mot actif) : chaque mot est surligné pendant qu'il est prononcé."""
    ev = []
    for sh in shots:
        for ln in sh["lines_t"]:
            words = ln["text"].split()
            if not words:
                continue
            weights = [len(w) + 2 + (3 if w[-1] in ".!?," else 0) for w in words]
            tot, t = sum(weights), sh["start"] + ln["start"]
            groups = _chunks(words)
            pos = 0
            for g in groups:
                for j, w in enumerate(g):
                    d = ln["dur"] * weights[pos] / tot
                    ev.append((t, t + d, g, j))
                    t += d; pos += 1
    return ev


_FONT_CACHE = {}


def _measure(text, size, weight=700):
    """Largeur du texte en pixels, mesurée avec la même police que le rendu (Fredoka variable, graisse 700)."""
    from PIL import ImageFont
    key = (size, weight)
    if key not in _FONT_CACHE:
        f = ImageFont.truetype(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "fonts", "Fredoka.ttf"), size)
        try:
            f.set_variation_by_axes([weight, 100])
        except Exception:
            pass
        _FONT_CACHE[key] = f
    return _FONT_CACHE[key].getlength(text)


def _caption_svg(group, active, y, size=88):
    """Chaque mot est posé à sa propre position : contour sombre dessous, mot clair dessus (le mot actif est jaune)."""
    space = _measure(" ", size) or size * 0.25
    widths = [_measure(w, size) for w in group]
    total = sum(widths) + space * (len(group) - 1)
    x = W / 2 - total / 2
    base = f'font-family="{I.FONT}" font-weight="700" font-size="{size}" text-anchor="start"'
    back, front = [], []
    for i, (w, wd) in enumerate(zip(group, widths)):
        back.append(f'<text x="{x:.1f}" y="{y}" {base} fill="#0B1030" stroke="#0B1030" stroke-width="16" stroke-linejoin="round">{_esc(w)}</text>')
        front.append(f'<text x="{x:.1f}" y="{y}" {base} fill="{"#FFE37A" if i == active else "#FFFFFF"}">{_esc(w)}</text>')
        x += wd + space
    return "".join(back) + "".join(front)


def _outlined(x, y, s, size, fill="#FFFFFF", weight=700):
    base = f'font-family="{I.FONT}" font-weight="{weight}" font-size="{size}" text-anchor="middle"'
    return (f'<text x="{x}" y="{y}" {base} fill="#0B1030" stroke="#0B1030" stroke-width="{size * 0.2:.0f}" stroke-linejoin="round">{_esc(s)}</text>'
            f'<text x="{x}" y="{y}" {base} fill="{fill}">{_esc(s)}</text>')


# ------------------------------------------------------------------ images
def frames(vid, shots, total, seed):
    """Génère des paires (décor, texte) : le décor passe par l'étalonnage « cinéma », le texte reste net par-dessus."""
    n = int(round(total * FPS))
    events = caption_events(shots)
    ei = 0
    s = HT / 720
    cx_s, last_si = None, -1
    series = vid["serie"]
    part_tag = f"PARTIE {vid['part']}/{vid['parts']}" if vid["parts"] > 1 else None
    hook_rows = H._wrap(vid["hook"], 17)
    _, end_pair = _cta(vid)
    for kf in range(n):
        ts = kf / FPS
        si = max((i for i, sh in enumerate(shots) if sh["start"] <= ts + 1e-6), default=0)
        sh = shots[si]
        local = max(0.0, ts - sh["start"])
        acts, speaking = H.actors(sh, local)
        xs = [a["x"] for a in acts]
        mid = sum(xs) / len(xs)
        spk = next((a["x"] for a in acts if speaking and a["who"] == speaking["who"]), mid)
        target = mid + 0.55 * (spk - mid)
        if si != last_si or cx_s is None:
            cx_s, last_si = target, si
        else:
            cx_s += (target - cx_s) * 0.10
        zoom = 1.12 + 0.06 * min(1.0, local / max(2.0, sh["dur"])) + 0.05 * (1 - I.smooth(min(1.0, local / 0.5)))
        gy = D.ground(sh["decor"])
        world = (f'<g transform="translate({W/2} 1080) scale({s * zoom:.4f}) translate({-cx_s:.1f} {-(gy - 70):.1f})">'
                 f'{H.shot_inner(sh, local, seed + si)}'
                 f'<defs><linearGradient id="bt" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#060B1C" stop-opacity="0"/>'
                 f'<stop offset="0.045" stop-color="#060B1C" stop-opacity="1"/><stop offset="1" stop-color="#060B1C"/></linearGradient></defs>'
                 f'<rect x="-3000" y="640" width="7000" height="1800" fill="url(#bt)"/></g>')
        over = []
        # série et numéro de partie, en haut (sous la barre de TikTok)
        over.append(_outlined(W / 2, 255, series, 40, "#E8EEFF", 600))
        if part_tag:
            over.append(_outlined(W / 2, 305, part_tag, 46, "#FFE37A"))
        # accroche : écrite dès la première image
        if ts < 3.6:
            op = 1.0 if ts < 3.1 else 1 - I.smooth((ts - 3.1) / 0.5)
            h = len(hook_rows) * 100 + 60
            y0 = 440
            block = [f'<rect x="50" y="{y0 - 95}" width="980" height="{h}" rx="34" fill="#0B1030" opacity="0.58"/>']
            block += [_outlined(W / 2, y0 + i * 100, r_, 76) for i, r_ in enumerate(hook_rows)]
            over.append(f'<g opacity="{op:.3f}">{"".join(block)}</g>')
        # sous-titres dynamiques
        while ei < len(events) - 1 and events[ei][1] <= ts:
            ei += 1
        t0, t1, grp, act = events[ei]
        if t0 - 0.05 <= ts < t1 + 0.35:
            over.append(_caption_svg(grp, act, 1350))
        # carte de fin
        if ts > total - 3.0:
            op = I.smooth((ts - (total - 3.0)) / 0.5)
            pulse = 1 + 0.04 * math.sin(2 * math.pi * 1.2 * ts)
            over.append(f'<g opacity="{op:.3f}" transform="translate({W/2} 600) scale({pulse:.3f}) translate({-W/2} -600)">'
                        + _outlined(W / 2, 560, end_pair[0], 96) + _outlined(W / 2, 670, end_pair[1], 96, "#FFE37A") + "</g>")
        yield (I.svg(W, HT, world), I.svg(W, HT, "".join(over)))


def raster_pair(pair):
    import cairosvg
    from PIL import Image
    from . import cinema
    world, over = pair
    base = Image.open(io.BytesIO(cinema.look(cairosvg.svg2png(bytestring=world.encode())))).convert("RGBA")
    top = Image.open(io.BytesIO(cairosvg.svg2png(bytestring=over.encode()))).convert("RGBA")
    base.alpha_composite(top)
    buf = io.BytesIO()
    base.convert("RGB").save(buf, "PNG", compress_level=1)
    return buf.getvalue()


# ------------------------------------------------------------------ production
def legende(vid):
    """Description TikTok en français, prête à copier-coller."""
    if vid["parts"] > 1:
        suite = "Partie 2 très vite, suis-moi pour ne pas la rater !" if vid["part"] < vid["parts"] else "Suis-moi pour la prochaine histoire !"
        return f"{vid['hook']} ({vid['serie']} - {vid['title']}, partie {vid['part']}/{vid['parts']}) {suite} {vid['tags']}"
    return f"{vid['hook']} ({vid['serie']}) Suis-moi pour d'autres secrets d'animaux ! {vid['tags']}"


def make(vid, out_mp4, rng, log=print):
    """Produit une vidéo TikTok (mp4 vertical + son). Renvoie la durée en secondes."""
    wav_path = out_mp4.replace(".mp4", ".wav")
    prev = style.s2()
    style.set_style("s2")
    try:
        shots, total, audio, mult = build(vid, rng)
        log(f"TikTok « {vid['title']} » partie {vid['part']}/{vid['parts']} : {total:.0f} s (voix x{mult:.2f})")
        w = wave.open(wav_path, "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(44100)
        w.writeframes((np.clip(compositeur.limit(audio), -1, 1) * 32767).astype("<i2").tobytes()); w.close()
        monteur.encode(frames(vid, shots, total, int(rng.integers(1e6))), out_mp4, gop=FPS * 2, audio=wav_path, crf=21, raster=raster_pair)
    finally:
        style.set_style("s2" if prev else "s1")
    return total
