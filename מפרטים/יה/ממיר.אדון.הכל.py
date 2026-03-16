#!/usr/bin/env python3
"""
ממיר.אדון.הכל.py

אברם מתגבש לאברהם - אדון הכל
יוצר מוצר סופי עם 22 מודולים

המוצר:
- תיקיה ראשית: אדון_הכל/
- 22 מודולי Python (א עד ת)
- CLI ראשי: אדון_הכל.py
- עדים נאמנים מאשרים

מקור: ספר יצירה
אז נגלה עליו אדון הכל ב"ה
והושיבהו בחיקו ונשקו על ראשו וקראו אוהבי

איסורים:
- no 3rd party
"""

from pathlib import Path

BASE = Path(__file__).parent
PROJECT_ROOT = BASE.parent.parent.parent  # מערכת/
ADON_DIR = PROJECT_ROOT / "אדון_הכל"

# 22 אותיות
OTIOT = ['א', 'ב', 'ג', 'ד', 'ה', 'ו', 'ז', 'ח', 'ט', 'י', 'כ',
         'ל', 'מ', 'נ', 'ס', 'ע', 'פ', 'צ', 'ק', 'ר', 'ש', 'ת']

# 3 אמות
IMOT = {'א': 'אויר', 'מ': 'מים', 'ש': 'אש'}

# 7 כפולות
KFULOT = {'ב': 'חכמה', 'ג': 'עושר', 'ד': 'זרע', 'כ': 'חיים', 'פ': 'ממשלה', 'ר': 'שלום', 'ת': 'חן'}

# 12 פשוטות - ספר יצירה שורה 42  # צירופים
# "ה' ו' ז', ח' ט' י', ל' נ' ס', ע' צ' ק', יסודן שיחה הרהור הלוך, ראיה שמיעה מעשה, תשמיש ריח שינה, רוגז לעיטה שחוק"
PSHUTOT = {
    'ה': 'שיחה', 'ו': 'הרהור', 'ז': 'הלוך',
    'ח': 'ראיה', 'ט': 'שמיעה', 'י': 'מעשה',
    'ל': 'תשמיש', 'נ': 'ריח', 'ס': 'שינה',
    'ע': 'רוגז', 'צ': 'לעיטה', 'ק': 'שחוק'
}


def get_ot_info(ot):
    """קבל מידע על אות - מספר יצירה בלבד"""
    # שלש אמות אמש - אויר מים אש
    if ot in IMOT:
        return {'אם': ot, 'יסוד': IMOT[ot]}
    # שבע כפולות בגדכפרת - חכמה עושר זרע חיים ממשלה שלום חן
    elif ot in KFULOT:
        return {'כפולה': ot, 'יסוד': KFULOT[ot]}
    # שתים עשרה פשוטות - שיחה הרהור הלוך ראיה שמיעה מעשה תשמיש ריח שינה רוגז לעיטה שחוק
    elif ot in PSHUTOT:
        return {'פשוטה': ot, 'יסוד': PSHUTOT[ot]}
    else:
        return {'אות': ot}


def create_module(ot):
    """צור מודול לאות - מספר יצירה בלבד"""
    info = get_ot_info(ot)

    # קבע משפחה
    if ot in IMOT:
        mishpacha = 'אם'
        makor = 'שלש אמות אמש בעולם אויר מים אש'
    elif ot in KFULOT:
        mishpacha = 'כפולה'
        makor = 'שבע כפולות בגדכפרת יסודן חכמה עושר זרע חיים ממשלה שלום וחן'
    elif ot in PSHUTOT:
        mishpacha = 'פשוטה'
        makor = 'שתים עשרה פשוטות יסודן שיחה הרהור הלוך ראיה שמיעה מעשה תשמיש ריח שינה רוגז לעיטה שחוק'
    else:
        mishpacha = 'אות'
        makor = 'עשרים ושתים אותיות יסוד'

    content = f'''#!/usr/bin/env python3
"""
{ot}.py - {mishpacha} {ot}

{makor}

יסוד: {info.get('יסוד', ot)}

מקור: ספר יצירה

איסורים:
- no 3rd party
"""

OT = '{ot}'
INFO = {info}


def tzafa():
    """צפה"""
    return INFO


def main():
    for k, v in INFO.items():
        print(f"{{k}}: {{v}}")


if __name__ == "__main__":
    main()
'''
    return content


def create_cli():
    """צור CLI ראשי"""
    content = '''#!/usr/bin/env python3
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
    print("=" * 32)  # נתיבות
    print("אדון הכל - צפה")
    print("=" * 32)  # נתיבות

    for ot in OTIOT:
        info = load_module(ot)
        status = "✓" if info['קיים'] else "✗"
        print(f"  {status} {ot}")

    print()
    total = len(OTIOT)
    print(f"סה״כ: {total} אותיות")


def cmd_edim():
    """עדים נאמנים - verify"""
    print("=" * 32)  # נתיבות
    print("עדים נאמנים")
    print("=" * 32)  # נתיבות

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
'''
    return content


def create_init():
    """צור __init__.py"""
    content = '''"""
אדון_הכל - חבילת 22 אותיות

אז נגלה עליו אדון הכל ב"ה
"""

from pathlib import Path

BASE = Path(__file__).parent

OTIOT = ['א', 'ב', 'ג', 'ד', 'ה', 'ו', 'ז', 'ח', 'ט', 'י', 'כ',
         'ל', 'מ', 'נ', 'ס', 'ע', 'פ', 'צ', 'ק', 'ר', 'ש', 'ת']

__all__ = OTIOT + ['OTIOT']
'''
    return content


def gabesh_adon_hakol():
    """גבש אדון הכל - יצירת המוצר הסופי"""
    print("=" * 32)  # נתיבות
    print("אברם מתגבש לאברהם - אדון הכל")
    print("=" * 32)  # נתיבות

    # צור תיקיה
    ADON_DIR.mkdir(exist_ok=True)
    print(f"\nתיקיה: {ADON_DIR}")

    # צור 22 מודולים
    print("\nיוצר 22 מודולים...")
    for ot in OTIOT:
        module_path = ADON_DIR / f"{ot}.py"
        content = create_module(ot)
        with open(module_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ {ot}.py")

    # צור CLI
    print("\nיוצר CLI ראשי...")
    cli_path = ADON_DIR / "אדון_הכל.py"
    with open(cli_path, 'w', encoding='utf-8') as f:
        f.write(create_cli())
    print(f"  ✓ אדון_הכל.py")

    # צור __init__.py
    init_path = ADON_DIR / "__init__.py"
    with open(init_path, 'w', encoding='utf-8') as f:
        f.write(create_init())
    print(f"  ✓ __init__.py")

    # סיכום
    print("\n" + "=" * 32)  # נתיבות
    print("אז נגלה עליו אדון הכל ב\"ה")
    print("והושיבהו בחיקו ונשקו על ראשו וקראו אוהבי")
    print("=" * 32)  # נתיבות

    print(f"\nנוצרו:")
    print(f"  22 מודולי אותיות")
    print(f"  1 CLI ראשי")
    print(f"  1 __init__.py")
    print(f"\nנתיב: {ADON_DIR}")


def main():
    gabesh_adon_hakol()


if __name__ == "__main__":
    main()
