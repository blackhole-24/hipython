# fix_dates2.py
# OperationResult 날짜 패턴 분석 → 정확히 수정
import sqlite3, re

conn = sqlite3.connect('db/PowerMgt.db')
cur  = conn.cursor()

# ── 1. 원본 날짜 패턴 전체 확인 ──────────────────────────────
print("=== 원본 날짜 값 전체 (중복 제거) ===")
rows = cur.execute(
    "SELECT DISTINCT date FROM OperationResult ORDER BY rowid LIMIT 30"
).fetchall()
for r in rows:
    print(f"  '{r[0]}'")

# ── 2. 행 번호와 함께 첫 20개 확인 ──────────────────────────
print("\n=== rowid + date + hour 첫 20개 ===")
rows2 = cur.execute(
    "SELECT rowid, date, hour FROM OperationResult ORDER BY rowid LIMIT 20"
).fetchall()
for r in rows2:
    print(f"  rowid={r[0]}  date='{r[1]}'  hour={r[2]}")

conn.close()
