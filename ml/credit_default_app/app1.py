import os
import streamlit as st
import joblib
import pandas as pd

FEATURE_COLS = [
    'LIMIT_BAL', 'SEX', 'EDUCATION', 'MARRIAGE', 'AGE',
    'PAY_0', 'PAY_2', 'PAY_3', 'PAY_4', 'PAY_5', 'PAY_6',
    'BILL_AMT1', 'BILL_AMT2', 'BILL_AMT3', 'BILL_AMT4', 'BILL_AMT5', 'BILL_AMT6',
    'PAY_AMT1', 'PAY_AMT2', 'PAY_AMT3', 'PAY_AMT4', 'PAY_AMT5', 'PAY_AMT6'
]

def prepare_input(user_input):
    df = pd.DataFrame([user_input], columns=FEATURE_COLS)
    df['EDUCATION'] = df['EDUCATION'].replace({0: 4, 5: 4, 6: 4})
    df['MARRIAGE']  = df['MARRIAGE'].replace({0: 3})
    return df[FEATURE_COLS]

def get_risk_level(prob):
    if prob < 0.2:   return {"level": "낮음",     "icon": "🟢"}
    elif prob < 0.4: return {"level": "주의",     "icon": "🟡"}
    elif prob < 0.6: return {"level": "위험",     "icon": "🔴"}
    else:            return {"level": "매우위험", "icon": "🚨"}

st.set_page_config(page_title="신용카드 채무불이행 예측", page_icon="💳", layout="wide")

@st.cache_resource
def load_model():
    try:
        base = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base, "model", "credit_pipeline.pkl")
        return joblib.load(path)
    except Exception as e:
        st.error(f"모델 로드 실패: {e}")
        return None

pipeline = load_model()

st.title("신용카드 채무불이행 예측 시스템")
st.divider()

if pipeline is None:
    st.warning("모델을 불러오지 못했습니다.")
    st.stop()

st.sidebar.header("고객 정보 입력")

LIMIT_BAL = st.sidebar.number_input("신용한도", min_value=10000, max_value=1000000, value=200000, step=10000)
SEX       = st.sidebar.selectbox("성별", options=[1, 2], format_func=lambda x: "남성" if x==1 else "여성")
EDUCATION = st.sidebar.selectbox("학력", options=[1,2,3,4],
                                  format_func=lambda x: {1:"대학원",2:"대학교",3:"고등학교",4:"기타"}[x])
MARRIAGE  = st.sidebar.selectbox("결혼여부", options=[1,2,3],
                                  format_func=lambda x: {1:"기혼",2:"미혼",3:"기타"}[x])
AGE       = st.sidebar.slider("나이", 20, 75, 35)

st.sidebar.subheader("납부상태 (PAY)")
st.sidebar.caption("-1=정상, 0=최소납부, 1~8=연체개월")
PAY_0 = st.sidebar.slider("9월", -1, 8, 0)
PAY_2 = st.sidebar.slider("8월", -1, 8, 0)
PAY_3 = st.sidebar.slider("7월", -1, 8, 0)
PAY_4 = st.sidebar.slider("6월", -1, 8, 0)
PAY_5 = st.sidebar.slider("5월", -1, 8, 0)
PAY_6 = st.sidebar.slider("4월", -1, 8, 0)

st.sidebar.subheader("청구금액 (BILL_AMT)")
BILL_AMT1 = st.sidebar.number_input("9월 청구", 0, 500000, 50000, 1000)
BILL_AMT2 = st.sidebar.number_input("8월 청구", 0, 500000, 50000, 1000)
BILL_AMT3 = st.sidebar.number_input("7월 청구", 0, 500000, 50000, 1000)
BILL_AMT4 = st.sidebar.number_input("6월 청구", 0, 500000, 50000, 1000)
BILL_AMT5 = st.sidebar.number_input("5월 청구", 0, 500000, 50000, 1000)
BILL_AMT6 = st.sidebar.number_input("4월 청구", 0, 500000, 50000, 1000)

st.sidebar.subheader("납부금액 (PAY_AMT)")
PAY_AMT1 = st.sidebar.number_input("9월 납부", 0, 500000, 2000, 1000)
PAY_AMT2 = st.sidebar.number_input("8월 납부", 0, 500000, 2000, 1000)
PAY_AMT3 = st.sidebar.number_input("7월 납부", 0, 500000, 2000, 1000)
PAY_AMT4 = st.sidebar.number_input("6월 납부", 0, 500000, 2000, 1000)
PAY_AMT5 = st.sidebar.number_input("5월 납부", 0, 500000, 2000, 1000)
PAY_AMT6 = st.sidebar.number_input("4월 납부", 0, 500000, 2000, 1000)

if st.sidebar.button("채무불이행 예측하기", use_container_width=True, type="primary"):
    user_input = {
        'LIMIT_BAL': LIMIT_BAL, 'SEX': SEX,
        'EDUCATION': EDUCATION, 'MARRIAGE': MARRIAGE, 'AGE': AGE,
        'PAY_0': PAY_0, 'PAY_2': PAY_2, 'PAY_3': PAY_3,
        'PAY_4': PAY_4, 'PAY_5': PAY_5, 'PAY_6': PAY_6,
        'BILL_AMT1': BILL_AMT1, 'BILL_AMT2': BILL_AMT2,
        'BILL_AMT3': BILL_AMT3, 'BILL_AMT4': BILL_AMT4,
        'BILL_AMT5': BILL_AMT5, 'BILL_AMT6': BILL_AMT6,
        'PAY_AMT1': PAY_AMT1, 'PAY_AMT2': PAY_AMT2,
        'PAY_AMT3': PAY_AMT3, 'PAY_AMT4': PAY_AMT4,
        'PAY_AMT5': PAY_AMT5, 'PAY_AMT6': PAY_AMT6,
    }
    try:
        X_input = prepare_input(user_input)
        prob = pipeline.predict_proba(X_input)[0][1]
        pred = pipeline.predict(X_input)[0]
        risk = get_risk_level(prob)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("예측 결과", "채무불이행" if pred==1 else "정상")
        with col2:
            st.metric("불이행 확률", f"{prob*100:.1f}%")
        with col3:
            st.metric("위험 등급", f"{risk['icon']} {risk['level']}")

        st.progress(float(prob))
        st.divider()
        st.dataframe(X_input, use_container_width=True)

    except Exception as e:
        st.error(f"예측 오류: {e}")

else:
    st.info("왼쪽 사이드바에서 정보 입력 후 예측하기 버튼을 눌러주세요.")
