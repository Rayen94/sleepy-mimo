"""Agent 6 — Rédacteur SEO : titres, descriptions et tags en anglais, sans promesses trompeuses."""
from .illustrateur import THEMES
from .compositeur import VOICE_NAMES

PROP_SENTENCE = {"moon": "falls asleep on the moon", "cloud": "drifts off on a soft cloud", "boat": "rocks gently in his little boat"}
FX_SENTENCE = {"stars": "under twinkling stars", "snow": "while snowflakes fall", "fireflies": "among glowing fireflies",
               "rain": "to the sound of a gentle rain"}

LONG_TITLES = [
    "{theme} Lullabies for Babies 😴 {m} Min of {voice} Sleep Music | Sleepy Mimo",
    "Baby Sleep Music 🌙 {m} Minutes of {voice} Lullabies | {theme} | Sleepy Mimo",
    "{voice} Lullabies for Babies to Go to Sleep 💤 {theme} | {m} Min | Sleepy Mimo",
    "Bedtime Lullabies for Babies & Toddlers ⭐ {theme} {voice} | {m} Min | Sleepy Mimo",
]
SHORT_TITLES = [
    "Mimo {action} {fx} 💤 {song} #shorts #lullaby",
    "{song} 🌙 Baby Lullaby #shorts #babysleep",
    "Sleepy Mimo {action} ✨ Lullaby for Babies #shorts",
]


def fmt(sec):
    sec = int(sec)
    return f"{sec // 3600}:{sec % 3600 // 60:02d}:{sec % 60:02d}" if sec >= 3600 else f"{sec // 60}:{sec % 60:02d}"


def long_meta(rng, plan, stamps, total, used_titles, extra_tags=()):
    th = THEMES[plan["long_theme"]]
    m = int(round(total / 60))
    voice = " & ".join(VOICE_NAMES[v] for v in dict.fromkeys(plan["voices"]))
    voice_short = VOICE_NAMES[plan["voices"][0]]
    title = None
    order = list(rng.permutation(len(LONG_TITLES)))
    for i in order:
        cand = LONG_TITLES[i].format(theme=th["name"], m=m, voice=voice_short)
        if cand not in used_titles and len(cand) <= 100:
            title = cand; break
    title = title or f"{th['name']} Lullabies for Babies 😴 {m} Min | Sleepy Mimo #{len(used_titles)+1}"
    chapters = []
    for pos, p in stamps:
        name = p["item"][1]
        chapters.append(f"{fmt(pos)} {name} ({VOICE_NAMES[p['voice']]})")
    desc = (f"🌙 Mimo the little bear {PROP_SENTENCE[th['prop']]} {FX_SENTENCE[th['fx']]}… and so will your baby!\n\n"
            f"{m} minutes of gentle {voice.lower()} lullabies to help babies and toddlers wind down for naptime and bedtime. "
            f"Original melodies by Sleepy Mimo and new arrangements of traditional nursery songs.\n\n"
            + "\n".join(chapters) +
            "\n\n💤 Subscribe for new lullabies with Mimo!\n\n#lullaby #babysleepmusic #bedtime")
    tags = ["lullabies for babies", "baby sleep music", "bedtime lullabies", f"{th['name'].lower()} lullaby",
            f"{voice_short.lower()} lullaby", "lullaby for babies to go to sleep", "soothing music for babies",
            "toddler bedtime songs", f"{m} minute lullaby", "sleepy mimo", "baby lullaby", "relaxing baby music"] + list(extra_tags)
    return dict(title=title, description=desc, tags=tags)


def short_meta(rng, s, used_titles, extra_tags=()):
    th = THEMES[s["theme"]]
    small = {"on", "the", "a", "in", "his", "off"}
    action = " ".join(w if (w in small and i) else w.capitalize() for i, w in enumerate(PROP_SENTENCE[th["prop"]].split()))
    for i in rng.permutation(len(SHORT_TITLES)):
        cand = SHORT_TITLES[i].format(action=action, fx=FX_SENTENCE[th["fx"]], song=s["name"])
        if cand not in used_titles and len(cand) <= 100:
            title = cand; break
    else:
        title = f"{s['name']} 💤 #shorts"
    desc = (f"Mimo {PROP_SENTENCE[th['prop']]} {FX_SENTENCE[th['fx']]}. 🌙\n"
            f"\"{s['name']}\" — an original {VOICE_NAMES[s['voice']].lower()} lullaby by Sleepy Mimo.\n\n"
            "Full-length lullabies on the channel 💤\n#shorts #lullaby #babysleep")
    tags = ["lullaby", "baby sleep", "shorts", "sleepy mimo", "baby lullaby", "bedtime"] + list(extra_tags)
    return dict(title=title, description=desc, tags=tags)


def short_overlay(s, W, H):
    from .illustrateur import text
    lines = s["overlay"]
    return text(W / 2, H * 0.14, lines[0], 84, "#FFF4C9") + text(W / 2, H * 0.14 + 100, lines[1], 84, "#FFD35C")
