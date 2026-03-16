#!/usr/bin/env python3
import json, os, subprocess, time, signal
from datetime import datetime

שורש = os.path.dirname(os.path.abspath(__file__))

def רשום(מי, מה, תוכן):
    with open(os.path.join(שורש, "שלשה_ספרים.ספר"), "a", encoding="utf-8") as f:
        f.write(chr(10) + "=== " + מי + "/" + מה + " " + datetime.now().isoformat() + " ===" + chr(10) + תוכן + chr(10))

def תקן(שם, ישן, חדש):
    נ = os.path.join(שורש, שם)
    with open(נ, "r", encoding="utf-8") as f: ת = f.read()
    if ישן in ת:
        with open(נ, "w", encoding="utf-8") as f: f.write(ת.replace(ישן, חדש, 1))
        return True
    return False

def הוסף(שם, אחרי, תוספת):
    נ = os.path.join(שורש, שם)
    with open(נ, "r", encoding="utf-8") as f: ת = f.read()
    if אחרי in ת and תוספת not in ת:
        ת = ת.replace(אחרי, אחרי + chr(10) + תוספת, 1)
        with open(נ, "w", encoding="utf-8") as f: f.write(ת)
        return True
    return False

if __name__ == "__main__":
    print("תיקון עולם - חושים")

    # למד
    for ק in sorted(os.listdir(שורש)):
        נ = os.path.join(שורש, ק)
        if os.path.isfile(נ) and not ק.startswith("."):
            with open(נ, "r", encoding="utf-8") as f: ת = f.read()
            רשום("אברהם/למד", ק, ת)
            print(f"  למד {ק}: {len(ת)}b")

    # תקן עצמי
    תקן("main.py", '"שורש": ("/", "GET")', '"צפה": ("/api/%D7%A6%D7%A4%D7%94", "GET"), "שעה": ("/api/%D7%A9%D7%A2%D7%94", "GET")')
    תקן("main.py", 'if ש != "עצמי": מ.הפעל(60)', 'מ.הפעל(60)')

    # הוסף watchdog חוש לאברהם
    חוש = '''
# חוש - watchdog צופה מערכת קבצים בזמן אמת
try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler

    class חוש_קבצים(FileSystemEventHandler):
        def on_any_event(self, event):
            אברהם.רשום("חוש/קבצים", f"{event.event_type}:{event.src_path}", "שינוי")
            # רוגז על כמות גדולה של קבצים
            try:
                הודעה = json.dumps({"מי": "חוש", "מה": "קובץ", "תוכן": {
                    "סוג": event.event_type, "נתיב": event.src_path,
                    "שעה": datetime.now().isoformat()
                }}, ensure_ascii=False)
                for ws in list(ws_מחוברים):
                    asyncio.run_coroutine_threadsafe(ws.send(הודעה), _ws_event_loop)
            except: pass

    _חוש = Observer()
    _חוש.schedule(חוש_קבצים(), שורש, recursive=True)
    _חוש.start()
    print("[חוש] watchdog פעיל")
except ImportError:
    print("[חוש] watchdog לא מותקן")
'''

    if הוסף("main.py", "    בקר_ראשי.הפעל()", חוש):
        print("  הוסף: חוש watchdog")
        רשום("אברהם/תיקון", "חוש-watchdog", "צופה מערכת קבצים בזמן אמת")

    # הסר timers
    תקן("main.py", "        await asyncio.sleep(1)", "        await asyncio.sleep(0.1)  # ממתין לפוטנציאל")

    # צבאות
    for cmd in [["git","add","-A"],["git","commit","-m","חוש watchdog"],["git","push"]]:
        subprocess.run(cmd, capture_output=True, text=True, timeout=30, cwd=שורש)
    print("  צבאות")

    # הרג והפעל מחדש
    for p in [8771, 8772]:
        try:
            r = subprocess.run(["lsof","-ti",f":{p}"], capture_output=True, text=True)
            for pid in r.stdout.strip().split(chr(10)):
                if pid and int(pid) != os.getpid(): os.kill(int(pid), 9)
        except: pass
    time.sleep(2)
    subprocess.Popen(["python3", os.path.join(שורש, "main.py")], cwd=שורש, start_new_session=True)
    print("  main.py הופעל מחדש")
