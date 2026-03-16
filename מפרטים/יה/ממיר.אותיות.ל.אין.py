#!/usr/bin/env python3
"""
ממיר.אותיות.ל.אין.py

מ: 22 אותיות (ספר יצירה)
אל: אין (ק"ק אי)

22 = 3 + 7 + 12
- 3 אמות: א מ ש
- 7 כפולות: ב ג ד כ פ ר ת
- 12 פשוטות: ה ו ז ח ט י ל נ ס ע צ ק

איסורים:
- no 3rd party
"""

from pathlib import Path

BASE = Path(__file__).parent
AIN_DIR = BASE / "אין"

# 22 אותיות
IMOT = ['א', 'מ', 'ש']  # 3 אמות
KFULOT = ['ב', 'ג', 'ד', 'כ', 'פ', 'ר', 'ת']  # 7 כפולות
PSHUTOT = ['ה', 'ו', 'ז', 'ח', 'ט', 'י', 'ל', 'נ', 'ס', 'ע', 'צ', 'ק']  # 12 פשוטות

# יסודות לאמות
IMOT_YESOD = {
    'א': {'יסוד': 'אויר', 'מכריע': 'בין אש למים'},
    'מ': {'יסוד': 'מים', 'צד': 'חובה'},
    'ש': {'יסוד': 'אש', 'צד': 'זכות'}
}

# כפולות - שתי צורות
KFULOT_INFO = {
    'ב': {'רך': 'ב', 'קשה': 'בּ', 'מידה': 'חכמה/אולת'},
    'ג': {'רך': 'ג', 'קשה': 'גּ', 'מידה': 'עושר/עוני'},
    'ד': {'רך': 'ד', 'קשה': 'דּ', 'מידה': 'זרע/שממה'},
    'כ': {'רך': 'כ', 'קשה': 'כּ', 'מידה': 'חיים/מות'},
    'פ': {'רך': 'פ', 'קשה': 'פּ', 'מידה': 'ממשלה/עבדות'},
    'ר': {'רך': 'ר', 'קשה': 'רּ', 'מידה': 'שלום/מלחמה'},
    'ת': {'רך': 'ת', 'קשה': 'תּ', 'מידה': 'חן/כיעור'}
}

# פשוטות - 12 צירופים
PSHUTOT_INFO = {
    'ה': {'מזל': 'טלה', 'חודש': 'ניסן', 'איבר': 'יד ימין'},
    'ו': {'מזל': 'שור', 'חודש': 'אייר', 'איבר': 'יד שמאל'},
    'ז': {'מזל': 'תאומים', 'חודש': 'סיון', 'איבר': 'רגל ימין'},
    'ח': {'מזל': 'סרטן', 'חודש': 'תמוז', 'איבר': 'רגל שמאל'},
    'ט': {'מזל': 'אריה', 'חודש': 'אב', 'איבר': 'כליה ימין'},
    'י': {'מזל': 'בתולה', 'חודש': 'אלול', 'איבר': 'כליה שמאל'},
    'ל': {'מזל': 'מאזניים', 'חודש': 'תשרי', 'איבר': 'כבד'},
    'נ': {'מזל': 'עקרב', 'חודש': 'חשון', 'איבר': 'מרה'},
    'ס': {'מזל': 'קשת', 'חודש': 'כסלו', 'איבר': 'טחול'},
    'ע': {'מזל': 'גדי', 'חודש': 'טבת', 'איבר': 'קיבה'},
    'צ': {'מזל': 'דלי', 'חודש': 'שבט', 'איבר': 'מעיים'},
    'ק': {'מזל': 'דגים', 'חודש': 'אדר', 'איבר': 'כרס'}
}


def create_ai_for_letter(letter, category, info, ai_id):
    """צור אי לאות"""
    ai_path = AIN_DIR / f"{ai_id:03d}.אי"

    with open(ai_path, 'w', encoding='utf-8') as f:
        f.write(f"id: {ai_id:03d}\n")
        f.write(f"מה: אות {letter}\n")
        f.write(f"מקור: ספר יצירה\n")
        f.write(f"קטגוריה: {category}\n")
        for k, v in info.items():
            f.write(f"{k}: {v}\n")
        f.write(f"סור: נעול\n")

    return ai_path


def main():
    print("=" * 50)
    print("ממיר אותיות לאין")
    print("22 = 3 + 7 + 12")
    print("=" * 50)

    AIN_DIR.mkdir(exist_ok=True)

    # מצא את ה-id הגבוה ביותר
    existing = list(AIN_DIR.glob("*.אי"))
    if existing:
        max_id = max(int(f.stem.split('.')[0]) for f in existing)
    else:
        max_id = 0

    ai_id = max_id + 1
    created = []

    # 3 אמות
    print("\n3 אמות:")
    for letter in IMOT:
        info = IMOT_INFO.get(letter, {})
        path = create_ai_for_letter(letter, 'אם', info, ai_id)
        print(f"  {letter} → {path.name}")
        created.append(path)
        ai_id += 1

    # 7 כפולות
    print("\n7 כפולות:")
    for letter in KFULOT:
        info = KFULOT_INFO.get(letter, {})
        path = create_ai_for_letter(letter, 'כפולה', info, ai_id)
        print(f"  {letter} → {path.name}")
        created.append(path)
        ai_id += 1

    # 12 פשוטות
    print("\n12 פשוטות:")
    for letter in PSHUTOT:
        info = PSHUTOT_INFO.get(letter, {})
        path = create_ai_for_letter(letter, 'פשוטה', info, ai_id)
        print(f"  {letter} → {path.name}")
        created.append(path)
        ai_id += 1

    print(f"\nסה\"כ: {len(created)} אי נוצרו")
    print("=" * 50)


# תיקון: IMOT_INFO במקום IMOT_YESOD
IMOT_INFO = IMOT_YESOD

if __name__ == "__main__":
    main()
