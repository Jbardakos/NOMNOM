<div align="center">

![NOMNOM](ui/logo.png)

# NOMNOM — Nyarlathotep Downloader

**YouTube bulk downloader. Paste anything. Download everything.**

*Vibed by [Iannis Bardakos](https://www.johnbardakos.com)*

[![Release](https://img.shields.io/github/v/release/Jbardakos/NOMNOM?style=flat-square&color=white&labelColor=000)](https://github.com/Jbardakos/NOMNOM/releases)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Windows-white?style=flat-square&labelColor=000)](https://github.com/Jbardakos/NOMNOM/releases)
[![Python](https://img.shields.io/badge/python-3.10+-white?style=flat-square&labelColor=000)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-white?style=flat-square&labelColor=000)](LICENSE)

</div>

---

## What it does

Paste any blob of text — a chat log, a browser history export, a list of links. NOMNOM extracts every YouTube URL automatically and downloads them all as best-quality MP4s.

---

## Quick Start (pre-built app — nothing else to install)

ffmpeg and yt-dlp are **bundled inside the app**. No Homebrew, no terminal, no dependencies.

1. Grab the file for your machine from [Releases](https://github.com/Jbardakos/NOMNOM/releases):

   | Your machine | File |
   |---|---|
   | Mac, Apple Silicon (M1/M2/M3/M4) | `NOMNOM-macos-applesilicon.zip` |
   | Mac, Intel | `NOMNOM-macos-intel.zip` |
   | Windows 10/11 | `NOMNOM-windows.zip` |

2. **macOS:** unzip, drag `NOMNOM.app` to Applications, then **right-click → Open → Open** on first launch (the app is not notarized).
   **Windows:** unzip, open the `NOMNOM` folder, run `NOMNOM.exe`. If SmartScreen warns, click **More info → Run anyway**.

> **macOS still blocked it?**
> ```bash
> xattr -dr com.apple.quarantine /Applications/NOMNOM.app
> ```

---

## Build from source

### Prerequisites

```bash
# Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Python 3.10+
brew install python
```

### Build

```bash
git clone https://github.com/Jbardakos/NOMNOM.git
cd NOMNOM
chmod +x build.sh
./build.sh
```

Output: `dist/NOMNOM.app`

```bash
open dist/NOMNOM.app
```

### What `build.sh` does

1. Creates a Python virtual environment (`venv/`)
2. Installs `PySide6`, `yt-dlp`, `imageio-ffmpeg`, `pyinstaller`
3. Runs PyInstaller — bundles Python, ffmpeg, and all dependencies into a self-contained `.app`
4. The `ui/` folder (HTML interface) is included in the bundle

---

## Project structure

```
nomnom/
├── app.py              ← Main Python app (PySide6 + QWebEngine + yt-dlp)
├── build.sh            ← One-command build script
├── requirements.txt    ← Python dependencies
├── ui/
│   └── index.html      ← Full UI (HTML/CSS/JS, talks to app.py via QWebChannel)
└── README.md
```

---

## How it works

```
┌─────────────────────────────────────────────┐
│              ui/index.html                  │
│  paste → extract URLs → queue → progress   │
│         QWebChannel (JS ↔ Python)           │
└──────────────┬──────────────────────────────┘
               │ backend.startDownloads([urls])
               ▼
┌─────────────────────────────────────────────┐
│                 app.py                      │
│  yt_dlp.YoutubeDL → progress_hook → Signal │
│  statusChanged.emit(json) → UI updates     │
└─────────────────────────────────────────────┘
               │
               ▼
   ~/Downloads/NOMNOM/
   └── Video Title.mp4
```

- **No server.** No polling. No HTTP tricks. PySide6 `Signal/Slot` pushes progress directly to the WebView in real time.
- **yt-dlp is bundled** as a Python library — no external binary needed.
- **ffmpeg is bundled too** (via `imageio-ffmpeg`) — best-quality video+audio merging works out of the box, with system ffmpeg as fallback.

---

## Stack

| Component | Technology |
|-----------|-----------|
| App shell | PySide6 (Qt6) |
| Web view  | QWebEngineView |
| IPC       | QWebChannel (JS ↔ Python) |
| Downloader| yt-dlp Python API |
| Packaging | PyInstaller |
| UI        | HTML · CSS · Vanilla JS |

---

## Troubleshooting

**Downloads fail silently**
YouTube changes frequently and yt-dlp patches fast — download the newest NOMNOM release.
> If you built from source, update the library and rebuild:
> ```bash
> source venv/bin/activate && pip install -U yt-dlp && ./build.sh
> ```

**App won't open (Apple quarantine)**
Right-click the app → Open → Open. If that fails:
```bash
xattr -dr com.apple.quarantine /Applications/NOMNOM.app
```

**Slow build / Qt download**
PySide6 is ~300MB. The first build downloads it once; subsequent builds use the cached `venv/`.

---

## License

MIT — do whatever you want with it.

---

<div align="center">
<sub>NOMNOM // Nyarlathotep Downloader // Vibed by Iannis Bardakos</sub>
</div>
