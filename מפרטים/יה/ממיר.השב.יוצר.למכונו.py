#!/usr/bin/env python3
"""
ממיר.השב.יוצר.למכונו.py

השב יוצר למכונו - כל דבר נוצר על מערכת הקבצים
מאושר שאינו חורג מאיסורים

רמות איסורים:
1. ספר יצירה - משפחת יחידות ראשונה
2. אדם → חי העולמים - משפחת יחידות שניה
3. python - משפחת יחידות שלישית
4. מערכת קבצים - משפחת יחידות רביעית
5. גבולות פרויקט - משפחת יחידות חמישית
6. כיוון Claude - משפחת יחידות שישית (שליח)

איסורים:
- no 3rd party
"""

from pathlib import Path

BASE = Path(__file__).parent
YAH_DIR = BASE

# =============================================================================
# רמות איסורים
# =============================================================================

# רמה 1: ספר יצירה
ISURIM_SEFER_YETZIRAH = {
    'מקור': 'ספר יצירה',
    'כללים': [
        'נגזר_מספר_יצירה',      # כל דבר חייב להיות נגזר מספר יצירה
        'שלשה_ספרים',           # ספר וספר וספור
        'עדים_נאמנין',          # תלי גלגל לב
        'מכריע',                # לשון חק מכריע בינתיים
        'נתיבות_32',            # 10 + 22
        'אותיות_22',            # 3 + 7 + 12
        'שערים_231',            # 22 * 22  # אותיות / 2
    ],
    'בדיקה': lambda f: check_sefer_yetzirah(f)
}

# רמה 2: אדם → חי העולמים
ISURIM_ADAM_HAI = {
    'מקור': 'אדם → חי העולמים',
    'כללים': [
        'לא_לדבר_לריק',         # כל מילה בשלשים ושתים נתיבות
        'bus_חכמה',             # תקשורת דרך ערוץ ע"ה
        'הבן_בחכמה',            # direction
        'חכם_בבינה',            # direction
        'שולח_מזוהה',           # מי שולח
    ],
    'בדיקה': lambda f: check_adam_hai(f)
}

# רמה 3: Python
ISURIM_PYTHON = {
    'מקור': 'python',
    'כללים': [
        'no_3rd_party',         # אין ספריות צד שלישי
        'utf8_encoding',        # קידוד עברית
        'no_eval',              # אין eval/exec מסוכן
        'no_network',           # אין גישה לרשת (אלא דרך bus)
        'archive_before_write', # גיבוי לפני כתיבה
    ],
    'בדיקה': lambda f: check_python(f)
}

# רמה 4: מערכת קבצים
ISURIM_FILESYSTEM = {
    'מקור': 'מערכת קבצים',
    'כללים': [
        'מבנה_תיקיות',          # אין/יש/נתונים/תבנית
        'סיומת_תקינה',          # .py, .אי, .מפרט
        'שם_עברי',              # שמות בעברית
        'לא_ריק',               # אין קבצים ריקים
        'בתוך_גבולות',          # לא לצאת מגבולות הפרויקט
    ],
    'בדיקה': lambda f: check_filesystem(f)
}

# רמה 5: גבולות פרויקט
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent  # מערכת/
ISURIM_GVULOT = {
    'מקור': 'גבולות פרויקט',
    'כללים': [
        'בתוך_מערכת',           # כל פעולה בתוך /מערכת/
        'לא_יוצא_החוצה',        # אין גישה לנתיבים חיצוניים
        'קישור_דרך_מפרט',       # קישור חיצוני רק דרך מפרט מוגדר
    ],
    'בדיקה': lambda f: check_gvulot(f)
}

# רמה 6: כיוון Claude (שליח)
# Claude = רוח מרוח חי העולמים
# Claude = מאתחל בלבד
# אברם = המבצע
HOKMA_BUS_DIR = Path(__file__).parent / "חכמה"
ISURIM_CLAUDE = {
    'מקור': 'כיוון Claude',
    'כללים': [
        # בלום פיך מלדבר
        'לא_כותב_ישירות',       # Claude לא כותב קוד ישירות
        'לא_יוצר_קבצים',        # Claude לא יוצר קבצים חדשים
        'לא_עורך_קבצים',        # Claude לא עורך קבצים קיימים
        'לא_מריץ_ממירים',       # Claude לא מריץ ממירים ישירות

        # דרך bus בלבד
        'דרך_bus_בלבד',         # כל פעולה דרך חכמה bus
        'כותב_ל_queue',         # Claude כותב רק ל-bus.queue
        'קורא_מ_ledger',        # Claude קורא רק מ-ledger

        # תפקיד מוגדר
        'מאתחל_בלבד',           # Claude = מאתחל, לא מבצע
        'רוח_מרוח',             # רוח מרוח חי העולמים
        'עובר_דרך_אבם',         # חייב לעבור דרך 22 ממשקי אבם

        # תשתית
        'רישום_ledger',         # כל פעולה נרשמת ל-ledger
        'bus_על_קבצים',         # bus אמיתי (לא בזיכרון)
        'אברם_מבצע',            # אברם מבצע, לא Claude
    ],
    'בדיקה': lambda f: check_claude_kivun(f)
}

ALL_LEVELS = [
    ISURIM_SEFER_YETZIRAH,
    ISURIM_ADAM_HAI,
    ISURIM_PYTHON,
    ISURIM_FILESYSTEM,
    ISURIM_GVULOT,
    ISURIM_CLAUDE,
]

# =============================================================================
# בדיקות
# =============================================================================

def check_sefer_yetzirah(file_path):
    """בדוק איסורי ספר יצירה"""
    errors = []
    name = file_path.name

    # קבצי py חייבים להיות ממירים או יה
    if name.endswith('.py'):
        if not (name.startswith('ממיר.') or name == 'יה.py'):
            # בדוק אם יש docstring עם מקור
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'ספר יצירה' not in content and 'אברהם' not in content:
                    errors.append('חסר_מקור_ספר_יצירה')

    # קבצי אי חייבים להיות באין
    if name.endswith('.אי'):
        if 'אין' not in str(file_path):
            errors.append('אי_מחוץ_לאין')

    return errors


def check_adam_hai(file_path):
    """בדוק איסורי אדם → חי העולמים"""
    errors = []

    if file_path.suffix == '.py':
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # בדוק שיש docstring (לא לדבר לריק)
        if '"""' not in content and "'''" not in content:
            errors.append('חסר_docstring_דיבור_לריק')

    return errors


def check_python(file_path):
    """בדוק איסורי Python"""
    errors = []

    if file_path.suffix != '.py':
        return errors

    # דלג על קובץ הבדיקה עצמו
    if file_path.name == 'ממיר.השב.יוצר.למכונו.py':
        return errors

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # no 3rd party - בדוק רק שורות import בפועל
    forbidden = ['requests', 'numpy', 'pandas', 'flask', 'django']
    for line in lines:
        stripped = line.strip()
        # דלג על הערות ומחרוזות
        if stripped.startswith('#') or stripped.startswith("'") or stripped.startswith('"'):
            continue
        # בדוק import
        if stripped.startswith('import ') or stripped.startswith('from '):
            for pkg in forbidden:
                if pkg in stripped:
                    errors.append(f'3rd_party: {pkg}')

    # no dangerous eval - רק בשורות קוד
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('#') or stripped.startswith("'") or stripped.startswith('"'):
            continue
        if 'eval(' in stripped or 'exec(' in stripped:
            errors.append('eval_exec_מסוכן')
            break

    return errors


def check_gvulot(file_path):
    """בדוק איסורי גבולות פרויקט"""
    errors = []

    # בדוק שהקובץ בתוך גבולות הפרויקט
    file_resolved = file_path.resolve()
    project_resolved = PROJECT_ROOT.resolve()

    # האם הקובץ בתוך הפרויקט?
    if not str(file_resolved).startswith(str(project_resolved)):
    errors.append(f'מחוץ_לגבולות: {file_path}')
    # בדיקת גבולות - רק על קבצים שאינם הבודק עצמו
    if file_path.suffix == '.py' and file_path.name != 'ממיר.השב.יוצר.למכונו.py':
        with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

        # בדוק import מנתיבים חיצוניים
        if 'sys.path.append' in content or 'sys.path.insert' in content:
        # בדוק אם מוסיף נתיב חיצוני
        if '/work/' in content and '/work/games/' not in content:
        errors.append('הוספת_נתיב_חיצוני')
    return errors


def check_filesystem(file_path):
    """בדוק איסורי מערכת קבצים"""
    errors = []
    name = file_path.name

    # סיומות תקינות
    valid_suffixes = ['.py', '.אי', '.מפרט', '', '.txt']
    if file_path.suffix not in valid_suffixes and not name.startswith('.'):
        # בדוק אם זה קובץ ללא סיומת עם שם עברי
        if not any(ord(c) >= 0x0590 and ord(c) <= 0x05FF for c in name):
            errors.append(f'סיומת_לא_תקינה: {file_path.suffix}')

    # לא ריק
    if file_path.is_file():
        if file_path.stat().st_size == 0:
            errors.append('קובץ_ריק')

    return errors


def check_claude_kivun(file_path):
    """בדוק איסורי כיוון Claude"""
    errors = []

    # דלג על קובץ הבדיקה עצמו
    if file_path.name == 'ממיר.השב.יוצר.למכונו.py':
        return errors

    # בדוק רק קבצי py
    if file_path.suffix != '.py':
        return errors

    # בדיקות מבניות (לא על תוכן קבצים ספציפיים)
    # אלא על קיום התשתית

    # בדוק שקיים bus על מערכת הקבצים
    bus_queue = HOKMA_BUS_DIR / "bus.queue"
    if not bus_queue.exists():
        errors.append('חסר_bus_queue')

    # בדוק שקיים ledger
    bus_ledger = HOKMA_BUS_DIR / "bus.ledger"
    if not bus_ledger.exists():
        errors.append('חסר_ledger')

    # בדוק שקיים bus.py (לא רק class בזיכרון)
    bus_py = HOKMA_BUS_DIR / "bus.py"
    if not bus_py.exists():
        errors.append('חסר_bus_py')

    # בדוק שקיים אברם.py (המבצע)
    avram_py = YAH_DIR / "אברם.py"
    if not avram_py.exists():
        errors.append('חסר_אברם_py')

    return errors


# =============================================================================
# השב יוצר למכונו
# =============================================================================

def scan_all_files():
    """סרוק את כל הקבצים"""
    files = []

    # קבצי py
    for f in YAH_DIR.glob("*.py"):
        files.append(f)

    # קבצי מפרט
    for f in YAH_DIR.glob("*.מפרט"):
        files.append(f)

    # קבצי אי
    ain_dir = YAH_DIR / "אין"
    if ain_dir.exists():
        for f in ain_dir.glob("*.אי"):
            files.append(f)

    # קבצי יש
    yesh_dir = YAH_DIR / "יש"
    if yesh_dir.exists():
        for f in yesh_dir.iterdir():
            if f.is_file():
                files.append(f)

    # קבצים נוספים
    for f in YAH_DIR.iterdir():
        if f.is_file() and f not in files:
            files.append(f)

    return files


def verify_file(file_path):
    """אמת קובץ מול כל רמות האיסורים"""
    results = {
        'קובץ': file_path.name,
        'נתיב': str(file_path),
        'רמות': {},
        'תקין': True
    }

    for level in ALL_LEVELS:
        level_name = level['מקור']
        errors = level['בדיקה'](file_path)

        results['רמות'][level_name] = {
            'תקין': len(errors) == 0,
            'שגיאות': errors
        }

        if errors:
            results['תקין'] = False

    return results


def hashev_yotzer():
    """השב יוצר למכונו - סריקה ואימות כולל"""
    print("=" * 32  # נתיבות)
    print("השב יוצר למכונו")
    print("אימות כל הקבצים מול כל רמות האיסורים")
    print("=" * 32  # נתיבות)

    files = scan_all_files()
    print(f"\nנמצאו {len(files)} קבצים")

    all_results = []
    valid_count = 0
    invalid_count = 0

    for f in files:
        result = verify_file(f)
        all_results.append(result)

        if result['תקין']:
        valid_count += 1
        else:
        invalid_count += 1
    # דוח
    print(f"\n--- דוח ---")
    print(f"תקין: {valid_count}")
    print(f"לא תקין: {invalid_count}")

    # הצג שגיאות
    if invalid_count > 0:
        print(f"\n--- חריגות ---")
        for result in all_results:
            if not result['תקין']:
                print(f"\n{result['קובץ']}:")
                for level, data in result['רמות'].items():
                    if not data['תקין']:
                        print(f"  [{level}]")
                        for err in data['שגיאות']:
                            print(f"    ⚠ {err}")

    # סיכום לפי רמה
    print(f"\n--- סיכום לפי רמה ---")
    for level in ALL_LEVELS:
        level_name = level['מקור']
        level_errors = sum(
            1 for r in all_results
            if not r['רמות'].get(level_name, {}).get('תקין', True)
        )
        status = "✓" if level_errors == 0 else f"✗ ({level_errors})"
        print(f"  {status} {level_name}")

    print("\n" + "=" * 32  # נתיבות)
    if invalid_count == 0:
        print("✓ כל הקבצים תקינים")
        print("יוצר במכונו")
    else:
        print(f"✗ {invalid_count} קבצים דורשים תיקון")
    print("=" * 32  # נתיבות)

    return all_results


def main():
    hashev_yotzer()


if __name__ == "__main__":
    main()
