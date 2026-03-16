#!/usr/bin/env python3
"""
ממיר.רצוא.ושוב.py

הלוך ורצוא ורצוא ושוב

מאין ליש - התרחבות
מיש לאין - התכווצות

בכל רמה:
  אין → יש (פנימה)
  יש → אין (החוצה)

עד למטה פנימה
ואז גם בפנימה לבחוץ

רמות:
  אחד (1)
    ↓ רצוא
  שלשה (3)
    ↓ רצוא
  שבעה (7)
    ↓ רצוא
  שנים עשר (12)
    ↑ שוב
  שבעה (7)
    ↑ שוב
  שלשה (3)
    ↑ שוב
  אחד (1)

כשלהבת קשורה בגחלת

איסורים:
- no 3rd party
"""

from pathlib import Path

BASE = Path(__file__).parent
YESH_DIR = BASE / "יש"
AIN_DIR = BASE / "אין"

# =============================================================================
# רמות ההיררכיה
# =============================================================================

LEVELS = [
    {'שם': 'אחד', 'מספר': 1, 'תוכן': 'אל מלך נאמן'},
    {'שם': 'שלשה', 'מספר': 3, 'תוכן': 'אמות: א מ ש'},
    {'שם': 'שבעה', 'מספר': 7, 'תוכן': 'כפולות: בגדכפרת'},
    {'שם': 'שנים_עשר', 'מספר': 12, 'תוכן': 'פשוטות: הוזחטילנסעצק'},
]


def ratzo(level_from, level_to, depth=0):
    """
    רצוא - התרחבות פנימה
    אין → יש
    """
    indent = "  " * depth
    print(f"{indent}רצוא: {level_from['שם']} ({level_from['מספר']}) → {level_to['שם']} ({level_to['מספר']})")

    return {
        'כיוון': 'פנימה',
        'מ': level_from['שם'],
        'אל': level_to['שם'],
        'יחס': level_to['מספר'] / level_from['מספר'],
        'עומק': depth
    }


def shov(level_from, level_to, depth=0):
    """
    שוב - התכווצות החוצה
    יש → אין
    """
    indent = "  " * depth
    print(f"{indent}שוב: {level_from['שם']} ({level_from['מספר']}) ← {level_to['שם']} ({level_to['מספר']})")

    return {
        'כיוון': 'החוצה',
        'מ': level_from['שם'],
        'אל': level_to['שם'],
        'יחס': level_from['מספר'] / level_to['מספר'],
        'עומק': depth
    }


def haloch_v_ratzo():
    """
    הלוך ורצוא - מלמעלה למטה פנימה
    1 → 3 → 7 → 12
    """
    print("\n=== הלוך ורצוא (פנימה) ===")
    print("אין → יש")

    steps = []
    for i in range(len(LEVELS) - 1):
        step = ratzo(LEVELS[i], LEVELS[i + 1], depth=i)
        steps.append(step)

    return steps


def ratzo_v_shov():
    """
    רצוא ושוב - מלמטה למעלה החוצה
    12 → 7 → 3 → 1
    """
    print("\n=== רצוא ושוב (החוצה) ===")
    print("יש → אין")

    steps = []
    for i in range(len(LEVELS) - 1, 0, -1):
        step = shov(LEVELS[i], LEVELS[i - 1], depth=len(LEVELS) - 1 - i)
        steps.append(step)

    return steps


def cycle_at_level(level_idx, inner_depth=0):
    """
    מחזור בכל רמה - רצוא ושוב פנימי
    """
    if level_idx >= len(LEVELS) - 1:
        return []

    level = LEVELS[level_idx]
    next_level = LEVELS[level_idx + 1]

    indent = "  " * inner_depth
    print(f"{indent}[רמה {level['שם']}]")

    cycles = []

    # רצוא פנימה
    cycles.append(ratzo(level, next_level, inner_depth))

    # מחזור פנימי (רקורסיה)
    inner = cycle_at_level(level_idx + 1, inner_depth + 1)
    cycles.extend(inner)

    # שוב החוצה
    cycles.append(shov(next_level, level, inner_depth))

    return cycles


def full_cycle():
    """
    מחזור מלא - כל הרמות
    פנימה עד הסוף, ואז החוצה
    """
    print("\n=== מחזור מלא ===")
    print("פנימה עד למטה, ואז החוצה")

    return cycle_at_level(0)


def ain_to_yesh_transform():
    """
    טרנספורמציה אין → יש
    """
    print("\n=== אין → יש ===")

    # ספור אי
    ain_count = len(list(AIN_DIR.glob("*.אי")))
    print(f"  אין: {ain_count} אי")

    # קרא שדה
    sade_path = YESH_DIR / "שדה"
    if sade_path.exists():
        with open(sade_path, 'r', encoding='utf-8') as f:
            sade_lines = len(f.readlines())
        print(f"  יש: {sade_lines} שורות בשדה")

    return {'אין': ain_count, 'יש': sade_lines if sade_path.exists() else 0}


def yesh_to_ain_transform():
    """
    טרנספורמציה יש → אין
    חזרה לשורש
    """
    print("\n=== יש → אין ===")

    # המהות שחוזרת מיש לאין
    essence = {
        'חתימה': 'נאמן',
        'מכריע': 'מאוזן',
        'קשר': 'וכולן אדוקין זה בזה'
    }

    for key, val in essence.items():
        print(f"  {key}: {val}")

    return essence


def write_cycle_to_sade(cycles):
    """כתוב מחזור לשדה"""
    sade_path = YESH_DIR / "שדה"

    with open(sade_path, 'a', encoding='utf-8') as f:
        f.write("\n# רצוא ושוב\n\n")
        f.write("הלוך_ורצוא:\n")
        f.write("  כיוון: פנימה (אין → יש)\n")
        f.write("  מסלול: 1 → 3 → 7 → 12\n\n")

        f.write("רצוא_ושוב:\n")
        f.write("  כיוון: החוצה (יש → אין)\n")
        f.write("  מסלול: 12 → 7 → 3 → 1\n\n")

        f.write("מחזור:\n")
        f.write("  עומק: 4 רמות\n")
        f.write("  צעדים: 6 (3 פנימה + 3 החוצה)\n")
        f.write("  עיקרון: כשלהבת קשורה בגחלת\n")


def main():
    print("=" * 32)  # נתיבות
    print("הלוך ורצוא ורצוא ושוב")
    print("=" * 32)  # נתיבות

    # אין → יש
    ain_yesh = ain_to_yesh_transform()

    # הלוך ורצוא (פנימה)
    ratzo_steps = haloch_v_ratzo()

    # רצוא ושוב (החוצה)
    shov_steps = ratzo_v_shov()

    # מחזור מלא
    full = full_cycle()

    # יש → אין
    yesh_ain = yesh_to_ain_transform()

    # כתוב לשדה
    print("\nכותב לשדה...")
    write_cycle_to_sade(full)

    print("\n" + "=" * 32  # נתיבות)
    print("כשלהבת קשורה בגחלת")
    print("נעוץ סופן בתחלתן ותחלתן בסופן")
    print("=" * 32)  # נתיבות


if __name__ == "__main__":
    main()
