#!/usr/bin/env python3
"""
ממיר.תקן.bus.queue.py

תיקון אמיתי של bus.queue:
1. הסר רקורסיה - תוצאה: תוצאה: תוצאה:...
2. הודעות מאברם = רישום (done), לא פקודות (pending)
3. תוצאה בודדת = done
4. נקה pending מזויף

מספר יצירה: גלגל חוזר פנים ואחור - לא לאינסוף (שורה 23)
"""

from pathlib import Path
import json

BASE = Path(__file__).parent
QUEUE_FILE = BASE / "חכמה" / "bus.queue"

def tiken():
    if not QUEUE_FILE.exists():
        return "לא נמצא bus.queue"

    with open(QUEUE_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    clean_lines = []
    removed_recursive = 0
    fixed_avram = 0
    fixed_result = 0

    for line in lines:
        # שמור שורות תיעוד
        if not line.startswith("{"):
            clean_lines.append(line)
            continue

        msg = json.loads(line)
        message = msg.get("message", "")
        sender = msg.get("sender", "")
        status = msg.get("status", "")

        # 1. הסר רקורסיה - תוצאה: תוצאה:
        if message.count("תוצאה:") > 1:
        removed_recursive += 1
        continue  # דלג על שורה רקורסיבית

        # 2. הודעות מאברם pending → done (רישום, לא פקודה)
        if sender == "אברם" and status == "pending":
        msg["status"] = "done"
        fixed_avram += 1

        # 3. תוצאה בודדת pending → done
        if message.startswith("תוצאה:") and status == "pending":
        msg["status"] = "done"
        fixed_result += 1

        clean_lines.append(json.dumps(msg, ensure_ascii=False) + "\n")
    # כתוב קובץ נקי
    with open(QUEUE_FILE, "w", encoding="utf-8") as f:
        f.writelines(clean_lines)

    return f"✓ הוסרו {removed_recursive} רקורסיות, תוקנו {fixed_avram} מאברם, {fixed_result} תוצאות"

if __name__ == "__main__":
    print(tiken())
