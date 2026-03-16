#!/usr/bin/env python3
"""
ח.py - פשוטה ח

שתים עשרה פשוטות יסודן שיחה הרהור הלוך ראיה שמיעה מעשה תשמיש ריח שינה רוגז לעיטה שחוק

יסוד: ראיה

מקור: ספר יצירה

איסורים:
- no 3rd party
"""

OT = 'ח'
INFO = {'פשוטה': 'ח', 'יסוד': 'ראיה'}


def tzafa():
    """צפה"""
    return INFO


def main():
    for k, v in INFO.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
