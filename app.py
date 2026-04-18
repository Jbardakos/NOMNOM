import sys, os, json, threading, platform
from pathlib import Path
from PySide6.QtCore import QObject, Slot, Signal
from PySide6.QtWidgets import QApplication, QFileDialog
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtCore import QUrl
import yt_dlp

BASE_DIR = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
UI_FILE = BASE_DIR / "ui" / "index.html"

class Backend(QObject):
    folderChanged = Signal(str)
    statusChanged = Signal(str)

    def __init__(self):
        super().__init__()
        self.download_dir = Path.home() / "Downloads" / "YTDL"

    def emit_status(self, data):
        self.statusChanged.emit(json.dumps(data, ensure_ascii=False))

    @Slot()
    def chooseFolder(self):
        folder = QFileDialog.getExistingDirectory(None, "Choose download folder", str(self.download_dir))
        if folder:
            self.download_dir = Path(folder)
            self.folderChanged.emit(str(self.download_dir))
            self.emit_status({
                "state":"item_done",
                "current":0,
                "total":0,
                "percent":0,
                "url":"Folder set: " + str(self.download_dir)
            })

    @Slot(result=str)
    def deviceInfo(self):
        return f"{platform.system()} {platform.machine()}"

    @Slot(result=str)
    def getCurrentFolder(self):
        return str(self.download_dir)

    @Slot(str)
    def startDownloads(self, urls_json):
        try:
            urls = json.loads(urls_json)
            if not isinstance(urls, list):
                raise ValueError("Bad URL payload")
        except Exception as e:
            self.emit_status({"state":"error","message":f"Invalid input: {e}"})
            return

        def worker():
            self.download_dir.mkdir(parents=True, exist_ok=True)
            total = len(urls)
            self.emit_status({"state":"starting","total":total})
            ok = 0
            fail = 0

            for i, url in enumerate(urls):
                current = i + 1

                def progress_hook(d, current=current, total=total, url=url):
                    status = d.get("status")
                    if status == "downloading":
                        pct_raw = d.get("_percent_str", "0%")
                        try:
                            percent = float(str(pct_raw).replace("%", "").strip())
                        except Exception:
                            percent = 0.0
                        self.emit_status({
                            "state":"running",
                            "current":current,
                            "total":total,
                            "percent":max(0, min(100, round(percent, 1))),
                            "url":url,
                            "speed": d.get("_speed_str", "") or "",
                            "eta": d.get("_eta_str", "") or ""
                        })
                    elif status == "finished":
                        self.emit_status({
                            "state":"running",
                            "current":current,
                            "total":total,
                            "percent":100,
                            "url":url,
                            "speed":"",
                            "eta":""
                        })

                ydl_opts = {
                    "outtmpl": str(self.download_dir / "%(title)s.%(ext)s"),
                    "progress_hooks": [progress_hook],
                    "noplaylist": False,
                    "quiet": True,
                    "no_warnings": True,
                    "restrictfilenames": False,
                }

                try:
                    self.emit_status({
                        "state":"running",
                        "current":current,
                        "total":total,
                        "percent":0,
                        "url":url,
                        "speed":"",
                        "eta":""
                    })
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([url])
                    ok += 1
                    self.emit_status({
                        "state":"item_done",
                        "current":current,
                        "total":total,
                        "percent":int((current/total)*100),
                        "url":url
                    })
                except Exception as e:
                    fail += 1
                    self.emit_status({
                        "state":"error",
                        "message":str(e)[:500],
                        "current":current,
                        "total":total,
                        "percent":int(((current-1)/total)*100) if total else 0,
                        "url":url
                    })

            self.emit_status({
                "state":"done",
                "ok":ok,
                "fail":fail,
                "dir":str(self.download_dir)
            })

        threading.Thread(target=worker, daemon=True).start()

def main():
    app = QApplication(sys.argv)
    backend = Backend()

    view = QWebEngineView()
    view.setWindowTitle("YTDL")
    view.resize(980, 760)

    channel = QWebChannel()
    channel.registerObject("backend", backend)
    view.page().setWebChannel(channel)
    view.load(QUrl.fromLocalFile(str(UI_FILE.resolve())))
    view.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
