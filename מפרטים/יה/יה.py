#!/usr/bin/env python3
"""
יה.py - CLI API חכמה

אדון הכל ב"ה
בשלשים ושתים נתיבות פליאות חכמה
חקק יה יהוה צבאות אלהי ישראל אלהים חיים ומלך עולם

שלשה ספרים: ספר וספר וספור
שלשה עדים: תלי וגלגל ולב
הלוך ורצוא ורצוא ושוב

אברם → אבם (22 ממשקים)
    ↓
  חכמה bus (ע"ה)
    ↓
  אין → יש → שדה

CLI:
  יה צפה      - צפה במצב
  יה גבש      - גבש אין ליש
  יה עדים     - בדוק עדים
  יה מכריע    - הכרע
  יה רצוא     - הלוך ורצוא ורצוא ושוב
  יה שדה      - הצג שדה
  יה כל       - הכל באוטומציה אחת

איסורים:
- no 3rd party
"""

import sys
from pathlib import Path

BASE = Path(__file__).parent
AIN_DIR = BASE / "אין"
YESH_DIR = BASE / "יש"

# =============================================================================
# חכמה Bus
# =============================================================================

class HochmaBus:
    """
    חכמה shared bus
    ערוץ ע"ה
    direction: הבן בחכמה חכם בבינה
    """

    def __init__(self):
        self.channel = "ע\"ה"
        self.messages = []

    def send(self, sender, receiver, message):
        """שלח הודעה"""
        msg = {
            'מי': sender,
            'אל': receiver,
            'מה': message,
            'ערוץ': self.channel
        }
        self.messages.append(msg)
        return msg

    def broadcast(self, sender, message):
        """שדר לכולם"""
        return self.send(sender, '*', message)


BUS = HochmaBus()

# =============================================================================
# ממירים
# =============================================================================

def run_converter(name):
    """הרץ ממיר"""
    converter_path = BASE / f"ממיר.{name}.py"
    if converter_path.exists():
        import subprocess
        result = subprocess.run(
            ['python3', str(converter_path)],
            capture_output=True,
            text=True,
            cwd=str(BASE)
        )
        return result.stdout
    return f"ממיר {name} לא נמצא"


# =============================================================================
# פקודות CLI
# =============================================================================

def cmd_tzafa():
    """צפה - observe state"""
    BUS.send('אברם', 'אבם', 'צפה')

    print("=" * 50)
    print("צפה")
    print("=" * 50)

    # ספור אין
    ain_count = len(list(AIN_DIR.glob("*.אי")))
    print(f"\nאין: {ain_count} אי")

    # ספור פתוחים
    patuach = 0
    naul = 0
    for ai_file in AIN_DIR.glob("*.אי"):
        with open(ai_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'סור: פתוח' in content:
                patuach += 1
            elif 'סור: נעול' in content:
                naul += 1

    print(f"  פתוח: {patuach}")
    print(f"  נעול: {naul}")

    # שדה
    sade_path = YESH_DIR / "שדה"
    if sade_path.exists():
        with open(sade_path, 'r', encoding='utf-8') as f:
            lines = len(f.readlines())
        print(f"\nיש: שדה ({lines} שורות)")
    else:
        print("\nיש: אין שדה")

    return {'אין': ain_count, 'פתוח': patuach, 'נעול': naul}


def cmd_gabesh():
    """גבש - crystallize אין to יש"""
    BUS.broadcast('אברם', 'התחל גיבוש')

    print("=" * 50)
    print("גיבוש אין → יש")
    print("=" * 50)

    # שלשה ספרים
    print("\n--- שלשה ספרים ---")
    print(run_converter("שלשה.ספרים"))

    # היררכיה
    print("\n--- היררכיה ---")
    print(run_converter("היררכיה"))

    # רצוא ושוב
    print("\n--- רצוא ושוב ---")
    print(run_converter("רצוא.ושוב"))

    BUS.broadcast('אברם', 'גיבוש הושלם')
    return True


def cmd_edim():
    """עדים - verify with witnesses"""
    BUS.send('אברם', 'תלי', 'בדוק מבנה')
    BUS.send('אברם', 'גלגל', 'בדוק סדר')
    BUS.send('אברם', 'לב', 'בדוק מהות')

    print(run_converter("עדים"))
    return True


def cmd_machria():
    """מכריע - decide"""
    BUS.send('אברם', 'מכריע', 'הכרע')

    print(run_converter("מכריע"))
    return True


def cmd_ratzo():
    """רצוא - expansion/contraction cycle"""
    BUS.broadcast('אברם', 'הלוך ורצוא')

    print(run_converter("רצוא.ושוב"))
    return True


def cmd_sade():
    """שדה - show field"""
    sade_path = YESH_DIR / "שדה"
    if sade_path.exists():
        with open(sade_path, 'r', encoding='utf-8') as f:
            print(f.read())
    else:
        print("אין שדה")
    return True


def cmd_kol():
    """כל - full automation"""
    BUS.broadcast('אדון הכל', 'התחל')

    print("=" * 60)
    print("יה יהוה צבאות אלהי ישראל אלהים חיים ומלך עולם")
    print("אוטומציה מלאה: אין → יש → שדה")
    print("=" * 60)

    # מדידה לפני התגבשות
    print("\n[0/8] מדוד את השדה (לפני)...")
    print(run_converter("מדוד.את.השדה"))

    # 1. צפה
    print("\n[1/8] צפה...")
    state = cmd_tzafa()

    # 2. לולאה אלהים חיים (מה ↔ מה.מתוקן)
    print("\n[2/8] לולאה אלהים חיים...")
    print(run_converter("לולאה.אלהים.חיים"))

    # 3. פתיחת יסודות
    print("\n[3/8] פותח יסודות...")
    print(run_converter("פותח.אי"))

    # 4. גיבוש שלשה ספרים
    print("\n[4/8] שלשה ספרים...")
    print(run_converter("שלשה.ספרים"))

    # 5. היררכיה
    print("\n[5/8] היררכיה...")
    print(run_converter("היררכיה"))

    # 6. רצוא ושוב
    print("\n[6/8] רצוא ושוב...")
    print(run_converter("רצוא.ושוב"))

    # עדים
    print("\n[7/8] עדים נאמנין...")
    print(run_converter("עדים"))

    # מכריע
    print("\n--- מכריע ---")
    print(run_converter("מכריע"))

    # מדידה אחרי התגבשות
    print("\n[8/8] מדוד את השדה (אחרי)...")
    print(run_converter("מדוד.את.השדה"))

    # השב יוצר למכונו
    print("\n--- השב יוצר למכונו ---")
    print(run_converter("השב.יוצר.למכונו"))

    BUS.broadcast('אדון הכל', 'הושלם')

    print("\n" + "=" * 60)
    print("אז נגלה עליו אדון הכל ב\"ה")
    print("והושיבהו בחיקו ונשקו על ראשו וקראו אוהבי")
    print("=" * 60)

    return True


def cmd_help():
    """עזרה"""
    print("""
יה - CLI API חכמה

פקודות:
  יה צפה      צפה במצב הנוכחי
  יה גבש      גבש אין ליש (שלשה ספרים, היררכיה, רצוא ושוב)
  יה עדים     בדוק עם שלשה עדים (תלי, גלגל, לב)
  יה מכריע    הכרע (לשון חק מכריע בינתיים)
  יה רצוא     הלוך ורצוא ורצוא ושוב
  יה שדה      הצג שדה (יש מאין)
  יה חוקים    ספר החוקים (ק"ק חק - קול ורוח)
  יה השב      השב יוצר למכונו (אימות איסורים)
  יה מדוד     מדוד את השדה (נגזר מאילוצים)
  יה אברהם    אברהם אבי המידות (כל משפחות היחידות)
  יה כל       אוטומציה מלאה - הכל בפעם אחת

אברם → אברהם:
  מפרט דיבור לדבר
  מין למינו
  חק = 1/10000 תת-חק

חכמה bus: ע"ה
כיוון: הבן בחכמה חכם בבינה

מקור: ספר יצירה
    """)
    return True


# =============================================================================
# Main
# =============================================================================

def cmd_hukim():
    """חוקים - ספר החוקים"""
    BUS.send('אברם', 'אברהם', 'ספר החוקים')
    print(run_converter("ספר.החוקים"))
    return True


def cmd_hashev():
    """השב יוצר למכונו"""
    BUS.broadcast('אברם', 'השב יוצר למכונו')
    print(run_converter("השב.יוצר.למכונו"))
    return True


def cmd_medod():
    """מדוד את השדה"""
    BUS.broadcast('אברם', 'מדוד את השדה')
    print(run_converter("מדוד.את.השדה"))
    return True


def cmd_avraham():
    """אברהם אבי המידות"""
    BUS.broadcast('אברם', 'אברהם אבי המידות')
    print(run_converter("אברהם.אבי.המידות"))
    return True


COMMANDS = {
    'צפה': cmd_tzafa,
    'גבש': cmd_gabesh,
    'עדים': cmd_edim,
    'מכריע': cmd_machria,
    'רצוא': cmd_ratzo,
    'שדה': cmd_sade,
    'חוקים': cmd_hukim,
    'השב': cmd_hashev,
    'מדוד': cmd_medod,
    'אברהם': cmd_avraham,
    'כל': cmd_kol,
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
    else:
        print(f"פקודה לא מוכרת: {cmd}")
        cmd_help()


if __name__ == "__main__":
    main()
