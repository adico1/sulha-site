#!/usr/bin/env python3
"""
סולחא - main.py
קובץ יחיד · תהליך אחוד · תקשורת אחודה
כל מה שהיה בקבצים נפרדים - עכשיו פנים המערכת
הצופה מציג את תוכן הקובץ בבקשה

פרוטוקול {מי}/{מה} · 3 ליבות · catch all · רישום חובה
WebSocket זמן אמת · 2 טאבים קבועים · צבאות אוטומטי
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
from datetime import datetime

try:
    import websockets
    WS = True
except ImportError:
    WS = False

שורש = os.path.dirname(os.path.abspath(__file__))
פורט = int(os.environ.get("PORT", 8771))
פורט_ws = 8772


# ══════════════════════════════════════
# ליבות: אבם · אברם · אברהם
# ══════════════════════════════════════

class ליבה:
    def __init__(self, שם, אב=None):
        self.שם = שם
        self.אב = אב
        self._נ = threading.Lock()
        self.ספר = []
        self.ספר2 = []
        self.ספור = []

    def רשום(self, מי, מה, כ="בקש"):
        with self._נ:
            ר = {"מי": f"{self.שם}/{מי}", "מה": מה, "כ": כ, "מתי": datetime.now().isoformat()}
            (self.ספר if כ == "בקש" else self.ספר2 if כ == "ענה" else self.ספור).append(ר)
            for ס in [self.ספר, self.ספר2, self.ספור]:
                if len(ס) > 500: del ס[:250]

    def צפה(self):
        return {"שם": self.שם, "אב": self.אב,
                "ספר": {"בקשות": len(self.ספר), "תגובות": len(self.ספר2), "שינויים": len(self.ספור)}}

אבם = ליבה("אבם")
אברם = ליבה("אברם", "אבם")
אברהם = ליבה("אברהם", "אברם")


# ══════════════════════════════════════
# עולמות
# ══════════════════════════════════════

עולמות = {
    "מחשב": {"פנימי": f"localhost:{פורט}", "חיצוני": "localhost", "סוג": "ליבה"},
    "github": {"פנימי": "github", "חיצוני": "https://api.github.com", "סוג": "חוץ", "pages": "adico1.github.io/sulha-site"},
    "דומיין": {"פנימי": "דומיין", "חיצוני": "xn--4dbjgtx.com", "סוג": "במה"},
    "cloudflare": {"פנימי": "cloudflare", "חיצוני": "https://api.cloudflare.com/client/v4", "סוג": "חוץ"},
}


# ══════════════════════════════════════
# צופה ממשק
# ══════════════════════════════════════

class צופה:
    def __init__(self, שם, בסיס, כותרות=None, פעולות=None):
        self.שם = שם; self.בסיס = בסיס; self.כותרות = כותרות or {}
        self.פעולות = פעולות or {}; self.מחובר = False; self.צפיות = 0
        self.רוגזים = 0; self._פעיל = False; self.אחרון = {}

    def בקש(self, נתיב, שיטה="GET"):
        אבם.רשום(self.שם, f"{שיטה}:{נתיב}")
        כ = f"{self.בסיס}{urllib.parse.quote(נתיב, safe='/:?&=%')}"
        try:
            בקשה = urllib.request.Request(כ, method=שיטה)
            for k, v in self.כותרות.items(): בקשה.add_header(k, v)
            ctx = ssl.create_default_context()
            with urllib.request.urlopen(בקשה, context=ctx, timeout=10) as ת:
                תוכן = json.loads(ת.read().decode("utf-8"))
                self.מחובר = True; self.צפיות += 1
                h = json.dumps(תוכן, ensure_ascii=False, sort_keys=True)[:500]
                if h != self.אחרון.get(נתיב):
                    if self.אחרון.get(נתיב): אבם.רשום(self.שם, f"שינוי:{נתיב}", "שינוי")
                    self.אחרון[נתיב] = h
                אבם.רשום(self.שם, f"ענה:{נתיב}", "ענה")
                return תוכן
        except Exception as e:
            self.רוגזים += 1; self.מחובר = False
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
        def _ל():
            while self._פעיל:
                time.sleep(מרווח)
                for פ in self.פעולות: self.עשה(פ)
        threading.Thread(target=_ל, daemon=True).start()

    def עצור(self): self._פעיל = False


# ══════════════════════════════════════
# בקר
# ══════════════════════════════════════

class בקר:
    def __init__(self):
        self.ממשקים = {}; self.בנים = {}
        self._אתחל()

    def _gh_token(self):
        try:
            r = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, timeout=5)
            return r.stdout.strip() if r.returncode == 0 else None
        except: return None

    def _אתחל(self):
        token = self._gh_token()
        if token:
            self.ממשקים["github"] = צופה("github", "https://api.github.com",
                {"Authorization": f"token {token}", "Accept": "application/vnd.github+json", "User-Agent": "sulha"},
                {"סטטוס": ("/repos/adico1/sulha-site/pages", "GET"),
                 "צפיות": ("/repos/adico1/sulha-site/traffic/views", "GET"),
                 "תוכן": ("/repos/adico1/sulha-site/contents/", "GET")})
        self.ממשקים["עצמי"] = צופה("עצמי", f"http://localhost:{פורט}", פעולות={"שורש": ("/", "GET")})

    def צפה_פנים(self):
        return {
            "ליבה": {"ממשקים": len(self.ממשקים), "בנים": len(self.בנים),
                     "רוגזים": sum(מ.רוגזים for מ in self.ממשקים.values())},
            "פנים": {ש: מ.צפה() for ש, מ in self.ממשקים.items()},
            "בנים": {ש: ב.צפה() for ש, ב in self.בנים.items()},
            "עולמות": עולמות,
        }

    def חולל(self, שם, בסיס, כותרות=None, פעולות=None, מרווח=60):
        בן = צופה(שם, בסיס, כותרות, פעולות)
        self.בנים[שם] = בן; בן.הפעל(מרווח)
        אברהם.רשום("מחולל", f"חולל:{שם}", "שינוי")
        return בן.צפה()

    def הפעל(self):
        for ש, מ in self.ממשקים.items():
            if ש != "עצמי": מ.הפעל(60)
        self.חולל("אברם", f"http://localhost:{פורט}",
            פעולות={"צפה": (f"/api/%D7%A6%D7%A4%D7%94", "GET"), "מצב": (f"/api/%D7%9E%D7%A6%D7%91", "GET"),
                     "רוגזים": (f"/api/%D7%A8%D7%95%D7%92%D7%96%D7%99%D7%9D", "GET"),
                     "מחולל": (f"/api/%D7%9E%D7%97%D7%95%D7%9C%D7%9C", "GET"),
                     "ספרים": (f"/api/%D7%A1%D7%A4%D7%A8%D7%99%D7%9D", "GET")}, מרווח=30)
        self.חולל("אבם", f"http://localhost:{פורט}",
            פעולות={"github": (f"/api/%D7%9E%D7%9E%D7%A9%D7%A7/github/%D7%A1%D7%98%D7%98%D7%95%D7%A1", "GET"),
                     "עולמות": (f"/api/%D7%A2%D7%95%D7%9C%D7%9E%D7%95%D7%AA", "GET")}, מרווח=60)
        threading.Thread(target=self._צופה_צבאות, daemon=True).start()

    def צבאות(self):
        אברהם.רשום("צבאות", "התחלה", "שינוי")
        ת = []
        try:
            for cmd in [["git", "add", "-A"],
                        ["git", "commit", "-m", f"צבאות {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"],
                        ["git", "push"]]:
                r = subprocess.run(cmd, capture_output=True, text=True, timeout=30, cwd=שורש)
                ת.append({"פקודה": cmd[-1], "ok": r.returncode == 0})
            אברהם.רשום("צבאות", f"סיום", "ענה")
        except Exception as e:
            אברהם.רשום("צבאות", f"רוגז:{e}", "שינוי")
        return ת

    def _צופה_צבאות(self):
        mt = {}
        while True:
            time.sleep(30)
            שינוי = False
            for ק in os.listdir(שורש):
                נ = os.path.join(שורש, ק)
                if os.path.isfile(נ) and not ק.startswith("."):
                    try:
                        t = os.path.getmtime(נ)
                        if ק in mt and t != mt[ק]: שינוי = True
                        mt[ק] = t
                    except: pass
            if שינוי: self.צבאות()
            # שמור ספרים
            try:
                with open(os.path.join(שורש, "שלשה_ספרים.ספר"), "w", encoding="utf-8") as f:
                    f.write(f"שלשה ספרים · {{מי}}/{{מה}} · {datetime.now().isoformat()}\n═══\n")
                    f.write(json.dumps({"אבם": {"ספר": אבם.ספר[-50:], "תגובות": אבם.ספר2[-50:], "שינויים": אבם.ספור[-50:]},
                        "אברם": {"ספר": אברם.ספר[-50:]}, "אברהם": {"ספר": אברהם.ספר[-50:], "שינויים": אברהם.ספור[-50:]}
                    }, ensure_ascii=False, indent=2))
            except: pass

בקר_ראשי = בקר()


# ══════════════════════════════════════
# תוכן מחולל - פנים המערכת
# כל מה שהיה בקבצים נפרדים
# ══════════════════════════════════════

def תוכן_אתר():
    """האתר - חוץ: שלום עולם · פנים: רישום · פנים פנים: ניהול צפיות"""
    return '''<!DOCTYPE html>
<html lang="he" dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>סולחא</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}body{font-family:'Segoe UI',Tahoma,Arial,sans-serif;background:#f5f0e8;color:#2c2c2c;min-height:100vh}
nav{background:#3a3a2a;padding:12px 24px;display:flex;justify-content:space-between;align-items:center}
nav .logo{color:#e8d9b0;font-size:1.5em;font-weight:bold}nav .links a{color:#ccc;text-decoration:none;margin-inline-start:20px;cursor:pointer}
nav .links a:hover{color:#fff}nav .links a.active{color:#e8d9b0;border-bottom:2px solid #e8d9b0}
.page{display:none;padding:40px 24px;max-width:700px;margin:0 auto}.page.visible{display:block}
h1{margin-bottom:20px;color:#3a3a2a}h2{margin-bottom:16px;color:#4a4a3a}
.card{background:#fff;border-radius:10px;padding:24px;margin-bottom:16px;box-shadow:0 2px 8px rgba(0,0,0,.08)}
input,button{font-size:1em;padding:10px 16px;border-radius:6px;border:1px solid #ccc;font-family:inherit}
input{width:100%;margin-bottom:12px}button{background:#3a3a2a;color:#e8d9b0;border:none;cursor:pointer;padding:10px 24px}
button:hover{background:#4a4a3a}.error{color:#c0392b;margin-bottom:10px}
.views-table{width:100%;border-collapse:collapse}.views-table th,.views-table td{padding:10px 14px;text-align:right;border-bottom:1px solid #eee}
.views-table th{background:#f5f0e8;font-weight:bold}.views-count{font-size:1.3em;font-weight:bold;color:#3a3a2a}
.logout-btn{background:transparent;color:#c0392b;border:1px solid #c0392b;font-size:.85em;padding:6px 14px}.logout-btn:hover{background:#c0392b;color:#fff}
</style></head><body>
<nav><div class="logo">סולחא</div><div class="links">
<a onclick="navigate('hutz')" id="nav-hutz">חוץ</a>
<a onclick="navigate('pnim')" id="nav-pnim">פנים</a>
<a onclick="navigate('pnim-pnim')" id="nav-pnim-pnim" style="display:none;">פנים פנים</a>
<span id="user-area"></span></div></nav>
<div id="page-hutz" class="page visible"><div class="card"><h1>שלום עולם</h1><p>ברוכים הבאים לסולחא.</p></div></div>
<div id="page-pnim" class="page"><div class="card" id="auth-form"><h2 id="auth-title">התחברות</h2>
<div id="auth-message"></div><input type="text" id="auth-username" placeholder="שם משתמש">
<input type="password" id="auth-password" placeholder="סיסמה">
<button onclick="doAuth()"><span id="auth-action-text">התחבר</span></button>
<p style="margin-top:12px"><a href="#" onclick="toggleAuthMode();return false" id="auth-toggle">אין לך חשבון? הירשם</a></p></div></div>
<div id="page-pnim-pnim" class="page"><div class="card"><h2>צפיות פנים</h2>
<table class="views-table"><thead><tr><th>אזור</th><th>צפיות</th></tr></thead><tbody>
<tr><td>ליבה</td><td class="views-count" id="views-liba">0</td></tr>
<tr><td>פנים</td><td class="views-count" id="views-pnim">0</td></tr>
<tr><td>חוץ</td><td class="views-count" id="views-hutz">0</td></tr></tbody></table></div></div>
<script>
let currentUser=JSON.parse(localStorage.getItem('sulha_user')||'null'),isReg=false;
function getViews(){return JSON.parse(localStorage.getItem('sulha_views')||'{"liba":0,"pnim":0,"hutz":0}')}
function addView(a){const v=getViews();v[a]=(v[a]||0)+1;localStorage.setItem('sulha_views',JSON.stringify(v))}
function getUsers(){return JSON.parse(localStorage.getItem('sulha_users')||'{}')}
function saveUsers(u){localStorage.setItem('sulha_users',JSON.stringify(u))}
function navigate(p){document.querySelectorAll('.page').forEach(x=>x.classList.remove('visible'));
document.querySelectorAll('nav .links a').forEach(a=>a.classList.remove('active'));
if(p==='pnim'&&currentUser)p='pnim-pnim';if(p==='pnim-pnim'&&!currentUser)p='pnim';
document.getElementById('page-'+p).classList.add('visible');const n=document.getElementById('nav-'+p);if(n)n.classList.add('active');
const m={hutz:'hutz',pnim:'pnim','pnim-pnim':'liba'};if(m[p])addView(m[p]);if(p==='pnim-pnim')updateViews()}
function updateViews(){const v=getViews();document.getElementById('views-liba').textContent=v.liba||0;
document.getElementById('views-pnim').textContent=v.pnim||0;document.getElementById('views-hutz').textContent=v.hutz||0}
function updateUI(){const n=document.getElementById('nav-pnim-pnim'),u=document.getElementById('user-area');
if(currentUser){n.style.display='inline';u.innerHTML=`<a style="color:#e8d9b0;margin-inline-start:16px">${currentUser}</a> <button class="logout-btn" onclick="logout()">יציאה</button>`}
else{n.style.display='none';u.innerHTML=''}}
function toggleAuthMode(){isReg=!isReg;document.getElementById('auth-title').textContent=isReg?'הרשמה':'התחברות';
document.getElementById('auth-action-text').textContent=isReg?'הירשם':'התחבר';
document.getElementById('auth-toggle').textContent=isReg?'יש לך חשבון? התחבר':'אין לך חשבון? הירשם';document.getElementById('auth-message').innerHTML=''}
function doAuth(){const u=document.getElementById('auth-username').value.trim(),p=document.getElementById('auth-password').value,m=document.getElementById('auth-message');
if(!u||!p){m.innerHTML='<div class="error">נא למלא שם משתמש וסיסמה</div>';return}const users=getUsers();
if(isReg){if(users[u]){m.innerHTML='<div class="error">שם משתמש תפוס</div>';return}users[u]=p;saveUsers(users);currentUser=u;localStorage.setItem('sulha_user',JSON.stringify(currentUser));updateUI();navigate('pnim-pnim')}
else{if(!users[u]||users[u]!==p){m.innerHTML='<div class="error">שם משתמש או סיסמה שגויים</div>';return}currentUser=u;localStorage.setItem('sulha_user',JSON.stringify(currentUser));updateUI();navigate('pnim-pnim')}}
function logout(){currentUser=null;localStorage.removeItem('sulha_user');updateUI();navigate('hutz')}
updateUI();addView('hutz');
</script></body></html>'''


def תוכן_משתמש():
    """טאב משתמש - האתר חי דרך WebSocket"""
    return f'''<!DOCTYPE html>
<html lang="he" dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>סולחא</title>
<style>*{{margin:0;padding:0;box-sizing:border-box}}body{{font-family:'Segoe UI',Tahoma,Arial,sans-serif;background:#f5f0e8;color:#2c2c2c;min-height:100vh}}
#ת{{min-height:100vh}}.ס{{position:fixed;bottom:6px;right:6px;font-size:.65em;color:#999}}</style></head><body>
<div id="ת">טוען...</div><div class="ס"><span id="נ" style="color:red">●</span> <span id="ס">מתחבר</span></div>
<script>let ws,last="";function c(){{ws=new WebSocket("ws://localhost:{פורט_ws}");
ws.onopen=()=>{{document.getElementById("נ").style.color="green";document.getElementById("ס").textContent="חי";ws.send(JSON.stringify({{מי:"משתמש",מה:"אתר"}}))}};
ws.onclose=()=>{{document.getElementById("נ").style.color="red";document.getElementById("ס").textContent="מנותק";setTimeout(c,3000)}};
ws.onmessage=e=>{{const d=JSON.parse(e.data);if(d.מה==="אתר"&&d.תוכן!==last){{last=d.תוכן;document.getElementById("ת").innerHTML=d.תוכן}}}}}};c();
</script></body></html>'''


def תוכן_ניהול():
    """טאב ניהול - צפה פנים חי דרך WebSocket, רק כשיש שינוי"""
    return f'''<!DOCTYPE html>
<html lang="he" dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>סולחא - ניהול</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}body{{font-family:'Segoe UI',Tahoma,Arial,sans-serif;background:#1a1a2e;color:#e0e0e0;height:100vh;display:flex;flex-direction:column}}
header{{background:#16213e;padding:10px 20px;display:flex;justify-content:space-between;align-items:center;border-bottom:2px solid #e8d9b0}}
.שם{{color:#e8d9b0;font-size:1.3em;font-weight:bold}}.נ{{width:10px;height:10px;border-radius:50%;display:inline-block;margin-inline-end:6px}}
.g{{background:#27ae60;box-shadow:0 0 6px #27ae60}}.r{{background:#c0392b}}.o{{background:#f39c12}}
.ת{{flex:1;overflow-y:auto;padding:16px}}.g3{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin-bottom:14px}}
.bx{{background:#16213e;border-radius:8px;padding:12px;text-align:center;border:1px solid #2a2a4a}}
.bt{{color:#e8d9b0;font-weight:bold;font-size:.85em}}.bn{{font-size:1.6em;font-weight:bold}}
.rw{{background:#16213e;border-radius:6px;padding:10px;margin-bottom:6px;border:1px solid #2a2a4a;display:flex;justify-content:space-between;align-items:center}}
.sm{{font-size:.75em;color:#888}}h3{{color:#e8d9b0;margin:12px 0 8px;font-size:.9em}}
</style></head><body>
<header><div class="שם">סולחא - ניהול</div><div><span class="נ r" id="נורה"></span><span id="סט">מתחבר...</span></div></header>
<div class="ת" id="ת">טוען...</div>
<script>let ws,lH="";
function draw(d){{const ת=d.תוכן||{{}};const ל=ת.ליבה||{{}};const פ=ת.פנים||{{}};const ב=ת.בנים||{{}};
let h='<div class="g3">';for(const n of["אבם","אברם","אברהם"]){{const x=ת[n]||{{}};const s=x.ספר||{{}};
h+=`<div class="bx"><div class="bt">${{n}}</div><div class="sm">אב: ${{x.אב||"שורש"}}</div><div class="sm">בקש:${{s.בקשות||0}} ענה:${{s.תגובות||0}} שינוי:${{s.שינויים||0}}</div></div>`}}
h+='</div><div class="g3">';h+=`<div class="bx"><div class="bt">ממשקים</div><div class="bn">${{ל.ממשקים||0}}</div></div>`;
h+=`<div class="bx"><div class="bt">בנים</div><div class="bn">${{ל.בנים||0}}</div></div>`;
h+=`<div class="bx"><div class="bt">רוגזים</div><div class="bn">${{ל.רוגזים||0}}</div></div>`;h+='</div>';
if(Object.keys(פ).length){{h+='<h3>ממשקים</h3>';for(const[n,m] of Object.entries(פ)){{h+=`<div class="rw"><div><span class="נ ${{m.מחובר?"g":"r"}}"></span><b>${{n}}</b></div><div class="sm">צפיות:${{m.צפיות||0}} רוגזים:${{m.רוגזים||0}} פעולות:${{(m.פעולות||[]).join(",")}}</div></div>`}}}}
if(Object.keys(ב).length){{h+='<h3>צופים בנים</h3>';for(const[n,b] of Object.entries(ב)){{h+=`<div class="rw"><div><span class="נ ${{b.מחובר?"g":"o"}}"></span>${{n}}</div><div class="sm">צפיות:${{b.צפיות||0}}</div></div>`}}}}
const ע=ת.עולמות||{{}};if(Object.keys(ע).length){{h+='<h3>עולמות</h3>';for(const[n,w] of Object.entries(ע)){{h+=`<div class="rw"><div><b>${{n}}</b></div><div class="sm">${{w.פנימי}} → ${{w.חיצוני}}</div></div>`}}}}
document.getElementById("ת").innerHTML=h}}
function c(){{ws=new WebSocket("ws://localhost:{פורט_ws}");
ws.onopen=()=>{{document.getElementById("נורה").className="נ g";document.getElementById("סט").textContent="מחובר"}};
ws.onclose=()=>{{document.getElementById("נורה").className="נ r";document.getElementById("סט").textContent="מנותק";setTimeout(c,3000)}};
ws.onmessage=e=>{{const d=JSON.parse(e.data);if(d.מה==="צפה_פנים"){{const h=JSON.stringify(d.תוכן);if(h!==lH){{lH=h;draw(d)}}}}}}}};c();
</script></body></html>'''


# ══════════════════════════════════════
# WebSocket
# ══════════════════════════════════════

ws_מחוברים = set()
ws_hash = {}

async def ws_שלח(מי, מה, תוכן):
    global ws_hash
    h = json.dumps(תוכן, ensure_ascii=False, sort_keys=True)[:2000]
    if h == ws_hash.get(מה): return
    ws_hash[מה] = h
    if ws_מחוברים:
        data = json.dumps({"מי": מי, "מה": מה, "תוכן": תוכן}, ensure_ascii=False)
        await asyncio.gather(*[ws.send(data) for ws in ws_מחוברים if ws.open])

async def ws_טפל(websocket):
    שם = f"דפדפן/{id(websocket)}"
    ws_מחוברים.add(websocket)
    אברהם.רשום(שם, "חיבור", "שינוי")
    await websocket.send(json.dumps({"מי": "אברהם", "מה": "צפה_פנים",
        "תוכן": {**בקר_ראשי.צפה_פנים(), "אבם": אבם.צפה(), "אברם": אברם.צפה(), "אברהם": אברהם.צפה()}
    }, ensure_ascii=False))
    try:
        async for הודעה in websocket:
            ב = json.loads(הודעה); מי = ב.get("מי", שם); מה = ב.get("מה", "")
            אברהם.רשום(מי, מה)
            if מה == "אתר":
                await websocket.send(json.dumps({"מי": "אברהם", "מה": "אתר", "תוכן": תוכן_אתר()}, ensure_ascii=False))
            elif מה == "צפה_פנים":
                await websocket.send(json.dumps({"מי": "אברהם", "מה": "צפה_פנים",
                    "תוכן": {**בקר_ראשי.צפה_פנים(), "אבם": אבם.צפה(), "אברם": אברם.צפה(), "אברהם": אברהם.צפה()}
                }, ensure_ascii=False))
            elif מה == "ספרים":
                await websocket.send(json.dumps({"מי": "אברהם", "מה": "ספרים", "תוכן": {
                    "אבם": אבם.ספר[-20:], "אברם": אברם.ספר[-20:], "אברהם": אברהם.ספר[-20:]
                }}, ensure_ascii=False))
            elif מה.startswith("/"):
                ממשק = "github" if "github" in מה else "עצמי"
                if ממשק in בקר_ראשי.ממשקים:
                    ת = בקר_ראשי.ממשקים[ממשק].בקש(מה)
                    await websocket.send(json.dumps({"מי": "אברהם", "מה": מה, "תוכן": ת}, ensure_ascii=False))
            else:
                ח = מה.split("/", 1)
                if len(ח) == 2 and ח[0] in בקר_ראשי.ממשקים:
                    ת = בקר_ראשי.ממשקים[ח[0]].עשה(ח[1])
                    await websocket.send(json.dumps({"מי": "אברהם", "מה": מה, "תוכן": ת}, ensure_ascii=False))
    finally:
        ws_מחוברים.discard(websocket)
        אברהם.רשום(שם, "ניתוק", "שינוי")

async def ws_צופה():
    while True:
        await asyncio.sleep(5)
        await ws_שלח("אברהם", "צפה_פנים",
            {**בקר_ראשי.צפה_פנים(), "אבם": אבם.צפה(), "אברם": אברם.צפה(), "אברהם": אברהם.צפה()})


# ══════════════════════════════════════
# HTTP שרת - catch all {מי}/{מה}
# ══════════════════════════════════════

class שרתHTTP(http.server.BaseHTTPRequestHandler):
    def _html(self, h):
        self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*"); self.end_headers()
        self.wfile.write(h.encode("utf-8"))

    def _json(self, d):
        self.send_response(200); self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,PUT,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type"); self.end_headers()
        self.wfile.write(json.dumps(d, ensure_ascii=False, indent=2).encode("utf-8"))

    def do_OPTIONS(self): self._json({})

    def do_GET(self):
        נ = urllib.parse.unquote(self.path.rstrip("/")) or "/"
        אברהם.רשום("HTTP", f"GET:{נ}")

        if נ == "/": self._html(תוכן_משתמש())
        elif נ == "/ניהול": self._html(תוכן_ניהול())
        elif נ == "/אתר": self._html(תוכן_אתר())
        elif נ == "/api/צפה": self._json(בקר_ראשי.צפה_פנים())
        elif נ == "/api/מצב": self._json({ש: מ.צפה() for ש, מ in בקר_ראשי.ממשקים.items()})
        elif נ == "/api/רוגזים": self._json({"אבם": אבם.ספור[-20:], "אברם": אברם.ספור[-20:], "אברהם": אברהם.ספור[-20:]})
        elif נ == "/api/מחולל": self._json({ש: ב.צפה() for ש, ב in בקר_ראשי.בנים.items()})
        elif נ == "/api/ספרים": self._json({"אבם": אבם.צפה(), "אברם": אברם.צפה(), "אברהם": אברהם.צפה()})
        elif נ == "/api/עולמות": self._json(עולמות)
        elif נ == "/api/צבאות": self._json(בקר_ראשי.צבאות())
        elif נ.startswith("/api/ממשק/"):
            ח = נ.split("/")
            if len(ח) >= 5 and ח[3] in בקר_ראשי.ממשקים: self._json(בקר_ראשי.ממשקים[ח[3]].עשה(ח[4]))
            elif len(ח) == 4 and ח[3] in בקר_ראשי.ממשקים: self._json(בקר_ראשי.ממשקים[ח[3]].צפה())
            else: self._json({"שגיאה": "לא קיים"})
        else: self._json({"מי": "אברהם", "מה": נ, "תוכן": "catch all"})

    def do_POST(self):
        אורך = int(self.headers.get("Content-Length", 0))
        גוף = json.loads(self.rfile.read(אורך).decode("utf-8")) if אורך > 0 else {}
        נ = urllib.parse.unquote(self.path.rstrip("/"))
        אברהם.רשום(גוף.get("מי", "HTTP"), גוף.get("מה", נ))
        if נ == "/api/חולל":
            self._json(בקר_ראשי.חולל(גוף.get("שם", ""), גוף.get("בסיס", ""),
                גוף.get("כותרות"), גוף.get("פעולות"), גוף.get("מרווח", 60)))
        elif נ == "/api/בקש":
            ממשק = גוף.get("ממשק", "")
            if ממשק in בקר_ראשי.ממשקים:
                self._json(בקר_ראשי.ממשקים[ממשק].בקש(גוף.get("נתיב", "/"), גוף.get("שיטה", "GET")))
            else: self._json({"שגיאה": f"ממשק '{ממשק}' לא קיים"})
        elif נ == "/api/צבאות": self._json(בקר_ראשי.צבאות())
        else: self._json({"מי": "אברהם", "מה": נ})

    def log_message(self, f, *a): pass


# ══════════════════════════════════════
# הפעלה
# ══════════════════════════════════════

def main():
    אברהם.רשום("אברהם", "ברא", "שינוי")
    print(f"""
╔═══════════════════════════════════════════╗
║  סולחא · תהליך אחוד · תקשורת אחודה      ║
║  קובץ יחיד · הכל פנים המערכת              ║
║  http://localhost:{פורט}/       צד משתמש     ║
║  http://localhost:{פורט}/ניהול  צד ניהול      ║
║  ws://localhost:{פורט_ws}     WebSocket        ║
╚═══════════════════════════════════════════╝
""")
    בקר_ראשי.הפעל()
    שרת = http.server.HTTPServer(("0.0.0.0", פורט), שרתHTTP)
    def _אתחל():
        time.sleep(2)
        נ = os.path.join(שורש, "main_קלוד.py")
        if os.path.exists(נ):
            ש = len(open(נ, encoding="utf-8").readlines())
            print(f"[אברהם] למד main_קלוד.py: {ש} שורות")
        webbrowser.open(f"http://localhost:{פורט}/")
        time.sleep(1)
        webbrowser.open(f"http://localhost:{פורט}/ניהול")
        print("[אברהם] 2 טאבים קבועים נפתחו")
    threading.Thread(target=_אתחל, daemon=True).start()
    if WS:
        def _ws():
            asyncio.run(_ws_main())
        async def _ws_main():
            async with websockets.serve(ws_טפל, "0.0.0.0", פורט_ws):
                print(f"[ws] ws://localhost:{פורט_ws}")
                await ws_צופה()
        threading.Thread(target=_ws, daemon=True).start()
    try:
        שרת.serve_forever()
    except KeyboardInterrupt:
        print("\nסולחא נעצר.")
        שרת.server_close()

if __name__ == "__main__":
    main()
