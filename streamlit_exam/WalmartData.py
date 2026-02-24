import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# 페이지 설정
st.set_page_config(
    page_title="월마트 데이터 분석 대시보드",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 커스텀 CSS - 테이블 흰색 글씨 + ROI 박스 통일
st.markdown("""
<style>
    /* 전체 배경 */
    .stApp {
        background: linear-gradient(135deg, #0a1929 0%, #1a237e 100%);
    }
    
    /* 사이드바 */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d47a1 0%, #01579b 100%);
    }
    
    /* 메인 컨테이너 */
    .main {
        background-color: rgba(13, 71, 161, 0.1);
    }
    
    /* 제목 스타일 */
    h1 {
        color: #b3e5fc !important;
        text-shadow: 0 0 20px rgba(179, 229, 252, 0.5);
    }
    
    h2, h3 {
        color: #81d4fa !important;
    }
    
    /* 메트릭 카드 */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #1565c0 0%, #0d47a1 100%);
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #42a5f5;
        box-shadow: 0 4px 15px rgba(66, 165, 245, 0.3);
    }
    
    [data-testid="stMetricLabel"] {
        color: #b3e5fc !important;
        font-size: 14px !important;
    }
    
    [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 28px !important;
        font-weight: bold !important;
    }
    
    /* 메트릭 delta 색상 수정 */
    [data-testid="stMetricDelta"] {
        color: #ffffff !important;
        background-color: rgba(255, 255, 255, 0.2) !important;
        padding: 4px 8px !important;
        border-radius: 4px !important;
        font-weight: bold !important;
    }
    
    [data-testid="stMetricDelta"] svg {
        fill: #ffffff !important;
    }
    
    /* 정보 박스 */
    .stAlert {
        background-color: rgba(21, 101, 192, 0.2) !important;
        border: 1px solid #42a5f5 !important;
        color: #b3e5fc !important;
    }
    
    /* HTML 테이블 스타일 - 흰색 글씨 강제 적용 */
    table {
        background-color: rgba(13, 71, 161, 0.3) !important;
        border-collapse: collapse !important;
        width: 100% !important;
    }
    
    table th {
        background-color: rgba(21, 101, 192, 0.5) !important;
        color: #ffffff !important;
        font-weight: bold !important;
        border: 1px solid #42a5f5 !important;
        padding: 12px !important;
        text-align: left !important;
    }
    
    table td {
        background-color: rgba(13, 71, 161, 0.2) !important;
        color: #ffffff !important;
        border: 1px solid #42a5f5 !important;
        padding: 10px !important;
    }
    
    /* Streamlit 기본 테이블 스타일 */
    .dataframe {
        background-color: rgba(13, 71, 161, 0.3) !important;
    }
    
    .dataframe th {
        background-color: rgba(21, 101, 192, 0.5) !important;
        color: #ffffff !important;
        font-weight: bold !important;
        border: 1px solid #42a5f5 !important;
        padding: 10px !important;
    }
    
    .dataframe td {
        background-color: rgba(13, 71, 161, 0.2) !important;
        color: #ffffff !important;
        border: 1px solid #42a5f5 !important;
        padding: 8px !important;
    }
    
    /* 버튼 */
    .stButton button {
        background: linear-gradient(135deg, #1976d2 0%, #1565c0 100%);
        color: white;
        border: 1px solid #42a5f5;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: bold;
        box-shadow: 0 2px 10px rgba(66, 165, 245, 0.3);
    }
    
    .stButton button:hover {
        background: linear-gradient(135deg, #1565c0 0%, #0d47a1 100%);
        box-shadow: 0 4px 15px rgba(66, 165, 245, 0.5);
    }
    
    /* 텍스트 */
    p, li, span {
        color: #b3e5fc !important;
    }
    
    /* 구분선 */
    hr {
        border-color: #42a5f5 !important;
    }
</style>
""", unsafe_allow_html=True)

# 사이드바 (제목 글씨 크기 축소로 줄바꿈 방지)
with st.sidebar:
    st.markdown("<h2 style='font-size: 20px; margin-bottom: 10px;'>🛒 월마트 데이터 분석</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    menu = st.radio(
        "메뉴 선택",
        ["🏠 메인", "📊 분석 개요", "💡 핵심 인사이트", "📈 데이터 시각화", "🎯 마케팅 전략", "💰 예상 결과"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### 📌 Quick Stats")
    st.metric("총 거래", "550,068건")
    st.metric("분석 기간", "Black Friday")
    st.metric("고객 수", "5,891명")

# ========================================
# 메인 페이지
# ========================================
if menu == "🏠 메인":
    st.title("🛒 월마트 고객 데이터 분석 대시보드")
    st.markdown("### Walmart Customer Analytics & Marketing Strategy")
    st.markdown("---")
    
    # 주요 지표
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📊 총 거래 건수",
            value="550,068건",
            delta="Black Friday 기간"
        )
    
    with col2:
        st.metric(
            label="👥 고유 고객",
            value="5,891명",
            delta="분석 완료"
        )
    
    with col3:
        st.metric(
            label="🎯 캐시카우 세그먼트",
            value="M_26-35",
            delta="18.19% 매출"
        )
    
    with col4:
        st.metric(
            label="💎 베스트셀러",
            value="P00025442",
            delta="1,586건 판매"
        )
    
    st.markdown("---")
    
    # 연구 가설 카드
    st.markdown("## 🎯 연구 가설")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("""
        **가설 1**
        
        특정 성별과 연령층의 조합이 전체 매출에 가장 큰 기여도를 보일 것이다.
        """)
    
    with col2:
        st.info("""
        **가설 2**
        
        해당 핵심 세그먼트가 가장 많이 구매하는 특정 베스트셀러 상품이 존재할 것이다.
        """)
    
    with col3:
        st.info("""
        **가설 3**
        
        핵심 세그먼트 타겟 마케팅은 전체 매출 증대에 가장 효과적일 것이다.
        """)
    
    st.markdown("---")
    
    # 프로젝트 개요
    st.markdown("## 📋 프로젝트 개요")
    
    st.markdown("""
    본 프로젝트는 **Kaggle의 월마트 데이터셋** 약 55만 건의 거래 데이터를 분석하여:
    
    - 🎯 **핵심 매출 기여 고객층(Cash Cow)** 식별
    - 💎 **베스트셀러 상품(Best Seller)** 발굴
    - 📈 **데이터 기반 마케팅 전략** 수립
    
    을 목표로 합니다.
    """)
    
    st.success("✅ **결론**: 26-35세 남성이 매출 18.19% 기여, 타겟 마케팅으로 매출 20% 증대 전망")

# ========================================
# 분석 개요
# ========================================
elif menu == "📊 분석 개요":
    st.title("📊 분석 개요")
    st.markdown("---")
    
    # 데이터 출처
    st.markdown("## 📁 데이터 출처")
    st.markdown("""
    - **출처**: [Kaggle - Walmart Sales Dataset](https://www.kaggle.com/datasets/devarajv88/walmart-sales-dataset)
    - **총 거래**: 550,068건
    - **고객 수**: 5,891명
    - **제품 수**: 3,631개
    - **분석 기간**: Black Friday
    """)
    
    st.markdown("---")
    
    # 분석 방법론
    st.markdown("## 🔬 분석 방법론")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 1️⃣ 데이터 전처리")
        st.markdown("""
        - 성별 × 연령대 세그먼트 정의
        - 총 14개 고객 세그먼트 생성
        - 결측치 및 이상치 검토
        """)
        
        st.markdown("### 2️⃣ 탐색적 데이터 분석")
        st.markdown("""
        - 세그먼트별 총 매출액 계산
        - 거래 건수 및 평균 구매금액 분석
        - 상관관계 및 분포 분석
        """)
    
    with col2:
        st.markdown("### 3️⃣ 세그먼트 분석")
        st.markdown("""
        - 매출 기여도 기준 순위 산정
        - 캐시카우 세그먼트 식별
        - 세그먼트별 특성 비교
        """)
        
        st.markdown("### 4️⃣ 제품 분석")
        st.markdown("""
        - 캐시카우 세그먼트의 구매 제품 분석
        - 베스트셀러 상품 식별
        - 제품-세그먼트 매트릭스 생성
        """)
    
    st.markdown("---")
    
    # 데이터 구조
    st.markdown("## 📊 데이터 구조")
    
    data_structure = {
        "컬럼명": ["User_ID", "Product_ID", "Gender", "Age", "Occupation", 
                   "City_Category", "Stay_In_Current_City_Years", "Marital_Status", 
                   "Product_Category", "Purchase"],
        "설명": ["고객 고유 ID", "제품 고유 ID", "성별 (M/F)", "연령대 (7개 구간)", 
                "직업 코드 (0-20)", "도시 등급 (A/B/C)", "거주 기간 (년)", 
                "결혼 여부 (0/1)", "제품 카테고리", "구매 금액 ($)"],
        "데이터 타입": ["int", "str", "str", "str", "int", "str", "str", "int", "int", "int"]
    }
    
    df_structure = pd.DataFrame(data_structure)
    st.dataframe(df_structure, use_container_width=True)

# ========================================
# 핵심 인사이트
# ========================================
elif menu == "💡 핵심 인사이트":
    st.title("💡 핵심 인사이트")
    st.markdown("---")
    
    # 캐시카우 세그먼트
    st.markdown("## 🏆 캐시카우 세그먼트")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #1565c0 0%, #0d47a1 100%); 
                    padding: 20px; border-radius: 10px; border: 2px solid #42a5f5;
                    box-shadow: 0 4px 15px rgba(66, 165, 245, 0.3);'>
            <p style='color: #b3e5fc; font-size: 13px; margin-bottom: 8px;'>세그먼트</p>
            <p style='color: #ffffff; font-size: 22px; font-weight: bold; margin: 0; line-height: 1.3;'>
                26-35세<br>남성
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #1565c0 0%, #0d47a1 100%); 
                    padding: 20px; border-radius: 10px; border: 2px solid #42a5f5;
                    box-shadow: 0 4px 15px rgba(66, 165, 245, 0.3);'>
            <p style='color: #b3e5fc; font-size: 13px; margin-bottom: 8px;'>매출 기여도</p>
            <p style='color: #ffffff; font-size: 28px; font-weight: bold; margin: 0;'>18.19%</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #1565c0 0%, #0d47a1 100%); 
                    padding: 20px; border-radius: 10px; border: 2px solid #42a5f5;
                    box-shadow: 0 4px 15px rgba(66, 165, 245, 0.3);'>
            <p style='color: #b3e5fc; font-size: 13px; margin-bottom: 8px;'>거래 비중</p>
            <p style='color: #ffffff; font-size: 28px; font-weight: bold; margin: 0;'>17.85%</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col4, col5 = st.columns(2)
    
    with col4:
        st.metric(
            label="평균 구매금액",
            value="$9,437",
            delta="전체 평균 대비 높음"
        )
    
    with col5:
        st.metric(
            label="총 매출액",
            value="$1.43억",
            delta="1위"
        )
    
    st.markdown("---")
    
    # 베스트셀러 상품
    st.markdown("## 💎 베스트셀러 상품")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="제품 코드",
            value="P00025442",
            delta="구매 빈도 1위"
        )
    
    with col2:
        st.metric(
            label="구매 건수",
            value="1,586건",
            delta="캐시카우 세그먼트"
        )
    
    with col3:
        st.metric(
            label="총 매출",
            value="$954만",
            delta="세그먼트 내 1.21%"
        )
    
    st.markdown("---")
    
    # 5개 핵심 인사이트
    st.markdown("## 📌 5대 핵심 인사이트")
    
    insights = [
        {
            "title": "인사이트 1",
            "content": "26-35세 남성 고객이 전체 매출의 **18.19%**를 차지하며 캐시카우로 식별되었다."
        },
        {
            "title": "인사이트 2",
            "content": "캐시카우 세그먼트는 전체 거래의 **17.85%**를 차지하며, 평균 구매금액은 **$9,437**이다."
        },
        {
            "title": "인사이트 3",
            "content": "캐시카우 세그먼트가 가장 많이 구매하는 베스트셀러 상품은 **P00025442**이며, 총 **1,586건** 구매되었다."
        },
        {
            "title": "인사이트 4",
            "content": "베스트셀러 상품은 캐시카우 세그먼트 구매의 **1.21%**를 차지하며, 총 매출은 **$954만**이다."
        },
        {
            "title": "인사이트 5",
            "content": "캐시카우 세그먼트와 베스트셀러 상품을 결합한 타겟 마케팅 시 예상 매출 증대 효과는 약 **20%**이다."
        }
    ]
    
    for i, insight in enumerate(insights):
        st.info(f"**{insight['title']}**: {insight['content']}")

# ========================================
# 데이터 시각화
# ========================================
elif menu == "📈 데이터 시각화":
    st.title("📈 데이터 시각화")
    st.markdown("---")
    
    # 시각화 1: 성별 분포
    st.markdown("## 👥 성별 거래 분포")
    
    gender_data = {
        '성별': ['남성', '여성'],
        '거래건수': [405380, 144688],
        '비율': [73.7, 26.3]
    }
    
    fig1 = go.Figure(data=[
        go.Pie(
            labels=gender_data['성별'],
            values=gender_data['거래건수'],
            hole=0.4,
            marker=dict(
                colors=['#1976d2', '#42a5f5'],
                line=dict(color='#0d47a1', width=2)
            ),
            textinfo='label+percent',
            textfont=dict(size=14, color='white', family='Arial Black'),
            hovertemplate='<b>%{label}</b><br>거래: %{value:,}건<br>비율: %{percent}<extra></extra>'
        )
    ])
    
    fig1.update_layout(
        title=dict(
            text='성별 거래 분포',
            font=dict(size=20, color='#b3e5fc', family='Arial Black'),
            x=0.5,
            xanchor='center'
        ),
        paper_bgcolor='rgba(13, 71, 161, 0.1)',
        plot_bgcolor='rgba(13, 71, 161, 0.1)',
        font=dict(color='#b3e5fc'),
        showlegend=True,
        legend=dict(
            font=dict(color='#b3e5fc', size=12),
            bgcolor='rgba(13, 71, 161, 0.3)',
            bordercolor='#42a5f5',
            borderwidth=1
        ),
        height=500
    )
    
    st.plotly_chart(fig1, use_container_width=True)
    
    st.markdown("---")
    
    # 시각화 2: Top 5 세그먼트
    st.markdown("## 🎯 Top 5 세그먼트별 총 매출")
    
    segments_data = {
        '세그먼트': ['M_26-35', 'M_36-45', 'M_18-25', 'F_26-35', 'M_46-50'],
        '총매출': [143199554, 126601993, 108907502, 82338131, 55906271],
        '비율': [18.19, 16.08, 13.83, 10.46, 7.10]
    }
    
    fig2 = go.Figure(data=[
        go.Bar(
            x=segments_data['총매출'],
            y=segments_data['세그먼트'],
            orientation='h',
            marker=dict(
                color=segments_data['총매출'],
                colorscale=[
                    [0, '#0d47a1'],
                    [0.5, '#1976d2'],
                    [1, '#42a5f5']
                ],
                line=dict(color='#42a5f5', width=1)
            ),
            text=[f'${x/1000000:.1f}M' for x in segments_data['총매출']],
            textposition='outside',
            textfont=dict(size=12, color='#b3e5fc', family='Arial'),
            hovertemplate='<b>%{y}</b><br>매출: $%{x:,.0f}<br>비율: %{customdata:.2f}%<extra></extra>',
            customdata=segments_data['비율']
        )
    ])
    
    fig2.update_layout(
        title=dict(
            text='Top 5 세그먼트별 총 매출',
            font=dict(size=20, color='#b3e5fc', family='Arial Black'),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title=dict(
                text='총 매출액 ($)',
                font=dict(size=14, color='#b3e5fc')
            ),
            tickfont=dict(color='#b3e5fc', size=11),
            gridcolor='rgba(66, 165, 245, 0.2)',
            showgrid=True
        ),
        yaxis=dict(
            title=dict(
                text='세그먼트',
                font=dict(size=14, color='#b3e5fc')
            ),
            tickfont=dict(color='#b3e5fc', size=11)
        ),
        paper_bgcolor='rgba(13, 71, 161, 0.1)',
        plot_bgcolor='rgba(13, 71, 161, 0.1)',
        font=dict(color='#b3e5fc'),
        height=500,
        margin=dict(l=100, r=100, t=80, b=60)
    )
    
    st.plotly_chart(fig2, use_container_width=True)
    
    # 주요 수치 요약
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("1위 세그먼트", "M_26-35", "18.19%")
    
    with col2:
        st.metric("1위 매출액", "$143.2M", "+$16.6M (vs 2위)")
    
    with col3:
        st.metric("Top 5 비중", "65.66%", "전체 매출의 2/3")

# ========================================
# 마케팅 전략
# ========================================
elif menu == "🎯 마케팅 전략":
    st.title("🎯 마케팅 전략")
    st.markdown("---")
    
    # 5대 전략
    st.markdown("## 📋 5대 핵심 전략")
    
    strategies = [
        {
            "icon": "🎯",
            "title": "전략 1: 세그먼트 타겟 광고",
            "content": "26-35세 남성 대상 SNS 광고 집중 (Instagram, Facebook, YouTube)",
            "budget": "30%"
        },
        {
            "icon": "💎",
            "title": "전략 2: 베스트셀러 상품 프로모션",
            "content": "P00025442 중심의 번들 상품, 할인 이벤트 기획",
            "budget": "25%"
        },
        {
            "icon": "📱",
            "title": "전략 3: 인플루언서 마케팅",
            "content": "26-35세 남성 인플루언서와 베스트셀러 상품 협업",
            "budget": "20%"
        },
        {
            "icon": "🔄",
            "title": "전략 4: 크로스셀링 전략",
            "content": "베스트셀러 상품 구매자에게 연관 제품 추천 알고리즘 적용",
            "budget": "15%"
        },
        {
            "icon": "📦",
            "title": "전략 5: 재고 및 진열 최적화",
            "content": "베스트셀러 상품의 재고 확대 및 매장 내 프라임 위치 배치",
            "budget": "10%"
        }
    ]
    
    for strategy in strategies:
        with st.expander(f"{strategy['icon']} {strategy['title']} - 예산 배분 {strategy['budget']}"):
            st.markdown(f"**실행 계획**: {strategy['content']}")
            st.progress(int(strategy['budget'].rstrip('%')) / 100)
    
    st.markdown("---")
    
    # 예산 배분 차트
    st.markdown("## 💰 마케팅 예산 배분")
    
    budget_data = {
        '전략': ['세그먼트 타겟 광고', '베스트셀러 프로모션', '인플루언서 마케팅', 
                '크로스셀링', '재고 최적화'],
        '예산비중': [30, 25, 20, 15, 10]
    }
    
    fig3 = go.Figure(data=[
        go.Bar(
            x=budget_data['전략'],
            y=budget_data['예산비중'],
            marker=dict(
                color=budget_data['예산비중'],
                colorscale=[
                    [0, '#0d47a1'],
                    [0.5, '#1976d2'],
                    [1, '#42a5f5']
                ],
                line=dict(color='#42a5f5', width=1)
            ),
            text=[f'{x}%' for x in budget_data['예산비중']],
            textposition='outside',
            textfont=dict(size=14, color='#b3e5fc', family='Arial Black'),
            hovertemplate='<b>%{x}</b><br>예산: %{y}%<extra></extra>'
        )
    ])
    
    fig3.update_layout(
        title=dict(
            text='마케팅 예산 배분',
            font=dict(size=20, color='#b3e5fc', family='Arial Black'),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title=dict(
                text='전략',
                font=dict(size=14, color='#b3e5fc')
            ),
            tickfont=dict(color='#b3e5fc', size=10),
            tickangle=-30
        ),
        yaxis=dict(
            title=dict(
                text='예산 비중 (%)',
                font=dict(size=14, color='#b3e5fc')
            ),
            tickfont=dict(color='#b3e5fc', size=11),
            gridcolor='rgba(66, 165, 245, 0.2)',
            showgrid=True,
            range=[0, 40]
        ),
        paper_bgcolor='rgba(13, 71, 161, 0.1)',
        plot_bgcolor='rgba(13, 71, 161, 0.1)',
        font=dict(color='#b3e5fc'),
        height=500,
        margin=dict(l=60, r=60, t=100, b=80)
    )
    
    st.plotly_chart(fig3, use_container_width=True)
    
    st.success("✅ **총 마케팅 예산**: 100% 최적 배분 완료")

# ========================================
# 예상 결과
# ========================================
elif menu == "💰 예상 결과":
    st.title("💰 예상 결과")
    st.markdown("---")
    
    # 최종 결론
    st.markdown("## 🎯 최종 결론")
    
    st.success("""
    ### 데이터 분석 결과
    
    월마트에서 가장 매출을 많이 기여하는 **캐시카우(Cash Cow)는 26-35세 남성**이며, 
    이들이 가장 많이 구매하는 **베스트셀러 상품은 P00025442**입니다.
    
    이들을 공략하기 위해 **SNS 광고, 인플루언서 마케팅** 등을 통해 베스트셀러 상품을 
    집중 프로모션해야 하며, 예상 효과는 **매출 20% 증대**입니다.
    """)
    
    st.markdown("---")
    
    # 예상 매출 증대 효과
    st.markdown("## 📈 예상 매출 증대 효과")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="현재 총 매출",
            value="$787M",
            delta="Black Friday 기준"
        )
    
    with col2:
        st.metric(
            label="예상 증대 매출",
            value="$157M",
            delta="+20%"
        )
    
    with col3:
        st.metric(
            label="목표 총 매출",
            value="$944M",
            delta="마케팅 후"
        )
    
    st.markdown("---")
    
    # 실행 타임라인 (흰색 글씨 강제 적용)
    st.markdown("## 📅 실행 타임라인")
    
    st.markdown("""
    <style>
        .timeline-table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        .timeline-table th {
            background-color: rgba(21, 101, 192, 0.6) !important;
            color: #ffffff !important;
            font-weight: bold !important;
            padding: 14px !important;
            border: 1px solid #42a5f5 !important;
            text-align: left !important;
            font-size: 15px !important;
        }
        .timeline-table td {
            background-color: rgba(13, 71, 161, 0.25) !important;
            color: #ffffff !important;
            padding: 12px !important;
            border: 1px solid #42a5f5 !important;
            font-size: 14px !important;
        }
    </style>
    
    <table class="timeline-table">
        <thead>
            <tr>
                <th>단계</th>
                <th>기간</th>
                <th>주요 활동</th>
                <th>예상 결과</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>1단계</td>
                <td>1-2개월</td>
                <td>타겟 광고 캠페인 시작</td>
                <td>브랜드 인지도 +15%</td>
            </tr>
            <tr>
                <td>2단계</td>
                <td>2-3개월</td>
                <td>베스트셀러 프로모션</td>
                <td>제품 판매 +25%</td>
            </tr>
            <tr>
                <td>3단계</td>
                <td>3-4개월</td>
                <td>인플루언서 협업</td>
                <td>SNS 참여도 +40%</td>
            </tr>
            <tr>
                <td>4단계</td>
                <td>4-6개월</td>
                <td>크로스셀링 알고리즘</td>
                <td>객단가 +18%</td>
            </tr>
            <tr>
                <td>5단계</td>
                <td>지속</td>
                <td>재고 최적화</td>
                <td>재고 회전율 +30%</td>
            </tr>
        </tbody>
    </table>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 투자 대비 수익 (ROI)
    st.markdown("## 💵 투자 대비 수익 (ROI)")
    
    roi_data = {
        '구분': ['마케팅 투자', '예상 매출 증대', '순이익', 'ROI'],
        '금액': ['$10M', '$157M', '$147M', '1,470%']
    }
    
    df_roi = pd.DataFrame(roi_data)
    st.table(df_roi)
    
    # ROI 설명 박스 (st.table과 동일한 스타일 적용)
    st.markdown("""
    <div style='background-color: rgba(33, 150, 243, 0.2); 
                border-left: 4px solid #2196F3; 
                padding: 15px; 
                border-radius: 5px;
                margin-top: 15px;'>
        <p style='margin: 0; 
                  color: #ffffff; 
                  font-size: 14px; 
                  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                  font-weight: 400;
                  line-height: 1.6;'>
            💡 <strong style='font-weight: 700;'>ROI 1,470%:</strong> 투자 $1당 $14.70의 수익 예상
        </p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #81d4fa; padding: 20px;'>
    <p>🛒 <b>월마트 데이터 분석 대시보드</b></p>
    <p style='font-size: 12px;'>Powered by Streamlit | Data from Kaggle</p>
</div>
""", unsafe_allow_html=True)