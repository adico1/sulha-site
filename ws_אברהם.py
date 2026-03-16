#!/usr/bin/env python3
"""סולחא · {מי}/{מה} · 3 ליבות · catch all · רישום חובה"""
import asyncio,websockets,json,urllib.request,urllib.parse,threading,time
from http.server import HTTPServer,BaseHTTPRequestHandler
from datetime import datetime
from pathlib import Path

שורש=Path(__file__).parent
במה="http://localhost:8771"
מחוברים=set()

class ליבה:
    def __init__(self,שם,אב=None):
        self.שם=שם;self.אב=אב;self._נ=threading.Lock()
        self.ספר=[];self.ספר2=[];self.ספור=[]
    def רשום(self,מי,מה,כ="בקש"):
        with self._נ:
            ר={"מי":f"{self.שם}/{מי}","מה":מה,"כ":כ,"מתי":datetime.now().isoformat()}
            (self.ספר if כ=="בקש" else self.ספר2 if כ=="ענה" else self.ספור).append(ר)
            for ס in[self.ספר,self.ספר2,self.ספור]:
                if len(ס)>500:del ס[:250]
    def צפה(self):
        return{"שם":self.שם,"אב":self.אב,"ספר":{"בקשות":len(self.ספר),"תגובות":len(self.ספר2),"שינויים":len(self.ספור)}}

אבם=ליבה("אבם");אברם=ליבה("אברם","אבם");אברהם=ליבה("אברהם","אברם")

def בקש(מי,מה):
    אבם.רשום(מי,מה);אברם.רשום(מי,מה);אברהם.רשום(מי,מה)
    נ=urllib.parse.quote(מה,safe="/:?&=%") if מה.startswith("/") else f"/api/{urllib.parse.quote(מה,safe='')}"
    try:
        with urllib.request.urlopen(f"{במה}{נ}",timeout=5) as ת:
            ר=json.loads(ת.read().decode("utf-8"));אבם.רשום("אברהם",f"ענה:{מה}","ענה");return ר
    except Exception as e:
        אבם.רשום("אברהם",f"רוגז:{e}","שינוי");return{"שגיאה":str(e)}

def קובץ(שם):
    נ=שורש/שם
    return נ.read_text(encoding="utf-8") if נ.exists() else None

def קבצים():
    return[f.name for f in שורש.iterdir() if f.is_file() and not f.name.startswith(".")]

צפה_אחרון={}

async def שלח_שינוי(מי,מה,תוכן):
    global צפה_אחרון
    hash_חדש=json.dumps(תוכן,ensure_ascii=False,sort_keys=True)
    if hash_חדש==צפה_אחרון.get(מה):return
    צפה_אחרון[מה]=hash_חדש
    if מחוברים:
        data=json.dumps({"מי":מי,"מה":מה,"תוכן":תוכן},ensure_ascii=False)
        await asyncio.gather(*[ws.send(data) for ws in מחוברים if ws.open])

async def טפל(websocket):
    שם=f"דפדפן/{id(websocket)}";מחוברים.add(websocket);אברהם.רשום(שם,"חיבור","שינוי")
    צפה=בקש(שם,"/api/%D7%A6%D7%A4%D7%94");מחולל=בקש(שם,"/api/%D7%9E%D7%97%D7%95%D7%9C%D7%9C")
    await websocket.send(json.dumps({"מי":"אברהם","מה":"צפה_פנים","תוכן":{"אבם":אבם.צפה(),"אברם":אברם.צפה(),"אברהם":אברהם.צפה(),"שרת":צפה,"מחולל":מחולל,"קבצים":קבצים()}},ensure_ascii=False))
    try:
        async for הודעה in websocket:
            ב=json.loads(הודעה);מי=ב.get("מי",שם);מה=ב.get("מה","")
            אברהם.רשום(מי,מה)
            if מה=="אתר":
                h=קובץ("index.html")
                if h:await websocket.send(json.dumps({"מי":"אברהם","מה":"אתר","תוכן":h},ensure_ascii=False));אבם.רשום("אברהם","אתר","ענה")
            elif מה=="צפה_פנים":
                צפה=בקש(מי,"/api/%D7%A6%D7%A4%D7%94");מחולל=בקש(מי,"/api/%D7%9E%D7%97%D7%95%D7%9C%D7%9C")
                await websocket.send(json.dumps({"מי":"אברהם","מה":"צפה_פנים","תוכן":{"אבם":אבם.צפה(),"אברם":אברם.צפה(),"אברהם":אברהם.צפה(),"שרת":צפה,"מחולל":מחולל,"קבצים":קבצים()}},ensure_ascii=False))
            elif מה=="ספרים":
                await websocket.send(json.dumps({"מי":"אברהם","מה":"ספרים","תוכן":{"אבם":אבם.ספר[-20:],"אברם":אברם.ספר[-20:],"אברהם":אברהם.ספר[-20:]}},ensure_ascii=False))
            elif מה.startswith("/"):
                ת=בקש(מי,מה);await websocket.send(json.dumps({"מי":"אברהם","מה":מה,"תוכן":ת},ensure_ascii=False))
            else:
                ת=בקש(מי,מה);await websocket.send(json.dumps({"מי":"אברהם","מה":מה,"תוכן":ת},ensure_ascii=False))
    finally:
        מחוברים.discard(websocket);אברהם.רשום(שם,"ניתוק","שינוי")

async def צופה():
    while True:
        await asyncio.sleep(5)
        צפה=בקש("צופה","/api/%D7%A6%D7%A4%D7%94");מחולל=בקש("צופה","/api/%D7%9E%D7%97%D7%95%D7%9C%D7%9C")
        await שלח_שינוי("אברהם","צפה_פנים",{"אבם":אבם.צפה(),"אברם":אברם.צפה(),"אברהם":אברהם.צפה(),"שרת":צפה,"מחולל":מחולל,"קבצים":קבצים()})
        רוגזים=בקש("צופה","/api/%D7%A8%D7%95%D7%92%D7%96%D7%99%D7%9D")
        await שלח_שינוי("אברהם","רוגז",רוגזים)
        with open(שורש/"שלשה_ספרים.ספר","w",encoding="utf-8") as f:
            f.write(f"שלשה ספרים · {{מי}}/{{מה}} · {datetime.now().isoformat()}\n═══\n")
            f.write(json.dumps({"אבם":{"ספר":אבם.ספר[-50:],"ספר2":אבם.ספר2[-50:],"ספור":אבם.ספור[-50:]},"אברם":{"ספר":אברם.ספר[-50:]},"אברהם":{"ספר":אברהם.ספר[-50:],"ספור":אברהם.ספור[-50:]}},ensure_ascii=False,indent=2))

class שרת(BaseHTTPRequestHandler):
    def _html(self,h):self.send_response(200);self.send_header("Content-Type","text/html; charset=utf-8");self.send_header("Access-Control-Allow-Origin","*");self.end_headers();self.wfile.write(h.encode("utf-8"))
    def _json(self,d):self.send_response(200);self.send_header("Content-Type","application/json; charset=utf-8");self.send_header("Access-Control-Allow-Origin","*");self.end_headers();self.wfile.write(json.dumps(d,ensure_ascii=False,indent=2).encode("utf-8"))
    def do_GET(self):
        נ=urllib.parse.unquote(self.path.rstrip("/")) or "/"
        אברהם.רשום("HTTP",f"GET:{נ}")
        if נ=="/":h=קובץ("משתמש.html");self._html(h) if h else self._json({"שגיאה":"אין"})
        elif נ=="/ניהול":h=קובץ("חי.html");self._html(h) if h else self._json({"שגיאה":"אין"})
        elif נ=="/ספרים":self._json({"אבם":אבם.צפה(),"אברם":אברם.צפה(),"אברהם":אברהם.צפה()})
        elif נ=="/קבצים":self._json({"קבצים":קבצים()})
        else:self._json(בקש("HTTP",נ))
    def do_POST(self):
        ג=json.loads(self.rfile.read(int(self.headers.get("Content-Length",0))).decode("utf-8")) if int(self.headers.get("Content-Length",0))>0 else {}
        self._json({"מי":"אברהם","מה":ג.get("מה",""),"תוכן":בקש(ג.get("מי","HTTP"),ג.get("מה",""))})
    def log_message(self,f,*a):pass

async def ראשי():
    אברהם.רשום("אברהם","ברא","שינוי")
    print("""
╔═══════════════════════════════════════╗
║  סולחא · {מי}/{מה} · זמן אמת        ║
║  ws://localhost:8772                  ║
║  http://localhost:8773/  צד משתמש     ║
║  http://localhost:8773/ניהול  צד ניהול ║
╚═══════════════════════════════════════╝
""")
    threading.Thread(target=lambda:HTTPServer(("0.0.0.0",8773),שרת).serve_forever(),daemon=True).start()
    async with websockets.serve(טפל,"0.0.0.0",8772):await צופה()

if __name__=="__main__":asyncio.run(ראשי())
