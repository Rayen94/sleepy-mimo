"""Agent 6 — Rédacteur SEO : titres, descriptions et tags en anglais, sans promesses trompeuses."""
from .illustrateur import THEMES
from .compositeur import VOICE_NAMES, AMBIENCE, AMBIENCE_NAMES

PROP_SENTENCE = {"moon": "falls asleep on the moon", "cloud": "drifts off on a soft cloud", "boat": "rocks gently in his little boat"}
FX_SENTENCE = {"stars": "under twinkling stars", "snow": "while snowflakes fall", "fireflies": "among glowing fireflies",
               "rain": "to the sound of a gentle rain"}

LONG_TITLES = [
    "Baby Sleep Music 🌙 {dur} of {voice} Lullabies | {theme} | Sleepy Mimo",
    "Lullabies for Babies to Go to Sleep 😴 {dur} | {voice} & {amb} | Sleepy Mimo",
    "{theme} Lullabies for Babies 💤 {dur} of Soothing Sleep Music | Sleepy Mimo",
    "Bedtime Lullabies for Babies & Toddlers ⭐ {dur} of {voice} | Sleepy Mimo",
    "{dur} Baby Lullaby with {amb} 🌙 Calm {voice} Music for Sleep | Sleepy Mimo",
]
SHORT_TITLES = [
    "Play This When Your Baby Can't Sleep 🌙 {song} #shorts #lullaby",
    "Shhh… Mimo Is Sleeping 💤 {song} #shorts #babysleep",
    "{secs} Seconds of Calm for Your Baby ✨ {song} #shorts",
    "Mimo {action} {fx} 💤 #shorts #lullaby",
]


def dur_label(sec):
    m = int(round(sec / 60))
    if m >= 55:
        h = round(m / 60)
        return f"{h} Hour" + ("s" if h > 1 else "")
    return f"{m} Min"


def fmt(sec):
    sec = int(sec)
    return f"{sec // 3600}:{sec % 3600 // 60:02d}:{sec % 60:02d}" if sec >= 3600 else f"{sec // 60}:{sec % 60:02d}"


SUNG_TITLES = [
    "Bedtime Sing-Along Lullabies for Babies 🌙 {dur} with Lyrics | Sleepy Mimo",
    "Nursery Rhymes & Lullabies for Babies 😴 {dur} | Sing Along with Mimo",
    "Twinkle Twinkle Little Star & More Bedtime Songs 💤 {dur} | Sleepy Mimo",
    "Sleepy Nursery Rhymes for Babies & Toddlers ⭐ {dur} with Lyrics | Sleepy Mimo",
]


STORY_TITLES = [
    "Sleepy Mimo Episode {ep}: {story} 🌙 Bedtime Story & Lullabies",
    "{story} ✨ Sleepy Mimo Episode {ep} | Story + Nursery Rhymes for Kids",
    "Sleepy Mimo Ep. {ep} 😴 {story} | Bedtime Story & Sing-Along Songs",
]


def long_meta(rng, plan, stamps, total, used_titles, extra_tags=(), sung=False, story=None):
    th = THEMES[plan["long_theme"]]
    dur = dur_label(total)
    voice = " & ".join(VOICE_NAMES[v] for v in dict.fromkeys(plan["voices"]))
    voice_short = VOICE_NAMES[plan["voices"][0]]
    amb = AMBIENCE_NAMES[AMBIENCE[plan["long_theme"]]]
    title = None
    pool = STORY_TITLES if story else (SUNG_TITLES if sung else LONG_TITLES)
    for i in rng.permutation(len(pool)):
        cand = pool[i].format(theme=th["name"], dur=dur, voice=voice_short, amb=amb, story=story["title"] if story else "", ep=story.get("episode", "") if story else "")
        if cand not in used_titles and len(cand) <= 100:
            title = cand; break
    title = title or f"{th['name']} Lullabies for Babies 😴 {dur} | Sleepy Mimo #{len(used_titles)+1}"
    chapters = []
    if story:
        chapters.append(f"0:00 Story: {story['title']}")
    for j, (pos, p) in enumerate(stamps):
        pos = 0 if (j == 0 and not story) else pos          # YouTube exige un premier chapitre à 0:00
        chapters.append(f"{fmt(pos)} {p['item'][1]} ({VOICE_NAMES[p['voice']]})")
    journey = [THEMES[t]["name"] for t in plan["scene_themes"]]
    trip = (f"Tonight Mimo drifts through {len(journey)} dreamy places: " + ", ".join(journey[:-1]) + f" and {journey[-1]}."
            if len(journey) > 1 else "")
    songs = list(dict.fromkeys(p["item"][1] for _, p in stamps if p.get("lyrics")))
    singalong = ""
    if songs:
        names = songs[0] if len(songs) == 1 else ", ".join(songs[:-1]) + " and " + songs[-1]
        singalong = f"🎤 Sing along with Mimo! Lyrics on screen for {names}.\n"
    storyline = (f"📺 Sleepy Mimo, episode {story.get('episode', '')}: {story['title']}.\n"
                 f"📖 Mimo and his friends talk, play and help each other before bedtime. A new episode of the series every day!\n"
                 if story else "")
    desc = (storyline + f"🌙 Mimo the little bear {PROP_SENTENCE[th['prop']]} {FX_SENTENCE[th['fx']]}… and so will your baby!\n\n" + singalong +
            f"{dur} of gentle {voice.lower()} lullabies with soft background sounds to help babies and toddlers wind down "
            f"for naptime and bedtime. {trip}\n"
            f"Original melodies by Sleepy Mimo and new arrangements of traditional nursery songs.\n\n"
            "⏱️ Chapters\n" + "\n".join(chapters) +
            "\n\n💤 Subscribe for new lullabies with Mimo!\n\n#lullaby #babysleepmusic #bedtime")
    tags = ["lullabies for babies", "baby sleep music", "bedtime lullabies", f"{th['name'].lower()} lullaby",
            f"{voice_short.lower()} lullaby", "lullaby for babies to go to sleep", "soothing music for babies",
            "toddler bedtime songs", f"{dur.lower()} lullaby", f"lullaby with {amb.lower()}", "sleepy mimo",
            "baby lullaby", "relaxing baby music"] + list(extra_tags)
    return dict(title=title, description=desc, tags=tags)


def short_meta(rng, s, used_titles, extra_tags=()):
    th = THEMES[s["theme"]]
    small = {"on", "the", "a", "in", "his", "off"}
    action = " ".join(w if (w in small and i) else w.capitalize() for i, w in enumerate(PROP_SENTENCE[th["prop"]].split()))
    for i in rng.permutation(len(SHORT_TITLES)):
        cand = SHORT_TITLES[i].format(action=action, fx=FX_SENTENCE[th["fx"]], song=s["name"], secs=int(s["seconds"]))
        if cand not in used_titles and len(cand) <= 100:
            title = cand; break
    else:
        title = f"{s['name']} 💤 #shorts"
    desc = (f"Mimo {PROP_SENTENCE[th['prop']]} {FX_SENTENCE[th['fx']]}. 🌙\n"
            f"\"{s['name']}\" — an original {VOICE_NAMES[s['voice']].lower()} lullaby by Sleepy Mimo.\n\n"
            "Full-length lullabies on the channel 💤\n#shorts #lullaby #babysleep")
    tags = ["lullaby", "baby sleep", "shorts", "sleepy mimo", "baby lullaby", "bedtime"] + list(extra_tags)
    return dict(title=title, description=desc, tags=tags)


def short_story_meta(rng, story, part, parts, used_titles, extra_tags=()):
    ep, t = story["episode"], story["title"]
    pt = f" (Part {part})" if parts > 1 else ""
    cands = [f"{t}{pt} 🌙 Sleepy Mimo Episode {ep} #shorts #kids",
             f"Sleepy Mimo Ep. {ep}: {t}{pt} ✨ #shorts #bedtimestory",
             f"{t}{pt} 💤 Bedtime Story for Kids | Sleepy Mimo #shorts"]
    title = next((c for c in cands if c not in used_titles and len(c) <= 100), cands[0][:100])
    desc = (f"A little moment from Sleepy Mimo, episode {ep}: {t}. 🌙\n"
            "Mimo and his friends talk, play and get ready for bed. Watch the full episode on the channel, with songs and lullabies! 💤\n"
            "#shorts #bedtimestory #kids #lullaby")
    tags = ["sleepy mimo", "bedtime story", "story for kids", "kids cartoon", "shorts", "lullaby", t.lower()] + list(extra_tags)
    return dict(title=title, description=desc, tags=tags)
