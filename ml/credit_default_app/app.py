import streamlit as st
from predict import predict

# ── 페이지 설정 ──────────────────────────────────────────
st.set_page_config(page_title='신용카드 채무불이행 예측', layout='wide')
st.title('💳 신용카드 채무불이행 고객 예측')
st.caption('모델 : RFC + SMOTE + PCA(PC15) | ROC-AUC 0.7398')

# ── 사이드바 ─────────────────────────────────────────────
with st.sidebar:
    st.header('⚙️ 예측 설정')
    threshold = st.slider('판정 임계값 (Threshold)', 0.1, 0.9, 0.5, 0.05,
                          help='낮출수록 채무불이행 탐지율(Recall) 상승, 오탐(FP) 증가')
    st.divider()
    st.markdown('''
    **모델 정보**
    - 알고리즘 : Random Forest
    - 전처리   : StandardScaler → PCA(15)
    - 불균형   : SMOTE
    - 피처 수  : 23개 → 15 PC
    ''')

# ── 입력 폼 ──────────────────────────────────────────────
st.subheader('📋 고객 정보 입력')
tab1, tab2, tab3, tab4 = st.tabs(['기본 정보', '납부 상태', '청구 금액', '납부 금액'])

with tab1:
    col1, col2, col3 = st.columns(3)
    LIMIT_BAL = col1.number_input('신용한도 (LIMIT_BAL)', 10000, 1000000, 200000, step=10000)
    AGE       = col2.number_input('나이 (AGE)', 21, 79, 35)
    SEX       = col3.selectbox('성별 (SEX)', [1, 2], format_func=lambda x: '남(1)' if x == 1 else '여(2)')
    EDUCATION = col1.selectbox('학력 (EDUCATION)',
                               [1, 2, 3, 4],
                               format_func=lambda x: {1:'대학원', 2:'대학', 3:'고등학교', 4:'기타'}[x])
    MARRIAGE  = col2.selectbox('결혼 (MARRIAGE)',
                               [1, 2, 3],
                               format_func=lambda x: {1:'기혼', 2:'미혼', 3:'기타'}[x])

with tab2:
    st.caption('납부 상태 : -2=소비없음, -1=정상납부, 0=리볼빙, 1~8=연체 개월수')
    col1, col2, col3 = st.columns(3)
    PAY_0 = col1.selectbox('PAY_0 (최근월)',   range(-2, 9), index=2)
    PAY_2 = col2.selectbox('PAY_2 (2개월 전)', range(-2, 9), index=2)
    PAY_3 = col3.selectbox('PAY_3 (3개월 전)', range(-2, 9), index=2)
    PAY_4 = col1.selectbox('PAY_4 (4개월 전)', range(-2, 9), index=2)
    PAY_5 = col2.selectbox('PAY_5 (5개월 전)', range(-2, 9), index=2)
    PAY_6 = col3.selectbox('PAY_6 (6개월 전)', range(-2, 9), index=2)

with tab3:
    col1, col2, col3 = st.columns(3)
    BILL_AMT1 = col1.number_input('BILL_AMT1 (최근월)', 0, 2000000, 50000, step=1000)
    BILL_AMT2 = col2.number_input('BILL_AMT2',          0, 2000000, 50000, step=1000)
    BILL_AMT3 = col3.number_input('BILL_AMT3',          0, 2000000, 50000, step=1000)
    BILL_AMT4 = col1.number_input('BILL_AMT4',          0, 2000000, 50000, step=1000)
    BILL_AMT5 = col2.number_input('BILL_AMT5',          0, 2000000, 50000, step=1000)
    BILL_AMT6 = col3.number_input('BILL_AMT6 (6개월 전)', 0, 2000000, 50000, step=1000)

with tab4:
    col1, col2, col3 = st.columns(3)
    PAY_AMT1 = col1.number_input('PAY_AMT1 (최근월)', 0, 2000000, 2000, step=1000)
    PAY_AMT2 = col2.number_input('PAY_AMT2',          0, 2000000, 2000, step=1000)
    PAY_AMT3 = col3.number_input('PAY_AMT3',          0, 2000000, 2000, step=1000)
    PAY_AMT4 = col1.number_input('PAY_AMT4',          0, 2000000, 2000, step=1000)
    PAY_AMT5 = col2.number_input('PAY_AMT5',          0, 2000000, 2000, step=1000)
    PAY_AMT6 = col3.number_input('PAY_AMT6 (6개월 전)', 0, 2000000, 2000, step=1000)

# ── 예측 실행 ─────────────────────────────────────────────
st.divider()
if st.button('🔍 채무불이행 예측 실행', type='primary', use_container_width=True):

    input_dict = {
        'LIMIT_BAL': LIMIT_BAL, 'SEX': SEX, 'EDUCATION': EDUCATION,
        'MARRIAGE': MARRIAGE,   'AGE': AGE,
        'PAY_0': PAY_0, 'PAY_2': PAY_2, 'PAY_3': PAY_3,
        'PAY_4': PAY_4, 'PAY_5': PAY_5, 'PAY_6': PAY_6,
        'BILL_AMT1': BILL_AMT1, 'BILL_AMT2': BILL_AMT2, 'BILL_AMT3': BILL_AMT3,
        'BILL_AMT4': BILL_AMT4, 'BILL_AMT5': BILL_AMT5, 'BILL_AMT6': BILL_AMT6,
        'PAY_AMT1': PAY_AMT1,   'PAY_AMT2': PAY_AMT2,   'PAY_AMT3': PAY_AMT3,
        'PAY_AMT4': PAY_AMT4,   'PAY_AMT5': PAY_AMT5,   'PAY_AMT6': PAY_AMT6,
    }

    result = predict(input_dict, threshold=threshold)

    # ── 결과 출력 ────────────────────────────────────────
    st.subheader('📊 예측 결과')
    col1, col2, col3 = st.columns(3)

    col1.metric('채무불이행 확률', f"{result['probability'] * 100:.1f}%")
    col2.metric('판정 임계값',     f"{result['threshold']:.2f}")

    if result['prediction'] == 1:
        col3.error(f"⚠️ 판정 : {result['label']}")
        st.progress(result['probability'], text=f"위험도 {result['probability']*100:.1f}%")
    else:
        col3.success(f"✅ 판정 : {result['label']}")
        st.progress(result['probability'], text=f"위험도 {result['probability']*100:.1f}%")

    # ── 입력값 요약 ──────────────────────────────────────
    with st.expander('입력값 확인'):
        st.json(input_dict)
