"""Agent 1 — Directeur général : orchestre toute l'équipe et produit la journée.
Chaque jour : 1 vidéo longue + 3 Shorts, contrôlés puis envoyés en privé sur la chaîne."""
import os, sys, datetime, shutil
import numpy as np
from agents import strategiste, compositeur, illustrateur, monteur, redacteur, miniaturiste
from agents import controleur_qualite, gardien_regles, publieur, analyste, rapporteur
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
    for w in warnings:
        log(f"Consigne : {w}")
    if cfg["pause"]:
        log("Directeur : l'équipe est en pause (consignes.yml). Rien n'est produit.")
        os.makedirs("reports", exist_ok=True)
        open(f"reports/{date}.md", "w").write(f"# Rapport Sleepy Mimo — {date}\n\n⏸️ Équipe en pause sur ta demande.\n")
        return
    SHORT_SECONDS = cfg["short_seconds"]
    mem = Memory()
    used_titles = mem.used_titles()

    log("Stratège : planification du jour")
    plan = strategiste.plan_day(rng, mem, cfg)

    # ---------- Vidéo longue ----------
    log(f"Compositeur : {len(plan['tracks'])} morceaux pour la vidéo longue")
    stamps, total = compositeur.build_long(plan["tracks"], rng, f"{OUT}/long.wav")
    log("Illustrateur : animation de la vidéo longue")
    illustrateur.render_loop(plan["long_theme"], 1280, 720, f"{OUT}/frames_long", seed=int(rng.integers(1e6)))
    log("Monteur : assemblage")
    monteur.encode_loop(f"{OUT}/frames_long", f"{OUT}/long_loop.mp4")
    monteur.mux(f"{OUT}/long_loop.mp4", f"{OUT}/long.wav", f"{OUT}/long.mp4")
    long_meta = redacteur.long_meta(rng, plan, stamps, total, used_titles, cfg["extra_tags"])
    miniaturiste.make(plan["long_theme"], int(round(total / 60)), f"{OUT}/long_thumbnail.png", int(rng.integers(1e6)))

    # ---------- Shorts ----------
    short_metas = []
    for i, s in enumerate(plan["shorts"], 1):
        log(f"Short {i} : {s['name']} ({s['theme']})")
        compositeur.build_short(s["spec"], s["voice"], s["octave"], s["transpose"], s["seconds"], f"{OUT}/short{i}.wav")
        illustrateur.render_loop(s["theme"], 1080, 1920, f"{OUT}/frames_s{i}", seed=int(rng.integers(1e6)),
                                 overlay=redacteur.short_overlay(s, 1080, 1920))
        monteur.encode_loop(f"{OUT}/frames_s{i}", f"{OUT}/s{i}_loop.mp4")
        monteur.mux(f"{OUT}/s{i}_loop.mp4", f"{OUT}/short{i}.wav", f"{OUT}/short{i}.mp4")
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
        p, info = controleur_qualite.check_video(f"{OUT}/short{i}.mp4", SHORT_SECONDS, vertical=True)
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
                r["video_id"], r["miniature"] = publieur.upload(yt, r["fichier"], r["meta"], r["thumb"])
                uploaded = True
        try:
            analytics = analyste.stats(yt)
        except Exception as e:
            log(f"Analyste : statistiques indisponibles ({e})")
    else:
        log("Publieur : envoi désactivé ou connexion non configurée, vidéos laissées en téléchargement")

    # ---------- Mémoire + rapport ----------
    mem.add_day(dict(date=date,
                     long=dict(title=long_meta["title"], theme=plan["long_theme"],
                               originals=[t["item"][1] for t in plan["tracks"] if t["item"][0] == "orig"],
                               video_id=results[0].get("video_id")),
                     shorts=[dict(title=m["title"], theme=s["theme"], song=s["name"], video_id=r.get("video_id"))
                             for m, s, r in zip(short_metas, plan["shorts"], results[1:])]))
    report = rapporteur.write(date, results, guard_issues, guard_notes + [f"Consigne : {w}" for w in warnings], analytics, uploaded, f"reports/{date}.md")
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        open(os.environ["GITHUB_STEP_SUMMARY"], "a").write(report)
    for d in os.listdir(OUT):
        if d.startswith("frames") or d.endswith(".wav") or d.endswith("_loop.mp4"):
            shutil.rmtree(f"{OUT}/{d}", ignore_errors=True) if os.path.isdir(f"{OUT}/{d}") else os.remove(f"{OUT}/{d}")
    log("Directeur : journée terminée")
    print(report)


if __name__ == "__main__":
    main()
