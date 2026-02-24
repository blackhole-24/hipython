import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

# 페이지 설정
st.set_page_config(
    page_title="🍓 Strawberry Dashboard 🍓",
    page_icon="🍓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 강력한 커스텀 CSS - 스트로베리 핑크 테마
st.markdown("""
    <style>
    /* 전체 배경을 핑크로 */
    .main {
        background: linear-gradient(135deg, #FFB6C1 0%, #FF69B4 50%, #FFB6C1 100%);
    }
    
    .block-container {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 30px;
        padding: 2rem;
        box-shadow: 0 10px 30px rgba(255, 20, 147, 0.3);
        border: 3px solid #FF1493;
    }
    
    /* 사이드바를 진한 핑크로 */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #FF1493 0%, #FF69B4 50%, #FFB6C1 100%);
        border-right: 5px solid #FF1493;
    }
    
    [data-testid="stSidebar"]::before {
        content: "🍓";
        font-size: 2.5rem;
        display: block;
        text-align: center;
        padding: 15px 0;
        animation: bounce 2s infinite;
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    /* 사이드바 모든 텍스트를 흰색으로 */
    [data-testid="stSidebar"] * {
        color: white !important;
        font-weight: 600 !important;
    }
    
    [data-testid="stSidebar"] h1 {
        font-size: 1.5rem !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        line-height: 1.2 !important;
    }
    
    /* 사이드바 라디오 버튼 스타일 개선 */
    [data-testid="stSidebar"] .row-widget.stRadio > div {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 10px;
        border-radius: 15px;
    }
    
    [data-testid="stSidebar"] .row-widget.stRadio > div > label {
        background-color: rgba(255, 255, 255, 0.25) !important;
        padding: 18px 25px !important;
        border-radius: 25px !important;
        margin: 8px 0 !important;
        transition: all 0.3s ease !important;
        font-size: 1.15rem !important;
        display: block !important;
        border: 2px solid rgba(255, 255, 255, 0.5) !important;
        font-weight: 700 !important;
        cursor: pointer !important;
    }
    
    [data-testid="stSidebar"] .row-widget.stRadio > div > label:hover {
        background-color: rgba(255, 255, 255, 0.45) !important;
        transform: translateX(8px) scale(1.02) !important;
        box-shadow: 0 5px 15px rgba(255, 255, 255, 0.3) !important;
        border-color: white !important;
    }
    
    /* 선택된 라디오 버튼 */
    [data-testid="stSidebar"] .row-widget.stRadio > div > label[data-baseweb="radio"] > div:first-child {
        background-color: white !important;
    }
    
    [data-testid="stSidebar"] input[type="radio"]:checked + div {
        background-color: rgba(255, 255, 255, 0.5) !important;
    }
    
    /* 메트릭 카드를 핑크로 */
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, #FFE0E9 0%, #FFB6C1 100%) !important;
        padding: 30px !important;
        border-radius: 25px !important;
        box-shadow: 0 10px 25px rgba(255, 20, 147, 0.4) !important;
        border: 4px solid #FF69B4 !important;
        transition: transform 0.3s ease !important;
        position: relative !important;
    }
    
    div[data-testid="metric-container"]::before {
        content: "🍓";
        position: absolute;
        top: 10px;
        right: 10px;
        font-size: 2rem;
        animation: rotate 3s infinite;
    }
    
    @keyframes rotate {
        0%, 100% { transform: rotate(0deg); }
        50% { transform: rotate(15deg); }
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-10px) scale(1.02) !important;
        box-shadow: 0 15px 35px rgba(255, 20, 147, 0.6) !important;
    }
    
    [data-testid="stMetricValue"] {
        color: #FF1493 !important;
        font-size: 3rem !important;
        font-weight: 900 !important;
        text-shadow: 2px 2px 4px rgba(255, 105, 180, 0.3);
    }
    
    [data-testid="stMetricLabel"] {
        color: #FF1493 !important;
        font-weight: 700 !important;
        font-size: 1.3rem !important;
    }
    
    [data-testid="stMetricDelta"] {
        color: #FF69B4 !important;
        font-weight: 700 !important;
    }
    
    /* 제목을 핑크로 */
    h1, h2, h3, h4 {
        color: #FF1493 !important;
        text-shadow: 3px 3px 6px rgba(255, 105, 180, 0.3) !important;
        font-weight: 900 !important;
    }
    
    h1::before, h2::before {
        content: "🍓 ";
    }
    
    h1::after, h2::after {
        content: " 🍓";
    }
    
    /* 탭을 핑크로 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 15px;
        background: linear-gradient(135deg, #FFB6C1 0%, #FF69B4 100%);
        padding: 15px;
        border-radius: 25px;
        box-shadow: 0 5px 15px rgba(255, 20, 147, 0.3);
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: white;
        color: #FF1493;
        border-radius: 20px;
        padding: 15px 30px;
        font-weight: 700;
        border: 3px solid #FF69B4;
        transition: all 0.3s ease;
        font-size: 1.1rem;
    }
    
    .stTabs [data-baseweb="tab"]::before {
        content: "🍓 ";
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: linear-gradient(135deg, #FF69B4 0%, #FF1493 100%);
        color: white;
        transform: scale(1.1);
        box-shadow: 0 5px 15px rgba(255, 20, 147, 0.5);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #FF1493 0%, #FF69B4 100%) !important;
        color: white !important;
        border: 3px solid white !important;
        transform: scale(1.05);
    }
    
    /* 버튼을 핑크로 */
    .stButton > button {
        background: linear-gradient(135deg, #FF1493 0%, #FF69B4 100%) !important;
        color: white !important;
        border-radius: 30px !important;
        padding: 15px 40px !important;
        font-weight: 900 !important;
        border: 3px solid white !important;
        box-shadow: 0 8px 20px rgba(255, 20, 147, 0.5) !important;
        transition: all 0.3s ease !important;
        font-size: 1.2rem !important;
    }
    
    .stButton > button::before {
        content: "🍓 ";
    }
    
    .stButton > button:hover {
        transform: translateY(-5px) scale(1.05) !important;
        box-shadow: 0 12px 30px rgba(255, 20, 147, 0.7) !important;
        background: linear-gradient(135deg, #FF69B4 0%, #FF1493 100%) !important;
    }
    
    /* 입력 필드를 핑크로 */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stNumberInput > div > div > input {
        border: 3px solid #FF69B4 !important;
        border-radius: 20px !important;
        background: linear-gradient(135deg, #FFF0F5 0%, #FFE0E9 100%) !important;
        color: #FF1493 !important;
        font-weight: 600 !important;
        padding: 12px !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #FF1493 !important;
        box-shadow: 0 0 20px rgba(255, 20, 147, 0.5) !important;
    }
    
    /* 체크박스를 핑크로 */
    .stCheckbox > label {
        color: #FF1493 !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
    }
    
    .stCheckbox > label::before {
        content: "🍓 ";
    }
    
    /* 데이터프레임을 핑크로 */
    .dataframe {
        border: 4px solid #FF69B4 !important;
        border-radius: 20px !important;
        background: linear-gradient(135deg, #FFF0F5 0%, #FFE0E9 100%) !important;
    }
    
    /* 알림 메시지를 핑크로 */
    .stSuccess {
        background: linear-gradient(135deg, #FFE0E9 0%, #FFB6C1 100%) !important;
        color: #FF1493 !important;
        border-left: 8px solid #FF1493 !important;
        border-radius: 15px !important;
        font-weight: 700 !important;
    }
    
    .stSuccess::before {
        content: "🍓 ";
    }
    
    .stInfo {
        background: linear-gradient(135deg, #E0F0FF 0%, #B6D4FF 100%) !important;
        color: #FF1493 !important;
        border-left: 8px solid #FF69B4 !important;
        border-radius: 15px !important;
        font-weight: 700 !important;
    }
    
    .stWarning {
        background: linear-gradient(135deg, #FFF0E0 0%, #FFD4B6 100%) !important;
        color: #FF1493 !important;
        border-left: 8px solid #FF69B4 !important;
        border-radius: 15px !important;
        font-weight: 700 !important;
    }
    
    /* 다운로드 버튼을 핑크로 */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #FFB6C1 0%, #FF69B4 100%) !important;
        color: white !important;
        border-radius: 25px !important;
        font-weight: 800 !important;
        border: 3px solid #FF1493 !important;
        padding: 12px 30px !important;
    }
    
    .stDownloadButton > button::before {
        content: "🍓 ";
    }
    
    /* 슬라이더를 핑크로 */
    .stSlider > div > div > div > div {
        background-color: #FF69B4 !important;
    }
    
    .stSlider > div > div > div {
        background-color: #FFB6C1 !important;
    }
    
    /* 구분선을 핑크로 */
    hr {
        border: none !important;
        height: 4px !important;
        background: linear-gradient(90deg, #FF1493, #FF69B4, #FFB6C1, #FF69B4, #FF1493) !important;
        margin: 40px 0 !important;
        border-radius: 5px !important;
    }
    
    /* 이미지 테두리를 핑크로 */
    img {
        border-radius: 25px !important;
        border: 5px solid #FF69B4 !important;
        box-shadow: 0 10px 30px rgba(255, 20, 147, 0.4) !important;
    }
    
    /* 스크롤바를 핑크로 */
    ::-webkit-scrollbar {
        width: 15px;
    }
    
    ::-webkit-scrollbar-track {
        background: #FFE0E9;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #FF1493, #FF69B4, #FFB6C1);
        border-radius: 10px;
        border: 2px solid white;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #FF69B4, #FF1493);
    }
    
    /* 차트 배경을 핑크로 */
    .js-plotly-plot {
        border-radius: 20px !important;
        background: linear-gradient(135deg, #FFF0F5 0%, #FFE0E9 100%) !important;
        padding: 20px !important;
        box-shadow: 0 8px 20px rgba(255, 20, 147, 0.3) !important;
        border: 3px solid #FF69B4 !important;
    }
    
    /* 날짜 입력 */
    .stDateInput > div > div > input {
        border: 3px solid #FF69B4 !important;
        border-radius: 20px !important;
        background: linear-gradient(135deg, #FFF0F5 0%, #FFE0E9 100%) !important;
        color: #FF1493 !important;
        font-weight: 600 !important;
    }
    
    /* 셀렉트 슬라이더 */
    .stSelectSlider > div > div {
        background: linear-gradient(135deg, #FFB6C1 0%, #FF69B4 100%) !important;
        border-radius: 20px !important;
    }
    
    /* 텍스트 색상 */
    p, span, div {
        color: #FF1493;
        font-weight: 500;
    }
    
    </style>
""", unsafe_allow_html=True)

# 샘플 데이터 생성
@st.cache_data
def generate_sample_data():
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    data = pd.DataFrame({
        '날짜': dates,
        '방문자수': np.random.randint(100, 500, 30),
        '활성사용자': np.random.randint(50, 300, 30),
        '페이지뷰': np.random.randint(200, 1000, 30)
    })
    return data

# 사이드바 구성
st.sidebar.markdown("<h1 style='text-align: center;'>컨트롤 센터</h1>", unsafe_allow_html=True)
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "메뉴 선택",
    ["메인페이지", "분석보고서", "설정"],
    label_visibility="collapsed"
)

st.sidebar.markdown("<br>", unsafe_allow_html=True)

st.sidebar.metric('접속자수:', 
    '백만명', "+백만명")

if st.sidebar.button('놀러봐!!!'):
    st.balloons()

st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    <div style='background-color: rgba(255, 255, 255, 0.3); 
                padding: 20px; 
                border-radius: 20px; 
                text-align: center;
                border: 3px solid white;'>
        <p style='margin: 0; font-size: 2rem;'>🍓</p>
        <p style='margin: 0; font-weight: 700; font-size: 1.2rem;'>💡 Tip</p>
        <p style='margin: 10px 0 0 0; font-size: 1rem;'>각 메뉴를 클릭하여<br>다양한 기능을 확인하세요!</p>
    </div>
    """,
    unsafe_allow_html=True
)

# 데이터 로드
df = generate_sample_data()

# 메인 페이지
if menu == "메인페이지":
    # 페이지 제목
    st.markdown("<h1 style='text-align: center; font-size: 3rem;'>Sweet Strawberry Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #FF1493; font-size: 1.8rem;'>실시간 통계를 한눈에 확인하세요 ✨</h3>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # KPI 대시보드 (2개 컬럼)
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            label="👥 오늘 방문자수",
            value=f"{df['방문자수'].iloc[-1]:,}명",
            delta=f"{df['방문자수'].iloc[-1] - df['방문자수'].iloc[-2]:,}명",
            delta_color="normal"
        )
        
        # 미니 차트
        st.line_chart(df.set_index('날짜')['방문자수'].tail(7), height=150, color='#FF1493')
    
    with col2:
        st.metric(
            label="⚡ 활성 사용자수",
            value=f"{df['활성사용자'].iloc[-1]:,}명",
            delta=f"{df['활성사용자'].iloc[-1] - df['활성사용자'].iloc[-2]:,}명",
            delta_color="normal"
        )
        
        # 미니 차트
        st.line_chart(df.set_index('날짜')['활성사용자'].tail(7), height=150, color='#FF69B4')
    
    st.markdown("---")
    
    # 추가 KPI
    col3, col4, col5 = st.columns(3)
    
    with col3:
        st.metric("📄 총 페이지뷰", f"{df['페이지뷰'].sum():,}", "↗")
    
    with col4:
        avg_visitors = df['방문자수'].mean()
        st.metric("📊 평균 방문자", f"{avg_visitors:.0f}명", "→")
    
    with col5:
        conversion_rate = (df['활성사용자'].iloc[-1] / df['방문자수'].iloc[-1] * 100)
        st.metric("💯 전환율", f"{conversion_rate:.1f}%", "↗")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 추가 정보 카드
    st.markdown(
        """
        <div style='background: linear-gradient(135deg, #FFE0E9 0%, #FFB6C1 100%);
                    padding: 40px;
                    border-radius: 30px;
                    border: 5px solid #FF1493;
                    text-align: center;
                    box-shadow: 0 10px 30px rgba(255, 20, 147, 0.4);'>
            <h2 style='color: #FF1493; margin-top: 0; font-size: 2.5rem;'>🍓 오늘의 성과 🍓</h2>
            <p style='color: #FF1493; font-size: 1.5rem; font-weight: 700;'>
                여러분의 노력으로 만들어진 멋진 결과입니다! 💪✨
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

# 분석 보고서 페이지
elif menu == "분석보고서":
    st.markdown("<h1 style='text-align: center; font-size: 3rem;'>분석 보고서</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #FF1493; font-size: 1.8rem;'>상세 데이터 분석 및 인사이트 ✨</h3>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 탭 구성
    tab1, tab2, tab3 = st.tabs(["차트", "데이터", "설정"])
    
    with tab1:
        st.markdown("<h2 style='color: #FF1493; font-size: 2rem;'>💕 사용자 방문 현황</h2>", unsafe_allow_html=True)
        
        # Plotly 인터랙티브 차트 - 핑크 컬러 스킴
        fig = px.line(df, x='날짜', y=['방문자수', '활성사용자', '페이지뷰'],
                     title='🍓 30일 트렌드 분석',
                     labels={'value': '수량', 'variable': '지표'},
                     color_discrete_sequence=['#FF1493', '#FF69B4', '#FFB6C1'])
        
        fig.update_layout(
            hovermode='x unified',
            height=500,
            plot_bgcolor='#FFF0F5',
            paper_bgcolor='#FFE0E9',
            font=dict(color='#FF1493', size=14, family='Arial'),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor='#FFB6C1',
                bordercolor='#FF1493',
                borderwidth=3,
                font=dict(size=12, color='white')
            ),
            title=dict(
                font=dict(size=24, color='#FF1493', family='Arial'),
                x=0.5,
                xanchor='center'
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # 추가 차트
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<h3 style='color: #FF1493;'>📊 방문자 분포</h3>", unsafe_allow_html=True)
            fig_bar = px.bar(df.tail(10), x='날짜', y='방문자수',
                            title='최근 10일 방문자',
                            color='방문자수',
                            color_continuous_scale=['#FFB6C1', '#FF69B4', '#FF1493'])
            fig_bar.update_layout(
                plot_bgcolor='#FFF0F5',
                paper_bgcolor='#FFE0E9',
                font=dict(color='#FF1493')
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        
        with col2:
            st.markdown("<h3 style='color: #FF1493;'>🥧 사용자 비율</h3>", unsafe_allow_html=True)
            pie_data = pd.DataFrame({
                '구분': ['신규 방문자', '재방문자', '활성 사용자'],
                '수': [150, 200, df['활성사용자'].iloc[-1]]
            })
            fig_pie = px.pie(pie_data, values='수', names='구분',
                            title='사용자 구성',
                            color_discrete_sequence=['#FF1493', '#FF69B4', '#FFB6C1'])
            fig_pie.update_layout(
                paper_bgcolor='#FFE0E9',
                font=dict(color='#FF1493', size=13)
            )
            st.plotly_chart(fig_pie, use_container_width=True)
    
    with tab2:
        st.markdown("<h2 style='color: #FF1493; font-size: 2rem;'>📋 데이터 테이블</h2>", unsafe_allow_html=True)
        
        # 필터 옵션
        col1, col2 = st.columns(2)
        with col1:
            date_range = st.date_input(
                "📅 날짜 범위 선택",
                value=(df['날짜'].min(), df['날짜'].max()),
                min_value=df['날짜'].min(),
                max_value=df['날짜'].max()
            )
        
        with col2:
            min_visitors = st.slider("👥 최소 방문자수", 0, 500, 0)
        
        # 필터링된 데이터
        filtered_df = df[
            (df['날짜'] >= pd.Timestamp(date_range[0])) &
            (df['날짜'] <= pd.Timestamp(date_range[1])) &
            (df['방문자수'] >= min_visitors)
        ]
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # 데이터프레임 표시
        st.dataframe(
            filtered_df.style.background_gradient(cmap='RdPu', subset=['방문자수'])
                            .background_gradient(cmap='PuRd', subset=['활성사용자'])
                            .format({'날짜': lambda x: x.strftime('%Y-%m-%d')}),
            use_container_width=True,
            height=400
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # 통계 요약
        st.markdown("<h3 style='color: #FF1493;'>📊 통계 요약</h3>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("총 레코드", len(filtered_df))
        with col2:
            st.metric("평균 방문자", f"{filtered_df['방문자수'].mean():.0f}")
        with col3:
            st.metric("최대 방문자", f"{filtered_df['방문자수'].max()}")
        with col4:
            st.metric("최소 방문자", f"{filtered_df['방문자수'].min()}")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # 다운로드 버튼
        csv = filtered_df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="CSV 다운로드",
            data=csv,
            file_name=f'strawberry_data_{datetime.now().strftime("%Y%m%d")}.csv',
            mime='text/csv',
        )
    
    with tab3:
        st.markdown("<h2 style='color: #FF1493; font-size: 2rem;'>⚙️ 연결 설정</h2>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<h4 style='color: #FF1493;'>💾 데이터 소스</h4>", unsafe_allow_html=True)
            auto_refresh = st.checkbox("자동 새로고침", value=True)
            real_time = st.checkbox("실시간 동기화", value=False)
            cache_data = st.checkbox("데이터 캐싱", value=True)
            
            if auto_refresh:
                refresh_interval = st.select_slider(
                    "새로고침 간격 (초)",
                    options=[5, 10, 30, 60, 300],
                    value=30
                )
        
        with col2:
            st.markdown("<h4 style='color: #FF1493;'>🔔 알림 설정</h4>", unsafe_allow_html=True)
            email_alert = st.checkbox("이메일 알림", value=False)
            threshold_alert = st.checkbox("임계값 알림", value=True)
            daily_report = st.checkbox("일일 리포트", value=True)
            
            if threshold_alert:
                threshold = st.number_input("임계값 설정", min_value=0, max_value=1000, value=100)
        
        st.markdown("---")
        
        # 설정 저장
        if st.button("설정 저장", type="primary"):
            st.success("✅ 설정이 저장되었습니다!")
            st.balloons()

# 설정 페이지
elif menu == "설정":
    st.markdown("<h1 style='text-align: center; font-size: 3rem;'>시스템 설정</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #FF1493; font-size: 1.8rem;'>대시보드 환경 구성 ✨</h3>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 탭으로 설정 분류
    tab1, tab2, tab3 = st.tabs(["테마", "사용자", "고급"])
    
    with tab1:
        st.markdown("<h2 style='color: #FF1493;'>🎨 테마 설정</h2>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            theme = st.selectbox(
                "🌈 컬러 테마",
                ["스트로베리 핑크 (현재)", "로즈 골드", "피치 핑크", "라벤더 핑크"]
            )
            
            accent_color = st.color_picker("💖 강조 색상", "#FF1493")
        
        with col2:
            font_size = st.select_slider(
                "📝 글자 크기",
                options=["작게", "보통", "크게"],
                value="보통"
            )
            
            chart_style = st.selectbox(
                "📊 차트 스타일",
                ["귀여운 핑크", "로맨틱 핑크", "모던 핑크"]
            )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # 테마 미리보기
        st.markdown(
            """
            <div style='background: linear-gradient(135deg, #FFE0E9 0%, #FFB6C1 100%);
                        padding: 40px;
                        border-radius: 30px;
                        border: 5px solid #FF1493;
                        text-align: center;
                        box-shadow: 0 10px 30px rgba(255, 20, 147, 0.4);'>
                <p style='font-size: 3rem; margin: 0;'>🍓</p>
                <h3 style='color: #FF1493; margin: 20px 0; font-size: 2rem;'>테마 미리보기</h3>
                <p style='color: #FF1493; font-size: 1.3rem; font-weight: 700;'>
                    스트로베리 핑크 테마가 적용되었습니다! 💕
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with tab2:
        st.markdown("<h2 style='color: #FF1493;'>👤 사용자 프로필</h2>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            username = st.text_input("사용자 이름", value="Admin")
            email = st.text_input("이메일", value="admin@strawberry.com")
        
        with col2:
            role = st.selectbox("역할", ["관리자", "분석가", "뷰어"])
            language = st.selectbox("언어", ["한국어", "English", "日本語"])
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # 프로필 카드
        st.markdown(
            f"""
            <div style='background: linear-gradient(135deg, #FFE0E9 0%, #FFB6C1 100%);
                        padding: 35px;
                        border-radius: 30px;
                        border: 5px solid #FF1493;
                        box-shadow: 0 10px 30px rgba(255, 20, 147, 0.4);'>
                <p style='text-align: center; font-size: 3rem; margin: 0;'>🍓</p>
                <h3 style='color: #FF1493; margin: 20px 0; text-align: center; font-size: 2rem;'>내 프로필</h3>
                <p style='color: #FF1493; font-size: 1.2rem; font-weight: 600;'><strong>이름:</strong> {username}</p>
                <p style='color: #FF1493; font-size: 1.2rem; font-weight: 600;'><strong>이메일:</strong> {email}</p>
                <p style='color: #FF1493; font-size: 1.2rem; font-weight: 600;'><strong>역할:</strong> {role}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with tab3:
        st.markdown("<h2 style='color: #FF1493;'>🔧 고급 설정</h2>", unsafe_allow_html=True)
        
        enable_debug = st.checkbox("디버그 모드", value=False)
        enable_analytics = st.checkbox("사용량 분석", value=True)
        enable_api = st.checkbox("API 접근", value=False)
        
        if enable_api:
            api_key = st.text_input("API 키", type="password", placeholder="API 키를 입력하세요")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # 보안 설정
        st.markdown("<h3 style='color: #FF1493;'>🔒 보안 설정</h3>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            two_factor = st.checkbox("2단계 인증", value=False)
            auto_logout = st.checkbox("자동 로그아웃", value=True)
        
        with col2:
            password_change = st.checkbox("비밀번호 변경 알림", value=True)
            login_alert = st.checkbox("로그인 알림", value=False)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("저장", type="primary", use_container_width=True):
            st.success("✅ 설정이 저장되었습니다!")
            st.balloons()
    
    with col2:
        if st.button("초기화", use_container_width=True):
            st.warning("⚠️ 설정이 초기화되었습니다.")
    
    with col3:
        if st.button("취소", use_container_width=True):
            st.info("ℹ️ 변경사항이 취소되었습니다.")

# 푸터
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; 
                background: linear-gradient(135deg, #FFE0E9 0%, #FFB6C1 100%);
                padding: 40px;
                border-radius: 30px;
                border: 5px solid #FF1493;
                box-shadow: 0 10px 30px rgba(255, 20, 147, 0.4);'>
        <p style='font-size: 3rem; margin: 0;'>🍓</p>
        <h3 style='color: #FF1493; margin: 20px 0; font-size: 2.5rem;'>Strawberry Dashboard v1.0</h3>
        <p style='color: #FF1493; margin: 15px 0; font-size: 1.3rem; font-weight: 700;'>Made with ❤️ using Streamlit</p>
        <p style='color: #FF1493; font-size: 1.1rem; margin: 10px 0;'>© 2026 All Rights Reserved</p>
    </div>
    """,
    unsafe_allow_html=True
)








# 바이브를 위한 프롬프트
# 파이썬 스트림릿 대시보드를 만들어주세요.
# 아래의 구조를 실행가능한 파이썬 코드로 완성하세요.
# 기본구성
# 페이지 제목 표시, 이미지 1장 넣기
# 사이드바는 컨트롤 센터로 지정
# 사이드바에 메뉴 이동 할 수 있는 라디오 번튼(메인페이지, 분석보고서, 설정)
# 메인페이지
# 2개의 컬럼으로 kpi 대시보드 구성
# 방문자수, 활성 사용자수를 메트릭 카드로 구성
# 분석페이지
# 탭으로 구성 (차트/데이터/설정)
# 차트에는 간단한 사용자 방문현황 그래프
# 데이터탭에는 데이터 테이블 출려
# 설정 탭에는 연결시 옵션 체크박스
# 추가 요구사항 
# streamlit 함수 : 기발하고 예쁜 것 위주로 적용
# 코드 전체를 한번에 출력
# 꼭 실행 가능한 코드여야 함.









#streamlit run app3.py
