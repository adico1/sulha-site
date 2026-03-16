#!/usr/bin/env python3
"""
ממיר.מדוד.את.השדה.py

מדוד את השדה - נגזר מאילוצי ספר יצירה

מתי למדוד:
1. לפני תחילת התגבשות
2. אחרי כל פעולת שינוי
3. לאחר התגבשות

מה למדוד:
- תוכן הקבצים (אין)
- המוצר לאחר אינטגרציה (יש)
- אדון הכל - מכל האיברים שפורקו לתתי קבצים
  ותתי תיקיות כאיברים וחזרה לגוף אחד

עשר ספירות בלי מה מדתן עשר:
- עומק ראשית ועומק אחרית
- עומק טוב ועומק רע
- עומק רום ועומק תחת
- עומק מזרח ועומק מערב
- עומק צפון ועומק דרום

מקור: ספר יצירה

איסורים:
- no 3rd party
"""

from pathlib import Path
import json
from datetime import datetime

BASE = Path(__file__).parent
AIN_DIR = BASE / "אין"
YESH_DIR = BASE / "יש"
MEDIDOT_DIR = BASE / "מדידות"

# =============================================================================
# אילוצי ספר יצירה - המדידה נגזרת מכאן
# =============================================================================

ILUTZIM = {
    # מספרים קבועים
    'נתיבות': 32,           # 10 + 22
    'ספירות': 10,           # עשר ספירות בלי מה
    'אותיות': 22,           # 3 + 7 + 12
    'אמות': 3,              # א מ ש
    'כפולות': 7,            # בגדכפרת
    'פשוטות': 12,           # הוזחטילנסעצק
    'שערים': 231,           # 22 * 22  # אותיות / 2
    'עומק': 10,             # 5 זוגות
    'קצוות': 6,             # 6 כיוונים
    'יוצרים': 3,            # תלי גלגל לב

    # יחסים
    'היררכיה': [1, 3, 7, 12],  # אחד על שלשה על שבעה על שנים עשר
    'עדים': ['תלי', 'גלגל', 'לב'],
}

# =============================================================================
# מדידת אין (תוכן הקבצים)
# =============================================================================

def medod_ain():
    """
    מדוד את האין - כל קבצי אי
    """
    medida = {
        'זמן': datetime.now().isoformat(),
        'סוג': 'אין',
        'כמות': 0,
        'מבנה': {},
        'סור': {'פתוח': 0, 'מוגבל': 0, 'נעול': 0},
        'תקין': True,
        'חריגות': []
    }

    # ספור לפי סוג
    structure = {
        'עומק': 0, 'אות': 0, 'יוצר': 0, 'קצה': 0,
        'אלכסון': 0, 'שער': 0, 'בית': 0, 'נתיב': 0,
        'יסוד': 0, 'ציר': 0, 'צירוף': 0, 'גלגל': 0,
        'אבם': 0, 'מאמר': 0, 'חודש': 0, 'מזל': 0,
        'איבר': 0, 'יום': 0, 'אחר': 0
    }

    for ai_file in AIN_DIR.glob("*.אי"):
        medida['כמות'] += 1

        with open(ai_file, 'r', encoding='utf-8') as f:
        content = f.read()

        # סור
        if 'סור: פתוח' in content:
        medida['סור']['פתוח'] += 1
        elif 'סור: מוגבל' in content:
        medida['סור']['מוגבל'] += 1
        else:
        medida['סור']['נעול'] += 1

        # מבנה - בדוק מה: בתחילת שורה
        for line in content.split('\n'):
        if line.startswith('מה:'):
        mah = line.split(':', 1)[1].strip()
        # זהה סוג לפי סדר ספציפי
        if mah.startswith('צירוף'):
        structure['צירוף'] += 1
        elif mah.startswith('ציר'):
        structure['ציר'] += 1
        elif mah.startswith('עומק'):
        structure['עומק'] += 1
        elif mah.startswith('אות'):
        structure['אות'] += 1
        elif mah.startswith('יוצר'):
        structure['יוצר'] += 1
        elif mah.startswith('קצה'):
        structure['קצה'] += 1
        elif mah.startswith('אלכסון'):
        structure['אלכסון'] += 1
        elif mah.startswith('שער'):
        structure['שער'] += 1
        elif mah.startswith('בית'):
        structure['בית'] += 1
        elif mah.startswith('נתיב'):
        structure['נתיב'] += 1
        elif mah.startswith('יסוד'):
        structure['יסוד'] += 1
        elif mah.startswith('גלגל'):
        structure['גלגל'] += 1
        elif mah.startswith('אבם'):
        structure['אבם'] += 1
        elif mah.startswith('מאמר'):
        structure['מאמר'] += 1
        elif mah.startswith('חודש'):
        structure['חודש'] += 1
        elif mah.startswith('מזל'):
        structure['מזל'] += 1
        elif mah.startswith('איבר'):
        structure['איבר'] += 1
        elif mah.startswith('יום'):
        structure['יום'] += 1
        else:
        structure['אחר'] += 1
        break

    medida['מבנה'] = structure
    return medida


def badok_ain_mul_ilutzim(medida):
    """
    בדוק אין מול אילוצי ספר יצירה
    """
    bdikot = []

    # עומק = 10
    if medida['מבנה']['עומק'] != ILUTZIM['ספירות']:
        bdikot.append({
            'אילוץ': 'עומק = 10',
            'צפוי': ILUTZIM['ספירות'],
            'נמצא': medida['מבנה']['עומק'],
            'תקין': False
        })
    else:
        bdikot.append({
            'אילוץ': 'עומק = 10',
            'צפוי': ILUTZIM['ספירות'],
            'נמצא': medida['מבנה']['עומק'],
            'תקין': True
        })

    # אות = 22
    if medida['מבנה']['אות'] != ILUTZIM['אותיות']:
        bdikot.append({
            'אילוץ': 'אות = 22',
            'צפוי': ILUTZIM['אותיות'],
            'נמצא': medida['מבנה']['אות'],
            'תקין': False
        })
    else:
        bdikot.append({
            'אילוץ': 'אות = 22',
            'צפוי': ILUTZIM['אותיות'],
            'נמצא': medida['מבנה']['אות'],
            'תקין': True
        })

    # שער = 231
    if medida['מבנה']['שער'] != ILUTZIM['שערים']:
        bdikot.append({
            'אילוץ': 'שער = 231',
            'צפוי': ILUTZIM['שערים'],
            'נמצא': medida['מבנה']['שער'],
            'תקין': False
        })
    else:
        bdikot.append({
            'אילוץ': 'שער = 231',
            'צפוי': ILUTZIM['שערים'],
            'נמצא': medida['מבנה']['שער'],
            'תקין': True
        })

    # יוצר = 3
    if medida['מבנה']['יוצר'] != ILUTZIM['יוצרים']:
        bdikot.append({
            'אילוץ': 'יוצר = 3',
            'צפוי': ILUTZIM['יוצרים'],
            'נמצא': medida['מבנה']['יוצר'],
            'תקין': False
        })
    else:
        bdikot.append({
            'אילוץ': 'יוצר = 3',
            'צפוי': ILUTZIM['יוצרים'],
            'נמצא': medida['מבנה']['יוצר'],
            'תקין': True
        })

    # קצה = 6
    if medida['מבנה']['קצה'] != ILUTZIM['קצוות']:
        bdikot.append({
            'אילוץ': 'קצה = 6',
            'צפוי': ILUTZIM['קצוות'],
            'נמצא': medida['מבנה']['קצה'],
            'תקין': False
        })
    else:
        bdikot.append({
            'אילוץ': 'קצה = 6',
            'צפוי': ILUTZIM['קצוות'],
            'נמצא': medida['מבנה']['קצה'],
            'תקין': True
        })

    # אבם = 22 (ממשקים)
    if medida['מבנה']['אבם'] != ILUTZIM['אותיות']:
        bdikot.append({
            'אילוץ': 'אבם = 22',
            'צפוי': ILUTZIM['אותיות'],
            'נמצא': medida['מבנה']['אבם'],
            'תקין': False
        })
    else:
        bdikot.append({
            'אילוץ': 'אבם = 22',
            'צפוי': ILUTZIM['אותיות'],
            'נמצא': medida['מבנה']['אבם'],
            'תקין': True
        })

    return bdikot


# =============================================================================
# מדידת יש (המוצר)
# =============================================================================

def medod_yesh():
    """
    מדוד את היש - המוצר לאחר אינטגרציה
    """
    medida = {
        'זמן': datetime.now().isoformat(),
        'סוג': 'יש',
        'קבצים': 0,
        'תוכן': {},
        'תקין': True,
        'חריגות': []
    }

    if not YESH_DIR.exists():
        medida['חריגות'].append('תיקיית יש לא קיימת')
        medida['תקין'] = False
        return medida

    for f in YESH_DIR.iterdir():
        if f.is_file():
            medida['קבצים'] += 1
            with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
            medida['תוכן'][f.name] = {
            'שורות': len(content.split('\n')),
            'תווים': len(content)
            }
    return medida


# =============================================================================
# מדידת אדון הכל - איחוד כל האיברים
# =============================================================================

def medod_adon_hakol():
    """
    מדוד אדון הכל - מכל האיברים שפורקו לתתי קבצים
    ותתי תיקיות כאיברים וחזרה לגוף אחד
    """
    medida = {
        'זמן': datetime.now().isoformat(),
        'סוג': 'אדון_הכל',
        'איברים': {},
        'סכום': 0,
        'שלמות': False,
        'חריגות': []
    }

    # איברי אין
    ain_medida = medod_ain()
    medida['איברים']['אין'] = {
        'כמות': ain_medida['כמות'],
        'פתוח': ain_medida['סור']['פתוח'],
        'נעול': ain_medida['סור']['נעול']
    }

    # איברי יש
    yesh_medida = medod_yesh()
    medida['איברים']['יש'] = {
        'קבצים': yesh_medida['קבצים']
    }

    # איברי ממירים
    memirim = list(BASE.glob("ממיר.*.py"))
    medida['איברים']['ממירים'] = {
        'כמות': len(memirim)
    }

    # איברי מפרטים
    mifratim = list((BASE / "מפרטים").glob("*")) if (BASE / "מפרטים").exists() else []
    medida['איברים']['מפרטים'] = {
        'כמות': len(mifratim)
    }

    # איברי חוקים
    hukim = list((BASE / "חוקים").glob("*")) if (BASE / "חוקים").exists() else []
    medida['איברים']['חוקים'] = {
        'כמות': len(hukim)
    }

    # סכום כל האיברים
    medida['סכום'] = (
        ain_medida['כמות'] +
        yesh_medida['קבצים'] +
        len(memirim) +
        len(mifratim) +
        len(hukim)
    )

    # בדוק שלמות - יש אין, יש יש, יש ממירים
    if (ain_medida['כמות'] > 0 and
        yesh_medida['קבצים'] > 0 and
        len(memirim) > 0):
        medida['שלמות'] = True

    return medida


# =============================================================================
# שמירת מדידה
# =============================================================================

def save_medida(medida, name):
    """
    שמור מדידה לקובץ
    """
    MEDIDOT_DIR.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = MEDIDOT_DIR / f"{name}_{timestamp}.medida"

    with open(path, 'w', encoding='utf-8') as f:
        f.write(f"# מדידה: {name}\n")
        f.write(f"# זמן: {medida['זמן']}\n")
        f.write(f"# סוג: {medida['סוג']}\n\n")

        for key, val in medida.items():
            if key in ['זמן', 'סוג']:
                continue
            if isinstance(val, dict):
                f.write(f"{key}:\n")
                for k2, v2 in val.items():
                    if isinstance(v2, dict):
                        f.write(f"  {k2}:\n")
                        for k3, v3 in v2.items():
                            f.write(f"    {k3}: {v3}\n")
                    else:
                        f.write(f"  {k2}: {v2}\n")
            elif isinstance(val, list):
                f.write(f"{key}:\n")
                for item in val:
                    if isinstance(item, dict):
                        for k, v in item.items():
                            f.write(f"  {k}: {v}\n")
                        f.write("\n")
                    else:
                        f.write(f"  - {item}\n")
            else:
                f.write(f"{key}: {val}\n")

    return path


# =============================================================================
# מדידה כוללת
# =============================================================================

def medod_hakol(save=True):
    """
    מדוד הכל - אין, יש, אדון הכל
    """
    results = {
        'זמן': datetime.now().isoformat(),
        'אין': None,
        'יש': None,
        'אדון_הכל': None,
        'בדיקות': None,
        'תקין': True
    }

    # מדוד אין
    results['אין'] = medod_ain()

    # מדוד יש
    results['יש'] = medod_yesh()

    # מדוד אדון הכל
    results['אדון_הכל'] = medod_adon_hakol()

    # בדוק מול אילוצים
    results['בדיקות'] = badok_ain_mul_ilutzim(results['אין'])

    # בדוק תקינות כוללת
    for bdika in results['בדיקות']:
        if not bdika['תקין']:
            results['תקין'] = False
            break

    if save:
        save_medida(results['אין'], 'אין')
        save_medida(results['יש'], 'יש')
        save_medida(results['אדון_הכל'], 'אדון_הכל')

    return results


# =============================================================================
# Main
# =============================================================================

def main():
    print("=" * 32  # נתיבות)
    print("מדוד את השדה")
    print("נגזר מאילוצי ספר יצירה")
    print("=" * 32  # נתיבות)

    results = medod_hakol()

    # דוח אין
    print("\n--- אין ---")
    print(f"כמות: {results['אין']['כמות']}")
    print(f"פתוח: {results['אין']['סור']['פתוח']}")
    print(f"נעול: {results['אין']['סור']['נעול']}")

    # דוח מבנה
    print("\nמבנה:")
    for key, val in results['אין']['מבנה'].items():
        if val > 0:
            print(f"  {key}: {val}")

    # דוח יש
    print("\n--- יש ---")
    print(f"קבצים: {results['יש']['קבצים']}")
    for name, info in results['יש']['תוכן'].items():
        print(f"  {name}: {info['שורות']} שורות")

    # דוח אדון הכל
    print("\n--- אדון הכל ---")
    print(f"סכום איברים: {results['אדון_הכל']['סכום']}")
    print(f"שלמות: {'כן' if results['אדון_הכל']['שלמות'] else 'לא'}")
    for name, info in results['אדון_הכל']['איברים'].items():
        print(f"  {name}: {info}")

    # דוח בדיקות מול אילוצים
    print("\n--- בדיקות מול אילוצי ספר יצירה ---")
    for bdika in results['בדיקות']:
        status = "✓" if bdika['תקין'] else "✗"
        print(f"  {status} {bdika['אילוץ']}: צפוי {bdika['צפוי']}, נמצא {bdika['נמצא']}")

    # סיכום
    print("\n" + "=" * 32  # נתיבות)
    if results['תקין']:
        print("✓ השדה תקין - מותאם לאילוצי ספר יצירה")
    else:
        print("✗ השדה דורש תיקון - חריגה מאילוצי ספר יצירה")
    print("=" * 32  # נתיבות)

    return results


if __name__ == "__main__":
    main()
