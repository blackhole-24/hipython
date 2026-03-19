import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import os

matplotlib.rcParams["font.family"]        = "Malgun Gothic"
matplotlib.rcParams["axes.unicode_minus"] = False

BASE = os.path.dirname(os.path.dirname(__file__))

@st.cache_data
def load_power():
    return pd.read_csv(os.path.join(BASE, "data", "okm_power_usage.csv"))

df_power = load_power()
EMISSION_FACTOR = 0.4153
DEMAND_CHARGE   = 8320

# ── 월별 집계 ─────────────────────────────────────
monthly = df_power.groupby("m").agg(
    총사용량kWh  = ("usage_kwh",  "sum"),
    총요금원     = ("cost_won",   "sum"),
    최대피크kW   = ("15분",       "max"),
    총생산량     = ("생산량",      "sum"),
    총탄소kg     = ("co2_kg",     "sum"),
    가동시간     = ("가동여부",    "sum"),
).reset_index()

monthly["기본요금"]    = (monthly["최대피크kW"] * DEMAND_CHARGE).astype(int)
monthly["총비용"]      = monthly["총요금원"] + monthly["기본요금"]
monthly["탄소tCO2"]   = (monthly["총탄소kg"] / 1000).round(2)
monthly["에너지집약도"] = (monthly["총사용량kWh"] /
                          monthly["총생산량"].replace(0, np.nan)).round(4)
MONTH_KR = {1:"1월",2:"2월",3:"3월",4:"4월",5:"5월",6:"6월",
            7:"7월",8:"8월",9:"9월",10:"10월",11:"11월",12:"12월"}
monthly["월명"] = monthly["m"].map(MONTH_KR)

# ── 연간 합계 ─────────────────────────────────────
total_kwh    = monthly["총사용량kWh"].sum()
total_cost   = monthly["총비용"].sum()
total_co2    = monthly["탄소tCO2"].sum()
total_prod   = monthly["총생산량"].sum()
intensity    = total_kwh / total_prod if total_prod > 0 else 0

# ── 메인 ──────────────────────────────────────────
st.title("ESG 리포트 센터")
st.caption("GRI 302 기준 에너지 사용량 · Scope2 탄소 배출량 자동 집계 | 2021년 연간 데이터")

st.divider()

# ── 연간 KPI ──────────────────────────────────────
st.subheader("연간 핵심 지표 (2021)")
c1,c2,c3,c4 = st.columns(4)
with c1:
    st.metric("연간 총 전력 사용량",
              f"{total_kwh:,.0f} kWh",
              delta=f"{total_kwh/1000:.1f} MWh")
with c2:
    st.metric("연간 총 전기요금",
              f"{total_cost/10000:,.0f} 만원")
with c3:
    st.metric("Scope2 탄소 배출",
              f"{total_co2:.2f} tCO2eq",
              delta=f"배출계수 {EMISSION_FACTOR}")
with c4:
    st.metric("에너지 집약도",
              f"{intensity:.4f} kWh/개",
              delta="GRI 302-3")

st.divider()

# ── 월별 에너지 차트 ──────────────────────────────
st.subheader("월별 에너지 사용량 및 탄소 배출량")

fig, axes = plt.subplots(1, 2, figsize=(14, 4))

# 전력 사용량 막대
axes[0].bar(monthly["월명"], monthly["총사용량kWh"],
            color="#3498DB", alpha=0.8, edgecolor="white")
axes[0].set_xlabel("월")
axes[0].set_ylabel("전력 사용량 (kWh)")
axes[0].set_title("월별 총 전력 사용량")
for i, (_, r) in enumerate(monthly.iterrows()):
    axes[0].text(i, r["총사용량kWh"]+200, f"{r['총사용량kWh']:,.0f}",
                 ha="center", fontsize=7, rotation=45)
axes[0].tick_params(axis="x", rotation=45)

# 탄소 배출량 라인
color_bars = ["#E74C3C" if m in [6,7,8] else
              "#F39C12" if m in [11,12,1,2] else
              "#2ECC71" for m in monthly["m"]]
axes[1].bar(monthly["월명"], monthly["탄소tCO2"],
            color=color_bars, alpha=0.8, edgecolor="white")
axes[1].set_xlabel("월")
axes[1].set_ylabel("탄소 배출량 (tCO2eq)")
axes[1].set_title("월별 Scope2 탄소 배출량")
axes[1].tick_params(axis="x", rotation=45)
from matplotlib.patches import Patch
legend_els = [Patch(color="#E74C3C",label="하계(6~8월)"),
              Patch(color="#F39C12",label="동계(11~2월)"),
              Patch(color="#2ECC71",label="봄가을")]
axes[1].legend(handles=legend_els, fontsize=8)
plt.tight_layout()
st.pyplot(fig)
plt.close()

st.divider()

# ── 피크 절감 시나리오 ────────────────────────────
st.subheader("피크 절감 시나리오별 ESG 성과")

pct = st.slider("피크 감축률 (%)", 5, 30, 10, step=5)
saved_kwh  = total_kwh * (pct/100)
saved_co2  = saved_kwh / 1000 * EMISSION_FACTOR * 1000
saved_cost = int(total_cost * (pct/100))
trees      = int(saved_co2 * 1000 / 6.67)  # 소나무 1그루 연간 6.67kg

c1,c2,c3,c4 = st.columns(4)
with c1:
    st.metric(f"피크 {pct}% 감축 시 절감",
              f"{saved_kwh:,.0f} kWh")
with c2:
    st.metric("CO2 감축량",
              f"{saved_co2:.2f} kg",
              delta=f"= 소나무 {trees:,}그루 효과")
with c3:
    st.metric("전기요금 절감",
              f"{saved_cost/10000:,.1f} 만원/년")
with c4:
    annual_basic = monthly["기본요금"].sum()
    saved_basic  = int(annual_basic * (pct/100))
    st.metric("기본요금 절감",
              f"{saved_basic/10000:,.1f} 만원/년")

st.divider()

# ── GRI 302 데이터 표 ─────────────────────────────
st.subheader("GRI 302 에너지 데이터 (월별)")

gri_df = monthly[[
    "월명","총사용량kWh","탄소tCO2","최대피크kW",
    "기본요금","총비용","에너지집약도"
]].copy()
gri_df.columns = [
    "월","총사용량(kWh)","Scope2(tCO2eq)","최대피크(kW)",
    "기본요금(원)","총비용(원)","에너지집약도(kWh/개)"
]
gri_df["총사용량(kWh)"]     = gri_df["총사용량(kWh)"].map("{:,.1f}".format)
gri_df["Scope2(tCO2eq)"]   = gri_df["Scope2(tCO2eq)"].map("{:.2f}".format)
gri_df["최대피크(kW)"]       = gri_df["최대피크(kW)"].map("{:.1f}".format)
gri_df["기본요금(원)"]        = gri_df["기본요금(원)"].map("{:,}".format)
gri_df["총비용(원)"]          = gri_df["총비용(원)"].map("{:,}".format)
gri_df["에너지집약도(kWh/개)"] = gri_df["에너지집약도(kWh/개)"].map("{:.4f}".format)

st.dataframe(gri_df, use_container_width=True, hide_index=True)

st.divider()

# ── CSV 다운로드 ──────────────────────────────────
st.subheader("ESG 데이터 다운로드")
col1, col2 = st.columns(2)

with col1:
    csv_monthly = monthly.to_csv(index=False, encoding="utf-8-sig")
    st.download_button(
        label="월별 ESG 데이터 CSV 다운로드",
        data=csv_monthly.encode("utf-8-sig"),
        file_name="esg_monthly_2021.csv",
        mime="text/csv",
        use_container_width=True
    )

with col2:
    summary = pd.DataFrame({
        "항목"  : ["연간 총 전력 사용량","연간 총 전기요금",
                  "Scope2 탄소 배출량","에너지 집약도",
                  "탄소 배출 계수","최대 피크 전력"],
        "값"    : [f"{total_kwh:,.1f} kWh",
                  f"{total_cost/10000:,.0f} 만원",
                  f"{total_co2:.2f} tCO2eq",
                  f"{intensity:.4f} kWh/개",
                  f"{EMISSION_FACTOR} tCO2eq/MWh",
                  f"{df_power['15분'].max():.1f} kW"],
        "GRI기준": ["GRI 302-1","GRI 302-1","GRI 305-2",
                   "GRI 302-3","온실가스종합정보센터","내부지표"]
    })
    csv_summary = summary.to_csv(index=False, encoding="utf-8-sig")
    st.download_button(
        label="연간 요약 ESG 리포트 CSV 다운로드",
        data=csv_summary.encode("utf-8-sig"),
        file_name="esg_summary_2021.csv",
        mime="text/csv",
        use_container_width=True
    )

st.caption("올라운더팀 | KAMP 자원 최적화 AI 프로젝트 2 | GRI 302 기준 | 2026")
