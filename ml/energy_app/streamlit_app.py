# ================================================================
# streamlit_app.py
# 역할  : 올라운더팀 전력 피크 예측 서비스 — 메인 진입점
# 실행  : python -m streamlit run streamlit_app.py
# 구조  : 5탭 (피크예측 / 전력조회 / 운영최적화 / DR시뮬 / ESG)
# ================================================================

import streamlit as st
import sys
import os

# ── pages 폴더를 import 경로에 추가 ──────────────────────────
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'pages'))
sys.path.insert(0, os.path.dirname(__file__))

# ── 페이지 기본 설정 ──────────────────────────────────────────
st.set_page_config(
    page_title  = "전력 피크 예측 | 올라운더",
    page_icon   = "⚡",
    layout      = "wide",
    initial_sidebar_state = "expanded",
)

# ── 공통 CSS ─────────────────────────────────────────────────
st.markdown("""
<style>
    /* 탭 글자 크기 */
    .stTabs [data-baseweb="tab"] {
        font-size: 14px;
        font-weight: 500;
        padding: 8px 20px;
    }
    /* 메인 패딩 줄이기 */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 1rem;
    }
    /* 사이드바 너비 */
    [data-testid="stSidebar"] {
        min-width: 220px;
        max-width: 260px;
    }
</style>
""", unsafe_allow_html=True)

# ── 헤더 ─────────────────────────────────────────────────────
st.markdown("""
<div style="
    background:#1E293B; color:white;
    padding:12px 20px; border-radius:10px;
    display:flex; align-items:center; gap:12px;
    margin-bottom:16px;
">
    <span style="
        background:#2563EB; color:white;
        font-weight:700; font-size:14px;
        padding:4px 10px; border-radius:6px;
    ">EP</span>
    <span style="font-size:16px; font-weight:500;">
        공장 전력 피크 예측 · 자원 최적화
    </span>
    <span style="margin-left:auto; font-size:12px; opacity:.6;">
        올라운더팀 2026
    </span>
</div>
""", unsafe_allow_html=True)

# ── 탭 구성 ──────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 피크 예측",
    "⚡ 전력 조회",
    "⚙️ 운영 최적화",
    "💰 DR 시뮬레이션",
    "🌿 ESG 리포트",
])

# ── Tab1: 피크 예측 대시보드 ──────────────────────────────────
with tab1:
    try:
        from tab1_dashboard import render as render_tab1
        render_tab1()
    except Exception as e:
        st.error(f"Tab1 로드 오류: {e}")
        import traceback
        st.code(traceback.format_exc())

# ── Tab2: 전력 조회 ───────────────────────────────────────────
with tab2:
    try:
        from tab2_power_query import render as render_tab2
        render_tab2()
    except Exception as e:
        st.error(f"Tab2 로드 오류: {e}")
        import traceback
        st.code(traceback.format_exc())

# ── Tab3: 운영 최적화 ─────────────────────────────────────────
with tab3:
    try:
        from tab3_optimization import render as render_tab3
        render_tab3()
    except Exception as e:
        st.error(f"Tab3 로드 오류: {e}")
        import traceback
        st.code(traceback.format_exc())

# ── Tab4: DR 시뮬레이션 ───────────────────────────────────────
with tab4:
    try:
        from tab4_dr_sim import render as render_tab4
        render_tab4()
    except Exception as e:
        st.error(f"Tab4 로드 오류: {e}")
        import traceback
        st.code(traceback.format_exc())

# ── Tab5: ESG 리포트 ──────────────────────────────────────────
with tab5:
    try:
        from tab5_esg import render as render_tab5
        render_tab5()
    except Exception as e:
        st.error(f"Tab5 로드 오류: {e}")
        import traceback
        st.code(traceback.format_exc())
