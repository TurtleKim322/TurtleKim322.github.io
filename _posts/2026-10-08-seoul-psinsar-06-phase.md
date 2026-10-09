---
title: "서울 Sentinel-1 PS-InSAR 분석 #6 - 간섭 위상과 wrapped phase 점검"
date: 2026-10-08
permalink: /insar-seoul/06-interferogram/
categories: [위성]
tags: [Sentinel-1, InSAR, PS-InSAR, StaMPS]
author_profile: true
toc: true
---

간섭 위상(interferometric phase)은 두 SAR 관측의 복소 신호를 곱해 얻는 위상 차다. StaMPS 입력에서 이를 후보점과 시간축으로 확인하면 결측, 위상 범위, 공간 패턴을 점검할 수 있다. 그러나 wrapped phase는 정수 주기만큼 접힌 값이므로 그 자체를 mm 단위 지표 이동으로 읽을 수 없다.

## 위상 차와 wrap

두 영상의 복소 신호를 각각 S1, S2라 하면 한 convention의 간섭 신호는 S1 × conjugate(S2)로 쓸 수 있고, 그 argument가 위상 차다. 부호는 곱의 순서와 처리 convention에 따라 달라질 수 있다. wrapped phase는 보통 −π에서 +π 사이에 놓인다. 위상 변화가 이 경계를 지나면 값이 반대편 끝으로 접혀 보이는 phase wrapping이 일어난다.

변위에 따른 LOS 위상은 단순화하면 Δφ_LOS = 4π × Δr / λ 관계를 갖는다. 여기서 Δr은 시선 방향 거리 변화, λ는 레이더 파장이다. 한 장의 wrapped 값에는 몇 번의 2π 주기가 접혔는지 정보가 없고, 관측에는 지형 잔차·대기·궤도·잡음도 포함된다. 따라서 phase unwrapping과 시계열 모델링, 기준점·오차 검토 전에는 변위로 환산할 수 없다. [위상 오차 항의 PS-InSAR 설명](https://doi.org/10.1029/2004GL021737)

## P9 위상 배열의 일부를 시각화

P9의 `ph1.mat`에서 후보점의 위상 배열을 읽고 영상 날짜 목록과 대조했다. 아래 패널은 124개 영상 중 인덱스 10, 30, 50, 70에 해당하는 네 시점이며, 인덱스 50은 **2021-11-18**이다. 기준 날짜는 **2022-07-16**이다.

![P9 네 시점의 wrapped phase 비교](/assets/images/insar-seoul/06-interferogram/wrapped-phase-comparison.png)

그림 1. P9 후보점 위상의 angle(ph) 분포. 색 범위는 wrapped phase −π–+π rad이며, 공간 패턴은 위상값의 분포이지 누적 변위 속도나 침하량이 아니다. 각 패널의 흰 공간은 해당 위치에 표시할 후보점이 없는 영역이다.

개별 시점은 비교용으로 같은 색 범위를 사용한다. 서로 다른 날짜의 색이 바뀌는 것은 wrapped phase가 변했음을 보여 주지만, 접힘과 여러 오차 성분 때문에 이동 방향이나 크기를 바로 판정하지 못한다.

## 이 단계에서 확인할 것

- 각 날짜가 `day` 배열과 일치하는지 확인한다.
- 위상값과 좌표 행의 개수가 맞고 NaN·Inf가 없는지 점검한다.
- 색 범위가 −π–+π rad인지, 표시 인덱스가 1부터인지 0부터인지 명시한다.
- phase map은 `lonlat` 좌표를 쓴 P9 진단 결과로 한정하고 AOI 전체 결과처럼 표시하지 않는다.
- `.diff` 원본은 현재 남아 있지 않으므로 되살리거나 다시 생성했다고 주장하지 않는다. 시각화는 남아 있는 StaMPS 위상 배열에서 만들었다.

그림은 현재 확인 가능한 P9 `ph1.mat`의 배열을 이용한 진단 시각화다. 이후 후보 선택과 시계열 보정이 끝나도 LOS 변위로 해석하려면 대기·궤도·기준점·unwrapping 영향을 따로 평가해야 한다.

앞 글: [기준 영상과 수직 기준선](/insar-seoul/04-master/) · 다음: [후보점 수와 patch 경계](/insar-seoul/07-candidates/)
