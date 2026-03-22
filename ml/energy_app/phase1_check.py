# ================================================================
# phase1_check.py
# Phase 1 전체 점검 스크립트
# 실행: python phase1_check.py
# ================================================================

import os, sys

print("=" * 60)
print("Phase 1 점검 — 올라운더팀 에너지 예측 시스템")
print("=" * 60)

results = []

# ── 1. 패키지 확인 ────────────────────────────────────────────
print("\n[1] 패키지 확인")
packages = {
    'pandas':   'pd',
    'numpy':    'np',
    'joblib':   'joblib',
    'xgboost':  'xgb',
    'sklearn':  'sklearn',
    'sqlite3':  'sqlite3',
    'streamlit':'st',
    'requests': 'requests',
    'plotly':   'plotly',
}
for pkg, alias in packages.items():
    try:
        __import__(pkg)
        print(f"  ✅ {pkg}")
        results.append((pkg, True))
    except ImportError:
        print(f"  ❌ {pkg}  →  pip install {pkg}")
        results.append((pkg, False))

# ── 2. pkl 파일 확인 ──────────────────────────────────────────
print("\n[2] pkl 파일 확인")
pkl_paths = [
    'energy_pipeline_v4.pkl',
    'models/energy_pipeline_v4.pkl',
    'energy_pipeline_v3.pkl',
    'models/energy_pipeline_v3.pkl',
]
pkl_found = False
for p in pkl_paths:
    if os.path.exists(p):
        size_mb = os.path.getsize(p) / 1024 / 1024
        print(f"  ✅ 발견: {p}  ({size_mb:.1f} MB)")
        pkl_found = True
        break
if not pkl_found:
    print("  ❌ pkl 파일 없음!")
    print("  → energy_pipeline_v4.pkl 을 이 폴더 또는 models/ 에 넣으세요.")
results.append(('pkl', pkl_found))

# ── 3. DB 파일 확인 ───────────────────────────────────────────
print("\n[3] DB 파일 확인")
db_paths = ['db/PowerMgt.db', 'PowerMgt.db']
db_path  = None
for p in db_paths:
    if os.path.exists(p):
        size_kb = os.path.getsize(p) / 1024
        print(f"  ✅ 발견: {p}  ({size_kb:.0f} KB)")
        db_path = p
        break
if not db_path:
    print("  ❌ PowerMgt.db 없음!")
    print("  → db/PowerMgt.db 경로에 파일을 배치하세요.")
results.append(('db', db_path is not None))

# ── 4. DB 테이블 확인 ─────────────────────────────────────────
if db_path:
    print("\n[4] DB 테이블 확인")
    import sqlite3, pandas as pd
    conn = sqlite3.connect(db_path)

    required_tables = {
        'WeatherForecast': '날씨 예보',
        'OperationForecast': '예측 결과 저장',
        'OperationResult': '실적 데이터',
        'Calendar': '공휴일 기준',
        'ElectricityTariff': 'TOU 요금',
        'DRResult': 'DR 결과 저장',
    }

    for tbl, desc in required_tables.items():
        try:
            cnt = pd.read_sql_query(f"SELECT COUNT(*) FROM {tbl}", conn).iloc[0, 0]
            icon = '✅' if cnt > 0 or tbl in ['OperationForecast', 'DRResult'] else '⚠'
            note = '' if cnt > 0 else ' ← 비어있음 (정상: 예측 후 채워짐)' if tbl == 'OperationForecast' else ''
            print(f"  {icon} {tbl:25s} {cnt:6d}행  ({desc}){note}")
        except Exception:
            print(f"  ❌ {tbl:25s} 없음  ({desc}) → db_setup.py 실행 필요")

    conn.close()

# ── 5. predictor1.py 파일 확인 ────────────────────────────────
print("\n[5] predictor1.py 확인")
if os.path.exists('predictor1.py'):
    print("  ✅ predictor1.py 존재")
else:
    print("  ❌ predictor1.py 없음 → 이 폴더에 붙여넣기 하세요.")
results.append(('predictor1', os.path.exists('predictor1.py')))

# ── 6. 핵심 데이터 CSV 확인 ───────────────────────────────────
print("\n[6] 데이터 CSV 확인")
csv_files = {
    'data/okm_enriched_final.csv': 'ESG 집계용 (8760행 37컬럼)',
    'data/okm_full_2021_pe.csv':   '팀원 GMM 통합본 (8760행)',
}
for path, desc in csv_files.items():
    if os.path.exists(path):
        import pandas as pd
        try:
            df = pd.read_csv(path, nrows=1, encoding='utf-8-sig')
            print(f"  ✅ {path}  ({desc})")
        except Exception as e:
            print(f"  ⚠ {path}  읽기 오류: {e}")
    else:
        print(f"  ❌ {path}  없음  ({desc})")

# ── 최종 요약 ─────────────────────────────────────────────────
print("\n" + "="*60)
print("Phase 1 점검 결과 요약")
print("="*60)

all_ok = all(ok for _, ok in results)
if all_ok:
    print("✅ 모든 항목 정상 — Phase 2 (HTML 구현)로 진행 가능!")
else:
    print("❌ 아래 항목을 먼저 해결하세요:")
    for name, ok in results:
        if not ok:
            print(f"   - {name}")
    print()
    print("해결 방법:")
    print("  1. 패키지 설치: pip install xgboost scikit-learn joblib plotly requests streamlit")
    print("  2. pkl 파일: energy_pipeline_v4.pkl → energy_app/ 폴더에 복사")
    print("  3. DB 세팅: python db_setup.py")
    print("  4. predictor 테스트: python predictor1.py")

print()
