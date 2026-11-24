"""Test des voix tunisiennes : choisit des voix de référence (LinTO, CC BY 4.0) homme / femme,
fait parler Habibi-TTS (dialecte TUN), puis réécoute avec Whisper pour mesurer si c'est compréhensible."""
import io, json, os, re, sys, time, glob, subprocess
import numpy as np, soundfile as sf
import parselmouth
from huggingface_hub import list_repo_files, hf_hub_download
import pyarrow.parquet as pq

OUT = "perso/tests"
os.makedirs(OUT, exist_ok=True)
os.makedirs("perso/refs", exist_ok=True)
REPO = "linagora/linto-dataset-audio-ar-tn"
log = open(f"{OUT}/log.txt", "w")


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True); log.write(s + "\n"); log.flush()


files = [f for f in list_repo_files(REPO, repo_type="dataset") if f.endswith(".parquet")]
P("parquet files:", len(files))
for f in files[:80]:
    P("  ", f)
picked = []
for key in ["ApprendreLeTunisien", "OneStory", "TunSwitch", "Youtube", ""]:
    for f in files:
        if key.lower() in f.lower() and f not in picked:
            picked.append(f)
            break
    if len(picked) >= 3:
        break
P("picked:", picked)

TEXT_KEYS = ["text", "transcript", "transcription", "sentence", "normalized_text"]
cands = []
for f in picked:
    path = hf_hub_download(REPO, f, repo_type="dataset")
    t = pq.read_table(path)
    P(f, "columns:", t.column_names, "rows:", t.num_rows)
    cols = t.column_names
    acol = next((c for c in cols if "audio" in c.lower()), None)
    tcol = next((c for c in TEXT_KEYS if c in cols), None)
    if not acol or not tcol:
        continue
    n = min(t.num_rows, 400)
    for i in range(n):
        a = t[acol][i].as_py(); txt = t[tcol][i].as_py()
        if not a or not txt:
            continue
        b = a.get("bytes") if isinstance(a, dict) else None
        if not b:
            continue
        try:
            y, sr = sf.read(io.BytesIO(b))
        except Exception:
            continue
        if y.ndim > 1:
            y = y.mean(1)
        d = len(y) / sr
        if not (4.0 <= d <= 9.5) or len(txt) < 25:
            continue
        snd = parselmouth.Sound(y, sr)
        f0 = snd.to_pitch().selected_array["frequency"]; f0 = f0[f0 > 0]
        if len(f0) < 50:
            continue
        fr = y[: len(y) // 512 * 512].reshape(-1, 512)
        e = np.sqrt((fr ** 2).mean(1) + 1e-12)
        snr = 20 * np.log10(np.percentile(e, 95) / max(np.percentile(e, 10), 1e-6))
        cands.append(dict(src=f, i=i, text=txt, dur=d, f0=float(np.median(f0)), snr=float(snr), y=y, sr=sr))
P("candidats:", len(cands))

fem = sorted([c for c in cands if c["f0"] > 175], key=lambda c: -c["snr"])[:4]
mal = sorted([c for c in cands if c["f0"] < 140], key=lambda c: -c["snr"])[:4]
refs = []
for g, lst in (("F", fem), ("M", mal)):
    for k, c in enumerate(lst):
        p = f"perso/refs/{g}{k}.wav"
        sf.write(p, c["y"], c["sr"])
        refs.append(dict(name=f"{g}{k}", path=p, text=c["text"], f0=c["f0"], snr=c["snr"], dur=c["dur"], src=c["src"]))
        P(g, k, round(c["f0"]), round(c["snr"], 1), round(c["dur"], 1), c["text"])

# --------------------------------------------------------------- Habibi
from importlib.resources import files as pfiles
from cached_path import cached_path
from omegaconf import OmegaConf
from hydra.utils import get_class
from f5_tts.infer.utils_infer import load_model, load_vocoder, preprocess_ref_audio_text
from habibi_tts.infer.utils_infer import infer_process
from habibi_tts.model.utils import dialect_id_map

cfg = OmegaConf.load(str(pfiles("f5_tts").joinpath("configs/F5TTS_v1_Base.yaml")))
ckpt = str(cached_path("hf://SWivid/Habibi-TTS/Unified/model_200000.safetensors"))
vocab = str(cached_path("hf://SWivid/Habibi-TTS/Unified/vocab.txt"))
model = load_model(get_class(f"f5_tts.model.{cfg.model.backbone}"), cfg.model.arch, ckpt,
                   mel_spec_type="vocos", vocab_file=vocab, device="cpu")
voc = load_vocoder(vocoder_name="vocos", device="cpu")

ALG = str(pfiles("habibi_tts").joinpath("assets/ALG.wav"))
refs.append(dict(name="ALG", path=ALG, text="أنيا هكا باغية ناكل هكا أني ن نشوف فيها الحاجة هذيكا.", f0=0, snr=0, dur=0, src="habibi"))

TESTS = ["شنوّة أحوالك يا صاحبي؟ لاباس عليك؟ توّا نمشيو نشربو قهوة في سيدي بوسعيد.",
         "يا عصبة! روح طير يا بلّوط، ما فهمت شي!"]

from faster_whisper import WhisperModel
asr = WhisperModel("medium", device="cpu", compute_type="int8")


def norm(s):
    s = re.sub(r"[ً-ْـ]", "", s)
    s = re.sub(r"[^ء-ي ]", " ", s)
    s = s.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا").replace("ة", "ه").replace("ى", "ي")
    return " ".join(s.split())


def cer(a, b):
    a, b = norm(a), norm(b)
    d = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        prev, d[0] = d[0], i
        for j, cb in enumerate(b, 1):
            prev, d[j] = d[j], min(d[j] + 1, d[j - 1] + 1, prev + (ca != cb))
    return d[len(b)] / max(1, len(a))


results = []
for r in refs:
    ra, rt = preprocess_ref_audio_text(r["path"], r["text"])
    row = dict(r); row["tests"] = []
    for k, txt in enumerate(TESTS):
        t0 = time.time()
        wav, sr, _ = infer_process(ra, rt, txt, model, voc, mel_spec_type="vocos", nfe_step=32,
                                   cfg_strength=2.0, sway_sampling_coef=-1.0, speed=1.0, device="cpu",
                                   dialect_id=dialect_id_map["TUN"])
        el = time.time() - t0
        p = f"{OUT}/{r['name']}_{k}.wav"
        sf.write(p, wav, sr)
        segs, _ = asr.transcribe(p, language="ar", beam_size=5)
        hyp = " ".join(s.text for s in segs)
        f0 = parselmouth.Sound(wav, sr).to_pitch().selected_array["frequency"]; f0 = f0[f0 > 0]
        row["tests"].append(dict(k=k, secs=len(wav) / sr, rtf=el / (len(wav) / sr), hyp=hyp, cer=cer(txt, hyp),
                                 f0=float(np.median(f0)) if len(f0) else 0))
        P(r["name"], k, "rtf", round(el / (len(wav) / sr), 2), "cer", round(cer(txt, hyp), 2), "|", hyp)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", p, "-b:a", "48k", p[:-4] + ".mp3"])
        os.remove(p)
    row["cer_mean"] = float(np.mean([t["cer"] for t in row["tests"]]))
    results.append(row)
for r in refs:
    if r["path"].startswith("perso/refs"):
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", r["path"], "-b:a", "48k", f"{OUT}/ref_{r['name']}.mp3"])
json.dump(results, open(f"{OUT}/results.json", "w"), ensure_ascii=False, indent=1)
P("FINI")
