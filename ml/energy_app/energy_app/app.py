import streamlit as st
import pandas as pd
import numpy as np
import joblib
import math
import os
import matplotlib
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="에너지 피크 예측 시스템",
    page_icon="⚡",
    layout="wide"
)

matplotlib.rcParams["font.family"]        = "Malgun Gothic"
matplotlib.rcParams["axes.unicode_minus"] = False

# ── 모델 로드 ─────────────────────────────────────
MODEL_PATH = os.path.join(
    os.path.dirname(__file__), "models", "energy_pipeline_v2.pkl")

@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)

loaded       = load_model()
model        = loaded["model"]
feature_cols = loaded["feature_cols"]

# ── 상수 ──────────────────────────────────────────
def get_tou(month, hour, is_holiday, is_weekend):
    if is_holiday or is_weekend:
        return 0, 95.7
    if month in [6,7,8]:
        if hour in [10,11,12,13,14,15,16,17]: return 2, 155.0
        if hour in [22,23,0,1,2,3,4,5]:       return 0, 95.7
        return 1, 121.5
    elif month in [11,12,1,2]:
        if hour in [9,10,17,18,19]:            return 2, 155.0
        if hour in [22,23,0,1,2,3,4,5]:        return 0, 95.7
        return 1, 121.5
    else:
        if hour in [10,11,12,13,14,15,16,17]:  return 1, 121.5
        if hour in [22,23,0,1,2,3,4,5]:        return 0, 95.7
        return 1, 121.5

TOU_LABEL = {0:"경부하(95.7원)", 1:"중간부하(121.5원)", 2:"최대부하(155.0원)"}
EMISSION  = 0.4153
MONTH_NAMES = ["1월","2월","3월","4월","5월","6월",
               "7월","8월","9월","10월","11월","12월"]
DAY_MAP = {"월":1,"화":2,"수":3,"목":4,"금":5,"토":6,"일":7}
SMP_2021 = {1:70.47,2:75.25,3:83.78,4:75.97,5:78.93,
            6:82.72,7:87.04,8:93.41,9:98.21,
            10:107.53,11:126.83,12:142.46}
NATIONAL_HOLIDAYS = [
    20210101,20210211,20210212,20210301,20210505,
    20210519,20210816,20210920,20210921,20210922,
    20211003,20211004,20211009,20211225,
]
SUMMER_VACATION = [
    20210731,20210801,20210802,20210803,20210804,
    20210805,20210806,20210807,20210808,
]
ALL_HOLIDAYS = set(NATIONAL_HOLIDAYS + SUMMER_VACATION)

GMM_LABEL = {
    0:"0 (비가동)",
    1:"1 (고생산)",
    2:"2 (중생산)",
    3:"3 (저생산)",
}
TARIFF_MAP = {
    "겨울 (109.8원/kWh)": 109.8,
    "봄가을 (167.2원/kWh)": 167.2,
    "여름 (191.6원/kWh)": 191.6,
}

# ── 타이틀 ───────────────────────────────────────
st.title("⚡ 제조 공장 피크 전력 예측 시스템")
st.caption("XGBoost-Tuned | Set_C | 올라운더팀 2026")
st.divider()

# ── 사이드바 ──────────────────────────────────────
st.sidebar.header("운영 조건 입력")
st.sidebar.divider()

st.sidebar.subheader("📅 날짜 · 시간")
hour     = st.sidebar.slider("시간 (0~23시)", 0, 23, 10)
month    = st.sidebar.selectbox("월", MONTH_NAMES, index=5)
day_name = st.sidebar.selectbox("요일", list(DAY_MAP.keys()), index=0)
date_d   = st.sidebar.slider("일 (1~31)", 1, 31, 15)

st.sidebar.divider()
st.sidebar.subheader("🏭 생산 조건")
production = st.sidebar.slider("생산량 (개)", 0, 9830, 500, step=10)
workers    = st.sidebar.slider("공장 인원 (명)", 0.0, 48.0, 10.0, step=0.5)
gmm_class  = st.sidebar.selectbox(
    "GMM 생산구분", options=[0,1,2,3],
    format_func=lambda x: GMM_LABEL[x], index=1)
furnace    = st.sidebar.radio(
    "열처리로 상태", options=[0,1],
    format_func=lambda x: "OFF (휴지)" if x==0 else "ON (가동)")
tariff_sel = st.sidebar.selectbox(
    "계절 요금", list(TARIFF_MAP.keys()), index=1)

st.sidebar.divider()
st.sidebar.subheader("🌤 날씨")
temperature = st.sidebar.slider("기온 (°C)", -20, 40, 20)
humidity    = st.sidebar.slider("습도 (%)", 0, 100, 60)
wind_speed  = st.sidebar.slider("풍속 (m/s)", 0.0, 10.0, 2.0, step=0.1)
rainfall    = st.sidebar.slider("강수량 (mm)", 0.0, 150.0, 0.0, step=0.5)

# ── 입력값 계산 ───────────────────────────────────
m_num      = MONTH_NAMES.index(month) + 1
wd_num     = DAY_MAP[day_name] - 1
is_weekend = 1 if wd_num >= 5 else 0
date_key   = int(f"2021{m_num:02d}{date_d:02d}")
is_holiday = 1 if date_key in ALL_HOLIDAYS else 0
is_work    = 1 if production > 0 else 0
is_day     = 1 if (8 <= hour <= 18) else 0
tou, tou_p = get_tou(m_num, hour, is_holiday, is_weekend)
smp        = SMP_2021.get(m_num, 87.0)
tariff     = TARIFF_MAP[tariff_sel]

# 인건비할증: 9~18시=1.0, 그외=1.5
labor = 1.0 if (9 <= hour <= 18) else 1.5

# log1p 변환
prod_log   = math.log1p(production)
worker_log = math.log1p(workers)
wind_log   = math.log1p(wind_speed)
rain_log   = math.log1p(rainfall)

input_dict = {
    "시간"        : hour,
    "day"         : DAY_MAP[day_name],
    "d"           : date_d,
    "m"           : m_num,
    "weekday"     : wd_num,
    "is_weekend"  : is_weekend,
    "is_holiday"  : is_holiday,
    "주간여부"     : is_day,
    "기온"         : temperature,
    "습도"         : humidity,
    "풍속"         : wind_log,
    "강수량"       : rain_log,
    "생산량"       : prod_log,
    "가동여부"     : is_work,
    "공장인원"     : worker_log,
    "GMM생산구분"  : gmm_class,
    "furnace_on"  : furnace,
    "전기요금(계절)": tariff,
    "tou_bucket"  : tou,
    "tou_price"   : tou_p,
    "smp_land"    : smp,
    "인건비"       : labor,
}

input_df = pd.DataFrame([input_dict])[feature_cols]
pred_kw  = max(0, float(model.predict(input_df)[0]))
co2_val  = round(pred_kw / 1000 * EMISSION * 1000, 3)
cost_won = int(pred_kw * tou_p)

if   pred_kw < 70:  grade, gcolor = "양호",  "green"
elif pred_kw < 110: grade, gcolor = "주의",  "blue"
elif pred_kw < 150: grade, gcolor = "위험",  "orange"
else:               grade, gcolor = "초과",  "red"

# ── 경보 배너 ────────────────────────────────────
if   pred_kw >= 150:
    st.error  (f"🔴 피크 초과 경보! {pred_kw:.1f} kW — 즉각 조치 필요")
elif pred_kw >= 110:
    st.warning(f"🟡 피크 위험 경보! {pred_kw:.1f} kW — 부하 분산 권고")
elif pred_kw >= 70:
    st.info   (f"🔵 피크 주의 구간. {pred_kw:.1f} kW")
else:
    st.success(f"🟢 양호 구간. {pred_kw:.1f} kW — 현재 조건 유지")

st.divider()

# ── KPI 카드 ─────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.metric("예측 피크",   f"{pred_kw:.1f} kW",
          delta=f"{pred_kw-90:+.1f} kW vs 평균")
c2.metric("위험 등급",   grade)
c3.metric("탄소 배출",   f"{co2_val:.3f} kg CO₂")
c4.metric("시간 요금",   f"{cost_won:,} 원")

st.divider()

# ── 24시간 시뮬레이션 ─────────────────────────────
st.subheader("📊 24시간 피크 시뮬레이션")
hourly_preds = []
for h in range(24):
    row = input_dict.copy()
    tou_h, tou_p_h = get_tou(m_num, h, is_holiday, is_weekend)
    row["시간"]      = h
    row["주간여부"]  = 1 if (8<=h<=18) else 0
    row["tou_bucket"]= tou_h
    row["tou_price"] = tou_p_h
    row["인건비"]    = 1.0 if (9<=h<=18) else 1.5
    df_h = pd.DataFrame([row])[feature_cols]
    hourly_preds.append(max(0, float(model.predict(df_h)[0])))

fig, ax = plt.subplots(figsize=(12, 4))
bar_cols = []
for h, v in enumerate(hourly_preds):
    if   v >= 150: bar_cols.append("#E74C3C")
    elif v >= 110: bar_cols.append("#F39C12")
    elif v >= 70:  bar_cols.append("#3498DB")
    else:          bar_cols.append("#2ECC71")

ax.bar(range(24), hourly_preds,
       color=bar_cols, edgecolor="white", alpha=0.85)
ax.axhline(150, color="#E74C3C", linestyle="--",
           lw=1.2, label="초과 150kW")
ax.axhline(110, color="#F39C12", linestyle="--",
           lw=1.2, label="위험 110kW")
ax.axhline(70,  color="#3498DB", linestyle="--",
           lw=1.2, label="주의 70kW")
ax.axvline(hour, color="black", linestyle="-",
           lw=2, alpha=0.5, label=f"현재 {hour}시")
ax.set_xlabel("시간 (시)")
ax.set_ylabel("예측 피크 (kW)")
ax.set_xticks(range(24))
ax.legend(fontsize=9)
ax.grid(alpha=0.3, axis="y")
plt.tight_layout()
st.pyplot(fig)
plt.close()

st.divider()

# ── 비용 절감 계산기 ─────────────────────────────
st.subheader("💰 비용 절감 계산기")
c1, c2, c3 = st.columns(3)
c1.metric("현재 시간 요금",  f"{cost_won:,} 원")
c2.metric("피크 10% 감축 시", f"{int(cost_won*0.10):,} 원 절감")
c3.metric("피크 20% 감축 시", f"{int(cost_won*0.20):,} 원 절감")

st.divider()

# ── 입력값 확인 ───────────────────────────────────
with st.expander("📋 현재 입력값 상세 보기"):
    display_df = pd.DataFrame({
        "항목": ["시간","월","일","요일","생산량","공장인원",
                 "GMM생산구분","열처리로","인건비할증",
                 "기온","습도","풍속","강수량","계절요금",
                 "TOU 구간","SMP","공휴일","주말"],
        "입력값": [
            f"{hour}시", month, f"{date_d}일", day_name,
            f"{production:,}개", f"{workers:.1f}명",
            GMM_LABEL[gmm_class],
            "ON" if furnace==1 else "OFF",
            f"{labor} ({'주간' if labor==1.0 else '야간'})",
            f"{temperature}°C", f"{humidity}%",
            f"{wind_speed}m/s", f"{rainfall}mm",
            f"{tariff}원/kWh",
            TOU_LABEL[tou], f"{smp:.2f}원/kWh",
            "예" if is_holiday else "아니오",
            "예" if is_weekend else "아니오",
        ],
    })
    st.dataframe(display_df, use_container_width=True,
                 hide_index=True)

st.caption("올라운더팀 | KAMP 자원 최적화 AI 프로젝트 2 | 2026")
