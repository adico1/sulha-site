#!/usr/bin/env python3
"""
פ.py - כפולה פ

שבע כפולות בגדכפרת יסודן חכמה עושר זרע חיים ממשלה שלום וחן

יסוד: ממשלה

מקור: ספר יצירה

איסורים:
- no 3rd party
"""

OT = 'פ'
INFO = {'כפולה': 'פ', 'יסוד': 'ממשלה'}


def tzafa():
    """צפה"""
    return INFO


def main():
    for k, v in INFO.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
