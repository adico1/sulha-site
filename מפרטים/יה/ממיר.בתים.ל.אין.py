#!/usr/bin/env python3
"""
ממיר.בתים.ל.אין.py

בתים מספר יצירה - עצרות
2! + 3! + 4! + 5! + 6! + 7! = 5,912

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
    ai_path = AIN_DIR / f"{ai_id:03d}.אי"
    with open(ai_path, 'w', encoding='utf-8') as f:
        f.write(f"id: {ai_id:03d}\n")
        f.write(f"מה: {mah}\n")
        f.write(f"מקור: {makor}\n")
        if extra:
            for k, v in extra.items():
                f.write(f"{k}: {v}\n")
        f.write(f"סור: נעול\n")
    return ai_path


def factorial(n):
    """חשב עצרת"""
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def main():
    print("=" * 50)
    print("ממיר בתים לאין")
    print("2! + 3! + 4! + 5! + 6! + 7! = 5,912")
    print("=" * 50)

    AIN_DIR.mkdir(exist_ok=True)
    ai_id = get_next_id()
    created = 0

    # בתים - עצרות
    for n in range(2, 8):  # 2! עד 7!
        count = factorial(n)
        print(f"\n{n}! = {count} בתים:")
        for i in range(count):
            create_ai(ai_id, f'בית {n}!.{i+1:04d}', f'ספר יצירה - בתים', {'עצרת': str(n), 'מספר': str(i+1)})
            ai_id += 1
            created += 1
            if (i + 1) % 1000 == 0:
                print(f"  ... {i+1}/{count}")
        print(f"  נוצרו {count}")

    print(f"\nסה\"כ: {created} אי נוצרו")
    print("=" * 50)


if __name__ == "__main__":
    main()
