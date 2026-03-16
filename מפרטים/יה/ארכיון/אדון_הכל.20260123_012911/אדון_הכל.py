#!/usr/bin/env python3
"""
אדון_הכל.py - CLI ראשי

אז נגלה עליו אדון הכל ב"ה
והושיבהו בחיקו ונשקו על ראשו וקראו אוהבי

22 מודולים מחוברים

מקור: ספר יצירה

איסורים:
- no 3rd party
"""

import sys
from pathlib import Path

BASE = Path(__file__).parent

# 22 אותיות
OTIOT = ['א', 'ב', 'ג', 'ד', 'ה', 'ו', 'ז', 'ח', 'ט', 'י', 'כ',
         'ל', 'מ', 'נ', 'ס', 'ע', 'פ', 'צ', 'ק', 'ר', 'ש', 'ת']


def load_module(ot):
    """טען מודול אות"""
    module_path = BASE / f"{ot}.py"
    if module_path.exists():
        # Read and extract info
        with open(module_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return {'אות': ot, 'קיים': True}
    return {'אות': ot, 'קיים': False}


def cmd_tzafa():
    """צפה - observe all"""
    print("=" * 50)
    print("אדון הכל - צפה")
    print("=" * 50)

    for ot in OTIOT:
        info = load_module(ot)
        status = "✓" if info['קיים'] else "✗"
        print(f"  {status} {ot}")

    print()
    total = len(OTIOT)
    print(f"סה״כ: {total} אותיות")


def cmd_edim():
    """עדים נאמנים - verify"""
    print("=" * 50)
    print("עדים נאמנים")
    print("=" * 50)

    takin = 0
    for ot in OTIOT:
        info = load_module(ot)
        if info['קיים']:
            takin += 1

    print(f"מודולים: {takin}/22")

    if takin == 22:
        print()
        print("✓ עדים נאמנים מאשרים")
        print("✓ אברם הפך לאברהם")
        print("✓ אדון הכל התגבש")
    else:
        missing = 22 - takin
        print()
        print(f"✗ חסרים {missing} מודולים")


def cmd_help():
    """עזרה"""
    print("""
אז נגלה עליו אדון הכל

פקודות:
  צפה    עשרים ושתים אותיות יסוד
  עדים   עדים נאמנים בתלי וגלגל ולב

עשרים ושתים אותיות יסוד:
  שלש אמות אמש
  שבע כפולות בגדכפרת
  שתים עשרה פשוטות הוזחטילנסעצק

מקור: ספר יצירה
    """)


COMMANDS = {
    'צפה': cmd_tzafa,
    'עדים': cmd_edim,
    'עזרה': cmd_help,
    'help': cmd_help,
}


def main():
    if len(sys.argv) < 2:
        cmd_help()
        return

    cmd = sys.argv[1]

    if cmd in COMMANDS:
        COMMANDS[cmd]()
    elif cmd in OTIOT:
        # Show specific letter module
        info = load_module(cmd)
        if info['קיים']:
            module_path = BASE / f"{cmd}.py"
            import subprocess
            subprocess.run(['python3', str(module_path)])
        else:
            print(f"מודול {cmd} לא נמצא")
    else:
        print(f"פקודה לא מוכרת: {cmd}")
        cmd_help()


if __name__ == "__main__":
    main()
