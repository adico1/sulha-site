#!/usr/bin/env python3
"""
ת.py - כפולה ת

שבע כפולות בגדכפרת יסודן חכמה עושר זרע חיים ממשלה שלום וחן

יסוד: חן

מקור: ספר יצירה

איסורים:
- no 3rd party
"""

OT = 'ת'
INFO = {'כפולה': 'ת', 'יסוד': 'חן'}


def tzafa():
    """צפה"""
    return INFO


def main():
    for k, v in INFO.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
