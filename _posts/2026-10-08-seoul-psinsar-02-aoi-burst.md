---
title: "서울 Sentinel-1 PS-InSAR 분석 #2 - AOI와 IW/Burst 후보 범위"
date: 2026-10-08
permalink: /insar-seoul/02-aoi-burst/
categories: [기술]
tags: [Sentinel-1, SAR, PS-InSAR, StaMPS]
author_profile: true
toc: true
---

이 글은 프로젝트 기록에 남은 AOI와 IW2 처리 범위를 정리한다. 원본 SAFE annotation과 SNAP 처리 그래프는 현재 작업 디렉터리에서 확인할 수 없어, burst 선택 그림은 설명용 도식으로 표시한다. 실제 footprint를 확인한 것처럼 해석하지 않는다.

## 분석 범위와 AOI

프로젝트 AOI는 위도 37.40–37.72°, 경도 126.75–127.20°로 기록되어 있다. 후보점 추출 결과의 좌표를 확인하면 전체 추출 범위는 AOI보다 넓다. 따라서 지도에는 추출 footprint와 AOI 경계를 함께 보여 주며, 모든 후보점이 AOI 내부라고 간주하지 않는다.

![IW2 burst 선택 개념도](/assets/images/insar-seoul/02-burst/iw2-burst-selection.png)

그림은 IW2와 burst 선택의 개념을 설명한다. 원본 annotation을 다시 대조하지 못했으므로 실제 burst footprint의 증거가 아니다.

## 후보점의 공간 분포

![후보점 공간 분포와 AOI](/assets/images/insar-seoul/07-candidates/ps-candidate-spatial-map.png)

원시 후보 행은 patch 간 중복을 포함한다. azimuth/range 좌표쌍으로 중복을 제거하면 전체 2,572,868개이고, AOI 경계 안의 고유 좌표쌍은 1,555,954개다. AOI 내부 원시 행은 2,108,270개다. 이 차이는 후보 추출 범위가 AOI로 잘리지 않은 결과와 patch 경계 중복을 각각 반영한다.

### 확인이 필요한 항목

실제 SAFE annotation, SNAP GPT/XML 및 burst별 footprint가 복구되면 원본 선택 결과와 대조할 수 있다. 그때까지 도식은 개념 설명으로만 사용한다.

이전: [프로젝트 개요](/insar-seoul/01-overview/) · 다음: [마스터 영상과 기준선](/insar-seoul/04-master/)
