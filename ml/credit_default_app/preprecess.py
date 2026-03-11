import pandas as pd

# 모델 학습 시 사용한 피처 순서 (23개)
FEATURE_COLS = [
    'LIMIT_BAL', 'SEX', 'EDUCATION', 'MARRIAGE', 'AGE',
    'PAY_0', 'PAY_2', 'PAY_3', 'PAY_4', 'PAY_5', 'PAY_6',
    'BILL_AMT1', 'BILL_AMT2', 'BILL_AMT3', 'BILL_AMT4', 'BILL_AMT5', 'BILL_AMT6',
    'PAY_AMT1', 'PAY_AMT2', 'PAY_AMT3', 'PAY_AMT4', 'PAY_AMT5', 'PAY_AMT6'
]

def prepare_input(user_input: dict) -> pd.DataFrame:
    """사용자 입력값을 모델 입력 형식으로 변환"""
    df = pd.DataFrame([user_input], columns=FEATURE_COLS)
    
    # 이상코드 통합 (학습 시와 동일한 전처리)
    df['EDUCATION'] = df['EDUCATION'].replace({0: 4, 5: 4, 6: 4})
    df['MARRIAGE']  = df['MARRIAGE'].replace({0: 3})
    
    return df[FEATURE_COLS]


def get_risk_level(prob: float) -> dict:
    """채무불이행 확률 → 위험등급 변환"""
    if prob < 0.2:
        return {"level": "낮음",     "icon": "🟢", "color": "#27AE60"}
    elif prob < 0.4:
        return {"level": "주의",     "icon": "🟡", "color": "#F39C12"}
    elif prob < 0.6:
        return {"level": "위험",     "icon": "🔴", "color": "#E74C3C"}
    else:
        return {"level": "매우위험", "icon": "🚨", "color": "#922B21"}

