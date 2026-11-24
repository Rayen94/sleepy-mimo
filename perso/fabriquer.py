"""Fabrique un épisode de « رايان و يقين » et l'envoie en PRIVÉ sur la chaîne (pas pour enfants)."""
import os, sys, json, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from perso import episodes as E, film as F, voix as V

num = int(sys.argv[1])
ep = E.EPISODES[num]
OUT = "perso_out"
os.makedirs(OUT, exist_ok=True)
logf = open(f"{OUT}/journal_ep{num}.txt", "w")


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True); logf.write(s + "\n"); logf.flush()


t0 = time.time()
voices = V.load_voices(ep, f"voix_ep{num}") if os.environ.get("FAKE_VOICES") != "1" else V.fake_voices(ep)
missing = sum(1 for si, li, ln in V.all_lines(ep) if not os.path.exists(f"voix_ep{num}/{si:02d}_{li:02d}.wav"))
log(f"voix chargées, manquantes : {missing}")
log(f"voix prêtes en {(time.time()-t0)/60:.1f} min")
mp4 = f"{OUT}/rayen_yakin_ep{num}.mp4"
shots, total = F.render(ep, voices, mp4, OUT, log=log)
log(f"vidéo prête : {total/60:.1f} min, en {(time.time()-t0)/60:.1f} min au total")

from agents import monteur
ok, err = monteur.decode_ok(mp4)
log("contrôle décodage :", ok, err)
log("volume :", monteur.loudness(mp4))

if os.environ.get("YT_REFRESH_TOKEN") and os.environ.get("ENVOYER", "1") == "1":
    from agents import publieur
    from googleapiclient.http import MediaFileUpload
    title = f"رايان و يقين — الحلقة {num}: {ep['title']}"
    desc = (f"رايان و يقين — الحلقة {num}\n"
            "سلسلة كرتون بالدارجة التونسية (مشروع شخصي).\n\n"
            "Voix : Habibi-TTS (SWivid, CC BY-NC-SA 4.0), voix de référence : LinTO Tunisian dataset (Linagora, CC BY 4.0). "
            "Usage personnel, non commercial.")
    body = {"snippet": {"title": title[:100], "description": desc, "categoryId": "1",
                        "defaultLanguage": "ar", "defaultAudioLanguage": "ar"},
            "status": {"privacyStatus": "private", "selfDeclaredMadeForKids": False}}
    try:
        yt = publieur.service()
        req = yt.videos().insert(part="snippet,status", body=body,
                                 media_body=MediaFileUpload(mp4, chunksize=8 * 1024 * 1024, resumable=True))
        resp = None
        while resp is None:
            _, resp = req.next_chunk()
        log("ENVOYÉE SUR YOUTUBE (privé) :", resp["id"])
        json.dump({"episode": num, "video_id": resp["id"]}, open(f"{OUT}/youtube_ep{num}.json", "w"))
    except Exception as e:
        log("ENVOI YOUTUBE ÉCHOUÉ :", repr(e)[:500])
