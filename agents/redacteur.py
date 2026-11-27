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


def tiktok_caption(story, part, parts):
    """Légende TikTok (en anglais) : accroche courte + mots-clés. Prête à copier-coller."""
    t = story["title"]
    pt = f" (part {part}/{parts})" if parts > 1 else ""
    nxt = " Follow for the next part! 🌙" if part < parts else " Full episode on YouTube: Sleepy Mimo 🌙"
    return (f"{t}{pt} 🐻 Cozy animal bedtime story for kids.{nxt} "
            "#bedtimestory #bedtimestoriesforkids #kidsstories #toddlers #storytime #lullaby #animalstories #sleepymimo")


EPISODE_TITLES = [
    "Sleepy Mimo Episode {ep}: {story} 🌙 Bedtime Story with Songs for Kids",
    "{story} ✨ Sleepy Mimo Episode {ep} | Story, Songs & Lullabies",
    "Sleepy Mimo Ep. {ep} 😴 {story} | Bedtime Adventure & Nursery Rhymes",
    "{story} 🌟 Episode {ep} | Sleepy Mimo Bedtime Story & Sing-Along",
]


# Mots-clés choisis avec vidIQ (nov. 2026) : "bedtime stories for toddlers" ≈44 000 recherches/mois (+81 %),
# "calming bedtime stories for kids with relaxing music" ≈5 900/mois et peu concurrencé ; "animal bedtime stories" < 750.
S2_TITLES = [
    "{story} 🌙 Calming Bedtime Stories for Toddlers | Sleepy Mimo Ep. {ep}",
    "{story} ✨ Calming Bedtime Story for Kids | Wild Nights Ep. {ep}",
    "{story} 🦉 Bedtime Stories for Kids with Relaxing Music | Sleepy Mimo {ep}",
    # Titre en question (hook) : ×2,5 de vues/heure après ce type de changement chez une petite chaîne d'ours (vidIQ).
    "Can Mimo Fall Asleep? {story} 🌙 Calming Bedtime Story | Ep. {ep}",
]


def episode_meta(rng, ep, number, res, used_titles, extra_tags=()):
    if ep.get("style") == "s2":
        return _episode_meta_s2(rng, ep, number, res, used_titles, extra_tags)
    title = None
    for i in rng.permutation(len(EPISODE_TITLES)):
        cand = EPISODE_TITLES[i].format(ep=number, story=ep["title"])
        if cand not in used_titles and len(cand) <= 100:
            title = cand; break
    title = title or f"Sleepy Mimo Episode {number}: {ep['title']} (#{len(used_titles) + 1})"
    songs = [c["song"]["name"] for c in ep["chapters"] if c.get("song")]
    chapters = "\n".join(f"{fmt(t)} {label}" for t, label in res["chapters"])
    cast = sorted({c for ch in ep["chapters"] for sh in ch["story"] for (c, *_r) in sh["cast"]})
    from .personnages import NAMES
    names = ", ".join(NAMES[c] for c in cast if c in NAMES)
    desc = (f"📺 Sleepy Mimo, episode {number}: {ep['title']}\n\n"
            f"Join Mimo the little bear and his friends ({names}) in a cozy bedtime adventure! "
            f"The story goes on all the way through the video, with songs sung by the characters "
            f"and gentle lullabies at the end to help little ones fall asleep. 🌙\n\n"
            f"🎵 Songs: {', '.join(dict.fromkeys(songs))} — lyrics on screen, sing along!\n\n"
            "⏱️ Chapters\n" + chapters +
            "\n\n💤 A new episode of the series every day. Subscribe so you don't miss what happens next!\n\n"
            "#bedtimestory #lullaby #nurseryrhymes #kidssongs #sleepymimo")
    tags = ["sleepy mimo", "bedtime story", "bedtime stories for kids", "nursery rhymes", "kids songs", "lullabies for babies",
            "sing along", "kids cartoon", "story for kids", "baby sleep music", ep["title"].lower()] + [s.lower() for s in songs[:3]] + list(extra_tags)
    return dict(title=title, description=desc, tags=tags[:30])


def _episode_meta_s2(rng, ep, number, res, used_titles, extra_tags=()):
    title = None
    for i in rng.permutation(len(S2_TITLES)):
        cand = S2_TITLES[i].format(ep=number, story=ep["title"])
        if cand not in used_titles and len(cand) <= 100:
            title = cand; break
    title = title or f"Sleepy Mimo Wild Nights {number}: {ep['title']}"
    songs = [c["song"]["name"] for c in ep["chapters"] if c.get("song")]
    chapters = "\n".join(f"{fmt(t)} {label}" for t, label in res["chapters"])
    cast = sorted({c for ch in ep["chapters"] for sh in ch["story"] for (c, *_r) in sh["cast"]})
    from .personnages import NAMES, SPECIES
    names = ", ".join(f"{NAMES[c]} the {SPECIES[c]}" for c in cast if c in NAMES)
    desc = (f"📺 Sleepy Mimo: Wild Nights, episode {number}: {ep['title']}\n\n"
            f"{ep.get('blurb', 'Mimo the little bear goes on a gentle night adventure in the wild.')}\n"
            f"Friends in this episode: {names}.\n\n"
            + (f"🦉 Real animal fact: {ep['fact']}\n\n" if ep.get("fact") else "")
            + (f"🎵 Songs: {', '.join(dict.fromkeys(songs))}\n\n" if songs else "")
            + "⏱️ Chapters\n" + chapters +
            "\n\n💤 Calming bedtime stories for toddlers and kids, with relaxing music: calm, kind stories to end the day. "
            "The episode finishes with soft lullabies while everyone falls asleep.\n\n"
            "#bedtimestories #bedtimestoriesforkids #animalsforkids #sleepymimo #lullaby")
    tags = ["sleepy mimo", "wild nights", "bedtime stories for toddlers", "bedtime stories for kids", "calming bedtime stories",
            "calming bedtime stories for kids with relaxing music", "kids bedtime stories", "animal stories for kids", "nature for kids",
            "lullabies for babies", "kids cartoon", "story for kids", ep["title"].lower()] + [s.lower() for s in songs[:3]] + list(extra_tags)
    return dict(title=title, description=desc, tags=tags[:30])
