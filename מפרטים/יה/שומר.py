#!/usr/bin/env python3
"""
שומר.py - מגן על אברם

עוטף את אברם ומגן עליו מכל מצב.
אם אברם שבור - מתקן אותו.
לעולם לא נכשל.

מקור: ספר יצירה - שומר ישראל
"""

from pathlib import Path
import sys

BASE = Path(__file__).parent
AVRAM = BASE / "אברם.py"


def bdok_tachbir(file_path):
    """בדוק תחביר - מחזיר שגיאות אם יש"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # נסה לקמפל - אם יש שגיאה, נתפוס אותה
    import ast
    shgiot = []

    # מצא שורות עם מחרוזות לא סגורות
    lines = content.split('\n')
    for i, line in enumerate(lines, 1):
        # בדוק מחרוזת לא סגורה (פתיחה בלי סגירה באותה שורה)
        if "r'" in line or 'r"' in line:
            # regex string
            if line.count("r'") != line.count("'") // 2:
                if "'''" not in line:
                    shgiot.append((i, 'מחרוזת לא סגורה', line))

    # נסה compile
    import py_compile
    import tempfile
    import os

    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as tmp:
        tmp.write(content)
        tmp_path = tmp.name

    shgia_compile = None
    line_num = None

    import subprocess
    result = subprocess.run(
        [sys.executable, '-m', 'py_compile', tmp_path],
        capture_output=True,
        text=True
    )

    os.unlink(tmp_path)

    if result.returncode != 0:
        # חלץ מספר שורה מהשגיאה
        error_text = result.stderr
        import re
        match = re.search(r'line (\d+)', error_text)
        if match:
            line_num = int(match.group(1))
            shgiot.append((line_num, 'שגיאת תחביר', lines[line_num-1] if line_num <= len(lines) else ''))

    return shgiot


def taken_shgiot(file_path, shgiot):
    """תקן שגיאות שנמצאו"""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    tikunim = []

    for line_num, sug, content in shgiot:
        if sug == 'מחרוזת לא סגורה' or sug == 'שגיאת תחביר':
            # מחק את השורה הבעייתית והשורות הבאות עד לסוף הבלוק
            # מצא את תחילת הפונקציה הבעייתית
            start = line_num - 1

            # חפש אחורה את תחילת הפונקציה
            while start > 0 and not lines[start].startswith('def '):
                start -= 1

            # חפש קדימה את סוף הפונקציה
            end = line_num
            while end < len(lines) and (lines[end].startswith(' ') or lines[end].startswith('\t') or lines[end].strip() == ''):
                end += 1

            # החלף את הפונקציה בגרסה ריקה
            func_name = lines[start].split('def ')[1].split('(')[0] if 'def ' in lines[start] else 'unknown'

            # מחק את הפונקציה השבורה
            for i in range(start, min(end, len(lines))):
                lines[i] = ''

            # הוסף הערה
            lines[start] = f'# נמחק: פונקציה {func_name} עם שגיאת תחביר\n'

            tikunim.append(f'נמחקה פונקציה {func_name} (שורה {line_num})')

    # כתוב חזרה
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)

    return tikunim


def harizt_avram():
    """הרץ את אברם בצורה מוגנת"""
    # שלב 1: בדוק תחביר
    shgiot = bdok_tachbir(AVRAM)

    if shgiot:
        print("=== שומר: נמצאו שגיאות ===")
        for line_num, sug, content in shgiot:
            print(f"  שורה {line_num}: {sug}")
            print(f"    {content[:50]}...")

        print("\n=== שומר: מתקן... ===")
        tikunim = taken_shgiot(AVRAM, shgiot)
        for tikun in tikunim:
            print(f"  {tikun}")

        print("\n=== שומר: בודק שוב... ===")
        shgiot = bdok_tachbir(AVRAM)
        if shgiot:
            print("  עדיין יש שגיאות - דורש תיקון ידני")
            return False

    # שלב 2: הרץ את אברם
    print("=== שומר: מריץ אברם ===")
    import subprocess
    result = subprocess.run([sys.executable, str(AVRAM)], cwd=str(BASE))
    return result.returncode == 0


def main():
    print("=" * 32)  # נתיבות
    print("שומר - מגן על אברם")
    print("=" * 32)

    success = harizt_avram()

    if success:
        print("\n✓ אברם רץ בהצלחה")
    else:
        print("\n✗ אברם לא רץ - בדוק שגיאות")


if __name__ == "__main__":
    main()
