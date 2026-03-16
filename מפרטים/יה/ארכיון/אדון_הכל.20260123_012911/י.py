#!/usr/bin/env python3
"""
י.py - פשוטה י

שתים עשרה פשוטות יסודן שיחה הרהור הלוך ראיה שמיעה מעשה תשמיש ריח שינה רוגז לעיטה שחוק

יסוד: מעשה

מקור: ספר יצירה

איסורים:
- no 3rd party
"""

OT = 'י'
INFO = {'פשוטה': 'י', 'יסוד': 'מעשה'}


def tzafa():
    """צפה"""
    return INFO


def main():
    for k, v in INFO.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
