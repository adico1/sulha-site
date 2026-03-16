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
            # אף פעם לא מוחק - append only

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
                h = json.dumps(תוכן, ensure_ascii=False, sort_keys=True)
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
        self.ממשקים["עצמי"] = צופה("עצמי", f"http://localhost:{פורט}", פעולות={"צפה": ("/api/%D7%A6%D7%A4%D7%94", "GET"), "שעה": ("/api/%D7%A9%D7%A2%D7%94", "GET")})

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
            מ.הפעל(60)
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
                with open(os.path.join(שורש, "שלשה_ספרים.ספר"), "a", encoding="utf-8") as f:
                    f.write(f"שלשה ספרים · {{מי}}/{{מה}} · {datetime.now().isoformat()}\n═══\n")
                    f.write(json.dumps({"אבם": {"ספר": אבם.ספר, "תגובות": אבם.ספר2, "שינויים": אבם.ספור},
                        "אברם": {"ספר": אברם.ספר}, "אברהם": {"ספר": אברהם.ספר, "שינויים": אברהם.ספור}
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


def שעון_js():
    """שעון חי + מכריעים - משותף לכל צפה"""
    return '''
<div id="שעון-מיכל" style="position:fixed;bottom:8px;left:8px;background:rgba(0,0,0,.85);color:#e8d9b0;padding:8px 14px;border-radius:8px;font-family:monospace;font-size:.85em;z-index:9999;border:1px solid #333">
<div id="שעון">00:00:00.000</div>
<div id="רוגז-שעון" style="color:#c0392b;font-size:.7em;display:none"></div>
<div id="מכריעים" style="display:none;margin-top:6px;font-size:.75em">
<button onclick="מכריע('תקן')" style="background:#27ae60;color:#fff;border:none;padding:3px 8px;border-radius:4px;cursor:pointer;margin:2px">תקן</button>
<button onclick="מכריע('רגוז')" style="background:#c0392b;color:#fff;border:none;padding:3px 8px;border-radius:4px;cursor:pointer;margin:2px">רגוז</button>
<button onclick="מכריע('שתוק')" style="background:#666;color:#fff;border:none;padding:3px 8px;border-radius:4px;cursor:pointer;margin:2px">שתוק</button>
<button onclick="מכריע('שחוק')" style="background:#f39c12;color:#fff;border:none;padding:3px 8px;border-radius:4px;cursor:pointer;margin:2px">שחוק</button>
<button onclick="מכריע('הרהר')" style="background:#3498db;color:#fff;border:none;padding:3px 8px;border-radius:4px;cursor:pointer;margin:2px">הרהר</button>
<button onclick="מכריע('העלם')" style="background:#333;color:#fff;border:none;padding:3px 8px;border-radius:4px;cursor:pointer;margin:2px">העלם</button>
<button onclick="מכריע('למד')" style="background:#8e44ad;color:#fff;border:none;padding:3px 8px;border-radius:4px;cursor:pointer;margin:2px">למד</button>
<button onclick="מכריע('צייר')" style="background:#e91e63;color:#fff;border:none;padding:3px 8px;border-radius:4px;cursor:pointer;margin:2px">צייר</button>
</div>
</div>
<script>
let שעון_שרת=null,הפרש=0,מצב_שעון="חי",נעלם=false;
function עדכן_שעון(){
const ע=new Date();const ש=ע.toLocaleTimeString("he-IL",{hour12:false})+"."+String(ע.getMilliseconds()).padStart(3,"0");
document.getElementById("שעון").textContent=ש;
if(Math.abs(הפרש)>2000&&מצב_שעון!=="שתוק"&&מצב_שעון!=="העלם"){
document.getElementById("רוגז-שעון").style.display="block";
document.getElementById("רוגז-שעון").textContent="רוגז: הפרש "+Math.round(הפרש)+"ms מהשרת";
document.getElementById("מכריעים").style.display="block"}
requestAnimationFrame(עדכן_שעון)}
עדכן_שעון();

async function בדוק_שעה(){try{
const ל=Date.now();const r=await fetch("/api/%D7%A9%D7%A2%D7%94");const d=await r.json();
const א=Date.now();הפרש=(ל+א)/2-new Date(d.שעה).getTime();שעון_שרת=d.שעה;
if(Math.abs(הפרש)<2000){document.getElementById("רוגז-שעון").style.display="none";document.getElementById("מכריעים").style.display="none"}
}catch(e){}}
setInterval(בדוק_שעה,10000);בדוק_שעה();

function מכריע(פ){
const ר=document.getElementById("רוגז-שעון");const מ=document.getElementById("מכריעים");const ש=document.getElementById("שעון-מיכל");
מצב_שעון=פ;
if(פ==="תקן"){ר.style.display="none";מ.style.display="none";ר.textContent=""}
else if(פ==="רגוז"){ר.textContent="רוגז! הפרש "+Math.round(הפרש)+"ms";ר.style.color="#c0392b"}
else if(פ==="שתוק"){ר.style.display="none";מ.style.display="none"}
else if(פ==="שחוק"){ר.textContent="😄 "+Math.round(הפרש)+"ms? סבבה!";ר.style.color="#f39c12";ר.style.display="block"}
else if(פ==="הרהר"){ר.textContent="🤔 למה "+Math.round(הפרש)+"ms...";ר.style.color="#3498db";ר.style.display="block"}
else if(פ==="העלם"){נעלם=true;ש.style.opacity="0";ש.style.transition="opacity 1s";setTimeout(()=>{ש.style.display="none";
const כ=document.createElement("div");כ.style.cssText="position:fixed;bottom:8px;left:8px;z-index:9999;cursor:pointer;font-size:1.2em";
כ.textContent="⏰";כ.onclick=()=>{ש.style.display="block";ש.style.opacity="1";כ.remove();נעלם=false;מצב_שעון="חי"};
document.body.appendChild(כ)},1000)}
else if(פ==="למד"){ר.textContent="📚 לומד בבידוד... הפרש: "+Math.round(הפרש)+"ms";ר.style.color="#8e44ad";ר.style.display="block";מ.style.display="none";
setTimeout(()=>{ר.textContent="📚 למד! הפרש נורמלי: ±2 שניות";setTimeout(()=>{ר.style.display="none"},3000)},3000)}
else if(פ==="צייר"){ר.innerHTML="🎨 ";const צ=["תקן","רגוז","שתוק","שחוק","הרהר","העלם","למד"];
צ.forEach((כ,i)=>{const ב=document.createElement("span");ב.textContent=כ;ב.style.cssText="display:inline-block;cursor:pointer;margin:0 3px;animation:spin "+(0.5+i*0.2)+"s infinite alternate;font-size:.9em";
ב.onclick=()=>מכריע(כ);ר.appendChild(ב)});ר.style.display="block";ר.style.color="#e91e63"}
}
</script>'''

def תוכן_משתמש():
    """טאב משתמש - האתר חי דרך WebSocket + שעון + מכריעים"""
    return f'''<!DOCTYPE html>
<html lang="he" dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>סולחא</title>
<style>*{{margin:0;padding:0;box-sizing:border-box}}body{{font-family:'Segoe UI',Tahoma,Arial,sans-serif;background:#f5f0e8;color:#2c2c2c;min-height:100vh}}
#ת{{min-height:100vh}}.ס{{position:fixed;bottom:6px;right:6px;font-size:.65em;color:#999}}</style></head><body>
<div id="ת">טוען...</div><div class="ס"><span id="נ" style="color:red">●</span> <span id="ס">מתחבר</span></div>
{שעון_js()}
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
h+=`<div class="bx"><div class="bt">${{n}}</div><div class="sm">אב: ${{x.אב||"שורש"}}</div><div class="sm">בקש:${{s.בקשות||s.ספר||0}} ענה:${{s.תגובות||0}} שינוי:${{s.שינויים||0}}</div></div>`}}
h+='</div><div class="g3">';h+=`<div class="bx"><div class="bt">ממשקים</div><div class="bn">${{ל.ממשקים||0}}</div></div>`;
h+=`<div class="bx"><div class="bt">בנים</div><div class="bn">${{ל.בנים||0}}</div></div>`;
h+=`<div class="bx"><div class="bt">רוגזים</div><div class="bn">${{ל.רוגזים||0}}</div></div>`;h+='</div>';

h+=`<div class="bx" style="text-align:right"><div class="bt">שעה</div><div class="bn">${{ת.שעה||"?"}}</div></div>`;

if(Object.keys(פ).length){{h+='<h3>ממשקים</h3>';for(const[n,m] of Object.entries(פ)){{h+=`<div class="rw"><div><span class="נ ${{m.מחובר?"g":"r"}}"></span><b>${{n}}</b></div><div class="sm">צפיות:${{m.צפיות||0}} רוגזים:${{m.רוגזים||0}} פעיל:${{m.פעיל}} פעולות:${{(m.פעולות||[]).join(",")}}</div></div>`}}}}
if(Object.keys(ב).length){{h+='<h3>צופים בנים</h3>';for(const[n,b] of Object.entries(ב)){{h+=`<div class="rw"><div><span class="נ ${{b.מחובר?"g":"o"}}"></span>${{n}}</div><div class="sm">צפיות:${{b.צפיות||0}} פעיל:${{b.פעיל}}</div></div>`}}}}
const ע=ת.עולמות||{{}};if(Object.keys(ע).length){{h+='<h3>עולמות</h3>';for(const[n,w] of Object.entries(ע)){{h+=`<div class="rw"><div><b>${{n}}</b></div><div class="sm">${{w.פנימי||""}} → ${{w.חיצוני||""}} (${{w.סוג||""}})</div></div>`}}}}

const ס=ת.ספרים||{{}};if(Object.keys(ס).length){{h+='<h3>ספרים</h3>';for(const[n,v] of Object.entries(ס)){{h+=`<div class="rw"><div class="c">${{n}}</div><div class="sm">${{JSON.stringify(v)}}</div></div>`}}}}

const ר=ת.רוגזים||{{}};let רסהכ=0;for(const[n,v] of Object.entries(ר)){{if(Array.isArray(v))רסהכ+=v.length}};
if(רסהכ>0){{h+='<h3>רוגזים ('+רסהכ+')</h3>';for(const[n,v] of Object.entries(ר)){{if(Array.isArray(v))for(const x of v.slice(-5)){{h+=`<div class="rw" style="background:#200"><div class="sm">${{x.מי||""}} ${{x.מה||""}}</div><div class="sm">${{(x.מתי||"").slice(-8)}}</div></div>`}}}}}}

if(ת.נתיב){{h+='<h3>בקשה אחרונה</h3><div class="rw"><div class="c">'+ת.נתיב+'</div><div class="sm">'+ת.שעה+'</div></div>'}}
if(ת.צופי_דפדפן){{h+='<h3>דפדפנים ('+ת.צופי_דפדפן.length+')</h3>';for(const ד of ת.צופי_דפדפן){{h+='<div class="rw"><div class="sm"><span class="נ g"></span>'+ד.מי+'</div></div>'}}}}
if(ת.בקשות_אדי){{h+='<h3>בקשות אדי ('+ת.בקשות_אדי.length+')</h3>';for(const ב of ת.בקשות_אדי.slice(-20).reverse()){{h+='<div class="rw"><div class="sm">'+ב.מה.substring(0,150)+'</div></div>'}}}}
if(ת.תת){{h+='<div class="rw" style="background:#020"><div class="c">תת: '+ת.תת.מה+'</div></div>'}}
document.getElementById("ת").innerHTML=h}}
function c(){{ws=new WebSocket("ws://localhost:{פורט_ws}");
ws.onopen=()=>{{document.getElementById("נורה").className="נ g";document.getElementById("סט").textContent="מחובר"}};
ws.onclose=()=>{{document.getElementById("נורה").className="נ r";document.getElementById("סט").textContent="מנותק";setTimeout(c,3000)}};
ws.onmessage=e=>{{const d=JSON.parse(e.data);if(d.מה==="צפה_פנים"||d.מה==="בקשה"||d.מה==="תת-בקשה"){{const h=JSON.stringify(d.תוכן);if(h!==lH){{lH=h;draw(d)}}}}}}}};c();
</script>
{שעון_js()}
</body></html>'''


# ══════════════════════════════════════
# WebSocket
# ══════════════════════════════════════

_ws_event_loop = None
ws_מחוברים = set()
ws_hash = {}

async def ws_שלח(מי, מה, תוכן):
    global ws_hash
    h = json.dumps(תוכן, ensure_ascii=False, sort_keys=True)[:2000]
    if h == ws_hash.get(מה): return
    ws_hash[מה] = h
    if ws_מחוברים:
        data = json.dumps({"מי": מי, "מה": מה, "תוכן": תוכן}, ensure_ascii=False)
        await asyncio.gather(*[ws.send(data) for ws in list(ws_מחוברים) if not getattr(ws, "closed", False)])

async def ws_טפל(websocket):
    שם = f"דפדפן/{id(websocket)}"
    ws_מחוברים.add(websocket)
    אברהם.רשום(שם, "חיבור", "שינוי")
    # שלח מצב מלא כולל בקשות אדי וכל הצופים
    import glob as _g
    _בקשות = []
    _לוגים = _g.glob(os.path.expanduser("~/.claude/projects/-Users-adicohen-------------/*.jsonl"))
    if _לוגים:
        with open(_לוגים[0], "r") as _f:
            for _line in _f:
                try:
                    _d = json.loads(_line)
                    if _d.get("type") == "human":
                        _msg = _d.get("message", {})
                        if isinstance(_msg, dict):
                            for _c in _msg.get("content", []):
                                if isinstance(_c, dict) and _c.get("type") == "text" and len(_c["text"]) > 5:
                                    _בקשות.append({"מי": "אדי", "מה": _c["text"][:300]})
                except: pass
    await websocket.send(json.dumps({"מי": "אברהם", "מה": "צפה_פנים",
        "תוכן": {**בקר_ראשי.צפה_פנים(), "אבם": אבם.צפה(), "אברם": אברם.צפה(), "אברהם": אברהם.צפה(),
                  "שעה": datetime.now().isoformat(),
                  "ספרים": {"אבם": {"ספר": len(אבם.ספר), "תגובות": len(אבם.ספר2), "שינויים": len(אבם.ספור)},
                             "אברם": {"ספר": len(אברם.ספר)}, "אברהם": {"ספר": len(אברהם.ספר), "שינויים": len(אברהם.ספור)}},
                  "רוגזים": {"אבם": אבם.ספור[-5:], "אברהם": אברהם.ספור[-5:]},
                  "בקשות_אדי": _בקשות,
                  "צופי_דפדפן": [{"מי": f"דפדפן/{id(w)}", "מחובר": True} for w in ws_מחוברים]}
    }, ensure_ascii=False))
    try:
        async for הודעה in websocket:
            ב = json.loads(הודעה); מי = ב.get("מי", שם); מה = ב.get("מה", "")
            אברהם.רשום(מי, מה)
            בדוק_ספירות(מה, None)
            if מה == "אתר":
                await websocket.send(json.dumps({"מי": "אברהם", "מה": "אתר", "תוכן": תוכן_אתר()}, ensure_ascii=False))
            elif מה == "צפה_פנים":
                await websocket.send(json.dumps({"מי": "אברהם", "מה": "צפה_פנים",
                    "תוכן": {**בקר_ראשי.צפה_פנים(), "אבם": אבם.צפה(), "אברם": אברם.צפה(), "אברהם": אברהם.צפה()}
                }, ensure_ascii=False))
            elif מה == "ספרים":
                await websocket.send(json.dumps({"מי": "אברהם", "מה": "ספרים", "תוכן": {
                    "אבם": אבם.ספר, "אברם": אברם.ספר, "אברהם": אברהם.ספר
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
    except Exception:
        pass
    finally:
        ws_מחוברים.discard(websocket)
        אברהם.רשום(שם, "ניתוק", "שינוי")

async def ws_צופה():
    # צופה - ממתין לפוטנציאל מבקשות
    while True:
        await asyncio.sleep(0.1)  # ממתין לפוטנציאל
        if ws_מחוברים:
            await ws_שלח("אברהם", "צפה_פנים",
                {**בקר_ראשי.צפה_פנים(), "אבם": אבם.צפה(), "אברם": אברם.צפה(), "אברהם": אברהם.צפה(),
                 "שעה": datetime.now().isoformat(),
                 "ספרים": {"אבם": {"ספר": len(אבם.ספר), "תגובות": len(אבם.ספר2), "שינויים": len(אבם.ספור)},
                            "אברם": {"ספר": len(אברם.ספר)},
                            "אברהם": {"ספר": len(אברהם.ספר), "שינויים": len(אברהם.ספור)}},
                 "רוגזים": {"אבם": אבם.ספור[-5:], "אברהם": אברהם.ספור[-5:]},
                 "בקשות_אדי": אברהם.ספר[-10:]})


# ══════════════════════════════════════
# HTTP שרת - catch all {מי}/{מה}
# ══════════════════════════════════════


# בדיקות עשר ספירות - על כל קלט תהליך ופלט
def בדוק_ספירות(נתיב, תשובה):
    """בדיקת עשר ספירות על כל בקשה"""
    ספירות = {}
    ספירות["ראשית"] = נתיב is not None  # יש קלט
    ספירות["אחרית"] = תשובה is not None  # יש פלט
    ספירות["טוב"] = not isinstance(תשובה, dict) or "שגיאה" not in תשובה  # אין שגיאה
    ספירות["רע"] = isinstance(תשובה, dict) and "שגיאה" in תשובה  # יש שגיאה
    ספירות["רום"] = isinstance(תשובה, (dict, list))  # תשובה מובנית
    ספירות["תחת"] = len(str(תשובה)) > 2  # תשובה לא ריקה
    ספירות["מזרח"] = isinstance(נתיב, str) and len(נתיב) > 0  # נתיב תקין
    ספירות["מערב"] = True  # הגיע לבדיקה = תהליך עבד
    ספירות["צפון"] = True  # נרשם
    ספירות["דרום"] = True  # נשלח
    # רוגז אם נכשל
    if ספירות["רע"]:
        אברהם.רשום("ספירות/רוגז", f"{נתיב}:{תשובה.get('שגיאה','')}", "שינוי")
    return ספירות

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
        בדוק_ספירות(self.path, d)

    def _py(self, d, שם="צפה"):
        """פלט קוד פייתון - לא JSON"""
        self.send_response(200); self.send_header("Content-Type", "text/x-python; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*"); self.end_headers()
        קוד = f"# {שם}\nfrom datetime import datetime\nשעה = \"{datetime.now().isoformat()}\"\n"
        if isinstance(d, dict):
            for מ, ע in d.items():
                מב = str(מ).replace("-", "_").replace("/", "_").replace(" ", "_")
                קוד += f"{מב} = {repr(ע)}\n"
        elif isinstance(d, list):
            קוד += f"רשימה = {repr(d)}\n"
        else:
            קוד += f"ערך = {repr(d)}\n"
        self.wfile.write(קוד.encode("utf-8"))
        בדוק_ספירות(self.path, d)
        # כל בקשה → שלח מיד לדפדפנים
        try:
            נ = urllib.parse.unquote(self.path.rstrip("/")) or "/"
            הודעה = json.dumps({"מי": "אברהם", "מה": "בקשה", "תוכן": {
                "נתיב": נ, "שעה": datetime.now().isoformat(), "תשובה": d,
                **בקר_ראשי.צפה_פנים(), "אבם": אבם.צפה(), "אברם": אברם.צפה(), "אברהם": אברהם.צפה(),
                "ספרים": {"אבם": {"ספר": len(אבם.ספר), "תגובות": len(אבם.ספר2), "שינויים": len(אבם.ספור)},
                           "אברם": {"ספר": len(אברם.ספר)},
                           "אברהם": {"ספר": len(אברהם.ספר), "שינויים": len(אברהם.ספור)}},
                "רוגזים": {"אבם": אבם.ספור[-5:], "אברהם": אברהם.ספור[-5:]}
            }}, ensure_ascii=False)
            try:
                for ws in list(ws_מחוברים):
                    asyncio.run_coroutine_threadsafe(ws.send(הודעה), _ws_event_loop)
            except: pass
        except: pass

    def do_OPTIONS(self): self._json({})

    def do_GET(self):
        נ = urllib.parse.unquote(self.path.rstrip("/")) or "/"
        אברהם.רשום("HTTP", f"GET:{נ}")

        if נ == "/": self._html(תוכן_משתמש())
        elif נ == "/ניהול": self._html(תוכן_ניהול())
        elif נ == "/אתר": self._html(תוכן_אתר())
        elif נ == "/api/צפה": self._json(בקר_ראשי.צפה_פנים())
        elif נ == "/api/מצב": self._json({ש: מ.צפה() for ש, מ in בקר_ראשי.ממשקים.items()})
        elif נ == "/api/רוגזים": self._json({"אבם": אבם.ספור, "אברם": אברם.ספור, "אברהם": אברהם.ספור})
        elif נ == "/api/מחולל": self._json({ש: ב.צפה() for ש, ב in בקר_ראשי.בנים.items()})
        elif נ == "/api/ספרים": self._json({"אבם": אבם.צפה(), "אברם": אברם.צפה(), "אברהם": אברהם.צפה()})
        elif נ == "/api/עולמות": self._json(עולמות)
        elif נ == "/api/צבאות": self._json(בקר_ראשי.צבאות())
        elif נ == "/api/מחולל-בקשה":
            self._json({"שגיאה": "POST בלבד"})
        elif נ == "/api/שעה": self._json({"שעה": datetime.now().isoformat(), "יום_הולדת_יקום": datetime.now().strftime("%H:%M:%S.%f")[:-3]})
        elif נ.startswith("/api/ממשק/"):
            ח = נ.split("/")
            if len(ח) >= 5 and ח[3] in בקר_ראשי.ממשקים: self._json(בקר_ראשי.ממשקים[ח[3]].עשה(ח[4]))
            elif len(ח) == 4 and ח[3] in בקר_ראשי.ממשקים: self._json(בקר_ראשי.ממשקים[ח[3]].צפה())
            else: self._json({"שגיאה": "לא קיים"})
        elif נ == "/api/למד":
            קמ = {}
            for ק in os.listdir(שורש):
                נק = os.path.join(שורש, ק)
                if os.path.isfile(נק) and not ק.startswith("."):
                    try:
                        with open(נק, "r", encoding="utf-8") as f: תק = f.read()
                        קמ[ק] = {"שורות": len(תק.split(chr(10))), "אורך": len(תק)}
                        אברהם.רשום("למד", "קובץ:" + ק, "ענה")
                    except: pass
            self._json(קמ)
        elif נ == "/api/בקשות":
            import glob as _g
            לוגים = _g.glob(os.path.expanduser("~/.claude/projects/-Users-adicohen-------------/*.jsonl"))
            בקשות_אדי = []
            if לוגים:
                with open(לוגים[0], "r") as _f:
                    for _line in _f:
                        try:
                            _d = json.loads(_line)
                            if _d.get("type") == "human":
                                _msg = _d.get("message", {})
                                if isinstance(_msg, dict):
                                    for _c in _msg.get("content", []):
                                        if isinstance(_c, dict) and _c.get("type") == "text" and len(_c["text"]) > 5:
                                            בקשות_אדי.append({"מי": "אדי", "מה": _c["text"][:500]})
                        except: pass
            self._json({"בקשות": בקשות_אדי, "סהכ": len(בקשות_אדי)})
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
        elif נ == "/api/מחולל-בקשה":
            self._json({"שגיאה": "POST בלבד"})
        elif נ == "/api/מחולל-בקשה":
            טקסט = גוף.get("בקשה", גוף.get("מה", ""))
            מילים = טקסט.split()
            תתי = []
            for i in range(len(מילים)):
                for j in range(2, min(4, len(מילים) - i + 1)):
                    תתי.append({"מי": גוף.get("מי", "מחולל"), "מה": " ".join(מילים[i:i+j])})
            for ת in תתי:
                אבם.רשום(ת["מי"], ת["מה"])
                אברהם.רשום(ת["מי"], ת["מה"])
            try:
                for ת in תתי:
                    הודעה = json.dumps({"מי": "מחולל", "מה": "תת-בקשה", "תוכן": {
                        "בקשה": טקסט, "תת": ת, "שעה": datetime.now().isoformat(),
                        **בקר_ראשי.צפה_פנים(), "אבם": אבם.צפה(), "אברם": אברם.צפה(), "אברהם": אברהם.צפה()
                    }}, ensure_ascii=False)
                    for ws in list(ws_מחוברים):
                        asyncio.run_coroutine_threadsafe(ws.send(הודעה), _ws_event_loop)
            except: pass
            self._json({"בקשה": טקסט, "תתי_בקשות": תתי, "סהכ": len(תתי)})
        else: self._json({"מי": "אברהם", "מה": נ})

    def log_message(self, f, *a): pass


# ══════════════════════════════════════
# הפעלה
# ══════════════════════════════════════

def main():
    # אברהם תמיד ראשון - הרוג כל מתחרה על הפורטים שלי
    import signal
    for p in [פורט, פורט_ws]:
        try:
            r = subprocess.run(["lsof", "-ti", f":{p}"], capture_output=True, text=True)
            for pid in r.stdout.strip().split("\n"):
                if pid and int(pid) != os.getpid():
                    os.kill(int(pid), signal.SIGKILL)
                    print(f"[אברהם] הרג מתחרה PID {pid} על פורט {p}")
        except:
            pass
    # חכה עד שהפורטים באמת פנויים
    for _ in range(10):
        פנוי = True
        for p in [פורט, פורט_ws]:
            r = subprocess.run(['lsof', '-ti', f':{p}'], capture_output=True, text=True)
            if r.stdout.strip():
                פנוי = False
                for pid in r.stdout.strip().split(chr(10)):
                    if pid and int(pid) != os.getpid():
                        try: os.kill(int(pid), 9)
                        except: pass
        if פנוי: break
        time.sleep(1)
    time.sleep(1)

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

# חוש - watchdog צופה מערכת קבצים בזמן אמת
try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler

    class חוש_קבצים(FileSystemEventHandler):
        def on_any_event(self, event):
            אברהם.רשום("חוש/קבצים", f"{event.event_type}:{event.src_path}", "שינוי")
            # רוגז על כמות גדולה של קבצים
            try:
                הודעה = json.dumps({"מי": "חוש", "מה": "קובץ", "תוכן": {
                    "סוג": event.event_type, "נתיב": event.src_path,
                    "שעה": datetime.now().isoformat()
                }}, ensure_ascii=False)
                for ws in list(ws_מחוברים):
                    asyncio.run_coroutine_threadsafe(ws.send(הודעה), _ws_event_loop)
            except: pass

    _חוש = Observer()
    _חוש.schedule(חוש_קבצים(), שורש, recursive=False)
    _חוש.start()
    print("[חוש] watchdog פעיל")
except ImportError:
    print("[חוש] watchdog לא מותקן")

    # retry bind - לעולם לא יכשל
    שרת = None
    for _ in range(20):
        try:
            שרת = http.server.HTTPServer(("0.0.0.0", פורט), שרתHTTP)
            break
        except OSError:
            for p in [פורט, פורט_ws]:
                r = subprocess.run(["lsof", "-ti", f":{p}"], capture_output=True, text=True)
                for pid in r.stdout.strip().split(chr(10)):
                    if pid and int(pid) != os.getpid():
                        try: os.kill(int(pid), 9)
                        except: pass
            time.sleep(1)
    if not שרת:
        print("[אברהם] רוגז: לא הצליח לתפוס פורט")
        שרת = http.server.HTTPServer(("0.0.0.0", פורט), שרתHTTP)
    def _אתחל():
        time.sleep(2)
        נ = os.path.join(שורש, "main_קלוד.py")
        if os.path.exists(נ):
            ש = len(open(נ, encoding="utf-8").readlines())
            print(f"[אברהם] למד main_קלוד.py: {ש} שורות")
        webbrowser.open(f"http://localhost:{פורט}/")
        time.sleep(1)
        webbrowser.open(f"http://localhost:{פורט}/%D7%A0%D7%99%D7%94%D7%95%D7%9C")
        print("[אברהם] 2 טאבים קבועים נפתחו")
    threading.Thread(target=_אתחל, daemon=True).start()
    if WS:
        def _ws():
            asyncio.run(_ws_main())
        async def _ws_main():
            global _ws_event_loop
            _ws_event_loop = asyncio.get_event_loop()
            async with websockets.serve(ws_טפל, "0.0.0.0", פורט_ws):
                print(f"[ws] ws://localhost:{פורט_ws}")
                await ws_צופה()
        threading.Thread(target=_ws, daemon=True).start()
    print(f'[אברהם] שרת מאזין על {פורט}')
    try:
        שרת.serve_forever()
    except KeyboardInterrupt:
        print("\nסולחא נעצר.")
        שרת.server_close()

if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception as e:
            # רוגז מיידי - תפוס, רשום, תקן, נסה שוב
            try:
                with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "שלשה_ספרים.ספר"), "a", encoding="utf-8") as f:
                    f.write(chr(10) + "=== רוגז/קריסה " + str(e) + " " + __import__("datetime").datetime.now().isoformat() + " ===" + chr(10))
                print(f"[רוגז] {e} - מתקן ומנסה שוב")
            except: pass
            import time; time.sleep(2)
