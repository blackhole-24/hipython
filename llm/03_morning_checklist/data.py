import yfinance as yf
import pandas as pd
from datetime import datetime

# ── 티커 정의 ──────────────────────────────────────────────
TICKERS = {
    # 미국 선물
    "ES=F":      {"label": "S&P500 선물",   "section": "futures"},
    "NQ=F":      {"label": "나스닥 선물",    "section": "futures"},
    "YM=F":      {"label": "다우 선물",      "section": "futures"},
    "^VIX":      {"label": "VIX 공포지수",   "section": "futures"},
    # 달러·환율
    "DX-Y.NYB":  {"label": "달러인덱스",     "section": "fx"},
    "KRW=X":     {"label": "원/달러",        "section": "fx"},
    "JPY=X":     {"label": "달러/엔",        "section": "fx"},
    # 금리
    "^TNX":      {"label": "미 10년 금리",   "section": "rates"},
    "^IRX":      {"label": "미 2년 금리",    "section": "rates"},
    # 원자재
    "CL=F":      {"label": "WTI 원유",       "section": "commodities"},
    "GC=F":      {"label": "금",             "section": "commodities"},
    "HG=F":      {"label": "구리",           "section": "commodities"},
    "NG=F":      {"label": "천연가스",       "section": "commodities"},
    # 한국·아시아
    "^KS11":     {"label": "KOSPI",          "section": "asia"},
    "^KQ11":     {"label": "KOSDAQ",         "section": "asia"},
    "^N225":     {"label": "닛케이",         "section": "asia"},
    "^HSI":      {"label": "항셍",           "section": "asia"},
    "EWY":       {"label": "EWY(야간한국)",  "section": "asia"},
    # 미국 섹터 ETF
    "XLK":       {"label": "IT",             "section": "sectors"},
    "XLF":       {"label": "금융",           "section": "sectors"},
    "XLV":       {"label": "헬스케어",       "section": "sectors"},
    "XLE":       {"label": "에너지",         "section": "sectors"},
    "XLY":       {"label": "소비재",         "section": "sectors"},
    "XLI":       {"label": "산업재",         "section": "sectors"},
}

def _fetch_one(ticker: str) -> dict:
    """단일 티커 → 현재가·등락률 반환"""
    try:
        t = yf.Ticker(ticker)
        hist = t.history(period="2d", interval="1d")
        if len(hist) < 2:
            hist = t.history(period="5d", interval="1d")
        if len(hist) < 1:
            return {"price": None, "change": None, "change_pct": None}

        price = float(hist["Close"].iloc[-1])
        if len(hist) >= 2:
            prev  = float(hist["Close"].iloc[-2])
            change = price - prev
            change_pct = (change / prev) * 100 if prev != 0 else 0.0
        else:
            change = 0.0
            change_pct = 0.0

        return {"price": price, "change": change, "change_pct": change_pct}
    except Exception as e:
        return {"price": None, "change": None, "change_pct": None}


def get_all_data() -> dict:
    """
    전체 23개 지표 수집.
    반환 구조:
    {
      "ES=F": {"label": "S&P500 선물", "section": "futures",
               "price": 5100.0, "change": 12.0, "change_pct": 0.24},
      ...
    }
    """
    result = {}
    all_tickers = list(TICKERS.keys())

    # yfinance 한 번에 다운로드 (빠름)
    try:
        raw = yf.download(
            tickers=all_tickers,
            period="5d",
            interval="1d",
            group_by="ticker",
            auto_adjust=True,
            progress=False,
            threads=True,
        )
    except Exception:
        raw = None

    for ticker, meta in TICKERS.items():
        entry = {"label": meta["label"], "section": meta["section"],
                 "price": None, "change": None, "change_pct": None}
        try:
            if raw is not None and ticker in raw.columns.get_level_values(0):
                closes = raw[ticker]["Close"].dropna()
                if len(closes) >= 2:
                    price = float(closes.iloc[-1])
                    prev  = float(closes.iloc[-2])
                    change = price - prev
                    change_pct = (change / prev) * 100 if prev != 0 else 0.0
                    entry.update({"price": price, "change": change, "change_pct": change_pct})
                elif len(closes) == 1:
                    entry.update({"price": float(closes.iloc[-1]), "change": 0.0, "change_pct": 0.0})
            else:
                # 개별 fallback
                entry.update(_fetch_one(ticker))
        except Exception:
            entry.update(_fetch_one(ticker))

        result[ticker] = entry

    return result


def get_section(data: dict, section: str) -> dict:
    """섹션별 필터링"""
    return {k: v for k, v in data.items() if v["section"] == section}


def fmt_price(ticker: str, price) -> str:
    """티커별 가격 포맷"""
    if price is None:
        return "N/A"
    if ticker in ("^TNX", "^IRX", "^TYX"):
        return f"{price:.2f}%"
    if ticker == "KRW=X":
        return f"₩{price:,.1f}"
    if ticker in ("^KS11", "^KQ11", "^N225", "^HSI"):
        return f"{price:,.0f}"
    if ticker == "HG=F":
        return f"${price:.3f}"
    return f"{price:,.2f}"


def fmt_delta(change_pct) -> str:
    if change_pct is None:
        return ""
    sign = "+" if change_pct >= 0 else ""
    return f"{sign}{change_pct:.2f}%"
