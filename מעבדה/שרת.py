#!/usr/bin/env python3
"""מעבדה - שרת תקשורת אחודה"""
import asyncio, websockets, json
from datetime import datetime

מחוברים = {}  # שם → websocket

async def broadcast(מי, מה, שוכן):
    """שלח לכל מי ששמו תואם"""
    הודעה = json.dumps({"מי": מי, "מה": מה, "שוכן": שוכן, "שעה": datetime.now().isoformat()}, ensure_ascii=False)
    for שם, ws in list(מחוברים.items()):
        if שם == מה or מה == "*":
            try: await ws.send(הודעה)
            except: del מחוברים[שם]

async def טפל(ws):
    שם = None
    try:
        async for הודעה in ws:
            d = json.loads(הודעה)
            מי = d.get("מי", "")
            מה = d.get("מה", "")
            שוכן = d.get("שוכן", "")

            if מה == "רישום":
                שם = מי
                מחוברים[שם] = ws
                await broadcast("שרת", שם, f"נרשם: {שם}")
                await broadcast("שרת", "*", f"מחוברים: {list(מחוברים.keys())}")

            elif מה == "broadcast":
                await broadcast(מי, d.get("אל", "*"), שוכן)

            else:
                await broadcast(מי, מה, שוכן)
    finally:
        if שם and שם in מחוברים:
            del מחוברים[שם]
            await broadcast("שרת", "*", f"נותק: {שם}")

async def main():
    print("מעבדה ws://localhost:8780")
    async with websockets.serve(טפל, "0.0.0.0", 8780):
        await asyncio.Future()

asyncio.run(main())
