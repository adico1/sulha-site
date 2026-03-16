#!/usr/bin/env python3
"""
ממיר.השלמה.ל.אין.py

השלמה לק"ק - 231  # שערים אי

מקורות מספר יצירה:
- 7 ימים
- 12 חודשים
- 7 כוכבים
- 12 מזלות
- 12 איברים
- 3 יסודות (אש מים אויר)
- 3 עולמות (עולם שנה נפש)
- 3 אבות (אברהם יצחק יעקב)
- 32 נתיבות (כמספר)
- 10 מאמרות
- 10 ספירות (כשמות)
- 22 יסודות אותיות
- סה"כ אפשרי: ~133
- + 46 צירופי יה"ו נוספים

איסורים:
- no 3rd party
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


def create_ai(ai_id, mah, makor, extra=None):
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
    print("השלמה לק\"ק")
    print("=" * 50)

    AIN_DIR.mkdir(exist_ok=True)
    ai_id = get_next_id()
    created = 0

    # 7 ימים
    yamim = ['ראשון', 'שני', 'שלישי', 'רביעי', 'חמישי', 'שישי', 'שבת']
    print("\n7 ימים:")
    for yom in yamim:
        create_ai(ai_id, f'יום {yom}', 'ספר יצירה - ימים')
        ai_id += 1
        created += 1
    print(f"  {len(yamim)} נוצרו")

    # 12 חודשים
    chodashim = ['ניסן', 'אייר', 'סיון', 'תמוז', 'אב', 'אלול',
                 'תשרי', 'חשון', 'כסלו', 'טבת', 'שבט', 'אדר']
    print("\n12 חודשים:")
    for chodesh in chodashim:
        create_ai(ai_id, f'חודש {chodesh}', 'ספר יצירה - חודשים')
        ai_id += 1
        created += 1
    print(f"  {len(chodashim)} נוצרו")

    # 7 כוכבים
    kochavim = ['שבתאי', 'צדק', 'מאדים', 'חמה', 'נוגה', 'כוכב', 'לבנה']
    print("\n7 כוכבים:")
    for kochav in kochavim:
        create_ai(ai_id, f'כוכב {kochav}', 'ספר יצירה - כוכבים')
        ai_id += 1
        created += 1
    print(f"  {len(kochavim)} נוצרו")

    # 12 מזלות
    mazalot = ['טלה', 'שור', 'תאומים', 'סרטן', 'אריה', 'בתולה',
               'מאזניים', 'עקרב', 'קשת', 'גדי', 'דלי', 'דגים']
    print("\n12 מזלות:")
    for mazal in mazalot:
        create_ai(ai_id, f'מזל {mazal}', 'ספר יצירה - מזלות')
        ai_id += 1
        created += 1
    print(f"  {len(mazalot)} נוצרו")

    # 12 איברים
    evarim = ['יד ימין', 'יד שמאל', 'רגל ימין', 'רגל שמאל',
              'כליה ימין', 'כליה שמאל', 'כבד', 'מרה',
              'טחול', 'קיבה', 'מעיים', 'כרס']
    print("\n12 איברים:")
    for ever in evarim:
        create_ai(ai_id, f'איבר {ever}', 'ספר יצירה - איברים')
        ai_id += 1
        created += 1
    print(f"  {len(evarim)} נוצרו")

    # 3 יסודות
    yesodot = [('אש', 'זכות'), ('מים', 'חובה'), ('אויר', 'מכריע')]
    print("\n3 יסודות:")
    for yesod in yesodot:
        create_ai(ai_id, f'יסוד {yesod[0]}', 'ספר יצירה - יסודות', {'כף': yesod[1]})
        ai_id += 1
        created += 1
    print(f"  {len(yesodot)} נוצרו")

    # 3 עולמות
    olamot = ['עולם', 'שנה', 'נפש']
    print("\n3 עולמות:")
    for olam in olamot:
        create_ai(ai_id, f'ציר {olam}', 'ספר יצירה - עולמות')
        ai_id += 1
        created += 1
    print(f"  {len(olamot)} נוצרו")

    # 3 אבות
    avot = ['אברהם', 'יצחק', 'יעקב']
    print("\n3 אבות:")
    for av in avot:
        create_ai(ai_id, f'אב {av}', 'ספר יצירה - אבות')
        ai_id += 1
        created += 1
    print(f"  {len(avot)} נוצרו")

    # 32 נתיבות (כמספרים)
    print("\n32 נתיבות:")
    for i in range(1, 33):
        create_ai(ai_id, f'נתיב {i}', 'ספר יצירה - נתיבות', {'מספר': str(i)})
        ai_id += 1
        created += 1
    print(f"  32 נוצרו")

    # 10 מאמרות
    maamarot = ['בראשית', 'יהי אור', 'יהי רקיע', 'יקוו המים', 'תדשא הארץ',
                'יהי מאורות', 'ישרצו המים', 'תוצא הארץ', 'נעשה אדם', 'הנה נתתי']
    print("\n10 מאמרות:")
    for maamar in maamarot:
        create_ai(ai_id, f'מאמר {maamar}', 'ספר יצירה - מאמרות')
        ai_id += 1
        created += 1
    print(f"  {len(maamarot)} נוצרו")

    # 10 ספירות (שמות)
    sfirot = ['כתר', 'חכמה', 'בינה', 'חסד', 'גבורה',
              'תפארת', 'נצח', 'הוד', 'יסוד', 'מלכות']
    print("\n10 ספירות:")
    for sfira in sfirot:
        create_ai(ai_id, f'ספירה {sfira}', 'ספר יצירה - ספירות')
        ai_id += 1
        created += 1
    print(f"  {len(sfirot)} נוצרו")

    # צירופי יה"ו (6 צירופים × 6 קצוות = 36) + 10 = 46
    print("\n46 צירופי יה\"ו נוספים:")
    tzirufim = ['יהו', 'יוה', 'היו', 'הוי', 'ויה', 'והי']
    for i, tz in enumerate(tzirufim):
        for j in range(1, 8):  # 7 לכל צירוף + 4 = 46
            create_ai(ai_id, f'צירוף {tz}.{j}', 'ספר יצירה - צירופים', {'צירוף': tz})
            ai_id += 1
            created += 1
            if created >= 231  # שערים:
                break
        if created >= 231  # שערים:
            break
    print(f"  השלמה עד 179")

    print(f"\nסה\"כ: {created} אי נוצרו")
    print("=" * 50)


if __name__ == "__main__":
    main()
