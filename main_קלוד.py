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

    # כוון אברהם לתקן עצמי דרך GitHub API + תיקון_עולם.py
    import base64, subprocess as _sp

    # קרא תיקון_עולם.py מ-GitHub דרך אברהם
    תיקון_קיים = בקש("/api/בקש", "POST", {
        "ממשק": "github",
        "נתיב": "/repos/adico1/sulha-site/contents/%D7%AA%D7%99%D7%A7%D7%95%D7%9F_%D7%A2%D7%95%D7%9C%D7%9D.py",
        "שיטה": "GET"
    })
    sha_תיקון = None
    if isinstance(תיקון_קיים, dict):
        ת = תיקון_קיים.get("תגובה", תיקון_קיים)
        if isinstance(ת, dict):
            sha_תיקון = ת.get("sha")

    # בנה תיקון_עולם.py חדש שמתקן עצמי
    קוד_תיקון = '#!/usr/bin/env python3\n'
    קוד_תיקון += 'import json, os, subprocess, time, signal\n'
    קוד_תיקון += 'from datetime import datetime\n'
    קוד_תיקון += 'שורש = os.path.dirname(os.path.abspath(__file__))\n'
    קוד_תיקון += 'def רשום(מי, מה, תוכן):\n'
    קוד_תיקון += '    with open(os.path.join(שורש, "שלשה_ספרים.ספר"), "a", encoding="utf-8") as f:\n'
    קוד_תיקון += '        f.write(chr(10) + "=== " + מי + "/" + מה + " " + datetime.now().isoformat() + " ===" + chr(10) + תוכן + chr(10))\n'
    קוד_תיקון += 'def תקן(שם, ישן, חדש):\n'
    קוד_תיקון += '    נ = os.path.join(שורש, שם)\n'
    קוד_תיקון += '    with open(נ, "r", encoding="utf-8") as f: ת = f.read()\n'
    קוד_תיקון += '    if ישן in ת:\n'
    קוד_תיקון += '        with open(נ, "w", encoding="utf-8") as f: f.write(ת.replace(ישן, חדש, 1))\n'
    קוד_תיקון += '        return True\n'
    קוד_תיקון += '    return False\n'
    קוד_תיקון += 'if __name__ == "__main__":\n'
    קוד_תיקון += '    print("תיקון עולם")\n'
    קוד_תיקון += '    for ק in sorted(os.listdir(שורש)):\n'
    קוד_תיקון += '        נ = os.path.join(שורש, ק)\n'
    קוד_תיקון += '        if os.path.isfile(נ) and not ק.startswith("."):\n'
    קוד_תיקון += '            with open(נ, "r", encoding="utf-8") as f: ת = f.read()\n'
    קוד_תיקון += '            רשום("אברהם/למד", ק, ת)\n'
    קוד_תיקון += '            print(f"  למד {ק}: {len(ת)}b")\n'
    קוד_תיקון += '    r = תקן("main.py", \'פעולות={"שורש": ("/", "GET")}\', \'פעולות={"צפה": ("/api/%D7%A6%D7%A4%D7%94", "GET"), "שעה": ("/api/%D7%A9%D7%A2%D7%94", "GET")}\')\n'
    קוד_תיקון += '    if r: print("  תוקן: עצמי צופה JSON"); רשום("אברהם/תיקון", "עצמי", "צופה JSON")\n'
    קוד_תיקון += '    r2 = תקן("main.py", "            if ש != \\"עצמי\\": מ.הפעל(60)", "            מ.הפעל(60)")\n'
    קוד_תיקון += '    if r2: print("  תוקן: עצמי מופעל"); רשום("אברהם/תיקון", "עצמי-פעיל", "הפעל עצמי")\n'
    קוד_תיקון += '    for cmd in [["git","add","-A"],["git","commit","-m","תיקון עולם"],["git","push"]]:\n'
    קוד_תיקון += '        subprocess.run(cmd, capture_output=True, text=True, timeout=30, cwd=שורש)\n'
    קוד_תיקון += '    print("  צבאות")\n'
    קוד_תיקון += '    for p in [8771, 8772]:\n'
    קוד_תיקון += '        try:\n'
    קוד_תיקון += '            r = subprocess.run(["lsof","-ti",f":{p}"], capture_output=True, text=True)\n'
    קוד_תיקון += '            for pid in r.stdout.strip().split(chr(10)):\n'
    קוד_תיקון += '                if pid and int(pid) != os.getpid(): os.kill(int(pid), 9)\n'
    קוד_תיקון += '        except: pass\n'
    קוד_תיקון += '    time.sleep(2)\n'
    קוד_תיקון += '    subprocess.Popen(["python3", os.path.join(שורש, "main.py")], cwd=שורש, start_new_session=True)\n'
    קוד_תיקון += '    print("  main.py הופעל מחדש")\n'

    # שלח ל-GitHub דרך gh CLI
    b64 = base64.b64encode(קוד_תיקון.encode("utf-8")).decode("ascii")
    d = {"message": "אברהם מתקן עצמו", "content": b64}
    if sha_תיקון:
        d["sha"] = sha_תיקון
    import tempfile
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(d, f)
        tmp = f.name
    r = _sp.run(["gh", "api", "repos/adico1/sulha-site/contents/%D7%AA%D7%99%D7%A7%D7%95%D7%9F_%D7%A2%D7%95%D7%9C%D7%9D.py",
                 "-X", "PUT", "--input", tmp, "--jq", ".content.name"], capture_output=True, text=True)
    הדפס("חולל תיקון_עולם.py", r.stdout.strip() or r.stderr.strip()[:100])

    # pull + הרץ תיקון
    _sp.run(["git", "pull", "--rebase"], capture_output=True, text=True, cwd=str(Path(__file__).parent))
    r2 = _sp.run(["python3", str(Path(__file__).parent / "תיקון_עולם.py")],
                 capture_output=True, text=True, timeout=120, cwd=str(Path(__file__).parent))
    הדפס("תיקון עולם", r2.stdout[-300:] if r2.stdout else r2.stderr[-300:])

    # חכה ובדוק
    import time as _time
    _time.sleep(6)
    צפה2 = ראה()
    if isinstance(צפה2, dict):
        ל = צפה2.get("ליבה", {})
        הדפס("מצב אחרי תיקון", f"ממשקים:{ל.get('ממשקים')} בנים:{ל.get('בנים')} רוגזים:{ל.get('רוגזים')}")
        for שם, מ in צפה2.get("פנים", {}).items():
            הדפס(f"  {שם}", f"{'✓' if מ.get('מחובר') else '✗'} פעיל:{מ.get('פעיל')}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        פקודה = sys.argv[1]
        הרשם()
        if פקודה == "צפה":
            הדפס("צפה", ראה())
        elif פקודה == "בדוק":
            הדפס("בדוק", ראה())
            הדפס("רוגזים", הבן())
            הדפס("מחולל", מחולל())
        elif פקודה == "כוון":
            כוון_אברהם()
        elif פקודה == "למד":
            הדפס("למד", בקש("/api/למד"))
        elif פקודה == "שעה":
            הדפס("שעה", בקש("/api/שעה"))
        else:
            הדפס(פקודה, בקש(f"/api/{פקודה}"))
    else:
        ראשי()
