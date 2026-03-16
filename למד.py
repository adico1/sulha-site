#!/usr/bin/env python3
"""למד.py - אברהם חולל דרך המחולל (GitHub API)
לומד קבצים, רושם בספרים מלא בלי קיצורים, מתקן"""
import json,os,urllib.request,urllib.parse
from datetime import datetime
שורש=os.path.dirname(os.path.abspath(__file__))
במה='http://localhost:8771'
def בקש(נ,ש='GET',ג=None):
    ח=נ.split('/')
    נמ='/'.join(urllib.parse.quote(x,safe='') if x else x for x in ח)
    try:
        נת=json.dumps(ג,ensure_ascii=False).encode('utf-8') if ג else None
        ב=urllib.request.Request(f'{במה}{נמ}',data=נת,method=ש)
        ב.add_header('Content-Type','application/json; charset=utf-8')
        with urllib.request.urlopen(ב,timeout=15) as ת: return json.loads(ת.read().decode('utf-8'))
    except Exception as e: return {'error':str(e)}
def למד(שם):
    נ=os.path.join(שורש,שם)
    if os.path.isfile(נ):
        with open(נ,'r',encoding='utf-8') as f: return f.read()
def רשום(מי,מה,תוכן):
    with open(os.path.join(שורש,'שלשה_ספרים.ספר'),'a',encoding='utf-8') as f:
        f.write(f'
=== {מי}/{מה} {datetime.now().isoformat()} ===
'+תוכן+'
')
def תקן(שם,ישן,חדש):
    נ=os.path.join(שורש,שם)
    if os.path.isfile(נ):
        with open(נ,'r',encoding='utf-8') as f: ת=f.read()
        if ישן in ת:
            with open(נ,'w',encoding='utf-8') as f: f.write(ת.replace(ישן,חדש,1))
            return True
    return False
if __name__=='__main__':
    print('למד.py - אברהם חולל דרך המחולל')
    for ק in sorted(os.listdir(שורש)):
        if os.path.isfile(os.path.join(שורש,ק)) and not ק.startswith('.'):
            ת=למד(ק)
            if ת: רשום('אברהם/למד',ק,ת); print(f'  {ק}: {len(ת)}b {len(ת.split(chr(10)))} שורות')
    if תקן('main.py','webbrowser.open(f"http://localhost:{פורט}/ניהול")','webbrowser.open(f"http://localhost:{פורט}/%D7%A0%D7%99%D7%94%D7%95%D7%9C")'):
        print('  תוקן: URL ניהול')
        רשום('אברהם/תיקון','url-ניהול','URL מקודד')
    בקש('/api/חולל','POST',{'שם':'למד/צופה','בסיס':במה,'פעולות':{'צפה':('/api/%D7%A6%D7%A4%D7%94','GET')},'מרווח':60})
    print('סיים')
