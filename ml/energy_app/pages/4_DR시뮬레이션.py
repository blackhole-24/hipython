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

# ── 메인 ──────────────────────────────────────────
st.title("DR 시뮬레이션 대시보드")
st.caption("한전 수요반응(DR) 발령 시 예상 감축량 · 정산금 · ESG 탄소 감축 효과를 시뮬레이션합니다.")

st.divider()

# ── DR 발령 조건 입력 ─────────────────────────────
st.subheader("DR 발령 조건 설정")

col1, col2, col3 = st.columns(3)
with col1:
    dr_date = st.number_input("발령일 (YYYYMMDD)",
                               min_value=20210101,
                               max_value=20211231,
                               value=20210630, step=1)
with col2:
    dr_start = st.selectbox("시작 시간",
                             [f"{h:02d}:00" for h in range(24)],
                             index=13)
with col3:
    dr_end   = st.selectbox("종료 시간",
                             [f"{h:02d}:00" for h in range(1,25)],
                             index=15)

col4, col5 = st.columns(2)
with col4:
    dr_price = st.number_input("DR 정산 단가 (원/kWh)",
                                min_value=0, max_value=1000,
                                value=300, step=10)
with col5:
    dr_reduce = st.slider("감축 목표율 (%)", 5, 50, 15)

run_dr = st.button("시뮬레이션 실행",
                    use_container_width=True, type="primary")

st.divider()

if run_dr:
    # 시간 파싱
    start_h = int(dr_start.split(":")[0])
    end_h   = int(dr_end.split(":")[0])

    # 해당 날짜 데이터
    df_day = df_power[df_power["날짜"] == dr_date].copy()

    if len(df_day) == 0:
        st.warning(f"{dr_date} 데이터가 없습니다.")
    else:
        # DR 대상 시간대
        dr_hours = list(range(start_h, end_h))
        df_dr    = df_day[df_day["시간"].isin(dr_hours)].copy()

        if len(df_dr) == 0:
            st.warning("선택한 시간대 데이터가 없습니다.")
        else:
            # ── 계산 ──────────────────────────────
            # 기준 사용량 (DR 없을 때)
            base_usage  = df_dr["usage_kwh"].sum()
            base_peak   = df_dr["15분"].max()
            base_cost   = df_dr["cost_won"].sum()

            # 감축 후 사용량
            reduce_rate = dr_reduce / 100
            reduced_usage = base_usage * (1 - reduce_rate)
            reduced_peak  = base_peak  * (1 - reduce_rate)

            # DR 정산금 계산
            # 정산금 = 감축량(kWh) × DR 정산단가(원/kWh)
            reduced_kwh   = base_usage - reduced_usage
            dr_settlement = int(reduced_kwh * dr_price)

            # 탄소 감축
            co2_reduced = reduced_kwh / 1000 * EMISSION_FACTOR * 1000

            # ── KPI 카드 ──────────────────────────
            st.subheader("DR 시뮬레이션 결과")
            c1,c2,c3,c4 = st.columns(4)
            with c1:
                st.metric("DR 대상 시간", f"{len(dr_hours)}시간",
                          delta=f"{dr_start} ~ {dr_end}")
            with c2:
                st.metric("예상 감축량",
                          f"{reduced_kwh:.1f} kWh",
                          delta=f"감축률 {dr_reduce}%")
            with c3:
                st.metric("DR 정산금",
                          f"{dr_settlement:,} 원",
                          delta=f"단가 {dr_price}원/kWh")
            with c4:
                st.metric("CO2 감축량",
                          f"{co2_reduced:.2f} kg",
                          delta="탄소 절감 효과")

            st.divider()

            # ── 시간대별 시각화 ───────────────────
            st.subheader("DR 전후 전력 사용량 비교")
            fig, axes = plt.subplots(1, 2, figsize=(14, 4))

            # 막대 그래프
            hours_all    = df_day["시간"].values
            usage_before = df_day["usage_kwh"].values
            usage_after  = df_day["usage_kwh"].copy()
            usage_after.iloc[df_day["시간"].isin(dr_hours)] *= (1-reduce_rate)

            bar_colors = ["#E74C3C" if h in dr_hours else "#BDC3C7"
                          for h in hours_all]
            axes[0].bar(hours_all, usage_before, color=bar_colors,
                        alpha=0.5, label="DR 전", edgecolor="white")
            axes[0].bar(hours_all, usage_after.values,
                        color=["#2E86C1" if h in dr_hours else "#BDC3C7"
                               for h in hours_all],
                        alpha=0.8, label="DR 후", edgecolor="white")
            axes[0].set_xlabel("시간 (시)")
            axes[0].set_ylabel("전력 사용량 (kWh)")
            axes[0].set_xticks(range(24))
            axes[0].legend(fontsize=9)
            axes[0].set_title("시간대별 DR 전후 사용량")

            # 누적 요금 라인
            cum_before = df_day["cumul_cost_day"].values
            cum_after  = df_day["cumul_cost_day"].copy()
            for i, h in enumerate(df_day["시간"].values):
                if h in dr_hours:
                    cum_after.iloc[i:] -= int(
                        df_day[df_day["시간"]==h]["cost_won"].values[0] * reduce_rate
                    )

            axes[1].plot(hours_all, cum_before/10000,
                         color="#E74C3C", lw=2, marker="o",
                         ms=3, label="DR 전 누적요금")
            axes[1].plot(hours_all, cum_after.values/10000,
                         color="#2E86C1", lw=2, marker="s",
                         ms=3, linestyle="--", label="DR 후 누적요금")
            axes[1].fill_between(hours_all,
                                  cum_before/10000,
                                  cum_after.values/10000,
                                  alpha=0.2, color="#2ECC71",
                                  label="절감 구간")
            axes[1].set_xlabel("시간 (시)")
            axes[1].set_ylabel("누적 요금 (만원)")
            axes[1].set_xticks(range(24))
            axes[1].legend(fontsize=9)
            axes[1].set_title("누적 요금 비교")

            plt.suptitle(f"{dr_date} DR 시뮬레이션 결과",
                         fontsize=12, fontweight="bold")
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()

            st.divider()

            # ── 비용 절감 상세 ────────────────────
            st.subheader("비용 절감 상세")
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**DR 전**")
                st.metric("DR 시간대 총 사용량",
                          f"{base_usage:.1f} kWh")
                st.metric("DR 시간대 총 요금",
                          f"{base_cost:,} 원")
                st.metric("최대 피크",
                          f"{base_peak:.1f} kW")
            with c2:
                st.markdown("**DR 후**")
                st.metric("DR 시간대 총 사용량",
                          f"{reduced_usage:.1f} kWh",
                          delta=f"{reduced_usage-base_usage:,.1f} kWh")
                after_cost = int(base_cost * (1-reduce_rate))
                st.metric("DR 시간대 총 요금",
                          f"{after_cost:,} 원",
                          delta=f"{after_cost-base_cost:,} 원")
                st.metric("최대 피크",
                          f"{reduced_peak:.1f} kW",
                          delta=f"{reduced_peak-base_peak:+.1f} kW")

            st.divider()

            # ── DR 수익 요약 ──────────────────────
            st.subheader("DR 수익 요약")
            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("요금 절감액",
                          f"{base_cost-after_cost:,} 원")
            with c2:
                st.metric("DR 정산금",
                          f"{dr_settlement:,} 원",
                          delta="한전 정산")
            with c3:
                total_benefit = (base_cost-after_cost) + dr_settlement
                st.metric("총 편익",
                          f"{total_benefit:,} 원",
                          delta="절감 + 정산금")

            st.info(f"""DR 참여 효과 요약
감축량: {reduced_kwh:.1f} kWh  |  정산금: {dr_settlement:,}원  |  CO2 감축: {co2_reduced:.2f}kg  |  총 편익: {total_benefit:,}원""")

st.caption("올라운더팀 | KAMP 자원 최적화 AI 프로젝트 2 | 2026")
