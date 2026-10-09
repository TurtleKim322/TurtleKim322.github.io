---
title: "서울 Sentinel-1 PS-InSAR 분석 #9 - P9 StaMPS Step 1–3 진단 결과"
date: 2026-10-08
permalink: /insar-seoul/09-step1-2/
categories: [위성]
tags: [PS-InSAR, StaMPS]
author_profile: true
toc: true
---

StaMPS Step 1은 후보점의 입력 자료를 준비하고 Step 2는 후보별 gamma 등 위상 안정성 관련 값을 추정한다. Step 3에서는 coherence 재추정과 임계값에 따라 선택을 진행한다. 이 글은 **P9 한 patch의 기존 산출물과 로그**를 중심으로 설명하고, P14의 선택 완료 기록도 별도로 표시한다. 두 patch의 결과를 서울 전체 분석으로 확대 해석하지 않는다.

## 진단 patch의 위치

P9 후보 좌표 범위는 경도 126.5181–126.7532°, 위도 37.3654–37.5279°다. 프로젝트 AOI의 대부분과 겹치지 않으며 일부 경계만 인접한다. 따라서 아래 그림과 통계는 서울 AOI 대표값이 아니라 P9 실행 진단 자료다.

## Step 2: gamma와 coherence 자료

![P9 Step 2 gamma 분포](/assets/images/insar-seoul/09-stamps-step1-2/step2-gamma-histogram.png)

그림 1. P9 `ps1.mat` 후보 303,941개의 Step 2 gamma 분포. 표시된 중앙값은 0.8773이고 비유한 값은 0개다. 파일 이름은 coherence histogram이지만 그래프 제목과 배열 근거에 맞춰 이 값을 gamma 분포로 읽는다. gamma와 Step 3에서 재추정되는 coherence는 관련은 있어도 같은 처리 단계의 값이라고 단정하지 않는다.

![P9 Step 2 coherence 재추정 지도](/assets/images/insar-seoul/09-stamps-step1-2/step2-coherence-map.png)

그림 2. P9 후보 좌표에 표시한 `coh_ps` 값(0–1). 값의 공간 분포를 보여 주며 변위량은 아니다.

## Step 2: 잔여 지형 위상 계수와 높이

![P9 K parameter 지도](/assets/images/insar-seoul/09-stamps-step1-2/step2-kps-map.png)

그림 3. P9의 `K_ps` 잔여 지형 위상 계수 분포. 단위는 수직 기준선 1 m당 rad로 표시되어 있다. 이는 지형 잔차와 관련된 계수이지 LOS 변위 속도 단위가 아니다.

![P9 후보점 높이](/assets/images/insar-seoul/09-stamps-step1-2/candidate-height-map.png)

그림 4. 후보점의 높이 자료. 원본의 `-32768` sentinel은 유효 표고로 취급하지 않았다. 수직 datum은 확인되지 않아 절대 고도 비교에는 주의가 필요하다.

## Step 3 로그에서 확인되는 범위

P9 `STAMPS.log`에는 2026-10-05에 Step 3가 시작되고, 2026-10-06에 coherence 재추정 뒤 **302,481개** 후보가 선택되었다는 기록이 있다. P14 로그에는 2026-10-07에 Step 3가 시작되고 2026-10-08에 **460,353개** 후보 선택이 기록되어 있다. 이는 각 patch의 실행 이력이다. 전체 20개 patch의 Step 3 완료, 최종 시계열 품질, LOS 변위 해석을 입증하지 않는다.

P9 로그의 Step 2에서는 `lambda=0.0554658`, `n_trial_wraps=0.937572`가 기록된다. 이는 앞서 초기 전역 로그의 `lambda=NaN`에서 파라미터를 바로잡은 뒤 계산된 구체적 실행값이다. Step 3 선택 수 역시 입력 후보 수와 다르며, 단순히 남은 “안정한 변위점” 수로 읽지 않는다.

## 해석의 한계와 다음 검증

P9는 AOI 안팎의 경계에 걸친 진단용 patch다. gamma, `coh_ps`, `K_ps`, height map은 알고리즘 중간 산출물을 각각 다른 물리·통계량으로 표현한다. 최종 LOS 변위 시계열을 말하려면 모든 patch 처리 상태, 위상 unwrapping, 기준점, 오차 보정과 공간 정합을 확인해야 한다. 현재 공개 자료는 이 전 과정을 완료한 서울 변위 지도가 아니다.

앞 글: [Octave와 C 처리 진단](/insar-seoul/08-debug/) · 다음: [당시 WSL 저장 공간 기록](/insar-seoul/10-storage/)
