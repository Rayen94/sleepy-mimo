"""Agent 2 — Stratège contenu : choisit les thèmes, les morceaux et les instruments du jour,
en évitant les répétitions grâce à la mémoire de la chaîne."""
from .illustrateur import THEMES
from .compositeur import PUBLIC_DOMAIN, VOICES, track_spec

ADJ = ["Starlight", "Moonbeam", "Cozy", "Dreamy", "Twinkly", "Snuggly", "Gentle", "Velvet", "Silver", "Sleepy",
       "Cuddly", "Whisper", "Feather", "Honey", "Lavender", "Stardust", "Pillow", "Misty"]
NOUN = ["Lullaby", "Dream", "Melody", "Goodnight", "Song", "Serenade", "Tune", "Nap Song", "Night Song", "Hush"]


def original_name(rng, used):
    for _ in range(200):
        n = f"Mimo's {ADJ[rng.integers(len(ADJ))]} {NOUN[rng.integers(len(NOUN))]}"
        if n not in used:
            return n
    return f"Mimo's Lullaby No. {len(used) + 1}"


def plan_day(rng, memory, cfg):
    long_minutes, short_seconds = cfg["long_minutes"], cfg["short_seconds"]
    recent = memory.recent_themes(days=2)
    allowed = [t for t in THEMES if t in cfg["themes"]] or list(THEMES)
    themes = [t for t in allowed if t not in recent] or allowed
    long_theme = cfg["long_theme"] or themes[rng.integers(len(themes))]
    others = [t for t in allowed if t != long_theme] or allowed
    rng.shuffle(others)
    short_themes = [others[i % len(others)] for i in range(cfg["n_shorts"])]
    used = memory.used_original_names()

    tracks, total = [], 0.0
    pd_names = [n for n in PUBLIC_DOMAIN if n in cfg["songs"]]; rng.shuffle(pd_names)
    pool = [v for v in VOICES if v in cfg["voices"]] or list(VOICES)
    voices_long = [str(v) for v in rng.permutation(pool)[:2]]
    if len(voices_long) == 1:
        voices_long *= 2
    i = 0
    while total < long_minutes * 60:
        if pd_names and rng.uniform(0, 100) >= cfg["original_pct"]:
            item = ("pd", pd_names.pop())
        else:
            name = original_name(rng, used); used.add(name)
            item = ("orig", name)
        voice = voices_long[0] if total < long_minutes * 30 else voices_long[1]
        seconds = float(rng.uniform(150, 210))
        tracks.append(dict(item=item, spec=track_spec(item, rng), voice=voice,
                           octave=12 if voice in ("box", "bell") else 0,
                           transpose=int(rng.integers(-3, 4)), tempo=float(rng.uniform(0.82, 1.0)), seconds=seconds))
        total += seconds + 6
        i += 1

    shorts = []
    for th in short_themes:
        name = original_name(rng, used); used.add(name)
        voice = str(pool[rng.integers(len(pool))])
        ov = cfg["overlays"][rng.integers(len(cfg["overlays"]))]
        shorts.append(dict(theme=th, overlay=ov, name=name, spec=track_spec(("orig", name), rng), voice=voice,
                           octave=12 if voice in ("box", "bell") else 0,
                           transpose=int(rng.integers(-3, 4)), seconds=short_seconds))
    return dict(long_theme=long_theme, tracks=tracks, voices=voices_long, shorts=shorts)
