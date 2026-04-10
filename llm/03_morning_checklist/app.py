import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

from data import get_all_data, get_section, fmt_price, fmt_delta

# ── 페이지 설정 ────────────────────────────────────────────
st.set_page_config(
    page_title="🌅 모닝 체크리스트",
    page_icon="🌅",
    layout="wide",
)

st.title("🌅 모닝 체크리스트")
st.caption(f"마지막 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 데이터 출처: yfinance (15분 지연)")

if st.button("🔄 데이터 새로고침"):
    st.cache_data.clear()
    st.rerun()

st.divider()

# ── 데이터 수집 (15분 캐시) ────────────────────────────────
@st.cache_data(ttl=900)
def load_data():
    return get_all_data()

with st.spinner("📡 글로벌 시장 데이터 수집 중..."):
    data = load_data()

# ── 헬퍼: st.metric 색상 델타 ─────────────────────────────
def show_metric(label, ticker, data, invert=False):
    """st.metric 출력. invert=True이면 하락이 좋은 지표(VIX, 금리 등)"""
    d = data[ticker]
    price_str = fmt_price(ticker, d["price"])
    delta_str  = fmt_delta(d["change_pct"])
    st.metric(label=label, value=price_str, delta=delta_str,
              delta_color="inverse" if invert else "normal")


# ══════════════════════════════════════════════════════════
# SECTION 1 — 미국 야간 선물
# ══════════════════════════════════════════════════════════
st.subheader("🇺🇸 미국 야간 선물")
c1, c2, c3, c4 = st.columns(4)
with c1: show_metric("S&P500 선물", "ES=F", data)
with c2: show_metric("나스닥 선물", "NQ=F", data)
with c3: show_metric("다우 선물",   "YM=F", data)
with c4:
    vix = data["^VIX"]
    vix_val = vix["price"]
    if vix_val is not None:
        if vix_val < 15:
            vix_status = "🟢 안전"
        elif vix_val < 20:
            vix_status = "🟡 보통"
        elif vix_val < 30:
            vix_status = "🟠 주의"
        else:
            vix_status = "🔴 위험"
        st.metric(label=f"VIX 공포지수  {vix_status}",
                  value=f"{vix_val:.2f}",
                  delta=fmt_delta(vix["change_pct"]),
                  delta_color="inverse")
    else:
        st.metric("VIX 공포지수", "N/A")

st.divider()

# ══════════════════════════════════════════════════════════
# SECTION 2 — 달러 · 환율 · 금리
# ══════════════════════════════════════════════════════════
st.subheader("💵 달러 · 환율 · 금리")
c1, c2, c3, c4, c5 = st.columns(5)
with c1: show_metric("달러인덱스 (DXY)", "DX-Y.NYB", data)
with c2: show_metric("원 / 달러",        "KRW=X",    data, invert=True)
with c3: show_metric("달러 / 엔",        "JPY=X",    data)
with c4: show_metric("미 10년 금리",     "^TNX",     data, invert=True)
with c5: show_metric("미 2년 금리",      "^IRX",     data, invert=True)

st.divider()

# ══════════════════════════════════════════════════════════
# SECTION 3 — 원자재
# ══════════════════════════════════════════════════════════
st.subheader("🛢 원자재")
c1, c2, c3, c4 = st.columns(4)
with c1: show_metric("WTI 원유 ($)",  "CL=F", data)
with c2: show_metric("금 ($)",        "GC=F", data)
with c3: show_metric("구리 ($/lb)",   "HG=F", data)
with c4: show_metric("천연가스",      "NG=F", data)

st.divider()

# ══════════════════════════════════════════════════════════
# SECTION 4 — 한국 · 아시아 지수
# ══════════════════════════════════════════════════════════
st.subheader("🇰🇷 한국 · 아시아 지수")
c1, c2, c3, c4, c5 = st.columns(5)
with c1: show_metric("KOSPI",        "^KS11", data)
with c2: show_metric("KOSDAQ",       "^KQ11", data)
with c3: show_metric("닛케이 225",   "^N225", data)
with c4: show_metric("항셍 (홍콩)",  "^HSI",  data)
with c5: show_metric("EWY 야간 등락", "EWY",  data)

st.divider()

# ══════════════════════════════════════════════════════════
# SECTION 4-1 — 글로벌 × 한국 신호등
# ══════════════════════════════════════════════════════════
st.subheader("📡 오늘 한국장 영향 신호등")
st.caption("글로벌 지표 → KOSPI 상관관계 기반 방향 신호 (r값: 상관계수)")

SIGNALS = [
    {
        "ticker":  "ES=F",
        "label":   "S&P500 선물",
        "r":       "r=+0.87",
        "comment": "미국 선물 = KOSPI 가장 강한 선행지표",
        "mode":    "change",   # 등락률 기준
        "up":   0.3,           # 이 이상이면 🟢
        "down": -0.3,          # 이 이하면 🔴
    },
    {
        "ticker":  "^VIX",
        "label":   "VIX 공포지수",
        "r":       "r=-0.79",
        "comment": "VIX 낮을수록 외국인 매수 유입",
        "mode":    "level",    # 절대값 기준
        "good":    20,         # 이 미만이면 🟢
        "bad":     25,         # 이 이상이면 🔴
        "invert":  True,       # 낮을수록 좋음
    },
    {
        "ticker":  "KRW=X",
        "label":   "원 / 달러",
        "r":       "r=-0.68",
        "comment": "원화 약세(환율 상승) = 외국인 매도 압력",
        "mode":    "change",
        "up":   0.3,
        "down": -0.3,
        "invert":  True,       # 상승이 나쁨
    },
    {
        "ticker":  "^TNX",
        "label":   "미 10년 금리",
        "r":       "r=-0.55",
        "comment": "금리 상승 = 달러 강세 → 외국인 이탈",
        "mode":    "change",
        "up":   1.0,
        "down": -1.0,
        "invert":  True,
    },
    {
        "ticker":  "^N225",
        "label":   "닛케이 225",
        "r":       "r=+0.72",
        "comment": "닛케이 상승 = 아시아 리스크온",
        "mode":    "change",
        "up":   0.3,
        "down": -0.3,
    },
    {
        "ticker":  "^HSI",
        "label":   "항셍 (홍콩)",
        "r":       "r=+0.65",
        "comment": "항셍 상승 = 중국 수출주 수혜",
        "mode":    "change",
        "up":   0.3,
        "down": -0.3,
    },
]

def get_signal(sig_cfg, data):
    d = data.get(sig_cfg["ticker"], {})
    invert = sig_cfg.get("invert", False)

    if sig_cfg["mode"] == "change":
        val = d.get("change_pct")
        if val is None:
            return "⚪", "데이터 없음"
        if not invert:
            if val >= sig_cfg["up"]:   return "🟢", f"{val:+.2f}%  상승 신호"
            elif val <= sig_cfg["down"]: return "🔴", f"{val:+.2f}%  하락 신호"
            else:                        return "🟡", f"{val:+.2f}%  중립"
        else:
            if val <= -sig_cfg["up"]:  return "🟢", f"{val:+.2f}%  우호적"
            elif val >= sig_cfg["down"] * -1: return "🔴", f"{val:+.2f}%  주의"
            else:                       return "🟡", f"{val:+.2f}%  중립"

    elif sig_cfg["mode"] == "level":
        val = d.get("price")
        if val is None:
            return "⚪", "데이터 없음"
        if invert:
            if val < sig_cfg["good"]:  return "🟢", f"{val:.2f}  안전권"
            elif val >= sig_cfg["bad"]: return "🔴", f"{val:.2f}  위험권"
            else:                       return "🟡", f"{val:.2f}  주의권"
        else:
            if val >= sig_cfg["good"]: return "🟢", f"{val:.2f}  우호"
            elif val < sig_cfg["bad"]: return "🔴", f"{val:.2f}  위험"
            else:                      return "🟡", f"{val:.2f}  중립"

# 신호등 집계
green = red = yellow = 0
rows = []
for s in SIGNALS:
    icon, status = get_signal(s, data)
    rows.append((icon, s["label"], s["r"], status, s["comment"]))
    if icon == "🟢": green += 1
    elif icon == "🔴": red += 1
    else: yellow += 1

# 종합 판정
total = len(SIGNALS)
if green >= 4:
    overall = "🟢 오늘 한국장 **상승** 우호적 환경"
elif red >= 4:
    overall = "🔴 오늘 한국장 **하락** 위험 신호"
elif green > red:
    overall = "🟡 전반적으로 **소폭 상승** 가능성"
else:
    overall = "🟡 혼조세 — 방향성 불분명"

st.markdown(f"### {overall}")
st.caption("🟢 상승 &nbsp;|&nbsp; 🟡 중립 &nbsp;|&nbsp; 🔴 위험")
with st.expander("신호 집계 보기", expanded=False):
    st.markdown(f"🟢 상승/우호 **{green}개** &nbsp; 🟡 중립 **{yellow}개** &nbsp; 🔴 위험 **{red}개**")

cols = st.columns([1, 2, 2, 3, 4])
cols[0].markdown("**신호**")
cols[1].markdown("**지표**")
cols[2].markdown("**상관계수**")
cols[3].markdown("**현재 상태**")
cols[4].markdown("**해석**")

for icon, label, r, status, comment in rows:
    c0, c1, c2, c3, c4 = st.columns([1, 2, 2, 3, 4])
    c0.markdown(f"## {icon}")
    c1.markdown(f"**{label}**")
    c2.markdown(f"`{r}`")
    c3.markdown(status)
    c4.markdown(f"<span style='color:gray;font-size:0.85em'>{comment}</span>",
                unsafe_allow_html=True)

st.divider()

# ══════════════════════════════════════════════════════════
# SECTION 5 — 미국 섹터 ETF 히트맵
# ══════════════════════════════════════════════════════════
st.subheader("📊 미국 섹터 ETF 등락률")

sector_tickers = ["XLK", "XLF", "XLV", "XLE", "XLY", "XLI"]
sector_labels  = [data[t]["label"] for t in sector_tickers]
sector_values  = [data[t]["change_pct"] if data[t]["change_pct"] is not None else 0.0
                  for t in sector_tickers]

# plotly 히트맵 (1행)
fig = go.Figure(go.Heatmap(
    z=[sector_values],
    x=sector_labels,
    y=["등락률 (%)"],
    colorscale=[
        [0.0,  "#d73027"],
        [0.4,  "#f46d43"],
        [0.499,"#fee08b"],
        [0.5,  "#f7f7f7"],
        [0.501,"#d9ef8b"],
        [0.6,  "#66bd63"],
        [1.0,  "#1a9850"],
    ],
    zmid=0,
    text=[[f"{v:+.2f}%" for v in sector_values]],
    texttemplate="%{text}",
    showscale=True,
    colorbar=dict(title="등락%", thickness=15),
))
fig.update_layout(
    height=160,
    margin=dict(l=10, r=10, t=10, b=10),
    font=dict(size=13),
)
st.plotly_chart(fig, use_container_width=True)

st.divider()

# ══════════════════════════════════════════════════════════
# SECTION 6 — AI 오늘의 한줄 요약
# ══════════════════════════════════════════════════════════
st.subheader("🤖 AI 오늘의 시장 브리핑")

if st.button("📝 AI 브리핑 생성", type="primary"):
    openai_key = os.getenv("OPENAI_API_KEY", "")
    if not openai_key:
        st.error("OPENAI_API_KEY가 .env에 없습니다.")
    else:
        try:
            from langchain_openai import ChatOpenAI
            from langchain_core.prompts import ChatPromptTemplate
            from langchain_core.output_parsers import StrOutputParser

            # 데이터 요약 텍스트 생성
            def snap(ticker, d):
                p = d[ticker]
                return f"{p['label']}: {fmt_price(ticker, p['price'])} ({fmt_delta(p['change_pct'])})"

            snapshot = "\n".join([
                "=== 미국 선물 ===",
                snap("ES=F",  data), snap("NQ=F", data), snap("YM=F", data),
                snap("^VIX",  data),
                "=== 달러·환율·금리 ===",
                snap("DX-Y.NYB", data), snap("KRW=X", data), snap("JPY=X", data),
                snap("^TNX", data), snap("^IRX", data),
                "=== 원자재 ===",
                snap("CL=F", data), snap("GC=F", data), snap("HG=F", data),
                "=== 한국·아시아 ===",
                snap("^KS11", data), snap("^KQ11", data),
                snap("^N225", data), snap("^HSI",  data), snap("EWY", data),
            ])

            prompt = ChatPromptTemplate.from_messages([
                ("system", "당신은 한국 주식 투자자를 위한 시장 브리핑 전문가입니다. 핵심만 간결하게 한국어로 작성합니다."),
                ("user", """아래 글로벌 시장 현황을 바탕으로 마크다운 형식의 아침 브리핑을 작성해주세요.

{snapshot}

다음 3개 섹션으로 작성:
1. **오늘의 글로벌 시장 요약** (3문장)
2. **한국 시장 예상 방향** (2문장, KOSPI·KOSDAQ 방향성)
3. **오늘 반드시 체크할 것** (3가지 bullet)"""),
            ])

            llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
            chain = prompt | llm | StrOutputParser()

            with st.spinner("AI 브리핑 생성 중..."):
                response = chain.invoke({"snapshot": snapshot})
            st.markdown(response)

        except Exception as e:
            st.error(f"AI 브리핑 오류: {e}")
else:
    st.info("위 버튼을 클릭하면 현재 글로벌 시장 데이터를 기반으로 AI 브리핑을 생성합니다.")

st.divider()
st.caption("⚠️ 본 서비스는 투자 참고용이며, 투자 판단의 책임은 본인에게 있습니다.")
