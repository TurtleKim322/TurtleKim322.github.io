---
layout: single
title: 논문 작성 공부 — EQ 열적노화 연구 노트
permalink: /research-study/
categories: [도전과제, 논문 작성 공부]
author_profile: true
toc: true
---

원전 EQ 열적노화의 **보수성 확보 방법**과 **Arrhenius 모델 불확실성이 검증수명에 미치는 영향**을 하나의 프로젝트로 공부한다. 고정 Safety Factor와 통계적 접근을 비교하되 어느 방법이 더 낫다는 결론은 아직 정하지 않는다.

## 핵심 질문

Arrhenius 모델로 원전 기기의 열수명을 예측할 때 모델·재료·운전조건·통계적 불확실성을 고려하기 위해 어느 정도의 보수성이 필요한가?

1. Arrhenius 열수명 계산에는 어떤 불확실성이 있는가?
2. Activation Energy 변화는 계산 열수명에 얼마나 영향을 주는가?
3. 운전온도 또는 Heat Rise가 1~5℃ 달라지면 수명이 얼마나 변하는가?
4. Intercept와 시험 데이터 산포는 결과에 어떻게 전달되는가?
5. 장기간 외삽의 불확실성을 어떻게 정량화할 수 있는가?
6. Fixed Safety Factor와 통계적 Lower Confidence Bound를 어떤 기준으로 비교할 수 있는가?
7. Monte Carlo Simulation으로 검증수명 산정의 확률적 접근 가능성을 평가할 수 있는가?

## 학습 로드맵

{% include research-study-roadmap.html %}

문제 발견 → 규제·규격 조사 → 개념과 이론 → 데이터 조사 → 통계와 민감도 → 기존 방법의 한계 → 가설 → 연구설계 → 분석 → 논문 작성 순서로 진행한다. 근거에 따라 질문과 계획을 수정한다.

## 진행상황

‘완료’는 해당 글의 작성 완료이며 연구 검증 완료를 뜻하지 않는다. #02~#18은 공개된 학습 개요이고 조사 결과가 아니다.

{% for item in site.data.thermal_aging %}
- **[{{ item.status }}] #{{ item.label }}** [{{ item.title }}]({{ item.url | relative_url }}){% if item.status != '완료' %} — 학습 개요{% endif %}
{% endfor %}

## 기록 원칙

규격 요구사항, 문헌의 보고 결과, 나의 연구 가설을 구분한다. 직접 확인하지 못한 조항은 ‘확인 필요’로 둔다. 회사·고객의 자료, 식별번호, 사내 판단기준, 유료 규격 전문은 포함하지 않는다. 계산에는 단위·종말점·출처·가정·재현 조건을 남긴다.

## 다음에 알아볼 것

[#02 규제체계 학습 개요]({{ '/research-study/02/' | relative_url }})에서 규정과 지침, 표준의 역할 및 적용 판본을 조사한다.

## References

1. U.S. NRC / eCFR, [10 CFR 50.49 — Environmental qualification of electric equipment important to safety for nuclear power plants](https://www.ecfr.gov/current/title-10/chapter-I/part-50/section-50.49). 조항 원문 재확인 필요.
2. U.S. NRC, [Regulatory Guide 1.89 공식 목록](https://www.nrc.gov/regulations-legislation/regulatory-guides-by-division/division-1---power-reactors/regulatory-guides-181---1100). Rev.2, 2023년 4월. 목록 확인; 상세 본문은 후속 조사.
3. IEEE, [IEC/IEEE 60780-323-2016 — Nuclear facilities — Electrical equipment important to safety — Qualification](https://standards.ieee.org/ieee/60780-323/5836/). 공개 개요 확인; IEEE 323-2003 후속 표준. 유료 본문 미확인.
4. IEEE, [IEEE/ANSI 101-1987 — IEEE Guide for the Statistical Analysis of Thermal Life Test Data](https://standards.ieee.org/ieee/101/258/). 공개 개요 확인; Inactive-Reserved. 유료 본문 미확인.
5. [KEPIC 공식 홈페이지](https://www.kepic.org/main/). END 적용 판본·세부 조항 확인 필요.
