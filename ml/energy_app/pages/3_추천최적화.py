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
pipeline     = loaded["pipeline"]
feature_cols = loaded["feature_cols"]

TOU_PRICE = {0:95.7, 1:121.5, 2:155.0}
TOU_LABEL = {0:"경부하", 1:"중간부하", 2:"최대부하"}
DEMAND_CHARGE = 8320

def get_tou(month, hour):
    if hour >= 22 or hour <= 7: return 0
    if month in [6,7,8]:
        return 2 if hour in [11,12,13,14,15,16,17] else 1
    elif month in [11,12,1,2]:
        return 2 if hour in [10,17,18,19,20] else 1
    return 1

# ── 메인 ──────────────────────────────────────────
st.title("추천 (최적화)")
st.caption("목표 생산량 기반 최적 운영안 추천 및 비용 비교")

st.divider()

# ── 최적화 조건 입력 ──────────────────────────────
st.subheader("최적화 조건 입력")

col1, col2, col3 = st.columns(3)
with col1:
    target_prod  = st.number_input("목표 생산량 (개)", 0, 9830, 1000, step=50)
with col2:
    current_workers = st.slider("현재 인원 (명)", 1, 48, 20)
with col3:
    month_sel = st.selectbox("월", list(range(1,13)),
                              format_func=lambda x: f"{x}월", index=5)

col4, col5 = st.columns(2)
with col4:
    current_hour = st.slider("현재 시간", 0, 23, 10)
with col5:
    furnace_now = st.radio("열처리로 현재 상태",
                            [0,1], format_func=lambda x: "OFF" if x==0 else "ON",
                            horizontal=True)

run_btn = st.button("추천 생성", use_container_width=True,
                     type="primary")

st.divider()

if run_btn:
    # ── 현재 운영 예측 ────────────────────────────
    tou_now = get_tou(month_sel, current_hour)

    def predict_peak(prod, workers, hour, furnace, month):
        is_work = 1 if prod > 0 else 0
        is_day  = 1 if (8<=hour<=18) else 0
        tou     = get_tou(month, hour)
        tariff  = 109.8 if month in [1,2,11,12] else (191.6 if month in [6,7,8] else 167.2)
        smp     = {1:70.47,2:75.25,3:83.78,4:75.97,5:78.93,
                   6:82.72,7:87.04,8:93.41,9:98.21,
                   10:107.53,11:126.83,12:142.46}.get(month, 87.0)
        row = {
            "시간":hour,"생산량":prod,"가동여부":is_work,
            "공장인원":workers,"day":1,"d":15,"m":month,
            "weekday":0,"is_weekend":0,"is_holiday":0,
            "주간여부":is_day,"furnace_on":furnace,
            "기온":20,"습도":60,"풍속":2,"강수량":0,
            "solar_MJ":1.0,"전기요금(계절)":tariff,
            "tou_bucket":tou,"tou_price":TOU_PRICE[tou],
            "smp_land":smp,"인건비":1.5 if (8<=hour<=18) else 1.0,
            "co2_kg":0.0
        }
        df_row = pd.DataFrame([row])[feature_cols]
        return max(0, float(pipeline.predict(df_row)[0]))

    current_peak = predict_peak(target_prod, current_workers,
                                 current_hour, furnace_now, month_sel)
    current_usage = current_peak * (0.80 if target_prod>0 else 0.88)
    current_cost  = int(current_usage * TOU_PRICE[tou_now])

    # ── 추천안 생성 ───────────────────────────────
    # 추천 1: 경부하 시간대 이전 (22시)
    peak_off   = predict_peak(target_prod, current_workers,
                               22, furnace_now, month_sel)
    usage_off  = peak_off * 0.80
    cost_off   = int(usage_off * TOU_PRICE[0])  # 경부하

    # 추천 2: 인원 10% 감축
    rec_workers = max(1, int(current_workers * 0.9))
    peak_rec    = predict_peak(target_prod, rec_workers,
                                current_hour, furnace_now, month_sel)
    usage_rec   = peak_rec * 0.80
    cost_rec    = int(usage_rec * TOU_PRICE[tou_now])

    # 추천 3: 열처리로 OFF + 경부하 이전
    peak_best  = predict_peak(target_prod, rec_workers, 22, 0, month_sel)
    usage_best = peak_best * 0.80
    cost_best  = int(usage_best * TOU_PRICE[0])

    # ── 결과 표시 ─────────────────────────────────
    st.subheader("현재 vs 추천안 비교")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("현재 예측 피크", f"{current_peak:.1f} kW")
        st.metric("현재 시간 요금", f"{current_cost:,} 원")
    with col2:
        st.metric("추천 1 — 경부하 이전",
                  f"{peak_off:.1f} kW",
                  delta=f"{peak_off-current_peak:+.1f} kW")
        st.metric("절감액", f"{current_cost-cost_off:,} 원",
                  delta="경부하(22시) 이전 시")
    with col3:
        st.metric("추천 2 — 인원 10% 감축",
                  f"{peak_rec:.1f} kW",
                  delta=f"{peak_rec-current_peak:+.1f} kW")
        st.metric("절감액", f"{current_cost-cost_rec:,} 원",
                  delta=f"인원 {current_workers}→{rec_workers}명")
    with col4:
        st.metric("추천 3 — 최적 조합",
                  f"{peak_best:.1f} kW",
                  delta=f"{peak_best-current_peak:+.1f} kW")
        st.metric("절감액", f"{current_cost-cost_best:,} 원",
                  delta="경부하+인원감축+열처리로OFF")

    st.divider()

    # ── 추천 운영 타임라인 ────────────────────────
    st.subheader("추천 운영 타임라인 (시간대별 인원/피크)")
    hours   = list(range(24))
    current_peaks = [predict_peak(target_prod, current_workers,
                                   h, furnace_now, month_sel) for h in hours]
    rec_peaks     = [predict_peak(target_prod, rec_workers,
                                   h, 0, month_sel) for h in hours]

    fig, ax = plt.subplots(figsize=(14, 4))
    x = np.arange(24)
    w = 0.35
    ax.bar(x-w/2, current_peaks, w, color="#7F8C8D",
           alpha=0.8, label="현재", edgecolor="white")
    ax.bar(x+w/2, rec_peaks,     w, color="#2E86C1",
           alpha=0.8, label="추천", edgecolor="white")
    ax.axhline(150, color="#E74C3C", linestyle="--", lw=1.2, label="위험 150kW")
    ax.axhline(110, color="#F39C12", linestyle="--", lw=1.2, label="주의 110kW")
    ax.set_xlabel("시간 (시)")
    ax.set_ylabel("예측 피크 (kW)")
    ax.set_xticks(range(24))
    ax.legend(fontsize=9)
    ax.set_title("현재 vs 추천 — 24시간 피크 비교")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    st.divider()

    # ── 비용 비교 ─────────────────────────────────
    st.subheader("비용 비교 (현재 vs 추천 최적)")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**현재 운영**")
        daily_current = sum([
            int(predict_peak(target_prod, current_workers, h,
                             furnace_now, month_sel) * 0.80
                * TOU_PRICE[get_tou(month_sel, h)]) for h in range(24)
        ])
        st.metric("일간 전력량 요금", f"{daily_current:,} 원")
        monthly_basic = int(current_peak * DEMAND_CHARGE)
        st.metric("월 기본요금 (피크 기준)", f"{monthly_basic:,} 원")
        st.metric("합계", f"{daily_current + monthly_basic:,} 원")

    with col2:
        st.markdown("**추천 최적 운영**")
        daily_best = sum([
            int(predict_peak(target_prod, rec_workers, h,
                             0, month_sel) * 0.80
                * TOU_PRICE[get_tou(month_sel, h)]) for h in range(24)
        ])
        monthly_basic_best = int(peak_best * DEMAND_CHARGE)
        saving_total = (daily_current + monthly_basic) - (daily_best + monthly_basic_best)
        st.metric("일간 전력량 요금", f"{daily_best:,} 원",
                  delta=f"{daily_best-daily_current:,} 원")
        st.metric("월 기본요금 (피크 기준)", f"{monthly_basic_best:,} 원",
                  delta=f"{monthly_basic_best-monthly_basic:,} 원")
        st.metric("합계", f"{daily_best+monthly_basic_best:,} 원",
                  delta=f"절감액 {saving_total:,} 원")

st.caption("올라운더팀 | KAMP 자원 최적화 AI 프로젝트 2 | 2026")
