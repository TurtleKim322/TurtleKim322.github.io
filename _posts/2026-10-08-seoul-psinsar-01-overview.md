---
title: "서울 Sentinel-1 PS-InSAR 분석 #1 - 프로젝트 개요와 처리 환경"
date: 2026-10-08
permalink: /insar-seoul/01-overview/
categories: [위성]
tags: [Sentinel-1, SAR, InSAR, PS-InSAR, SNAP, StaMPS, Octave]
author_profile: true
toc: true
toc_sticky: true
---

이 글은 Sentinel-1 124장을 이용해 서울 지역을 분석한 PS-InSAR 작업의 출발점과 처리 환경을 정리한다. 이 시리즈는 완료된 계산과 아직 진행 중인 단계를 구분하고, 각 그림이 실제 자료인지 개념도인지 밝힌다.

## SAR, InSAR, PS-InSAR

SAR는 위성에서 마이크로파를 보내고 되돌아온 복소 신호를 기록한다. 두 시기의 SAR 영상에서 같은 산란체의 위상 차를 구하면 지형과 관측 시점 사이의 경로 변화가 섞인 간섭 위상을 얻는다. PS-InSAR는 여러 시기에 걸쳐 위상이 비교적 안정적인 산란체를 골라 장기 변화를 추정하는 방법이다. 간섭 위상은 대기, 궤도 오차, 지형 잔차의 영향도 받으므로 위상만으로 침하량을 단정할 수 없다.

## 분석 조건

| 항목 | 프로젝트 기록 |
|---|---|
| 자료 | Sentinel-1 IW SLC, 124 scene |
| 궤도·기간 | Ascending, relative orbit 127; 2020-01-04–2025-03-26 |
| 편파·subswath | VV, IW2 |
| burst / master | 2–4 / 2022-07-16 |
| 처리 환경 | SNAP, StaMPS, GNU Octave, WSL2 Ubuntu |
| AOI 기록 | 위도 37.4–37.72°, 경도 126.75–127.2° |

좌표 검증 결과, 후보 추출 범위는 AOI 사각형보다 넓다. 따라서 시리즈의 공간 그림은 필요할 때 AOI 경계를 같이 표시하며, 전체 장면을 서울 AOI로 오해하지 않도록 한다.

## 처리 흐름

![서울 PS-InSAR 처리 흐름](/assets/images/insar-seoul/01-environment/pipeline-overview.png)

그림 1. **개념도.** TOPSAR-Split과 궤도 적용부터 StaMPS 처리까지의 순서다. Step 3 이후 결과와 LOS 변위는 이 그림에서 완료된 것으로 표시하지 않았다.

Sentinel-1 SLC를 분리하고 궤도를 적용한 뒤 master와 secondary를 정합한다. 이후 간섭 위상 자료를 StaMPS 입력으로 변환하고 후보를 처리한다. StaMPS 작업 디렉터리에는 20개 PATCH와 124개 영상에 해당하는 자료가 남아 있다. 각 단계의 세부 검증은 다음 글에서 다룬다.

## 시리즈 이동

[전체 시리즈](/insar-seoul/series/) · 다음 글: [AOI와 IW/Burst 선정](/insar-seoul/02-aoi-burst/)
