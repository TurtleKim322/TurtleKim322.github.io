---
title: "서울 Sentinel-1 PS-InSAR 분석 #6 - 간섭 위상 점검"
date: 2026-10-08
permalink: /insar-seoul/06-interferogram/
categories: [기술]
tags: [Sentinel-1, InSAR, PS-InSAR, StaMPS]
author_profile: true
toc: true
---

P9의 `ph1.mat`에 저장된 후보점 간섭 위상에서 인덱스 50을 시각화했다. 영상 날짜 목록과 대조한 해당 획득일은 2021-11-18이다. 그림은 wrapped phase를 보여 주며, 이를 곧바로 mm 단위 변위로 읽을 수 없다.

![P9 인덱스 50 wrapped phase, 2021-11-18](/assets/images/insar-seoul/06-interferogram/wrapped-phase-index-050.png)

![여러 날짜의 wrapped phase 비교](/assets/images/insar-seoul/06-interferogram/wrapped-phase-comparison.png)

위상은 대기 지연, 지형 잔차, 궤도 오차, decorrelation 및 변위의 영향을 함께 받을 수 있다. 이 단계의 그림은 자료 점검용이다. 변위 해석에는 StaMPS의 시간·공간 필터링과 기준점 선택 등 후속 처리가 필요하다.

앞 글: [마스터와 기준선](/insar-seoul/04-master/) · 다음: [후보점과 patch 중복](/insar-seoul/07-candidates/)
