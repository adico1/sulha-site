#!/usr/bin/env python3
# ממיר.תקן.newlines.py
# תקן newlines בקבצי python

from pathlib import Path
import re

def taken_newlines(file_path):
    path = Path(file_path)
    if not path.exists():
        return "לא נמצא"
    
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # מצא f.write עם newline פנימי ותקן
    # דפוס: f.write("...
") -> רשימת שורות
    
    fixed = content.replace(
        "f.write("# חתימת אדון הכל
")",
        "lines = ["# חתימת אדון הכל"]"
    )
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(fixed)
    
    return "תוקן"

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        result = taken_newlines(sys.argv[1])
        print(result)
