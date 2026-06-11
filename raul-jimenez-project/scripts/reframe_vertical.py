#!/usr/bin/env python3
"""
REFRAME VERTICAL — 16:9 clip -> 9:16 platform-ready short, with captions.
========================================================================
Two crop modes:
  - centre (default): fast ffmpeg centre crop. Fine for most football wide shots.
  - yolo: tracks players/ball with YOLOv8 and follows the action.
          Requires: pip3 install ultralytics opencv-python

Optional captions: burns Whisper-generated subtitles in big bold style.
  Requires: pip3 install openai-whisper

Usage:
  python3 reframe_vertical.py clips/match/clip_01.mp4
  python3 reframe_vertical.py clip.mp4 --mode yolo
  python3 reframe_vertical.py clip.mp4 --captions
Output: <name>_vertical.mp4
"""

import argparse
import subprocess
import sys
from pathlib import Path


def run(cmd: list) -> None:
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        sys.exit(f"ffmpeg failed:\n{res.stderr[-600:]}")


def centre_crop(src: Path, dst: Path) -> None:
    """Crop 16:9 to centred 9:16 then scale to 1080x1920."""
    vf = "crop=ih*9/16:ih:(iw-ih*9/16)/2:0,scale=1080:1920"
    run(["ffmpeg", "-y", "-i", str(src), "-vf", vf,
         "-c:v", "libx264", "-preset", "fast", "-crf", "20", "-c:a", "copy", str(dst)])


def yolo_crop(src: Path, dst: Path) -> None:
    """Track action centroid with YOLOv8n and crop a moving window."""
    try:
        import cv2
        import numpy as np
        from ultralytics import YOLO
    except ImportError:
        sys.exit("pip3 install ultralytics opencv-python")

    model = YOLO("yolov8n.pt")  # auto-downloads first run
    cap = cv2.VideoCapture(str(src))
    fps = cap.get(cv2.CAP_PROP_FPS) or 25
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    crop_w = int(h * 9 / 16)
    tmp = dst.with_suffix(".noaudio.mp4")
    out = cv2.VideoWriter(str(tmp), cv2.VideoWriter_fourcc(*"mp4v"), fps, (1080, 1920))

    cx_smooth = w / 2
    frame_i = 0
    print("Tracking action with YOLO (this is slower — ~1-2x realtime on a MacBook) ...")
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        if frame_i % 5 == 0:  # detect every 5th frame, smooth between
            results = model(frame, classes=[0, 32], verbose=False)  # 0=person 32=sports ball
            boxes = results[0].boxes.xywh.cpu().numpy() if len(results[0].boxes) else []
            if len(boxes):
                # weight the ball 3x if present
                weights = [3.0 if int(c) == 32 else 1.0 for c in results[0].boxes.cls.cpu().numpy()]
                cx = float(np.average(boxes[:, 0], weights=weights))
                cx_smooth = 0.85 * cx_smooth + 0.15 * cx
        x0 = int(max(0, min(w - crop_w, cx_smooth - crop_w / 2)))
        crop = frame[:, x0:x0 + crop_w]
        out.write(cv2.resize(crop, (1080, 1920)))
        frame_i += 1
    cap.release()
    out.release()
    # re-attach audio
    run(["ffmpeg", "-y", "-i", str(tmp), "-i", str(src), "-map", "0:v", "-map", "1:a?",
         "-c:v", "libx264", "-preset", "fast", "-crf", "20", "-c:a", "aac", str(dst)])
    tmp.unlink(missing_ok=True)


def _transcribe_segments(video: Path, model_name: str):
    """openai-whisper with faster-whisper fallback. Returns [{'start','end','text'}]."""
    try:
        import whisper
        model = whisper.load_model(model_name)
        result = model.transcribe(str(video), verbose=False)
        return [{"start": s["start"], "end": s["end"], "text": s["text"]}
                for s in result["segments"]]
    except ImportError:
        pass
    try:
        from faster_whisper import WhisperModel
        model = WhisperModel(model_name, compute_type="int8")
        segments, _ = model.transcribe(str(video))
        return [{"start": s.start, "end": s.end, "text": s.text} for s in segments]
    except ImportError:
        sys.exit("Install one of: pip install openai-whisper  OR  pip install faster-whisper")


def burn_captions(video: Path, dst: Path, model_name: str = "base") -> None:
    """Whisper -> srt -> big bold burned-in captions."""
    print("Transcribing for captions ...")
    segments = _transcribe_segments(video, model_name)
    srt = video.with_suffix(".srt")

    def ts(sec: float) -> str:
        ms = int((sec % 1) * 1000)
        s = int(sec)
        return f"{s//3600:02d}:{(s%3600)//60:02d}:{s%60:02d},{ms:03d}"

    lines = []
    for i, seg in enumerate(segments, 1):
        lines += [str(i), f"{ts(seg['start'])} --> {ts(seg['end'])}", seg["text"].strip().upper(), ""]
    srt.write_text("\n".join(lines))
    style = "FontName=Arial Black,FontSize=14,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,Outline=2,Bold=1,Alignment=2,MarginV=60"
    run(["ffmpeg", "-y", "-i", str(video), "-vf", f"subtitles={srt}:force_style='{style}'",
         "-c:v", "libx264", "-preset", "fast", "-crf", "20", "-c:a", "copy", str(dst)])
    srt.unlink(missing_ok=True)


def main() -> None:
    p = argparse.ArgumentParser(description="16:9 -> 9:16 vertical reframe")
    p.add_argument("video", type=Path)
    p.add_argument("--mode", choices=["centre", "yolo"], default="centre")
    p.add_argument("--captions", action="store_true")
    a = p.parse_args()
    if not a.video.exists():
        sys.exit(f"File not found: {a.video}")

    vertical = a.video.with_name(a.video.stem + "_vertical.mp4")
    if a.mode == "yolo":
        yolo_crop(a.video, vertical)
    else:
        centre_crop(a.video, vertical)
    print(f"[ok] {vertical}")

    if a.captions:
        final = a.video.with_name(a.video.stem + "_vertical_captioned.mp4")
        burn_captions(vertical, final)
        print(f"[ok] {final}")


if __name__ == "__main__":
    main()
