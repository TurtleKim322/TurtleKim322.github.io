---
title: "서울 Sentinel-1 PS-InSAR 분석 #4 - 기준 영상과 수직 기준선 네트워크"
date: 2026-10-08
permalink: /insar-seoul/04-master/
categories: [위성]
tags: [Sentinel-1, InSAR, PS-InSAR]
author_profile: true
toc: true
---

여러 시기의 SAR 영상을 비교하려면 한 장을 기준(master)으로 지정하고 나머지 영상을 같은 관측 기하로 맞춘다. 마스터 날짜와 각 영상 사이의 수직 기준선은 간섭쌍의 시간·기하 구성을 설명하지만, 지표 변위 결과는 아니다.

## 이 프로젝트의 기준 영상

프로젝트의 기준 날짜는 **2022-07-16**이다. P9 `ps1.mat`에는 124개 영상에 대응하는 `day`와 `bperp` 배열, `master_day`, `master_ix`가 있다. 이 산출물에서 기준 인덱스는 65이며, 수직 기준선 값은 −252.054 m에서 +481.418 m 범위다. 이는 P9에서 확인한 입력 네트워크의 속성이다.

![P9 영상의 획득일과 수직 기준선](/assets/images/insar-seoul/04-master/baseline-time-network.png)

그림 1. P9 `ps1.mat`의 영상 날짜와 마스터 기준 수직 기준선. 기준선은 SAR 영상 쌍의 관측 기하 차이를 설명한다. 이 그림은 시간에 따른 지표 이동이나 분석 결과의 정확도를 나타내지 않는다.

## 수직 기준선이 알려 주는 것

간섭쌍 사이의 수직 기준선은 두 관측 궤도의 분리를 나타내는 기하 정보다. 기준선이 달라지면 같은 지형에 대한 위상 민감도와 지형 잔차의 영향도 달라질 수 있다. 시간 간격은 산란체의 시간적 안정성과 변화 가능성에 관계된다. 따라서 날짜와 기준선 분포는 연결 가능한 영상쌍과 자료의 기하를 살피는 출발점이지, 단독으로 “좋은 마스터”를 판정하는 점수는 아니다.

이 작업의 기록만으로 2022-07-16이 가능한 기준 영상 중 최적이라고 입증되지는 않는다. 그런 결론을 내려면 후보 영상별 유효 간섭쌍 수, 기준선 분포, 정합 품질, 유효 산란점과 실제 분석 목적을 같은 기준으로 비교해야 한다.

## TOPS 자료 정합과의 관계

마스터와 secondary는 같은 IW subswath와 편파로 준비하고 공통 좌표계에 정합해야 한다. TOPS 자료에서는 burst별 관측 특성과 azimuth 위상 램프가 중요하기 때문에 SNAP의 Back-Geocoding과 필요 시 ESD 단계가 사용된다. 아래 그림은 처리 원리를 설명하는 개념도다. 이 프로젝트의 잔차 측정이나 SNAP 실행 로그가 아니다. [SNAP Back-Geocoding 문서](https://step.esa.int/main/wp-content/help/versions/13.0.0/snap-toolboxes/eu.esa.microwavetbx.sar.op.sentinel1.ui/operators/BackGeocodingOp.html)

![TOPS 공동등록 개념도](/assets/images/insar-seoul/05-coreg/tops-coregistration.png)

그림 2. **개념도.** 기준 영상에 보조 영상을 정합하는 흐름만 설명한다. 프로젝트의 실제 ESD 잔차값은 표시하지 않는다.

다음 공개 글에서는 정합된 후보 자료에 남은 wrapped phase를 살핀다. 기준선 그래프와 위상 지도를 같은 종류의 “변위 결과”로 혼동하지 않는 것이 핵심이다.

앞 글: [AOI와 IW/Burst 범위](/insar-seoul/02-aoi-burst/) · 다음 공개 글: [wrapped phase 점검](/insar-seoul/06-interferogram/)
