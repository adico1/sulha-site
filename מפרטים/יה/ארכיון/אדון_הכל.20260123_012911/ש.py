#!/usr/bin/env python3
"""
ש.py - אם ש

שלש אמות אמש בעולם אויר מים אש

יסוד: אש

מקור: ספר יצירה

איסורים:
- no 3rd party
"""

OT = 'ש'
INFO = {'אם': 'ש', 'יסוד': 'אש'}


def tzafa():
    """צפה"""
    return INFO


def main():
    for k, v in INFO.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
