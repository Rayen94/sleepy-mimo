"""Agent 14 — Parolier : paroles des comptines traditionnelles (domaine public), découpées en syllabes
calées sur les notes, et sous-titres karaoké (format ASS) incrustés dans la vidéo.
Chaque ligne : (texte affiché, syllabes chantées). Le nombre de syllabes = le nombre de notes."""

LYRICS = {
    "Twinkle Twinkle Little Star": [
        ("Twin-kle, twin-kle, lit-tle star,", "twin kul twin kul lit tul star"),
        ("How I won-der what you are!", "how eye wun der what you are"),
        ("Up a-bove the world so high,", "up uh buv the world so high"),
        ("Like a dia-mond in the sky.", "like uh die mund in the sky"),
        ("Twin-kle, twin-kle, lit-tle star,", "twin kul twin kul lit tul star"),
        ("How I won-der what you are!", "how eye wun der what you are"),
    ],
    "Row Row Row Your Boat": [
        ("Row, row, row your boat,", "row row row your boat"),
        ("Gent-ly down the stream.", "jent lee down the stream"),
        ("Mer-ri-ly, mer-ri-ly, mer-ri-ly, mer-ri-ly,", "mer ree lee mer ree lee mer ree lee mer ree lee"),
        ("Life is but a dream.", "life is but uh dream"),
    ],
    "Are You Sleeping (Frère Jacques)": [
        ("Are you sleep-ing, are you sleep-ing,", "are you sleep ing are you sleep ing"),
        ("Bro-ther John? Bro-ther John?", "bruh ther jon bruh ther jon"),
        ("Morn-ing bells are ring-ing, morn-ing bells are ring-ing,", "morn ing bells are ring ing morn ing bells are ring ing"),
        ("Ding, dang, dong. Ding, dang, dong.", "ding dang dong ding dang dong"),
    ],
    "Mary Had a Little Lamb": [
        ("Ma-ry had a lit-tle lamb,", "mair ee had uh lit tul lamb"),
        ("lit-tle lamb, lit-tle lamb.", "lit tul lamb lit tul lamb"),
        ("Ma-ry had a lit-tle lamb,", "mair ee had uh lit tul lamb"),
        ("its fleece was white as snow.", "its fleece was white as snow"),
    ],
    "London Bridge": [
        ("Lon-don Bridge is fall-ing down,", "lun dun bridge is fall ing down"),
        ("fall-ing down, fall-ing down.", "fall ing down fall ing down"),
        ("Lon-don Bridge is fall-ing down,", "lun dun bridge is fall ing down"),
        ("my fair la-dy.", "my fair lay dee"),
    ],
}


def display_syllables(text):
    out = []
    for word in text.split(" "):
        parts = word.split("-")
        for i, p in enumerate(parts):
            out.append(p + ("-" if i < len(parts) - 1 else " "))
    out[-1] = out[-1].rstrip()
    return out


def lines(song):
    """Liste de lignes ; chaque ligne = liste de (syllabe affichée, syllabe chantée)."""
    res = []
    for disp, sung in LYRICS.get(song, []):
        d, s = display_syllables(disp), sung.split()
        assert len(d) == len(s), (song, disp, len(d), len(s))
        res.append(list(zip(d, s)))
    return res


def check(song, n_notes):
    return sum(len(l) for l in lines(song)) == n_notes


# ---------------------------------------------------------------- Sous-titres ASS
HEADER = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Karaoke,Fredoka,76,&H005CD3FF,&H00FFFFFF,&H00301020,&H64000000,-1,0,0,0,100,100,1,0,1,5,3,2,80,80,70,1
Style: Title,Fredoka,64,&H00C9F4FF,&H00FFFFFF,&H00301020,&H64000000,-1,0,0,0,100,100,1,0,1,4,3,8,80,80,60,1
Style: Story,Fredoka,60,&H00FFFFFF,&H00FFFFFF,&H00402030,&H78000000,-1,0,0,0,100,100,0.5,0,1,4,2,2,120,120,55,1
Style: StoryTitle,Fredoka,96,&H00A0E9FF,&H00FFFFFF,&H00602040,&H78000000,-1,0,0,0,100,100,1,0,1,6,4,8,80,80,120,1
Style: Brand,Fredoka,150,&H00C9F4FF,&H00FFFFFF,&H00301020,&H64000000,-1,0,0,0,100,100,2,0,1,6,4,5,80,80,0,1
Style: BrandSub,Fredoka,58,&H005CD3FF,&H00FFFFFF,&H00301020,&H64000000,-1,0,0,0,100,100,1,0,1,4,3,5,80,80,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def ts(s):
    s = max(0.0, s)
    h = int(s // 3600); m = int(s % 3600 // 60); sec = s % 60
    return f"{h}:{m:02d}:{sec:05.2f}"


def ass_line(start, end, syllables, times):
    """syllables : textes affichés ; times : instants de début de chaque syllabe (absolus)."""
    lead = max(0, int(round((times[0] - start) * 100)))
    parts = [f"{{\\fad(250,250)}}{{\\k{lead}}}"]
    for i, syl in enumerate(syllables):
        nxt = times[i + 1] if i + 1 < len(times) else times[i] + 0.6
        cs = max(1, int(round((nxt - times[i]) * 100)))
        parts.append(f"{{\\kf{cs}}}{syl}")
    return f"Dialogue: 0,{ts(start)},{ts(end)},Karaoke,,0,0,0,,{''.join(parts)}"


def ass_title(start, text, dur=5.0):
    return f"Dialogue: 1,{ts(start)},{ts(start + dur)},Title,,0,0,0,,{{\\fad(600,600)}}{text}"


def ass_brand(start, dur, name, sub):
    return (f"Dialogue: 2,{ts(start + 0.3)},{ts(start + dur)},Brand,,0,0,0,,{{\\fad(500,500)\\pos(960,300)\\t(0,600,\\fscx108\\fscy108)\\t(600,1000,\\fscx100\\fscy100)}}{name}\n"
            f"Dialogue: 2,{ts(start + 1.0)},{ts(start + dur)},BrandSub,,0,0,0,,{{\\fad(500,500)\\pos(960,420)}}{sub}")


SPEAKER_COLORS = {"mimo": "&H0070B0E8&", "owl": "&H00DB7B9A&", "bunny": "&H00C9A7F7&", "star": "&H005AD9FF&", "lamb": "&H00F2D0C9&", "kitten": "&H005AA6F2&", "duck": "&H0066E0FF&", "fox": "&H002A7AF0&"}


def ass_dialogue(start, end, who, text, name):
    if who == "narrator":
        body = "{\\i1}" + text
    else:
        body = "{\\c" + SPEAKER_COLORS.get(who, "&H00FFFFFF&") + "}" + name + " : {\\c&H00FFFFFF&}" + text
    return f"Dialogue: 0,{ts(start)},{ts(end)},Story,,0,0,0,,{{\\fad(150,150)}}{body}"


def ass_story_title(start, text, dur=4.0):
    return f"Dialogue: 3,{ts(start)},{ts(start + dur)},StoryTitle,,0,0,0,,{{\\fad(500,500)\\t(0,500,\\fscx105\\fscy105)\\t(500,900,\\fscx100\\fscy100)}}{text}"
