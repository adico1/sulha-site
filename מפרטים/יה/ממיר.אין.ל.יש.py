#!/usr/bin/env python3
"""
ממיר.אין.ל.יש.py

מ: אין (ק"ק אי = 100×100)
אל: יש (שדה)

עשר ספירות בלי מה מדתן עשר שאין להם סוף
עשר עומק × עשר אברהם = שדה

סדר:
1. קרא אין (כל ה-אי בתיקיית אין)
2. מיין לפי עומק (10 צירים)
3. הפעל 10 פעולות אברהם
4. צור שדה (יש)

עשר עומק:
- עומק ראשית / עומק אחרית
- עומק טוב / עומק רע
- עומק רום / עומק תחת
- עומק מזרח / עומק מערב
- עומק צפון / עומק דרום

עשר אברהם:
צפה → הביט → ראה → חקר → הבין → חקק → חצב → צרף → צר → עלתה

איסורים:
- no 3rd party
- תארכב מקור לפני כתיבה
"""

from pathlib import Path
from datetime import datetime

BASE = Path(__file__).parent
AIN_DIR = BASE / "אין"
YESH_DIR = BASE / "יש"
ARCHIVE = BASE / "ארכיון"

# עשר עומק
OMEK = [
    ('ראשית', 'אחרית'),   # זמן
    ('טוב', 'רע'),         # מוסר
    ('רום', 'תחת'),        # אנכי
    ('מזרח', 'מערב'),      # אופקי א
    ('צפון', 'דרום')       # אופקי ב
]

# עשר אברהם
AVRAHAM = [
    'צפה',    # 1 - observe
    'הביט',   # 2 - gaze
    'ראה',    # 3 - see
    'חקר',    # 4 - investigate
    'הבין',   # 5 - understand
    'חקק',    # 6 - engrave
    'חצב',    # 7 - carve
    'צרף',    # 8 - combine
    'צר',     # 9 - form
    'עלתה'    # 10 - succeeded
]


def archive(file_path):
    """תארכב קובץ לפני שינוי"""
    ARCHIVE.mkdir(exist_ok=True)
    if file_path.exists():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_path = ARCHIVE / f"{file_path.name}.{timestamp}"
        with open(file_path, 'r', encoding='utf-8') as src:
            content = src.read()
        with open(archive_path, 'w', encoding='utf-8') as dst:
            dst.write(content)
        return True
    return False


def read_ain():
    """קרא כל אי מתיקיית אין"""
    ain_list = []

    if not AIN_DIR.exists():
        print(f"  אין תיקיית אין")
        return ain_list

    for ai_file in sorted(AIN_DIR.glob("*.אי")):
        ai = {'קובץ': ai_file.name}
        with open(ai_file, 'r', encoding='utf-8') as f:
            for line in f:
                if ':' in line:
                    key, val = line.split(':', 1)
                    ai[key.strip()] = val.strip()
        ain_list.append(ai)

    return ain_list


def tzafa(ain_list):
    """צפה - observe: סקירה ראשונית - ק"ק = 100×100 = 10,000"""
    KAK = 32  # נתיבות * 32  # נתיבות  # ק"ק
    current = len(ain_list)
    print(f"  צפה: {current}/{KAK} אי ({current/KAK*100:.2f}%)")
    return {'count': current, 'target': KAK, 'items': ain_list}


def hibit(data):
    """הביט - gaze: מיקוד"""
    # סנן לפי סור
    by_sur = {'פתוח': [], 'מוגבל': [], 'נעול': []}
    for ai in data['items']:
        sur = ai.get('סור', 'פתוח')
        if sur in by_sur:
            by_sur[sur].append(ai)
    print(f"  הביט: פתוח={len(by_sur['פתוח'])}, מוגבל={len(by_sur['מוגבל'])}, נעול={len(by_sur['נעול'])}")
    data['by_sur'] = by_sur
    return data


def raah(data):
    """ראה - see: זיהוי"""
    # זהה מקורות
    sources = {}
    for ai in data['items']:
        src = ai.get('מקור', 'לא ידוע')
        if src not in sources:
            sources[src] = []
        sources[src].append(ai)
    print(f"  ראה: {len(sources)} מקורות")
    data['sources'] = sources
    return data


def chakar(data):
    """חקר - investigate: חקירה"""
    # חקור את התוכן
    contents = {}
    for ai in data['items']:
        mah = ai.get('מה', '')
        if mah:
            contents[ai.get('id', '?')] = mah
    print(f"  חקר: {len(contents)} תכנים")
    data['contents'] = contents
    return data


def hevin(data):
    """הבין - understand: הבנה"""
    # מצא קשרים
    connections = []
    items = data['items']
    for i, ai1 in enumerate(items):
        for ai2 in items[i+1:]:
            # חפש קשר במקור
            if ai1.get('מקור') == ai2.get('מקור'):
                connections.append((ai1.get('id'), ai2.get('id'), 'מקור'))
    print(f"  הבין: {len(connections)} קשרים")
    data['connections'] = connections
    return data


def chakak(data):
    """חקק - engrave: חקיקה - יצירת מבנה"""
    # חקוק מבנה עומק
    omek_structure = {}
    for pair in OMEK:
        omek_structure[pair[0]] = []
        omek_structure[pair[1]] = []

    # מפה אי לעומק לפי תוכן
    for ai in data['items']:
        mah = ai.get('מה', '').lower()
        for pair in OMEK:
            if pair[0] in mah:
                omek_structure[pair[0]].append(ai)
            elif pair[1] in mah:
                omek_structure[pair[1]].append(ai)

    print(f"  חקק: מבנה עומק נחקק")
    data['omek'] = omek_structure
    return data


def chatzav(data):
    """חצב - carve: חציבה - עיצוב פרטים"""
    # חצוב שדות
    fields = {
        'id': [],
        'מה': [],
        'מקור': [],
        'שורה': [],
        'סור': []
    }
    for ai in data['items']:
        for field in fields:
            if field in ai:
                fields[field].append(ai[field])

    print(f"  חצב: {len(fields)} שדות נחצבו")
    data['fields'] = fields
    return data


def tzaraf(data):
    """צרף - combine: צירוף"""
    # צרף הכל לשדה
    sade = {
        'אין': {
            'count': data['count'],
            'target': data['target'],  # ק"ק = 10,000
            'by_sur': {k: len(v) for k, v in data['by_sur'].items()},
            'sources': list(data['sources'].keys())
        },
        'עומק': {k: len(v) for k, v in data['omek'].items() if v},
        'קשרים': len(data['connections'])
    }
    print(f"  צרף: שדה נוצר ({data['count']}/{data['target']})")
    data['sade'] = sade
    return data


def tzar(data):
    """צר - form: יצירה"""
    # צור את קובץ יש
    YESH_DIR.mkdir(exist_ok=True)

    yesh_path = YESH_DIR / "שדה"
    with open(yesh_path, 'w', encoding='utf-8') as f:
        f.write("# שדה - יש מאין\n\n")

        sade = data['sade']

        f.write("אין:\n")
        f.write(f"  ק\"ק: {sade['אין']['target']} (100×100)\n")
        f.write(f"  נוכחי: {sade['אין']['count']}\n")
        f.write(f"  חסר: {sade['אין']['target'] - sade['אין']['count']}\n")
        f.write(f"  פתוח: {sade['אין']['by_sur'].get('פתוח', 0)}\n")
        f.write(f"  מוגבל: {sade['אין']['by_sur'].get('מוגבל', 0)}\n")
        f.write(f"  נעול: {sade['אין']['by_sur'].get('נעול', 0)}\n\n")

        f.write("עומק:\n")
        for omek, count in sade['עומק'].items():
            f.write(f"  {omek}: {count}\n")
        f.write("\n")

        f.write("מקורות:\n")
        for src in sade['אין']['sources']:
            f.write(f"  - {src}\n")
        f.write("\n")

        f.write(f"קשרים: {sade['קשרים']}\n")

    print(f"  צר: יש/שדה נוצר")
    data['yesh_path'] = yesh_path
    return data


def alta(data):
    """עלתה - succeeded: הצלחה"""
    print(f"  עלתה: אין → יש")
    return True


def main():
    print("=" * 50)
    print("ממיר אין ליש")
    print("עשר עומק × עשר אברהם = שדה")
    print("=" * 50)

    # קרא אין
    print("\nקורא אין:")
    ain_list = read_ain()

    if not ain_list:
        print("אין אי בתיקיית אין")
        return

    # עשר פעולות אברהם
    print("\nעשר אברהם:")

    data = tzafa(ain_list)      # 1
    data = hibit(data)          # 2
    data = raah(data)           # 3
    data = chakar(data)         # 4
    data = hevin(data)          # 5
    data = chakak(data)         # 6
    data = chatzav(data)        # 7
    data = tzaraf(data)         # 8
    data = tzar(data)           # 9
    result = alta(data)         # 10

    print("\n" + "=" * 50)
    if result:
        print("עלתה. יש מאין.")
    print("=" * 50)


if __name__ == "__main__":
    main()
