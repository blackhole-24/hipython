# ================================================================
# pages/tab4_dr_sim.py
# 역할 : DR 시뮬레이션 (Tab4) — tab3_dr_sim.py render 호출
# ================================================================
import streamlit as st

def render():
    try:
        from tab3_dr_sim import render as _render
        _render()
    except Exception as e:
        st.error(f"DR 시뮬레이션 로드 오류: {e}")
        import traceback
        st.code(traceback.format_exc())
