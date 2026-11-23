"""Agent 16 — Réalisateur : monte la vidéo longue comme un vrai programme de comptines.
Intro « Sleepy Mimo » → une scène par chanson (scène dédiée pour chaque comptine, décor pour les berceuses),
fondus enchaînés pile pendant les silences entre deux chansons, titre de chaque chanson à l'écran,
paroles en karaoké, puis incrustation finale en Full HD."""
import math, os, subprocess
from . import illustrateur as I, animateur as A, monteur as M, parolier as P, histoires as HS, personnages as PE

FPS = M.FPS
LOOP_S, TRANS_S = 16, 3
N_LOOP, N_TRANS = FPS * LOOP_S, FPS * TRANS_S


def scene_key(track):
    kind, name = track["item"]
    if kind == "pd" and name in A.SONG_SCENES:
        return A.SONG_SCENES[name]
    return track["theme"]


def make_pe(key, W, H, seed):
    return A.particles(key, seed) if key in A.SCENES else I.make_particles(key, W, H, seed)


def frame(key, W, H, t, pe, watermark=True):
    if key in A.SCENES:
        return A.body(key, W, H, t, pe)
    return I.scene_body(key, W, H, t, pe, watermark=watermark)


def loop_frames(key, W, H, pe):
    for k in range(N_LOOP):
        yield I.svg(W, H, frame(key, W, H, k / N_LOOP, pe))


def trans_frames(a, pea, a_phase, b, peb, W, H):
    for k in range(N_TRANS):
        fa = frame(a, W, H, (a_phase + k / N_LOOP) % 1.0, pea)
        fb = frame(b, W, H, (N_LOOP - N_TRANS + k) / N_LOOP, peb)
        o = I.smooth((k + 0.5) / N_TRANS)
        yield I.svg(W, H, f'<g>{fa}</g><g opacity="{o:.3f}">{fb}</g>')


def intro_frames(seconds, next_body, W, H, pe_intro, subtitle="Lullabies for babies"):
    """Intro de marque : Mimo sur la lune, zoom doux, « Sleepy Mimo » qui apparaît, puis fondu vers la 1re scène."""
    n = int(round(seconds * FPS))
    n_fade = min(n // 2, int(1.5 * FPS))
    k_ = W / 1280
    for k in range(n):
        ts = k / FPS
        cam = 1.12 - 0.12 * I.smooth(ts / 3.0)
        base = I.scene_body("moon", W, H, (k % N_LOOP) / N_LOOP, pe_intro, cam=cam, watermark=False, mimo_dy=115, mimo_scale=0.82)
        pop = I.ease_out_back((ts - 0.4) / 0.6) if ts > 0.4 else 0.0
        op1 = min(1.0, max(0.0, (ts - 0.4) / 0.4))
        op2 = min(1.0, max(0.0, (ts - 1.1) / 0.5))
        cx, cy = W / 2, 95 * k_
        brand = (f'<g opacity="{op1:.3f}" transform="translate({cx} {cy}) scale({max(0.01, pop):.3f}) translate({-cx} {-cy})">'
                 + I.text(cx, cy + 40 * k_, "Sleepy Mimo", int(110 * k_), "#FFE9A0") + "</g>"
                 + f'<g opacity="{op2:.3f}">' + I.text(cx, cy + 105 * k_, subtitle, int(46 * k_), "#FFFFFF", 600) + "</g>")
        body = f"<g>{base}{brand}</g>"
        if k >= n - n_fade:
            o = I.smooth((k - (n - n_fade) + 0.5) / n_fade)
            body += f'<g opacity="{o:.3f}">{next_body(n - k)}</g>'
        yield I.svg(W, H, body)


def write_ass(path, stamps, karaoke, total, story=None, outro=None):
    lines = [P.HEADER]
    if story:
        t0 = story['start']
        lines.append(P.ass_story_title(t0 + 0.3, story.get('card', story['title'])))
        for a, b, who, text in story['subs']:
            lines.append(P.ass_dialogue(t0 + a, t0 + b, who, text, PE.NAMES.get(who, '')))
    if outro:
        for a, b, who, text in outro['subs']:
            lines.append(P.ass_dialogue(outro['start'] + a, outro['start'] + b, who, text, PE.NAMES.get(who, '')))
    kar = sorted(karaoke, key=lambda x: x["times"][0])
    for i, ln in enumerate(kar):
        start = ln["times"][0] - 0.6
        end = ln["end"] + 0.5
        if i + 1 < len(kar):
            end = min(end, kar[i + 1]["times"][0] - 0.65)
        lines.append(P.ass_line(start, max(end, ln["times"][-1] + 0.3), ln["syllables"], ln["times"]))
    for pos, p in stamps:
        lines.append(P.ass_title(pos + 0.4, "♪ " + p["item"][1]))
    open(path, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    return path


def build_long(stamps, total, wav, out, workdir, rng, karaoke, log=print, W=1920, H=1080, fonts="fonts", story=None, outro=None, episode=None):
    keys = [scene_key(p) for _, p in stamps]
    pes = {}
    for k in dict.fromkeys(keys):
        pes[k] = make_pe(k, W, H, int(rng.integers(1e6)))
    loops = {}
    for k in pes:
        log(f"Animateur : scène « {k} »")
        loops[k] = M.encode(loop_frames(k, W, H, pes[k]), os.path.join(workdir, f"loop_{k}.ts"), gop=N_LOOP)
    entries = []
    first_scene = lambda rem: frame(keys[0], W, H, (N_LOOP - rem) / N_LOOP, pes[keys[0]])
    intro = (story["start"] if story else stamps[0][0]) if stamps else 0
    if intro > 0.5:
        log("Animateur : intro Sleepy Mimo")
        pe_i = I.make_particles("moon", W, H, int(rng.integers(1e6)))
        if story:
            seed = story["seed"]
            nxt = lambda rem: HS.shot_body(story["shots"][0], 0.0, W, H, seed)
        else:
            nxt = first_scene
        sub = f"Episode {episode}" if episode else "Lullabies for babies"
        entries.append((M.encode(intro_frames(intro, nxt, W, H, pe_i, sub), os.path.join(workdir, "intro.ts"), gop=FPS), None))
    if story:
        log(f"Metteur en scène : histoire « {story['title']} » ({story['total']:.0f} s)")
        entries.append((M.encode(HS.frames(story["shots"], story["total"], W, H, story["seed"], next_body=first_scene),
                                 os.path.join(workdir, "story.ts"), gop=FPS * 2), None))
    for i, (pos, p) in enumerate(stamps):
        k = keys[i]
        seg_start = pos + (TRANS_S - 2.5 if i > 0 else 0.0)
        seg_end = stamps[i + 1][0] - 2.5 if i + 1 < len(stamps) else (outro["start"] if outro else total + 1)
        q, r = divmod(max(0.0, seg_end - seg_start), LOOP_S)
        entries += [(loops[k], None)] * int(q)
        if r > 1.5 / FPS:
            entries.append((loops[k], round(r * FPS) / FPS))
        if i + 1 < len(stamps):
            phase = (round(r * FPS) % N_LOOP) / N_LOOP if r > 1.5 / FPS else 0.0
            nk = keys[i + 1]
            tf = M.encode(trans_frames(k, pes[k], phase, nk, pes[nk], W, H), os.path.join(workdir, f"trans_{i}.ts"), gop=N_TRANS)
            entries.append((tf, None))
    if outro:
        log("Metteur en scène : générique de fin")
        entries.append((M.encode(HS.frames(outro["shots"], outro["total"], W, H, outro["seed"]),
                                 os.path.join(workdir, "outro.ts"), gop=FPS * 2), None))
    lst = os.path.join(workdir, "concat.txt")
    with open(lst, "w") as f:
        for e, op in entries:
            f.write(f"file '{os.path.abspath(e)}'\n")
            if op:
                f.write(f"outpoint {op:.4f}\n")
    ass = write_ass(os.path.join(workdir, "lyrics.ass"), stamps, karaoke, total, story, outro)
    log("Réalisateur : incrustation des paroles et des titres + mixage final")
    vf = f"ass={ass}:fontsdir={fonts}"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-i", wav,
                    "-map", "0:v", "-map", "1:a", "-vf", vf, "-c:v", "libx264", "-preset", "veryfast", "-tune", "animation",
                    "-crf", "22", "-pix_fmt", "yuv420p", "-g", str(FPS * 4), "-c:a", "aac", "-b:a", "192k",
                    "-t", f"{total:.3f}", "-movflags", "+faststart", out], check=True)
    return M.duration(out)
