"""Agent 1 — Directeur général : orchestre toute l'équipe et produit la journée.
Chaque jour : 1 vidéo longue + 3 Shorts, contrôlés puis envoyés en privé sur la chaîne."""
import os, sys, datetime, shutil
import numpy as np
from agents import strategiste, compositeur, illustrateur, monteur, redacteur, miniaturiste
from agents import controleur_qualite, gardien_regles, publieur, analyste, rapporteur, realisateur, histoires
from agents.archiviste import Memory
from agents import consignes

OUT = "output"


def log(msg):
    print(f"[{datetime.datetime.now():%H:%M:%S}] {msg}", flush=True)


def main():
    date = os.environ.get("RUN_DATE") or datetime.date.today().isoformat()
    rng = np.random.default_rng(int(date.replace("-", "")))
    shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT)
    cfg, warnings = consignes.load()
    TEST = bool(os.environ.get("TEST_RUN"))
    if TEST:
        cfg["upload"] = False
    for w in warnings:
        log(f"Consigne : {w}")
    if cfg["pause"]:
        log("Directeur : l'équipe est en pause (consignes.yml). Rien n'est produit.")
        os.makedirs("reports", exist_ok=True)
        open(f"reports/{date}.md", "w").write(f"# Rapport Sleepy Mimo — {date}\n\n⏸️ Équipe en pause sur ta demande.\n")
        return
    SHORT_SECONDS = cfg["short_seconds"]
    mem = Memory()
    if os.environ.get("GITHUB_EVENT_NAME") == "schedule" and any(d["date"] == date for d in mem.data["days"]):
        log(f"Directeur : la journée du {date} est déjà produite, le déclencheur de secours ne fait rien.")
        return
    used_titles = mem.used_titles()

    log("Stratège : planification du jour")
    plan = strategiste.plan_day(rng, mem, cfg)

    # ---------- Vidéo longue ----------
    n_loop = monteur.FPS * 16
    sung = sum(1 for t in plan["tracks"] if t.get("lyrics"))
    log(f"Compositeur + Chanteur : {len(plan['tracks'])} morceaux dont {sung} chantés "
        f"({len(plan['scene_themes'])} décors : {', '.join(plan['scene_themes'])})")
    story, outro = None, None
    episode = int(os.environ.get("EPISODE_OVERRIDE") or 0) or mem.next_episode()
    from agents.episodes_longs import LONG_EPISODES
    from agents.saison1 import EPISODES
    n1 = len(EPISODES)
    if episode > n1 and plan.get("story"):
        sid = f"s2e{episode - n1:02d}"            # saison 2 : épisodes 13 à 24
        if sid not in LONG_EPISODES:
            log(f"Directeur : l'épisode {episode} ({sid}) n'est pas encore écrit. Rien n'est produit (on ne rejoue pas la saison 1).")
            os.makedirs("reports", exist_ok=True)
            open(f"reports/{date}.md", "w").write(f"# Rapport Sleepy Mimo — {date}\n\n⏸️ L'épisode {episode} n'est pas encore écrit : rien n'a été produit.\n")
            return
        plan["story"] = dict(EPISODES[0], id=sid, title=LONG_EPISODES[sid]["title"])
    elif plan.get("story") and os.environ.get("EPISODE_OVERRIDE"):
        plan["story"] = EPISODES[(episode - 1) % len(EPISODES)]
    long_ep = LONG_EPISODES.get(plan["story"]["id"]) if plan.get("story") else None
    if long_ep:
        # Épisode long : l'histoire dure toute la vidéo (chapitres + chansons des personnages + berceuses)
        from agents import showrunner
        log(f"Showrunner : épisode {episode} « {long_ep['title']} » ({len(long_ep['chapters'])} chapitres)")
        res = showrunner.build(long_ep, episode, rng, f"{OUT}/long.mp4", OUT, log=log)
        total = res["total"]
        story = dict(title=long_ep["title"], id=long_ep["id"], shots=res["story_shots"], total=res["story_total"],
                     audio=res["story_audio"], seed=int(rng.integers(1e6)), episode=episode)
        long_meta = redacteur.episode_meta(rng, long_ep, episode, res, used_titles, cfg["extra_tags"])
        miniaturiste.make_episode(long_ep, episode, f"{OUT}/long_thumbnail.png")
    if not long_ep and plan.get("story"):
        st = plan["story"]
        log(f"Scénariste + Comédiens : histoire « {st['title']} »")
        s_audio, s_shots, s_subs, s_total = histoires.build(st, rng, compositeur.track_spec(("orig", "story"), rng))
        story = dict(title=st["title"], id=st["id"], shots=s_shots, subs=s_subs, total=s_total, audio=s_audio,
                     seed=int(rng.integers(1e6)), start=5.0 if cfg["intro"] else 0.0, episode=episode,
                     card=f"Episode {episode}: {st['title']}", raw=st)
        o_audio, o_shots, o_subs, o_total = histoires.outro(st, rng)
        outro = dict(shots=o_shots, subs=o_subs, total=o_total, audio=o_audio, seed=int(rng.integers(1e6)))
    if not long_ep:
      stamps, total, karaoke = compositeur.build_long(plan["tracks"], rng, f"{OUT}/long.wav", ambience=cfg["ambience"],
                                                      intro=5.0 if cfg["intro"] else 0.0, vocals=cfg["vocals"],
                                                      story_audio=story["audio"] if story else None,
                                                      outro_audio=outro["audio"] if outro else None)
      if outro:
          outro["start"] = total - outro["total"]
      realisateur.build_long(stamps, total, f"{OUT}/long.wav", f"{OUT}/long.mp4", OUT, rng, karaoke, log=log, story=story,
                             outro=outro, episode=episode if story else None)
      long_meta = redacteur.long_meta(rng, plan, stamps, total, used_titles, cfg["extra_tags"], sung=bool(karaoke), story=story)
      miniaturiste.make(plan["long_theme"], int(round(total / 60)), f"{OUT}/long_thumbnail.png", int(rng.integers(1e6)))

    # ---------- Shorts ----------
    short_metas, short_durs = [], []
    if story and cfg["n_shorts"]:
        # Shorts tirés de l'épisode du jour : un moment de l'histoire par Short
        parts = histoires.short_parts(story["shots"], story["total"], cfg["n_shorts"])
        import wave
        for i, (t0, t1) in enumerate(parts, 1):
            log(f"Short {i} : épisode {episode}, partie {i}/{len(parts)} ({t1 - t0:.0f} s)")
            x = histoires.short_audio(story["audio"], t0, t1)
            w = wave.open(f"{OUT}/short{i}.wav", "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(44100)
            w.writeframes((np.clip(compositeur.limit(x), -1, 1) * 32767).astype("<i2").tobytes()); w.close()
            frames = histoires.short_frames(story["shots"], t0, t1, story["seed"], episode, story["title"], i, len(parts))
            monteur.encode(frames, f"{OUT}/short{i}.mp4", gop=monteur.FPS * 2, audio=f"{OUT}/short{i}.wav", crf=21)
            short_metas.append(redacteur.short_story_meta(rng, story, i, len(parts), used_titles, cfg["extra_tags"]))
            short_durs.append(t1 - t0)
    else:
        for i, s in enumerate(plan["shorts"], 1):
            log(f"Short {i} : {s['name']} ({s['theme']})")
            compositeur.build_short(s["spec"], s["voice"], s["octave"], s["transpose"], s["seconds"], f"{OUT}/short{i}.wav",
                                    theme=s["theme"], ambience=cfg["ambience"], seed=int(rng.integers(1e6)))
            pe = illustrateur.make_particles(s["theme"], 1080, 1920, int(rng.integers(1e6)))
            frames = illustrateur.short_frames(s["theme"], pe, s["hook"], s["overlay"], monteur.FPS, s["seconds"], n_loop)
            monteur.encode(frames, f"{OUT}/short{i}.mp4", gop=monteur.FPS * 2, audio=f"{OUT}/short{i}.wav", crf=20)
            short_metas.append(redacteur.short_meta(rng, s, used_titles, cfg["extra_tags"]))


    # ---------- Contrôles ----------
    log("Gardien des règles + Contrôleur qualité")
    metas = [("Vidéo longue", long_meta)] + [(f"Short {i}", m) for i, m in enumerate(short_metas, 1)]
    guard_issues, guard_notes = gardien_regles.check(plan, metas, mem, cfg)
    results = []
    p, info = controleur_qualite.check_video(f"{OUT}/long.mp4", total)
    results.append(dict(type="Vidéo longue", titre=long_meta["title"], problemes=p, infos=info,
                        fichier=f"{OUT}/long.mp4", meta=long_meta, thumb=f"{OUT}/long_thumbnail.png"))
    for i, m in enumerate(short_metas, 1):
        p, info = controleur_qualite.check_video(f"{OUT}/short{i}.mp4", short_durs[i - 1] if i <= len(short_durs) else SHORT_SECONDS, vertical=True)
        results.append(dict(type=f"Short {i}", titre=m["title"], problemes=p, infos=info,
                            fichier=f"{OUT}/short{i}.mp4", meta=m, thumb=None))

    # ---------- Publication ----------
    analytics, uploaded = None, False
    if publieur.configured() and cfg["upload"]:
        yt = publieur.service()
        if guard_issues:
            log("Gardien des règles : envoi annulé pour la journée")
        else:
            for r in results:
                if r["problemes"]:
                    continue
                log(f"Publieur : envoi en privé — {r['titre']}")
                try:
                    r["video_id"], r["miniature"] = publieur.upload(yt, r["fichier"], r["meta"], r["thumb"])
                    uploaded = True
                except Exception as e:          # ex. limite d'envois YouTube du jour atteinte : on garde la vidéo en téléchargement
                    log(f"Publieur : envoi impossible ({str(e)[:200]})")
                    r["problemes"].append("Envoi YouTube impossible aujourd'hui (limite d'envois atteinte ?). La vidéo reste téléchargeable dans GitHub.")
        try:
            analytics = analyste.stats(yt)
        except Exception as e:
            log(f"Analyste : statistiques indisponibles ({e})")
    else:
        log("Publieur : envoi désactivé ou connexion non configurée, vidéos laissées en téléchargement")

    # ---------- Mémoire + rapport ----------
    if not TEST:
      mem.add_day(dict(date=date, run=os.environ.get("GITHUB_RUN_ID", "local"),
                     long=dict(title=long_meta["title"], theme=plan["long_theme"], story=story["id"] if story else None, episode=episode if story else None,
                               originals=[t["item"][1] for t in plan["tracks"] if t["item"][0] == "orig"],
                               video_id=results[0].get("video_id")),
                     shorts=[dict(title=m["title"], theme=s["theme"], song=s["name"], video_id=r.get("video_id"))
                             for m, s, r in zip(short_metas, plan["shorts"], results[1:])]))
    report = rapporteur.write(date, results, guard_issues, guard_notes + [f"Consigne : {w}" for w in warnings], analytics, uploaded, f"{OUT}/rapport_test.md" if TEST else f"reports/{date}.md")
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        open(os.environ["GITHUB_STEP_SUMMARY"], "a").write(report)
    for d in os.listdir(OUT):
        if d.endswith((".wav", ".ts", ".txt", ".ass")):
            shutil.rmtree(f"{OUT}/{d}", ignore_errors=True) if os.path.isdir(f"{OUT}/{d}") else os.remove(f"{OUT}/{d}")
    log("Directeur : journée terminée")
    print(report)


if __name__ == "__main__":
    main()
