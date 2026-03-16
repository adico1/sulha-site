#!/usr/bin/env python3
"""
ממיר.מפרטי.בדיקות.עומק.py

מפרטי בדיקות נגזרות מהספירות עומק
מארץ לשמים ומשמים לארץ
עד שמתגלות כל היחידות שבין ובין

עשר ספירות בלי מה:
עומק ראשית ועומק אחרית
עומק טוב ועומק רע
עומק רום ועומק תחת
עומק מזרח ועומק מערב
עומק צפון ועומק דרום

מקור: ספר יצירה פרק א משנה ה

איסורים:
- no 3rd party
"""

from pathlib import Path

BASE = Path(__file__).parent
AIN_DIR = BASE / "אין"
MIFRATIM_DIR = BASE / "מפרטים"

# =============================================================================
# עשר ספירות עומק
# =============================================================================

OMEK_PAIRS = [
    ('ראשית', 'אחרית', 'זמן', 'התחלה וסוף'),
    ('טוב', 'רע', 'ערך', 'חיובי ושלילי'),
    ('רום', 'תחת', 'גובה', 'למעלה ולמטה'),
    ('מזרח', 'מערב', 'רוחב', 'מקדם ולאחור'),
    ('צפון', 'דרום', 'אורך', 'ימין ושמאל'),
]

# =============================================================================
# מארץ לשמים - מתתי איסורים ומעלה
# =============================================================================

def me_eretz_l_shamayim():
    """
    מארץ לשמים - בדיקה מלמטה למעלה
    מתתי איסורים (מערכת קבצים) עד למעלה (ספר יצירה)
    """
    levels = []

    # רמה 1: מערכת קבצים (ארץ)
    level_1 = {
        'שם': 'מערכת קבצים',
        'עומק': 'תחת',
        'בדיקות': [
            'קובץ_קיים',
            'סיומת_תקינה',
            'לא_ריק',
            'בתוך_גבולות',
        ],
        'כיוון': 'מלמטה'
    }
    levels.append(level_1)

    # רמה 2: Python
    level_2 = {
        'שם': 'python',
        'עומק': 'מערב',
        'בדיקות': [
            'no_3rd_party',
            'utf8_encoding',
            'no_eval',
            'syntax_valid',
        ],
        'כיוון': 'מלמטה'
    }
    levels.append(level_2)

    # רמה 3: אדם → חי העולמים
    level_3 = {
        'שם': 'אדם → חי העולמים',
        'עומק': 'צפון',
        'בדיקות': [
            'לא_לדבר_לריק',
            'bus_חכמה',
            'שולח_מזוהה',
            'direction_correct',
        ],
        'כיוון': 'מלמטה'
    }
    levels.append(level_3)

    # רמה 4: ספר יצירה (שמים)
    level_4 = {
        'שם': 'ספר יצירה',
        'עומק': 'רום',
        'בדיקות': [
            'נגזר_מספר_יצירה',
            'שלשה_ספרים',
            'עדים_נאמנין',
            'נתיבות_32',
        ],
        'כיוון': 'מלמטה'
    }
    levels.append(level_4)

    return levels


def mi_shamayim_l_eretz():
    """
    משמים לארץ - בדיקה מלמעלה למטה
    מספר יצירה (שמים) עד למטה (מערכת קבצים)
    """
    levels = []

    # רמה 1: ספר יצירה (שמים)
    level_1 = {
        'שם': 'ספר יצירה',
        'עומק': 'ראשית',
        'בדיקות': [
            'מקור_תקין',
            'גזירה_נכונה',
            'חתימה_תקינה',
            'עדים_אימתו',
        ],
        'כיוון': 'מלמעלה'
    }
    levels.append(level_1)

    # רמה 2: אדם → חי העולמים
    level_2 = {
        'שם': 'אדם → חי העולמים',
        'עומק': 'דרום',
        'בדיקות': [
            'מקבל_מזוהה',
            'ערוץ_פתוח',
            'הודעה_הגיעה',
            'אישור_קבלה',
        ],
        'כיוון': 'מלמעלה'
    }
    levels.append(level_2)

    # רמה 3: Python
    level_3 = {
        'שם': 'python',
        'עומק': 'מזרח',
        'בדיקות': [
            'הרצה_תקינה',
            'פלט_צפוי',
            'לא_חריגות',
            'משאבים_תקינים',
        ],
        'כיוון': 'מלמעלה'
    }
    levels.append(level_3)

    # רמה 4: מערכת קבצים (ארץ)
    level_4 = {
        'שם': 'מערכת קבצים',
        'עומק': 'אחרית',
        'בדיקות': [
            'נכתב_למערכת',
            'קובץ_נוצר',
            'תוכן_שמור',
            'גיבוי_קיים',
        ],
        'כיוון': 'מלמעלה'
    }
    levels.append(level_4)

    return levels


# =============================================================================
# יחידות בין ובין
# =============================================================================

def galeh_yechidot_bein_u_vein(level_above, level_below):
    """
    גלה יחידות שבין ובין
    מה שמתגלה בין שתי רמות
    """
    yechidot = []

    # יחידת קישור
    yechidot.append({
        'סוג': 'קישור',
        'מ': level_above['שם'],
        'אל': level_below['שם'],
        'עומק_מ': level_above['עומק'],
        'עומק_אל': level_below['עומק'],
        'תפקיד': 'מגשר בין רמות'
    })

    # יחידת תרגום
    yechidot.append({
        'סוג': 'תרגום',
        'מ': level_above['עומק'],
        'אל': level_below['עומק'],
        'תפקיד': 'מתרגם בין עומקים'
    })

    # יחידת אימות
    yechidot.append({
        'סוג': 'אימות',
        'בדיקות_מעל': level_above['בדיקות'],
        'בדיקות_מתחת': level_below['בדיקות'],
        'תפקיד': 'מוודא עקביות'
    })

    return yechidot


def galeh_kol_yechidot():
    """
    גלה כל היחידות שבין ובין
    """
    eretz_shamayim = me_eretz_l_shamayim()
    shamayim_eretz = mi_shamayim_l_eretz()

    all_yechidot = []

    # מארץ לשמים
    for i in range(len(eretz_shamayim) - 1):
        yechidot = galeh_yechidot_bein_u_vein(
            eretz_shamayim[i + 1],
            eretz_shamayim[i]
        )
        all_yechidot.extend(yechidot)

    # משמים לארץ
    for i in range(len(shamayim_eretz) - 1):
        yechidot = galeh_yechidot_bein_u_vein(
            shamayim_eretz[i],
            shamayim_eretz[i + 1]
        )
        all_yechidot.extend(yechidot)

    return all_yechidot


# =============================================================================
# מפרט בדיקות לכל עומק
# =============================================================================

def create_omek_mifrat(omek_name, omek_pair):
    """
    צור מפרט בדיקות לעומק
    """
    a, b, dimension, desc = omek_pair

    mifrat = {
        'שם': f'עומק {omek_name}',
        'זוג': (a, b),
        'מימד': dimension,
        'תיאור': desc,
        'בדיקות': []
    }

    # בדיקות לפי מימד
    if dimension == 'זמן':
        mifrat['בדיקות'] = [
            'התחלה_מוגדרת',
            'סיום_מוגדר',
            'רצף_תקין',
            'אין_קפיצות',
        ]
    elif dimension == 'ערך':
        mifrat['בדיקות'] = [
            'ערך_חיובי_מזוהה',
            'ערך_שלילי_מזוהה',
            'מכריע_בינתיים',
            'איזון_נשמר',
        ]
    elif dimension == 'גובה':
        mifrat['בדיקות'] = [
            'רמה_עליונה_נגישה',
            'רמה_תחתונה_נגישה',
            'מעבר_תקין',
            'היררכיה_שמורה',
        ]
    elif dimension == 'רוחב':
        mifrat['בדיקות'] = [
            'קדימה_אפשרי',
            'אחורה_אפשרי',
            'כיוון_מזוהה',
            'מסלול_תקין',
        ]
    elif dimension == 'אורך':
        mifrat['בדיקות'] = [
            'ימין_מזוהה',
            'שמאל_מזוהה',
            'צד_נבחר',
            'סימטריה_שמורה',
        ]

    return mifrat


def create_all_mifratim():
    """
    צור כל מפרטי הבדיקות לעשר עומק
    """
    mifratim = []

    for pair in OMEK_PAIRS:
        a, b, dim, desc = pair

        # מפרט לעומק א
        mifrat_a = create_omek_mifrat(a, pair)
        mifratim.append(mifrat_a)

        # מפרט לעומק ב
        mifrat_b = create_omek_mifrat(b, pair)
        mifratim.append(mifrat_b)

    return mifratim


# =============================================================================
# כתיבת מפרטים
# =============================================================================

def write_mifratim(mifratim):
    """
    כתוב מפרטי בדיקות לקבצים
    """
    MIFRATIM_DIR.mkdir(exist_ok=True)

    # מפרט כללי
    main_path = MIFRATIM_DIR / "עומק.מפרט"
    with open(main_path, 'w', encoding='utf-8') as f:
        f.write("# מפרטי בדיקות עומק\n")
        f.write("# עשר ספירות בלי מה מדתן עשר\n\n")

        f.write("מקור: ספר יצירה פרק א משנה ה\n\n")

        f.write("עומקים:\n")
        for pair in OMEK_PAIRS:
            a, b, dim, desc = pair
            f.write(f"  {a} ↔ {b}: {dim} ({desc})\n")

        f.write("\n")
        f.write("כיוונים:\n")
        f.write("  מארץ לשמים: תחת → רום\n")
        f.write("  משמים לארץ: ראשית → אחרית\n")

        f.write("\n")
        f.write(f"סה\"כ מפרטים: {len(mifratim)}\n")

    # מפרט לכל עומק
    for mifrat in mifratim:
        omek_name = mifrat['שם'].replace('עומק ', '')
        path = MIFRATIM_DIR / f"{omek_name}.עומק.מפרט"

        with open(path, 'w', encoding='utf-8') as f:
            f.write(f"# {mifrat['שם']}\n\n")
            f.write(f"זוג: {mifrat['זוג'][0]} ↔ {mifrat['זוג'][1]}\n")
            f.write(f"מימד: {mifrat['מימד']}\n")
            f.write(f"תיאור: {mifrat['תיאור']}\n\n")

            f.write("בדיקות:\n")
            for b in mifrat['בדיקות']:
                f.write(f"  - {b}\n")

    return main_path


def write_yechidot(yechidot):
    """
    כתוב יחידות בין ובין
    """
    path = MIFRATIM_DIR / "יחידות.בין.ובין"
    with open(path, 'w', encoding='utf-8') as f:
        f.write("# יחידות בין ובין\n")
        f.write("# מתגלות במעבר בין רמות\n\n")

        f.write(f"סה\"כ יחידות: {len(yechidot)}\n\n")

        by_type = {}
        for y in yechidot:
            t = y['סוג']
            if t not in by_type:
                by_type[t] = []
            by_type[t].append(y)

        for sug, items in by_type.items():
            f.write(f"\n{sug}:\n")
            for item in items:
                if 'מ' in item and 'אל' in item:
                    f.write(f"  {item['מ']} → {item['אל']}: {item['תפקיד']}\n")
                else:
                    f.write(f"  {item['תפקיד']}\n")

    return path


def write_eretz_shamayim():
    """
    כתוב מפרט מארץ לשמים ומשמים לארץ
    """
    path = MIFRATIM_DIR / "ארץ.שמים.מפרט"

    eretz_shamayim = me_eretz_l_shamayim()
    shamayim_eretz = mi_shamayim_l_eretz()

    with open(path, 'w', encoding='utf-8') as f:
        f.write("# מארץ לשמים ומשמים לארץ\n\n")

        f.write("מארץ לשמים (מלמטה למעלה):\n")
        for i, level in enumerate(eretz_shamayim):
            f.write(f"  {i+1}. {level['שם']} (עומק {level['עומק']})\n")
            for b in level['בדיקות']:
                f.write(f"     - {b}\n")

        f.write("\n")
        f.write("משמים לארץ (מלמעלה למטה):\n")
        for i, level in enumerate(shamayim_eretz):
            f.write(f"  {i+1}. {level['שם']} (עומק {level['עומק']})\n")
            for b in level['בדיקות']:
                f.write(f"     - {b}\n")

    return path


# =============================================================================
# הרצת בדיקות
# =============================================================================

def run_omek_tests():
    """
    הרץ בדיקות עומק על אין
    """
    results = {
        'עומק': {},
        'תקין': 0,
        'נכשל': 0
    }

    for pair in OMEK_PAIRS:
        a, b, dim, desc = pair

        # בדוק עומק a
        a_file = AIN_DIR / f"עומק {a}.אי"
        results['עומק'][a] = {
            'קיים': a_file.exists(),
            'מימד': dim
        }
        if a_file.exists():
            results['תקין'] += 1
        else:
            results['נכשל'] += 1

        # בדוק עומק b
        b_file = AIN_DIR / f"עומק {b}.אי"
        results['עומק'][b] = {
            'קיים': b_file.exists(),
            'מימד': dim
        }
        if b_file.exists():
            results['תקין'] += 1
        else:
            results['נכשל'] += 1

    return results


# =============================================================================
# Main
# =============================================================================

def main():
    print("=" * 32  # נתיבות)
    print("מפרטי בדיקות עומק")
    print("מארץ לשמים ומשמים לארץ")
    print("=" * 32  # נתיבות)

    # צור מפרטי עומק
    print("\nיוצר מפרטי בדיקות לעשר עומק...")
    mifratim = create_all_mifratim()
    print(f"  {len(mifratim)} מפרטים")

    # גלה יחידות בין ובין
    print("\nמגלה יחידות בין ובין...")
    yechidot = galeh_kol_yechidot()
    print(f"  {len(yechidot)} יחידות")

    # כתוב מפרטים
    print("\nכותב מפרטים...")
    main_path = write_mifratim(mifratim)
    print(f"  {main_path}")

    yechidot_path = write_yechidot(yechidot)
    print(f"  {yechidot_path}")

    eretz_path = write_eretz_shamayim()
    print(f"  {eretz_path}")

    # הרץ בדיקות
    print("\nמריץ בדיקות עומק...")
    results = run_omek_tests()
    print(f"  תקין: {results['תקין']}")
    print(f"  נכשל: {results['נכשל']}")

    # סיכום
    print("\n" + "=" * 32  # נתיבות)
    print("עשר ספירות בלי מה מדתן עשר:")
    for pair in OMEK_PAIRS:
        a, b, dim, desc = pair
        a_ok = results['עומק'].get(a, {}).get('קיים', False)
        b_ok = results['עומק'].get(b, {}).get('קיים', False)
        status_a = "✓" if a_ok else "✗"
        status_b = "✓" if b_ok else "✗"
        print(f"  {status_a} {a} ↔ {status_b} {b} ({dim})")

    print("\n" + "=" * 32  # נתיבות)
    print("מארץ לשמים: תחת → צפון → מערב → רום")
    print("משמים לארץ: ראשית → דרום → מזרח → אחרית")
    print("=" * 32  # נתיבות)


if __name__ == "__main__":
    main()
