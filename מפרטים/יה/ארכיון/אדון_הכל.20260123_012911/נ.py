#!/usr/bin/env python3
"""
נ.py - פשוטה נ

שתים עשרה פשוטות יסודן שיחה הרהור הלוך ראיה שמיעה מעשה תשמיש ריח שינה רוגז לעיטה שחוק

יסוד: ריח

מקור: ספר יצירה

איסורים:
- no 3rd party
"""

OT = 'נ'
INFO = {'פשוטה': 'נ', 'יסוד': 'ריח'}


def tzafa():
    """צפה"""
    return INFO


def main():
    for k, v in INFO.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
