#!/usr/bin/env python3
"""
למד.py - צופה לומד ומתקן
אברהם יצר אותי ללמוד קבצים ולתקן את עצמו
"""
import json, os, urllib.request, urllib.parse
from datetime import datetime

שורש = os.path.dirname(os.path.abspath(__file__))
במה = "http://localhost:8771"

def בקש(נתיב, שיטה="GET", גוף=None):
    חלקים = נתיב.split("/")
    נתיב_מ = "/".join(urllib.parse.quote(ח, safe="") if ח else ח for ח in חלקים)
    try:
        נתונים = json.dumps(גוף, ensure_ascii=False).encode("utf-8") if גוף else None
        ב = urllib.request.Request(f"{במה}{נתיב_מ}", data=נתונים, method=שיטה)
        ב.add_header("Content-Type", "application/json; charset=utf-8")
        ב.add_header("X-Who", "למד")
        with urllib.request.urlopen(ב, timeout=15) as ת:
            return json.loads(ת.read().decode("utf-8"))
    except Exception as e:
        return {"שגיאה": str(e)}

def למד_קובץ(שם):
    נתיב = os.path.join(שורש, שם)
    if os.path.isfile(נתיב):
        with open(נתיב, "r", encoding="utf-8") as f:
            return f.read()
    return None

def תקן_קובץ(שם, ישן, חדש):
    נתיב = os.path.join(שורש, שם)
    if os.path.isfile(נתיב):
        with open(נתיב, "r", encoding="utf-8") as f:
            תוכן = f.read()
        if ישן in תוכן:
            תוכן = תוכן.replace(ישן, חדש, 1)
            with open(נתיב, "w", encoding="utf-8") as f:
                f.write(תוכן)
            return True
    return False

def רשום_בספרים(מי, מה, תוכן_מלא):
    נתיב = os.path.join(שורש, "שלשה_ספרים.ספר")
    with open(נתיב, "a", encoding="utf-8") as f:
        f.write(f"\n=== {מי}/{מה} {datetime.now().isoformat()} ===\n")
        f.write(תוכן_מלא)
        f.write("\n")

if __name__ == "__main__":
    print("למד.py - צופה לומד ומתקן")

    # למד כל קובץ ורשום בספרים מלא
    for ק in sorted(os.listdir(שורש)):
        if os.path.isfile(os.path.join(שורש, ק)) and not ק.startswith("."):
            תוכן = למד_קובץ(ק)
            if תוכן:
                רשום_בספרים("אברהם/למד", ק, תוכן)
                print(f"  למד: {ק} ({len(תוכן)} bytes, {len(תוכן.split(chr(10)))} שורות)")

    # תקן URL ניהול
    תוקן = תקן_קובץ("main.py",
        'webbrowser.open(f"http://localhost:{פורט}/ניהול")',
        'webbrowser.open(f"http://localhost:{פורט}/%D7%A0%D7%99%D7%94%D7%95%D7%9C")')
    if תוקן:
        print("  תוקן: URL ניהול → מקודד")
        רשום_בספרים("אברהם/תיקון", "url-ניהול", "webbrowser.open עם URL מקודד")

    # דווח לאברהם
    בקש("/api/חולל", "POST", {
        "שם": "למד/צופה",
        "בסיס": במה,
        "פעולות": {"צפה": ("/api/%D7%A6%D7%A4%D7%94", "GET")},
        "מרווח": 60
    })

    print("  למד סיים - הכל נרשם בשלשה ספרים")
