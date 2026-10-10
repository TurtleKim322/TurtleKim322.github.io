---
layout: single
title: "원전 EQ 열적노화 논문 공부 #01 - 왜 열수명의 보수성을 연구하려고 하는가"
permalink: /research-study/01/
categories: [도전과제, 논문 작성 공부]
study_number: 1
author_profile: true
toc: true
comments: true
---

## 오늘 알아볼 문제

Arrhenius Equation으로 수십 년의 Thermal Life를 계산할 수 있다. 그런데 **이 계산값을 실제 Qualified Life로 어느 정도 신뢰할 수 있을까?** 입력 데이터와 모델 자체에 불확실성이 있다면, 단순한 고정 Safety Factor가 가장 합리적인 방법일까?

이 질문을 출발점으로 공부를 시작한다. 특정 계수가 옳다거나 틀리다는 결론은 아직 없다. 단순한 방법이 주는 일관성과 추적성도, 통계적 방법이 요구하는 데이터와 가정도 함께 살펴보고 싶다.

## EQ와 열적노화가 궁금한 이유

여기서 EQ는 원전 기기의 환경조건과 노화를 고려하는 Environmental Qualification 맥락으로 사용한다. 공개된 IEC/IEEE 60780-323의 개요는 안전에 중요한 전기기기가 적용 가능한 사용조건에서 안전기능을 수행할 능력을 입증하고 문서화하는 일을 다룬다.[3] 단순히 지금 작동하는지를 보는 것보다 넓은 질문이다.

이 연구 노트는 그중 열적노화에 집중한다. 열수명 모델은 정해진 재료와 열화 종말점, 온도 이력에 대한 예측 도구로 공부한다. 계산 결과를 기기 전체의 모든 환경조건에 대한 적합성으로 곧바로 확대하지 않는다. 방사선이나 복합환경 효과를 어디까지 분리할 수 있는지도 이후에 확인할 질문이다.

## 비슷해 보이는 수명 용어부터 구분하기

아래는 학습을 위한 작업상 구분이다. 규격의 정의를 그대로 옮긴 표가 아니며, #02~#03에서 적용 판본의 원문과 대조한다.

| 용어 | 이 노트에서 먼저 구분할 의미 | 함께 기록할 조건 |
| --- | --- | --- |
| Thermal Life | 정한 열화 종말점까지의 열적 수명 예측 | 재료, 온도, 모델, 종말점 |
| Qualified Life | 정한 사용조건에서 요구 기능을 충족하도록 적격성이 입증된 기간 | 검증 근거, 환경조건, 정비·교체 조건 |
| Design Life | 설계에서 의도한 사용기간 | 설계 가정과 요구 기능 |
| Installed Life | 설치 상태에서의 기간과 관련된 개념 | 기산점과 해당 규격 정의 확인 필요 |
| Remaining Life | 평가 시점 이후 남아 있다고 평가하는 기간 | 실제 이력, 현재 상태, 미래 조건 |

따라서 Thermal Life가 길게 계산되었다는 사실만으로 같은 기간의 Qualified Life가 확보되었다고 쓰지 않겠다. Remaining Life 역시 과거 이력과 조건을 확인하지 않고 설계수명에서 달력상 경과기간만 빼서 확정하지 않겠다.

## 규격에서는 어떻게 이야기하는가

출발 자료는 10 CFR 50.49와 NRC RG 1.89, IEEE 계열 표준, KEPIC이다. NRC 공식 목록에서 RG 1.89 Rev.2는 2023년 4월로 확인했다.[2] 지침의 존재나 최신 판본만으로 특정 발전소에 적용되는 판본을 확정하지는 않는다.

IEEE 공개 목록은 IEC/IEEE 60780-323-2016이 IEEE 323-2003을 대체한다고 안내한다.[3] IEEE 101-1987은 열수명 시험 데이터의 통계 분석을 다루지만 현재 목록상 Inactive-Reserved 상태다.[4] 이를 현행 의무요건으로 제시하지 않고 학습 참고자료로 검토한다.

이 자료들을 일렬로 나열했다고 해서 모두 직접적인 법적 위계나 상호 인용 관계가 되는 것은 아니다. 미국 규정과 국내 적용 근거도 따로 확인해야 한다. 이번 글에서는 확인하지 못한 상세 조항이나 특정 Safety Factor 요구값을 적지 않는다.

## 직접 계산하기 전에 정할 것

첫 글에서는 실제 재료의 수명값을 계산하지 않는다. 아직 재료·종말점·시험온도·추정계수가 정해지지 않았기 때문이다. 이후 예제에는 ‘가상 학습 데이터’ 또는 공개 시험 출처를 분명하게 표시한다.

Ea 하나뿐 아니라 Intercept, 사용 단위, 계수의 공분산, 시험온도 범위까지 확보할 계획이다. 온도는 계산식에서 K를 사용하고, 주변온도와 부품 발열을 구분한다. 무엇을 고정한 상태에서 Ea를 바꾸는지도 계산마다 남긴다.

## 연구하고 싶은 질문

1. Arrhenius 열수명 계산에는 어떤 불확실성이 있는가?
2. Activation Energy 변화는 계산 열수명에 얼마나 영향을 주는가?
3. 운전온도 또는 Heat Rise가 1~5℃ 달라지면 수명이 얼마나 변하는가?
4. Intercept와 시험 데이터 산포는 결과에 어떻게 전달되는가?
5. 장기간 외삽의 불확실성을 어떻게 정량화할 수 있는가?
6. Fixed Safety Factor와 통계적 Lower Confidence Bound를 어떤 기준으로 비교할 수 있는가?
7. Monte Carlo Simulation으로 검증수명 산정의 확률적 접근 가능성을 평가할 수 있는가?

P(Thermal Life ≥ Design Life) ≥ 95% 같은 확률 기준은 **검토할 연구 가설**이다. 규제에서 승인된 판정기준이라고 주장하지 않는다. 평균 수명의 95% 신뢰하한과 개체 수명 분포의 5백분위수도 다른 개념이다. 어느 대상을 추정하는지 먼저 정한 뒤 비교하려 한다.

## 내가 이해한 내용과 아직 남은 질문

지금 필요한 일은 가장 그럴듯한 보수계수를 고르는 것이 아니라 계산값이 무엇을 설명하며 어떤 가정에 의존하는지 추적하는 일이다. 고정 계수의 성능도, 통계적 하한의 성능도 동일한 자료와 목표 아래에서 비교해야 한다.

시험 범위를 벗어난 수십 년 예측에 충분한 근거가 있는가? 재료 간 차이와 시험 산포를 어떻게 나눌 것인가? 통계적 모델이 다루지 못한 열화기구 변화는 어떻게 남길 것인가? 이 질문들은 아직 열어 둔다.

## 앞으로의 학습 로드맵

{% include research-study-roadmap.html %}

시리즈는 한 번에 결론까지 채우지 않는다. 규격과 개념을 먼저 확인하고, 공개 데이터를 수집한 다음 민감도와 불확실성을 분석한다. 마지막에 연구방법을 설계하고 실제 결과에 따라 논문의 방향을 수정한다.

## 다음에 알아볼 것

#02에서는 10 CFR 50.49, RG 1.89, IEEE 323 계열, IEEE 101, KEPIC END의 역할과 연결 근거를 조사한다. 공개 개요에서 확인한 사실과 유료 원문이 있어야 확인할 수 있는 조항을 분리한 조사표를 작성한다.

## References

1. U.S. NRC / eCFR, [10 CFR 50.49 — Environmental qualification of electric equipment important to safety for nuclear power plants](https://www.ecfr.gov/current/title-10/chapter-I/part-50/section-50.49). 조항 원문 재확인 필요.
2. U.S. NRC, [Regulatory Guide 1.89 공식 목록](https://www.nrc.gov/regulations-legislation/regulatory-guides-by-division/division-1---power-reactors/regulatory-guides-181---1100). Rev.2, 2023년 4월. 목록 확인; 상세 본문은 후속 조사.
3. IEEE, [IEC/IEEE 60780-323-2016 — Nuclear facilities — Electrical equipment important to safety — Qualification](https://standards.ieee.org/ieee/60780-323/5836/). 공개 개요 확인; IEEE 323-2003 후속 표준. 유료 본문 미확인.
4. IEEE, [IEEE/ANSI 101-1987 — IEEE Guide for the Statistical Analysis of Thermal Life Test Data](https://standards.ieee.org/ieee/101/258/). 공개 개요 확인; Inactive-Reserved. 유료 본문 미확인.
5. [KEPIC 공식 홈페이지](https://www.kepic.org/main/). END 적용 판본·세부 조항 확인 필요.

{% include research-study-nav.html %}
