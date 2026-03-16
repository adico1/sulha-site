#!/usr/bin/env python3
"""
ממיר.ברא.10000.אי.סורים.py

גזירה מספר יצירה:
- שורה 6: עשר ולא תשע עשר ולא אחת עשרה
- שורה 7: 5 צירי הפכים
- שורה 39: שבע ולא שש שבע ולא שמונה

תבנית סור = גבול מבני שאסור לחצות
"""

from pathlib import Path

BASE = Path(__file__).parent
TARGET = BASE.parent.parent.parent / "א" / "אי-סורים"

# מספרי ספר יצירה
SFIROT = 10
OTIOT = 22
NTIVOT = SFIROT + OTIOT  # 32
KAMA = SFIROT ** 4  # 3600  # גלגל

# 5 צירים מספר יצירה שורה 7
TZIRIM = [
    ("ראשית", "אחרית", "זמן"),
    ("טוב", "רע", "מוסר"),
    ("רום", "תחת", "אנכי"),
    ("מזרח", "מערב", "אופקי"),
    ("צפון", "דרום", "אופקי"),
]

def gzor_sor(i):
    """גזור סור ומדידות מאינדקס"""
    # פרק ל-4 ספרות בסיס 10
    d0 = i % SFIROT
    d1 = (i // SFIROT) % SFIROT
    d2 = (i // (SFIROT * SFIROT)) % SFIROT
    d3 = (i // (SFIROT ** 3)) % SFIROT
    d4 = (d0 + d1 + d2 + d3) % SFIROT
    
    digits = [d0, d1, d2, d3, d4]
    
    # הציר הדומיננטי = הציר עם הספרה הגבוהה ביותר
    max_idx = digits.index(max(digits[:4]))
    tzir = TZIRIM[max_idx]
    
    # הגבול נקבע לפי הספרה
    d = digits[max_idx]
    if d < SFIROT // 2:
        gvul = tzir[0]  # גבול תחתון
        kelal = f"{d} ולא {d-1}" if d > 0 else f"{d} ולא פחות"
    else:
        gvul = tzir[1]  # גבול עליון
        kelal = f"{d} ולא {d+1}" if d < SFIROT-1 else f"{d} ולא יותר"
    
    midot = {
        "עומק_ראשית": d0,
        "עומק_אחרית": SFIROT - 1 - d0,
        "עומק_טוב": d1,
        "עומק_רע": SFIROT - 1 - d1,
        "עומק_רום": d2,
        "עומק_תחת": SFIROT - 1 - d2,
        "עומק_מזרח": d3,
        "עומק_מערב": SFIROT - 1 - d3,
        "עומק_צפון": d4,
        "עומק_דרום": SFIROT - 1 - d4,
    }
    
    sor = {
        "ציר": tzir[2],
        "קוטב": gvul,
        "כלל": kelal,
        "שבירה": "קריסה",
    }
    
    return midot, sor

def main():
    print("=" * NTIVOT)
    print("ברא 3600  # גלגל אי-סורים")
    print("=" * NTIVOT)

    TARGET.mkdir(parents=True, exist_ok=True)

    for i in range(1, KAMA + 1):
        midot, sor = gzor_sor(i)
        
        content = f"id: {i}\n"
        content += f"מה: סור_{i}\n"
        content += f"טיפוס: איסור\n"
        content += f"סור:\n"
        content += f"  ציר: {sor['ציר']}\n"
        content += f"  קוטב: {sor['קוטב']}\n"
        content += f"  כלל: {sor['כלל']}\n"
        content += f"  שבירה: {sor['שבירה']}\n"
        content += f"מדידות:\n"
        for k, v in midot.items():
            content += f"  {k}: {v}\n"
        content += f"אינבריאנט: זוג_הפכים_סוכם_ל_9\n"
        content += f"מקור: ספר_יצירה_שורות_6_7\n"

        path = TARGET / f"סור_{i:05d}.אי"
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

        if i % (SFIROT ** 3) == 0:
            print(f"  נוצרו {i}/{KAMA}")

    print(f"✓ נוצרו {KAMA} אי-סורים")

if __name__ == "__main__":
    main()
