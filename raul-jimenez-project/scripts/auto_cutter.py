#!/usr/bin/env python3
"""
AUTO-CUTTER — finds the big moments in football footage and cuts clips.
=======================================================================
Detection layers (combined score):
  1. Crowd-roar audio peaks (RMS volume)      — catches goals/big moments
  2. Whisper commentary keywords ("Jimenez", "goal", ...) — player filter
Cuts clips with ffmpeg around the highest-scoring moments.

Usage:
  python3 auto_cutter.py match.mp4                          # audio peaks only
  python3 auto_cutter.py match.mp4 --whisper                # + keyword spotting
  python3 auto_cutter.py match.mp4 --whisper --keywords jimenez,raul,goal
  python3 auto_cutter.py match.mp4 --top 8 --pre 8 --post 7 # tune cuts

Requires: ffmpeg on PATH. pip3 install numpy
Optional: pip3 install openai-whisper   (for --whisper)

Output: clips/<source-name>/clip_01_score87_t3412.mp4 + clips_report.json
"""

import argparse
import json
import subprocess
import sys
import wave
from pathlib import Path

try:
    import numpy as np
except ImportError:
    sys.exit("pip3 install numpy")

DEFAULT_KEYWORDS = ["jimenez", "jiménez", "raul", "raúl", "goal", "scores", "header", "penalty", "what a"]


def run(cmd: list) -> None:
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        sys.exit(f"Command failed: {' '.join(cmd[:6])}...\n{res.stderr[-600:]}")


def extract_audio(video: Path, tmp_wav: Path) -> None:
    """Mono 16kHz wav for both RMS analysis and Whisper."""
    print("[1/4] Extracting audio ...")
    run(["ffmpeg", "-y", "-i", str(video), "-vn", "-ac", "1", "-ar", "16000",
         "-acodec", "pcm_s16le", str(tmp_wav)])


def audio_peak_scores(tmp_wav: Path) -> np.ndarray:
    """Rolling RMS per second, normalized 0..1. Crowd roar = high score."""
    print("[2/4] Scanning for crowd roars (audio RMS) ...")
    with wave.open(str(tmp_wav), "rb") as w:
        sr, n = w.getframerate(), w.getnframes()
        raw = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float32)
    seconds = len(raw) // sr
    rms = np.array([np.sqrt((raw[i * sr:(i + 1) * sr] ** 2).mean()) for i in range(seconds)])
    # smooth over 5s so sustained roars beat single bangs
    kernel = np.ones(5) / 5
    smooth = np.convolve(rms, kernel, mode="same")
    lo, hi = smooth.min(), smooth.max()
    return (smooth - lo) / (hi - lo + 1e-9)


def _transcribe(tmp_wav: Path, model_name: str):
    """Try openai-whisper first, fall back to faster-whisper.
    Returns list of segments: [{'start': s, 'end': e, 'text': t}, ...] or None."""
    try:
        import whisper
        print(f"[3/4] Transcribing with openai-whisper ({model_name}) ...")
        model = whisper.load_model(model_name)
        result = model.transcribe(str(tmp_wav), verbose=False)
        return [{"start": s["start"], "end": s["end"], "text": s["text"]}
                for s in result["segments"]]
    except ImportError:
        pass
    try:
        from faster_whisper import WhisperModel
        print(f"[3/4] Transcribing with faster-whisper ({model_name}) ...")
        model = WhisperModel(model_name, compute_type="int8")
        segments, _info = model.transcribe(str(tmp_wav))
        return [{"start": s.start, "end": s.end, "text": s.text} for s in segments]
    except ImportError:
        print("[!] Neither openai-whisper nor faster-whisper installed —")
        print("    pip install openai-whisper   (needs torch, Python <=3.12)")
        print("    pip install faster-whisper   (no torch needed)")
        return None


def whisper_keyword_scores(tmp_wav: Path, duration: int, keywords: list, model_name: str) -> np.ndarray:
    """Transcribe commentary; +1.0 around every keyword mention."""
    segments = _transcribe(tmp_wav, model_name)
    if segments is None:
        return np.zeros(duration)
    scores = np.zeros(duration)
    hits = []
    for seg in segments:
        text = seg["text"].lower()
        if any(k in text for k in keywords):
            s, e = int(seg["start"]), min(int(seg["end"]) + 1, duration)
            scores[max(0, s - 3):e] += 1.0
            hits.append((int(seg["start"]), seg["text"].strip()))
    print(f"      {len(hits)} keyword mentions found:")
    for t, txt in hits[:20]:
        print(f"        {t//60:02d}:{t%60:02d}  {txt[:90]}")
    return np.clip(scores, 0, 2.0) / 2.0


def pick_moments(score: np.ndarray, top: int, min_gap: int = 45) -> list:
    """Highest-scoring seconds, at least min_gap apart (one event = one clip)."""
    order = np.argsort(score)[::-1]
    chosen = []
    for t in order:
        if score[t] <= 0.05:
            break
        if all(abs(int(t) - c) >= min_gap for c in chosen):
            chosen.append(int(t))
        if len(chosen) >= top:
            break
    return sorted(chosen)


def cut_clips(video: Path, moments: list, score: np.ndarray, pre: int, post: int, out_dir: Path) -> list:
    print("[4/4] Cutting clips with ffmpeg ...")
    out_dir.mkdir(parents=True, exist_ok=True)
    report = []
    for i, t in enumerate(moments, 1):
        start = max(0, t - pre)
        name = f"clip_{i:02d}_score{int(score[t]*100)}_t{t}.mp4"
        out = out_dir / name
        run(["ffmpeg", "-y", "-ss", str(start), "-i", str(video), "-t", str(pre + post),
             "-c:v", "libx264", "-preset", "fast", "-crf", "20", "-c:a", "aac", str(out)])
        ts = f"{t//60:02d}:{t%60:02d}"
        print(f"      {name}   (moment at {ts}, score {score[t]:.2f})")
        report.append({"file": name, "moment_sec": t, "timestamp": ts, "score": round(float(score[t]), 3)})
    return report


def main() -> None:
    p = argparse.ArgumentParser(description="Auto-cut football highlights")
    p.add_argument("video", type=Path)
    p.add_argument("--whisper", action="store_true", help="add commentary keyword detection")
    p.add_argument("--keywords", type=str, default=",".join(DEFAULT_KEYWORDS))
    p.add_argument("--model", type=str, default="base", help="whisper model: tiny/base/small")
    p.add_argument("--top", type=int, default=6, help="number of clips")
    p.add_argument("--pre", type=int, default=10, help="seconds before the moment")
    p.add_argument("--post", type=int, default=8, help="seconds after the moment")
    a = p.parse_args()

    if not a.video.exists():
        sys.exit(f"File not found: {a.video}")
    out_dir = Path("clips") / a.video.stem
    tmp_wav = Path(f".tmp_{a.video.stem}.wav")

    extract_audio(a.video, tmp_wav)
    audio = audio_peak_scores(tmp_wav)
    combined = audio.copy()
    if a.whisper:
        kw = [k.strip().lower() for k in a.keywords.split(",") if k.strip()]
        kws = whisper_keyword_scores(tmp_wav, len(audio), kw, a.model)
        combined = 0.5 * audio + 0.8 * kws  # keyword mentions outrank raw noise

    moments = pick_moments(combined, a.top)
    if not moments:
        sys.exit("No strong moments found — try a longer video or lower-quality threshold.")
    report = cut_clips(a.video, moments, combined, a.pre, a.post, out_dir)
    (out_dir / "clips_report.json").write_text(json.dumps(report, indent=2))
    tmp_wav.unlink(missing_ok=True)
    print(f"\n[done] {len(report)} clips -> {out_dir}/  (+ clips_report.json)")
    print("Next: python3 reframe_vertical.py <clip>  ->  9:16 with captions")


if __name__ == "__main__":
    main()
