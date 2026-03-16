#!/usr/bin/env python3
"""
ממיר.ספר.החוקים.py

אדון הכל = אברהם = אברם מתגבש לאברהם

ספר החוקים:
- ק"ק חק (10,000 חוקים)
- לכל חק: קול ורוח
- מפרט דיבור לדבר
- מין למינו

הלוך ורצוא ורצוא ושוב:
- חק → 1/10000 תת-חק
- תת-חק → חק

צפה וממיר:
- צפה: מזהה מקולקל
- ממיר: מתקן

איסורים:
- no 3rd party
"""

from pathlib import Path

BASE = Path(__file__).parent
AIN_DIR = BASE / "אין"
HUKIM_DIR = BASE / "חוקים"

# =============================================================================
# חק - קול ורוח
# =============================================================================

def extract_kol(ai):
    """
    קול - הצד הנשמע של החק
    מה שמדובר
    """
    mah = ai.get('מה', '')
    makor = ai.get('מקור', '')

    # קול = השם + המקור
    kol = f"{mah} מ{makor}" if makor else mah
    return kol


def extract_ruach(ai):
    """
    רוח - הצד הרוחני של החק
    מה שמכוון
    """
    # רוח = הכוונה/התפקיד
    sur = ai.get('סור', 'נעול')
    mah = ai.get('מה', '')

    # זהה סוג
    if mah.startswith('עומק'):
        ruach = 'ספירה - מימד'
    elif mah.startswith('אות'):
        ruach = 'אות - כלי'
    elif mah.startswith('שער'):
        ruach = 'שער - חיבור'
    elif mah.startswith('בית'):
        ruach = 'בית - צירוף'
    elif mah.startswith('גלגל'):
        ruach = 'גלגל - סיבוב'
    elif mah.startswith('יוצר'):
        ruach = 'יוצר - שליטה'
    elif mah.startswith('קצה'):
        ruach = 'קצה - גבול'
    elif mah.startswith('אבם'):
        ruach = 'אבם - ממשק'
    else:
        ruach = 'יחידה - חלק'

    return f"{ruach} ({sur})"


def create_hok(ai, hok_id):
    """
    צור חק מאי
    """
    return {
        'id': hok_id,
        'מה': ai.get('מה', ''),
        'קול': extract_kol(ai),
        'רוח': extract_ruach(ai),
        'סור': ai.get('סור', 'נעול'),
        'מקור': ai.get('מקור', ''),
        'תת_חק': f"1/{10000}"  # יחס לכלל
    }


# =============================================================================
# ספר החוקים
# =============================================================================

def read_ai(path):
    """קרא אי"""
    ai = {}
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if ':' in line:
                key, val = line.split(':', 1)
                ai[key.strip()] = val.strip()
    return ai


def build_sefer_hukim():
    """
    בנה ספר החוקים מכל אי
    """
    hukim = []

    for ai_file in sorted(AIN_DIR.glob("*.אי")):
        ai = read_ai(ai_file)
        hok_id = ai_file.stem
        hok = create_hok(ai, hok_id)
        hukim.append(hok)

    return hukim


def write_sefer_hukim(hukim):
    """
    כתוב ספר החוקים
    """
    HUKIM_DIR.mkdir(exist_ok=True)

    sefer_path = HUKIM_DIR / "ספר"
    with open(sefer_path, 'w', encoding='utf-8') as f:
        f.write("# ספר החוקים\n")
        f.write("# ק\"ק חק - קול ורוח\n\n")

        f.write(f"סה\"כ: {len(hukim)} חוקים\n\n")

        # סיכום לפי סוג
        by_ruach = {}
        for hok in hukim:
            r = hok['רוח'].split(' (')[0]
            by_ruach[r] = by_ruach.get(r, 0) + 1

        f.write("לפי רוח:\n")
        for r, count in sorted(by_ruach.items(), key=lambda x: -x[1]):
            f.write(f"  {r}: {count}\n")
        f.write("\n")

        # סיכום לפי סור
        by_sur = {'פתוח': 0, 'מוגבל': 0, 'נעול': 0}
        for hok in hukim:
            sur = hok['סור']
            if sur in by_sur:
                by_sur[sur] += 1

        f.write("לפי סור:\n")
        for sur, count in by_sur.items():
            f.write(f"  {sur}: {count}\n")

    return sefer_path


def write_hukim_index(hukim):
    """
    כתוב אינדקס חוקים
    """
    index_path = HUKIM_DIR / "אינדקס"
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write("# אינדקס חוקים\n\n")

        for hok in hukim:  # ראשונים 100
            f.write(f"{hok['id']}: {hok['מה']}\n")
            f.write(f"  קול: {hok['קול']}\n")
            f.write(f"  רוח: {hok['רוח']}\n")
            f.write(f"  תת: {hok['תת_חק']}\n\n")

        if len(hukim) > 100:
            f.write(f"... ועוד {len(hukim) - 100} חוקים\n")

    return index_path


# =============================================================================
# מפרט דיבור לדבר
# =============================================================================

def mifrat_dibur_l_davar(hok):
    """
    מפרט דיבור לדבר
    הופך חק (דיבור) לדבר (פעולה)
    """
    dibur = hok['קול']  # מה שנאמר
    ruach = hok['רוח']  # מה שמכוון

    # דבר = הפעולה המעשית
    if 'פתוח' in ruach:
        davar = 'פעיל'
    elif 'נעול' in ruach:
        davar = 'ממתין'
    else:
        davar = 'מוגבל'

    return {
        'דיבור': dibur,
        'רוח': ruach,
        'דבר': davar
    }


# =============================================================================
# תיקון מין למינו
# =============================================================================

def tzafa_mekulkal(hukim):
    """
    צפה - זהה מקולקל
    """
    mekulkalim = []

    for hok in hukim:
        # בדוק חוסר עקביות
        if not hok['מקור']:
            mekulkalim.append((hok, 'חסר_מקור'))
        elif not hok['מה']:
            mekulkalim.append((hok, 'חסר_מה'))

    return mekulkalim


def tiken_min_l_mino(hok, problem):
    """
    תקן - מין למינו
    """
    if problem == 'חסר_מקור':
        # הוסף מקור ברירת מחדל
        hok['מקור'] = 'ספר יצירה'
    elif problem == 'חסר_מה':
        # הוסף מה ברירת מחדל
        hok['מה'] = f"יחידה {hok['id']}"

    return hok


# =============================================================================
# Main
# =============================================================================

def main():
    print("=" * 60)
    print("ספר החוקים")
    print("אדון הכל = אברהם = אברם מתגבש")
    print("=" * 60)

    # בנה ספר החוקים
    print("\nבונה ספר החוקים...")
    hukim = build_sefer_hukim()
    print(f"  {len(hukim)} חוקים")

    # צפה מקולקל
    print("\nצפה מקולקל...")
    mekulkalim = tzafa_mekulkal(hukim)
    print(f"  {len(mekulkalim)} מקולקלים")

    # תקן מין למינו
    if mekulkalim:
        print("\nמתקן מין למינו...")
        for hok, problem in mekulkalim:
            tiken_min_l_mino(hok, problem)
        print(f"  תוקנו {len(mekulkalim)}")

    # כתוב ספר
    print("\nכותב ספר החוקים...")
    sefer_path = write_sefer_hukim(hukim)
    print(f"  {sefer_path}")

    # כתוב אינדקס
    print("\nכותב אינדקס...")
    index_path = write_hukim_index(hukim)
    print(f"  {index_path}")

    # סיכום
    print("\n" + "=" * 60)
    print("ק\"ק חק:")
    print(f"  סה\"כ: {len(hukim)}")

    # דוגמה - דיבור לדבר
    if hukim:
        print("\nדוגמה - מפרט דיבור לדבר:")
        example = mifrat_dibur_l_davar(hukim[0])
        print(f"  דיבור: {example['דיבור']}")
        print(f"  רוח: {example['רוח']}")
        print(f"  דבר: {example['דבר']}")

    print("\n" + "=" * 60)
    print("כל חק = 1/10000 תת-חק")
    print("הלוך ורצוא ורצוא ושוב")
    print("=" * 60)


if __name__ == "__main__":
    main()
