#!/usr/bin/env python3
"""
ז.py - פשוטה ז

שתים עשרה פשוטות יסודן שיחה הרהור הלוך ראיה שמיעה מעשה תשמיש ריח שינה רוגז לעיטה שחוק

יסוד: הלוך

מקור: ספר יצירה

איסורים:
- no 3rd party
"""

OT = 'ז'
INFO = {'פשוטה': 'ז', 'יסוד': 'הלוך'}


def tzafa():
    """צפה"""
    return INFO


def main():
    for k, v in INFO.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
