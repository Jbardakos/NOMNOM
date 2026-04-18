# Changelog

All notable changes are documented here.

---

## [1.5.0] — 2025

### Added
- NOMNOM redesign — black/white bitmap aesthetic, Courier Prime + VT323 fonts
- Logo embedded directly in UI — no external asset loading
- ASCII block progress bar `[████████████        ] 67.3%`
- Per-URL queue with live status indicators (▶ active / ✓ done / ✗ fail)
- Folder picker — choose any download destination
- Font size slider — persists across sessions
- Error log — failed URLs shown with reason inline
- Device info display

### Changed
- UI rebuilt as single `ui/index.html` — all CSS/JS inline
- QWebChannel bridge rewritten with proper async init (`initChannel` retry loop)
- All DOM access null-safe (`setText` helper)
- yt-dlp used as Python library (bundled) — no external binary dependency

### Fixed
- `QWebChannel is not defined` — was firing before `qwebchannel.js` loaded
- `Cannot set properties of undefined` — DOM queries now null-checked

---

## [1.0.0] — Initial release

- PySide6 + QWebEngineView shell
- yt-dlp Python API integration
- Folder picker via `QFileDialog`
- Real-time progress via `progress_hook` → `Signal` → JS
- PyInstaller build pipeline
