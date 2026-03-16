#!/usr/bin/env python3
import json, os, urllib.request, urllib.parse, subprocess, time, signal
from datetime import datetime

שורש = os.path.dirname(os.path.abspath(__file__))
במה = "http://localhost:8771"

def בקש(נ, ש="GET", ג=None):
    ח = נ.split("/")
    נמ = "/".join(urllib.parse.quote(x, safe="") if x else x for x in ח)
    try:
        נת = json.dumps(ג, ensure_ascii=False).encode("utf-8") if ג else None
        ב = urllib.request.Request(f"{במה}{נמ}", data=נת, method=ש)
        ב.add_header("Content-Type", "application/json; charset=utf-8")
        with urllib.request.urlopen(ב, timeout=15) as ת:
            return json.loads(ת.read().decode("utf-8"))
    except Exception as e:
        return {"error": str(e)}

def רשום(מי, מה, תוכן):
    with open(os.path.join(שורש, "שלשה_ספרים.ספר"), "a", encoding="utf-8") as f:
        f.write(chr(10) + "=== " + מי + "/" + מה + " " + datetime.now().isoformat() + " ===" + chr(10) + תוכן + chr(10))

def תקן(שם, ישן, חדש):
    נ = os.path.join(שורש, שם)
    with open(נ, "r", encoding="utf-8") as f:
        ת = f.read()
    if ישן in ת:
        with open(נ, "w", encoding="utf-8") as f:
            f.write(ת.replace(ישן, חדש, 1))
        return True
    return False

if __name__ == "__main__":
    print("תיקון עולם")

    # למד כל קבצים
    for ק in sorted(os.listdir(שורש)):
        נ = os.path.join(שורש, ק)
        if os.path.isfile(נ) and not ק.startswith("."):
            with open(נ, "r", encoding="utf-8") as f:
                ת = f.read()
            רשום("אברהם/למד", ק, ת)
            print(f"  למד {ק}: {len(ת)}b")

    # תקן main.py - הוסף /api/למד אם חסר
    with open(os.path.join(שורש, "main.py"), "r", encoding="utf-8") as f:
        main = f.read()

    if "/api/למד" not in main:
        bloc = '        elif נ == "/api/למד":\n'
        bloc += '            קמ = {}\n'
        bloc += '            for ק in os.listdir(שורש):\n'
        bloc += '                נק = os.path.join(שורש, ק)\n'
        bloc += '                if os.path.isfile(נק) and not ק.startswith("."):\n'
        bloc += '                    try:\n'
        bloc += '                        with open(נק, "r", encoding="utf-8") as f: תק = f.read()\n'
        bloc += '                        קמ[ק] = {"שורות": len(תק.split(chr(10))), "אורך": len(תק)}\n'
        bloc += '                        אברהם.רשום("למד", "קובץ:" + ק, "ענה")\n'
        bloc += '                    except: pass\n'
        bloc += '            self._json(קמ)\n'

        old = '        # catch all\n        else:'
        new = bloc + '        # catch all\n        else:'
        if תקן("main.py", old, new):
            print("  תוקן: הוסף /api/למד")
            רשום("אברהם/תיקון", "api-למד", "endpoint למידה")

    # צבאות
    for cmd in [["git","add","-A"],["git","commit","-m","תיקון עולם"],["git","push"]]:
        subprocess.run(cmd, capture_output=True, text=True, timeout=30, cwd=שורש)
    print("  צבאות")

    # הרג ישן והפעל מחדש
    for p in [8771, 8772]:
        try:
            r = subprocess.run(["lsof","-ti",f":{p}"], capture_output=True, text=True)
            for pid in r.stdout.strip().split(chr(10)):
                if pid: os.kill(int(pid), signal.SIGKILL)
        except: pass
    time.sleep(2)

    subprocess.Popen(["python3", os.path.join(שורש, "main.py")], cwd=שורש, start_new_session=True)
    print("  main.py הופעל מחדש")
    time.sleep(5)

    # בדוק
    צפה = בקש("/api/צפה")
    if isinstance(צפה, dict) and "ליבה" in צפה:
        print(f"  ליבה: {צפה['ליבה']}")
    else:
        print(f"  {צפה}")

    print("סיים")
