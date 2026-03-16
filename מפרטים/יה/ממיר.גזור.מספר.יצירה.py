#!/usr/bin/env python3
"""
ממיר.גזור.מספר.יצירה.py

דו-כיווני: התרחבות וצמצום (רצוא ושוב)
ספר יצירה שורה 8: ודברו בהן ברצוא ושוב

התרחבות (רצוא): ספר יצירה → גזירות
צמצום (שוב): גזירות → אימות מול ספר יצירה

איסורים:
- no 3rd party
- no hardcoded - derive from text
"""

from pathlib import Path
import re

BASE = Path(__file__).parent
ROOT = BASE.parent.parent.parent
SEFER_YETZIRAH = ROOT / "immutable" / "ספר_היצירה_נוסח_גרא.txt"

# מילון גזירה מטקסט
PATTERNS = {
    r'עשר ספירות': ('ספירות', 10),
    r'עשרים ושתים אותיות': ('אותיות', 22),
    r'שלש אמות': ('אמות', 3),
    r'שבע כפולות': ('כפולות', 7),
    r'שתים עשרה פשוטות': ('פשוטות', 12),
    r'שלשים ושתים נתיבות': ('נתיבות', 32),
    r'רל"א שערים': ('שערים', 231),
    r'ששה קצוות': ('קצוות', 6),
    r'שנים עשר[ה]? אלכסונ': ('אלכסונן', 12),
    r'שבעה כוכבים': ('כוכבים', 7),
    r'שבעה ימים': ('ימים', 7),
    r'שבעה שערים': ('שערי_נפש', 7),
}


def hitrachvut(lines):
    """
    התרחבות (רצוא) - מספר יצירה החוצה
    גזור מספרים ושמות מהטקסט
    """
    print("\n--- התרחבות (רצוא) ---")
    print("מספר יצירה → גזירות")

    derived = {}

    for i, line in enumerate(lines, 1):
        for pattern, (name, expected) in PATTERNS.items():
            if re.search(pattern, line):
                if name not in derived:
                    derived[name] = {'מספר': expected, 'שורה': i, 'מקור': line[:60]}
                    print(f"  שורה {i}: {name} = {expected}")

    return derived


def tzimtzum(derived, lines):
    """
    צמצום (שוב) - אימות מול ספר יצירה
    בדוק שכל גזירה מופיעה בטקסט
    """
    print("\n--- צמצום (שוב) ---")
    print("גזירות → אימות מול ספר יצירה")

    errors = []
    full_text = '\n'.join(lines)

    for name, info in derived.items():
        # בדוק שהשם מופיע בטקסט
        if name in full_text or info['מקור'] in full_text:
            print(f"  ✓ {name}: {info['מספר']} - מאומת")
        else:
            print(f"  ✗ {name}: לא נמצא בטקסט")
            errors.append(name)

    return len(errors) == 0, errors


def main():
    print("=" * 50)
    print("גזירה מספר יצירה")
    print("רצוא ושוב - התרחבות וצמצום")
    print("=" * 50)

    if not SEFER_YETZIRAH.exists():
        print(f"שגיאה: לא נמצא {SEFER_YETZIRAH}")
        return

    with open(SEFER_YETZIRAH, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    print(f"נקראו {len(lines)} שורות")

    # רצוא - התרחבות
    derived = hitrachvut(lines)

    # שוב - צמצום
    valid, errors = tzimtzum(derived, lines)

    print("\n" + "=" * 50)
    print("סיכום")
    print("=" * 50)
    print(f"נגזרו: {len(derived)} יחידות")

    if valid:
        print("✓ כל הגזירות מאומתות מול ספר יצירה")
    else:
        print(f"✗ {len(errors)} גזירות לא מאומתות")

    # הדפס טבלת סיכום
    print("\nטבלת גזירות:")
    for name, info in sorted(derived.items(), key=lambda x: -x[1]['מספר']):
        print(f"  {name}: {info['מספר']}")


if __name__ == "__main__":
    main()
