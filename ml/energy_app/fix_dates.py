# fix_dates.py
# OperationResult 날짜 '2021--0-1-' 형태 → '2021-01-01' 수정
import sqlite3, re

conn = sqlite3.connect('db/PowerMgt.db')
cur  = conn.cursor()

rows = cur.execute("SELECT rowid, date FROM OperationResult").fetchall()
fixed = 0

for rowid, date_val in rows:
    d = str(date_val).strip()
    # '2021--0-1-' → 숫자만 추출해서 재조합
    nums = re.findall(r'\d+', d)
    if len(nums) >= 3:
        year, month, day = nums[0], nums[1].zfill(2), nums[2].zfill(2)
        new_date = f"{year}-{month}-{day}"
        if new_date != d:
            cur.execute("UPDATE OperationResult SET date=? WHERE rowid=?",
                        (new_date, rowid))
            fixed += 1

conn.commit()

# 결과 확인
samples = cur.execute(
    "SELECT date FROM OperationResult LIMIT 5"
).fetchall()
print(f"✅ 날짜 수정 완료: {fixed}건")
print("수정 후 샘플:")
for r in samples:
    print(f"  {r[0]}")

conn.close()
