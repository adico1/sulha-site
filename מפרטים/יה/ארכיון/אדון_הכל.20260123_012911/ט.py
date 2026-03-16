#!/usr/bin/env python3
"""
ט.py - פשוטה ט

שתים עשרה פשוטות יסודן שיחה הרהור הלוך ראיה שמיעה מעשה תשמיש ריח שינה רוגז לעיטה שחוק

יסוד: שמיעה

מקור: ספר יצירה

איסורים:
- no 3rd party
"""

OT = 'ט'
INFO = {'פשוטה': 'ט', 'יסוד': 'שמיעה'}


def tzafa():
    """צפה"""
    return INFO


def main():
    for k, v in INFO.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
