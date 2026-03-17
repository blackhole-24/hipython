import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import matplotlib
import matplotlib.pyplot as plt

# ── 반드시 가장 먼저 호출 ─────────────────────────
st.set_page_config(
    page_title="에너지 피크 예측 시스템",
    page_icon="",
    layout="wide"
)

matplotlib.rcParams["font.family"]        = "Malgun Gothic"
matplotlib.rcParams["axes.unicode_minus"] = False

# ── 모델 로드 ─────────────────────────────────────
MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "energy_pipeline_v2.pkl")

@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)

loaded       = load_model()
pipeline     = loaded["pipeline"]
feature_cols = loaded["feature_cols"]

# ── 한전 TOU 요금 구간 함수 ───────────────────────
def get_tou_bucket(month, hour):
    if hour >= 22 or hour <= 7:
        return 0
    if month in [6,7,8]:
        if hour in [11,12,13,14,15,16,17]: return 2
        else: return 1
    elif month in [11,12,1,2]:
        if hour in [10,17,18,19,20]: return 2
        else: return 1
    else:
        return 1

TOU_PRICE    = {0: 95.7, 1: 121.5, 2: 155.0}
TOU_LABEL    = {0: "경부하 (95.7원/kWh)", 1: "중간부하 (121.5원/kWh)", 2: "최대부하 (155.0원/kWh)"}
EMISSION_FACTOR = 0.4153
MONTH_NAMES  = ["1월","2월","3월","4월","5월","6월","7월","8월","9월","10월","11월","12월"]
DAY_MAP      = {"월":1,"화":2,"수":3,"목":4,"금":5,"토":6,"일":7}
SMP_2021     = {1:70.47,2:75.25,3:83.78,4:75.97,5:78.93,
                6:82.72,7:87.04,8:93.41,9:98.21,10:107.53,11:126.83,12:142.46}
HOLIDAYS     = [20210101,20210212,20210301,20210505,20210519,
                20210606,20210815,20210920,20210921,20210922,20211003]

# ── 타이틀 ───────────────────────────────────────
st.title("제조 공장 피크 전력 예측 시스템")
st.caption("KAMP 자원 최적화 AI | Random Forest 모델 | 선박 부품 제조 공장 | 올라운더팀")
st.divider()

# ── 사이드바 입력 ─────────────────────────────────
st.sidebar.header("공정 파라미터 입력")
st.sidebar.caption("현장 조건을 입력하면 피크 전력을 예측합니다")
st.sidebar.divider()

st.sidebar.subheader("시간 / 날짜")
hour     = st.sidebar.slider("시간 (0~23시)", 0, 23, 10)
month    = st.sidebar.selectbox("월", MONTH_NAMES, index=4)
day_name = st.sidebar.selectbox("요일", list(DAY_MAP.keys()), index=0)
date_d   = st.sidebar.slider("일 (1~31)", 1, 31, 15)

st.sidebar.divider()
st.sidebar.subheader("생산 조건")
production = st.sidebar.slider("생산량", 0, 9830, 200, step=10)
workers    = st.sidebar.slider("공장 인원", 0.0, 48.0, 5.0, step=0.5)
labor_cost = st.sidebar.radio("근무 유형",
                               options=[1.0, 1.5],
                               format_func=lambda x: "주간 (1.0)" if x==1.0 else "야간 (1.5)",
                               index=1)

st.sidebar.divider()
st.sidebar.subheader("날씨 조건")
temperature = st.sidebar.slider("기온 (C)", -12, 34, 20)
humidity    = st.sidebar.slider("습도 (%)", 8, 98, 60)
wind_speed  = st.sidebar.slider("풍속 (m/s)", 0.0, 7.6, 2.0, step=0.1)
rainfall    = st.sidebar.slider("강수량 (mm)", 0.0, 122.4, 0.0, step=0.5)
solar       = st.sidebar.slider("일사량 (MJ/m2)", 0.0, 4.0, 1.0, step=0.1)

st.sidebar.divider()
st.sidebar.subheader("전기요금")
tariff_options = {
    "겨울 (109.8원/kWh)": 109.8,
    "봄가을 (167.2원/kWh)": 167.2,
    "여름 (191.6원/kWh)": 191.6,
}
season_label = st.sidebar.selectbox("계절별 단가", list(tariff_options.keys()), index=1)
tariff       = tariff_options[season_label]

# ── 입력값 계산 ───────────────────────────────────
m_num       = MONTH_NAMES.index(month) + 1
weekday_num = DAY_MAP[day_name] - 1
is_weekend  = 1 if weekday_num >= 5 else 0
is_holiday  = 1 if (int(f"2021{m_num:02d}{date_d:02d}") in HOLIDAYS) else 0
is_working  = 1 if production > 0 else 0
is_daytime  = 1 if (8 <= hour <= 18) else 0
tou         = get_tou_bucket(m_num, hour)
tou_price   = TOU_PRICE[tou]
smp         = SMP_2021.get(m_num, 87.0)

input_dict = {
    "시간"         : hour,
    "생산량"        : production,
    "가동여부"       : is_working,
    "공장인원"       : workers,
    "day"          : DAY_MAP[day_name],
    "d"            : date_d,
    "m"            : m_num,
    "weekday"      : weekday_num,
    "is_weekend"   : is_weekend,
    "is_holiday"   : is_holiday,
    "주간여부"       : is_daytime,
    "기온"          : temperature,
    "습도"          : humidity,
    "풍속"          : wind_speed,
    "강수량"         : rainfall,
    "solar_MJ"     : solar,
    "전기요금(계절)"  : tariff,
    "tou_bucket"   : tou,
    "tou_price"    : tou_price,
    "smp_land"     : smp,
    "인건비"         : labor_cost,
    "co2_kg"       : 0.0,
}

input_df = pd.DataFrame([input_dict])[feature_cols]
pred_kw   = float(pipeline.predict(input_df)[0])
pred_kw   = max(0, pred_kw)
co2_val   = round(pred_kw / 1000 * EMISSION_FACTOR * 1000, 4)

# ── 위험 등급 ─────────────────────────────────────
if pred_kw < 70:
    grade, color = "안전", "green"
elif pred_kw < 110:
    grade, color = "보통", "blue"
elif pred_kw < 150:
    grade, color = "주의", "orange"
else:
    grade, color = "위험", "red"

# ── KPI 카드 ──────────────────────────────────────
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("예측 피크전력", f"{pred_kw:.1f} kW",
              delta=f"{pred_kw-90:+.1f} kW (vs 평균 90kW)")
with col2:
    st.metric("위험 등급", grade)
with col3:
    st.metric("TOU 요금 구간", TOU_LABEL[tou])
with col4:
    st.metric("SMP 단가", f"{smp:.2f} 원/kWh")
with col5:
    st.metric("탄소 배출", f"{co2_val:.3f} kg CO2")

st.divider()

# ── 차트 ──────────────────────────────────────────
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("피크전력 게이지")
    fig, ax = plt.subplots(figsize=(6, 3))
    zones    = [70, 110, 150, 210]
    colors_z = ["#2ecc71","#3498db","#f39c12","#e74c3c"]
    prev = 0
    for z, c in zip(zones, colors_z):
        ax.barh(0, z-prev, left=prev, height=0.5, color=c, alpha=0.4)
        prev = z
    ax.axvline(pred_kw, color=color, linewidth=4, label=f"예측 {pred_kw:.1f}kW")
    ax.axvline(90, color="gray", linewidth=1.5, linestyle="--", label="평균 90kW")
    ax.set_xlim(0, 220)
    ax.set_yticks([])
    ax.set_xlabel("피크전력 (kW)")
    ax.legend()
    ax.set_title(f"현재 예측: {pred_kw:.1f} kW  [{grade}]")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col_right:
    st.subheader("24시간 시뮬레이션")
    hourly_preds = []
    for h in range(24):
        row = input_dict.copy()
        row["시간"]       = h
        row["주간여부"]    = 1 if (8 <= h <= 18) else 0
        row["tou_bucket"] = get_tou_bucket(m_num, h)
        row["tou_price"]  = TOU_PRICE[row["tou_bucket"]]
        df_h = pd.DataFrame([row])[feature_cols]
        hourly_preds.append(max(0, float(pipeline.predict(df_h)[0])))

    fig2, ax2 = plt.subplots(figsize=(6, 3))
    bar_cols = [color if h == hour else "steelblue" for h in range(24)]
    ax2.bar(range(24), hourly_preds, color=bar_cols, alpha=0.8, edgecolor="white")
    ax2.axhline(130, color="orange", linestyle="--", linewidth=1.5, label="고피크 130kW")
    ax2.axhline(90,  color="gray",   linestyle=":",  linewidth=1.2, label="평균 90kW")
    ax2.set_xlabel("시간 (시)")
    ax2.set_ylabel("예측 피크전력 (kW)")
    ax2.set_xticks(range(24))
    ax2.legend()
    ax2.set_title("24시간 피크전력 시뮬레이션")
    plt.tight_layout()
    st.pyplot(fig2)
    plt.close()

st.divider()

# ── 조치 가이드 ───────────────────────────────────
st.subheader("운영 조치 가이드")
if grade == "안전":
    st.success(f"안전 구간 — 현재 조건을 유지하세요. 예측 피크: {pred_kw:.1f}kW")
elif grade == "보통":
    st.info(f"보통 구간 — 정상 운영 중입니다. 예측 피크: {pred_kw:.1f}kW")
elif grade == "주의":
    st.warning(f"주의 구간 — 피크 상승 가능성. 예측 피크: {pred_kw:.1f}kW\n\n생산량 일부를 경부하(22시 이후)로 분산하세요.")
else:
    st.error(f"위험 구간 — 즉각 조치 필요! 예측 피크: {pred_kw:.1f}kW\n\n열처리로 추가 가동 중단 / 생산량 {int(production*0.8):,} 이하 조정 권장")

st.divider()

# ── ESG 탄소 배출 ─────────────────────────────────
st.subheader("ESG 탄소 배출 현황")
col_e1, col_e2, col_e3 = st.columns(3)
with col_e1:
    st.metric("시간당 탄소 배출", f"{co2_val:.3f} kg CO2")
with col_e2:
    st.metric("일간 예상 탄소 배출", f"{co2_val*24:.2f} kg CO2")
with col_e3:
    st.metric("연간 추정 탄소 배출", f"{co2_val*24*365/1000:.2f} tCO2")

with st.expander("현재 입력값 상세 보기"):
    display_df = pd.DataFrame({
        "항목": ["시간","월","일","요일","생산량","공장인원","근무유형",
                 "기온","습도","풍속","강수량","일사량","전기요금","TOU구간","SMP"],
        "입력값": [f"{hour}시", month, f"{date_d}일", day_name,
                  f"{production:,}", f"{workers:.1f}명",
                  "주간" if labor_cost==1.0 else "야간",
                  f"{temperature}C", f"{humidity}%",
                  f"{wind_speed}m/s", f"{rainfall}mm",
                  f"{solar}MJ/m2", f"{tariff}원/kWh",
                  TOU_LABEL[tou], f"{smp:.2f}원/kWh"]
    })
    st.dataframe(display_df, use_container_width=True, hide_index=True)

st.caption("올라운더팀 | KAMP 자원 최적화 AI 프로젝트 2 | 2026")
