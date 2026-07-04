# Installation Guide

## Option A — Pre-built app (easiest, nothing else to install)

ffmpeg and yt-dlp are bundled inside the app. No Homebrew, no terminal, no dependencies.

1. Go to [Releases](https://github.com/Jbardakos/NOMNOM/releases)
2. Download the file for your machine:

   | Your machine | File |
   |---|---|
   | Mac, Apple Silicon (M1/M2/M3/M4) | `NOMNOM-macos-applesilicon.zip` |
   | Mac, Intel | `NOMNOM-macos-intel.zip` |
   | Windows 10/11 | `NOMNOM-windows.zip` |

3. **macOS:** unzip, drag `NOMNOM.app` to `/Applications`, then on first launch **right-click → Open → Open** (needed once — the app is not notarized).

   > If macOS still says "cannot be opened because the developer cannot be verified":
   > ```bash
   > xattr -dr com.apple.quarantine /Applications/NOMNOM.app
   > ```

4. **Windows:** unzip, open the `NOMNOM` folder, double-click `NOMNOM.exe`.

   > If SmartScreen warns, click **More info → Run anyway** (the app is unsigned).

---

## Option B — Build from source (macOS)

### 1. Get the code

```bash
git clone https://github.com/Jbardakos/NOMNOM.git
cd NOMNOM
```

### 2. Install system dependencies

```bash
# Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Python 3.10+
brew install python
```

### 3. Build

```bash
chmod +x build.sh
./build.sh
```

This will:
- Create `venv/` with all Python dependencies (~350MB first time)
- Run PyInstaller
- Output `dist/NOMNOM.app` with ffmpeg bundled inside

### 4. Run

```bash
open dist/NOMNOM.app
```

---

## Keep yt-dlp updated

YouTube changes its internals frequently. If downloads stop working:

**Pre-built app:** download the newest release — each release is built with the latest yt-dlp.

**From source:**
```bash
source venv/bin/activate
pip install -U yt-dlp
# then rebuild:
./build.sh
```

---

## Uninstall

**macOS:**
```bash
rm -rf /Applications/NOMNOM.app
```

**Windows:** delete the `NOMNOM` folder.

Downloads remain in `~/Downloads/NOMNOM/` — delete manually if needed.
