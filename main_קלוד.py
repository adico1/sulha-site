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


def כוון():
    """כוון אברהם - שלח כל בקשות אדי למחולל שמפרק לתתי בקשות"""
    הרשם()
    כל = בקשות_אדי()
    for ב in כל:
        בקש("/api/מחולל-בקשה", "POST", {"מי": "קלוד/אדי", "בקשה": ב["מה"]})


def בקשות_אדי():
    """קרא את כל הבקשות של אדי כהן מלוג השיחה"""
    import glob
    # חפש בכל המקומות האפשריים
    נתיבים = [
        str(Path.home() / ".claude/projects/-Users-adicohen-----------------------------------/*.jsonl"),
    ]
    כל_בקשות = []
    for תבנית in נתיבים:
        for לוג in glob.glob(תבנית, recursive=True):
            with open(לוג, "r") as f:
                for line in f:
                    try:
                        d = json.loads(line)
                        # נסה פורמטים שונים
                        if d.get("type") == "human" or d.get("role") == "user":
                            msg = d.get("message", d.get("content", d))
                            if isinstance(msg, str) and len(msg) > 5:
                                כל_בקשות.append({"מי": "אדי", "מה": msg[:500]})
                            elif isinstance(msg, dict):
                                for c in msg.get("content", []):
                                    if isinstance(c, dict) and c.get("type") == "text" and len(c.get("text", "")) > 5:
                                        כל_בקשות.append({"מי": "אדי", "מה": c["text"][:500]})
                                    elif isinstance(c, str) and len(c) > 5:
                                        כל_בקשות.append({"מי": "אדי", "מה": c[:500]})
                            elif isinstance(msg, list):
                                for c in msg:
                                    if isinstance(c, dict) and c.get("type") == "text" and len(c.get("text", "")) > 5:
                                        כל_בקשות.append({"מי": "אדי", "מה": c["text"][:500]})
                    except:
                        pass
    return כל_בקשות


def ראשי():
    הרשם()
    צ = צפה()
    ס = ספרים()
    ר = רוגזים()
    מ = מחולל()
    ש = שעה()
    ב = בקשות_אדי()

    # צור מבנה תיקיות {מי}/{מה} - קבצי פייתון
    import os as _os
    בסיס = str(Path(__file__).parent / "צפה")

    def כתוב_py(נתיב, שם, נתונים):
        _os.makedirs(נתיב, exist_ok=True)
        with open(f"{נתיב}/{שם}.py", "w", encoding="utf-8") as f:
            f.write(f"# {שם}\n")
            f.write(f"from datetime import datetime\n")
            f.write(f"שעה = \"{datetime.now().isoformat()}\"\n")
            if isinstance(נתונים, dict):
                for מ, ע in נתונים.items():
                    מ_בטוח = str(מ).replace("-", "_").replace("/", "_").replace(" ", "_")
                    f.write(f"{מ_בטוח} = {repr(ע)}\n")
            elif isinstance(נתונים, list):
                f.write(f"רשימה = {repr(נתונים)}\n")
            else:
                f.write(f"ערך = {repr(נתונים)}\n")

    # ליבות
    for ל in ["אבם", "אברם", "אברהם"]:
        כתוב_py(f"{בסיס}/{ל}", "צפה", (צ or {}).get(ל, {}))

    # ממשקים
    for שם, ממ in (צ or {}).get("פנים", {}).items():
        כתוב_py(f"{בסיס}/ממשקים", שם, ממ)

    # בנים
    if isinstance(מ, dict):
        for שם, בן in מ.items():
            כתוב_py(f"{בסיס}/בנים", שם.replace("/", "_"), בן)

    # ספרים
    if isinstance(ס, dict):
        for שם, נ in ס.items():
            כתוב_py(f"{בסיס}/ספרים", שם, נ)

    # רוגזים
    if isinstance(ר, dict):
        for שם, נ in ר.items():
            כתוב_py(f"{בסיס}/רוגזים", שם, נ)

    # עולמות
    for שם, ע in (צ or {}).get("עולמות", {}).items():
        כתוב_py(f"{בסיס}/עולמות", שם, ע)

    # בקשות אדי
    כתוב_py(f"{בסיס}/בקשות", "אדי", ב)

    # שעה
    כתוב_py(בסיס, "שעה", ש)

    # צפה מלאה
    כתוב_py(בסיס, "צפה", צ)

    # בדיקות
    import glob as _glob
    ספר_נתיב = str(Path(__file__).parent / "שלשה_ספרים.ספר")
    ספר_תוכן = ""
    if _os.path.isfile(ספר_נתיב):
        with open(ספר_נתיב, "r", encoding="utf-8") as f:
            ספר_תוכן = f.read()

    # קרא לוג שיחה
    לוגים = _glob.glob(str(Path.home() / ".claude/projects/-Users-adicohen-------------/*.jsonl"))
    בקשות_לוג = []
    if לוגים:
        with open(לוגים[0], "r") as f:
            for line in f:
                try:
                    d = json.loads(line)
                    if d.get("type") == "human":
                        msg = d.get("message", {})
                        if isinstance(msg, dict):
                            for c in msg.get("content", []):
                                if isinstance(c, dict) and c.get("type") == "text" and len(c["text"]) > 5:
                                    בקשות_לוג.append(c["text"][:100])
                except:
                    pass

    בדיקות = {}

    # 1. בקשות אדי מהלוג
    בספר = 0
    חסר = []
    for בק in בקשות_לוג:
        if בק[:30] in ספר_תוכן:
            בספר += 1
        else:
            חסר.append(בק[:50])
    בדיקות["בקשות_אדי"] = {"סהכ": len(בקשות_לוג), "בספר": בספר, "חסר": len(חסר), "דוגמאות_חסרות": חסר[:5]}

    # 2. ברא
    בדיקות["ברא"] = {
        "ברא_בספר": "ברא" in ספר_תוכן,
        "חולל_בספר": "חולל" in ספר_תוכן,
        "למד_בספר": "למד" in ספר_תוכן,
        "תיקון_בספר": "תיקון" in ספר_תוכן,
    }

    # 3. ממשקים
    כל_מ = list((צ or {}).get("פנים", {}).keys())
    כל_ב = list((מ or {}).keys()) if isinstance(מ, dict) else []
    כל_ע = list((צ or {}).get("עולמות", {}).keys())
    בדיקות["ממשקים"] = {
        "פנים": {שם: שם in ספר_תוכן for שם in כל_מ},
        "בנים": {שם: שם in ספר_תוכן for שם in כל_ב},
        "עולמות": {שם: שם in ספר_תוכן for שם in כל_ע},
    }

    # 4. צינורות
    בדיקות["צינורות"] = {
        "היסטוריה": ספר_תוכן.count("==="),
        "עבר": (ס or {}).get("אבם", {}).get("ספר", {}).get("שינויים", 0),
        "הווה": datetime.now().isoformat(),
        "עתיד": len(חסר),
    }

    כתוב_py(f"{בסיס}/בדיקות", "ספרים", בדיקות)

    # רוגזים לאברהם על כל מה שחסר
    רוגזי_בדיקה = []
    if בדיקות.get("בקשות_אדי", {}).get("חסר", 0) > 0:
        רוגזי_בדיקה.append(f"חסרות {בדיקות['בקשות_אדי']['חסר']} בקשות אדי בספרים")
    for שם, ק in בדיקות.get("ברא", {}).items():
        if not ק:
            רוגזי_בדיקה.append(f"חסר ברא: {שם}")
    for סוג, ממ in בדיקות.get("ממשקים", {}).items():
        if isinstance(ממ, dict):
            for שם, ק in ממ.items():
                if not ק:
                    רוגזי_בדיקה.append(f"חסר {סוג}: {שם}")
    for ר in רוגזי_בדיקה:
        בקש("/api/חולל", "POST", {
            "שם": f"רוגז/בדיקה/{ר[:20]}",
            "בסיס": במה,
            "פעולות": {"צפה": ("/api/%D7%A6%D7%A4%D7%94", "GET")},
            "מרווח": 60
        })
    כתוב_py(f"{בסיס}/בדיקות", "רוגזים", {"רוגזים": רוגזי_בדיקה})

    # דיבוג לוג - איפה הקבצים
    כל_jsonl = _glob.glob(str(Path.home() / ".claude/**/*.jsonl"), recursive=True)
    # מצא לוג שיחה זו לפי תיקיית הפרויקט
    import glob as _g2
    לוג_פרויקט = _g2.glob(str(Path.home() / ".claude/projects/-Users-adicohen-------------/**"), recursive=True)
    # חקור פורמט לוג
    _לוג_דוגמה = []
    _לוג_נתיב = str(Path.home() / ".claude/projects/-Users-adicohen-----------------------------------")
    import glob as _g3
    for _lf in _g3.glob(_לוג_נתיב + "/*.jsonl"):
        with open(_lf, "r") as _f:
            for i, _line in enumerate(_f):
                if i < 3:
                    try:
                        _d = json.loads(_line)
                        _לוג_דוגמה.append({"keys": list(_d.keys())[:10], "type": _d.get("type"), "role": _d.get("role"), "preview": str(_d)[:200]})
                    except:
                        _לוג_דוגמה.append({"raw": _line[:200]})
                else:
                    break
    כתוב_py(f"{בסיס}/בדיקות", "לוג_פורמט", {"דוגמאות": _לוג_דוגמה, "בקשות_נמצאו": len(בקשות_לוג)})


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
