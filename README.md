# hipython
KPMG Git Hub Initialize
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








