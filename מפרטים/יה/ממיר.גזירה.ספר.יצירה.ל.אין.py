#!/usr/bin/env python3
"""
ממיר.גזירה.ספר.יצירה.ל.אין.py

גזרות אחורה מספר יצירה (ארץ לשמים)

מקורות:
- 10 ספירות עומק
- 32 נתיבות = 10 + 22
- 231 שערים = 22×21/2
- 6 קצוות × יה"ו = 6 צירופים
- 12 אלכסונן × 5 = 32  # נתיבות פנים
- 7! = 5040 בתים מכפולות

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


def gzira_10_sfirot():
    """גזור 10 ספירות עומק"""
    sfirot = [
        ('עומק ראשית', 'זמן קדימה'),
        ('עומק אחרית', 'זמן אחורה'),
        ('עומק טוב', 'מוסר חיובי'),
        ('עומק רע', 'מוסר שלילי'),
        ('עומק רום', 'מרחב למעלה'),
        ('עומק תחת', 'מרחב למטה'),
        ('עומק מזרח', 'מרחב קדימה'),
        ('עומק מערב', 'מרחב אחורה'),
        ('עומק צפון', 'מרחב שמאל'),
        ('עומק דרום', 'מרחב ימין')
    ]
    return [{'מה': s[0], 'תיאור': s[1]} for s in sfirot]


def gzira_231_shearim():
    """גזור 231 שערים - צירופי 2 אותיות"""
    alef_bet = 'אבגדהוזחטיכלמנסעפצקרשת'
    shearim = []
    for i, a in enumerate(alef_bet):
        for b in alef_bet[i+1:]:
            shearim.append({'מה': f'שער {a}{b}', 'צירוף': f'{a}{b}/{b}{a}'})
    return shearim  # 231


def gzira_6_ktzavot():
    """גזור 6 קצוות עם יה"ו"""
    ktzavot = [
        ('רום', 'יה"ו'),
        ('תחת', 'יו"ה'),
        ('מזרח', 'הי"ו'),
        ('מערב', 'הו"י'),
        ('צפון', 'וי"ה'),
        ('דרום', 'וה"י')
    ]
    return [{'מה': f'קצה {k[0]}', 'חותם': k[1]} for k in ktzavot]


def gzira_12_alakhsonin():
    """גזור 12 אלכסונן"""
    alakhsonin = [
        'מזרח-רום', 'מזרח-תחת',
        'מערב-רום', 'מערב-תחת',
        'צפון-רום', 'צפון-תחת',
        'דרום-רום', 'דרום-תחת',
        'מזרח-צפון', 'מזרח-דרום',
        'מערב-צפון', 'מערב-דרום'
    ]
    return [{'מה': f'אלכסון {a}'} for a in alakhsonin]


def gzira_3_yotzrim():
    """גזור 3 יוצרים (controllers)"""
    yotzrim = [
        ('תלי', 'עולם', 'כמלך על כסאו'),
        ('גלגל', 'שנה', 'כמלך במדינה'),
        ('לב', 'נפש', 'כמלך במלחמה')
    ]
    return [{'מה': f'יוצר {y[0]}', 'ציר': y[1], 'משל': y[2]} for y in yotzrim]


def factorial(n):
    """חשב עצרת"""
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def gzira_batim(n):
    """גזור בתים - צירופי n אותיות"""
    # 2! = 2, 3! = 6, 4! = 24, 5! = 120, 6! = 720, 7! = 5040
    count = factorial(n)
    batim = []
    for i in range(count):
        batim.append({'מה': f'בית {n}!.{i+1:04d}', 'עצרת': n, 'מספר': i+1})
    return batim


def main():
    print("=" * 50)
    print("גזירה אחורה מספר יצירה")
    print("ארץ לשמים")
    print("=" * 50)

    AIN_DIR.mkdir(exist_ok=True)
    ai_id = get_next_id()
    created = 0

    # 10 ספירות עומק
    print("\n10 ספירות עומק:")
    for item in gzira_10_sfirot():
        create_ai(ai_id, item['מה'], 'ספר יצירה - עומק', {'תיאור': item['תיאור']})
        print(f"  {ai_id:03d}: {item['מה']}")
        ai_id += 1
        created += 1

    # 6 קצוות
    print("\n6 קצוות:")
    for item in gzira_6_ktzavot():
        create_ai(ai_id, item['מה'], 'ספר יצירה - קצוות', {'חותם': item['חותם']})
        print(f"  {ai_id:03d}: {item['מה']}")
        ai_id += 1
        created += 1

    # 12 אלכסונן
    print("\n12 אלכסונן:")
    for item in gzira_12_alakhsonin():
        create_ai(ai_id, item['מה'], 'ספר יצירה - אלכסונן')
        print(f"  {ai_id:03d}: {item['מה']}")
        ai_id += 1
        created += 1

    # 3 יוצרים
    print("\n3 יוצרים:")
    for item in gzira_3_yotzrim():
        create_ai(ai_id, item['מה'], 'ספר יצירה - יוצרים', {'ציר': item['ציר'], 'משל': item['משל']})
        print(f"  {ai_id:03d}: {item['מה']}")
        ai_id += 1
        created += 1

    # 231 שערים
    print("\n231 שערים:")
    shearim = gzira_231_shearim()
    for item in shearim:
        create_ai(ai_id, item['מה'], 'ספר יצירה - שערים', {'צירוף': item['צירוף']})
        ai_id += 1
        created += 1
    print(f"  נוצרו {len(shearim)} שערים")

    # בתים - עצרות
    # 2! + 3! + 4! + 5! + 6! + 7! = 2 + 6 + 24 + 120 + 720 + 5040 = 5912
    print("\nבתים (עצרות):")
    for n in range(2, 8):  # 2! עד 7!
        batim = gzira_batim(n)
        for item in batim:
            create_ai(ai_id, item['מה'], f'ספר יצירה - בתים {n}!', {'עצרת': str(n), 'מספר': str(item['מספר'])})
            ai_id += 1
            created += 1
        print(f"  {n}! = {len(batim)} בתים")

    print(f"\nסה\"כ: {created} אי נוצרו מגזירה")
    print("=" * 50)


if __name__ == "__main__":
    main()
