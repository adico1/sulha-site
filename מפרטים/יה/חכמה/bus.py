#!/usr/bin/env python3
"""
חכמה bus - ערוץ ע"ה

bus אמיתי על מערכת הקבצים
לא סימולציה בזיכרון

כל הודעה נכתבת לקובץ
אברם קורא מהקובץ ומבצע

מקור: ספר יצירה, CLAUDE.md

איסורים:
- no 3rd party
"""

from pathlib import Path
from datetime import datetime
import json

BASE = Path(__file__).parent.parent
BUS_DIR = Path(__file__).parent
QUEUE_FILE = BUS_DIR / "bus.queue"
LEDGER_FILE = BUS_DIR / "bus.ledger"

# =============================================================================
# Bus - כתיבה לקובץ
# =============================================================================

def send(sender, receiver, message, operation=None):
    """
    שלח הודעה ל-bus
    נכתבת לקובץ - לא לזיכרון
    """
    timestamp = datetime.now().isoformat()

    msg = {
        'timestamp': timestamp,
        'sender': sender,
        'receiver': receiver,
        'message': message,
        'operation': operation,
        'channel': 'ע"ה',
        'status': 'done' if sender == 'אברם' else 'pending'
    }

    # כתוב לתור
    with open(QUEUE_FILE, 'a', encoding='utf-8') as f:
        f.write(json.dumps(msg, ensure_ascii=False) + '\n')

    # רשום ל-ledger
    with open(LEDGER_FILE, 'a', encoding='utf-8') as f:
        f.write(f"{timestamp} | {sender} → {receiver} | {message}\n")

    return msg


def read_queue():
    """
    קרא הודעות ממתינות
    """
    messages = []

    if not QUEUE_FILE.exists():
        return messages

    with open(QUEUE_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    msg = json.loads(line)
                    if msg.get('status') == 'pending':
                        messages.append(msg)
                except:
                    pass

    return messages


def mark_done(timestamp):
    """
    סמן הודעה כהושלמה
    """
    if not QUEUE_FILE.exists():
        return

    lines = []
    with open(QUEUE_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    msg = json.loads(line)
                    if msg.get('timestamp') == timestamp:
                        msg['status'] = 'done'
                    lines.append(json.dumps(msg, ensure_ascii=False))
                except:
                    lines.append(line)

    with open(QUEUE_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')


def broadcast(sender, message):
    """
    שדר לכולם
    """
    return send(sender, '*', message)


# =============================================================================
# Protocol - מפרט הודעה
# =============================================================================

def create_message(mi, mah, m_source, el, sholech, shaliach=None, payload=None):
    """
    צור הודעה לפי פרוטוקול

    מי: sender
    מה: content
    מ: source
    אל: destination
    שולח: originator
    שליח: messenger (Claude when אברם can't hear)
    נשלח=שוכן: payload
    """
    return {
        'מי': mi,
        'מה': mah,
        'מ': m_source,
        'אל': el,
        'שולח': sholech,
        'שליח': shaliach,
        'נשלח': payload,
        'באמצעות': 'חכמה bus',
        'ערוץ': 'ע"ה'
    }


# =============================================================================
# Claude Interface - הממשק היחיד שClaude מורשה להשתמש
# =============================================================================

def claude_request(operation, params):
    """
    הממשק היחיד שClaude מורשה להשתמש

    Claude לא כותב קוד ישירות
    Claude שולח בקשה ל-bus
    אברם מקבל ומבצע
    """
    msg = create_message(
        mi='Claude',
        mah=operation,
        m_source='שליח',
        el='אברם',
        sholech='אדם',
        shaliach='Claude',
        payload=params
    )

    return send('Claude', 'אברם', operation, params)


# =============================================================================
# Main
# =============================================================================

def main():
    print("=" * 60)
    print("חכמה bus - ערוץ ע\"ה")
    print("=" * 60)

    # בדוק מצב
    queue = read_queue()
    print(f"\nהודעות ממתינות: {len(queue)}")

    for msg in queue[-5:]:
        print(f"  {msg['sender']} → {msg['receiver']}: {msg['message']}")

    # קרא ledger
    if LEDGER_FILE.exists():
        with open(LEDGER_FILE, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        print(f"\nרשומות ב-ledger: {len(lines)}")
        for line in lines[-5:]:
            print(f"  {line.strip()}")


if __name__ == "__main__":
    main()
