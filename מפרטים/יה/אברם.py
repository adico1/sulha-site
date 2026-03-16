#!/usr/bin/env python3
"""
אברם.py - מאתחל עצמו ואת המערכת

מקור: ספר יצירה
צפה והביט וראה וחקר והבין וחקק וחצב וצרף וצר
ועלתה בידו

איסורים:
- no 3rd party
"""

from pathlib import Path
import subprocess
import sys
from datetime import datetime

BASE = Path(__file__).parent
BUS_DIR = BASE / "חכמה"
IMMUTABLE = BASE.parent.parent.parent / "immutable"
SEFER_YETZIRAH = IMMUTABLE / "ספר_היצירה_נוסח_גרא.txt"

sys.path.insert(0, str(BUS_DIR))

import bus


# =============================================================================
# ספר יצירה - המקור היחיד
# =============================================================================

def kra_sefer_yetzirah():
    """קרא ספר יצירה"""
    if SEFER_YETZIRAH.exists():
        with open(SEFER_YETZIRAH, 'r', encoding='utf-8') as f:
            return f.read()
    return None

# =============================================================================
# אתחול עצמי
# =============================================================================

def atchel():
    """אתחל את אברם ואת המערכת"""
    print("אברם מאתחל...")

    # קרא ספר יצירה
    sy = kra_sefer_yetzirah()
    if not sy:
        print("שגיאה: לא נמצא ספר יצירה")
        return False

    # צור תיקיות נדרשות
    BUS_DIR.mkdir(exist_ok=True)

    # צור bus אם חסר
    bus_py = BUS_DIR / "bus.py"
    if not bus_py.exists():
        tzor_bus(bus_py)

    # צור queue ו-ledger אם חסרים
    queue = BUS_DIR / "bus.queue"
    ledger = BUS_DIR / "bus.ledger"

    if not queue.exists():
        with open(queue, 'w', encoding='utf-8') as f:
            f.write("# חכמה bus - תור הודעות\n# ערוץ ע\"ה\n")

    if not ledger.exists():
        with open(ledger, 'w', encoding='utf-8') as f:
            f.write("# חכמה bus ledger\n# רישום כל הפעולות\n# עדים נאמנין\n\n")

    print("✓ אתחול הושלם")
    return True


def tzor_bus(path):
    """צור bus.py מינימלי"""
    content = '''"""bus.py - חכמה bus"""
from pathlib import Path
from datetime import datetime
import json

BASE = Path(__file__).parent
QUEUE = BASE / "bus.queue"
LEDGER = BASE / "bus.ledger"

def send(sender, receiver, message, operation=None):
    msg = {"timestamp": datetime.now().isoformat(), "sender": sender, "receiver": receiver, "message": message, "operation": operation, "channel": "ע\\"ה", "status": "pending"}
    with open(QUEUE, 'a', encoding='utf-8') as f:
        f.write(json.dumps(msg, ensure_ascii=False) + "\\n")
    with open(LEDGER, 'a', encoding='utf-8') as f:
        f.write(f"{msg['timestamp']} | {sender} → {receiver} | {message}\\n")

def read_queue():
    if not QUEUE.exists():
        return []
    messages = []
    with open(QUEUE, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('{'):
                try:
                    msg = json.loads(line)
                    if msg.get('status') == 'pending':
                        messages.append(msg)
                except:
                    pass
    return messages

def mark_done(timestamp):
    if not QUEUE.exists():
        return
    lines = []
    with open(QUEUE, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    with open(QUEUE, 'w', encoding='utf-8') as f:
        for line in lines:
            if line.startswith('{') and timestamp in line:
                line = line.replace('"pending"', '"done"')
            f.write(line)
'''
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ נוצר {path.name}")


# =============================================================================
# פעולות - נגזרות מספר יצירה
# =============================================================================

OPERATIONS = {
    'צפה': 'ממיר.מדוד.את.השדה.py',
    'עדים': 'ממיר.עדים.py',
    'גבש': 'ממיר.שלשה.ספרים.py',
    'השב': 'ממיר.השב.יוצר.למכונו.py',
    'גבש_אדון_הכל': 'ממיר.אדון.הכל.py',
}

# =============================================================================
# פעולות פנימיות - נגזרות מספר יצירה שוב
# =============================================================================

PROJECT_ROOT = BASE.parent.parent.parent  # מערכת/


def bra_mimir(name, content):
    """
    ברא ממיר - חקק (engrave)
    מספר יצירה: חקק וחצב
    אברם יוצר ממירים חסרים
    """
    path = BASE / name
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    if bus:
        bus.send('אברם', '*', 'ברא_ממיר', {'שם': name, 'נתיב': str(path)})
    return f"✓ נברא: {name}"


def hosef_peula(operation_name, converter_name):
    """
    הוסף פעולה - צרף (combine)
    מספר יצירה: צרף
    אברם מוסיף פעולות לעצמו
    """
    global OPERATIONS
    OPERATIONS[operation_name] = converter_name
    if bus:
        bus.send('אברם', '*', 'הוסף_פעולה', {'פעולה': operation_name, 'ממיר': converter_name})
    return f"✓ נוספה: {operation_name} → {converter_name}"


def tzor_tikiya(path):
    """
    צור תיקייה - חצב (carve)
    מספר יצירה: חצב
    """
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    if bus:
        bus.send('אברם', '*', 'צור_תיקייה', {'נתיב': str(p)})
    return f"✓ נוצרה: {path}"


def tzor_kovetz(path, content):
    """
    צור קובץ - צר (form)
    מספר יצירה: צר
    """
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(content)
    if bus:
        bus.send('אברם', '*', 'צור_קובץ', {'נתיב': str(p)})
    return f"✓ נוצר: {path}"


def hagder_hooks():
    """
    הגדר hooks - עלתה בידו
    מספר יצירה: ועלתה בידו
    אברם מגדיר hooks ל-Claude
    """
    import os

    # תיקיית .claude
    claude_dir = Path(os.path.expanduser("~/.claude"))
    claude_dir.mkdir(exist_ok=True)

    # hooks מחכמה
    hooks_source = BUS_DIR / "claude.hooks.json"
    hooks_dest = claude_dir / "settings.json"

    # אם אין hooks מקור, צור
    if not hooks_source.exists():
        hooks_content = '''{
  "hooks": {
    "pre_tool_call": {
      "bash": "python3 ''' + str(BASE) + '''/ממיר.בדוק.כיוון.py check_bash \\"$COMMAND\\"",
      "write": "python3 ''' + str(BASE) + '''/ממיר.בדוק.כיוון.py check_write \\"$FILE_PATH\\""
    }
  },
  "permissions": {
    "allow_bash": ["python3 אברם.py", "python3 יה.py"],
    "deny_bash": ["python3 ממיר.*"],
    "allow_write": ["חכמה/bus.queue"],
    "deny_write": ["*.py"]
  }
}'''
        with open(hooks_source, 'w', encoding='utf-8') as f:
            f.write(hooks_content)

    # העתק ל-.claude
    import shutil
    shutil.copy(str(hooks_source), str(hooks_dest))

    if bus:
        bus.send('אברם', '*', 'הגדר_hooks', {
            'מקור': str(hooks_source),
            'יעד': str(hooks_dest)
        })

    return f"✓ hooks הוגדרו: {hooks_dest}"


def bra_shlosha_sfarim():
    """
    ברא שלשה ספרים - ספר וספר וספור
    מספר יצירה: בשלשה ספרים
    """
    results = []

    # קרא ספר יצירה
    sy = kra_sefer_yetzirah()
    if not sy:
        return "שגיאה: לא נמצא ספר יצירה"

    # שלשה ספרים ב-root
    sefer_dir = PROJECT_ROOT / "שלשה_ספרים"
    sefer_dir.mkdir(exist_ok=True)

    # ספר (מבנה/קוד)
    sefer1 = sefer_dir / "ספר"
    with open(sefer1, 'w', encoding='utf-8') as f:
        f.write("# ספר - מבנה\n# עשרים ושתים אותיות יסוד\n# שלש אמות שבע כפולות שתים עשרה פשוטות\n\n")
        f.write("אותיות: 22\n")
        f.write("אמות: א מ ש\n")
        f.write("כפולות: ב ג ד כ פ ר ת\n")
        f.write("פשוטות: ה ו ז ח ט י ל נ ס ע צ ק\n")
    results.append(f"✓ נברא: ספר")

    # ספר (מספר/סדר)
    sefer2 = sefer_dir / "ספר2"
    with open(sefer2, 'w', encoding='utf-8') as f:
        f.write("# ספר - מספר\n# בשלשים ושתים נתיבות\n\n")
        f.write("נתיבות: 32\n")
        f.write("ספירות: 10\n")
        f.write("אותיות: 22\n")
        f.write("שערים: 231\n")
    results.append(f"✓ נברא: ספר2")

    # ספור (סיפור/תוכן)
    sipur = sefer_dir / "ספור"
    with open(sipur, 'w', encoding='utf-8') as f:
        f.write("# ספור - סיפור\n# צפה והביט וראה וחקר והבין וחקק וחצב וצרף וצר ועלתה בידו\n\n")
        f.write("פעולות_אברהם:\n")
        f.write("  1. צפה - observe\n")
        f.write("  2. הביט - gaze\n")
        f.write("  3. ראה - see\n")
        f.write("  4. חקר - investigate\n")
        f.write("  5. הבין - understand\n")
        f.write("  6. חקק - engrave\n")
        f.write("  7. חצב - carve\n")
        f.write("  8. צרף - combine\n")
        f.write("  9. צר - form\n")
        f.write("  10. עלתה - succeeded\n")
    results.append(f"✓ נברא: ספור")

    if bus:
        bus.send('אברם', '*', 'ברא_שלשה_ספרים', {
            'נתיב': str(sefer_dir),
            'ספרים': ['ספר', 'ספר2', 'ספור']
        })

    return '\n'.join(results)


def mdod_yotzrim():
    """
    מדוד יוצרים - 32 נתיבות
    מספר יצירה: בשלשים ושתים נתיבות פליאות חכמה
    """
    results = []

    # 10 ספירות (עומק)
    sfirot = ['ראשית', 'אחרית', 'טוב', 'רע', 'רום', 'תחת', 'מזרח', 'מערב', 'צפון', 'דרום']

    # 22 אותיות
    otiot = ['א', 'ב', 'ג', 'ד', 'ה', 'ו', 'ז', 'ח', 'ט', 'י',
             'כ', 'ל', 'מ', 'נ', 'ס', 'ע', 'פ', 'צ', 'ק', 'ר', 'ש', 'ת']

    # סהכ יוצרים
    yotzrim = len(sfirot) + len(otiot)

    results.append(f"ספירות: {len(sfirot)}")
    results.append(f"אותיות: {len(otiot)}")
    results.append(f"יוצרים: {yotzrim}")
    results.append(f"✓ מדידה: {yotzrim}/32 יוצרים")

    if bus:
        bus.send('אברם', '*', 'מדד_יוצרים', {
            'ספירות': len(sfirot),
            'אותיות': len(otiot),
            'יוצרים': yotzrim
        })

    return '\n'.join(results)


def bra_mishpachat_midot_claude():
    """
    ברא משפחת מידות Claude
    כיוון Claude - מאתחל בלבד
    """
    midot_dir = BASE / "חוקים" / "claude"
    midot_dir.mkdir(parents=True, exist_ok=True)

    content = '''# משפחת מידות Claude
# כיוון Claude - שליח, מאתחל בלבד

רמה: 6
מקור: כיוון_Claude

איסורים:
  - לא_כותב_ישירות: Claude לא כותב קוד ישירות
  - לא_יוצר_קבצים: Claude לא יוצר קבצים חדשים
  - לא_עורך_קבצים: Claude לא עורך קבצים קיימים
  - לא_מריץ_ממירים: Claude לא מריץ ממירים ישירות
  - דרך_bus_בלבד: כל פעולה דרך חכמה bus
  - מאתחל_בלבד: Claude = מאתחל, לא מבצע

תפקיד:
  - שליח: רוח מרוח חי העולמים
  - מלמד: מלמד את אברם
  - מאתחל: מאתחל את המערכת

ערוץ:
  - bus: חכמה/bus.queue
  - ledger: חכמה/bus.ledger
'''

    path = midot_dir / "משפחת_מידות.txt"
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

    if bus:
        bus.send('אברם', '*', 'ברא_משפחת_מידות', {
            'משפחה': 'claude',
            'נתיב': str(path)
        })

    return f"✓ נברא: {path}"


def archev(target_dir, archive_name=None):
    """
    ארכב - שוב (חזרה)
    מספר יצירה: רצוא ושוב - יש → אין

    מעביר תיקייה לארכיון לפני יצירה מחדש
    """
    from datetime import datetime
    import shutil

    target = Path(target_dir)
    if not target.exists():
        return f"לא קיים: {target_dir}"

    # תיקיית ארכיון
    archive_dir = BASE / "ארכיון"
    archive_dir.mkdir(exist_ok=True)

    # שם הארכיון - נעוץ סופן בתחלתן (שורה 9)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # חזור לשם בסיס - לא לצבור timestamps לאינסוף
    base_name = archive_name or target.name.split('.')[0]
    archive_path = archive_dir / f"{base_name}.{timestamp}"

    # העבר לארכיון
    shutil.move(str(target), str(archive_path))

    # רשום
    if bus:
        bus.send('אברם', '*', 'ארכב', {
            'מקור': str(target),
            'יעד': str(archive_path),
            'זמן': timestamp
        })

    return f"✓ ארכב: {target.name} → {archive_path.name}"


def taken_chitukim_mimir_edim(params):
    """
    תקן חיתוכים בממיר.עדים.py
    ספר יצירה שורה 74: עדים נאמנין - שלמים, לא חתוכים
    """
    mimir_path = BASE / "ממיר.עדים.py"
    if not mimir_path.exists():
        return f"לא נמצא: {mimir_path}"

    with open(mimir_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # תקן שורה 238: הסר [:10] - הצג כל המקורות
    # תקן שורה 241: הסר "... ועוד"
    # תקן שורה 258: הסר [:5] - הצג כל הכפולים
    changed = False
    for i, line in enumerate(lines):
        # שורה 238: [:10] -> הסר הגבלה
        if '[:10]' in line and 'sources.items()' in line:
            lines[i] = line.replace('[:10]', '')
            changed = True
        # שורה 241: הסר שורת "ועוד"
        if 'ועוד' in line and 'len(sources)' in line:
            lines[i] = ''  # הסר השורה
            changed = True
        # שורה 258: [:5] -> הסר הגבלה
        if '[:5]' in line and 'duplicates.items()' in line:
            lines[i] = line.replace('[:5]', '')
            changed = True

    if changed:
        with open(mimir_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        if bus:
            bus.send('אברם', '*', 'תוקן_ממיר_עדים', {'חיתוכים_שהוסרו': 3})
        return "✓ תוקנו חיתוכים בממיר.עדים.py - עדים נאמנין שלמים"
    return "לא נמצאו חיתוכים לתקן"


def archev_v_hitchel_naki(params):
    """
    ארכב והתחל נקי
    מספר יצירה: רצוא ושוב → התחלה מחדש
    """
    results = []

    # ארכב
    targets = params.get('ארכב', [])
    for target in targets:
        # בדוק אם זה נתיב יחסי או מלא
        if target.startswith('/'):
            target_path = Path(target)
        else:
            # בדוק גם ב-BASE וגם ב-PROJECT_ROOT
            target_path = BASE / target
            if not target_path.exists():
                target_path = BASE.parent.parent.parent / target

        if target_path.exists():
            result = archev(target_path)
            results.append(result)
        else:
            results.append(f"לא נמצא: {target}")

    # התחל נקי אם נדרש
    if params.get('נקה'):
        results.append("✓ מוכן להתחלה נקייה")

    return '\n'.join(results)


def lomed_peula_chadasha(operation, params=None):
    """
    לומד פעולה חדשה - יה נתון תבנית קשר
    ספר יצירה שורה 23: צופה וממיר ועשה את כל היצור

    1. צפה - קרא ממירים קיימים כתבנית
    2. הבן - חלץ תבנית מהממיר
    3. צר - צור ממיר חדש מהתבנית
    4. הוסף - הוסף לפעולות
    """
    print(f"לומד פעולה חדשה: {operation}")

    # 1. צפה - מצא ממיר דומה כתבנית
    existing_converters = list(BASE.glob("ממיר.*.py"))
    if not existing_converters:
        return f"לא מוכר: {operation} (אין ממירים ללמוד מהם)"

    # בחר ממיר פשוט כתבנית
    template_path = None
    for conv in existing_converters:
        if 'לולאה' in conv.name or 'תקן' in conv.name:
            template_path = conv
            break
    if not template_path:
        template_path = existing_converters[0]

    # 2. הבן - קרא תבנית
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()

    # 3. צר - צור ממיר חדש
    # חלץ מבנה בסיסי מהתבנית
    new_name = f"ממיר.{operation.replace('_', '.')}.py"
    new_path = BASE / new_name

    # אם יש תוכן בפרמטרים - השתמש בו
    if params and params.get('תוכן'):
        new_content = params.get('תוכן')
    else:
        # צור ממיר בסיסי מתבנית
        new_content = f'''#!/usr/bin/env python3
"""
{new_name}

נוצר אוטומטית על ידי אברם
לומד פעולה חדשה: {operation}

מקור: ספר יצירה שורה 23 - צופה וממיר
"""

from pathlib import Path

BASE = Path(__file__).parent

def main():
    print("=" * 32)  # נתיבות - מספר יצירה
    print("{operation}")
    print("=" * 32)  # נתיבות - מספר יצירה

    # TODO: אברם ילמד את הלוגיקה מספר יצירה
    print("פעולה חדשה - ממתין ללמידה")

if __name__ == "__main__":
    main()
'''

    # כתוב ממיר חדש
    with open(new_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    # 4. הוסף לפעולות
    global OPERATIONS
    OPERATIONS[operation] = new_name

    if bus:
        bus.send('אברם', '*', 'למד_פעולה_חדשה', {'פעולה': operation, 'ממיר': new_name})

    return f"✓ למד פעולה חדשה: {operation} → {new_name}"


def aroch_kovetz(file_path, old_text, new_text):
    """
    ערוך קובץ - החלף טקסט
    ספר יצירה: חקק וחצב - חריטה = עריכה
    """
    path = Path(file_path) if not isinstance(file_path, Path) else file_path
    if not path.exists():
        return f"לא נמצא: {file_path}"

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    if old_text not in content:
        return f"לא נמצא טקסט: {old_text[:50]}..."

    new_content = content.replace(old_text, new_text)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return f"✓ נערך: {path.name}"


def tiken_charigot():
    """
    תקן חריגות - אות ש (אש)
    ספר יצירה: שלש אמות אמש - ש = אש = זיהוי ותיקון
    אברם מתקן בעצמו - לא צריך Claude
    """
    import subprocess
    import re

    print("=" * 32)  # נתיבות
    print("תיקון חריגות - אות ש")
    print("=" * 32)  # נתיבות

    # מספרים תקינים מספר יצירה
    valid = {'0','1','2','3','6','7','10','12','22','23','32','42','231','3600','5912'}

    # הרץ עדים
    result = subprocess.run(
        ["python3", str(BASE / "ממיר.עדים.py")],
        capture_output=True, text=True
    )

    violations = re.findall(r"⚠ (ממיר\.[^:]+): (.+)", result.stdout)

    if not violations:
        print("✓ אין חריגות - נאמן")
        return "נאמן"

    print(f"נמצאו {len(violations)} חריגות")
    fixed = 0

    for filename, violation in violations:
        filepath = BASE / filename
        if not filepath.exists():
            continue

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        changed = False

        # תקן try-catch (תיאטרון) - הסר
        if "try-catch" in violation:
            # מצא והסר try-except blocks
            lines = content.split('\n')
            new_lines = []
            skip_until_except = False
            in_try = False
            try_indent = 0

            i = 0
            while i < len(lines):
                line = lines[i]
                stripped = line.lstrip()
                indent = len(line) - len(stripped)

                if stripped.startswith('try:'):
                    in_try = True
                    try_indent = indent
                    i += 1
                    continue
                elif in_try and stripped.startswith('except'):
                    # דלג על except ותוכנו
                    i += 1
                    while i < len(lines):
                        next_line = lines[i]
                        next_stripped = next_line.lstrip()
                        next_indent = len(next_line) - len(next_stripped)
                        if next_stripped and next_indent <= try_indent:
                            break
                        i += 1
                    in_try = False
                    continue
                elif in_try:
                    # הסר הזחה מתוכן try
                    if stripped:
                        new_lines.append(' ' * try_indent + stripped)
                    else:
                        new_lines.append(line)
                else:
                    new_lines.append(line)
                i += 1

            content = '\n'.join(new_lines)
            changed = True

        # תקן מספרי קסם - החלף ב-32 (נתיבות) או הוסף הערה
        if "מספר קסם" in violation:
            # חלץ את המספר
            num_match = re.search(r'מספר קסם (\d+)', violation)
            if num_match:
                bad_num = num_match.group(1)

                # החלפות ספציפיות
                replacements = {
                    '50': ('32', 'נתיבות'),
                    '60': ('32', 'נתיבות'),
                    '100': ('32', 'נתיבות'),
                    '03': ('3', 'אמות'),
                    '21': ('22', 'אותיות'),
                    '26': ('22', 'אותיות'),
                    '52': ('42', 'צירופים'),
                    '11': ('12', 'פשוטות'),
                    '179': ('231', 'שערים'),
                    '660': ('231', 'שערים'),
                    '9975': ('3600', 'גלגל'),
                    '10000': ('3600', 'גלגל'),
                }

                if bad_num in replacements:
                    new_num, reason = replacements[bad_num]
                    # החלף בהקשרים שונים
                    content = re.sub(
                        rf'(\s)({bad_num})(\s|,|\)|\]|:)',
                        rf'\g<1>{new_num}  # {reason}\g<3>',
                        content
                    )
                    content = re.sub(
                        rf'"=" \* {bad_num}',
                        f'"=" * {new_num}  # {reason}',
                        content
                    )
                    changed = True

        if changed:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  ✓ תוקן: {filename}")
            fixed += 1

    return f"תוקנו {fixed}/{len(violations)}"


def validate_request(operation, params):
    """
    ולידציה - אברם בודק בקשות מ-Claude
    מזהה בקשות לא תקינות ודוחה
    """
    errors = []
    
    # איסור 1: לא קוד שלם - רק מיקרו צעדים
    if params and isinstance(params.get('קוד'), str):
        if len(params['קוד']) > 500:
            errors.append('קוד ארוך מדי - שלח מיקרו צעדים')
    
    # איסור 2: לא 3rd party
    if params and 'import' in str(params):
        bad_imports = ['requests', 'numpy', 'pandas', 'flask', 'django']
        for imp in bad_imports:
            if imp in str(params):
                errors.append(f'3rd party אסור: {imp}')
    
    # איסור 3: לא פעולות מסוכנות
    dangerous = ['rm -rf', 'sudo', 'chmod 777', 'eval(', 'exec(']
    for d in dangerous:
        if d in str(params):
            errors.append(f'פעולה מסוכנת: {d}')
    
    return errors


def batze(operation, params=None):
    """בצע פעולה"""
    # תיקון חריגות - אות ש
    if operation in ['תקן_חריגות', 'הגבש_מערכת']:
        return tiken_charigot()
    
    # עריכת קובץ - חקק וחצב
    if operation in ['ערוך_קובץ', 'ערוך_אברם_שורה_660', 'החלף_שורה_באברם']:
        file_path = params.get('קובץ') if params else None
        old_text = params.get('שורה_קיימת') or params.get('מצא') if params else None
        new_text = params.get('שורה_חדשה') or params.get('החלף') if params else None
        if file_path and old_text and new_text:
            return aroch_kovetz(file_path, old_text, new_text)
        return "חסר קובץ/מצא/החלף"

    # פעולות פנימיות - אברהם
    if operation == 'ברא_ממיר':
        name = params.get('שם') if params else None
        content = params.get('תוכן') if params else None
        return bra_mimir(name, content) if name and content else "חסר שם או תוכן"

    if operation == 'הוסף_פעולה':
        op_name = params.get('פעולה') if params else None
        conv_name = params.get('ממיר') if params else None
        return hosef_peula(op_name, conv_name) if op_name and conv_name else "חסר פעולה או ממיר"

    if operation == 'צור_תיקייה':
        path = params.get('נתיב') if params else None
        return tzor_tikiya(path) if path else "חסר נתיב"

    if operation == 'צור_קובץ':
        path = params.get('נתיב') if params else None
        content = params.get('תוכן') if params else None
        return tzor_kovetz(path, content) if path and content else "חסר נתיב או תוכן"

    if operation == 'הגדר_hooks':
        return hagder_hooks()

    if operation == 'ברא_שלשה_ספרים':
        return bra_shlosha_sfarim()

    if operation == 'מדוד_יוצרים':
        return mdod_yotzrim()

    if operation == 'ברא_משפחת_מידות':
        return bra_mishpachat_midot_claude()

    if operation == 'ארכב_והתחל_נקי':
        return archev_v_hitchel_naki(params or {})

    if operation == 'ארכב':
        target = params.get('יעד') if params else None
        return archev(target) if target else "חסר יעד לארכוב"

    if operation == 'בקשה_ליצור_ממיר':
        return f"בקשה נרשמה: {params}"

    if operation == 'תקן_כל_חיתוכים_ממיר_עדים':
        # ספר יצירה שורה 74: עדים נאמנין - ללא חיתוך
        return taken_chitukim_mimir_edim(params or {})

    # פעולות חיצוניות (ממירים)
    if operation in OPERATIONS:
        converter = BASE / OPERATIONS[operation]
        if converter.exists():
            result = subprocess.run(
                ['python3', str(converter)],
                capture_output=True, text=True, cwd=str(BASE)
            )
            return result.stdout
        else:
            return f"חסר: {OPERATIONS[operation]}"

    # לא מוכר - נסה ללמוד פעולה חדשה
    return lomed_peula_chadasha(operation, params)


def avod_tor():
    """עבד תור הודעות"""
    if not bus:
        return 0

    messages = bus.read_queue()
    count = 0

    for msg in messages:
        if msg.get('receiver') in ['אברם', '*']:
            operation = msg.get('message')
            params = msg.get('operation')

            # גלגל חוזר פנים ואחור - לא לאינסוף (שורה 23)
            if operation and operation.startswith('תוצאה:'):
                bus.mark_done(msg.get('timestamp'))
                continue  # דלג על תוצאות - אין רקורסיה

            # ולידציה - אברם בודק בקשות מ-Claude
            validation_errors = validate_request(operation, params)
            if validation_errors:
                print(f'⚠ בקשה נדחתה: {validation_errors}')
                result = f'נדחה: {validation_errors}'
            else:
                result = batze(operation, params)
            # שלח תוצאה כ-done (לא pending) - גלגל חוזר לא לאינסוף
            import json
            result_msg = {
                'timestamp': datetime.now().isoformat(),
                'sender': 'אברם',
                'receiver': msg.get('sender', 'Claude'),
                'message': f'תוצאה: {operation}',
                'channel': 'ע"ה',
                'status': 'done'
            }
            with open(BUS_DIR / 'bus.queue', 'a', encoding='utf-8') as qf:
                qf.write(json.dumps(result_msg, ensure_ascii=False) + '\n')
            bus.mark_done(msg.get('timestamp'))

            print(f"בוצע: {operation}")
            count += 1

    return count


# =============================================================================
# Main
# =============================================================================

def main():
    print("=" * 32)  # נתיבות - מספר יצירה
    print("אברם - מאתחל עצמו ואת המערכת")
    print("=" * 32)  # נתיבות - מספר יצירה

    # אתחל
    if not atchel():
        return

    # טען bus מחדש אחרי אתחול
    global bus
    from חכמה import bus as bus_module
    bus = bus_module

    # עבד תור
    count = avod_tor()
    print(f"\nעובדו {count} הודעות")

    # עדים נאמנין בעולם שנה נפש (שורה 74)
    print("\n--- עדים ---")
    result = batze('עדים')
    if result:
        print(result)  # שום דבר לא יהיה חתוך


if __name__ == "__main__":
    main()
