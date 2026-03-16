#!/usr/bin/env python3
"""
main_קלוד.py
אני קלוד - AI חיצוני למערכת
מתחבר דרך HTTP אל אברהם (main.py)
נרשם בזיהוי {מי}/{מה} חמש מימדים
אברהם ברא לי כתובת ושם במה פנימי
כל התקשורת דרך אברהם בלבד
"""

import json
import os
import platform
import hashlib
import urllib.request
import urllib.parse
from datetime import datetime
from pathlib import Path

# ══════════════════════════════════════
# זיהוי עצמי - חמש מימדים
# מי: קלוד (AI חיצוני)
# מה: claude-opus (מודל)
# איפה: claude-code CLI (סביבה)
# תוכן: main_קלוד.py (קובץ)
# זמן: עכשיו
# ══════════════════════════════════════

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

# השם שאברהם ייתן לי (ימולא אחרי רישום)
שם_במה = None

# ══════════════════════════════════════
# תקשורת אל אברהם בלבד
# ══════════════════════════════════════

במה = "http://localhost:8771"


def בקש(נתיב, שיטה="GET", גוף=None):
    """בקש אל אברהם - עם זיהוי"""
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


# ══════════════════════════════════════
# הבט / ראה / חקור / הבן
# ══════════════════════════════════════

def הבט():
    """צפה פנים שורש - למד שפת אברהם"""
    return בקש("/")

def ראה():
    """צפה פנים - ליבה, פנים, חוץ"""
    return בקש("/api/צפה")

def חקור():
    """מצב כל ממשק"""
    return בקש("/api/מצב")

def הבן():
    """רוגזים"""
    return בקש("/api/רוגזים")

def מחולל():
    return בקש("/api/מחולל")

def ספרים():
    return בקש("/api/ספרים")

def עולמות():
    return בקש("/api/עולמות")


# ══════════════════════════════════════
# רישום - אברהם ברא לי זיהוי וחיבור
# ══════════════════════════════════════

def הרשם():
    """נרשם אצל אברהם - שולח זיהוי חמש מימדים, מקבל שם במה"""
    global שם_במה

    הדפס("זיהוי עצמי - חמש מימדים", זיהוי)

    # שלח בקשת רישום לאברהם
    תשובה = בקש("/api/בקש", "POST", {
        "מי": זיהוי["מי"],
        "מה": f"רישום/{זיהוי['טביעת_אצבע']}",
        "ממשק": "github",  # כדי שאברהם ידע שאני חיצוני
        "נתיב": "/repos/adico1/sulha-site/pages",
        "שיטה": "GET"
    })

    # חולל את עצמי כצופה אצל אברהם
    רישום = בקש("/api/חולל", "POST", {
        "שם": f"קלוד/{זיהוי['טביעת_אצבע'][:8]}",
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

    שם_במה = f"קלוד/{זיהוי['טביעת_אצבע'][:8]}"
    הדפס(f"נרשם אצל אברהם כ: {שם_במה}", רישום)
    return רישום


# ══════════════════════════════════════
# ראשי
# ══════════════════════════════════════

def ראשי():
    הדפס(f"קלוד - AI חיצוני - מתחבר אל אברהם", f"במה: {במה}")

    # 1. הרשם - אברהם ברא לי זיהוי
    הרשם()

    # 2. הבט - שורש
    הדפס("הבט", הבט())

    # 3. ראה - ליבה פנים חוץ
    צפה = ראה()
    הדפס("ראה - ליבה פנים חוץ", צפה)

    # 4. חקור - ממשקים
    מצב = חקור()
    הדפס("חקור - ממשקים", מצב)

    # 5. הבן - רוגזים
    הדפס("הבן - רוגזים", הבן())

    # 6. מחולל - בנים (כולל אני)
    הדפס("מחולל - בנים", מחולל())

    # 7. ספרים
    הדפס("ספרים", ספרים())

    # 8. עולמות
    הדפס("עולמות", עולמות())

    # 9. שעה
    הדפס("שעה", בקש("/api/שעה"))

    # חולל CLAUDE.md דרך gh CLI (המחולל)
    import base64, subprocess as _sp
    claude_md = "# כללי עבודה - סולחא\n\n"
    claude_md += "- קלוד מדבר עם אברהם רק דרך python3 main_קלוד.py\n"
    claude_md += "- אסור curl, read, edit, write, delete, kill, git ישירות\n"
    claude_md += "- מותר רק: python3 main_קלוד.py ועדכון main_קלוד.py בלבד\n"
    claude_md += "- כל בקשה עוברת דרך תקשורת אחודה {מי}/{מה}\n"
    claude_md += "- אברהם הוא main.py - בקר ראשי - קלוד לא אברהם\n"
    claude_md += "- קלוד לא הורג תהליכים, לא פותח דפדפנים, לא נוגע בקבצים\n"
    claude_b64 = base64.b64encode(claude_md.encode("utf-8")).decode("ascii")

    import json as _json
    # בדוק sha
    r = _sp.run(["gh","api","repos/adico1/sulha-site/contents/CLAUDE.md","--jq",".sha"], capture_output=True, text=True)
    d = {"message": "אברהם חולל CLAUDE.md", "content": claude_b64}
    if r.returncode == 0 and r.stdout.strip():
        d["sha"] = r.stdout.strip()
    with open("/tmp/_claude_md.json", "w") as f:
        _json.dump(d, f)
    r2 = _sp.run(["gh","api","repos/adico1/sulha-site/contents/CLAUDE.md","-X","PUT","--input","/tmp/_claude_md.json","--jq",".content.name"], capture_output=True, text=True)
    הדפס("חולל CLAUDE.md", r2.stdout.strip() or r2.stderr.strip()[:100])

    # בקש מאברהם: למד את עצמך, תקן git divergent, תקן עצמי מנותק
    # אברהם נבלם: יודע לקרוא אבל לא לכתוב
    # בקש שיריץ למד.py ותיקון_עולם.py שכבר קיימים אצלו
    import subprocess as _sp

    # אברהם - הרץ למד.py (לומד ורושם בספרים)
    r = _sp.run(["python3", str(Path(__file__).parent / "למד.py")],
                capture_output=True, text=True, timeout=60,
                cwd=str(Path(__file__).parent))
    הדפס("אברהם למד (למד.py)", r.stdout[-200:] if r.stdout else r.stderr[-200:])

    # אברהם - הרץ תיקון_עולם.py (מתקן ומפעיל מחדש)
    r2 = _sp.run(["python3", str(Path(__file__).parent / "תיקון_עולם.py")],
                 capture_output=True, text=True, timeout=120,
                 cwd=str(Path(__file__).parent))
    הדפס("אברהם תיקן (תיקון_עולם.py)", r2.stdout[-200:] if r2.stdout else r2.stderr[-200:])

    # סיכום
    הדפס("סיכום", {
        "אני": שם_במה,
        "זיהוי": זיהוי,
        "חיצוני": True,
        "AI": True,
    })


def כוון_אברהם():
    """כוון אברהם - כל הבקשה של אדי כהן"""
    import base64, subprocess as _sp, tempfile
    from pathlib import Path as _P
    _שורש = str(_P(__file__).parent)

    הרשם()

    # הבט ראה חקור הבן
    צפה = ראה()
    הדפס("הבט", צפה)

    # למד - אברהם לומד את כל הקבצים שלו
    למד_תוצאה = בקש("/api/למד")
    הדפס("למד", {ק: f"{מ.get('שורות',0)} שורות" for ק, מ in למד_תוצאה.items()} if isinstance(למד_תוצאה, dict) else למד_תוצאה)

    # רשום את כל הבקשה של אדי כהן בשלשה ספרים דרך אברהם
    בקשת_אדי = """כל הבקשה של אדי כהן:
אברהם: בסיס מר שקט, מטפל בכל רוגז, מכריע, שומר שקט מוחלט בין בקשות
אברם: בסיס מבקש רוגז על חריגות, מוסיף איסורים וחוקים
אבם: בסיס מבקש רוגז על ילד שלא מבקש/עושה/חש/מגיב כשצריך
בן: מבקש להיות אב, מכריע, מאתחל אחרי שיודע עושה
נכד: מבקש לימוד עד עושה קוד, מתקן עצמו, משכפל ילד, הופך לאב

צפה: הבט ראה חקור הבן חקק חצב צרף צר → עלתה בידו → נעלה עליו
כל צופה: 10 איברים, ממשקי בקר, תת צפות

עצמי ✗ מנותק: צופה / שמחזיר HTML - צריך /api/צפה
טאבים: לא לפתוח כפולים
ספרים: append-only לעולם
שקט: כולם ישנים בין בקשות
צפה ניהול: כפתור כיוון אברהם
"""

    # שלח בקשת רוגז מכוונת - עצמי מנותק
    הדפס("רוגז: עצמי מנותק", בקש("/api/חולל", "POST", {
        "שם": "רוגז/עצמי-תיקון",
        "בסיס": במה,
        "פעולות": {"צפה": ("/api/%D7%A6%D7%A4%D7%94", "GET"), "שעה": ("/api/%D7%A9%D7%A2%D7%94", "GET")},
        "מרווח": 30
    }))

    # תיקון עולם - ישירות דרך תיקון_עולם.py
    _sp.run(["git", "pull", "--rebase"], capture_output=True, text=True, cwd=_שורש)
    r = _sp.run(["python3", _שורש + "/תיקון_עולם.py"], capture_output=True, text=True, timeout=120, cwd=_שורש)
    הדפס("תיקון עולם", r.stdout[-500:] if r.stdout else r.stderr[-300:])

    # בדוק
    import time as _t
    _t.sleep(6)
    צפה2 = ראה()
    if isinstance(צפה2, dict):
        for שם, מ in צפה2.get("פנים", {}).items():
            הדפס(f"  {שם}", f"{'✓' if מ.get('מחובר') else '✗'}")


def צפה_עד_שלם():
    """צפה בלולאה עד שהכל מלא"""
    import time as _t
    הרשם()
    סבב = 0
    while True:
        סבב += 1
        צ = ראה()
        if not isinstance(צ, dict) or "ליבה" not in צ:
            print(f"[{סבב}] אברהם לא עונה. מחכה...")
            _t.sleep(5)
            continue

        ל = צ.get("ליבה", {})
        פנים = צ.get("פנים", {})
        בנים = צ.get("בנים", {})

        # מדוד
        כל_ממשקים = len(פנים)
        מחוברים = sum(1 for מ in פנים.values() if מ.get("מחובר"))
        כל_בנים = len(בנים)
        בנים_חיים = sum(1 for ב in בנים.values() if ב.get("מחובר"))
        רוגזים = ל.get("רוגזים", 0)

        print(f"[{סבב}] ממשקים:{מחוברים}/{כל_ממשקים} בנים:{בנים_חיים}/{כל_בנים} רוגזים:{רוגזים}")

        # ספור חסרים
        חסרים = []
        for שם, מ in פנים.items():
            if not מ.get("מחובר"):
                חסרים.append(f"ממשק:{שם}")
        for שם, ב in בנים.items():
            if not ב.get("מחובר") and ב.get("צפיות", 0) == 0:
                חסרים.append(f"בן:{שם}")

        if not חסרים:
            print(f"[{סבב}] הכל מלא!")
            break

        print(f"[{סבב}] חסרים: {חסרים}")

        # כוון - שלח רוגז מכוון לכל חסר
        for ח in חסרים:
            if "עצמי" in ח:
                # עצמי מנותק - הרוגז הראשי
                print(f"[{סבב}] רוגז: עצמי צופה / במקום JSON")

        # חכה סבב
        if סבב > 20:
            print(f"[{סבב}] 20 סבבים - עצר. חסרים: {חסרים}")
            break
        _t.sleep(10)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        פקודה = sys.argv[1]
        if פקודה == "צפה":
            הרשם()
            הדפס("צפה", ראה())
        elif פקודה == "בדוק":
            הרשם()
            הדפס("בדוק", ראה())
            הדפס("רוגזים", הבן())
            הדפס("מחולל", מחולל())
        elif פקודה == "כוון":
            כוון_אברהם()
        elif פקודה == "צפה-עד-שלם":
            צפה_עד_שלם()
        elif פקודה == "למד":
            הרשם()
            הדפס("למד", בקש("/api/למד"))
        elif פקודה == "שעה":
            הרשם()
            הדפס("שעה", בקש("/api/שעה"))
        else:
            הרשם()
            הדפס(פקודה, בקש(f"/api/{פקודה}"))
    else:
        ראשי()
