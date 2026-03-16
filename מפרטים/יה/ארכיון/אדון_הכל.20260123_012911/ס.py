#!/usr/bin/env python3
"""
ס.py - פשוטה ס

שתים עשרה פשוטות יסודן שיחה הרהור הלוך ראיה שמיעה מעשה תשמיש ריח שינה רוגז לעיטה שחוק

יסוד: שינה

מקור: ספר יצירה

איסורים:
- no 3rd party
"""

OT = 'ס'
INFO = {'פשוטה': 'ס', 'יסוד': 'שינה'}


def tzafa():
    """צפה"""
    return INFO


def main():
    for k, v in INFO.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
