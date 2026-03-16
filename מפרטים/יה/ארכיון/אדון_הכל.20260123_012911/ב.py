#!/usr/bin/env python3
"""
ב.py - כפולה ב

שבע כפולות בגדכפרת יסודן חכמה עושר זרע חיים ממשלה שלום וחן

יסוד: חכמה

מקור: ספר יצירה

איסורים:
- no 3rd party
"""

OT = 'ב'
INFO = {'כפולה': 'ב', 'יסוד': 'חכמה'}


def tzafa():
    """צפה"""
    return INFO


def main():
    for k, v in INFO.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
