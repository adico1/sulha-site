#!/usr/bin/env python3
"""
ממיר.איסור.ל.אין.py
מ: י/מפרטים/יה/מה
אל: י/מפרטים/יה/אין/

פעולה: גזירת איסורים לאי-ים ואחסון באין

איסורים:
- no 3rd party (no json, yaml)
- אי = יחידה קטנה ביותר
"""

import os
from pathlib import Path

BASE = Path(__file__).parent
AIN_DIR = BASE / "אין"


def find_isurim(file_path):
    """מצא כל האיסורים בקובץ מפרט"""
    isurim = []
    in_isurim_section = False

    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.rstrip()

            if 'איסורים #' in line:
                in_isurim_section = True
                continue

            if in_isurim_section:
                if line.startswith('- '):
                    isur_text = line[2:].strip()
                    isurim.append({
                        'מה': isur_text,
                        'מקור': file_path.name,
                        'שורה': line_num
                    })
                elif line and not line.startswith(' ') and not line.startswith('-'):
                    in_isurim_section = False

    return isurim


def write_ai(ai_id, ai_data):
    """כתוב קובץ אי"""
    filename = AIN_DIR / f"{ai_id:03d}.אי"
    content = f"""id: {ai_id:03d}
מה: {ai_data['מה']}
מקור: {ai_data['מקור']}
שורה: {ai_data['שורה']}
סור: נעול
"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    return filename


def main():
    print("=" * 50)
    print("ממיר איסור לאין")
    print("=" * 50)

    # וודא שתיקיית אין קיימת
    AIN_DIR.mkdir(exist_ok=True)

    # מצא כל קבצי מפרט
    all_isurim = []
    for mifrat in BASE.glob("**/*.מפרט"):
        if 'אין' not in str(mifrat):  # אל תכלול את אין עצמו
            isurim = find_isurim(mifrat)
            all_isurim.extend(isurim)
            if isurim:
                print(f"נמצאו {len(isurim)} איסורים ב-{mifrat.name}")

    print(f"\nסה״כ: {len(all_isurim)} איסורים")
    print("\nגוזר לאי-ים...")

    # גזור כל איסור לאי
    for i, isur in enumerate(all_isurim, 1):
        filename = write_ai(i, isur)
        print(f"  {i:03d}: {isur['מה']}")

    # כתוב מונה
    counter_file = AIN_DIR / "מונה"
    with open(counter_file, 'w', encoding='utf-8') as f:
        f.write(f"סה״כ: {len(all_isurim)}\n")
        f.write(f"מקסימום: 10000\n")  # ק"ק
        f.write(f"נותר: {10000 - len(all_isurim)}\n")

    print(f"\nעלתה. {len(all_isurim)} אי-ים נוצרו באין/")
    print("=" * 50)


if __name__ == "__main__":
    main()
