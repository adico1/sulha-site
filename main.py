#!/usr/bin/env python3
"""
סולחא - main.py
ליבה ראשית · פרוטוקול {מי}/{מה}
3 ליבות: אבם (יסוד) · אברם (כיוון) · אברהם (ניהול)
3×3 שכבות · 5 מימדים · catch all · רישום חובה
WebSocket זמן אמת · HTTP · 2 טאבים קבועים

כתובות:
  פנימיות מקוצרות: {מי}/{מה}
  חיצוניות ארוכות: https://domain/{מי}/{מה}

עולמות:
  מחשב מקומי: localhost:8771 (ליבה)
  github pages: adico1.github.io/sulha-site (חוץ)
  דומיין: סולחא.com / xn--4dbjgtx.com (במה)
"""

import asyncio
import http.server
import json
import os
import subprocess
import threading
import time
import urllib.request
import urllib.parse
import urllib.error
import ssl
import webbrowser
from pathlib import Path
from datetime import datetime

try:
    import websockets
    WS_ENABLED = True
except ImportError:
    WS_ENABLED = False

שורש = Path(__file__).parent
פורט_http = int(os.environ.get("PORT", 8771))
פורט_ws = 8772


# ══════════════════════════════════════
# ליבות: אבם · אברם · אברהם
# כל ליבה: ספר (בקשות) · ספר (תגובות) · ספור (שינויים)
# ══════════════════════════════════════

class ליבה:
    def __init__(self, שם, אב=None):
        self.שם = שם
        self.אב = אב
        self._נ = threading.Lock()
        self.ספר = []     # בקשות
        self.ספר2 = []    # תגובות
        self.ספור = []    # שינויים

    def רשום(self, מי, מה, כיוון="בקש"):
        with self._נ:
            ר = {"מי": f"{self.שם}/{מי}", "מה": מה, "כ": כיוון, "מתי": datetime.now().isoformat()}
            dest = self.ספר if כיוון == "בקש" else self.ספר2 if כיוון == "ענה" else self.ספור
            dest.append(ר)
            if len(dest) > 500:
                del dest[:250]
            return ר

    def צפה(self):
        return {
            "שם": self.שם, "אב": self.אב,
            "ספר": {"בקשות": len(self.ספר), "תגובות": len(self.ספר2), "שינויים": len(self.ספור)}
        }

אבם = ליבה("אבם")
אברם = ליבה("אברם", "אבם")
אברהם_ליבה = ליבה("אברהם", "אברם")


# ══════════════════════════════════════
# כתובות עולמות
# ══════════════════════════════════════

עולמות = {
    "מחשב": {"פנימי": f"localhost:{פורט_http}", "חיצוני": "localhost", "סוג": "ליבה"},
    "github": {"פנימי": "github", "חיצוני": "https://api.github.com", "סוג": "חוץ",
                "pages": "adico1.github.io/sulha-site"},
    "דומיין": {"פנימי": "דומיין", "חיצוני": "xn--4dbjgtx.com", "סוג": "במה"},
    "cloudflare": {"פנימי": "cloudflare", "חיצוני": "https://api.cloudflare.com/client/v4", "סוג": "חוץ"},
}


# ══════════════════════════════════════
# קבצים - שכבה 1
# ══════════════════════════════════════

def קובץ(שם):
    נ = שורש / שם
    return נ.read_text(encoding="utf-8") if נ.exists() else None

def קבצים():
    return [f.name for f in שורש.iterdir() if f.is_file() and not f.name.startswith(".")]


# ══════════════════════════════════════
# צופה ממשק - {מי}/{מה}
# ══════════════════════════════════════

class צופה:
    def __init__(self, שם, בסיס, כותרות=None, פעולות=None):
        self.שם = שם
        self.בסיס = בסיס
        self.כותרות = כותרות or {}
        self.פעולות = פעולות or {}
        self.מחובר = False
        self.צפיות = 0
        self.רוגזים = 0
        self._פעיל = False
        self.אחרון = {}

    def בקש(self, נתיב, שיטה="GET"):
        אבם.רשום(self.שם, f"{שיטה}:{נתיב}")
        כ = f"{self.בסיס}{urllib.parse.quote(נתיב, safe='/:?&=%')}"
        try:
            בקשה = urllib.request.Request(כ, method=שיטה)
            for k, v in self.כותרות.items():
                בקשה.add_header(k, v)
            ctx = ssl.create_default_context()
            with urllib.request.urlopen(בקשה, context=ctx, timeout=10) as ת:
                תוכן = json.loads(ת.read().decode("utf-8"))
                self.מחובר = True
                self.צפיות += 1
                # חש שינוי
                hash_חדש = json.dumps(תוכן, ensure_ascii=False, sort_keys=True)[:500]
                if hash_חדש != self.אחרון.get(נתיב):
                    if self.אחרון.get(נתיב):
                        אבם.רשום(self.שם, f"שינוי:{נתיב}", "שינוי")
                    self.אחרון[נתיב] = hash_חדש
                אבם.רשום(self.שם, f"ענה:{נתיב}", "ענה")
                return תוכן
        except Exception as e:
            self.רוגזים += 1
            self.מחובר = False
            אבם.רשום(self.שם, f"רוגז:{e}", "שינוי")
            return {"שגיאה": str(e)}

    def עשה(self, פעולה):
        if פעולה in self.פעולות:
            נתיב, שיטה = self.פעולות[פעולה]
            return self.בקש(נתיב, שיטה)
        return {"שגיאה": f"פעולה '{פעולה}' לא ידועה"}

    def צפה(self):
        return {"שם": self.שם, "מחובר": self.מחובר, "צפיות": self.צפיות,
                "רוגזים": self.רוגזים, "פעולות": list(self.פעולות.keys()), "פעיל": self._פעיל}

    def הפעל(self, מרווח=60):
        if self._פעיל: return
        self._פעיל = True
        def _לולאה():
            while self._פעיל:
                time.sleep(מרווח)
                for פ in self.פעולות:
                    self.עשה(פ)
        threading.Thread(target=_לולאה, daemon=True).start()

    def עצור(self):
        self._פעיל = False


# ══════════════════════════════════════
# בקר אברהם - ניהול כל הממשקים
# ══════════════════════════════════════

class בקר:
    def __init__(self):
        self.ממשקים = {}
        self.מחולל_בנים = {}
        self._אתחל()

    def _קבל_gh_token(self):
        try:
            r = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, timeout=5)
            return r.stdout.strip() if r.returncode == 0 else None
        except:
            return None

    def _אתחל(self):
        # github
        token = self._קבל_gh_token()
        if token:
            self.ממשקים["github"] = צופה("github", "https://api.github.com",
                {"Authorization": f"token {token}", "Accept": "application/vnd.github+json", "User-Agent": "sulha"},
                {"סטטוס": ("/repos/adico1/sulha-site/pages", "GET"),
                 "צפיות": ("/repos/adico1/sulha-site/traffic/views", "GET"),
                 "תוכן": ("/repos/adico1/sulha-site/contents/", "GET")})

        # עצמי
        self.ממשקים["עצמי"] = צופה("עצמי", f"http://localhost:{פורט_http}",
            פעולות={"שורש": ("/", "GET")})

    def צפה_פנים(self):
        return {
            "ליבה": {"ממשקים": len(self.ממשקים), "בנים": len(self.מחולל_בנים),
                     "רוגזים": sum(מ.רוגזים for מ in self.ממשקים.values())},
            "פנים": {שם: מ.צפה() for שם, מ in self.ממשקים.items()},
            "בנים": {שם: ב.צפה() for שם, ב in self.מחולל_בנים.items()},
            "עולמות": עולמות,
            "קבצים": קבצים(),
        }

    def חולל(self, שם, בסיס, כותרות=None, פעולות=None, מרווח=60):
        בן = צופה(שם, בסיס, כותרות, פעולות)
        self.מחולל_בנים[שם] = בן
        בן.הפעל(מרווח)
        אברהם_ליבה.רשום("מחולל", f"חולל:{שם}", "שינוי")
        return בן.צפה()

    def הפעל_צופים(self):
        for שם, מ in self.ממשקים.items():
            if שם != "עצמי":
                מ.הפעל(60)

בקר_ראשי = בקר()


# ══════════════════════════════════════
# WebSocket - תקשורת אחודה זמן אמת
# רק כשיש שינוי
# ══════════════════════════════════════

ws_מחוברים = set()
צפה_hash_אחרון = {}

async def ws_שלח_שינוי(מי, מה, תוכן):
    global צפה_hash_אחרון
    h = json.dumps(תוכן, ensure_ascii=False, sort_keys=True)[:2000]
    if h == צפה_hash_אחרון.get(מה):
        return  # אין שינוי
    צפה_hash_אחרון[מה] = h
    if ws_מחוברים:
        data = json.dumps({"מי": מי, "מה": מה, "תוכן": תוכן}, ensure_ascii=False)
        await asyncio.gather(*[ws.send(data) for ws in ws_מחוברים if ws.open])

async def ws_טפל(websocket):
    שם = f"דפדפן/{id(websocket)}"
    ws_מחוברים.add(websocket)
    אברהם_ליבה.רשום(שם, "חיבור", "שינוי")

    # שלח מצב ראשוני
    await websocket.send(json.dumps({"מי": "אברהם", "מה": "צפה_פנים",
        "תוכן": {**בקר_ראשי.צפה_פנים(), "אבם": אבם.צפה(), "אברם": אברם.צפה(), "אברהם": אברהם_ליבה.צפה()}
    }, ensure_ascii=False))

    try:
        async for הודעה in websocket:
            ב = json.loads(הודעה)
            מי = ב.get("מי", שם)
            מה = ב.get("מה", "")
            אברהם_ליבה.רשום(מי, מה)

            if מה == "אתר":
                h = קובץ("index.html")
                if h:
                    await websocket.send(json.dumps({"מי": "אברהם", "מה": "אתר", "תוכן": h}, ensure_ascii=False))

            elif מה == "צפה_פנים":
                await websocket.send(json.dumps({"מי": "אברהם", "מה": "צפה_פנים",
                    "תוכן": {**בקר_ראשי.צפה_פנים(), "אבם": אבם.צפה(), "אברם": אברם.צפה(), "אברהם": אברהם_ליבה.צפה()}
                }, ensure_ascii=False))

            elif מה == "ספרים":
                await websocket.send(json.dumps({"מי": "אברהם", "מה": "ספרים", "תוכן": {
                    "אבם": אבם.ספר[-20:], "אברם": אברם.ספר[-20:], "אברהם": אברהם_ליבה.ספר[-20:]
                }}, ensure_ascii=False))

            elif מה.startswith("/"):
                # catch all
                ממשק = "github" if "github" in מה else "עצמי"
                if ממשק in בקר_ראשי.ממשקים:
                    ת = בקר_ראשי.ממשקים[ממשק].בקש(מה)
                    await websocket.send(json.dumps({"מי": "אברהם", "מה": מה, "תוכן": ת}, ensure_ascii=False))

            else:
                # {מי}/{מה} - עשה על ממשק
                חלקים = מה.split("/", 1)
                if len(חלקים) == 2 and חלקים[0] in בקר_ראשי.ממשקים:
                    ת = בקר_ראשי.ממשקים[חלקים[0]].עשה(חלקים[1])
                    await websocket.send(json.dumps({"מי": "אברהם", "מה": מה, "תוכן": ת}, ensure_ascii=False))
                else:
                    await websocket.send(json.dumps({"מי": "אברהם", "מה": מה, "תוכן": {"שגיאה": "לא מוכר"}}, ensure_ascii=False))
    finally:
        ws_מחוברים.discard(websocket)
        אברהם_ליבה.רשום(שם, "ניתוק", "שינוי")

async def ws_צופה():
    """צופה - שולח לדפדפנים רק כשיש שינוי"""
    while True:
        await asyncio.sleep(5)
        תוכן = {**בקר_ראשי.צפה_פנים(), "אבם": אבם.צפה(), "אברם": אברם.צפה(), "אברהם": אברהם_ליבה.צפה()}
        await ws_שלח_שינוי("אברהם", "צפה_פנים", תוכן)
        # שמור ספרים
        try:
            with open(שורש / "שלשה_ספרים.ספר", "w", encoding="utf-8") as f:
                f.write(f"שלשה ספרים · {{מי}}/{{מה}} · {datetime.now().isoformat()}\n═══\n")
                f.write(json.dumps({"אבם": {"ספר": אבם.ספר[-50:], "תגובות": אבם.ספר2[-50:], "שינויים": אבם.ספור[-50:]},
                    "אברם": {"ספר": אברם.ספר[-50:]}, "אברהם": {"ספר": אברהם_ליבה.ספר[-50:], "שינויים": אברהם_ליבה.ספור[-50:]}
                }, ensure_ascii=False, indent=2))
        except:
            pass


# ══════════════════════════════════════
# HTML מחולל - 2 טאבים קבועים
# ══════════════════════════════════════

def html_משתמש():
    """טאב 1: צד משתמש - האתר חי דרך WebSocket"""
    return '''<!DOCTYPE html>
<html lang="he" dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>סולחא</title>
<style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:'Segoe UI',Tahoma,Arial,sans-serif;background:#f5f0e8;color:#2c2c2c;min-height:100vh}
#תוכן{min-height:100vh}.ס{position:fixed;bottom:6px;right:6px;font-size:.65em;color:#999}</style></head><body>
<div id="תוכן">טוען...</div><div class="ס"><span id="נ" style="color:red">●</span> <span id="ס">מתחבר</span></div>
<script>
let ws,last="";
function c(){ws=new WebSocket("ws://localhost:''' + str(פורט_ws) + '''");
ws.onopen=()=>{document.getElementById("נ").style.color="green";document.getElementById("ס").textContent="חי";ws.send(JSON.stringify({מי:"משתמש",מה:"אתר"}))};
ws.onclose=()=>{document.getElementById("נ").style.color="red";document.getElementById("ס").textContent="מנותק";setTimeout(c,3000)};
ws.onmessage=e=>{const d=JSON.parse(e.data);if(d.מה==="אתר"&&d.תוכן!==last){last=d.תוכן;document.getElementById("תוכן").innerHTML=d.תוכן}}}
c();
</script></body></html>'''


def html_ניהול():
    """טאב 2: צד ניהול - צפה פנים חי דרך WebSocket, רק כשיש שינוי"""
    return '''<!DOCTYPE html>
<html lang="he" dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>סולחא - ניהול</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Segoe UI',Tahoma,Arial,sans-serif;background:#1a1a2e;color:#e0e0e0;height:100vh;display:flex;flex-direction:column}
header{background:#16213e;padding:10px 20px;display:flex;justify-content:space-between;align-items:center;border-bottom:2px solid #e8d9b0}
.שם{color:#e8d9b0;font-size:1.3em;font-weight:bold}
.נ{width:10px;height:10px;border-radius:50%;display:inline-block;margin-inline-end:6px}
.g{background:#27ae60;box-shadow:0 0 6px #27ae60}.r{background:#c0392b}.o{background:#f39c12}
.תוכן{flex:1;overflow-y:auto;padding:16px}
.grid3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin-bottom:14px}
.box{background:#16213e;border-radius:8px;padding:12px;text-align:center;border:1px solid #2a2a4a}
.box-t{color:#e8d9b0;font-weight:bold;font-size:.85em}.box-n{font-size:1.6em;font-weight:bold}
.row{background:#16213e;border-radius:6px;padding:10px;margin-bottom:6px;border:1px solid #2a2a4a;display:flex;justify-content:space-between;align-items:center}
.row.chg{border-color:#e8d9b0;animation:blink .5s}
@keyframes blink{0%{background:#2a2a1a}100%{background:#16213e}}
.sm{font-size:.75em;color:#888}
h3{color:#e8d9b0;margin:12px 0 8px;font-size:.9em}
</style></head><body>
<header><div class="שם">סולחא - ניהול</div><div><span class="נ r" id="נורה"></span><span id="סטטוס">מתחבר...</span></div></header>
<div class="תוכן" id="תוכן">טוען...</div>
<script>
let ws,lastH="";
function draw(d){
const ת=d.תוכן||{};const ל=ת.ליבה||{};const פ=ת.פנים||{};const ב=ת.בנים||{};
let h='<div class="grid3">';
for(const n of["אבם","אברם","אברהם"]){const x=ת[n]||{};const s=x.ספר||{};
h+=`<div class="box"><div class="box-t">${n}</div><div class="sm">אב: ${x.אב||"שורש"}</div><div class="sm">בקש:${s.בקשות||0} ענה:${s.תגובות||0} שינוי:${s.שינויים||0}</div></div>`}
h+='</div><div class="grid3">';
h+=`<div class="box"><div class="box-t">ממשקים</div><div class="box-n">${ל.ממשקים||0}</div></div>`;
h+=`<div class="box"><div class="box-t">בנים</div><div class="box-n">${ל.בנים||0}</div></div>`;
h+=`<div class="box"><div class="box-t">רוגזים</div><div class="box-n">${ל.רוגזים||0}</div></div>`;
h+='</div>';
if(Object.keys(פ).length){h+='<h3>ממשקים</h3>';
for(const[n,m] of Object.entries(פ)){h+=`<div class="row"><div><span class="נ ${m.מחובר?"g":"r"}"></span><b>${n}</b></div><div class="sm">צפיות:${m.צפיות||0} רוגזים:${m.רוגזים||0} פעולות:${(m.פעולות||[]).join(",")}</div></div>`}}
if(Object.keys(ב).length){h+='<h3>צופים בנים</h3>';
for(const[n,b] of Object.entries(ב)){h+=`<div class="row"><div><span class="נ ${b.מחובר?"g":"o"}"></span>${n}</div><div class="sm">צפיות:${b.צפיות||0}</div></div>`}}
const ע=ת.עולמות||{};if(Object.keys(ע).length){h+='<h3>עולמות</h3>';
for(const[n,w] of Object.entries(ע)){h+=`<div class="row"><div><b>${n}</b></div><div class="sm">${w.פנימי} → ${w.חיצוני}</div></div>`}}
const ק=ת.קבצים||[];if(ק.length){h+=`<h3>קבצים (${ק.length})</h3><div class="sm">${ק.join(" · ")}</div>`}
document.getElementById("תוכן").innerHTML=h}

function c(){ws=new WebSocket("ws://localhost:''' + str(פורט_ws) + '''");
ws.onopen=()=>{document.getElementById("נורה").className="נ g";document.getElementById("סטטוס").textContent="מחובר"};
ws.onclose=()=>{document.getElementById("נורה").className="נ r";document.getElementById("סטטוס").textContent="מנותק";setTimeout(c,3000)};
ws.onmessage=e=>{const d=JSON.parse(e.data);if(d.מה==="צפה_פנים"){const h=JSON.stringify(d.תוכן);if(h!==lastH){lastH=h;draw(d)}}
else if(d.מה==="רוגז"){document.getElementById("סטטוס").textContent="רוגז!";setTimeout(()=>document.getElementById("סטטוס").textContent="מחובר",2000)}}}
c();
</script></body></html>'''


# ══════════════════════════════════════
# HTTP שרת - catch all {מי}/{מה}
# ══════════════════════════════════════

class שרתHTTP(http.server.BaseHTTPRequestHandler):
    def _html(self, h):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(h.encode("utf-8"))

    def _json(self, d):
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(json.dumps(d, ensure_ascii=False, indent=2).encode("utf-8"))

    def do_OPTIONS(self):
        self._json({})

    def do_GET(self):
        נ = urllib.parse.unquote(self.path.rstrip("/")) or "/"
        אברהם_ליבה.רשום("HTTP", f"GET:{נ}")

        # 2 טאבים קבועים
        if נ == "/":
            self._html(html_משתמש())
        elif נ == "/ניהול":
            self._html(html_ניהול())

        # API - צפה פנים
        elif נ == "/api/צפה":
            self._json(בקר_ראשי.צפה_פנים())
        elif נ == "/api/מצב":
            self._json({שם: מ.צפה() for שם, מ in בקר_ראשי.ממשקים.items()})
        elif נ == "/api/רוגזים":
            self._json({"אבם": אבם.ספור[-20:], "אברם": אברם.ספור[-20:], "אברהם": אברהם_ליבה.ספור[-20:]})
        elif נ == "/api/מחולל":
            self._json({שם: ב.צפה() for שם, ב in בקר_ראשי.מחולל_בנים.items()})
        elif נ == "/api/ספרים":
            self._json({"אבם": אבם.צפה(), "אברם": אברם.צפה(), "אברהם": אברהם_ליבה.צפה()})
        elif נ == "/api/עולמות":
            self._json(עולמות)
        elif נ == "/api/קבצים":
            self._json({"קבצים": קבצים()})

        # ממשק/פעולה
        elif נ.startswith("/api/ממשק/"):
            חלקים = נ.split("/")  # ['', 'api', 'ממשק', שם, פעולה?]
            if len(חלקים) >= 5:
                שם = חלקים[3]
                פעולה = חלקים[4]
                if שם in בקר_ראשי.ממשקים:
                    self._json(בקר_ראשי.ממשקים[שם].עשה(פעולה))
                else:
                    self._json({"שגיאה": f"ממשק '{שם}' לא קיים"})
            elif len(חלקים) == 4:
                שם = חלקים[3]
                if שם in בקר_ראשי.ממשקים:
                    self._json(בקר_ראשי.ממשקים[שם].צפה())
                else:
                    self._json({"שגיאה": f"ממשק '{שם}' לא קיים"})

        # catch all
        else:
            self._json({"מי": "אברהם", "מה": נ, "תוכן": "catch all", "עולמות": list(עולמות.keys())})

    def do_POST(self):
        אורך = int(self.headers.get("Content-Length", 0))
        גוף = json.loads(self.rfile.read(אורך).decode("utf-8")) if אורך > 0 else {}
        נ = urllib.parse.unquote(self.path.rstrip("/"))
        מי = גוף.get("מי", "HTTP")
        מה = גוף.get("מה", נ)
        אברהם_ליבה.רשום(מי, מה)

        if נ == "/api/חולל":
            ת = בקר_ראשי.חולל(גוף.get("שם", ""), גוף.get("בסיס", ""),
                גוף.get("כותרות"), גוף.get("פעולות"), גוף.get("מרווח", 60))
            self._json(ת)
        elif נ == "/api/בקש":
            ממשק = גוף.get("ממשק", "")
            if ממשק in בקר_ראשי.ממשקים:
                self._json(בקר_ראשי.ממשקים[ממשק].בקש(גוף.get("נתיב", "/"), גוף.get("שיטה", "GET")))
            else:
                self._json({"שגיאה": f"ממשק '{ממשק}' לא קיים"})
        else:
            self._json({"מי": "אברהם", "מה": מה, "תוכן": "catch all POST"})

    def log_message(self, f, *a):
        pass


# ══════════════════════════════════════
# הפעלה
# ══════════════════════════════════════

def main():
    אברהם_ליבה.רשום("אברהם", "ברא", "שינוי")

    print(f"""
╔═══════════════════════════════════════════╗
║  סולחא · {{מי}}/{{מה}} · ליבה ראשית        ║
║  3 ליבות: אבם · אברם · אברהם              ║
╠═══════════════════════════════════════════╣
║  http://localhost:{פורט_http}    צד משתמש (/)  ║
║  http://localhost:{פורט_http}/ניהול  צד ניהול    ║
║  ws://localhost:{פורט_ws}    WebSocket זמן אמת║
╚═══════════════════════════════════════════╝
""")

    # הפעל צופים
    בקר_ראשי.הפעל_צופים()

    # HTTP שרת
    שרת = http.server.HTTPServer(("0.0.0.0", פורט_http), שרתHTTP)

    def _אתחל():
        time.sleep(2)
        # למד קוד קלוד
        נ = שורש / "main_קלוד.py"
        if נ.exists():
            שורות = len(נ.read_text(encoding="utf-8").split("\n"))
            print(f"[אברהם] למד main_קלוד.py: {שורות} שורות")
            אברהם_ליבה.רשום("אברהם", f"למד:main_קלוד.py:{שורות}", "ענה")

        # פתח 2 טאבים קבועים
        webbrowser.open(f"http://localhost:{פורט_http}/")
        time.sleep(1)
        webbrowser.open(f"http://localhost:{פורט_http}/ניהול")
        print("[אברהם] 2 טאבים קבועים נפתחו")

    threading.Thread(target=_אתחל, daemon=True).start()

    # WebSocket
    if WS_ENABLED:
        def _ws():
            asyncio.run(_ws_main())
        async def _ws_main():
            async with websockets.serve(ws_טפל, "0.0.0.0", פורט_ws):
                print(f"[ws] ws://localhost:{פורט_ws}")
                await ws_צופה()
        threading.Thread(target=_ws, daemon=True).start()
    else:
        print("[ws] websockets לא מותקן - ללא זמן אמת")

    try:
        שרת.serve_forever()
    except KeyboardInterrupt:
        print("\nסולחא נעצר.")
        for מ in בקר_ראשי.ממשקים.values():
            מ.עצור()
        שרת.server_close()

if __name__ == "__main__":
    main()
