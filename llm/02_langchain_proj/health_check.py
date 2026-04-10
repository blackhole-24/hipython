import sys, os

print("=" * 50)
print("1. Python / 가상환경 확인")
print(f"   Python: {sys.ve  rsion}")
print(f"   실행경로: {sys.executable}")
print()

print("=" * 50)
print("2. 라이브러리 설치 확인")
libs = {
    'meilisearch': 'meilisearch',
    'yfinance': 'yfinance',
    'pandas': 'pandas',
    'tabulate': 'tabulate',
    'langchain_openai': 'langchain-openai',
    'langchain_core': 'langchain-core',
    'streamlit': 'streamlit',
    'dotenv': 'python-dotenv',
}
import importlib.util
all_ok = True
for mod, name in libs.items():
    ok = importlib.util.find_spec(mod) is not None
    status = "OK  " if ok else "MISSING"
    if not ok:
        all_ok = False
    print(f"   {status}  {name}")
print()

print("=" * 50)
print("3. .env 파일 및 API 키 확인")
from dotenv import load_dotenv
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(env_path)
keys = ['OPENAI_API_KEY', 'MEILI_SEARCH_KEY']
for k in keys:
    v = os.environ.get(k, '')
    if v:
        print(f"   OK    {k}: {v[:10]}...")
    else:
        print(f"   MISSING  {k}")
print()

print("=" * 50)
print("4. yfinance 데이터 다운로드 테스트 (AAPL)")
try:
    import yfinance as yf
    s = yf.Ticker('AAPL')
    h = s.history(period='5d')
    print(f"   OK    행수: {len(h)}")
    print(f"   최근 종가: ${h['Close'].iloc[-1]:.2f}")
except Exception as e:
    print(f"   ERROR: {e}")
print()

print("=" * 50)
print("5. MeiliSearch 서버 연결 확인 (localhost:7700)")
try:
    import meilisearch
    key = os.environ.get('MEILI_SEARCH_KEY', '')
    client = meilisearch.Client('http://127.0.0.1:7700', key)
    stats = client.get_all_stats()
    print(f"   OK    서버 연결 성공")
    idx = stats.get('indexes', {})
    if 'nasdaq' in idx:
        print(f"   OK    nasdaq 인덱스 문서 수: {idx['nasdaq']['numberOfDocuments']}")
    else:
        print(f"   WARNING  nasdaq 인덱스 없음 → 01_search_engine_setting.ipynb 실행 필요")
except Exception as e:
    print(f"   ERROR: MeiliSearch 서버 꺼짐 또는 키 오류")
    print(f"         {str(e)[:80]}")
print()

print("=" * 50)
print("6. stock_info.py Stock 클래스 테스트")
try:
    sys.path.insert(0, os.path.dirname(__file__))
    from stock_info.stock_info import Stock
    s = Stock('AAPL')
    info = s.get_basic_info()
    print(f"   OK    get_basic_info() 정상 ({len(info)}자)")
except Exception as e:
    print(f"   ERROR: {e}")
print()

print("=" * 50)
print("7. investment_report.py import 확인")
try:
    from report_service.investment_report import investment_report
    print("   OK    import 성공 (실제 API 호출은 생략)")
except Exception as e:
    print(f"   ERROR: {e}")
print()

print("=" * 50)
print("전체 결과:", "모두 정상" if all_ok else "일부 문제 있음 — 위 MISSING/ERROR 확인")
