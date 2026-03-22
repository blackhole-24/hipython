# fix_dates_final.py
# rowid 순서 기반으로 날짜 정확히 재구성
# rowid 721~6168 = 216행 = 9일 × 24시간
# rowid 721~744 = 1일차 00~23시, 745~768 = 2일차 ...
import sqlite3
from datetime import date, timedelta

conn = sqlite3.connect('db/PowerMgt.db')
cur  = conn.cursor()

# rowid 전체 목록 순서대로 가져오기
rows = cur.execute(
    "SELECT rowid FROM OperationResult ORDER BY rowid"
).fetchall()

print(f"총 행수: {len(rows)}")
print(f"rowid 범위: {rows[0][0]} ~ {rows[-1][0]}")

# bill_rate로 월 추정
# 109.8 = 겨울(11~2월), 167.2 = 봄가을(3~5,9월), 191.6 = 여름(6~8월)
sample = cur.execute(
    "SELECT bill_rate, COUNT(*) as cnt FROM OperationResult GROUP BY bill_rate"
).fetchall()
print("\nbill_rate 분포:")
for r in sample:
    season = {109.8:'겨울(11~2월)', 167.2:'봄가을(3~5,9월)', 191.6:'여름(6~8월)'}.get(r[0], '?')
    print(f"  {r[0]} → {season}: {r[1]}행")

# 날짜 추정:
# 216행 = 9일치. bill_rate 109.8이 앞부분에 있으면 겨울(1월),
# 167.2가 뒤에 있으면 봄 or 9월
# rowid가 원본 okm 데이터(6168행)의 일부라면 → 원본 데이터 1~9일
# 원본 데이터 시작: 2021-01-01 (1월 1일)
START_DATE = date(2021, 1, 1)

print(f"\n추정 시작 날짜: {START_DATE} (2021년 1월 1일)")
print("(bill_rate 109.8 = 겨울요금 → 1~2월 데이터로 판단)")

# rowid 순서대로 날짜 할당 (24시간 = 1일)
updates = []
for i, (rowid,) in enumerate(rows):
    day_offset = i // 24        # 0~8 (9일)
    new_date   = START_DATE + timedelta(days=day_offset)
    updates.append((new_date.strftime('%Y-%m-%d'), rowid))

# 미리보기
print("\n[수정 미리보기 - 처음 5행]")
for u in updates[:5]:
    print(f"  rowid={u[1]} → {u[0]}")
print("[수정 미리보기 - 마지막 5행]")
for u in updates[-5:]:
    print(f"  rowid={u[1]} → {u[0]}")

confirm = input("\n위 날짜로 수정하시겠습니까? (y/n): ").strip().lower()
if confirm != 'y':
    print("취소되었습니다.")
    conn.close()
    exit()

# 실제 UPDATE
cur.executemany(
    "UPDATE OperationResult SET date=? WHERE rowid=?",
    updates
)
conn.commit()

# 결과 확인
print("\n=== 수정 완료 후 날짜별 행수 ===")
import pandas as pd
df = pd.read_sql_query(
    "SELECT date, COUNT(*) as cnt, MIN(hour) as h_min, MAX(hour) as h_max "
    "FROM OperationResult GROUP BY date ORDER BY date",
    conn
)
print(df.to_string(index=False))

print(f"\n✅ 날짜 수정 완료: {len(updates)}건")
conn.close()
