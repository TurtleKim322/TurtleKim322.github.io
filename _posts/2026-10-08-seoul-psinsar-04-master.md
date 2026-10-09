---
title: "서울 Sentinel-1 PS-InSAR 분석 #4 - 기준 영상은 어떻게 골랐나"
date: 2026-10-08
permalink: /insar-seoul/04-master/
categories: [취미, 개인 프로젝트, 서울 PS-InSAR, 프로그래밍, 신호처리]
project: seoul-psinsar
project_order: 3
tags: [Sentinel-1, InSAR, PS-InSAR]
author_profile: true
toc: true
---

날짜가 다른 SAR 영상을 나란히 비교하려면 먼저 한 장을 기준으로 정해야 한다. 그 영상을 master, 나머지 영상을 secondary라고 부른다. 모든 secondary는 master와 같은 지상 위치가 겹치도록 정합한다. 이 프로젝트에서 기록된 master는 **2022년 7월 16일** 영상이다.

날짜만 확인하고 넘어가기보다, 각 영상이 기준 영상과 어떤 관측 기하를 갖는지도 살펴봤다. 아래 그래프는 P9의 `ps1.mat`에 들어 있는 영상 날짜와 수직 기준선 값으로 만들었다. 수직 기준선(perpendicular baseline)은 master와 각 영상의 궤도 위치가 얼마나 떨어져 있는지 나타내는 값이다. 기하 차이가 커지면 간섭 위상에서 지형의 영향도 달라질 수 있다.

![P9 영상의 획득일과 수직 기준선](/assets/images/insar-seoul/04-master/baseline-time-network.png)

그림을 볼 때는 두 가지를 구분하면 된다. 가로축의 날짜는 시간 간격을, 기준선 값은 궤도 기하 차이를 보여 준다. P9 자료에는 124개 영상이 있고, master index는 65다. 기준선은 −252.054 m에서 +481.418 m 사이에 분포한다. 이것은 P9 산출물의 값이지, 서울 전체의 변위나 master의 우수성을 나타내는 지표는 아니다.

기준 영상이 왜 이 날짜로 정해졌는지는 현재 남아 있는 자료만으로 설명하기 어렵다. 기준선과 날짜 그림은 선택 결과를 보여 주지만, 다른 후보 날짜보다 최적이었다는 비교 기록은 아니다. 그 이유를 확인하지 못한 부분은 추측해서 채우지 않았다.

## 다음은 영상끼리 맞추는 일

master와 secondary를 정했다고 바로 위상 차를 계산할 수 있는 것은 아니다. 같은 도로가 두 영상에서 서로 다른 픽셀에 놓이면, 픽셀 간 차이는 지표 변화가 아니라 위치 오차일 수 있다. 두 영상을 같은 좌표에 맞추는 과정을 coregistration(공동등록)이라고 한다.

Sentinel-1 TOPS 자료는 burst 경계와 azimuth 방향의 작은 오차에도 민감하다. 그래서 SNAP에서는 궤도와 지형 정보를 사용한 Back-Geocoding으로 secondary를 master 기준으로 옮기고, 여러 burst를 썼다면 ESD로 미세 정합을 보정하는 작업이 이어질 수 있다. 아래 그림은 원리만 나타낸 **개념도**다. 이 프로젝트의 실제 ESD 측정값이나 처리 완료 로그는 아니다. [SNAP Back-Geocoding 설명](https://step.esa.int/main/wp-content/help/versions/13.0.0/snap-toolboxes/eu.esa.microwavetbx.sar.op.sentinel1.ui/operators/BackGeocodingOp.html)

![TOPS 공동등록 개념도](/assets/images/insar-seoul/05-coreg/tops-coregistration.png)

여기까지가 날짜와 촬영 기하를 정리하는 준비다. 다음 공개 글에서는 남아 있는 P9 위상 배열에서 여러 날짜의 색이 어떻게 바뀌는지 살펴본다. 아직 최종 변위 그림은 아니므로, 위상색을 곧바로 침하량으로 읽지 않는 방법도 함께 설명한다.

앞 글: [서울 AOI와 IW/Burst 범위](/insar-seoul/02-aoi-burst/) · 다음 공개 글: [간섭 위상과 wrapped phase](/insar-seoul/06-interferogram/)
