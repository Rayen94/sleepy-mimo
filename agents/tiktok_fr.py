"""Série TikTok en français : des vidéos verticales de 62 à 90 s, 100 % séparées de YouTube (autres histoires, autre langue,
autre montage). Ce qui a fait ses preuves chez les petits comptes francophones (vidIQ, novembre 2026) :
  - la phrase d'accroche écrite à l'écran dès la première image, et la voix qui démarre tout de suite ;
  - des sous-titres dynamiques (le mot dit est surligné) ;
  - une histoire animée racontée en voix off, avec un suspense qui donne envie de voir la partie 2 ;
  - plus d'une minute (seuil du programme de récompenses TikTok).
Rien n'est repris d'un autre créateur : scénarios, dessins, voix et musique sont produits ici."""
import os
import io, math, wave, datetime, shutil
import numpy as np
from . import histoires as H, comediens as V, voixia, illustrateur as I, style, monteur, decors as D, compositeur, monde3d
from .tiktok_fr_scripts import BANK as _BANK_BASE, SERIE_FAITS
from .tiktok_fr_noel import DANS_FORET, ADVENT, SECRETS, GATEAUX, COURSE, SERIE_AVENT, SERIE_DANS

SR = V.SR
FPS = monteur.FPS
W, HT = 1080, 1920
ESPECES_3D = ("fox", "owl", "hedgehog", "bunny", "otter", "fawn", "beaver", "turtle")
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


def _order():
    """Ordre de sortie : d'abord les 3 séries de 3 parties (une partie de chaque série par tour, pour que le public attende la suite),
    puis « Dans cette forêt… » et le reste de la banque en alternance."""
    base, dans, out = list(_BANK_BASE), list(DANS_FORET), []
    for i in range(3):
        out += [SECRETS[i], GATEAUX[i], COURSE[i]]
    while base or dans:
        if dans:
            out.append(dans.pop(0))
        if base:
            out.append(base.pop(0))
    return out


BANK = _order()


def pick(date, n):
    """Les n vidéos du jour (déterministe : relancer la même journée redonne les mêmes vidéos).
    Du 1er au 24 décembre, la première place est prise par l'épisode du Calendrier de l'Avent du jour (s'il est écrit)."""
    target = date if isinstance(date, datetime.date) else datetime.date.fromisoformat(date)
    p, out = 0, []
    day = START
    while day <= target:
        slots, today = n, []
        adv = ADVENT.get(day.day) if day.month == 12 and day.day <= 24 else None
        if adv and slots:
            today.append(adv); slots -= 1
        for _ in range(slots):
            if p < len(BANK):
                today.append(BANK[p]); p += 1
        out = today
        day += datetime.timedelta(days=1)
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


def _jour(vid):
    try:
        return int(vid["label"].split()[1].split("/")[0])
    except Exception:
        return 0


def _cta(vid):
    if vid["serie"] == SERIE_AVENT:
        return ("narrator", "Suis-moi pour ne pas rater la suite du calendrier !"), ("Demain :", f"jour {_jour(vid) + 1} !")
    if vid["serie"] == SERIE_DANS:
        return ("narrator", "Suis-moi pour une nouvelle histoire dans cette forêt !"), ("Suis-moi pour", "la prochaine histoire !")
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


# ------------------------------------------------------------------ bruitages (faits ici, doux, sans droits d'auteur)
def _env(n, attack=0.01, decay=6.0):
    t = np.arange(n) / SR
    return np.minimum(1.0, t / attack) * np.exp(-decay * t)


def _whoosh(rng, dur=0.42):
    n = int(SR * dur); t = np.arange(n) / SR
    f = 250 + 1700 * (t / dur) ** 1.6
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR)
    noise = rng.standard_normal(n); noise = np.convolve(noise, np.ones(6) / 6, mode="same")
    env = np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 2
    return (0.55 * tone + 0.45 * noise) * env * 0.16


def _pop(f0=900, dur=0.14):
    n = int(SR * dur); t = np.arange(n) / SR
    f = f0 * np.exp(-6 * t)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * _env(n, 0.004, 22) * 0.20


def _sparkle():
    out = np.zeros(int(SR * 0.9))
    for k, f in enumerate((1318.5, 1760.0, 2093.0, 2637.0)):
        n = int(SR * 0.45); t = np.arange(n) / SR
        b = np.sin(2 * np.pi * f * t) * _env(n, 0.004, 7.5) * 0.10
        i = int(SR * 0.07 * k); out[i:i + n] += b
    return out


def sfx_track(shots, total, rng):
    """Petits bruitages aux endroits clés : « pop » à l'accroche, « whoosh » à chaque changement de décor,
    « pop » sur les exclamations des personnages, scintillement à la carte de fin."""
    n = int(total * SR)
    out = np.zeros(n)

    def put(t, y):
        i = int(t * SR)
        if 0 <= i < n:
            out[i:i + len(y)] += y[:n - i]
    put(0.03, _pop(700, 0.18))
    for sh in shots[1:]:
        put(max(0.0, sh["start"] - 0.12), _whoosh(rng))
    for sh in shots:
        for ln in sh["lines_t"]:
            if ln["who"] != "narrator" and "!" in ln["text"]:
                put(sh["start"] + ln["start"] + 0.02, _pop(1000 + 150 * int(rng.integers(0, 3)), 0.12))
    for t0, _kind in sticker_events(caption_events(shots)):
        put(t0, _pop(1300, 0.16))
    put(max(0.0, total - 3.0), _sparkle())
    return out



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
    fx = sfx_track(shots, total, rng)[:n]
    audio = voice_st + bg + np.stack([fx, fx], 1)
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
    space = max(_measure(" ", size), size * 0.30)
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


# ------------------------------------------------------------------ autocollants animés (comme les vidéos qui marchent)
KEYMAP = {
    "feuille": "leaf", "feuilles": "leaf", "etoile": "star", "etoiles": "star",
    "coeur": "heart", "merci": "heart", "aime": "heart", "adore": "heart", "amie": "heart",
    "neige": "flake", "flocon": "flake", "flocons": "flake",
    "cadeau": "gift", "cadeaux": "gift", "paquet": "gift", "echarpe": "gift",
    "lanterne": "flame", "bougie": "flame", "lumiere": "flame", "flamme": "flame", "lumieres": "flame",
    "lune": "moon", "piece": "coin", "pieces": "coin", "tresor": "coin", "or": "coin",
    "sapin": "tree", "arbre": "tree", "gateau": "cake", "pourquoi": "question", "mysterieux": "question", "mystere": "question",
    "peur": "alert", "attention": "alert", "tempete": "alert",
}


def _norm(w):
    import unicodedata
    w = unicodedata.normalize("NFD", w.lower().strip(".,!?;:«»\"'…()"))
    return "".join(c for c in w if unicodedata.category(c) != "Mn")


def sticker_events(events, first=3.9, gap=2.4, limit=14):
    """(début, type) : un autocollant jaillit à l'écran quand le mot correspondant est prononcé."""
    out, last = [], -9.0
    for t0, _t1, grp, j in events:
        kind = KEYMAP.get(_norm(grp[j]))
        if kind and t0 >= first and t0 - last >= gap and len(out) < limit:
            out.append((t0, kind)); last = t0
    return out


def _icon(kind):
    """Dessins simples (cadre 100 x 100)."""
    st = 'stroke="#FFFFFF" stroke-width="6" stroke-linejoin="round" paint-order="stroke"'
    if kind == "leaf":
        return (f'<path d="M50 92 C12 62 18 20 50 6 C82 20 88 62 50 92 Z" fill="#5BC85A" {st}/>'
                '<path d="M50 88 L50 22 M50 62 L32 46 M50 50 L68 34 M50 74 L70 58" stroke="#2C8F3C" stroke-width="4" fill="none" stroke-linecap="round"/>')
    if kind == "star":
        return f'<polygon points="50,6 62,37 95,38 69,58 79,92 50,72 21,92 31,58 5,38 38,37" fill="#FFD84A" {st}/>'
    if kind == "heart":
        return f'<path d="M50 90 C6 58 4 24 27 15 C40 11 48 19 50 27 C52 19 60 11 73 15 C96 24 94 58 50 90 Z" fill="#FF5C7A" {st}/>'
    if kind == "flake":
        arms = "".join(f'<g transform="rotate({a} 50 50)"><path d="M50 8 L50 92 M50 22 L40 12 M50 22 L60 12 M50 78 L40 88 M50 78 L60 88" /></g>' for a in (0, 60, 120))
        return f'<g stroke="#FFFFFF" stroke-width="12" stroke-linecap="round" fill="none">{arms}</g><g stroke="#8ED0FF" stroke-width="6" stroke-linecap="round" fill="none">{arms}</g>'
    if kind == "gift":
        return (f'<rect x="14" y="42" width="72" height="48" rx="5" fill="#E5484D" {st}/><rect x="9" y="30" width="82" height="18" rx="5" fill="#C9333A" {st}/>'
                '<rect x="44" y="30" width="12" height="60" fill="#FFD84A"/><ellipse cx="38" cy="22" rx="14" ry="10" fill="#FFD84A" stroke="#E0A800" stroke-width="3"/>'
                '<ellipse cx="62" cy="22" rx="14" ry="10" fill="#FFD84A" stroke="#E0A800" stroke-width="3"/>')
    if kind == "flame":
        return (f'<rect x="36" y="52" width="28" height="40" rx="4" fill="#FFF1D0" {st}/>'
                f'<path d="M50 4 C66 24 70 36 50 54 C30 36 34 24 50 4 Z" fill="#FFB02E" {st}/><path d="M50 22 C58 32 58 40 50 48 C42 40 42 32 50 22 Z" fill="#FFE27A"/>')
    if kind == "moon":
        return f'<path d="M64 8 A42 42 0 1 0 92 64 A34 34 0 1 1 64 8 Z" fill="#FFE9A8" {st}/>'
    if kind == "coin":
        return (f'<circle cx="50" cy="50" r="42" fill="#FFD23F" {st}/><circle cx="50" cy="50" r="31" fill="none" stroke="#E0A800" stroke-width="5"/>'
                '<path d="M36 38 Q50 24 64 38" stroke="#FFF3B0" stroke-width="6" fill="none" stroke-linecap="round"/>')
    if kind == "tree":
        return (f'<rect x="43" y="76" width="14" height="18" fill="#7A4B26"/><polygon points="50,8 78,40 62,40 86,68 14,68 38,40 22,40" fill="#2E9E5B" {st}/>'
                '<circle cx="42" cy="56" r="4" fill="#FF5C7A"/><circle cx="60" cy="46" r="4" fill="#FFD84A"/><circle cx="52" cy="66" r="4" fill="#8ED0FF"/>')
    if kind == "cake":
        return (f'<rect x="12" y="58" width="76" height="32" rx="6" fill="#F2A65A" {st}/><rect x="20" y="38" width="60" height="26" rx="6" fill="#FFE1B8" {st}/>'
                '<rect x="46" y="18" width="8" height="20" fill="#8ED0FF"/><path d="M50 4 C57 12 57 16 50 20 C43 16 43 12 50 4 Z" fill="#FFB02E"/>')
    if kind == "question":
        return (f'<circle cx="50" cy="50" r="42" fill="#7C5CFF" {st}/><text x="50" y="72" font-family="Fredoka, sans-serif" font-weight="700" font-size="66" text-anchor="middle" fill="#FFFFFF">?</text>')
    return (f'<circle cx="50" cy="50" r="42" fill="#FF8A3D" {st}/><text x="50" y="72" font-family="Fredoka, sans-serif" font-weight="700" font-size="66" text-anchor="middle" fill="#FFFFFF">!</text>')


def _sticker_svg(kind, t, idx, size=250):
    """Un autocollant qui jaillit (rebond), flotte un peu, puis disparaît."""
    dur = 1.7
    u = min(1.0, t / 0.28)
    pop = 0.3 + 0.7 * (1 + 2.70158 * (u - 1) ** 3 + 1.70158 * (u - 1) ** 2)
    fade = 1.0 if t < dur - 0.3 else max(0.0, (dur - t) / 0.3)
    x = 540 + (-250 if idx % 2 == 0 else 250) * 0.8 * (1 if idx % 3 else 0.0)
    y = 640 - 28 * t
    rot = (-7 if idx % 2 == 0 else 7) * (1 - u) + 4 * math.sin(2 * math.pi * 0.9 * t)
    sc = size / 100 * pop
    return (f'<g opacity="{fade:.3f}" transform="translate({x:.0f} {y:.0f}) rotate({rot:.1f}) scale({sc:.3f}) translate(-50 -50)">'
            f'<g opacity="0.35" transform="translate(4 6)">{_icon(kind)}</g>{_icon(kind)}</g>')


# ------------------------------------------------------------------ images
FRAMING = {                       # (zoom, hauteur de la caméra au-dessus du sol, centrée sur la tête ?)
    "wide": (1.00, 70, False), "med": (1.28, 64, False), "close": (1.65, 54, True), "xclose": (2.05, 50, True),
}
_CYCLE = ["wide", "close", "med", "close", "med", "xclose"]


def _beats(sh):
    """Temps de caméra d'un plan : un changement de cadre à chaque réplique, et toutes les ~3,4 s dans les longues répliques."""
    cuts = [0.0]
    for ln in sh["lines_t"]:
        cuts.append(ln["start"])
        if ln["dur"] > 5.0:
            n = int(ln["dur"] // 3.4)
            cuts += [ln["start"] + ln["dur"] * k / (n + 1) for k in range(1, n + 1)]
    cuts = sorted(set(round(c, 3) for c in cuts))
    return [c for i, c in enumerate(cuts) if i == 0 or c - cuts[i - 1] > 1.1] or [0.0]


def _frame_for(sh, k, t, first_shot):
    """Cadre du k-ième temps : large au début, puis gros plans sur celui qui parle (ou en alternance pendant le narrateur)."""
    kind = "wide" if k == 0 else _CYCLE[k % len(_CYCLE)]
    ln = next((l for l in sh["lines_t"] if l["start"] <= t + 0.05 < l["start"] + l["dur"]), None)
    if ln and ln["who"] != "narrator" and kind == "close" and ("!" in ln["text"] or "?" in ln["text"]):
        kind = "xclose"
    who = None
    if ln and ln["who"] != "narrator":
        who = ln["who"]
    else:                                                  # narrateur : on alterne entre les personnages à l'écran
        cast = [c[0] for c in sh["cast"]]
        who = cast[k % len(cast)]
    return kind, who


def frames(vid, shots, total, seed, mode3d=False):
    """Génère des paires (décor, texte) : le décor passe par l'étalonnage « cinéma », le texte reste net par-dessus.
    mode3d : le premier élément est alors l'état de la scène 3D (dict) au lieu d'un dessin."""
    n = int(round(total * FPS))
    events = caption_events(shots)
    ei = 0
    s = HT / 720
    series = vid["serie"]
    part_tag = vid.get("label") or (f"PARTIE {vid['part']}/{vid['parts']}" if vid["parts"] > 1 else None)
    hook_rows = H._wrap(vid["hook"], 17)
    _, end_pair = _cta(vid)
    beats = [_beats(sh) for sh in shots]
    stickers = sticker_events(events)
    last_key, cx_s, cy_w, zoom0, beat_t0, beat_len = None, 0.0, 0.0, 1.0, 0.0, 3.0
    for kf in range(n):
        ts = kf / FPS
        si = max((i for i, sh in enumerate(shots) if sh["start"] <= ts + 1e-6), default=0)
        sh = shots[si]
        local = max(0.0, ts - sh["start"])
        acts, speaking = H.actors(sh, local)
        bk = max(i for i, c in enumerate(beats[si]) if c <= local + 1e-6)
        gy = D.ground(sh["decor"])
        kind, who = _frame_for(sh, bk, beats[si][bk], si == 0)
        z0, off, head = FRAMING[kind]
        tgt_act = next((a for a in acts if a["who"] == who), acts[0])
        mid = sum(a["x"] for a in acts) / len(acts)
        if kind == "wide":
            target = mid
        elif kind == "med":
            target = mid + 0.7 * (tgt_act["x"] - mid)
        else:
            target = tgt_act["x"] + 70 * tgt_act["f"]
        if (si, bk) != last_key:                           # changement de cadre : coupe franche, pas de glissement
            last_key = (si, bk)
            cx_s, cy_w, zoom0, beat_t0 = target, gy - off, z0, ts
            nxt = beats[si][bk + 1] if bk + 1 < len(beats[si]) else sh["dur"]
            beat_len = max(1.0, nxt - beats[si][bk])
        else:
            cx_s += (target - cx_s) * 0.12
        lb = ts - beat_t0
        zoom = zoom0 * (1.0 + 0.05 * min(1.0, lb / beat_len) + 0.07 * max(0.0, 1 - lb / 0.22) ** 2)
        if mode3d:
            yaw = (0.11 if bk % 2 == 0 else -0.11) if kind == "wide" else -0.2 * tgt_act["f"] + (0.05 if bk % 2 else -0.05)
            yaw += 0.05 * min(1.0, lb / beat_len) * (1 if bk % 2 == 0 else -1)
            world = dict(decor=sh["decor"], seed=(seed + si) % 99991, t=round(ts, 4),
                         cam=dict(x=round(cx_s, 2), kind=kind, zoom=round(zoom / zoom0, 4), yaw=round(yaw, 4)),
                         actors=[dict(who=a["who"], x=round(a["x"], 2), f=a["f"], jump=round(a["jump"], 2), tilt=round(a["tilt"], 2),
                                      mouth=round(a["mouth"], 3), blink=bool(a["blink"]), walk=round(a["walk"], 3), wave=round(a["wave"], 3),
                                      look=a["look"], moving=bool(a["moving"])) for a in acts if a["who"] in ESPECES_3D])
        else:
            world = (f'<g transform="translate({W/2} 1080) scale({s * zoom:.4f}) translate({-cx_s:.1f} {-cy_w:.1f})">'
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
            u = min(1.0, ts / 0.3)
            pop = 0.8 + 0.2 * (1 + 2.70158 * (u - 1) ** 3 + 1.70158 * (u - 1) ** 2)
            cy_h = y0 - 95 + h / 2
            over.append(f'<g opacity="{op:.3f}" transform="translate({W/2} {cy_h:.0f}) scale({pop:.3f}) translate({-W/2} {-cy_h:.0f})">{"".join(block)}</g>')
        # autocollants qui jaillissent sur les mots importants
        for si_, (st0, kind) in enumerate(stickers):
            if st0 <= ts < st0 + 1.7:
                over.append(_sticker_svg(kind, ts - st0, si_))
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
        yield (world if mode3d else I.svg(W, HT, world), I.svg(W, HT, "".join(over)))


def raster_pair(pair):
    import cairosvg
    from PIL import Image
    from . import cinema
    world, over = pair
    if world.startswith("<"):
        raw = cairosvg.svg2png(bytestring=world.encode())
    else:                                                 # image 3D déjà rendue par render3d
        with open(world, "rb") as f:
            raw = f.read()
    base = Image.open(io.BytesIO(cinema.look(raw))).convert("RGBA")
    top = Image.open(io.BytesIO(cairosvg.svg2png(bytestring=over.encode()))).convert("RGBA")
    base.alpha_composite(top)
    buf = io.BytesIO()
    base.convert("RGB").save(buf, "PNG", compress_level=1)
    return buf.getvalue()


# ------------------------------------------------------------------ production
def legende(vid):
    """Description TikTok en français, prête à copier-coller."""
    if vid["serie"] == SERIE_AVENT:
        return f"{vid['hook']} ({SERIE_AVENT}, {vid['label'].lower()}) Un nouvel épisode chaque jour jusqu'à Noël, suis-moi pour ne rien rater ! {vid['tags']}"
    if vid["serie"] == SERIE_DANS:
        return f"{vid['hook']} ({vid['serie']}) Suis-moi pour d'autres histoires dans cette forêt ! {vid['tags']}"
    if vid["parts"] > 1:
        suite = f"La partie {vid['part'] + 1} arrive très vite, suis-moi pour ne pas la rater !" if vid["part"] < vid["parts"] else "Suis-moi pour la prochaine série !"
        return f"Histoire animée en 3D, partie {vid['part']}/{vid['parts']} : {vid['hook']} ({vid['serie']} - {vid['title']}) {suite} {vid['tags']}"
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
        seed = int(rng.integers(1e6))
        if monde3d.disponible() and not os.environ.get("TIKTOK_2D"):
            etats = [st for st, _ in frames(vid, shots, total, seed, mode3d=True)]
            dossier = out_mp4.replace(".mp4", "_3d")
            monde3d.rendre(etats, dossier, log=log)
            paires = ((os.path.join(dossier, f"f{i:06d}.jpg"), over) for i, (_, over) in enumerate(frames(vid, shots, total, seed, mode3d=True)))
            monteur.encode(paires, out_mp4, gop=FPS * 2, audio=wav_path, crf=21, raster=raster_pair)
            shutil.rmtree(dossier, ignore_errors=True)
        else:
            monteur.encode(frames(vid, shots, total, seed), out_mp4, gop=FPS * 2, audio=wav_path, crf=21, raster=raster_pair)
    finally:
        style.set_style("s2" if prev else "s1")
    return total


def commentaire(vid):
    """Question à épingler en premier commentaire (c'est toi qui l'écris sous la vidéo) : les commentaires et les partages
    pèsent beaucoup dans la diffusion, et une question simple donne envie de répondre."""
    if vid["serie"] == SERIE_AVENT:
        return "Quel est ton moment préféré de Noël ? Dis-le en commentaire, et dis-moi quelle histoire tu veux demain 👇"
    if vid["serie"] == SERIE_DANS:
        return "Et toi, tu aurais fait quoi à sa place ? Dis-le en commentaire, et propose-moi une autre règle étrange pour cette forêt 👇"
    if vid["serie"] == SERIE_FAITS:
        return "Tu connaissais ce secret ? Dis-moi en commentaire quel animal tu veux découvrir ensuite 👇"
    if vid["part"] < vid["parts"]:
        return f"À ton avis, que va-t-il se passer dans la partie {vid['part'] + 1} ? Réponds en commentaire, je lis tout 👇"
    return "Quelle est la leçon de cette histoire pour toi ? Dis-le en commentaire, et dis-moi quelle fable tu veux ensuite 👇"


def find(vid_id):
    for v in list(BANK) + list(ADVENT.values()) + list(SECRETS) + list(GATEAUX) + list(COURSE):
        if v["id"] == vid_id:
            return v
    raise KeyError(f"scénario inconnu : {vid_id}")


def produce(date, n, out_dir, log=print, ids=None, only=None):
    """Produit les vidéos TikTok du jour dans out_dir (+ tiktok.md, légendes françaises).
    ids : liste d'identifiants imposés ; only : ne produire que la k-ième vidéo (pour les rendre en parallèle sur GitHub)."""
    notes = []
    vids = [find(i) for i in ids] if ids else pick(date, n)
    if not vids:
        notes.append("TikTok : tous les scénarios de la série sont déjà sortis. Dis-moi d'en écrire de nouveaux.")
        log(notes[-1]); return notes
    os.makedirs(out_dir, exist_ok=True)
    entete = ["# Vidéos TikTok du jour (en français)", "",
              "Poste-les dans l'ordre, avec quelques heures d'écart. Coche « contenu généré par IA » dans TikTok. "
              "Copie la légende telle quelle (elle contient les mots-clés).",
              "Heures à tester en France : vers 12 h 30, 18 h 30 et 20 h 30 (ensuite, regarde dans les statistiques TikTok à quelle heure ton public est connecté).",
              "Après avoir posté : épingle le commentaire proposé ci-dessous, puis réponds aux premiers commentaires dans l'heure (c'est toi qui écris, à la main).", ""]
    md = list(entete)
    for i, vid in enumerate(vids, 1):
        if only and i != only:
            continue
        rng_tt = np.random.default_rng(int(date.replace("-", "")) * 10 + i)
        dur = make(vid, f"{out_dir}/tiktok{i}.mp4", rng_tt, log=log)
        part = f", partie {vid['part']}/{vid['parts']}" if vid["parts"] > 1 else ""
        section = [f"## tiktok{i}.mp4 — {vid['serie']} : {vid['title']}{part} ({dur:.0f} s)", "", "Légende :", "", legende(vid), "",
                   "Commentaire à épingler :", "", commentaire(vid), ""]
        notes.append(f"TikTok {i} : {vid['serie']} — {vid['title']}{part} ({dur:.0f} s), fichier tiktok{i}.mp4")
        if only:
            open(f"{out_dir}/tiktok{i}.md", "w", encoding="utf-8").write("\n".join(section))
        md += section
    if not only:
        open(f"{out_dir}/tiktok.md", "w", encoding="utf-8").write("\n".join(md))
    elif not notes:
        notes.append(f"TikTok : pas de vidéo n°{only} aujourd'hui.")
    return notes
