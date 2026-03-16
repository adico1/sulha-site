#!/usr/bin/env python3
"""
ממיר.סיום.ל.אין.py

22  # אותיות אי אחרונים להשלמת ק"ק
"""

from pathlib import Path

BASE = Path(__file__).parent
AIN_DIR = BASE / "אין"


def get_next_id():
    existing = list(AIN_DIR.glob("*.אי"))
    if existing:
        ids = []
        for f in existing:
            ids.append(int(f.stem.split('.')[0]))
        return max(ids) + 1 if ids else 1
    return 1


def create_ai(ai_id, mah, makor):
    ai_path = AIN_DIR / f"{ai_id:04d}.אי"
    with open(ai_path, 'w', encoding='utf-8') as f:
        f.write(f"id: {ai_id:04d}\n")
        f.write(f"מה: {mah}\n")
        f.write(f"מקור: {makor}\n")
        f.write(f"סור: נעול\n")
    return ai_path


def main():
    print("=" * 50)
    print("סיום ק\"ק - 22  # אותיות אחרונים")
    print("=" * 50)

    AIN_DIR.mkdir(exist_ok=True)
    ai_id = get_next_id()

    # 22  # אותיות = 22 אותיות (שמות) + 4 (אחד, שלש, שבע, שתים עשרה)
    items = [
        'אות אלף', 'אות בית', 'אות גימל', 'אות דלת',
        'אות הא', 'אות וו', 'אות זין', 'אות חית',
        'אות טית', 'אות יוד', 'אות כף', 'אות למד',
        'אות מם', 'אות נון', 'אות סמך', 'אות עין',
        'אות פא', 'אות צדי', 'אות קוף', 'אות ריש',
        'אות שין', 'אות תו',
        'מספר אחד', 'מספר שלש', 'מספר שבע', 'מספר שתים עשרה'
    ]

    for item in items:
        create_ai(ai_id, item, 'ספר יצירה - סיום')
        ai_id += 1
        print(f"  {ai_id-1:04d}: {item}")

    print(f"\nסה\"כ: {len(items)} אי נוצרו")
    print("ק\"ק = 10,000 שלם!")
    print("=" * 50)


if __name__ == "__main__":
    main()
