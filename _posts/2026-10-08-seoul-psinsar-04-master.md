---
title: "서울 Sentinel-1 PS-InSAR 분석 #4 - 마스터 영상과 수직 기준선"
date: 2026-10-08
permalink: /insar-seoul/04-master/
categories: [기술]
tags: [Sentinel-1, InSAR, PS-InSAR]
author_profile: true
toc: true
---

프로젝트의 마스터 영상은 2022-07-16 획득 영상으로 기록되어 있다. P9의 `ps1.mat`에서 124개 영상과 마스터 인덱스 65를 확인했고, 수직 기준선은 −252.054 m부터 +481.418 m까지 분포한다.

![P9 영상의 획득일과 수직 기준선](/assets/images/insar-seoul/04-master/baseline-time-network.png)

이 플롯은 P9 진단 산출물이다. 마스터 선택의 실제 기록을 보여 주지만, 이 자료만으로 마스터가 최적이었다고 결론 내리지는 않는다. 영상 시계열과 수직 기준선은 PS 네트워크의 기하 조건을 이해하는 자료이며, 변위 자체를 나타내지 않는다.

![TOPS 공동등록 개념도](/assets/images/insar-seoul/05-coreg/tops-coregistration.png)

공동등록 그림은 설명용 개념도이며 ESD 잔차 측정 결과가 아니다. ESD 로그와 실제 SNAP 그래프가 확인되면 별도로 검증해야 한다.

앞 글: [AOI와 burst 후보 범위](/insar-seoul/02-aoi-burst/) · 다음 공개 글: [간섭 위상 살펴보기](/insar-seoul/06-interferogram/)
