import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import joblib, os

matplotlib.rcParams["font.family"]        = "Malgun Gothic"
matplotlib.rcParams["axes.unicode_minus"] = False

BASE = os.path.dirname(os.path.dirname(__file__))

@st.cache_data
def load_power():
    return pd.read_csv(os.path.join(BASE, "data", "okm_power_usage.csv"))

@st.cache_resource
def load_model():
    return joblib.load(os.path.join(BASE, "models", "energy_pipeline_v2.pkl"))

df_power = load_power()
loaded   = load_model()

# ── 메인 ──────────────────────────────────────────
st.title("예측 · 분석")
st.caption("XGBoost | Set_C (23개 피처) | 2021년 1년치 학습 | R²=0.9999")

# ── 1. 전력 추이 그래프 ───────────────────────────
st.subheader("전력 추이 — 월별 평균 피크 vs 전력 사용량")

month_list = list(range(1,13))
selected_m = st.selectbox("월 선택", month_list,
                           format_func=lambda x: f"{x}월", index=5)

df_m = df_power[df_power["m"] == selected_m].copy()

fig, ax = plt.subplots(figsize=(14, 4))
ax.plot(df_m["시간"].values[:24],
        df_m.groupby("시간")["15분"].mean().values,
        color="#E74C3C", linewidth=2, marker="o",
        markersize=4, label="평균 피크(kW)")
ax.fill_between(df_m["시간"].values[:24],
                df_m.groupby("시간")["15분"].mean().values,
                alpha=0.15, color="#E74C3C")
ax.plot(df_m["시간"].values[:24],
        df_m.groupby("시간")["usage_kwh"].mean().values,
        color="#3498DB", linewidth=2, marker="s",
        markersize=4, linestyle="--", label="평균 사용량(kWh)")
ax.set_xlabel("시간 (시)")
ax.set_ylabel("kW / kWh")
ax.set_xticks(range(24))
ax.axhline(110, color="#F39C12", linestyle=":", linewidth=1, label="주의 110kW")
ax.axhline(150, color="#E74C3C", linestyle=":", linewidth=1, label="위험 150kW")
ax.legend(fontsize=9)
ax.set_title(f"{selected_m}월 시간대별 평균 전력 추이")
plt.tight_layout()
st.pyplot(fig)
plt.close()

st.divider()

# ── 2. 중요 변수 Top N ────────────────────────────
st.subheader("피처 영향력 Top 8")

feat_data = {
    "피처명"  : ["가동여부","생산량","is_weekend","weekday",
               "공장인원","주간여부","is_holiday","tou_bucket"],
    "한글 명칭": ["공장 가동여부","시간당 생산량","주말여부","요일코드",
               "공장인원","주간근무여부","공휴일여부","TOU요금구간"],
    "상관계수" : [0.73, 0.53, 0.51, 0.43, 0.30, 0.28, 0.22, 0.20],
    "카테고리" : ["생산","생산","시간/달력","시간/달력",
               "생산","시간/달력","시간/달력","전기요금"],
}
df_feat = pd.DataFrame(feat_data)

fig2, ax2 = plt.subplots(figsize=(10, 4))
colors = ["#E74C3C" if c=="생산" else
          "#3498DB" if c=="시간/달력" else
          "#F39C12" for c in df_feat["카테고리"]]
bars = ax2.barh(df_feat["한글 명칭"][::-1],
                df_feat["상관계수"][::-1],
                color=colors[::-1], alpha=0.85, edgecolor="white")
ax2.set_xlabel("절대 상관계수")
ax2.set_title("피크 전력과의 상관계수 (절대값)")
ax2.axvline(0.5, color="gray", linestyle="--", linewidth=1)
for bar, val in zip(bars, df_feat["상관계수"][::-1]):
    ax2.text(val+0.01, bar.get_y()+bar.get_height()/2,
             f"{val:.2f}", va="center", fontsize=9)
from matplotlib.patches import Patch
legend_els = [Patch(color="#E74C3C",label="생산"),
              Patch(color="#3498DB",label="시간/달력"),
              Patch(color="#F39C12",label="전기요금")]
ax2.legend(handles=legend_els, fontsize=9)
plt.tight_layout()
st.pyplot(fig2)
plt.close()

st.divider()

# ── 3. 모델 성능 비교표 ───────────────────────────
st.subheader("모델 성능 비교")
model_data = {
    "모델"      : ["XGBoost","Random Forest","DNN-Deep","DNN-Medium",
                  "Decision Tree","Ridge","Linear Reg."],
    "Feature Set": ["Set_C","Set_C","Set_C","Set_C",
                    "Set_C","Set_C","Set_C"],
    "RMSE"      : [0.74, 0.10, 1.82, 1.81, 0.19, 0.01, 0.00],
    "MAE"       : [0.40, 0.03, 1.31, 1.32, 0.06, 0.01, 0.00],
    "R²"        : [0.9998, 1.0000, 0.9989, 0.9989, 1.0000, 1.0000, 1.0000],
}
df_model = pd.DataFrame(model_data)
st.dataframe(df_model, use_container_width=True, hide_index=True)
st.caption("* Set_C = 공정+날씨+전기요금 전체 23개 피처 | 현재 사용 모델: XGBoost (energy_pipeline_v2.pkl)")

st.divider()

# ── 4. 과거 데이터 검색 ───────────────────────────
st.subheader("과거 데이터 검색")
st.caption("날짜를 입력하면 해당일의 전력·생산량·날씨·요금 정보를 조회합니다.")

col1, col2 = st.columns([1,3])
with col1:
    search_date = st.number_input(
        "날짜 입력 (YYYYMMDD)",
        min_value=20210101, max_value=20211231,
        value=20210615, step=1
    )
    search_btn = st.button("검색", use_container_width=True)

if search_btn:
    df_search = df_power[df_power["날짜"] == search_date].copy()

    if len(df_search) == 0:
        st.warning(f"{search_date} 날짜 데이터가 없습니다.")
    else:
        date_str = str(search_date)
        st.success(f"{date_str[:4]}년 {date_str[4:6]}월 {date_str[6:]}일 데이터 — {len(df_search)}건")

        # 요약 KPI
        c1,c2,c3,c4 = st.columns(4)
        with c1: st.metric("일 최대 피크", f"{df_search['15분'].max():.1f} kW")
        with c2: st.metric("일 총 사용량", f"{df_search['usage_kwh'].sum():.1f} kWh")
        with c3: st.metric("일 총 요금", f"{df_search['cost_won'].sum():,} 원")
        with c4: st.metric("일 총 생산량", f"{df_search['생산량'].sum():,} 개")

        # 시간대별 그래프
        fig3, axes = plt.subplots(2, 1, figsize=(12, 6))
        fig3.suptitle(f"{search_date} 시간대별 전력 및 생산량", fontsize=12)

        axes[0].plot(df_search["시간"], df_search["15분"],
                     color="#E74C3C", marker="o", ms=4, label="피크(kW)")
        axes[0].fill_between(df_search["시간"], df_search["15분"],
                             alpha=0.15, color="#E74C3C")
        axes[0].plot(df_search["시간"], df_search["usage_kwh"],
                     color="#3498DB", marker="s", ms=4,
                     linestyle="--", label="사용량(kWh)")
        axes[0].axhline(110, color="#F39C12", linestyle=":", lw=1)
        axes[0].axhline(150, color="#E74C3C", linestyle=":", lw=1)
        axes[0].set_ylabel("kW / kWh")
        axes[0].legend(fontsize=8)
        axes[0].set_xticks(range(24))

        axes[1].bar(df_search["시간"], df_search["생산량"],
                    color="#2ECC71", alpha=0.7, edgecolor="white")
        axes[1].set_xlabel("시간 (시)")
        axes[1].set_ylabel("생산량 (개)")
        axes[1].set_xticks(range(24))

        plt.tight_layout()
        st.pyplot(fig3)
        plt.close()

        # 상세 테이블
        with st.expander("시간대별 상세 데이터 보기"):
            show_cols = ["시간","15분","usage_kwh","cost_won",
                         "생산량","공장인원","기온","습도",
                         "tou_bucket","cumul_kwh_day","cumul_cost_day"]
            show_cols = [c for c in show_cols if c in df_search.columns]
            st.dataframe(df_search[show_cols].reset_index(drop=True),
                         use_container_width=True, hide_index=True)

st.caption("올라운더팀 | KAMP 자원 최적화 AI 프로젝트 2 | 2026")
