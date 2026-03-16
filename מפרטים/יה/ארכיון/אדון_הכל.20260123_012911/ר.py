#!/usr/bin/env python3
"""
ר.py - כפולה ר

שבע כפולות בגדכפרת יסודן חכמה עושר זרע חיים ממשלה שלום וחן

יסוד: שלום

מקור: ספר יצירה

איסורים:
- no 3rd party
"""

OT = 'ר'
INFO = {'כפולה': 'ר', 'יסוד': 'שלום'}


def tzafa():
    """צפה"""
    return INFO


def main():
    for k, v in INFO.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
