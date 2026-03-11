import sys
import os

# preprocess.py 위치를 Python 경로에 추가 (오류 수정)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import joblib
from preprocess import prepare_input, get_risk_level

# ── 페이지 기본 설정 ──────────────────────────────────────
st.set_page_config(
    page_title="신용카드 채무불이행 예측",
    page_icon="💳",
    layout="wide"
)

# ── 모델 로드 (캐시: 최초 1회만 로드) ────────────────────
@st.cache_resource
def load_model():
    base = os.path.dirname(os.path.abspath(__file__))
    pipeline = joblib.load(os.path.join(base, "model", "credit_pipeline.pkl"))
    return pipeline

pipeline = load_model()

# ── 타이틀 ────────────────────────────────────────────────
st.title("💳 신용카드 채무불이행 예측 시스템")
st.markdown("고객 정보를 입력하면 **채무불이행 가능성**을 예측합니다.")
st.divider()

# ── 사이드바 입력 ─────────────────────────────────────────
st.sidebar.header("📋 고객 정보 입력")

LIMIT_BAL = st.sidebar.number_input("신용한도 (LIMIT_BAL)", min_value=10000, max_value=1000000, value=200000, step=10000)
SEX       = st.sidebar.selectbox("성별 (SEX)", options=[1, 2], format_func=lambda x: "남성" if x == 1 else "여성")
EDUCATION = st.sidebar.selectbox("학력 (EDUCATION)", options=[1, 2, 3, 4],
                                  format_func=lambda x: {1:"대학원", 2:"대학교", 3:"고등학교", 4:"기타"}[x])
MARRIAGE  = st.sidebar.selectbox("결혼여부 (MARRIAGE)", options=[1, 2, 3],
                                  format_func=lambda x: {1:"기혼", 2:"미혼", 3:"기타"}[x])
AGE       = st.sidebar.slider("나이 (AGE)", min_value=20, max_value=75, value=35)

st.sidebar.subheader("💰 납부상태 (PAY) — 최근 6개월")
st.sidebar.caption("-1=정상납부, 0=최소납부, 1~8=연체개월수")
PAY_0 = st.sidebar.slider("9월 납부상태 (PAY_0)", -1, 8, 0)
PAY_2 = st.sidebar.slider("8월 납부상태 (PAY_2)", -1, 8, 0)
PAY_3 = st.sidebar.slider("7월 납부상태 (PAY_3)", -1, 8, 0)
PAY_4 = st.sidebar.slider("6월 납부상태 (PAY_4)", -1, 8, 0)
PAY_5 = st.sidebar.slider("5월 납부상태 (PAY_5)", -1, 8, 0)
PAY_6 = st.sidebar.slider("4월 납부상태 (PAY_6)", -1, 8, 0)

st.sidebar.subheader("📄 청구금액 (BILL_AMT) — 최근 6개월")
BILL_AMT1 = st.sidebar.number_input("9월 청구금액", 0, 500000, 50000, 1000)
BILL_AMT2 = st.sidebar.number_input("8월 청구금액", 0, 500000, 50000, 1000)
BILL_AMT3 = st.sidebar.number_input("7월 청구금액", 0, 500000, 50000, 1000)
BILL_AMT4 = st.sidebar.number_input("6월 청구금액", 0, 500000, 50000, 1000)
BILL_AMT5 = st.sidebar.number_input("5월 청구금액", 0, 500000, 50000, 1000)
BILL_AMT6 = st.sidebar.number_input("4월 청구금액", 0, 500000, 50000, 1000)

st.sidebar.subheader("💵 납부금액 (PAY_AMT) — 최근 6개월")
PAY_AMT1 = st.sidebar.number_input("9월 납부금액", 0, 500000, 2000, 1000)
PAY_AMT2 = st.sidebar.number_input("8월 납부금액", 0, 500000, 2000, 1000)
PAY_AMT3 = st.sidebar.number_input("7월 납부금액", 0, 500000, 2000, 1000)
PAY_AMT4 = st.sidebar.number_input("6월 납부금액", 0, 500000, 2000, 1000)
PAY_AMT5 = st.sidebar.number_input("5월 납부금액", 0, 500000, 2000, 1000)
PAY_AMT6 = st.sidebar.number_input("4월 납부금액", 0, 500000, 2000, 1000)

# ── 예측 버튼 ─────────────────────────────────────────────
if st.sidebar.button("🔍 채무불이행 예측하기", use_container_width=True, type="primary"):

    user_input = {
        'LIMIT_BAL': LIMIT_BAL, 'SEX': SEX, 'EDUCATION': EDUCATION,
        'MARRIAGE': MARRIAGE,   'AGE': AGE,
        'PAY_0': PAY_0, 'PAY_2': PAY_2, 'PAY_3': PAY_3,
        'PAY_4': PAY_4, 'PAY_5': PAY_5, 'PAY_6': PAY_6,
        'BILL_AMT1': BILL_AMT1, 'BILL_AMT2': BILL_AMT2, 'BILL_AMT3': BILL_AMT3,
        'BILL_AMT4': BILL_AMT4, 'BILL_AMT5': BILL_AMT5, 'BILL_AMT6': BILL_AMT6,
        'PAY_AMT1': PAY_AMT1,   'PAY_AMT2': PAY_AMT2,   'PAY_AMT3': PAY_AMT3,
        'PAY_AMT4': PAY_AMT4,   'PAY_AMT5': PAY_AMT5,   'PAY_AMT6': PAY_AMT6,
    }

    X_input = prepare_input(user_input)
    prob    = pipeline.predict_proba(X_input)[0][1]
    pred    = pipeline.predict(X_input)[0]
    risk    = get_risk_level(prob)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="예측 결과", value="⚠️ 채무불이행" if pred == 1 else "✅ 정상")
    with col2:
        st.metric(label="불이행 확률", value=f"{prob*100:.1f}%")
    with col3:
        st.metric(label="위험 등급", value=f"{risk['icon']} {risk['level']}")

    st.markdown(f"### 채무불이행 확률: **{prob*100:.1f}%**")
    st.progress(float(prob))

    st.divider()
    st.subheader("📊 입력 정보 요약")
    st.dataframe(X_input, use_container_width=True)

else:
    st.info("👈 왼쪽 사이드바에서 고객 정보를 입력한 후 **예측하기** 버튼을 눌러주세요.")
