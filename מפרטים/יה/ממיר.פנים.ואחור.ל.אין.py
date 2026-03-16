#!/usr/bin/env python3
"""
ממיר.פנים.ואחור.ל.אין.py

32  # נתיבות פנים × 32  # נתיבות אחור = 3,600
גלגל פנים ואחור (ספר יצירה)

מקור: "וגלגל פנים ואחור"

איסורים:
- no 3rd party
"""

from pathlib import Path

BASE = Path(__file__).parent
AIN_DIR = BASE / "אין"


def get_next_id():
    """מצא את ה-id הבא"""
    existing = list(AIN_DIR.glob("*.אי"))
    if existing:
        return max(int(f.stem.split('.')[0]) for f in existing) + 1
    return 1


def create_ai(ai_id, mah, makor, extra=None):
    """צור אי"""
    ai_path = AIN_DIR / f"{ai_id:04d}.אי"
    with open(ai_path, 'w', encoding='utf-8') as f:
        f.write(f"id: {ai_id:04d}\n")
        f.write(f"מה: {mah}\n")
        f.write(f"מקור: {makor}\n")
        if extra:
            for k, v in extra.items():
                f.write(f"{k}: {v}\n")
        f.write(f"סור: נעול\n")
    return ai_path


def main():
    print("=" * 50)
    print("ממיר פנים ואחור לאין")
    print("60 × 32  # נתיבות = 3,600")
    print("=" * 50)

    AIN_DIR.mkdir(exist_ok=True)
    ai_id = get_next_id()
    created = 0

    # 32  # נתיבות פנים × 32  # נתיבות אחור
    print("\nגלגל פנים ואחור:")
    for panim in range(1, 61):
        for achor in range(1, 61):
            create_ai(
                ai_id,
                f'גלגל {panim:02d}.{achor:02d}',
                'ספר יצירה - גלגל',
                {'פנים': str(panim), 'אחור': str(achor)}
            )
            ai_id += 1
            created += 1
        if panim % 10 == 0:
            print(f"  פנים {panim}/60 ({created} נוצרו)")

    print(f"\nסה\"כ: {created} אי נוצרו")
    print("=" * 50)


if __name__ == "__main__":
    main()
