---
title: "서울 Sentinel-1 PS-InSAR 분석 #2 - AOI와 IW/Burst 범위 확인"
date: 2026-10-08
permalink: /insar-seoul/02-aoi-burst/
categories: [위성]
tags: [Sentinel-1, SAR, PS-InSAR]
author_profile: true
toc: true
---

PS-InSAR의 첫 공간 검증은 “서울을 선택했다”는 설정 문구만 확인하는 일이 아니다. AOI 좌표, SLC의 subswath와 burst 선택, 그리고 최종 후보 좌표가 실제로 어느 범위를 덮는지 서로 대조해야 한다. 이 글은 프로젝트 기록에 남은 AOI와 후보점 범위를 나누어 설명한다.

## IW와 burst

Sentinel-1 IW SLC는 세 개의 subswath(IW1–IW3)로 구성되고, 각 subswath 영상은 azimuth 방향의 burst를 포함한다. TOPS 자료는 burst 경계에서 관측 기하와 위상 연속성을 고려해야 하므로 여러 burst를 이어 쓸 때는 같은 subswath·편파를 선택하고 정합 상태를 확인한다. [ESA Sentinel-1 제품 정의](https://sentiwiki.copernicus.eu/__attachments/1673968/S1-RS-MDA-52-7440-Sentinel-1-Product-Definition-2025-2.8.pdf)

프로젝트 메모에는 VV 편파와 IW2, burst 2–4가 기재되어 있다. 다만 원본 SAFE annotation과 사용한 SNAP GPT/XML 그래프를 현재 자료에서 다시 대조하지 못했으므로, 이는 프로젝트 설정 기록이지 burst footprint를 독립 검증한 결과는 아니다.

![IW2 burst 선택 개념도](/assets/images/insar-seoul/02-burst/iw2-burst-selection.png)

그림 1. **개념도.** 한 subswath 안의 burst 구간과 관심 범위를 고르는 원리를 나타낸다. 실제 서울 지표의 footprint, burst 번호, 경계 좌표를 그린 자료가 아니다.

## AOI와 후보 좌표는 다른 범위

프로젝트에 기록된 AOI는 경도 126.75–127.20°, 위도 37.40–37.72°의 직사각형이다. 이에 비해 PATCH별 후보 자료를 지리 좌표로 그리면 서쪽에 AOI 바깥 점이 포함되고, patch 경계에 따라 관측 범위가 이어진다. 따라서 후보 지도는 AOI 그 자체가 아니라 **처리된 후보점의 공간 분포와 AOI의 중첩**을 보여 준다.

![전체 PATCH의 후보 좌표와 AOI 경계](/assets/images/insar-seoul/07-candidates/ps-candidate-spatial-map.png)

그림 2. PATCH ID별 후보 좌표와 기록된 AOI 사각형. 색은 patch 구분을 위한 범주값이며, 후보 품질이나 변위 크기를 뜻하지 않는다. 일부 영역의 점 밀도는 산란점 후보의 위치를 나타낼 뿐 지표 변화의 크기를 나타내지 않는다.

이 그림을 서울 전체의 PS 결과로 읽으면 안 된다. 후보점은 처리 단계의 산출물이며, 중복·결측 좌표·선택 단계의 영향을 받는다. 지도에 사용한 범위와 개수 집계 방식은 다음 글에서 별도로 구분한다.

## 다시 검증할 때의 체크 항목

SAFE annotation에서 IW2의 burst 시간·좌표 정보를 확인하고, SNAP 그래프에서 subswath, polarization, burst 시작·끝 설정을 대조한다. 그 다음 처리 후 좌표를 동일한 지리 좌표계로 변환하여 AOI와 중첩한다. annotation이 확인되기 전까지 개념도에서 실제 footprint를 추론하거나, AOI 밖 후보를 임의로 잘라 전체 개수를 새로 해석하지 않는다.

앞 글: [프로젝트 개요](/insar-seoul/01-overview/) · 다음 공개 글: [마스터 영상과 기준선](/insar-seoul/04-master/)
