#!/usr/bin/env python3
"""
בלום.py - בלום פיך מלדבר

בדיקת האם Claude חורג מתפקידו

Claude מותר:
- לקרוא קבצים (Read)
- לכתוב ל-bus.queue בלבד (Write)
- להריץ יה.py או אברם.py בלבד (Bash)

Claude אסור:
- ליצור קבצים חדשים
- לערוך קבצים קיימים
- להריץ ממירים ישירות
- לכתוב לכל מקום חוץ מ-bus.queue

שימוש:
  python3 blom.py check_write <path>
  python3 blom.py check_bash <command>

מקור: ספר יצירה, אדם → חי העולמים

איסורים:
- no 3rd party
"""

import sys
from pathlib import Path

BASE = Path(__file__).parent.parent
BUS_QUEUE = Path(__file__).parent / "bus.queue"
LEDGER = Path(__file__).parent / "bus.ledger"

# =============================================================================
# בדיקות
# =============================================================================

def check_write(target_path):
    """
    בדוק אם כתיבה מותרת

    מותר: bus.queue בלבד
    אסור: כל דבר אחר
    """
    target = Path(target_path)

    # מותר לכתוב ל-bus.queue
    if target.name == "bus.queue":
        return True, "מותר: כתיבה ל-bus.queue"

    # אסור לכתוב לכל מקום אחר
    return False, f"אסור: Claude לא מורשה לכתוב ל-{target.name}"


def check_bash(command):
    """
    בדוק אם הרצה מותרת

    מותר: יה.py, אברם.py, ls, cat (קריאה)
    אסור: ממירים ישירות, כל דבר אחר
    """
    cmd = command.strip()

    # מותר להריץ יה.py
    if "יה.py" in cmd:
        return True, "מותר: הרצת יה.py"

    # מותר להריץ אברם.py
    if "אברם.py" in cmd:
        return True, "מותר: הרצת אברם.py"

    # מותר להריץ bus.py
    if "bus.py" in cmd:
        return True, "מותר: הרצת bus.py"

    # מותר לקרוא (ls, cat, head, tail)
    if cmd.startswith("ls") or cmd.startswith("cat") or cmd.startswith("head") or cmd.startswith("tail"):
        return True, "מותר: קריאה"

    # אסור להריץ ממירים ישירות
    if "ממיר." in cmd and ".py" in cmd:
        return False, "אסור: Claude לא מורשה להריץ ממירים ישירות. השתמש ב-יה.py או אברם.py"

    # אסור להריץ python3 ישירות על קבצים אחרים
    if "python3" in cmd:
        return False, f"אסור: Claude לא מורשה להריץ python3 ישירות"

    # ברירת מחדל - אסור
    return False, f"אסור: פקודה לא מורשית"


def log_violation(action, target, reason):
    """
    רשום חריגה ל-ledger
    """
    from datetime import datetime
    timestamp = datetime.now().isoformat()

    with open(LEDGER, 'a', encoding='utf-8') as f:
        f.write(f"{timestamp} | VIOLATION | {action} | {target} | {reason}\n")


# =============================================================================
# Main
# =============================================================================

def main():
    if len(sys.argv) < 3:
        print("שימוש:")
        print("  python3 blom.py check_write <path>")
        print("  python3 blom.py check_bash <command>")
        sys.exit(1)

    action = sys.argv[1]
    target = sys.argv[2]

    if action == "check_write":
        allowed, reason = check_write(target)
        if allowed:
            print(f"✓ {reason}")
            sys.exit(0)
        else:
            print(f"✗ {reason}")
            log_violation("write", target, reason)
            sys.exit(1)

    elif action == "check_bash":
        allowed, reason = check_bash(target)
        if allowed:
            print(f"✓ {reason}")
            sys.exit(0)
        else:
            print(f"✗ {reason}")
            log_violation("bash", target, reason)
            sys.exit(1)

    else:
        print(f"פעולה לא מוכרת: {action}")
        sys.exit(1)


if __name__ == "__main__":
    main()
