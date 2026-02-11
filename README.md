# 월마트 고객 데이터 분석 프로젝트

## 프로젝트 개요

본 프로젝트는 월마트의 약 55만 건의 거래 데이터를 분석하여 **핵심 매출 기여 고객층(Cash Cow)**을 식별하고, 해당 고객층이 선호하는 **베스트셀러 상품(Best Seller)**을 발굴하는 데이터 분석 프로젝트입니다. 성별과 연령대를 기준으로 고객을 세분화하여 매출 기여도가 가장 높은 세그먼트를 도출하고, 이를 바탕으로 효과적인 마케팅 전략을 제시합니다.

**주요 분석 내용:**
- 성별과 연령대 조합을 통한 14개 고객 세그먼트 분석
- 세그먼트별 매출 기여도 분석 (총 매출, 거래 건수, 평균 구매금액)
- 캐시카우 세그먼트 식별 및 심층 분석
- 베스트셀러 상품 발굴 및 특성 분석
- 타겟 마케팅 전략 수립 및 예상 효과 도출
- 세그먼트별 도시 등급, 결혼 여부, 거주 기간 등 추가 특성 분석

---

## 데이터 출처

**출처:** [Kaggle - Walmart Sales Dataset](https://www.kaggle.com/datasets/devarajv88/walmart-sales-dataset)

**데이터 상세:**
- 총 550,068건의 거래 데이터 (약 55만 건)
- 5,891명의 고유 고객
- 3,631개의 고유 제품

**주요 컬럼:**
- `User_ID`: 고객 고유 식별번호 (7자리 숫자)
- `Product_ID`: 제품 고유 식별번호 (문자+숫자 조합)
- `Gender`: 성별 (M: 남성, F: 여성)
- `Age`: 연령대 (0-17, 18-25, 26-35, 36-45, 46-50, 51-55, 55+)
- `Occupation`: 직업 코드 (0-20, 익명화됨)
- `City_Category`: 도시 등급 (A, B, C)
- `Stay_In_Current_City_Years`: 현재 도시 거주 기간 (0, 1, 2, 3, 4+년)
- `Marital_Status`: 결혼 여부 (0: 미혼, 1: 기혼)
- `Product_Category`: 제품 카테고리 (1-20, 익명화됨)
- `Purchase`: 구매 금액 (인도 루피 ₹)

---

## 기술 스택

**Python 3.12.9 이상**

**핵심 라이브러리:**
- **Pandas**: 데이터 전처리 및 분석
- **NumPy**: 수치 계산 및 통계 분석
- **Matplotlib**: 데이터 시각화 (차트 생성)
- **Seaborn**: 고급 시각화 (히트맵, 상관관계 분석)

**개발 환경:**
- Jupyter Notebook (데이터 탐색 및 분석)
- VS Code (코드 개발 및 실행)

---

## 분석 목표

### 1. 캐시카우 고객층 식별
- 성별 × 연령대 교차 분석을 통한 고객 세분화
- 총 매출 기여도 기준 최대 매출 세그먼트 도출
- 세그먼트별 거래 건수, 평균 구매금액 비교 분석

### 2. 베스트셀러 상품 발굴
- 캐시카우 세그먼트의 구매 제품 Top 10 분석
- 구매 빈도 1위 제품을 베스트셀러 상품으로 식별
- 베스트셀러 상품의 제품 카테고리, 평균 가격, 매출 기여도 분석

### 3. 타겟 마케팅 전략 수립
- 캐시카우 세그먼트 특성 분석 (도시 등급, 결혼 여부, 거주 기간)
- 베스트셀러 상품의 세그먼트별 선호도 검증
- SNS 광고, 인플루언서 마케팅 등 구체적 전략 제시
- 예상 매출 증대 효과 산출 (약 20% 목표)

### 4. 데이터 기반 의사결정 지원
- 상위 3개 세그먼트 비교 분석
- 캐시카우의 차별화 요소 도출
- 재고 및 진열 최적화 전략 제시

---

## 프로젝트 결과

### 캐시카우 세그먼트: [데이터 분석 결과에 따라 자동 도출]

- 전체 매출의 약 X% 차지
- 전체 거래의 약 Y% 차지
- 평균 구매금액: ₹Z

### 베스트셀러 상품: [제품 코드 자동 식별]

- 캐시카우 세그먼트 내 구매 건수 1위
- 총 매출: ₹A
- 세그먼트 내 매출 기여도: B%

### 마케팅 전략:

1. 캐시카우 세그먼트 타겟 SNS 광고 집중
2. 베스트셀러 상품 중심 번들 상품 및 할인 이벤트
3. 인플루언서 마케팅 협업
4. 크로스셀링 알고리즘 적용
5. 재고 확대 및 매장 내 프라임 위치 배치

### 예상 효과: 매출 20% 증대

---

## 파일 구조
```
walmart-analysis/
├── data/
│   └── walmart.csv              # 원본 데이터
├── notebooks/
│   └── walmart_analysis.ipynb   # 분석 노트북
├── src/
│   └── analysis.py              # 전체 분석 코드
├── results/
│   ├── figures/                 # 시각화 차트
│   └── reports/                 # 분석 레포트
└── README.md
```

---

## 실행 방법
```bash
# 1. 라이브러리 설치
pip install pandas numpy matplotlib seaborn

# 2. 데이터 다운로드
# Kaggle에서 walmart.csv 다운로드 후 data/ 폴더에 저장

# 3. 분석 실행
python src/analysis.py
```

---

## 분석 결과 시각화 예시

- 성별 거래 건수 및 비율
- 연령대별 거래 건수 분포
- 성별 × 연령대 히트맵
- 세그먼트별 총 매출액 Top 10
- 세그먼트별 거래 건수 Top 10
- 베스트셀러 상품의 세그먼트별 구매 분포

---

## 한계점 및 향후 연구

**한계점:**
- 시간 데이터 부재로 계절성 분석 불가
- 제품명 익명화로 실제 상품 특성 파악 제한
- 온라인/오프라인 구분 정보 부재

**향후 연구:**
- 시계열 데이터 확보 시 트렌드 분석
- 제품 카테고리별 심층 분석
- 고객 생애 가치(LTV) 분석

---

## 라이센스

이 프로젝트는 교육 목적으로 작성되었으며, 데이터는 Kaggle의 Walmart Sales Dataset을 사용하였습니다.

---

## 작성자

**이형주**  
**프로젝트 기간:** 2026년 2월 2일  
**분석 도구:** Python, Jupyter Notebook, VS Code



===========================================================================================================================================================================================


# hipython
KPMG Git Hub Initialize

## 📝 펀드메니저 & AI 컨설턴트 포트폴리오

안녕하세요. 약 **8년간 금융업계 전반**에서 쌓아온 탄탄한 도메인 지식을 바탕으로, 이제는 **AI라는 강력한 도구**를 통해 비즈니스의 미래를 설계하고자 합니다.

급변하는 AI 시대에 맞춰 **IT 업계로의 전략적 전환**을 선언하며, 현재 **삼정KPMG Future Academy**에서 컴퓨터 언어와 생성형 AI 기술을 연마하고 있습니다. 단순히 기술을 습득하는 것에 그치지 않고, 금융을 넘어 다양한 산업 현장에서 **AI 기술이 실제 가치를 창출**할 수 있도록 주도하는 전문가 역량을 갖추고자 끊임없이 노력하고 있습니다.

---

## 👤 About Me
* **데이터 기반 의사결정 구조화**: 금융기관 근무 경험과 비즈니스 기획 역량을 바탕으로, 업무 프로세스를 데이터 구조로 전환하고 판단 로직을 자동화하는 데 강점이 있습니다.
* **실무 중심의 AI 솔루션 설계**: 단순한 분석 결과 도출에 그치지 않고, 비즈니스 요구사항을 재정의하여 현업에서 즉시 활용 가능한 서비스 형태의 결과물을 만드는 데 집중합니다.
* **효율적인 시스템 구축**: 반복적인 수작업을 줄이고 조직의 의사결정 리스크를 관리할 수 있는 설명 가능한 AI 시스템을 지향합니다.

---

## 🛠 기술 스택
* **Data / AI**: Python (Pandas, NumPy), 데이터 전처리 및 분석, 생성형 AI 활용 맥락 해석 및 리포트 자동 생성
* **Backend / Data**: Python 기반 데이터 처리 및 API 구조 이해, MySQL 데이터 및 DB 구조 설계
* **Collaboration**: README 및 기획 문서 중심의 협업, 비즈니스 요구사항 정의 및 데이터 모델링

---

## 🚀 프로젝트

### **PRISM AI: 설명 가능한 데이터 기반 팀 구성 의사결정 지원 시스템**
* **개요**: 조직 내 팀 빌딩 의사결정을 데이터 기반으로 구조화하여 추천 결과와 그 근거를 함께 제시하는 시스템입니다.
* **주요 역할**: 비즈니스 요구사항을 데이터 모델로 재정의하고, 조직 이론을 기반으로 한 판단 로직 설계 및 데이터 처리 프로세스를 구축했습니다.
* **주요 기능**: 
    * 생성형 AI를 활용한 프로젝트 요구사항(자연어) 맥락 해석 및 가중치 자동 설정
    * 모든 팀 조합 비교 분석을 통한 최적의 팀 추천 및 리스크/기여도 산출
    * 사람이 납득 가능한 형태의 설명 리포트 자동 생성 및 UI 프로토타입 설계

---

## 🎓 배경 및 역량
* **타이거컴퍼니 (응용소프트웨어개발업)**: 경영팀, 기획, 수석
* **리더스기술투자 (VC)**: 투자팀, 과장
* **W자산운용**: 운용팀, 주니어매니저
* **메리츠증권**: 영업부, 대리
* **한양대학교 경영전문대학원 (MBA)** 졸업
* **Pennsylvania State University (B.A / Finance)** 졸업
* **투자자산운용사**


---

## 📩 Contact
* **Email**: blackhole1247@gmail.com
* **Github**: [https://github.com/blackhole-24](https://github.com/blackhole-24)




---
---


# 안녕하세요. KPMG Future Academy 8기 이형주입니다. #
## 1차 프로젝트로 우리 PRISM팀은 산업에서 AI를 활용하여 업무를 자동화 시키는 것을 주제로 AI가 최적의 TF팀을 구성하는 서비스를 구현하였습니다.

# PRISM AI 

**설명 가능한 데이터 기반 팀 구성 의사결정 지원 시스템**

PRISM AI는 *사람을 평가하는 AI*가 아니라, **팀 구성 “의사결정”을 설명 가능하게 구조화하는 AI**입니다.

> PRISM AI는 팀을 추천만 하지 않습니다.
> **선택한 이유를 설명합니다.**

---

## 1. Executive Summary

본 프로젝트는 “조직의 팀 구성 의사결정이 왜 설명되지 못하는가”라는 문제의식에서 출발했습니다.

대부분의 조직은 팀 성과가 좋지 않을 경우 사람의 역량이나 태도를 문제 삼지만, 정작

* **왜 이 조합이 선택되었는지**
* **다른 선택지는 무엇이었는지**
에 대한 구조적 설명은 부재했습니다.

PRISM AI는 **결과(팀 추천)** 뿐 아니라 **근거(판단 기준/맥락/리스크)** 를 함께 제시하여 의사결정의 **투명성과 신뢰성**을 확보하는 것을 목표로 합니다.

![Executive Summary](https://github.com/KpmgFuture-Academy/fa08-1st-PRISM/raw/main/docs/images/%EA%B7%B8%EB%A6%BC1.png)

---

## 2. Problem Definition

### 기존 의사결정의 한계

* 팀 구성 기준이 **암묵적**이며 사후 설명 불가
* 성과 실패 시 **책임이 개인에게 전가**
* 자동화 도입 시 **초기 데이터 편향이 그대로 학습**될 위험

![기존 의사결정의 한계](https://github.com/KpmgFuture-Academy/fa08-1st-PRISM/raw/main/docs/images/%EA%B7%B8%EB%A6%BC2.png)

### 핵심 문제 재정의

> 문제는 사람이 아니라, **의사결정 시스템**입니다.

![문제 재정의](https://github.com/KpmgFuture-Academy/fa08-1st-PRISM/raw/main/docs/images/%EA%B7%B8%EB%A6%BC3.png)

---

## 3. Project Objective

* 팀 구성 의사결정을 **데이터 기반으로 구조화**
* 결과뿐 아니라 **판단 근거와 리스크를 함께 제시**
* 조직 맥락에 따라 유연하게 달라지는 **기준 설계**
* 초기 단계에서는 자동화보다 **신뢰 가능한 기준선(Baseline) 확보**

![Project Objective](https://github.com/KpmgFuture-Academy/fa08-1st-PRISM/raw/main/docs/images/%EA%B7%B8%EB%A6%BC4.png)

---

## 4. Key Personas & Needs

| Persona | 핵심 니즈 |
| :--- | :--- |
| **CEO** | 결과에 대한 **설명 가능성** |
| **팀 리더** | 팀 구성 **리스크의 사전 인지** |
| **실무자** | **개인 책임 전가 구조 완화** |
| **HR** | **일관된 평가 기준과 기록** |

![Key Personas](https://github.com/KpmgFuture-Academy/fa08-1st-PRISM/raw/main/docs/images/%EA%B7%B8%EB%A6%BC5.png)

---

## 5. Solution Overview (3단계 구조)

PRISM AI는 **3단계 구조**로 의사결정을 지원합니다.

![AI 기반 팀 빌딩 시스템 흐름](https://github.com/KpmgFuture-Academy/fa08-1st-PRISM/raw/main/docs/images/%EA%B7%B8%EB%A6%BC6.png)

### STEP 1. 데이터 정량화 (Human-in-the-Loop)

* HR 원천 데이터를 **그대로 사용하지 않음**
* **McKinsey Team Health 7 Drivers** 기준 수작업 라벨링
* **점수 + 판단 근거** 동시 기록
* 이후 모델 학습을 위한 **신뢰 가능한 Baseline 확보**

![STEP 1 라벨링 구조](https://github.com/KpmgFuture-Academy/fa08-1st-PRISM/raw/main/docs/images/%EA%B7%B8%EB%A6%BC7.png)
![데이터 구조 설계](https://github.com/KpmgFuture-Academy/fa08-1st-PRISM/raw/main/docs/images/%EA%B7%B8%EB%A6%BC8.png)
![STEP 1 개요](https://github.com/KpmgFuture-Academy/fa08-1st-PRISM/raw/main/docs/images/%EA%B7%B8%EB%A6%BC9.png)

---

### STEP 2. 맥락 기반 가중치 설계

* 프로젝트 요구사항을 **자연어로 입력**
* 생성형 AI가 프로젝트 맥락을 해석하여 **Context Signal 추출**
* 조직 이론 기반 **가중치 모델 적용**
* “예측”이 아닌 **판단 기준 설정 단계**

![STEP 2 라벨링 구조](https://github.com/KpmgFuture-Academy/fa08-1st-PRISM/raw/main/docs/images/%EA%B7%B8%EB%A6%BC10.png)
![STEP 2 개요](https://github.com/KpmgFuture-Academy/fa08-1st-PRISM/raw/main/docs/images/%EA%B7%B8%EB%A6%BC11.png)
![프롬프트 기반 맥락 해석](https://github.com/KpmgFuture-Academy/fa08-1st-PRISM/raw/main/docs/images/%EA%B7%B8%EB%A6%BC12.png)
![이론 + AI 결합 (1)](https://github.com/KpmgFuture-Academy/fa08-1st-PRISM/raw/main/docs/images/%EA%B7%B8%EB%A6%BC13.png)
![이론 + AI 결합 (2)](https://github.com/KpmgFuture-Academy/fa08-1st-PRISM/raw/main/docs/images/%EA%B7%B8%EB%A6%BC14.png)
![가중치 최적화 모델](https://github.com/KpmgFuture-Academy/fa08-1st-PRISM/raw/main/docs/images/%EA%B7%B8%EB%A6%BC15.png)

---

### STEP 3. 최적화 및 평가 + 설명 생성

* 가능한 **모든 팀 조합 비교**
* 팀 점수 + 리스크 + 개인 기여도 산출
* **개인 순위 산출 금지(가드레일)**
* 결과에 대한 **설명 리포트 자동 생성**

![STEP 3 개요](https://github.com/KpmgFuture-Academy/fa08-1st-PRISM/raw/main/docs/images/%EA%B7%B8%EB%A6%BC16.png)
![평가 모델 구조](https://github.com/KpmgFuture-Academy/fa08-1st-PRISM/raw/main/docs/images/%EA%B7%B8%EB%A6%BC17.png)
![최적화 알고리즘 실행](https://github.com/KpmgFuture-Academy/fa08-1st-PRISM/raw/main/docs/images/%EA%B7%B8%EB%A6%BC18.png)

---

## 6. 생성형 AI 모듈 구성

### 생성형 AI 2: 프롬프트 맥락 해석

* 입력: **프로젝트 요구사항(자연어)**
* 출력: **Context Vector / Context Signal**
* 목적: 팀 건강 드라이버의 **상대적 중요도(가중치) 설계**

### 생성형 AI 3: 리포트 생성

* 입력: 최적화 결과(추천 팀 / 리스크 / 기여도 / 근거)
* 출력: 사람이 납득 가능한 **설명 리포트**

![설명 리포트 생성](https://github.com/KpmgFuture-Academy/fa08-1st-PRISM/raw/main/docs/images/%EA%B7%B8%EB%A6%BC19.png)

---

## 7. Output Example (산출물 구성)

* **Top-N 팀 추천**
* 팀 **강점 / 리스크 요약**
* Driver별 **기여도**
* 개인별 **팀 기여 설명**
* **권장 액션 아이템**

![결과 산출 예시](https://github.com/KpmgFuture-Academy/fa08-1st-PRISM/raw/main/docs/images/%EA%B7%B8%EB%A6%BC20.png)
![팀 선택 근거 설명](https://github.com/KpmgFuture-Academy/fa08-1st-PRISM/raw/main/docs/images/%EA%B7%B8%EB%A6%BC21.png)

---

## 8. UI Prototype

![프롬프트 입력 UI](https://github.com/KpmgFuture-Academy/fa08-1st-PRISM/raw/main/docs/images/%EA%B7%B8%EB%A6%BC22.png)
![추천 결과 UI](https://github.com/KpmgFuture-Academy/fa08-1st-PRISM/raw/main/docs/images/%EA%B7%B8%EB%A6%BC23.png)
![분석 리포트 UI](https://github.com/KpmgFuture-Academy/fa08-1st-PRISM/raw/main/docs/images/%EA%B7%B8%EB%A6%BC24.png)
![팀 상세 분석 UI](https://github.com/KpmgFuture-Academy/fa08-1st-PRISM/raw/main/docs/images/%EA%B7%B8%EB%A6%BC25.png)

---

## 9. Technical Stack

| 영역 | 내용 |
| :--- | :--- |
| **LLM** | GPT-4.0-mini |
| **핵심 로직** | **가중치 기반 조합 최적화** |
| **데이터 구조** | **Feature Store** |
| **리포트** | **AI 기반 설명 생성** |

![기술 스택](https://github.com/KpmgFuture-Academy/fa08-1st-PRISM/raw/main/docs/images/%EA%B7%B8%EB%A6%BC26.png)
![설명 모델 비교](https://github.com/KpmgFuture-Academy/fa08-1st-PRISM/raw/main/docs/images/%EA%B7%B8%EB%A6%BC27.png)

---

## 10. Expected Business Impact

* **팀 구성 실패 리스크 감소**
* **의사결정 책임의 구조화**
* HR 판단의 **일관성 강화**
* 조직 내 **갈등 및 납득 비용 감소**

---

## 11. Future Expansion

* Step 1 **반자동 라벨링**
* 실제 성과 데이터 기반 학습
* 조직 규모 확장 대응
* HR 시스템 연계

---

# 📌 One-liner

**PRISM AI는 ‘팀을 추천’하는 것이 아니라, ‘왜 그 팀이어야 하는지’를 설명하는 시스템입니다.**








