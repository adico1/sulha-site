#!/usr/bin/env python3
"""
ע.py - פשוטה ע

שתים עשרה פשוטות יסודן שיחה הרהור הלוך ראיה שמיעה מעשה תשמיש ריח שינה רוגז לעיטה שחוק

יסוד: רוגז

מקור: ספר יצירה

איסורים:
- no 3rd party
"""

OT = 'ע'
INFO = {'פשוטה': 'ע', 'יסוד': 'רוגז'}


def tzafa():
    """צפה"""
    return INFO


def main():
    for k, v in INFO.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
