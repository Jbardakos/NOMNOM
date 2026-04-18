# Installation Guide

## Option A — Pre-built app (easiest)

1. Go to [Releases](https://github.com/yourusername/nomnom/releases)
2. Download `NOMNOM.app.zip`
3. Unzip it
4. Drag `YTDL.app` to your `/Applications` folder
5. Install ffmpeg:
   ```bash
   brew install ffmpeg
   ```
6. Double-click `YTDL.app`

> If macOS says "cannot be opened because the developer cannot be verified":
> ```bash
> xattr -dr com.apple.quarantine /Applications/YTDL.app
> ```

---

## Option B — Build from source

### 1. Get the code

```bash
git clone https://github.com/yourusername/nomnom.git
cd nomnom
```

### 2. Install system dependencies

```bash
# Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Python 3.10+ and ffmpeg
brew install python ffmpeg
```

### 3. Build

```bash
chmod +x build.sh
./build.sh
```

This will:
- Create `venv/` with all Python dependencies (~350MB first time)
- Run PyInstaller
- Output `dist/YTDL.app`

### 4. Run

```bash
open dist/YTDL.app
```

---

## Verify ffmpeg

```bash
ffmpeg -version
```

If not found: `brew install ffmpeg`

ffmpeg is the **only** external dependency. Everything else (Python, PySide6, yt-dlp) is bundled inside the `.app`.

---

## Keep yt-dlp updated

YouTube changes its internals frequently. If downloads stop working:

**Pre-built app:** rebuild from source with latest yt-dlp.

**From source:**
```bash
source venv/bin/activate
pip install -U yt-dlp
# then rebuild:
./build.sh
```

---

## Uninstall

```bash
rm -rf /Applications/YTDL.app
```

Downloads remain in `~/Downloads/YTDL_*/` — delete manually if needed.
