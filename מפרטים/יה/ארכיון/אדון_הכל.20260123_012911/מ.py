#!/usr/bin/env python3
"""
מ.py - אם מ

שלש אמות אמש בעולם אויר מים אש

יסוד: מים

מקור: ספר יצירה

איסורים:
- no 3rd party
"""

OT = 'מ'
INFO = {'אם': 'מ', 'יסוד': 'מים'}


def tzafa():
    """צפה"""
    return INFO


def main():
    for k, v in INFO.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
