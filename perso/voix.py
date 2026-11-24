"""Les voix tunisiennes : Habibi-TTS (dialecte TUN) avec une voix de référence par personnage,
contrôle de compréhension par Whisper (on refait la réplique si elle est mal prononcée)."""
import json, os, re, time
import numpy as np, soundfile as sf

SR = 44100
# personnage -> (voix de référence, vitesse, facteur de hauteur, facteur de formants)
CHOIX = "perso/refs/choix.json"
DEFAULT = {"rayen": ("M0", 1.0, 1.0, 1.0), "hamma": ("M1", 1.05, 0.92, 0.97), "skander": ("M2", 0.97, 1.04, 1.0),
           "yakin": ("F0", 1.0, 1.0, 1.0), "sarra": ("F1", 1.05, 1.03, 1.0), "mama": ("F2", 0.95, 0.9, 0.97)}

_M = {}


def _load():
    if _M:
        return _M
    from importlib.resources import files as pfiles
    from cached_path import cached_path
    from omegaconf import OmegaConf
    from hydra.utils import get_class
    from f5_tts.infer.utils_infer import load_model, load_vocoder
    from habibi_tts.model.utils import dialect_id_map
    cfg = OmegaConf.load(str(pfiles("f5_tts").joinpath("configs/F5TTS_v1_Base.yaml")))
    ckpt = str(cached_path("hf://SWivid/Habibi-TTS/Unified/model_200000.safetensors"))
    vocab = str(cached_path("hf://SWivid/Habibi-TTS/Unified/vocab.txt"))
    _M["model"] = load_model(get_class(f"f5_tts.model.{cfg.model.backbone}"), cfg.model.arch, ckpt,
                             mel_spec_type="vocos", vocab_file=vocab, device="cpu")
    _M["voc"] = load_vocoder(vocoder_name="vocos", device="cpu")
    _M["tun"] = dialect_id_map["TUN"]
    try:
        from faster_whisper import WhisperModel
        _M["asr"] = WhisperModel("small", device="cpu", compute_type="int8")
    except Exception:
        _M["asr"] = None
    return _M


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


def _clean(text):
    t = text.replace("...", "،").replace("…", "،").replace("\"", "")
    t = re.sub(r"\s+", " ", t).strip()
    return t


def _post(y, sr, pitch, formant):
    import parselmouth
    from parselmouth.praat import call
    snd = parselmouth.Sound(y.astype(np.float64), sampling_frequency=sr)
    if abs(pitch - 1) > 0.01 or abs(formant - 1) > 0.01:
        f0 = snd.to_pitch().selected_array["frequency"]
        med = float(np.median(f0[f0 > 0])) if (f0 > 0).any() else 150.0
        snd = call(snd, "Change gender", 75, 600, formant, med * pitch, 1.0, 1.0)
    y = call(snd, "Resample", SR, 50).values[0]
    env = np.convolve(np.abs(y), np.ones(400) / 400, mode="same")
    idx = np.where(env > env.max() * 0.04)[0]
    if len(idx):
        y = y[max(0, idx[0] - 300): idx[-1] + 2500]
    y = y / (np.sqrt((y ** 2).mean()) + 1e-9) * 0.085
    y = np.clip(y, -0.95, 0.95)
    hop = SR // 100
    n = len(y) // hop
    rms = np.sqrt(np.mean(y[:n * hop].reshape(n, hop) ** 2, axis=1))
    mouth = np.clip(rms / (np.percentile(rms, 92) + 1e-9), 0, 1)
    return y, np.convolve(mouth, np.ones(3) / 3, mode="same")


def episode_voices(ep, cache_dir, log=print):
    from f5_tts.infer.utils_infer import preprocess_ref_audio_text
    from habibi_tts.infer.utils_infer import infer_process
    m = _load()
    choix = json.load(open(CHOIX)) if os.path.exists(CHOIX) else {}
    refs = json.load(open("perso/refs/refs.json"))
    os.makedirs(cache_dir, exist_ok=True)
    prepared = {}
    out, report = {}, []
    t_all = time.time()
    for si, sh in enumerate(ep["shots"]):
        for li, ln in enumerate(sh.get("lines", [])):
            who, text = ln[0], ln[3]
            rname, speed, pitch, formant = choix.get(who, DEFAULT[who])
            if rname not in prepared:
                r = refs[rname]
                prepared[rname] = preprocess_ref_audio_text(r["path"], r["text"])
            ra, rt = prepared[rname]
            gen = _clean(text)
            best = None
            for attempt in range(3):
                wav, sr, _ = infer_process(ra, rt, gen, m["model"], m["voc"], mel_spec_type="vocos", nfe_step=32,
                                           cfg_strength=2.0, sway_sampling_coef=-1.0, speed=speed, device="cpu",
                                           dialect_id=m["tun"])
                wav = np.asarray(wav, dtype=np.float32)
                score = 0.0
                if m["asr"] is not None and len(norm(gen)) >= 6:
                    p = os.path.join(cache_dir, "_tmp.wav"); sf.write(p, wav, sr)
                    segs, _ = m["asr"].transcribe(p, language="ar", beam_size=3)
                    hyp = " ".join(s.text for s in segs)
                    score = cer(gen, hyp)
                dur = len(wav) / sr
                ratio = dur / max(1, len(norm(gen)))
                if ratio > 0.2 or ratio < 0.035:
                    score += 0.5
                if best is None or score < best[0]:
                    best = (score, wav, sr)
                if score < 0.45:
                    break
            y, mouth = _post(best[1], best[2], pitch, formant)
            out[(si, li)] = (y, mouth)
            sf.write(os.path.join(cache_dir, f"{si:02d}_{li:02d}.wav"), y, SR, subtype="PCM_16")
            report.append(dict(k=f"{si}-{li}", who=who, cer=round(best[0], 2), secs=round(len(y) / SR, 2)))
            log(f"  voix {si}-{li} {who} cer={best[0]:.2f} {len(y)/SR:.1f}s ({time.time()-t_all:.0f}s)")
    json.dump(report, open(os.path.join(cache_dir, "rapport_voix.json"), "w"), ensure_ascii=False, indent=1)
    return out


def fake_voices(ep):
    """Voix muettes (tests locaux)."""
    out = {}
    for si, sh in enumerate(ep["shots"]):
        for li, ln in enumerate(sh.get("lines", [])):
            d = 0.6 + len(ln[3]) * 0.07
            n = int(d * SR)
            y = np.sin(np.arange(n) / SR * 2 * np.pi * 180) * 0.05
            out[(si, li)] = (y, np.abs(np.sin(np.arange(int(d * 100)) / 3)))
    return out
