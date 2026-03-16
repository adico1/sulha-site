#!/usr/bin/env python3
"""
ק.py - פשוטה ק

שתים עשרה פשוטות יסודן שיחה הרהור הלוך ראיה שמיעה מעשה תשמיש ריח שינה רוגז לעיטה שחוק

יסוד: שחוק

מקור: ספר יצירה

איסורים:
- no 3rd party
"""

OT = 'ק'
INFO = {'פשוטה': 'ק', 'יסוד': 'שחוק'}


def tzafa():
    """צפה"""
    return INFO


def main():
    for k, v in INFO.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
