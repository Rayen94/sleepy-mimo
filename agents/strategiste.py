"""Agent 2 — Stratège contenu : choisit les thèmes, les morceaux et les instruments du jour,
en évitant les répétitions grâce à la mémoire de la chaîne."""
import math
from .illustrateur import THEMES
from .compositeur import PUBLIC_DOMAIN, VOICES, track_spec
from .parolier import LYRICS

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

    # Vidéo longue : plusieurs décors (un toutes les ~X minutes), chacun avec son instrument
    n_scenes = max(1, min(len(allowed), round(long_minutes / cfg["scene_minutes"])))
    rest = [t for t in allowed if t != long_theme]; rng.shuffle(rest)
    scene_themes = [long_theme] + rest[:n_scenes - 1]
    pool = [v for v in VOICES if v in cfg["voices"]] or list(VOICES)
    order = [str(v) for v in rng.permutation(pool)]
    scene_voices = [order[i % len(order)] for i in range(len(scene_themes))]

    tracks, total = [], 0.0
    pd_pool = [n for n in PUBLIC_DOMAIN if n in cfg["songs"]]
    pd_names, last_pd = [], None
    target = long_minutes * 60
    story = None
    if cfg.get("story", True):
        from .saison1 import EPISODES          # la série : les épisodes sont diffusés dans l'ordre
        story = EPISODES[(memory.next_episode() - 1) % len(EPISODES)]
    forced = story["song"] if story and story["song"] in PUBLIC_DOMAIN else None
    while total < target:
        si = min(int(total / (target / len(scene_themes))), len(scene_themes) - 1)
        if forced:
            item = ("pd", forced); last_pd = forced; forced = None
        elif pd_pool and rng.uniform(0, 100) >= cfg["original_pct"]:
            if not pd_names:                      # on refait un tour des comptines, sans répéter la dernière
                pd_names = list(pd_pool); rng.shuffle(pd_names)
                if len(pd_names) > 1 and pd_names[-1] == last_pd:
                    pd_names[0], pd_names[-1] = pd_names[-1], pd_names[0]
            item = ("pd", pd_names.pop()); last_pd = item[1]
        else:
            name = original_name(rng, used); used.add(name)
            item = ("orig", name)
        voice = scene_voices[si]
        spec = track_spec(item, rng)
        tempo = float(rng.uniform(0.82, 1.0))
        L = sum(d for _, d in spec[1]) * 60 / (spec[0] * tempo)          # durée d'un passage du morceau
        reps = max(1, round(float(rng.uniform(150, 200)) / L))
        seconds = min(reps * L - 0.01, target - total + 30)
        reps = max(1, math.ceil(seconds / L))
        lyrics = item[1] if (item[0] == "pd" and cfg.get("vocals", True) and item[1] in LYRICS) else None
        tracks.append(dict(item=item, spec=spec, voice=voice, scene=si, theme=scene_themes[si], lyrics=lyrics,
                           octave=12 if voice in ("box", "bell") else 0,
                           transpose=int(rng.integers(-3, 4)), tempo=tempo, seconds=seconds))
        total += reps * L + 4 + 2       # durée réelle : passages + fin + silence
    voices_long = list(dict.fromkeys(scene_voices))

    shorts = []
    for th in short_themes:
        name = original_name(rng, used); used.add(name)
        voice = str(pool[rng.integers(len(pool))])
        ov = cfg["overlays"][rng.integers(len(cfg["overlays"]))]
        hook = cfg["hooks"][rng.integers(len(cfg["hooks"]))]
        shorts.append(dict(theme=th, overlay=ov, hook=hook, name=name, spec=track_spec(("orig", name), rng), voice=voice,
                           octave=12 if voice in ("box", "bell") else 0,
                           transpose=int(rng.integers(-3, 4)), seconds=short_seconds))
    return dict(long_theme=long_theme, scene_themes=scene_themes, tracks=tracks, voices=voices_long, shorts=shorts, story=story)
