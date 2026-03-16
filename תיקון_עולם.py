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
if __name__ == "__main__":
    print("תיקון עולם")
    for ק in sorted(os.listdir(שורש)):
        נ = os.path.join(שורש, ק)
        if os.path.isfile(נ) and not ק.startswith("."):
            with open(נ, "r", encoding="utf-8") as f: ת = f.read()
            רשום("אברהם/למד", ק, ת)
            print(f"  למד {ק}: {len(ת)}b")
    r = תקן("main.py", 'פעולות={"שורש": ("/", "GET")}', 'פעולות={"צפה": ("/api/%D7%A6%D7%A4%D7%94", "GET"), "שעה": ("/api/%D7%A9%D7%A2%D7%94", "GET")}')
    if r: print("  תוקן: עצמי צופה JSON"); רשום("אברהם/תיקון", "עצמי", "צופה JSON")
    r2 = תקן("main.py", "            if ש != \"עצמי\": מ.הפעל(60)", "            מ.הפעל(60)")
    if r2: print("  תוקן: עצמי מופעל"); רשום("אברהם/תיקון", "עצמי-פעיל", "הפעל עצמי")
    for cmd in [["git","add","-A"],["git","commit","-m","תיקון עולם"],["git","push"]]:
        subprocess.run(cmd, capture_output=True, text=True, timeout=30, cwd=שורש)
    print("  צבאות")
    for p in [8771, 8772]:
        try:
            r = subprocess.run(["lsof","-ti",f":{p}"], capture_output=True, text=True)
            for pid in r.stdout.strip().split(chr(10)):
                if pid and int(pid) != os.getpid(): os.kill(int(pid), 9)
        except: pass
    time.sleep(2)
    subprocess.Popen(["python3", os.path.join(שורש, "main.py")], cwd=שורש, start_new_session=True)
    print("  main.py הופעל מחדש")
