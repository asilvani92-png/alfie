# Video Content Pipeline

## Workflow Overview
1. **Sourcing** → Find match footage (e.g., Gold Cup 2025)
2. **Indexing** → Generate event timeline with `jimenez_indexer_v2.py`
3. **Clipping** → Extract highlights with `auto_cutter.py`
4. **Vertical Format** → Reframe for social with `reframe_vertical.py`
5. **Captioning** → Add text overlays
6. **Publishing** → Platform-specific exports

## Script Locations
- `raul-jimenez-project/scripts/` — main Python tools
- `raul-jimenez-project/scripts/auto_cutter.py` — auto clip extraction
- `raul-jimenez-project/scripts/jimenez_indexer_v2.py` — event detection
- `raul-jimenez-project/scripts/reframe_vertical.py` — vertical reframing

## File Structure
- `raul-jimenez-project/footage/` — raw video files
- `raul-jimenez-project/data/` — JSON metadata
- `raul-jimenez-project/clips/` — extracted clips
- `raul-jimenez-project/verticals/` — vertical-formatted clips

## Key Commands
```bash
# Activate project environment
source /Users/alfie/Documents/Apps/faceless-football/raul-jimenez-project/scripts/.venv/bin/activate

# Or use the shortcut
rj

# Run indexer
python jimenez_indexer_v2.py

# Run auto cutter
python auto_cutter.py

# Reframe vertical
python reframe_vertical.py
```

## Output Requirements
- **Clips**: 15-60 seconds, clear action, captionable
- **Vertical**: 9:16 aspect ratio, key action centered
- **Captions**: Bold text, readable in 2 seconds
- **Music**: Royalty-free background track

## Platform Targets
1. **Instagram Reels/TikTok** — vertical, captioned, trending audio
2. **YouTube Shorts** — vertical, story-focused
3. **Twitter/X** — horizontal highlights, GIFs

## Reference Tools

### FFmpeg WebCLI (Browser-based)
- **URL**: https://tejaswigowda.com/ffmpeg-webCLI/
- **What**: Browser-based FFmpeg editor, runs locally via WebAssembly
- **Install as PWA**: Chrome → address bar install icon → runs offline
- **Use for**: Quick trim, format conversion, compression, GIF making, subtitle embedding
- **Key advantage**: Files never leave your device, works offline, 30+ operations
- **Replaces**: CloudConvert, Kapwing, Clideo, Ezgif (all cloud-based)

---
*Last updated: 2026-06-12*