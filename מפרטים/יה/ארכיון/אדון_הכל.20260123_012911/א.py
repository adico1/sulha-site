#!/usr/bin/env python3
"""
א.py - אם א

שלש אמות אמש בעולם אויר מים אש

יסוד: אויר

מקור: ספר יצירה

איסורים:
- no 3rd party
"""

OT = 'א'
INFO = {'אם': 'א', 'יסוד': 'אויר'}


def tzafa():
    """צפה"""
    return INFO


def main():
    for k, v in INFO.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
