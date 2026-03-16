#!/usr/bin/env python3
"""
ל.py - פשוטה ל

שתים עשרה פשוטות יסודן שיחה הרהור הלוך ראיה שמיעה מעשה תשמיש ריח שינה רוגז לעיטה שחוק

יסוד: תשמיש

מקור: ספר יצירה

איסורים:
- no 3rd party
"""

OT = 'ל'
INFO = {'פשוטה': 'ל', 'יסוד': 'תשמיש'}


def tzafa():
    """צפה"""
    return INFO


def main():
    for k, v in INFO.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
