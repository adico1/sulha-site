#!/usr/bin/env python3
"""
ה.py - פשוטה ה

שתים עשרה פשוטות יסודן שיחה הרהור הלוך ראיה שמיעה מעשה תשמיש ריח שינה רוגז לעיטה שחוק

יסוד: שיחה

מקור: ספר יצירה

איסורים:
- no 3rd party
"""

OT = 'ה'
INFO = {'פשוטה': 'ה', 'יסוד': 'שיחה'}


def tzafa():
    """צפה"""
    return INFO


def main():
    for k, v in INFO.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
