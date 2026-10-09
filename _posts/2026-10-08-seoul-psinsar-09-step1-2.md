---
title: "서울 Sentinel-1 PS-InSAR 분석 #9 - P9 후보는 얼마나 안정적이었나"
date: 2026-10-08
permalink: /insar-seoul/09-step1-2/
categories: [취미, 개인 프로젝트, 서울 PS-InSAR, 프로그래밍, 신호처리]
project: seoul-psinsar
project_order: 7
tags: [PS-InSAR, StaMPS]
author_profile: true
toc: true
---

후보점을 뽑았다고 바로 움직임을 읽을 수 있는 것은 아니다. StaMPS는 먼저 여러 시기의 위상 이력을 이용해 후보별 gamma를 추정한다. 그 다음 단계에서 coherence 기준과 다른 조건을 사용해 점을 선택한다. 용어가 비슷해 보이지만, 어느 Step의 어느 변수인지 확인해야 혼동하지 않는다.

먼저 위치를 확인했다. P9 후보의 경도 범위는 126.5181–126.7532°, 위도는 37.3654–37.5279°다. 프로젝트 AOI의 대부분과 겹치지 않는 진단용 PATCH다. 아래 결과를 서울 전체의 지도로 읽으면 안 된다.

## Step 2에서 추정한 gamma

gamma는 여러 관측에서 후보점의 위상이 얼마나 일관되게 설명되는지 나타내는 값이다. StaMPS의 `ps_est_gamma_quick.m`은 이를 추정하면서 결과를 `coh_ps`라는 변수에 저장한다. 따라서 아래 그래프 제목의 gamma와 코드 변수명 `coh_ps`는 여기서 서로 다른 지표 두 개를 가리키지 않는다.

P9 `ps1.mat`에는 후보 303,941개가 있다. 그래프를 만들 때 먼저 분포가 어느 구간에 모이는지, 비정상 값이 있는지 확인했다. 중앙값은 0.8773이고 유한하지 않은 값은 0개였다.

![P9 Step 2 gamma 분포](/assets/images/insar-seoul/09-stamps-step1-2/step2-gamma-histogram.png)

이 히스토그램은 gamma 추정 결과를 요약한다. Step 3에서 coherence를 다시 추정하고 선택한 결과까지 보여 주는 그래프는 아니다.

## 지도에서 같은 값을 공간으로 보기

아래 지도도 색상 막대에 `coh_ps`라고 적혀 있다. 그래프 제목은 Step 2 gamma다. 코드에서 이 두 이름이 연결되는 만큼, 히스토그램과 다른 측정량이라고 보지 않고 같은 추정값의 공간 분포로 설명한다. 색은 0–1 범위의 값이지 지표 이동량이 아니다.

![P9 Step 2 gamma 공간 분포](/assets/images/insar-seoul/09-stamps-step1-2/step2-coherence-map.png)

## 지형 잔차와 후보 높이

간섭 위상에는 지형 자료의 오차도 섞일 수 있다. `K_ps`는 위상에서 수직 기준선 변화와 함께 달라지는 잔여 지형 성분을 나타내는 계수다. 그림의 단위는 기준선 1 m당 rad이며, mm/년으로 표현하는 침하 속도와 다르다.

![P9 잔여 지형 위상 계수 지도](/assets/images/insar-seoul/09-stamps-step1-2/step2-kps-map.png)

높이 그림은 후보 위치에 연결된 높이 자료를 보여 준다. 원본에서 `-32768`은 결측을 나타내는 sentinel이라 실제 고도로 취급하지 않았다. 수직 datum도 확인되지 않아 절대 표고로 해석할 수 없다.

![P9 후보점 높이](/assets/images/insar-seoul/09-stamps-step1-2/candidate-height-map.png)

## 로그에는 선택 결과가 남아 있다

Step 3에서는 gamma와 amplitude dispersion 조건을 바탕으로 coherence를 재평가하고 후보를 고른다. P9 로그에는 302,481개, P14 로그에는 460,353개가 선택됐다고 기록되어 있다. 이는 두 PATCH의 처리 기록이다. 20개 PATCH 전체가 완료됐거나 이 점들이 최종 변위 시계열로 검증됐다는 뜻은 아니다.

P9은 서울 AOI 대부분 바깥에 놓인 진단용 PATCH다. 그래서 gamma와 `K_ps`, 높이 그림도 해당 patch에서 어떤 값이 나왔는지를 설명할 뿐, 서울 전체의 대표 결과가 아니다. 모든 PATCH의 상태, 기준점과 보정, phase unwrapping을 확인해야 최종 LOS 변위를 해석할 수 있다. 현재 자료만으로 서울 전체 변위 지도를 제시하지 않는 이유다.

앞 글: [Octave 오류를 하나씩 따라가기](/insar-seoul/08-debug/) · 다음: [WSL 저장공간이 부족해졌을 때](/insar-seoul/10-storage/)
