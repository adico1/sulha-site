#!/usr/bin/env python3
"""
ו.py - פשוטה ו

שתים עשרה פשוטות יסודן שיחה הרהור הלוך ראיה שמיעה מעשה תשמיש ריח שינה רוגז לעיטה שחוק

יסוד: הרהור

מקור: ספר יצירה

איסורים:
- no 3rd party
"""

OT = 'ו'
INFO = {'פשוטה': 'ו', 'יסוד': 'הרהור'}


def tzafa():
    """צפה"""
    return INFO


def main():
    for k, v in INFO.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
