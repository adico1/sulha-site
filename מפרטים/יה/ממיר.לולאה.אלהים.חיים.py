#!/usr/bin/env python3
"""
ממיר.לולאה.אלהים.חיים.py

לולאה = אלהים חיים
מיישר מה עם מה.מתוקן

עד ש: מה.מתוקן = מה
ע"י: גזרת נתונים לתת-נתונים ותבנית לתת-תבנית

כשלהבת קשורה בגחלת:
- יה = גחלת
- מה = שלהבת

נעוץ סופן בתחלתן:
- מה → יה → מה.מתוקן → מה

איסורים:
- no 3rd party
"""

from pathlib import Path

BASE = Path(__file__).parent
MAH_PATH = BASE / "מה"
METUKAN_PATH = BASE / "מה.מתוקן"
NETUNIM_PATH = BASE / "נתונים"
TAVNIT_PATH = BASE / "תבנית"


def read_file(path):
    """קרא קובץ"""
    if not path.exists():
        return ""
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def write_file(path, content):
    """כתוב קובץ"""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


def extract_netunim(mah_content):
    """חלץ נתונים ממה"""
    netunim = []
    lines = mah_content.strip().split('\n')

    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        # חלץ ערכים
        if ':' in line:
            key, val = line.split(':', 1)
            val = val.strip()
            if val and not val.startswith('{') and not val.startswith('['):
                netunim.append(f"{key.strip()}: {val}")

    return netunim


def extract_tavnit(mah_content):
    """חלץ תבנית ממה"""
    tavnit = []
    lines = mah_content.strip().split('\n')

    for line in lines:
        stripped = line.strip()
        if not stripped:
            tavnit.append('')
            continue

        if stripped.startswith('#'):
            tavnit.append(stripped)
            continue

        # שמור מבנה עם placeholder
        if ':' in line:
            key = line.split(':')[0]
            indent = len(line) - len(line.lstrip())
            tavnit.append(' ' * indent + key.strip() + ': {' + key.strip() + '}')
        else:
            tavnit.append(line)

    return tavnit


def generate_metukan(netunim, tavnit):
    """צור מה.מתוקן מנתונים ותבנית"""
    # בנה מילון נתונים
    data = {}
    for line in netunim:
        if ':' in line:
            key, val = line.split(':', 1)
            data[key.strip()] = val.strip()

    # החלף בתבנית
    result = []
    for line in tavnit:
        new_line = line
        for key, val in data.items():
            placeholder = '{' + key + '}'
            if placeholder in new_line:
                new_line = new_line.replace(placeholder, val)
        result.append(new_line)

    return '\n'.join(result)


def compare(mah, metukan):
    """השווה מה למתוקן"""
    mah_lines = mah.strip().split('\n')
    metukan_lines = metukan.strip().split('\n')

    diffs = []
    max_len = max(len(mah_lines), len(metukan_lines))

    for i in range(max_len):
        mah_line = mah_lines[i] if i < len(mah_lines) else '<חסר>'
        met_line = metukan_lines[i] if i < len(metukan_lines) else '<חסר>'

        if mah_line != met_line:
            diffs.append((i + 1, mah_line, met_line))

    return diffs


def loop_iteration(iteration):
    """איטרציה אחת של הלולאה"""
    print(f"\n--- איטרציה {iteration} ---")

    # קרא מה
    mah = read_file(MAH_PATH)
    if not mah:
        print("  אין מה")
        return False, 0

    # חלץ נתונים ותבנית
    netunim = extract_netunim(mah)
    tavnit = extract_tavnit(mah)

    # שמור נתונים ותבנית
    write_file(NETUNIM_PATH, '\n'.join(netunim))
    write_file(TAVNIT_PATH, '\n'.join(tavnit))

    print(f"  נתונים: {len(netunim)} שורות")
    print(f"  תבנית: {len(tavnit)} שורות")

    # צור מתוקן
    metukan = generate_metukan(netunim, tavnit)
    write_file(METUKAN_PATH, metukan)

    # השווה
    diffs = compare(mah, metukan)

    if not diffs:
        print("  ✓ מה = מה.מתוקן")
        return True, 0
    else:
        print(f"  ✗ {len(diffs)} הבדלים")

        # הסר יתר (מה.מתוקן !== מה מותר)
        # החלף מה במתוקן
        write_file(MAH_PATH, metukan)
        print(f"  → מה עודכן (הוסר יתר)")

        return False, len(diffs)


def main():
    print("=" * 32)  # נתיבות
    print("לולאה = אלהים חיים")
    print("מיישר מה עם מה.מתוקן")
    print("=" * 32)  # נתיבות

    max_iterations = 10
    iteration = 0

    while iteration < max_iterations:
        iteration += 1
        done, diffs = loop_iteration(iteration)

        if done:
            print("\n" + "=" * 32  # נתיבות)
            print("✓ נעוץ סופן בתחלתן")
            print("מה = מה.מתוקן")
            print("=" * 32)  # נתיבות
            break

        if diffs == 0:
            break

    else:
        print(f"\n⚠ הגיע למקסימום {max_iterations} איטרציות")

    # הדפס מצב סופי
    print("\nמצב סופי:")
    mah = read_file(MAH_PATH)
    metukan = read_file(METUKAN_PATH)
    mah_lines = len(mah.strip().split('\n')) if mah.strip() else 0
    met_lines = len(metukan.strip().split('\n')) if metukan.strip() else 0
    print(f"  מה: {mah_lines} שורות")
    print(f"  מתוקן: {met_lines} שורות")


if __name__ == "__main__":
    main()
