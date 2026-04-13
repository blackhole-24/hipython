# 🌅 모닝 체크리스트 — 글로벌 시장 아침 브리핑 서비스

> **한국 주식 투자자를 위한 펀드매니저급 아침 루틴 자동화 대시보드**  
> yfinance + LangChain + Streamlit으로 구현한 AI 글로벌 시장 모니터링 서비스

---

## 📌 프로젝트 개요

매일 아침 한국 주식 시장 개장(09:00) 전, **글로벌 야간 시장의 핵심 지표 23개**를 자동으로 수집하고  
AI(GPT-4o-mini)가 오늘 한국 시장 방향을 분석·해석해주는 Streamlit 기반 웹 대시보드입니다.

```
회사명/키워드 입력 → 글로벌 지표 자동 수집 → 신호등 판정 → AI 브리핑 생성
```

| 항목 | 내용 |
|---|---|
| 개발 기간 | 1일 (MVP) |
| 실행 환경 | Windows / Anaconda (langchain_rag_env) |
| 접속 주소 | http://localhost:8501 |
| 데이터 지연 | yfinance 기준 15분 지연 |

---

## 🗂 파일 구조

```
모닝_체크리스트/
│
├── app.py          ← Streamlit 메인 앱 (오케스트레이터)
├── data.py         ← 데이터 수집·처리·포맷 모듈
├── .env            ← API 키 보관 (OPENAI_API_KEY)
└── README.md
```

---

## 🗺 데이터 지도 (Data Flow)

서비스의 전체 데이터 흐름은 **3단계 파이프라인**으로 구성됩니다.

```
┌─────────────────────────────────────────────────────────────────────┐
│                      외부 데이터 소스 (yfinance)                      │
│                                                                     │
│  [선물 4종]     [달러·환율 3종]   [금리 2종]   [원자재 4종]           │
│  ES·NQ·YM·VIX  DXY·KRW·JPY      ^TNX·^IRX   WTI·금·구리·NG         │
│                                                                     │
│  [아시아·한국 5종]                [섹터 ETF 6종]                      │
│  KOSPI·KOSDAQ·닛케이·항셍·EWY     XLK·XLF·XLV·XLE·XLY·XLI          │
└─────────────────────────┬───────────────────────────────────────────┘
                          │  yf.download() 배치 호출 (threads=True)
                          ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      data.py — 처리 레이어                            │
│                                                                     │
│  ① TICKERS 설정 dict   → 23개 티커·섹션 정의 (수집 명세서)            │
│  ② get_all_data()      → yf.download() 배치 + _fetch_one() 폴백     │
│  ③ get_section()       → 섹션별 필터 반환 (futures/fx/rates...)      │
│  ④ fmt_price/delta()   → 티커별 단위·포맷 변환                       │
│  ⑤ @st.cache_data      → ttl=900 (15분 캐시, API 비용 절감)          │
│  ⑥ LangChain LCEL      → prompt | llm | StrOutputParser()           │
└─────────────────────────┬───────────────────────────────────────────┘
                          │  dict 반환 → app.py에서 import
                          ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      app.py — UI 출력 (Streamlit)                    │
│                                                                     │
│  ① 미국 선물·VIX    ② 달러·환율·금리    ③ 원자재                     │
│  ④ 한국·아시아     ⑤ 신호등 판정       ⑥ ETF 히트맵                  │
│  ⑦ AI 브리핑 (LangChain LCEL → GPT-4o-mini → 마크다운 출력)         │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🏗 시스템 아키텍처

```
┌──────────────────────────────────────────────┐
│          L1 — 사용자 브라우저                  │
│         localhost:8501 (Streamlit)            │
└────────────────────┬─────────────────────────┘
                     │ 요청 / 버튼 클릭
                     ▼
┌──────────────────────────────────────────────────────────────────────┐
│  L2 — Streamlit app.py (오케스트레이션)                               │
│                                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐   │
│  │  UI 렌더링    │  │  신호등 엔진  │  │  캐시 · 환경설정          │   │
│  │ show_metric()│  │ SIGNALS dict │  │  @st.cache_data          │   │
│  │ plotly 차트   │  │ get_signal() │  │  ttl=900 (15분)          │   │
│  │ 6개 섹션 구성 │  │ 🟢🟡🔴 판정 │  │  load_dotenv() → .env   │   │
│  │ invert 색반전 │  │ 종합 판정문  │  │  OPENAI_API_KEY 로드     │   │
│  └──────────────┘  └──────────────┘  └──────────────────────────┘   │
└───────────┬───────────────────────────────────────┬──────────────────┘
            │ from data import get_all_data          │ from langchain_openai
            ▼                                        ▼
┌─────────────────────────┐          ┌──────────────────────────────┐
│  L3a — data.py          │          │  L3b — ai/ (LangChain)       │
│                         │          │                              │
│  get_all_data()         │          │  ChatPromptTemplate          │
│  yf.download() 배치     │          │  ChatOpenAI                  │
│  _fetch_one() 폴백      │          │  (gpt-4o-mini, temp=0.3)     │
│  get_section() 필터     │          │  StrOutputParser()           │
│  fmt_price() 포맷       │          │  chain.invoke({snapshot})    │
└────────────┬────────────┘          └──────────────┬───────────────┘
             │ yfinance API 호출                      │ OpenAI REST 호출
             ▼                                        ▼
┌─────────────────────────┐          ┌──────────────────────────────┐
│  L4a — yfinance API     │          │  L4b — OpenAI API            │
│  23개 티커 수집           │          │  GPT-4o-mini                 │
│  5d/1d 배치 다운로드     │          │  마크다운 브리핑 반환          │
│  15분 지연 데이터         │          │  temperature=0.3             │
└─────────────────────────┘          └──────────────────────────────┘
```

---

## 📡 수집 지표 전체 목록 (23개)

### 미국 선물
| 티커 | 지표명 | 한국 시장 영향 |
|---|---|---|
| `ES=F` | S&P 500 선물 | KOSPI와 r=+0.87 (가장 강한 선행지표) |
| `NQ=F` | 나스닥 100 선물 | 반도체·IT주 직결, KOSDAQ r=+0.85 |
| `YM=F` | 다우존스 선물 | 전통 산업 심리 |
| `^VIX` | 공포지수 | KOSPI와 r=-0.79 (역방향), 20↑ 주의·30↑ 위험 |

### 달러·환율
| 티커 | 지표명 | 한국 시장 영향 |
|---|---|---|
| `DX-Y.NYB` | 달러인덱스 (DXY) | 원달러와 r=+0.89, 달러↑=외국인 이탈 |
| `KRW=X` | 원/달러 환율 | KOSPI 외국인 수급 핵심 결정 변수 |
| `JPY=X` | 달러/엔 환율 | 엔약세=한국 자동차·반도체 경쟁 압박 |

### 미국 국채 금리
| 티커 | 지표명 | 한국 시장 영향 |
|---|---|---|
| `^TNX` | 미 10년 국채금리 | 달러강세·원화약세 연쇄 (r=-0.55) |
| `^IRX` | 미 2년 국채금리 | Fed 금리 방향 선행 반영 |

### 원자재 선물
| 티커 | 지표명 | 한국 시장 영향 |
|---|---|---|
| `CL=F` | WTI 원유 | 한국 무역수지 직접 영향 |
| `GC=F` | 금 선물 | 안전자산 지표 |
| `HG=F` | 구리 선물 | 글로벌 경기 선행 (닥터 코퍼) |
| `NG=F` | 천연가스 | LNG 수입비용·한전 수익 연동 |

### 한국·아시아 지수
| 티커 | 지표명 | 비고 |
|---|---|---|
| `^KS11` | KOSPI | 15분 지연 |
| `^KQ11` | KOSDAQ | 15분 지연 |
| `^N225` | 닛케이 225 | 엔화와 함께 해석 필요 |
| `^HSI` | 항셍지수 | 중국 경기·대중 수출주 선행 |
| `EWY` | 한국 ETF (미국 상장) | 미국 야간 한국 전망 선행 지표 |

### 미국 섹터 ETF
`XLK` IT · `XLF` 금융 · `XLV` 헬스케어 · `XLE` 에너지 · `XLY` 소비재 · `XLI` 산업재

---

## 📊 화면 구성 (6개 섹션)

### Section 1 — 미국 야간 선물
```
[S&P500 선물]  [나스닥 선물]  [다우 선물]  [VIX 🟢안전/🟡보통/🟠주의/🔴위험]
```
- `show_metric()` 함수로 등락률 색상 자동 처리
- VIX는 절대값(15/20/30) 기준으로 상태 자동 판정

### Section 2 — 달러·환율·금리
```
[달러인덱스]  [원/달러]  [달러/엔]  [미 10년]  [미 2년]
```
- `invert=True` 파라미터: VIX·금리·원달러는 상승이 나쁨 → 색상 자동 반전

### Section 3 — 원자재
```
[WTI]  [금]  [구리]  [천연가스]
```

### Section 4 — 한국·아시아 지수
```
[KOSPI]  [KOSDAQ]  [닛케이]  [항셍]  [EWY 야간]
```

### Section 4-1 — 글로벌 × 한국 신호등 판정 ⭐
```
📡 오늘 한국장 영향 신호등

지표         상관계수    신호    현재 상태         해석
S&P500 선물  r=+0.87   🟢     +1.24% 상승 신호   미국 선물 = KOSPI 가장 강한 선행지표
VIX          r=-0.79   🟢     18.3 안전권        VIX 낮을수록 외국인 매수 유입
원/달러       r=-0.68   🟡     +0.12% 중립        원화 약세 = 외국인 매도 압력
미 10년 금리  r=-0.55   🟢     -2bp 우호적        금리 하락 = 달러 약세 신호
닛케이        r=+0.72   🟢     +0.8% 상승 신호    아시아 리스크온
항셍          r=+0.65   🟡     -0.3% 중립         중국 수출주 방향 확인 필요

→ 종합 판정: 🟢 오늘 한국장 상승 우호적 환경
```

**신호등 판정 로직:**
- `mode="change"` : 등락률 기준 판정 (선물, 환율, 지수)
- `mode="level"` : 절대값 기준 판정 (VIX: 20 미만=안전, 25 이상=위험)
- `invert=True` : 해당 지표가 하락할수록 한국에 긍정적인 경우

### Section 5 — 미국 섹터 ETF 히트맵
```
plotly Heatmap (zmid=0) → 0% 기준 빨강(하락) / 흰색(보합) / 초록(상승)
```
- `zmid=0` 핵심: 0%를 색상 중심으로 고정 → 절대 기준 시각화

### Section 6 — AI 오늘의 시장 브리핑 (LangChain)
```
[📝 AI 브리핑 생성 버튼]
→ 글로벌 지표 텍스트 직렬화 (snapshot)
→ ChatPromptTemplate + ChatOpenAI
→ StrOutputParser → st.markdown()
```

---

## 🔧 핵심 기술 스택

### data.py 핵심 설계

```python
# 1. 설정 레지스트리 — 티커·라벨·섹션을 하나의 딕셔너리로 관리
TICKERS = {
    "ES=F": {"label": "S&P500 선물", "section": "futures"},
    "^VIX": {"label": "VIX 공포지수", "section": "futures"},
    ...
}

# 2. 배치 다운로드 (속도 최적화)
raw = yf.download(
    tickers=all_tickers,
    period="5d",        # 전일 종가 비교용
    interval="1d",
    threads=True,       # 병렬 처리 → 23개를 3~5초에 처리
    progress=False,
)

# 3. 이중 안전망 — 배치 실패 시 개별 폴백
if raw is not None and ticker in raw:
    # 배치 데이터 사용
else:
    entry.update(_fetch_one(ticker))  # 개별 수집으로 전환

# 4. 등락률 계산 → LLM 컨텍스트의 핵심 재료
price      = float(closes.iloc[-1])
prev       = float(closes.iloc[-2])
change_pct = (price - prev) / prev * 100
```

### app.py 핵심 설계

```python
# 1. 캐시 전략 — 15분마다 자동 갱신
@st.cache_data(ttl=900)
def load_data():
    return get_all_data()

# 2. invert 파라미터 — VIX/금리는 오르면 나쁨
def show_metric(label, ticker, data, invert=False):
    st.metric(..., delta_color="inverse" if invert else "normal")

# 3. 신호등 판정 — 금융 도메인 지식을 딕셔너리로 코드화
SIGNALS = [
    {"ticker": "ES=F", "r": "r=+0.87", "mode": "change", "up": 0.3, "down": -0.3},
    {"ticker": "^VIX", "r": "r=-0.79", "mode": "level", "good": 20, "bad": 25, "invert": True},
    ...
]

# 4. LangChain LCEL 파이프라인 — 데이터를 텍스트로 직렬화 후 LLM 주입
snapshot = f"S&P500 선물: {fmt_price('ES=F', p)} ({fmt_delta(pct)})\n..."
chain = prompt | ChatOpenAI(model="gpt-4o-mini") | StrOutputParser()
response = chain.invoke({"snapshot": snapshot})
st.markdown(response)
```

---

## ⚡ 글로벌 × 한국 상관관계 TOP 5

| 순위 | 글로벌 지표 | 한국 지표 | 방향 | 상관계수 |
|---|---|---|---|---|
| 1 | S&P500 선물 (ES=F) | KOSPI | ↑↑ / ↓↓ | r=+0.87 |
| 2 | VIX 공포지수 | KOSPI / 외국인수급 | ↑↓ (역방향) | r=-0.79 |
| 3 | 나스닥 선물 (NQ=F) | KOSDAQ / 반도체 | ↑↑ / ↓↓ | r=+0.85 |
| 4 | 달러인덱스 (DXY) | 원달러 / 외국인 | ↑↓ (KOSPI) | r=+0.89 |
| 5 | 미 10년 국채금리 | 원달러 / KTB3Y | ↑↑ (환율) | r=+0.76 |

> **아침 브리핑 핵심 3가지**: ① ES 선물 등락률 ② VIX 수준 ③ 원달러 방향  
> 이 3개만 봐도 당일 한국장 방향 **70%** 예측 가능

---

## 🚀 설치 및 실행

### 1. 가상환경 활성화

```bash
conda activate langchain_rag_env
```

### 2. 패키지 설치

```bash
pip install streamlit yfinance pandas plotly langchain-openai openai python-dotenv
```

### 3. 환경변수 설정

`.env` 파일 생성:

```
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxx
```

### 4. 실행

```bash
cd 모닝_체크리스트_경로
streamlit run app.py
```

브라우저에서 http://localhost:8501 접속

---

## 🐛 주요 오류 및 해결법

| 오류 | 원인 | 해결 |
|---|---|---|
| `KeyError: 'OPENAI_API_KEY'` | .env 파일 없거나 키 이름 오타 | `.env` 파일 확인, `OPENAI_API_KEY` 정확한 표기 |
| `yfinance 데이터 None` | 장 마감 시간대 데이터 없음 | `_fetch_one()` 폴백 자동 실행, 정상 동작 |
| `plotly` ImportError | 패키지 미설치 | `app.py` 상단 `subprocess.run(pip install plotly)` 자동 처리 |
| AI 브리핑 오류 | API 키 만료 또는 잔액 부족 | OpenAI 콘솔에서 잔액 확인 |

---

## 📈 향후 확장 계획

- [ ] **Tab 1** — 포트폴리오 현황 (보유 종목 손익·수익률·베타)
- [ ] **Tab 2** — 아침 글로벌 체크 (현재 서비스 고도화)
- [ ] **Tab 3** — AI 종목 분석 (MeiliSearch + yfinance + ChatOpenAI)
- [ ] **Tab 4** — AI 아침 브리핑 (포트폴리오 연동)
- [ ] **한국은행 API** — 기준금리·국고채·CD금리 연동
- [ ] **FRED API** — 미국 CPI·고용 경제지표 연동
- [ ] **KRX 데이터포털** — 외국인·기관 순매수 수급 연동

---

## 📚 참고 자료

- [yfinance GitHub](https://github.com/ranaroussi/yfinance)
- [LangChain 공식 문서](https://python.langchain.com/)
- [Streamlit 공식 문서](https://docs.streamlit.io/)
- [Plotly 공식 문서](https://plotly.com/python/)

---

## ⚠️ 면책 조항

본 서비스는 **투자 참고용**이며, 제공되는 데이터는 15분 지연 데이터입니다.  
모든 투자 판단의 책임은 본인에게 있습니다.

---

*Made with ❤️ by blackhole-24 | 2026.04*
