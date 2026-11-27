"""Agent 20 — Scénariste + metteur en scène : une petite histoire différente à chaque vidéo (anglais),
avec des personnages qui parlent, puis la comptine qui va avec l'histoire.
Le scénario est tiré au sort parmi plusieurs modèles, avec des variantes (ami, lieu, répliques)."""
import math, random
import numpy as np
from . import personnages as C, decors as D, comediens as V, illustrateur as I, style as STYLE

SR = 44100
FPS = 30
FRIEND_HELLO = {"owl": ["Hoo hoo! Hello, Mimo!", "Hoo hoo! Good evening, Mimo!"],
                "bunny": ["Hop hop! Hi, Mimo!", "Hello Mimo! Hop hop!"],
                "lamb": ["Baa! Hello, Mimo!", "Baa baa! Hi there, Mimo!"]}


def _pick(r, xs):
    return xs[r.randrange(len(xs))]


# ---------------------------------------------------------------- Scénarios
def story_lost_star(r):
    f = _pick(r, ["owl", "bunny"]); F = C.NAMES[f]
    place = _pick(r, ["meadow", "forest"]); P = D.PLACE_NAMES[place]
    return dict(id="lost_star", title="Mimo and the Lost Star", song="Twinkle Twinkle Little Star", shots=[
        dict(decor="bedroom", cast=[("mimo", 640, 640, 1)], lines=[
            ("narrator", "Once upon a time, a little bear named Mimo was getting ready for bed."),
            ("mimo", _pick(r, ["I brushed my teeth, and I have my sleepy hat!", "Pajamas on, teeth brushed, sleepy hat on!"])),
            ("mimo", _pick(r, ["Good night, moon! Good night, stars!", "Time for bed! Good night, sky!"]))]),
        dict(decor="bedroom", cast=[("mimo", 640, 860, 1)], lines=[
            ("narrator", "But when Mimo looked out of the window, something was not right."),
            ("mimo", "One, two, three, four... Oh no! One little star is missing!"),
            ("mimo", "I have to find it. A star cannot sleep all alone!")]),
        dict(decor=place, cast=[("mimo", -150, 470, 1), (f, 820, 820, -1)], lines=[
            ("narrator", f"So Mimo tiptoed outside, all the way to {P}. There, he met {F} the {C.SPECIES[f]}."),
            (f, _pick(r, FRIEND_HELLO[f])),
            ("mimo", f"{F}, have you seen a little star? It fell out of the sky!"),
            (f, _pick(r, ["Yes! I saw a tiny light fall behind the hill.", "I saw something shiny fly over the hill!"])),
            ("mimo", "Will you help me find it?"),
            (f, "Of course! Friends always help each other.")]),
        dict(decor="clouds", cast=[("mimo", -150, 460, 1), (f, -330, 760, 1)], lines=[
            ("narrator", "They looked behind the soft clouds."),
            (f, "Little star! Are you here?"),
            ("mimo", "Not here. Only fluffy clouds and a rainbow."),
            (f, "Let's look on the lantern hill!")]),
        dict(decor="night", cast=[("mimo", -150, 470, 1), (f, -330, 230, 1), ("star", 960, 960, -1)], lines=[
            ("narrator", "They walked and walked, until they heard a tiny, sleepy voice."),
            ("star", _pick(r, ["Here I am! I fell asleep and slipped out of the sky.", "Hello! I was so sleepy, I fell down from the sky."])),
            ("mimo", "We found you! Are you okay, little star?"),
            ("star", "I am okay. But I am too sleepy to fly home."),
            (f, "I know! A song will give you sparkles!"),
            ("mimo", "Yes! Let's sing you back home. Ready? One, two, three!")]),
    ])


def story_river(r):
    f = _pick(r, ["owl", "bunny"]); F = C.NAMES[f]
    return dict(id="river", title="Mimo's Boat Trip", song="Row Row Row Your Boat", shots=[
        dict(decor="meadow", cast=[("mimo", -150, 450, 1), (f, 820, 820, -1)], lines=[
            ("narrator", "One golden evening, Mimo was picking flowers in the meadow."),
            (f, _pick(r, FRIEND_HELLO[f])),
            ("mimo", f"Hello, {F}! Look, I made a flower crown!"),
            (f, "It is so pretty! Where are you going with it?"),
            ("mimo", "To the sparkly river! Do you want to come on a boat trip?"),
            (f, _pick(r, ["Oh yes! I love boats!", "Yes please! Let's go!"]))]),
        dict(decor="forest", cast=[("mimo", -150, 520, 1), (f, -330, 340, 1)], lines=[
            ("narrator", "They walked through the rainbow forest, past the red mushrooms."),
            (f, "Hop, skip, and jump! We are almost there!"),
            ("mimo", "I can hear the water. Splish, splash!")]),
        dict(decor="river", boat=True, cast=[("mimo", 560, 560, 1), (f, 720, 720, -1)], lines=[
            ("narrator", "Their little boat was waiting for them on the sparkly river."),
            ("mimo", "Everybody in! Now we row gently, gently."),
            (f, "Look, Mimo! The fish are dancing!"),
            ("mimo", "And the water lilies are waving hello!"),
            (f, "This is the best boat trip ever!"),
            ("mimo", "When we row, we sing our rowing song. Sing with us!")]),
    ])


def story_sheep(r):
    f = _pick(r, ["bunny", "owl"]); F = C.NAMES[f]
    return dict(id="sheep", title=f"{F} Can't Sleep", song="Mary Had a Little Lamb", shots=[
        dict(decor="bedroom", cast=[("mimo", 420, 420, 1), (f, 1450, 820, -1)], lines=[
            ("narrator", "It was bedtime, and Mimo was all ready to sleep."),
            (f, "Mimo? Mimo? I can't fall asleep!"),
            ("mimo", f"Oh, {F}! Why not?"),
            (f, "My eyes are wide open, and my feet want to dance!"),
            ("mimo", "I know a trick. Let's count sheep together!"),
            (f, "Okay! One sheep, two sheep, three sheep...")]),
        dict(decor=_pick(r, ["meadow", "night"]), cast=[("mimo", 330, 330, 1), (f, 540, 540, 1), ("lamb", 1450, 920, -1)], lines=[
            ("narrator", "And then, a real little lamb came hopping by!"),
            ("lamb", _pick(r, FRIEND_HELLO["lamb"])),
            ("lamb", "My name is Wooly. I heard someone counting sheep!"),
            (f, "That was me! I can't sleep."),
            ("lamb", "Don't worry. I know a sleepy song about a little lamb."),
            ("mimo", "Yay! Let's sing it together, very softly.")]),
    ])


def story_bell(r):
    f = _pick(r, ["bunny", "lamb"]); F = C.NAMES[f]
    return dict(id="bell", title="The Bedtime Bell", song="Are You Sleeping (Frère Jacques)", shots=[
        dict(decor="forest", cast=[("owl", 640, 640, 1)], lines=[
            ("narrator", "In the rainbow forest lives Luna, the owl who keeps the bedtime bell."),
            ("owl", "Hoo hoo! Every night, I ring the bedtime bell."),
            ("owl", "Ding, dang, dong! It means: time to sleep, everyone!")]),
        dict(decor="night", cast=[("owl", -200, 380, 1), (f, 900, 900, -1)], lines=[
            (f, "Luna! Luna! Where is Mimo? We wanted to play!"),
            ("owl", "Hoo hoo! I think Mimo is already in bed."),
            (f, "Already? Let's go and see!")]),
        dict(decor="forest", cast=[("owl", -200, 420, 1), (f, -380, 700, 1)], lines=[
            ("narrator", "They tiptoed through the rainbow forest, past the sleepy mushrooms."),
            (f, "Luna, why do owls stay awake at night?"),
            ("owl", "Because someone has to watch over the stars, little one."),
            (f, "Wow! You are like a night-time guardian!"),
            ("owl", "Hoo hoo! That's right. Now, shhh, we are almost there.")]),
        dict(decor="bedroom", sleeping=True, cast=[("owl", 1450, 760, -1), (f, 1600, 960, -1)], lines=[
            ("narrator", "They peeked into Mimo's room. Mimo was snoring softly, hugging his pillow."),
            (f, "Shhh. He is fast asleep."),
            ("owl", "He must be dreaming of honey and stars."),
            (f, "Can we sing him a little song? Very, very softly?"),
            ("owl", "Yes. Our bell song. Ready?"),
            (f, "Are you sleeping, Mimo?")]),
    ])


def story_bridge(r):
    f = _pick(r, ["bunny", "owl"]); F = C.NAMES[f]
    return dict(id="bridge", title="The Lantern Bridge", song="London Bridge", shots=[
        dict(decor="bedroom", cast=[("mimo", 640, 640, 1)], lines=[
            ("narrator", "Mimo had heard about a magic bridge, where lanterns glow every night."),
            ("mimo", "I want to see the lantern bridge before I sleep!")]),
        dict(decor="meadow", cast=[("mimo", -150, 450, 1), (f, 820, 820, -1)], lines=[
            (f, _pick(r, FRIEND_HELLO[f])),
            ("mimo", f"{F}, do you know the way to the lantern bridge?"),
            (f, "Yes! Follow the river, then turn at the big rainbow."),
            ("mimo", "Let's go together!")]),
        dict(decor="night", cast=[("mimo", -150, 470, 1), (f, -330, 260, 1)], lines=[
            ("narrator", "When the sky turned purple, the lanterns began to glow."),
            (f, "Look, Mimo! Pink, yellow, blue and purple lights!"),
            ("mimo", "It's so pretty! The bridge looks like it's dancing."),
            (f, "People say the bridge loves a song. Shall we sing it one?"),
            ("mimo", "Yes! Let's sing the bridge song!")]),
    ])


def story_lost_lamb(r):
    f = _pick(r, ["owl", "bunny"]); F = C.NAMES[f]
    return dict(id="lost_lamb", title="Where Is Wooly?", song="Mary Had a Little Lamb", shots=[
        dict(decor="meadow", cast=[("lamb", 640, 640, 1)], lines=[
            ("narrator", "Wooly the little lamb loved to chase butterflies."),
            ("lamb", "Come back, butterfly! I want to play!")]),
        dict(decor="forest", cast=[("lamb", -150, 640, 1)], lines=[
            ("narrator", "He chased them so far that he ended up deep in the rainbow forest."),
            ("lamb", "Oh no. Where am I? I can't find my way home!")]),
        dict(decor="meadow", cast=[("mimo", -150, 470, 1), (f, 820, 820, -1)], lines=[
            ("narrator", "Back in the meadow, Mimo noticed that someone was missing."),
            ("mimo", f"{F}, have you seen Wooly? He's not with the other sheep!"),
            (f, "Oh no! I saw him running after a butterfly, toward the forest."),
            ("mimo", "The forest is big. Wooly might be lost!"),
            (f, "Let's go! We can call his name together."),
            ("mimo", "Wooly! Woooly! Where are you?")]),
        dict(decor="forest", cast=[("lamb", 640, 640, -1), ("mimo", 1450, 900, -1), (f, 1600, 1080, -1)], lines=[
            ("mimo", "Wooly! There you are! Everybody was looking for you."),
            (f, "Don't be scared, little lamb. We will take you home."),
            ("lamb", "Thank you, friends! I was a little scared."),
            ("mimo", "It's okay to be scared. Friends are always here for you."),
            (f, "Next time, let's chase butterflies together!"),
            ("lamb", "Yes! Together is better."),
            ("mimo", "Let's walk home together, and sing your favorite song!")]),
    ])


def story_cloud_picnic(r):
    f = _pick(r, ["bunny", "lamb", "owl"]); F = C.NAMES[f]
    return dict(id="cloud_picnic", title="A Picnic on the Clouds", song="Twinkle Twinkle Little Star", shots=[
        dict(decor="bedroom", cast=[("mimo", 640, 640, 1)], lines=[
            ("narrator", "One night, Mimo found a little note on his pillow."),
            ("mimo", "It says: Come to a picnic on the clouds! Love, Twinkle.")]),
        dict(decor="night", cast=[("mimo", -150, 470, 1), (f, 820, 820, -1)], lines=[
            ("mimo", f"{F}! Look, Twinkle invited us to a picnic on the clouds!"),
            (f, "On the clouds? But how do we get up there?"),
            ("narrator", "Just then, a soft rainbow slid down from the sky, like a slide."),
            ("mimo", "A rainbow slide! Hold my paw, and let's climb up!"),
            (f, "Wheee! This is fun!")]),
        dict(decor="clouds", cast=[("mimo", -150, 420, 1), (f, -330, 250, 1), ("star", 950, 950, -1)], lines=[
            ("star", "Welcome to my cloud picnic! I made moon cookies."),
            (f, "Moon cookies? Yummy!"),
            ("mimo", "Thank you, Twinkle! The clouds are so soft and bouncy."),
            ("star", "And I brought starberry juice. It sparkles!"),
            (f, "Mmm! It tastes like sunshine and sleepy dreams."),
            ("star", "After the picnic, will you sing my favorite song?"),
            ("mimo", "Of course! Everybody, sing with us!")]),
    ])


def story_owl_lullaby(r):
    f = _pick(r, ["bunny", "lamb"]); F = C.NAMES[f]
    return dict(id="owl_lullaby", title="Luna's Secret Lullaby", song="Brahms' Lullaby", shots=[
        dict(decor="bedroom", cast=[("mimo", 640, 640, 1)], lines=[
            ("narrator", "It was a windy night, and Mimo could not fall asleep."),
            ("mimo", "The wind is so loud. Whoosh, whoosh!"),
            ("mimo", "Maybe Luna knows a way to help me sleep.")]),
        dict(decor="forest", cast=[("mimo", -150, 470, 1), (f, 820, 820, -1)], lines=[
            (f, _pick(r, FRIEND_HELLO[f])),
            (f, "You can't sleep either? The wind is too noisy!"),
            ("mimo", "Let's ask Luna. She is the wisest owl in the forest."),
            (f, "Good idea! She always knows what to do.")]),
        dict(decor="night", cast=[("mimo", 360, 360, 1), (f, 560, 560, 1), ("owl", 1450, 900, -1)], lines=[
            ("narrator", "Every night, Mimo and his friends sat on the lantern hill."),
            ("owl", "Hoo hoo! Tonight, I will share my secret lullaby."),
            (f, "A secret lullaby? I love secrets!"),
            ("owl", "It's very old, and very gentle. Close your eyes and listen."),
            ("mimo", "Goodnight, Luna. Goodnight, everyone.")]),
    ])


STORIES = [story_lost_star, story_river, story_sheep, story_bell, story_bridge, story_lost_lamb, story_cloud_picnic, story_owl_lullaby]


def pick_story(rng, recent_ids=()):
    r = random.Random(int(rng.integers(1e9)))
    choices = [s for s in STORIES if s(random.Random(0))["id"] not in recent_ids] or STORIES
    return choices[r.randrange(len(choices))](r)


# ---------------------------------------------------------------- Son + minutage
def build(story, rng, music_spec=None):
    """Prépare voix, minutage des plans et musique de fond. Renvoie (audio stéréo, plans minutés, sous-titres)."""
    from . import compositeur as M
    shots, t = [], 0.0
    clips = []
    for sh in story["shots"]:
        st = t; lines = []
        t += 0.7
        for who, text in sh["lines"]:
            y, mouth = V.speak(who, text)
            lines.append(dict(who=who, text=text, start=t - st, dur=len(y) / SR, mouth=mouth))
            clips.append((t, y))
            t += len(y) / SR + 0.75
        t += 0.8
        shots.append(dict(sh, start=st, dur=t - st, lines_t=lines))
    total = math.ceil(t * FPS) / FPS
    n = int(total * SR)
    voice = np.zeros(n)
    for t0, y in clips:
        i = int(t0 * SR); voice[i:i + len(y)] += y[:n - i]
    # musique de fond douce (boîte à musique) + ambiance
    bg = np.zeros((n, 2))
    if music_spec is not None:
        bpm, mel, ch = music_spec
        m = M.reverb(M.render(bpm * 0.9, mel, ch, "box", 12, 0, total + 1, seed=7))[:n]
        bg[:len(m)] += m * 0.22
    voice_st = M.reverb(voice) * 0.25 + np.stack([voice, voice], 1) * 0.75
    audio = voice_st + bg
    k = int(SR * 1.0); audio[:k] *= np.linspace(0, 1, k)[:, None]
    subs = [(sh["start"] + ln["start"], sh["start"] + ln["start"] + ln["dur"] + 0.3, ln["who"], ln["text"])
            for sh in shots for ln in sh["lines_t"]]
    return audio, shots, subs, total


# ---------------------------------------------------------------- Image
def _boat_front(t):
    bob = 4 * math.sin(2 * math.pi * t * 0.5)
    return (f'<g transform="translate(0 {bob:.1f})"><path d="M360 560 L920 560 Q880 660 640 660 Q400 660 360 560Z" fill="#E8896B"/>'
            '<path d="M368 580 L912 580" stroke="#F6C2A8" stroke-width="12"/>'
            + "".join(f'<circle cx="{x}" cy="620" r="12" fill="#F6C2A8"/>' for x in (480, 640, 800)) + "</g>")


CHEER = ("Hooray", "hooray", "Yay", "You did it", "I did it", "I'm swimming", "We found you", "Wow")
ARMS = ("mimo", "bunny", "kitten", "fox")


def actors(sh, ts):
    """Où est chaque personnage, et ce qu'il fait (marcher, parler, regarder, sauter...)."""
    dur = sh["dur"]
    speaking = None
    for ln in sh["lines_t"]:
        if ln["start"] <= ts < ln["start"] + ln["dur"]:
            speaking = ln
    move_t = min(3.0, dur * 0.4)
    acts = []
    for idx, (who, x0, x1, facing) in enumerate(sh["cast"]):
        u = I.smooth(min(1.0, ts / move_t)) if x0 != x1 else 1.0
        x = x0 + (x1 - x0) * u
        moving = x0 != x1 and ts < move_t
        s = 0.95 if who != "star" else 0.8
        y = (D.GROUND if sh.get("boat") else D.ground(sh["decor"])) - 134 * s
        if who == "fish":
            s, y = 1.25, 470 + 8 * math.sin(2 * math.pi * ts / 2.2)
        if who == "star":
            y = 330 + 14 * math.sin(2 * math.pi * ts / 3)
        if who == "bat":
            y = 330 + 18 * math.sin(2 * math.pi * ts / 2.4)
        acts.append(dict(who=who, x=x, y=y, s=s, x0=x0, x1=x1, facing=facing, moving=moving, idx=idx))
    sp = next((a for a in acts if speaking and a["who"] == speaking["who"]), None)
    for a in acts:
        who, idx = a["who"], a["idx"]
        a["walk"] = (abs(a["x"] - a["x0"]) / 140.0) % 1.0 if a["moving"] else 0.0
        a["mouth"], a["wave"], a["jump"], a["tilt"], a["look"] = 0.0, 0.0, 0.0, 0.0, 0.0
        a["blink"] = ((ts + idx * 1.7) % 3.9) < 0.14
        if not a["moving"] and who not in ("star", "fish", "bat"):
            a["y"] += 2 * math.sin(2 * math.pi * ts / 2.5 + idx)
        f = a["facing"] if not a["moving"] else (1 if a["x1"] > a["x0"] else -1)
        a["f"] = f
        if speaking:
            dt = ts - speaking["start"]
            if sp is a:
                i = int(dt * 100)
                a["mouth"] = float(speaking["mouth"][min(i, len(speaking["mouth"]) - 1)]) if i >= 0 else 0.0
                if "!" in speaking["text"] and dt < 0.45 and who not in ("fish",):
                    a["jump"] = 22 * math.sin(math.pi * dt / 0.45)
                if "?" in speaking["text"]:
                    a["tilt"] = 6 * math.sin(math.pi * min(1.0, dt / 0.6))
                if who in ARMS or STYLE.s2():
                    hello = any(w in speaking["text"] for w in ("Hello", "Hi,", "Hi ", "Hey"))
                    a["wave"] = math.sin(math.pi * min(1, dt / 1.4)) if (hello and dt < 1.4) else 0.25 + 0.2 * math.sin(2 * math.pi * 1.3 * ts)
            elif sp is not None and who != "fish":
                a["look"] = (1 if sp["x"] > a["x"] else -1) * f
            if any(w in speaking["text"] for w in CHEER) and dt < 2.0 and who not in ("fish", "star"):
                a["jump"] = max(a["jump"], 18 * abs(math.sin(2 * math.pi * 2 * dt + idx)))
    return acts, speaking


def shot_inner(sh, ts, seed, cam=None):
    t_dec = (ts / 16.0) % 1.0
    parts = [D.DECORS[sh["decor"]](t_dec, seed, cam) if sh["decor"] in D._D2.DECORS else D.DECORS[sh["decor"]](t_dec, seed)]
    if sh.get("sleeping"):
        parts.append(f'<g transform="translate(250 455) scale(0.85)">{I.bear(("#8FB8E8", "#B9D4F3"), ts / 16.0)}{I.zzz(ts / 16.0)}</g>')
    acts, _ = actors(sh, ts)
    for a in acts:
        body = C.draw(a["who"], 0, 0, a["s"], mouth=a["mouth"], blink=a["blink"], walk=a["walk"], wave=a["wave"], facing=a["f"], look=a["look"], t=ts, pose=sh.get("pose"))
        parts.append(f'<g transform="translate({a["x"]:.1f} {a["y"] - a["jump"]:.1f}) rotate({a["tilt"] * a["f"]:.2f} 0 {134 * a["s"]:.0f})">{body}</g>')
    if sh.get("boat"):
        parts.append(_boat_front(ts))
    if any(c[0] == "fish" for c in sh["cast"]):
        parts.append(D.water_front(ts / 4.0))
    if sh["decor"] in D._D2.FRONTS:
        parts.append(D.foreground(sh["decor"], t_dec, cam))
    else:
        dx = 0.0 if cam is None else (cam[0] - 640) * -0.25
        parts.append(f'<g transform="translate({dx:.1f} 0)">{D.foreground(sh["decor"], t_dec)}</g>')
    return "".join(parts)


def _clamp_cam(cx, cy, z):
    hw, hh = 640 / z, 360 / z
    return min(max(cx, hw), 1280 - hw), min(max(cy, hh), 720 - hh), z


def _cam_for(sh, ts, li, acts):
    """Cadrage d'une réplique : plan large, gros plan sur celui qui parle, ou plan à deux."""
    if li is None:
        return (640.0, 360.0, 1.0)
    ln = sh["lines_t"][li]
    sp = next((a for a in acts if a["who"] == ln["who"]), None)
    if sp is None or sp["moving"]:
        return (640.0, 360.0, 1.0) if len(acts) != 1 else _clamp_cam(acts[0]["x"], acts[0]["y"] + 40, 1.2)
    v = li % 3
    if v == 0 or len(acts) == 1:
        return _clamp_cam(sp["x"], sp["y"] + 25, 1.55)
    if v == 1:
        others = [a for a in acts if a is not sp]
        nb = min(others, key=lambda a: abs(a["x"] - sp["x"]))
        return _clamp_cam((sp["x"] + nb["x"]) / 2, (sp["y"] + nb["y"]) / 2 + 60, 1.22)
    return _clamp_cam(sp["x"], sp["y"] + 45, 1.32)


def camera(sh, ts):
    acts, _ = actors(sh, ts)
    lis = [i for i, ln in enumerate(sh["lines_t"]) if ln["start"] <= ts]
    li = lis[-1] if lis else None
    cur = _cam_for(sh, ts, li, acts)
    if li is None:
        return cur
    prev = _cam_for(sh, ts, li - 1 if li > 0 else None, acts)
    u = I.smooth((ts - sh["lines_t"][li]["start"]) / 0.6)
    return tuple(p + (c - p) * u for p, c in zip(prev, cur))


VIGNETTE = ('<defs><radialGradient id="vig_story" cx="0.5" cy="0.45" r="0.8"><stop offset="0.55" stop-color="#000" stop-opacity="0"/>'
            '<stop offset="1" stop-color="#1A1030" stop-opacity="0.38"/></radialGradient></defs>')


def shot_body(sh, ts, W, H, seed):
    """Image d'un plan à l'instant ts (secondes depuis le début du plan), en SVG (sans balise <svg>)."""
    k = W / 1280
    cx, cy, z = camera(sh, ts)
    z *= 1.0 + 0.02 * ts / max(sh["dur"], 1)
    return (VIGNETTE + f'<g transform="scale({k:.4f}) translate(640 360) scale({z:.4f}) translate({-cx:.1f} {-cy:.1f})">'
            f'{shot_inner(sh, ts, seed, (cx, cy, z))}</g>'
            f'<rect width="{W}" height="{H}" fill="url(#vig_story)"/>'
            + I.text(W - 30 * k, 50 * k, "Sleepy Mimo", int(26 * k), "#FFFFFF", 600, "end", False, 0.7))


def frames(shots, total, W, H, seed, next_body=None, n_fade_out=45):
    """Toutes les images de l'histoire, avec fondus entre les décors et fondu final vers la scène suivante."""
    n = int(round(total * FPS))
    prev_last, si = None, 0
    fade_in = 12
    for kf in range(n):
        ts = kf / FPS
        while si + 1 < len(shots) and ts >= shots[si + 1]["start"]:
            si += 1
        sh = shots[si]
        local = ts - sh["start"]
        body = shot_body(sh, local, W, H, seed + si)
        if si > 0 and local < fade_in / FPS:
            prev = shots[si - 1]
            pb = shot_body(prev, prev["dur"] - 1 / FPS, W, H, seed + si - 1)
            o = I.smooth(local * FPS / fade_in)
            body = f"<g>{pb}</g><g opacity=\"{o:.3f}\">{body}</g>"
        if next_body and kf >= n - n_fade_out:
            o = I.smooth((kf - (n - n_fade_out) + 0.5) / n_fade_out)
            body += f'<g opacity="{o:.3f}">{next_body(n - kf)}</g>'
        yield I.svg(W, H, body)


def outro(story, rng):
    """Générique de fin : Mimo et son ami disent au revoir et donnent rendez-vous au prochain épisode."""
    friends = [c for sh in story["shots"] for (c, *_rest) in sh["cast"] if c not in ("mimo", "star")]
    f = friends[0] if friends else "owl"
    sh = dict(decor="night", cast=[("mimo", 520, 520, 1), (f, 780, 780, -1)], lines=[
        ("mimo", "Goodnight, friends! Thank you for watching."),
        (f, "See you in the next episode! Sweet dreams!")])
    return build(dict(shots=[sh]), rng, None)


# ---------------------------------------------------------------- Shorts tirés de l'épisode
def _wrap(text, n=24):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > n and cur:
            lines.append(cur); cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        lines.append(cur)
    return lines


COLORS = {"mimo": "#FFC36B", "owl": "#C9A7FF", "bunny": "#FFB3D1", "star": "#FFE37A", "lamb": "#F2E6FF", "kitten": "#FFB27A", "duck": "#FFE066", "fox": "#FF9A5A", "fish": "#5EC8F2", "hedgehog": "#D9B98E", "otter": "#C99A6E", "fawn": "#F0B56E", "beaver": "#C48A5A", "bat": "#C7A8E8", "turtle": "#9ED08A", "narrator": "#FFFFFF"}


def short_parts(shots, total, n, min_len=25.0, max_len=58.0):
    """Découpe l'histoire en n parties consécutives (entre deux répliques), de 25 à 58 s si possible."""
    n = max(1, min(n, int(total // min_len) or 1))
    bounds = sorted({0.0, total} | {sh["start"] + ln["start"] - 0.4 for sh in shots for ln in sh["lines_t"]})
    parts, start = [], 0.0
    for k in range(n):
        target = total * (k + 1) / n
        end = total if k == n - 1 else min(bounds, key=lambda b: abs(b - target))
        end = min(end, start + max_len) if k < n - 1 else end
        if end - start > 3:
            parts.append((start, end))
        start = end
    if parts and parts[-1][1] - parts[-1][0] > max_len:
        a_, b_ = parts[-1]; parts[-1] = (a_, a_ + max_len)
    return parts


def short_frames(shots, t0, t1, seed, episode, title, part, parts, W=1080, H=1920, platform="yt"):
    dur = t1 - t0
    n = int(round(dur * FPS))
    s = H / 720
    for kf in range(n):
        ts = kf / FPS
        g = t0 + ts
        si = max(i for i, sh in enumerate(shots) if sh["start"] <= g + 1e-6)
        sh = shots[si]
        local = g - sh["start"]
        xs = [x1 for (_, _, x1, _) in sh["cast"]]
        cx = min(max(sum(xs) / len(xs), 205), 1075)
        zoom = 1.06 - 0.06 * I.smooth(ts / 1.5) + 0.03 * ts / dur
        body = [f'<g transform="translate({W/2} {H/2}) scale({zoom:.4f}) translate({-W/2} {-H/2})">'
                f'<g transform="translate({W/2} 0) scale({s:.4f}) translate({-cx:.1f} 0)">{shot_inner(sh, local, seed + si)}</g></g>']
        body.append(I.text(40, 120, "Sleepy Mimo", 44, "#FFFFFF", 600, "start", True, 0.85))
        if ts < 3.6:
            pop = I.ease_out_back(ts / 0.45) if ts < 0.45 else 1.0
            op = 1.0 if ts < 3.1 else 1 - I.smooth((ts - 3.1) / 0.5)
            sc = 0.55 + 0.45 * pop
            tl = _wrap(title, 18)
            gg = I.text(W / 2, 300, f"Episode {episode}" + (f" · Part {part}" if parts > 1 else ""), 70, "#FFE37A")
            gg += "".join(I.text(W / 2, 400 + i * 95, ln, 84, "#FFFFFF") for i, ln in enumerate(tl))
            body.append(f'<g opacity="{op:.3f}" transform="translate({W/2} 380) scale({sc:.3f}) translate({-W/2} -380)">{gg}</g>')
        for ln in sh["lines_t"]:
            if ln["start"] - 0.1 <= local < ln["start"] + ln["dur"] + 0.3:
                name = "" if ln["who"] == "narrator" else C.NAMES[ln["who"]]
                rows = _wrap(ln["text"], 24)
                y0 = 850 - (len(rows) - 1) * 39
                if name:
                    body.append(I.text(W / 2, y0 - 85, name, 60, COLORS[ln["who"]]))
                body.append("".join(I.text(W / 2, y0 + i * 78, r_, 64, "#FFFFFF") for i, r_ in enumerate(rows)))
        if ts > dur - 3.2:
            op = I.smooth((ts - (dur - 3.2)) / 0.5)
            pulse = 1 + 0.04 * math.sin(2 * math.pi * 1.2 * ts)
            last = part == parts
            l1, l2 = ("Watch the full", "episode!") if last else ("To be", "continued...")
            if platform == "tiktok":
                l1, l2 = ("Full episode on", "YouTube!") if last else ("Follow for", f"part {part + 1}!")
            body.append(f'<g opacity="{op:.3f}" transform="translate({W/2} 330) scale({pulse:.3f}) translate({-W/2} -330)">'
                        + I.text(W / 2, 300, l1, 88, "#FFFFFF") + I.text(W / 2, 400, l2, 88, "#FFE37A") + "</g>")
        yield I.svg(W, H, "".join(body))


def short_audio(audio, t0, t1):
    a, b = int(t0 * SR), int(t1 * SR)
    x = audio[a:b].copy()
    k = min(len(x) // 4, int(SR * 0.3)); x[:k] *= np.linspace(0, 1, k)[:, None]
    k = min(len(x) // 4, int(SR * 1.5)); x[-k:] *= np.linspace(1, 0, k)[:, None]
    return x
