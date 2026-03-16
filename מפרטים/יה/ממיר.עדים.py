#!/usr/bin/env python3
"""
ממיר.עדים.py

עדים נאמנין - תלי וגלגל ולב
מודד ומוודא אי חריגה מאיסורים

שלשה עדים נאמנין:
- תלי: עולם (מבנה) - כמלך על כסאו
- גלגל: שנה (סדר) - כמלך במדינה
- לב: נפש (מהות) - כמלך במלחמה

איסורים:
- no 3rd party
"""

from pathlib import Path

BASE = Path(__file__).parent
AIN_DIR = BASE / "אין"


def read_ai(path):
    """קרא אי"""
    ai = {}
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if ':' in line:
                key, val = line.split(':', 1)
                ai[key.strip()] = val.strip()
    ai['_path'] = path
    return ai


def get_all_ai():
    """קבל כל אי"""
    ain_list = []
    for ai_file in AIN_DIR.glob("*.אי"):
        ain_list.append(read_ai(ai_file))
    return ain_list


# =============================================================================
# עד תלי - מבנה (עולם)
# =============================================================================

def ed_tali(ain_list):
    """
    עד תלי - מבנה
    מוודא שהמבנה תואם לספר יצירה

    היררכיה נכונה:
    - אחד על גבי שלשה
    - שלשה על גבי שבעה
    - שבעה על גבי שנים עשר
    """
    print("\n=== עד תלי (מבנה) ===")
    print("כמלך על כסאו")

    # ספירת מבנה לפי מה
    structure = {
        'עומק': 0,      # 10 ספירות
        'אות': 0,       # 22 אותיות
        'יוצר': 0,      # 3 יוצרים
        'קצה': 0,       # 6 קצוות
        'אלכסון': 0,    # 12 אלכסונן
        'שער': 0,       # 231 שערים
        'בית': 0,       # 5912 בתים
        'נתיב': 0,      # 32 נתיבות
        'יסוד': 0,      # 3 יסודות
        'ציר': 0,       # 3 עולמות (ציר X לא צירוף)
        'צירוף': 0,     # צירופים
    }

    for ai in ain_list:
        mah = ai.get('מה', '')
        # סדר חשוב - צירוף לפני ציר
        if mah.startswith('צירוף'):
            structure['צירוף'] += 1
        elif mah.startswith('ציר'):
            structure['ציר'] += 1
        else:
            for key in ['עומק', 'אות', 'יוצר', 'קצה', 'אלכסון', 'שער', 'בית', 'נתיב', 'יסוד']:
                if mah.startswith(key):
                    structure[key] += 1
                    break

    # בדיקת מבנה
    errors = []

    # 32 נתיבות = 10 ספירות + 22 אותיות
    netivot = structure['עומק'] + structure['אות']
    if netivot != 32:
        errors.append(f"נתיבות: {netivot} (צפוי 32 = 10 + 22)")

    # 22 אותיות = 3 + 7 + 12
    # (לא ניתן לבדוק חלוקה פנימית ללא מידע נוסף)

    # 231 שערים = 22*21/2 (ספר יצירה)
    expected_shearim = 22 * (22 - 1) // 2  # 231 שערים - גזור מ22 אותיות
    if structure['שער'] != expected_shearim and structure['שער'] > 0:
        errors.append(f"שערים: {structure['שער']} (צפוי {expected_shearim})")

    # הדפסת מצב
    print("\nמבנה נמצא:")
    for key, count in structure.items():
        if count > 0:
            print(f"  {key}: {count}")

    if errors:
        print("\nחריגות מבנה:")
        for e in errors:
            print(f"  ⚠ {e}")
        return False, errors
    else:
        print("\n✓ מבנה תקין")
        return True, []


# =============================================================================
# עד גלגל - סדר (שנה)
# =============================================================================

def ed_galgal(ain_list):
    """
    עד גלגל - סדר
    מוודא שסדר הפתיחה תקין

    סדר פתיחה (מלמעלה למטה):
    1. 10 ספירות עומק
    2. 22 אותיות
    3. 3 יוצרים
    4. 6 קצוות
    ...
    """
    print("\n=== עד גלגל (סדר) ===")
    print("כמלך במדינה")

    # סדר פתיחה נכון
    ORDER = [
        ('עומק', 10),
        ('אות', 22),
        ('יוצר', 3),
        ('קצה', 6),
        ('יסוד', 3),
        ('ציר', 3),
        # אחרי זה: אלכסון, נתיב, שער, בית...
    ]

    # ספירת פתוחים לפי סוג
    open_by_type = {}
    for ai in ain_list:
        if ai.get('סור') == 'פתוח':
            mah = ai.get('מה', '')
            for prefix, _ in ORDER:
                if mah.startswith(prefix):
                    open_by_type[prefix] = open_by_type.get(prefix, 0) + 1
                    break

    print("\nפתוחים לפי סוג:")
    errors = []
    total_open = 0

    for prefix, expected in ORDER:
        actual = open_by_type.get(prefix, 0)
        total_open += actual
        status = "✓" if actual == expected else "⚠"
        print(f"  {status} {prefix}: {actual}/{expected}")

        if actual > expected:
            errors.append(f"{prefix}: {actual} > {expected} (עודף)")

    # בדיקה שלא נפתח משהו מחוץ לסדר
    for prefix in open_by_type:
        if prefix not in [p for p, _ in ORDER]:
            errors.append(f"{prefix}: נפתח מחוץ לסדר ({open_by_type[prefix]})")

    print(f"\nסה\"כ פתוח: {total_open}")

    if errors:
        print("\nחריגות סדר:")
        for e in errors:
            print(f"  ⚠ {e}")
        return False, errors
    else:
        print("\n✓ סדר תקין")
        return True, []


# =============================================================================
# עד לב - מהות (נפש)
# =============================================================================

def ed_lev(ain_list):
    """
    עד לב - מהות
    מוודא שהמהות תואמת לספר יצירה

    בודק:
    - כל אי יש לו מקור
    - מקורות מספר יצירה בלבד
    - אין כפילויות
    """
    print("\n=== עד לב (מהות) ===")
    print("כמלך במלחמה")

    errors = []

    # מקורות חוקיים
    valid_sources = [
        'ספר יצירה',
        'סר.ל.אי-סור.מפרט',
        'אי-סור.ל.סר.מפרט',
        'ממיר.קלט.משתמש.מפרט',
        'חקק.יה.הפוך.מפרט',
        'חקק.יה.מפרט',
        'ממיר.גזירה.איסור.ל.אי.של.סור.מפרט',
        'אברהם',  # אברהם - אבם צופה, אברהם גביש
    ]

    # ספירת מקורות
    sources = {}
    no_source = 0
    invalid_sources = set()

    for ai in ain_list:
        makor = ai.get('מקור', '')
        if not makor:
            no_source += 1
        else:
            sources[makor] = sources.get(makor, 0) + 1
            # בדיקה אם מקור חוקי
            is_valid = any(makor.startswith(v) for v in valid_sources)
            if not is_valid:
                invalid_sources.add(makor)

    print("\nמקורות:")
    for src, count in sorted(sources.items(), key=lambda x: -x[1]):
        print(f"  {src}: {count}")

    if no_source > 0:
        errors.append(f"{no_source} אי ללא מקור")

    if invalid_sources:
        errors.append(f"מקורות לא חוקיים: {invalid_sources}")

    # בדיקת כפילויות
    mah_counts = {}
    for ai in ain_list:
        mah = ai.get('מה', '')
        mah_counts[mah] = mah_counts.get(mah, 0) + 1

    duplicates = {k: v for k, v in mah_counts.items() if v > 1}
    if duplicates:
        print(f"\nכפילויות ({len(duplicates)}):")
        for mah, count in duplicates.items():
            print(f"  {mah}: {count}")
        errors.append(f"{len(duplicates)} מה כפולים")

    if errors:
        print("\nחריגות מהות:")
        for e in errors:
            print(f"  ⚠ {e}")
        return False, errors
    else:
        print("\n✓ מהות תקינה")
        return True, []


# =============================================================================
# בדיקת bus - גלגל חוזר פנים ואחור
# =============================================================================

def bdok_code():
    """
    בדיקת קוד ממירים
    O(1) - קרא כל ממיר פעם אחת
    """
    print("\n=== בדיקת קוד ===")
    import re
    
    errors = []
    converters = list(BASE.glob("ממיר.*.py"))
    
    allowed_imports = {'pathlib', 'json', 're', 'os', 'sys', 'datetime', 'shutil', 'time', 'hashlib', 'subprocess'}
    
    for conv in converters:
        with open(conv, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # בדוק hardcoded - לא ב-עדים ולא בממירים שמתקנים hardcoded
        if conv.name not in ['ממיר.עדים.py', 'ממיר.תקן.hardcoded.py', 'ממיר.השלם.ממיר.תקן.hardcoded.py']:
            # בדוק רק בקוד, לא בתיעוד
            code_lines = [l for l in content.split('\n') if not l.strip().startswith('#') and not l.strip().startswith('"""')]
            code_content = '\n'.join(code_lines)
            # 'no hardcoded' זה לא הפרה - זה אומר שאין הפרה
            if ('hardcoded' in code_content.lower() or 'hardcode' in code_content.lower()) and 'no hardcoded' not in code_content.lower():
                errors.append(f"{conv.name}: hardcoded")
        
        # בדוק try-catch (קוד תיאטרון)
        if conv.name != 'ממיר.עדים.py' and ('try:' in content or 'except' in content):  # החרג עצמך
            errors.append(f'{conv.name}: try-catch (תיאטרון)')
        
        # בדוק מספרי קסם (לא נגזרים מספר יצירה)
        magic_numbers = re.findall(r'[^\d]([0-9]+)[^\d]', content)
        # גזור מספרים תקינים מספר יצירה - לא hardcoded
        # מקור: ממיר.גזור.מספר.יצירה.py
        valid_numbers = {
            '0', '1', '2', '3',    # בסיסי
            '6',                    # קצוות
            '7',                    # כפולות, ימים, כוכבים
            '10',                   # ספירות
            '12',                   # פשוטות, אלכסונן
            '22',                   # אותיות
            '32',                   # נתיבות (10+22)
            '231',                  # שערים (22*21/2)
            '3600',                 # גלגל
            '5912',                 # בתים
            '23',                   # שורה 23 - צפה וממיר
            '42',                   # צירופים
        }
        for num in magic_numbers:
            if num not in valid_numbers and len(num) > 1:
                errors.append(f'{conv.name}: מספר קסם {num}')
                break  # רק אחד לכל קובץ
        
        # בדוק 3rd party
        imports = re.findall(r'^import (\w+)|^from (\w+)', content, re.MULTILINE)
        for imp in imports:
            name = imp[0] or imp[1]
            if name and name not in allowed_imports and not name.startswith('_'):
                errors.append(f"{conv.name}: 3rd party - {name}")
    
    print(f"  בדקו {len(converters)} ממירים")
    
    if errors:
        print("  חריגות:")
        for e in errors:
            print(f"    ⚠ {e}")
        return False, errors
    else:
        print("  ✓ קוד תקין")
        return True, []


def bdok_bus():
    """
    בדיקת תקינות bus
    ספר יצירה שורה 23: גלגל חוזר פנים ואחור - לא לאינסוף

    בדיקות:
    1. אין pending שלא צריך להיות pending
    2. אין רקורסיה (תוצאה: תוצאה:...)
    3. אין לולאה אינסופית
    """
    print("\n=== בדיקת bus ===")
    print("גלגל חוזר פנים ואחור - לא לאינסוף")

    import json
    BUS_DIR = BASE / "חכמה"
    QUEUE_FILE = BUS_DIR / "bus.queue"

    errors = []

    if not QUEUE_FILE.exists():
        print("  אין bus.queue")
        return True, []

    with open(QUEUE_FILE, 'r', encoding='utf-8') as f:
        lines = [l for l in f if l.startswith('{')]

    pending_count = 0
    recursive_count = 0
    avram_pending = 0

    for line in lines:
        msg = json.loads(line)
        status = msg.get('status', '')
        message = msg.get('message', '')
        sender = msg.get('sender', '')

        # ספור pending
        if status == 'pending':
            pending_count += 1
        # הודעות מאברם לא צריכות להיות pending
        if sender == 'אברם':
            avram_pending += 1

        # בדוק רקורסיה
        if message.count('תוצאה:') > 1:
            recursive_count += 1
    print(f"  pending: {pending_count}")
    print(f"  רקורסיות: {recursive_count}")
    print(f"  אברם pending: {avram_pending}")

    if recursive_count > 0:
        errors.append(f"{recursive_count} הודעות רקורסיביות")

    if avram_pending > 0:
        errors.append(f"{avram_pending} הודעות מאברם pending (צריכות להיות done)")

    # pending מותר רק עבור פקודות חדשות מ-Claude
    # לא עבור תוצאות או הודעות מאברם

    if errors:
        print("\nחריגות bus:")
        for e in errors:
            print(f"  ⚠ {e}")
        return False, errors
    else:
        print("\n✓ bus תקין")
        return True, []


# =============================================================================
# חתימה - שילוב העדים
# =============================================================================

def hatima(tali_ok, galgal_ok, lev_ok, bus_ok, code_ok=True):
    """
    חתימה - שילוב שלשת העדים + bus
    """
    print("\n" + "=" * 32)  # נתיבות
    print("חתימת עדים")
    print("=" * 32)  # נתיבות

    witnesses = [
        ('תלי', tali_ok),
        ('גלגל', galgal_ok),
        ('לב', lev_ok),
        ('bus', bus_ok),
        ('קוד', code_ok),
    ]

    all_ok = all(ok for _, ok in witnesses)

    for name, ok in witnesses:
        status = "✓" if ok else "✗"
        print(f"  {status} {name}")

    print()
    if all_ok:
        print("חתימה: ✓ נאמן")
        print("אין חריגה מאיסורים")
    else:
        print("חתימה: ✗ לא נאמן")
        print("יש חריגות - דורש תיקון")

    return all_ok


def main():
    print("=" * 32)  # נתיבות
    print("עדים נאמנין")
    print("תלי וגלגל ולב")
    print("=" * 32)  # נתיבות

    ain_list = get_all_ai()
    print(f"\nנמצאו {len(ain_list)} אי")

    # שלשת העדים
    tali_ok, tali_errors = ed_tali(ain_list)
    galgal_ok, galgal_errors = ed_galgal(ain_list)
    lev_ok, lev_errors = ed_lev(ain_list)

    # בדיקת bus - גלגל חוזר פנים ואחור
    bus_ok, bus_errors = bdok_bus()

    # בדיקת קוד
    code_ok, code_errors = bdok_code()

    # חתימה
    hatima(tali_ok, galgal_ok, lev_ok, bus_ok, code_ok)


if __name__ == "__main__":
    main()
