# ================================================================
# pages/tab1_dashboard.py
# 역할 : 피크 예측 대시보드 (Tab1)
# 의존 : predictor1.py, energy_pipeline_v4.pkl
# ================================================================

import streamlit as st
import pandas as pd
import numpy as np
import sys, os
import plotly.graph_objects as go

# predictor1.py 경로 등록 (energy_app 루트)
ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# ── 상수 ──────────────────────────────────────────────────────
SMP_2021 = {
    1:70.47, 2:75.25,  3:83.78,  4:75.97,  5:78.93,  6:82.72,
    7:87.04, 8:93.41,  9:98.21, 10:107.53, 11:126.83, 12:142.46
}
EMISSION   = 0.4781          # 환경부 고시 2022
BASIC_RATE = 8320            # 원/kW/월
TOU_LABEL  = {0:"경부하 (95.7원/kWh)",
              1:"중간부하 (121.5원/kWh)",
              2:"최대부하 (155.0원/kWh)"}
GMM_LABEL  = {0:"0 — 비가동", 1:"1 — 고생산",
              2:"2 — 중생산", 3:"3 — 저생산"}
MONTH_KR   = ["1월","2월","3월","4월","5월","6월",
              "7월","8월","9월","10월","11월","12월"]
DAY_KR     = {"월":1,"화":2,"수":3,"목":4,"금":5,"토":6,"일":7}
HOLIDAYS   = {
    20210101,20210211,20210212,20210301,20210505,
    20210519,20210816,20210920,20210921,20210922,
    20211003,20211009,20211225,
    20210731,20210801,20210802,20210803,20210804,
    20210805,20210806,20210807,20210808,
}

def get_tou(month, hour, is_holiday, is_weekend):
    if is_holiday or is_weekend:
        return 0, 95.7
    if month in [6,7,8]:
        if 10 <= hour <= 17:          return 2, 155.0
        if hour <= 5 or hour >= 22:   return 0, 95.7
        return 1, 121.5
    elif month in [11,12,1,2]:
        if hour in [9,10,17,18,19]:   return 2, 155.0
        if hour <= 5 or hour >= 22:   return 0, 95.7
        return 1, 121.5
    else:
        if 10 <= hour <= 17:          return 1, 121.5
        if hour <= 5 or hour >= 22:   return 0, 95.7
        return 1, 121.5

def get_grade(peak, th_c, th_w, th_d, th_e):
    if peak >= th_e: return "🔴 초과",  "#DC2626"
    if peak >= th_d: return "🟠 위험",  "#EA580C"
    if peak >= th_w: return "🟡 경고",  "#D97706"
    if peak >= th_c: return "🔵 수의",  "#2563EB"
    return                   "🟢 양호", "#059669"

def get_season(month):
    if month in [6,7,8]:    return "여름",  191.6
    if month in [11,12,1,2]: return "겨울", 109.8
    return                          "봄가을",167.2

# ── predictor1 로드 (없으면 Mock) ────────────────────────────
@st.cache_resource
def load_predictor():
    try:
        from predictor1 import predict
        return predict, True
    except Exception as e:
        return None, False

def mock_predict(hour, month, production, gmm, furnace):
    """predictor1.py 없을 때 시뮬레이션용"""
    base = 43.5
    if furnace == 1:
        if gmm == 1: base += 115 + production / 90
        elif gmm == 2: base += 68 + production / 130
        elif gmm == 3: base += 25 + production / 180
        else: base += 5
    if 9 <= hour <= 18: base *= 1.12
    return round(max(base, 20.0), 1)

def do_predict(predict_fn, using_real,
               month, day_d, hour, day_name,
               production, gmm, furnace,
               temperature, humidity, wind_speed, rainfall):
    """실제 or Mock 예측 수행 → {y1,y2,y3,y4} 반환"""
    is_weekend = 1 if DAY_KR[day_name] >= 6 else 0
    date_key   = int(f"2021{month:02d}{day_d:02d}")
    is_holiday = 1 if date_key in HOLIDAYS else 0

    if using_real:
        df_in = pd.DataFrame([{
            'Date':        f'2021-{month:02d}-{day_d:02d}',
            'hour':        hour,
            'temperature': temperature,
            'humidity':    humidity,
            'windspeed':   wind_speed,
            'rainfall':    rainfall,
            'op_code':     gmm,
            'output':      production,
            'weekday':     DAY_KR[day_name],
            'weekend':     is_weekend,
            'holiday':     is_holiday,
        }])
        res = predict_fn(df_in)
        r   = res['Set_C'][0]
        return r['y1'], r['y2'], r['y3'], r['y4'], is_weekend, is_holiday
    else:
        p = mock_predict(hour, month, production, gmm, furnace)
        return p, p*1.03, p*1.05, p*1.04, is_weekend, is_holiday

def do_predict_hour(predict_fn, using_real, h,
                    month, day_d, day_name,
                    production, gmm, furnace,
                    temperature, humidity, wind_speed, rainfall,
                    is_weekend, is_holiday):
    """24시간 시뮬용 — 시간만 바꿔 예측"""
    if using_real:
        df_h = pd.DataFrame([{
            'Date':        f'2021-{month:02d}-{day_d:02d}',
            'hour':        h,
            'temperature': temperature,
            'humidity':    humidity,
            'windspeed':   wind_speed,
            'rainfall':    rainfall,
            'op_code':     gmm,
            'output':      production,
            'weekday':     DAY_KR[day_name],
            'weekend':     is_weekend,
            'holiday':     is_holiday,
        }])
        return predict_fn(df_h)['Set_C'][0]['y1']
    else:
        return mock_predict(h, month, production, gmm, furnace)

# ══════════════════════════════════════════════════════════════
# 메인 렌더 함수
# ══════════════════════════════════════════════════════════════
def render():
    predict_fn, using_real = load_predictor()

    # ── 사이드바 ──────────────────────────────────────────────
    with st.sidebar:
        st.markdown("""
        <div style="background:#1E293B;color:#fff;border-radius:8px;
                    padding:10px 14px;margin-bottom:14px;font-size:13px;font-weight:700;">
            ⚡ 피크 예측 — 운영 조건
        </div>
        """, unsafe_allow_html=True)

        # 날짜·시간
        st.markdown("**📅 날짜 · 시간**")
        col_m, col_day = st.columns(2)
        with col_m:
            month = st.selectbox("월", range(1,13), index=6,
                format_func=lambda x: f"{x}월",
                key="t1_month",
                help="계절별 TOU 요금 자동 결정\n여름(6~8월)=191.6원 / 겨울(11~2월)=109.8원 / 봄가을=167.2원")
        with col_day:
            day_name = st.selectbox("요일", list(DAY_KR.keys()),
                key="t1_day",
                help="토·일은 경부하(95.7원) 요금 구간 적용")
        hour  = st.slider("시간 (0~23시)", 0, 23, 14, key="t1_hour",
                           help="주간(9~18시) 피크가 높게 예측됩니다")
        day_d = st.number_input("일", 1, 31, 15, key="t1_dayd",
                                 help="공휴일 여부 자동 판별에 사용")

        st.divider()

        # 생산 조건
        st.markdown("**🏭 생산 조건**")
        production = st.slider("생산량 (개)", 0, 9830, 500, step=10,
            key="t1_prod",
            help="📊 피크와의 상관계수 r=+0.526\n생산량 0 → 구분0(비가동) 자동 처리")
        gmm = st.selectbox("GMM 생산구분", [0,1,2,3],
            format_func=lambda x: GMM_LABEL[x],
            index=1, key="t1_gmm",
            help="0=비가동(기저 43.5kW)\n1=고생산(145~182kW)\n2=중생산(92~131kW)\n3=저생산(21~68kW)")
        furnace = st.radio("열처리로", [1, 0],
            format_func=lambda x: "🔥 ON (가동)" if x==1 else "⚫ OFF (휴지)",
            horizontal=True, key="t1_furnace",
            help="📊 가장 강한 피크 변수 r=+0.725\n비가동 시에도 43.5kW 기저전력 상시 소비")

        st.divider()

        # 날씨
        st.markdown("**🌤 날씨**")
        temperature = st.slider("기온 (°C)",  -20, 40, 28, key="t1_temp",
                                 help="r=+0.044 — 냉각 설비 가동에 영향")
        humidity    = st.slider("습도 (%)",    0, 100, 72, key="t1_hum",
                                 help="r=-0.090 — 높을수록 냉방 부하 증가")
        wind_speed  = st.slider("풍속 (m/s)", 0.0, 10.0, 2.1, step=0.1,
                                 key="t1_wind",
                                 help="r=+0.120 — log1p 변환 후 모델 입력")
        rainfall    = st.slider("강수량 (mm)", 0.0, 150.0, 0.0, step=0.5,
                                 key="t1_rain",
                                 help="r=-0.007 — 피크와 거의 무관, 날씨 맥락용")

        st.divider()

        # 경보 임계값
        st.markdown("**⚙️ 경보 임계값 (kW)**")
        st.caption("예측 피크가 이 값을 넘으면 경보 색상이 바뀝니다")
        c1, c2 = st.columns(2)
        with c1:
            th_c = st.number_input("🔵 수의",  0, 300,  70, key="t1_tc",
                                    help="수의 구간 임계값 (기본 70kW)")
            th_d = st.number_input("🟠 위험", 0, 300, 150, key="t1_td",
                                    help="위험 구간 임계값 (기본 150kW)")
        with c2:
            th_w = st.number_input("🟡 경고", 0, 300, 110, key="t1_tw",
                                    help="경고 구간 임계값 (기본 110kW)")
            th_e = st.number_input("🔴 초과", 0, 300, 180, key="t1_te",
                                    help="기본요금 결정 위험 구간 (기본 180kW)")

        st.divider()
        predict_btn = st.button("🔍 피크 예측 조회",
                                 type="primary",
                                 use_container_width=True,
                                 key="t1_btn")

    # ── 페이지 헤더 ───────────────────────────────────────────
    st.markdown("""
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:4px;">
        <div style="background:#1D4ED8;color:#fff;font-weight:700;
                    font-size:13px;padding:4px 10px;border-radius:6px;">EP</div>
        <span style="font-size:20px;font-weight:700;">피크 예측 대시보드</span>
    </div>
    """, unsafe_allow_html=True)
    st.caption("KAMP 자원 최적화 AI | 울산 볼트·너트 제조공장 | 올라운더팀 2026")

    if not using_real:
        st.warning("⚠️ predictor1.py 또는 energy_pipeline_v4.pkl 미연결 — **시뮬레이션 값**으로 표시됩니다.",
                   icon="⚠️")

    # ── 날씨 카드 + 임계값 (3:1 비율) ────────────────────────
    tou_b, tou_p = get_tou(month, hour,
                            1 if int(f"2021{month:02d}{day_d:02d}") in HOLIDAYS else 0,
                            1 if DAY_KR[day_name] >= 6 else 0)
    season_label, tariff_val = get_season(month)
    smp = SMP_2021.get(month, 87.0)
    is_hol = 1 if int(f"2021{month:02d}{day_d:02d}") in HOLIDAYS else 0
    is_wkd = 1 if DAY_KR[day_name] >= 6 else 0

    col_w, col_t = st.columns([3, 1])
    with col_w:
        hol_tag = "🚨 공휴일" if is_hol else ("🏖 주말" if is_wkd else "")
        st.markdown(f"""
        <div style="background:#fff;border:1px solid rgba(0,0,0,0.08);
                    border-radius:10px;padding:16px 20px;margin-bottom:12px;">
            <div style="font-size:13px;font-weight:500;margin-bottom:12px;
                        display:flex;justify-content:space-between;">
                <span>🌤 현재 날씨 입력값</span>
                <span style="font-size:11px;color:#94A3B8;">
                    기상청 WeatherForecast DB | 울산 지점 152
                </span>
            </div>
            <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;
                        text-align:center;">
                <div>
                    <div style="font-size:22px;">🌡️</div>
                    <div style="font-size:22px;font-weight:700;color:#2563EB;
                                font-family:monospace;">{temperature}</div>
                    <div style="font-size:11px;color:#94A3B8;">기온 (°C)</div>
                </div>
                <div>
                    <div style="font-size:22px;">💧</div>
                    <div style="font-size:22px;font-weight:700;color:#2563EB;
                                font-family:monospace;">{humidity}</div>
                    <div style="font-size:11px;color:#94A3B8;">습도 (%)</div>
                </div>
                <div>
                    <div style="font-size:22px;">💨</div>
                    <div style="font-size:22px;font-weight:700;color:#2563EB;
                                font-family:monospace;">{wind_speed}</div>
                    <div style="font-size:11px;color:#94A3B8;">풍속 (m/s)</div>
                </div>
                <div>
                    <div style="font-size:22px;">🌧️</div>
                    <div style="font-size:22px;font-weight:700;color:#2563EB;
                                font-family:monospace;">{rainfall}</div>
                    <div style="font-size:11px;color:#94A3B8;">강수량 (mm)</div>
                </div>
            </div>
            <div style="font-size:10px;color:#94A3B8;margin-top:10px;
                        padding-top:8px;border-top:1px solid rgba(0,0,0,0.06);">
                {month}월 {season_label} · 계절요금 {tariff_val}원/kWh ·
                TOU {TOU_LABEL[tou_b]} · SMP {smp}원/kWh
                {" · " + hol_tag if hol_tag else ""}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_t:
        st.markdown(f"""
        <div style="background:#fff;border:1px solid rgba(0,0,0,0.08);
                    border-radius:10px;padding:16px 18px;margin-bottom:12px;">
            <div style="font-size:12px;font-weight:500;margin-bottom:10px;">
                ⚙️ 경보 임계값
            </div>
            <div style="font-size:12px;color:#475569;line-height:2.1;">
                🔵 수의 &nbsp;<b>{th_c} kW</b><br>
                🟡 경고 &nbsp;<b>{th_w} kW</b><br>
                🟠 위험 &nbsp;<b>{th_d} kW</b><br>
                🔴 초과 &nbsp;<b>{th_e} kW</b>
            </div>
            <div style="font-size:10px;color:#94A3B8;margin-top:8px;">
                사이드바에서 조정
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── 예측 실행 ─────────────────────────────────────────────
    if predict_btn:
        with st.spinner("🔍 AI 피크 예측 중..."):
            p15, p30, p45, p60, is_weekend, is_holiday = do_predict(
                predict_fn, using_real,
                month, day_d, hour, day_name,
                production, gmm, furnace,
                temperature, humidity, wind_speed, rainfall
            )
        st.session_state["tab1_result"] = {
            "p15":p15, "p30":p30, "p45":p45, "p60":p60,
            "month":month, "day_d":day_d, "hour":hour,
            "day_name":day_name, "production":production,
            "gmm":gmm, "furnace":furnace,
            "temperature":temperature, "humidity":humidity,
            "wind_speed":wind_speed, "rainfall":rainfall,
            "is_weekend":is_weekend, "is_holiday":is_holiday,
            "tou_b":tou_b, "tou_p":tou_p,
        }
        # Tab3(운영 최적화)와 공유
        st.session_state["predicted_peak"] = p15
        st.session_state["predicted_month"] = month

    # ── 결과 표시 ─────────────────────────────────────────────
    if "tab1_result" not in st.session_state:
        # 초기 안내
        st.markdown("""
        <div style="text-align:center;padding:60px 20px;color:#94A3B8;">
            <div style="font-size:52px;margin-bottom:16px;">📊</div>
            <div style="font-size:16px;font-weight:500;color:#475569;margin-bottom:10px;">
                  왼쪽 사이드바에서 운영 조건을 설정하세요
            </div>
            <div style="font-size:13px;line-height:2.0;">
                월 · 시간 · 생산량 · GMM 생산구분 · 열처리로 상태를 입력하고<br>
                <b>🔍 피크 예측 조회</b> 버튼을 누르면 결과가 표시됩니다.
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    r   = st.session_state["tab1_result"]
    p15 = r["p15"]
    grade_label, grade_color = get_grade(p15, th_c, th_w, th_d, th_e)
    co2_val  = round(p15 / 1000 * EMISSION * 1000, 3)
    cost_val = int(p15 * r["tou_p"])
    save10   = int(p15 * 0.10 * BASIC_RATE / 730)
    save20   = int(p15 * 0.20 * BASIC_RATE / 730)

    # ── 경보 배너 ─────────────────────────────────────────────
    if p15 >= th_e:
        st.error(  f"🔴 **피크 초과 경보** — 즉각 조치 필요!  예측 피크: **{p15:.1f} kW**")
    elif p15 >= th_d:
        st.warning(f"🟠 **피크 위험 경보** — 부하 분산 권고.  예측 피크: **{p15:.1f} kW**")
    elif p15 >= th_w:
        st.info(   f"🟡 **피크 경고 구간**.  예측 피크: **{p15:.1f} kW**")
    elif p15 >= th_c:
        st.info(   f"🔵 **피크 수의 구간**.  예측 피크: **{p15:.1f} kW**")
    else:
        st.success(f"🟢 **양호 구간** — 현재 조건 유지.  예측 피크: **{p15:.1f} kW**")

    # ── KPI 카드 4개 ──────────────────────────────────────────
    k1, k2, k3, k4 = st.columns(4)
    k1.metric(
        "예측 피크 (15분)", f"{p15:.1f} kW",
        delta=f"{p15-90:+.1f} kW vs 평균(90kW)",
        help="XGBoost v4.pkl Set_C 22피처 예측\nR²=0.78 / RMSE=21.6kW")
    k2.metric(
        "피크 위험 등급", grade_label,
        help="사이드바 임계값 기준으로 자동 분류")
    k3.metric(
        "탄소 배출 (시간당)", f"{co2_val:.3f} kg CO₂",
        help=f"공식: 피크(kW) ÷ 1000 × {EMISSION} × 1000\nScope 2 간접 배출")
    k4.metric(
        "시간당 전기요금", f"{cost_val:,} 원",
        delta=f"TOU {TOU_LABEL[r['tou_b']]}",
        help="예측 피크 × TOU 단가\n경부하 95.7 / 중간 121.5 / 최대 155.0원")

    st.divider()

    # ── 24시간 차트 + 4타겟 상세 ─────────────────────────────
    col_chart, col_detail = st.columns([3, 2])

    with col_chart:
        st.markdown("**📊 24시간 피크 예측 추이**")

        with st.spinner("24시간 시뮬레이션 중..."):
            hourly = []
            for h in range(24):
                ph = do_predict_hour(
                    predict_fn, using_real, h,
                    r["month"], r["day_d"], r["day_name"],
                    r["production"], r["gmm"], r["furnace"],
                    r["temperature"], r["humidity"],
                    r["wind_speed"], r["rainfall"],
                    r["is_weekend"], r["is_holiday"]
                )
                hourly.append(max(0.0, ph))

        # 막대 색상 — 등급별
        bar_colors = []
        for v in hourly:
            if v >= th_e:   bar_colors.append("#DC2626")
            elif v >= th_d: bar_colors.append("#EA580C")
            elif v >= th_w: bar_colors.append("#D97706")
            elif v >= th_c: bar_colors.append("#2563EB")
            else:           bar_colors.append("#059669")

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=list(range(24)), y=hourly,
            marker_color=bar_colors,
            hovertemplate="<b>%{x}시</b><br>예측 피크: %{y:.1f} kW<extra></extra>"
        ))
        fig.add_hline(y=th_e, line_dash="dash",
                      line_color="#DC2626", line_width=1.2,
                      annotation_text=f"초과 {th_e}kW",
                      annotation_font_size=10,
                      annotation_position="bottom right")
        fig.add_hline(y=th_d, line_dash="dash",
                      line_color="#EA580C", line_width=1.2,
                      annotation_text=f"위험 {th_d}kW",
                      annotation_font_size=10,
                      annotation_position="bottom right")
        fig.add_vline(x=r["hour"], line_dash="dot",
                      line_color="#1D4ED8", line_width=1.5,
                      annotation_text=f"{r['hour']}시 (현재)",
                      annotation_font_size=10)
        fig.update_layout(
            height=240,
            margin=dict(l=0, r=0, t=8, b=0),
            plot_bgcolor="#F8FAFC",
            paper_bgcolor="#FFFFFF",
            xaxis=dict(title="시간", gridcolor="#E2E8F0",
                       tickmode="linear", dtick=2,
                       tickfont=dict(size=11)),
            yaxis=dict(title="피크 (kW)", gridcolor="#E2E8F0",
                       tickfont=dict(size=11)),
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_detail:
        st.markdown("**⚡ 4타겟 상세 예측**")
        d1, d2 = st.columns(2)
        d1.metric("15분 피크", f"{r['p15']:.1f} kW",
                   help="기본요금 산정 기준\nmodels['15분']['Set_C']")
        d2.metric("30분 피크", f"{r['p30']:.1f} kW",
                   help="설비 스케줄링 참고")
        d1.metric("45분 피크", f"{r['p45']:.1f} kW",
                   help="DR 발령 구간 파악용")
        d2.metric("60분 피크", f"{r['p60']:.1f} kW",
                   help="CBL 계산·DR 감축량 기준")

        st.divider()
        st.markdown("**💰 비용 절감 계산기**")
        st.markdown(f"""
        <div style="background:#F8FAFC;border:1px solid rgba(0,0,0,0.08);
                    border-radius:8px;padding:12px 14px;font-size:12px;">
            <div style="display:flex;justify-content:space-between;
                        padding:5px 0;border-bottom:1px solid rgba(0,0,0,0.06);">
                <span style="color:#475569;">현재 시간 요금</span>
                <b style="font-family:monospace;">{cost_val:,} 원</b>
            </div>
            <div style="display:flex;justify-content:space-between;
                        padding:5px 0;border-bottom:1px solid rgba(0,0,0,0.06);">
                <span style="color:#475569;">피크 10% 감축 시</span>
                <b style="color:#059669;font-family:monospace;">+{save10:,} 원 절감</b>
            </div>
            <div style="display:flex;justify-content:space-between;padding:5px 0;">
                <span style="color:#475569;">피크 20% 감축 시</span>
                <b style="color:#059669;font-family:monospace;">+{save20:,} 원 절감</b>
            </div>
        </div>
        <div style="font-size:10px;color:#94A3B8;margin-top:5px;">
            ※ 기본요금 {BASIC_RATE:,}원/kW/월 기준
        </div>
        """, unsafe_allow_html=True)

        # Tab3 연동 안내
        if "predicted_peak" in st.session_state:
            st.markdown(f"""
            <div style="background:rgba(5,150,105,0.08);border:1px solid rgba(5,150,105,0.25);
                        border-radius:6px;padding:8px 12px;margin-top:8px;font-size:11px;
                        color:#065F46;">
                ✅ 예측값 {p15:.1f}kW →
                <b>운영 최적화 탭</b>에 자동 연동됨
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    # ── ESG 탄소 배출 ──────────────────────────────────────────
    st.markdown("**🌿 ESG 탄소 배출 현황 (Scope 2)**")
    e1, e2, e3 = st.columns(3)
    e1.metric("시간당 CO₂",  f"{co2_val:.3f} kg",
               help=f"배출계수 {EMISSION} kgCO₂/kWh (환경부 고시 2022년)")
    e2.metric("일간 예상",    f"{co2_val*24:.2f} kg",
               help="현재 조건 24시간 유지 가정")
    e3.metric("연간 추정",    f"{co2_val*24*365/1000:.2f} tCO₂",
               help="GRI 302 ESG 탭에서 정밀 집계 가능")

    st.divider()

    # ── 입력값 확인 ───────────────────────────────────────────
    with st.expander("📋 현재 입력값 상세 보기"):
        disp = pd.DataFrame({
            "항목": ["월","시간","요일","일","생산량","GMM 생산구분",
                     "열처리로","기온","습도","풍속","강수량",
                     "계절 요금","TOU 구간","SMP","공휴일","주말"],
            "입력값": [
                f"{r['month']}월", f"{r['hour']}시",
                r["day_name"], f"{r['day_d']}일",
                f"{r['production']:,}개",
                GMM_LABEL[r["gmm"]],
                "🔥 ON" if r["furnace"]==1 else "⚫ OFF",
                f"{r['temperature']}°C", f"{r['humidity']}%",
                f"{r['wind_speed']}m/s", f"{r['rainfall']}mm",
                f"{tariff_val}원/kWh ({season_label})",
                TOU_LABEL[r["tou_b"]],
                f"{smp}원/kWh",
                "예" if r["is_holiday"] else "아니오",
                "예" if r["is_weekend"] else "아니오",
            ]
        })
        st.dataframe(disp, use_container_width=True, hide_index=True)

    st.caption("올라운더팀 | KAMP 자원 최적화 AI 프로젝트 2 | 2026")
