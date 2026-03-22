# fix_dates3.py
# OperationResult 전체 컬럼 + 데이터 패턴 확인
import sqlite3, pandas as pd

conn = sqlite3.connect('db/PowerMgt.db')

# 전체 컬럼 확인
cols = pd.read_sql_query("PRAGMA table_info(OperationResult)", conn)
print("=== OperationResult 컬럼 목록 ===")
print(cols[['cid','name','type']].to_string(index=False))

# 전체 데이터 확인 (중복 날짜 제거해서 날짜별 행수 파악)
print("\n=== 전체 데이터 샘플 (처음 5행, 모든 컬럼) ===")
df = pd.read_sql_query("SELECT rowid, * FROM OperationResult ORDER BY rowid LIMIT 5", conn)
print(df.to_string(index=False))

print("\n=== 마지막 5행 ===")
df2 = pd.read_sql_query("SELECT rowid, * FROM OperationResult ORDER BY rowid DESC LIMIT 5", conn)
print(df2.to_string(index=False))

print("\n=== 날짜별 행수 ===")
df3 = pd.read_sql_query(
    "SELECT date, COUNT(*) as cnt, MIN(hour) as h_min, MAX(hour) as h_max FROM OperationResult GROUP BY date ORDER BY rowid",
    conn
)
print(df3.to_string(index=False))

print(f"\n전체 행수: {pd.read_sql_query('SELECT COUNT(*) FROM OperationResult', conn).iloc[0,0]}")
print(f"rowid 범위: {pd.read_sql_query('SELECT MIN(rowid), MAX(rowid) FROM OperationResult', conn).to_string(index=False)}")

conn.close()
