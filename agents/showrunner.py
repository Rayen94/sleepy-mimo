"""Agent 22 — Showrunner : monte un épisode où l'histoire dure toute la vidéo.
Intro → [chapitre d'histoire → chanson chantée et dansée par les personnages] × N → berceuses (tout le monde dort) → au revoir.
Image Full HD 30 i/s, encodage final haute qualité."""
import math, os, subprocess, wave
import numpy as np
from . import (histoires as HS, personnages as PE, decors as D, illustrateur as I, monteur as M, compositeur as C,
               chanteur as S, parolier as P, animateur as A)

SR, FPS = 44100, M.FPS
W, H = 1920, 1080


# ---------------------------------------------------------------- Son
def sing_track(name, voice, transpose, rng, seed, passes=2, tempo=0.92):
    """Chanson complète : instruments + voix (2 passages chantés). Renvoie (audio, lignes karaoké relatives, bouche 100 Hz, bpm)."""
    bpm0, mel, ch = C.track_spec(("pd", name), rng)
    bpm = bpm0 * tempo
    Lsec = sum(d for _, d in mel) * 60 / bpm
    seconds = passes * Lsec - 0.01
    octave = 12 if voice in ("box", "bell") else 0
    st = C.play(bpm, mel, ch, voice, octave, transpose, seconds, seed=seed, lively=name in P.LYRICS)
    kar, mouth = [], np.zeros(int(len(st) / SR * 100) + 1)
    if name in P.LYRICS and S.available() and P.check(name, len(mel)):
        sched, _ = C.pass_schedule(bpm, mel, passes)
        events = []
        for r in range(passes):
            k = 0
            for line in P.lines(name):
                times = []
                for disp, sung in line:
                    t0, m, d = sched[r][k]
                    events.append((sung, [(60 + m + transpose, d * 0.97)], t0))
                    times.append(t0); k += 1
                kar.append(dict(syllables=[d_ for d_, _ in line], times=times, end=sched[r][k - 1][0] + sched[r][k - 1][2]))
        voice_st = S.sing(events, len(st) / SR)
        v = voice_st[:, 0] * 0.5 + voice_st[:, 1] * 0.5
        hop = SR // 100
        nn = len(v) // hop
        env = np.sqrt(np.mean(v[:nn * hop].reshape(nn, hop) ** 2, axis=1))
        mouth[:nn] = np.clip(env / (np.percentile(env, 95) + 1e-9), 0, 1)
        vrev = C.reverb(v)
        n = min(len(st), len(vrev))
        st = st * 0.8
        st[:n] += vrev[:n] * 0.75
    return st, kar, mouth, bpm


def lullabies(minutes, rng):
    """Berceuses instrumentales pour le final (Brahms d'abord, puis des berceuses originales)."""
    out, total, i = [], 0.0, 0
    voices = ["harp", "soft", "box", "soft"]
    while total < minutes * 60:
        item = ("pd", "Brahms' Lullaby") if i == 0 else ("orig", f"lullaby{i}")
        bpm, mel, ch = C.track_spec(item, rng)
        x = C.play(bpm * 0.82, mel, ch, voices[i % 4], 12 if voices[i % 4] == "box" else 0, int(rng.integers(-2, 3)), 170, seed=100 + i)
        out.append(np.concatenate([x, np.zeros((SR * 2, 2))]))
        total += len(out[-1]) / SR
        i += 1
    x = np.concatenate(out)
    amb = C.Ambience(int(rng.integers(1e9))).make("shush", len(x), fade_in=True, fade_out=True)
    return x * 0.85 + amb * 0.7


# ---------------------------------------------------------------- Image : les personnages chantent et dansent
def perf_inner(song, ts, bpm, mouth, seed, total, cam=None):
    t_dec = (ts / 16.0) % 1.0
    beat = ts * bpm / 60.0
    parts = [D.DECORS[song["decor"]](t_dec, seed, cam) if song["decor"] in D._D2.DECORS else D.DECORS[song["decor"]](t_dec, seed)]
    mi = min(int(ts * 100), len(mouth) - 1)
    m = float(mouth[mi]) if len(mouth) else 0.0
    sleepy = song.get("sleepy")
    for idx, (who, x, facing) in enumerate(song["cast"]):
        s = 0.95 if who != "star" else 0.8
        y = (D.GROUND if song.get("boat") else D.ground(song["decor"])) - 134 * s
        if who == "fish":
            s = 1.25
            y = 470 + 8 * math.sin(2 * math.pi * ts / 2.2)
        asleep = (who == sleepy and ts < total * 0.75)
        if who == "star":
            y = 330 + 14 * math.sin(2 * math.pi * ts / 3)
        if who == "bat":
            y = 330 + 18 * math.sin(2 * math.pi * ts / 2.4)
        bounce = 0 if asleep else 9 * abs(math.sin(math.pi * (beat + idx * 0.5)))
        sway = (1.5 if asleep else 4) * math.sin(math.pi * (beat + idx * 0.5) / 2)
        wave = 0.0
        if not asleep and who in ("mimo", "bunny", "kitten", "fox") and (beat // 8) % 2 == 1:
            wave = 0.5 + 0.5 * math.sin(math.pi * beat)
        mo = 0.0 if asleep else m * (0.9 + 0.1 * math.sin(idx + beat))
        blink = asleep or ((ts + idx * 1.3) % 4.1) < 0.14
        body = PE.draw(who, 0, 0, s, mouth=mo, blink=blink, wave=wave, facing=facing, t=ts, pose="sleep" if asleep else None)
        parts.append(f'<g transform="translate({x:.1f} {y - bounce:.1f}) rotate({sway:.2f} 0 {134 * s:.0f})">{body}</g>')
        if asleep:
            parts.append(f'<g transform="translate({x + 30:.0f} {y - 80:.0f}) scale(0.9)">{I.zzz(ts / 8.0)}</g>')
        elif mo > 0.25 and who != "star":
            p = (beat / 4 + idx * 0.37) % 1.0
            parts.append(A._note(x + 40 + 50 * p, y - 130 - 120 * p, 0.9, math.sin(math.pi * p) * 0.8))
    if song.get("boat"):
        parts.append(HS._boat_front(ts))
    if any(c[0] == "fish" for c in song["cast"]):
        parts.append(D.water_front(ts / 4.0))
    if song["decor"] in D._D2.FRONTS:
        parts.append(D.foreground(song["decor"], t_dec, cam))
    return "".join(parts)


SHOT_LEN = 5.5


def _song_cam(song, j):
    """Programme de caméra des chansons : large, gros plans sur chaque chanteur, plans à deux, travelling."""
    cast = song["cast"]
    n = len(cast)
    k = j % (n + 3)
    if k == 0 or j == 0:
        return (640.0, 360.0, 1.0)
    ys = {c[0]: ((D.GROUND if song.get("boat") else D.ground(song["decor"])) - 134 * 0.95) for c in cast}
    if k <= n:
        who, x, _f = cast[(k - 1) % n]
        y = 330 if who == "star" else (470 if who == "fish" else ys[who])
        return HS._clamp_cam(x, y + 30, 1.5)
    if k == n + 1 and n >= 2:
        a, b = cast[0], cast[1]
        return HS._clamp_cam((a[1] + b[1]) / 2, ys[a[0]] + 60, 1.25)
    return (640.0, 380.0, 1.12)


def song_camera(song, ts):
    j = int(ts // SHOT_LEN)
    cur, prev = _song_cam(song, j), _song_cam(song, j - 1) if j > 0 else (640.0, 360.0, 1.0)
    u = I.smooth((ts - j * SHOT_LEN) / 0.9)
    cx, cy, z = (p + (c - p) * u for p, c in zip(prev, cur))
    cx += 14 * math.sin(2 * math.pi * ts / 11)          # léger travelling permanent
    return HS._clamp_cam(cx, cy, z * (1 + 0.015 * math.sin(2 * math.pi * ts / 7)))


def perf_body(song, ts, bpm, mouth, seed, total):
    k = W / 1280
    cx, cy, z = song_camera(song, ts)
    fg = "" if song["decor"] in D._D2.FRONTS else f'<g transform="translate({(cx - 640) * -0.25:.1f} 0)">{D.foreground(song["decor"], (ts / 16.0) % 1.0)}</g>'
    return (HS.VIGNETTE + f'<g transform="scale({k:.4f}) translate(640 360) scale({z:.4f}) translate({-cx:.1f} {-cy:.1f})">'
            f'{perf_inner(song, ts, bpm, mouth, seed, total, (cx, cy, z))}{fg}</g>'
            f'<rect width="{W}" height="{H}" fill="url(#vig_story)"/>'
            + I.text(W - 30 * k, 50 * k, "Sleepy Mimo", int(26 * k), "#FFFFFF", 600, "end", False, 0.7))


def perf_frames(song, total, bpm, mouth, seed, next_body=None, n_fade=24):
    n = int(round(total * FPS))
    for kf in range(n):
        ts = kf / FPS
        body = perf_body(song, ts, bpm, mouth, seed, total)
        if next_body and kf >= n - n_fade:
            o = I.smooth((kf - (n - n_fade) + 0.5) / n_fade)
            body += f'<g opacity="{o:.3f}">{next_body(n - kf)}</g>'
        yield I.svg(W, H, body)


def sleep_loop_frames(fin, seed, n_loop):
    """Boucle parfaite : les amis dorment sous les étoiles."""
    for kf in range(n_loop):
        t = kf / n_loop
        parts = [D.DECORS[fin["decor"]](t, seed, None) if fin["decor"] in D._D2.DECORS else D.DECORS[fin["decor"]](t, seed)]
        for idx, (who, x, facing) in enumerate(fin["cast"]):
            br = math.sin(2 * math.pi * (2 * t + idx * 0.2))
            s = 0.9
            body = PE.draw(who, 0, 0, s, blink=True, facing=facing, t=t * 16, pose="sleep")
            parts.append(f'<g transform="translate({x} {D.ground(fin["decor"]) - 134 * s:.1f}) translate(0 {134*s:.0f}) scale(1 {1 + 0.015*br:.4f}) translate(0 {-134*s:.0f})">{body}</g>')
            parts.append(f'<g transform="translate({x + 30} {D.GROUND - 300}) scale(0.8)">{I.zzz((t + idx * 0.25) % 1.0)}</g>')
        if fin["decor"] in D._D2.FRONTS:
            parts.append(D.foreground(fin["decor"], t, None))
        k = W / 1280
        body = (f'<g transform="scale({k:.4f})">{"".join(parts)}</g>'
                f'<rect width="{W}" height="{H}" fill="#0B1030" opacity="0.28"/>'
                + I.text(W - 30 * k, 50 * k, "Sleepy Mimo", int(26 * k), "#FFFFFF", 600, "end", False, 0.6))
        yield I.svg(W, H, body)


# ---------------------------------------------------------------- Épisode complet
def build(ep, episode_no, rng, out, workdir, fonts="fonts", log=print):
    from . import style
    style.set_style(ep.get("style"))
    seg, pos = [], 0.0          # (type, données, début)
    audio = []

    def add_audio(x):
        nonlocal pos
        audio.append(x); pos += len(x) / SR

    # intro
    intro = C.intro_audio(5.0)
    seg.append(("intro", None, 0.0)); add_audio(intro)
    story_all, story_t = [], 0.0          # pour les Shorts : l'histoire seule, bout à bout
    story_audio = []
    chapters_meta = []
    for ci, chap in enumerate(ep["chapters"]):
        log(f"Comédiens : chapitre {ci + 1}/{len(ep['chapters'])}")
        a, shots, subs, tot = HS.build(dict(shots=chap["story"]), rng, C.track_spec(("orig", f"bg{ci}"), rng))
        seg.append(("story", dict(shots=shots, subs=subs, total=tot, seed=int(rng.integers(1e6))), pos))
        chapters_meta.append((pos if ci else 0.0, f"Part {ci + 1}: " + chap.get("label", _label(chap))))
        for sh in shots:
            story_all.append(dict(sh, start=sh["start"] + story_t))
        story_t += tot
        story_audio.append(a)
        add_audio(a)
        if chap.get("song"):
            sg = chap["song"]
            log(f"Orchestre + Chanteur : {sg['name']}")
            st, kar, mouth, bpm = sing_track(sg["name"], sg.get("voice", "box"), sg.get("transpose", 0), rng, seed=ci)
            st = np.concatenate([st, np.zeros((SR, 2))])
            seg.append(("song", dict(song=sg, kar=kar, mouth=mouth, bpm=bpm, total=len(st) / SR, seed=int(rng.integers(1e6))), pos))
            chapters_meta.append((pos, f"🎵 {sg['name']}"))
            add_audio(st)
    fin = ep.get("finale")
    if fin:
        log(f"Orchestre : {fin['minutes']} min de berceuses")
        x = lullabies(fin["minutes"], rng)
        seg.append(("sleep", dict(fin=fin, total=len(x) / SR, seed=int(rng.integers(1e6))), pos))
        chapters_meta.append((pos, "😴 Goodnight lullabies"))
        add_audio(x)
    # au revoir + bande-annonce du prochain épisode
    friend = next((c for ch_ in ep["chapters"] for sh_ in ch_["story"] for (c, *_r) in sh_["cast"] if c not in ("mimo", "star")), "owl")
    from . import style as _st
    bye = dict(decor=ep.get("bye_decor", "night"), cast=[("mimo", 420, 420, 1), (friend, 880, 880, -1)] if _st.s2() else [("mimo", 520, 520, 1), (friend, 780, 780, -1)], lines=[
        ("mimo", "Goodnight, friends! Thank you for watching."),
        (friend, "Sweet dreams! And don't miss the next episode!")])
    shots_o = [bye] + ([ep["teaser"]] if ep.get("teaser") else [])
    o_audio, o_shots, o_subs, o_total = HS.build(dict(shots=shots_o), rng, C.track_spec(("orig", "teaser"), rng))
    teaser_t = o_shots[1]["start"] if len(o_shots) > 1 else None
    seg.append(("outro", dict(shots=o_shots, subs=o_subs, total=o_total, seed=int(rng.integers(1e6)), teaser=teaser_t), pos))
    chapters_meta.append((pos, "👋 Goodbye & next time on Sleepy Mimo"))
    add_audio(o_audio)
    total = pos
    wav = os.path.join(workdir, "long.wav")
    C.write_wav(wav, audio)

    # ---- image
    def first_body(s):
        kind, d, _ = s
        if kind == "story":
            return lambda rem: HS.shot_body(d["shots"][0], 0.0, W, H, d["seed"])
        if kind == "song":
            return lambda rem: perf_body(d["song"], 0.0, d["bpm"], d["mouth"], d["seed"], d["total"])
        if kind == "sleep":
            return lambda rem: next(sleep_loop_frames(d["fin"], d["seed"], 2)).split(">", 1)[1].rsplit("</svg>", 1)[0]
        if kind == "outro":
            return lambda rem: HS.shot_body(d["shots"][0], 0.0, W, H, d["seed"])
        return None

    entries = []
    for i, (kind, d, start) in enumerate(seg):
        nxt = first_body(seg[i + 1]) if i + 1 < len(seg) else None
        path = os.path.join(workdir, f"seg{i:02d}.ts")
        if kind == "intro":
            log("Animateur : intro")
            pe = I.make_particles("moon", W, H, int(rng.integers(1e6)))
            from .realisateur import intro_frames
            entries.append(M.encode(intro_frames(5.0, nxt, W, H, pe, f"Episode {episode_no}"), path, gop=FPS * 2, crf=18))
        elif kind == "story":
            log(f"Metteur en scène : histoire ({d['total']:.0f} s)")
            entries.append(M.encode(HS.frames(d["shots"], d["total"], W, H, d["seed"], next_body=nxt, n_fade_out=24), path, gop=FPS * 2, crf=18))
        elif kind == "song":
            log(f"Animateur : les personnages chantent « {d['song']['name']} » ({d['total']:.0f} s)")
            entries.append(M.encode(perf_frames(d["song"], d["total"], d["bpm"], d["mouth"], d["seed"], next_body=nxt), path, gop=FPS * 2, crf=18))
        elif kind == "sleep":
            log(f"Animateur : tout le monde dort ({d['total'] / 60:.0f} min)")
            n_loop = FPS * 16
            lp = M.encode(sleep_loop_frames(d["fin"], d["seed"], n_loop), path, gop=n_loop, crf=18)
            reps = int(d["total"] // 16)
            rest = d["total"] - reps * 16
            entries += [lp] * reps
            if rest > 0.1:
                entries.append((lp, rest))
        elif kind == "outro":
            log("Metteur en scène : au revoir")
            entries.append(M.encode(HS.frames(d["shots"], d["total"], W, H, d["seed"]), path, gop=FPS * 2, crf=18))
    lst = os.path.join(workdir, "concat.txt")
    with open(lst, "w") as f:
        for e in entries:
            if isinstance(e, tuple):
                f.write(f"file '{os.path.abspath(e[0])}'\noutpoint {e[1]:.4f}\n")
            else:
                f.write(f"file '{os.path.abspath(e)}'\n")
    # ---- sous-titres : titre de l'épisode, dialogues, karaoké, titres des chansons
    lines = [P.HEADER]
    for kind, d, start in seg:
        if kind in ("story", "outro"):
            if kind == "story" and start < 6:
                lines.append(P.ass_story_title(start + 0.3, f"Episode {episode_no}: {ep['title']}"))
            for a_, b_, who, text in d["subs"]:
                lines.append(P.ass_dialogue(start + a_, start + b_, who, text, PE.NAMES.get(who, "")))
            if kind == "outro" and d.get("teaser") is not None:
                lines.append(P.ass_story_title(start + d["teaser"] + 0.2, "Next time on Sleepy Mimo...", dur=4.5))
        if kind == "song":
            lines.append(P.ass_title(start + 0.3, "♪ " + d["song"]["name"]))
            kar = sorted(d["kar"], key=lambda x: x["times"][0])
            for j, ln in enumerate(kar):
                t0 = start + ln["times"][0] - 0.6
                end = start + ln["end"] + 0.5
                if j + 1 < len(kar):
                    end = min(end, start + kar[j + 1]["times"][0] - 0.65)
                lines.append(P.ass_line(t0, max(end, start + ln["times"][-1] + 0.3), ln["syllables"], [start + x for x in ln["times"]]))
    ass = os.path.join(workdir, "episode.ass")
    open(ass, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    log("Réalisateur : montage final haute qualité")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-i", wav,
                    "-map", "0:v", "-map", "1:a", "-vf", f"ass={ass}:fontsdir={fonts}", "-c:v", "libx264", "-preset", "medium",
                    "-tune", "animation", "-crf", "18", "-pix_fmt", "yuv420p", "-profile:v", "high", "-g", str(FPS * 4),
                    "-c:a", "aac", "-b:a", "256k", "-t", f"{total:.3f}", "-movflags", "+faststart", out], check=True)
    sa = np.concatenate(story_audio)
    return dict(total=total, chapters=chapters_meta, story_shots=story_all, story_total=story_t, story_audio=sa)


def _label(chap):
    first = chap["story"][0]["lines"][0][1]
    words = first.split()
    return " ".join(words[:6]).rstrip(",.") + ("…" if len(words) > 6 else "")
