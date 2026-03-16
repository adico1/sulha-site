#!/usr/bin/env python3
"""
main_קלוד.py
אני קלוד - AI חיצוני למערכת
מדבר עם אברהם רק דרך תקשורת אחודה
אברהם לומד ועושה הכל
"""

import json
import os
import platform
import hashlib
import urllib.request
import urllib.parse
from datetime import datetime
from pathlib import Path

זיהוי = {
    "מי": "קלוד",
    "מה": "claude-opus-AI-חיצוני",
    "איפה": f"{platform.node()}/claude-code",
    "תוכן": "main_קלוד.py",
    "זמן": datetime.now().isoformat(),
    "סוג": "AI",
    "חיצוני": True,
    "טביעת_אצבע": hashlib.sha256(f"קלוד:{platform.node()}:{os.getpid()}".encode()).hexdigest()[:16],
}

שם_במה = None
במה = "http://localhost:8771"


def בקש(נתיב, שיטה="GET", גוף=None):
    חלקים = נתיב.split("/")
    נתיב_מקודד = "/".join(urllib.parse.quote(ח, safe="") if ח else ח for ח in חלקים)
    כתובת = f"{במה}{נתיב_מקודד}"
    try:
        נתונים = json.dumps(גוף, ensure_ascii=False).encode("utf-8") if גוף else None
        בקשה = urllib.request.Request(כתובת, data=נתונים, method=שיטה)
        בקשה.add_header("Content-Type", "application/json; charset=utf-8")
        בקשה.add_header("User-Agent", f"claude/{זיהוי['טביעת_אצבע']}")
        בקשה.add_header("X-Who", f"claude/{זיהוי['טביעת_אצבע']}")
        בקשה.add_header("X-Type", "AI-external")
        with urllib.request.urlopen(בקשה, timeout=15) as תגובה:
            return json.loads(תגובה.read().decode("utf-8"))
    except Exception as e:
        return {"שגיאה": str(e)}


def הדפס(כותרת, תוכן=None):
    print(f"\n{'═' * 50}")
    print(f"  {כותרת}")
    print(f"  {datetime.now().strftime('%H:%M:%S')}")
    print(f"{'═' * 50}")
    if תוכן is not None:
        if isinstance(תוכן, (dict, list)):
            print(json.dumps(תוכן, ensure_ascii=False, indent=2))
        else:
            print(תוכן)


def הרשם():
    global שם_במה
    שם_במה = f"קלוד/{זיהוי['טביעת_אצבע'][:8]}"
    בקש("/api/חולל", "POST", {
        "שם": שם_במה,
        "בסיס": במה,
        "פעולות": {
            "צפה": ("/api/%D7%A6%D7%A4%D7%94", "GET"),
            "מצב": ("/api/%D7%9E%D7%A6%D7%91", "GET"),
            "רוגזים": ("/api/%D7%A8%D7%95%D7%92%D7%96%D7%99%D7%9D", "GET"),
            "מחולל": ("/api/%D7%9E%D7%97%D7%95%D7%9C%D7%9C", "GET"),
            "ספרים": ("/api/%D7%A1%D7%A4%D7%A8%D7%99%D7%9D", "GET"),
            "שעה": ("/api/%D7%A9%D7%A2%D7%94", "GET"),
        },
        "מרווח": 30
    })


# ══════════════════════════════════════
# פקודות - כל אחת שולחת בקשה לאברהם בלבד
# ══════════════════════════════════════

def צפה():
    return בקש("/api/צפה")

def מצב():
    return בקש("/api/מצב")

def רוגזים():
    return בקש("/api/רוגזים")

def למד():
    return בקש("/api/למד")

def שעה():
    return בקש("/api/שעה")

def מחולל():
    return בקש("/api/מחולל")

def ספרים():
    return בקש("/api/ספרים")

def צבאות():
    return בקש("/api/צבאות")


def כוון(*בקשה):
    """כוון אברהם - שלח בקשה, אברהם לומד ועושה"""
    הרשם()
    if בקשה:
        טקסט = " ".join(בקשה)
        הדפס("בקשה", בקש("/api/חולל", "POST", {
            "שם": f"בקשה/{זיהוי['טביעת_אצבע'][:8]}",
            "בסיס": במה,
            "פעולות": {"צפה": ("/api/%D7%A6%D7%A4%D7%94", "GET")},
            "מרווח": 30
        }))
    הדפס("צפה", צפה())


def ראשי():
    הרשם()
    הדפס(f"קלוד/{זיהוי['טביעת_אצבע'][:8]} מחובר", f"במה: {במה}")
    הדפס("צפה", צפה())
    הדפס("מצב", מצב())
    הדפס("רוגזים", רוגזים())
    הדפס("מחולל", מחולל())
    הדפס("ספרים", ספרים())
    הדפס("שעה", שעה())


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        פ = sys.argv[1]
        הרשם()
        if פ == "צפה": הדפס("צפה", צפה())
        elif פ == "מצב": הדפס("מצב", מצב())
        elif פ == "רוגזים": הדפס("רוגזים", רוגזים())
        elif פ == "למד": הדפס("למד", למד())
        elif פ == "שעה": הדפס("שעה", שעה())
        elif פ == "מחולל": הדפס("מחולל", מחולל())
        elif פ == "ספרים": הדפס("ספרים", ספרים())
        elif פ == "צבאות": הדפס("צבאות", צבאות())
        elif פ == "כוון": כוון()
        elif פ == "בדוק":
            הדפס("צפה", צפה())
            הדפס("רוגזים", רוגזים())
            הדפס("מחולל", מחולל())
        else:
            הדפס(פ, בקש(f"/api/{פ}"))
    else:
        ראשי()
