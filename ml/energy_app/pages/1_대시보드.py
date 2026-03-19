import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import joblib, os

matplotlib.rcParams["font.family"]        = "Malgun Gothic"
matplotlib.rcParams["axes.unicode_minus"] = False

# ── 데이터 로드 ───────────────────────────────────
BASE = os.path.dirname(os.path.dirname(__file__))

@st.cache_data
def load_power():
    path = os.path.join(BASE, "data", "okm_power_usage.csv")
    return pd.read_csv(path)

@st.cache_resource
def load_model():
    path = os.path.join(BASE, "models", "energy_pipeline_v2.pkl")
    return joblib.load(path)

df_power = load_power()
loaded   = load_model()
pipeline     = loaded["pipeline"]
feature_cols = loaded["feature_cols"]

# ── 상수 ─────────────────────────────────────────
MONTH_NAMES = ["1월","2월","3월","4월","5월","6월",
               "7월","8월","9월","10월","11월","12월"]
DAY_MAP     = {"월":1,"화":2,"수":3,"목":4,"금":5,"토":6,"일":7}
SMP_2021    = {1:70.47,2:75.25,3:83.78,4:75.97,5:78.93,
               6:82.72,7:87.04,8:93.41,9:98.21,
               10:107.53,11:126.83,12:142.46}
HOLIDAYS    = [20210101,20210212,20210301,20210505,20210519,
               20210606,20210815,20210920,20210921,20210922,20211003]
TOU_PRICE   = {0:95.7, 1:121.5, 2:155.0}
TOU_LABEL   = {0:"경부하(95.7원)", 1:"중간부하(121.5원)", 2:"최대부하(155.0원)"}
EMISSION_FACTOR = 0.4153

def get_tou(month, hour):
    if hour >= 22 or hour <= 7: return 0
    if month in [6,7,8]:
        return 2 if hour in [11,12,13,14,15,16,17] else 1
    elif month in [11,12,1,2]:
        return 2 if hour in [10,17,18,19,20] else 1
    return 1

# ── 사이드바 입력 ─────────────────────────────────
st.sidebar.title("EP 에너지 피크 예측")
st.sidebar.caption("제조 전력 피크 예측 · 자원 최적화 PoC")
st.sidebar.divider()

st.sidebar.subheader("운영 조건 입력")
month    = st.sidebar.selectbox("월", MONTH_NAMES, index=5)
day_name = st.sidebar.selectbox("요일", list(DAY_MAP.keys()), index=0)
date_d   = st.sidebar.slider("일", 1, 31, 15)
hour     = st.sidebar.slider("시간", 0, 23, 10)

st.sidebar.divider()
production = st.sidebar.slider("생산량 (개)", 0, 9830, 500, step=10)
workers    = st.sidebar.slider("공장 인원 (명)", 0.0, 48.0, 10.0, step=0.5)
furnace    = st.sidebar.radio("열처리로", [0,1],
                               format_func=lambda x: "OFF" if x==0 else "ON")
labor      = st.sidebar.radio("근무 유형",
                               [1.0,1.5],
                               format_func=lambda x: "주간(1.0)" if x==1.0 else "야간(1.5)")

st.sidebar.divider()
temperature = st.sidebar.slider("기온 (°C)", -20, 40, 20)
humidity    = st.sidebar.slider("습도 (%)", 0, 100, 60)
wind_speed  = st.sidebar.slider("풍속 (m/s)", 0.0, 10.0, 2.0, step=0.1)
rainfall    = st.sidebar.slider("강수량 (mm)", 0.0, 150.0, 0.0, step=0.5)
solar       = st.sidebar.slider("일사량 (MJ/m2)", 0.0, 4.0, 1.0, step=0.1)

tariff_map  = {"겨울(109.8원)":109.8, "봄가을(167.2원)":167.2, "여름(191.6원)":191.6}
season      = st.sidebar.selectbox("전기요금 계절", list(tariff_map.keys()), index=1)
tariff      = tariff_map[season]

# ── 입력 계산 ─────────────────────────────────────
m_num      = MONTH_NAMES.index(month) + 1
wd_num     = DAY_MAP[day_name] - 1
is_weekend = 1 if wd_num >= 5 else 0
is_holiday = 1 if int(f"2021{m_num:02d}{date_d:02d}") in HOLIDAYS else 0
is_work    = 1 if production > 0 else 0
is_day     = 1 if (8<=hour<=18) else 0
tou        = get_tou(m_num, hour)
smp        = SMP_2021.get(m_num, 87.0)

input_dict = {
    "시간":hour, "생산량":production, "가동여부":is_work,
    "공장인원":workers, "day":DAY_MAP[day_name], "d":date_d,
    "m":m_num, "weekday":wd_num, "is_weekend":is_weekend,
    "is_holiday":is_holiday, "주간여부":is_day,
    "furnace_on":furnace, "기온":temperature, "습도":humidity,
    "풍속":wind_speed, "강수량":rainfall, "solar_MJ":solar,
    "전기요금(계절)":tariff, "tou_bucket":tou,
    "tou_price":TOU_PRICE[tou], "smp_land":smp,
    "인건비":labor, "co2_kg":0.0,
}

input_df = pd.DataFrame([input_dict])[feature_cols]
pred_kw  = max(0, float(pipeline.predict(input_df)[0]))
usage_kwh = pred_kw * 0.80 if production > 0 else (
            pred_kw * 0.88 if pred_kw >= 60 else pred_kw * 0.92)
cost_now  = int(usage_kwh * TOU_PRICE[tou])
co2_val   = round(pred_kw / 1000 * EMISSION_FACTOR * 1000, 3)
saving_10 = int(cost_now * 0.10)
saving_20 = int(cost_now * 0.20)

# 위험 등급
if pred_kw < 70:
    grade, gcolor = "양호", "#2ECC71"
elif pred_kw < 110:
    grade, gcolor = "주의", "#3498DB"
elif pred_kw < 150:
    grade, gcolor = "위험", "#F39C12"
else:
    grade, gcolor = "초과", "#E74C3C"

# ── 메인 화면 ─────────────────────────────────────
st.title("메인 대시보드")
st.caption(f"XGBoost | Set_C (23개 피처) | 2021년 1년치 학습 데이터")

# 피크 위험 경보
if pred_kw >= 150:
    st.error(f"""피크 위험 경보 — 즉시 조치 필요
위험 시간대: {hour:02d}:00 ~ {hour+1:02d}:00  |  위험 수준: {grade}  |  예측 피크: {pred_kw:.1f} kW""")
elif pred_kw >= 110:
    st.warning(f"""피크 주의 경보
위험 시간대: {hour:02d}:00 ~ {hour+1:02d}:00  |  위험 수준: {grade}  |  예측 피크: {pred_kw:.1f} kW""")

st.divider()

# KPI 카드 4개
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("현재 전력 사용량", f"{usage_kwh:.1f} kWh",
              delta=f"{usage_kwh-70:+.1f} kWh vs 평균")
with col2:
    st.metric("예측 피크 (향후 1h)", f"{pred_kw:.1f} kW",
              delta=grade, delta_color="inverse" if pred_kw>110 else "normal")
with col3:
    st.metric("피크 위험 등급", grade)
with col4:
    st.metric("예상 절감 가능액", f"{saving_20:,} 원",
              delta=f"피크 20% 감축 시")

st.divider()

# 게이지 + 24h 시뮬레이션
col_l, col_r = st.columns(2)

with col_l:
    st.subheader("피크 위험 게이지")
    fig, ax = plt.subplots(figsize=(6,3))
    zones   = [70,110,150,210]
    zcolors = ["#2ECC71","#3498DB","#F39C12","#E74C3C"]
    zlabels = ["양호","주의","위험","초과"]
    prev = 0
    for z,c,l in zip(zones, zcolors, zlabels):
        ax.barh(0, z-prev, left=prev, height=0.5, color=c, alpha=0.4, label=l)
        prev = z
    ax.axvline(pred_kw, color=gcolor, linewidth=4, label=f"예측 {pred_kw:.1f}kW")
    ax.axvline(90, color="gray", linewidth=1.5, linestyle="--", label="평균 90kW")
    ax.set_xlim(0,220); ax.set_yticks([])
    ax.set_xlabel("피크전력 (kW)")
    ax.legend(loc="upper left", fontsize=8)
    ax.set_title(f"현재: {pred_kw:.1f}kW [{grade}]")
    plt.tight_layout(); st.pyplot(fig); plt.close()

with col_r:
    st.subheader("24시간 전력 시뮬레이션")
    hourly = []
    for h in range(24):
        row = input_dict.copy()
        row["시간"]       = h
        row["주간여부"]    = 1 if (8<=h<=18) else 0
        row["tou_bucket"] = get_tou(m_num, h)
        row["tou_price"]  = TOU_PRICE[row["tou_bucket"]]
        row["co2_kg"]     = 0.0
        df_h = pd.DataFrame([row])[feature_cols]
        hourly.append(max(0, float(pipeline.predict(df_h)[0])))

    fig2, ax2 = plt.subplots(figsize=(6,3))
    bar_cols = [gcolor if h==hour else "steelblue" for h in range(24)]
    ax2.bar(range(24), hourly, color=bar_cols, alpha=0.8, edgecolor="white")
    ax2.axhline(150, color="#E74C3C", linestyle="--", lw=1.2, label="위험 150kW")
    ax2.axhline(110, color="#F39C12", linestyle="--", lw=1.2, label="주의 110kW")
    ax2.set_xlabel("시간"); ax2.set_ylabel("kW")
    ax2.set_xticks(range(24)); ax2.legend(fontsize=8)
    ax2.set_title("24시간 피크 예측")
    plt.tight_layout(); st.pyplot(fig2); plt.close()

st.divider()

# 운영 현황 요약
st.subheader("현재 운영 현황")
c1,c2,c3,c4 = st.columns(4)
with c1: st.metric("생산량", f"{production:,} 개")
with c2: st.metric("투입 인원", f"{workers:.0f} 명")
with c3: st.metric("전기요금 (계절)", season)
with c4: st.metric("날씨", f"{temperature}°C / 습도 {humidity}%")

st.divider()

# 비용 절감 계산기
st.subheader("비용 절감 예상 계산기")
c1,c2,c3 = st.columns(3)
with c1:
    st.metric("현재 시간 요금", f"{cost_now:,} 원")
with c2:
    st.metric("피크 10% 감축 시", f"{saving_10:,} 원 절감")
with c3:
    st.metric("피크 20% 감축 시", f"{saving_20:,} 원 절감")

# 탄소 배출
st.divider()
st.subheader("ESG 탄소 배출")
c1,c2,c3 = st.columns(3)
with c1: st.metric("시간당 CO2", f"{co2_val:.3f} kg")
with c2: st.metric("일간 예상", f"{co2_val*24:.2f} kg")
with c3: st.metric("연간 추정", f"{co2_val*24*365/1000:.2f} tCO2")

# 조치 가이드
st.divider()
st.subheader("운영 조치 가이드")
if grade == "양호":
    st.success(f"양호 구간 — 현재 조건을 유지하세요. 예측 피크: {pred_kw:.1f}kW")
elif grade == "주의":
    st.info(f"주의 구간 — 피크 상승 가능성. 예측 피크: {pred_kw:.1f}kW\n생산량 일부를 경부하(22시 이후)로 분산하세요.")
elif grade == "위험":
    st.warning(f"위험 구간 — 즉각 조치 필요. 예측 피크: {pred_kw:.1f}kW\n열처리로 가동 시점 재조정 및 설비 대기모드 전환하세요.")
else:
    st.error(f"초과 구간 — 긴급 조치! 예측 피크: {pred_kw:.1f}kW\n생산량 {int(production*0.8):,}개 이하 즉시 조정 권장.")

st.caption("올라운더팀 | KAMP 자원 최적화 AI 프로젝트 2 | 2026")
