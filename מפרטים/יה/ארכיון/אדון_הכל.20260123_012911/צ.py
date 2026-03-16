#!/usr/bin/env python3
"""
צ.py - פשוטה צ

שתים עשרה פשוטות יסודן שיחה הרהור הלוך ראיה שמיעה מעשה תשמיש ריח שינה רוגז לעיטה שחוק

יסוד: לעיטה

מקור: ספר יצירה

איסורים:
- no 3rd party
"""

OT = 'צ'
INFO = {'פשוטה': 'צ', 'יסוד': 'לעיטה'}


def tzafa():
    """צפה"""
    return INFO


def main():
    for k, v in INFO.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
