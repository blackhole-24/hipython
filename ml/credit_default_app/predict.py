import joblib
import numpy as np
import pandas as pd
from pathlib import Path

# 모델 로드 (모듈 임포트 시 1회만 실행)
MODEL_PATH = Path(__file__).parent / 'models' / 'credit_default_pipeline.pkl'
pipeline   = joblib.load(MODEL_PATH)

# 피처 순서 (학습 시와 동일하게 유지)
FEATURE_COLS = [
    'LIMIT_BAL', 'SEX', 'EDUCATION', 'MARRIAGE', 'AGE',
    'PAY_0', 'PAY_2', 'PAY_3', 'PAY_4', 'PAY_5', 'PAY_6',
    'BILL_AMT1', 'BILL_AMT2', 'BILL_AMT3', 'BILL_AMT4', 'BILL_AMT5', 'BILL_AMT6',
    'PAY_AMT1',  'PAY_AMT2',  'PAY_AMT3',  'PAY_AMT4',  'PAY_AMT5',  'PAY_AMT6',
]


def preprocess(input_dict: dict) -> pd.DataFrame:
    """
    사용자 입력값 전처리
    - EDUCATION : 미정의값(0, 5, 6) → 4(기타)
    - MARRIAGE  : 미정의값(0)       → 3(기타)
    """
    df = pd.DataFrame([input_dict], columns=FEATURE_COLS)
    df['EDUCATION'] = df['EDUCATION'].replace({0: 4, 5: 4, 6: 4})
    df['MARRIAGE']  = df['MARRIAGE'].replace({0: 3})
    return df


def predict(input_dict: dict, threshold: float = 0.5) -> dict:
    """
    채무불이행 예측

    Parameters
    ----------
    input_dict : 피처명-값 딕셔너리 (FEATURE_COLS 기준)
    threshold  : 채무불이행 판정 임계값 (기본 0.5)

    Returns
    -------
    {
        'probability' : float,  채무불이행 확률 (0~1)
        'prediction'  : int,    0=정상 / 1=채무불이행
        'label'       : str,    '정상' / '채무불이행'
        'threshold'   : float,  적용된 임계값
    }
    """
    X   = preprocess(input_dict)
    prob = pipeline.predict_proba(X)[0, 1]
    pred = int(prob >= threshold)

    return {
        'probability': round(float(prob), 4),
        'prediction' : pred,
        'label'      : '채무불이행' if pred == 1 else '정상',
        'threshold'  : threshold,
    }
