import streamlit as st

st.set_page_config(
    page_title="제조 전력 피크 예측 · 자원 최적화 PoC",
    page_icon="EP",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    [data-testid="stSidebarNav"] ul {margin-top: 0;}
    .main-header {
        background: linear-gradient(90deg, #1A5276, #2E86C1);
        padding: 14px 20px;
        border-radius: 8px;
        margin-bottom: 16px;
    }
</style>
""", unsafe_allow_html=True)

st.title("EP   제조 전력 피크 예측 · 자원 최적화 PoC")
st.markdown("""
| 항목 | 내용 |
|---|---|
| 데이터 | KAMP 자원 최적화 AI 데이터셋 (okm_augumented_2021.csv) |
| 모델 | XGBoost | Set_C 23개 피처 | R²=0.9999 |
| 학습 기간 | 2021년 1월~12월 (1년치 증강) |
| 팀 | 올라운더팀 | 2026.03 |
""")

st.divider()

st.subheader("서비스 메뉴 안내")

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.info("""**대시보드**

피크 위험 경보
실시간 KPI
24h 시뮬레이션
비용 절감 계산기""")
with col2:
    st.info("""**예측·분석**

전력 추이 그래프
피처 영향력 Top8
모델 성능 비교
과거 데이터 검색""")
with col3:
    st.success("""**추천(최적화)**

목표 생산량 입력
최적 운영안 추천
24h 타임라인
비용 비교""")
with col4:
    st.warning("""**DR 시뮬레이션**

DR 발령 조건 설정
감축량 계산
정산금 예측
누적 요금 비교""")
with col5:
    st.error("""**ESG 리포트**

GRI 302 기준
월별 탄소 배출
절감 시나리오
CSV 다운로드""")

st.divider()
st.caption("올라운더팀 | KAMP 자원 최적화 AI 프로젝트 2 | 2026")
