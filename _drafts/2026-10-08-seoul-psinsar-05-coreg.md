---
title: "서울 Sentinel-1 PS-InSAR 분석 #5 - TOPS 공동등록과 ESD 검증 (검증 대기)"
date: 2026-10-08
permalink: /insar-seoul/05-coreg/
categories: [위성]
tags: [Sentinel-1, TOPS, PS-InSAR]
---

> **상태: 공개 전 검증 대기.** 현재 그림은 TOPS 공동등록 원리를 설명하는 개념도다. 프로젝트의 실제 SNAP 그래프와 ESD 잔차 로그를 확보하지 못했으므로, 아래 설명을 수행 완료 기록으로 읽어서는 안 된다.

## 왜 TOPS 공동등록에 정밀 검증이 필요한가

StaMPS에서 여러 시기의 간섭 위상을 비교하려면 같은 지상 산란체가 같은 픽셀 위치로 정렬되어야 한다. SNAP의 Sentinel-1 Back-Geocoding은 두 SLC의 같은 subswath를 궤도와 DEM을 사용해 공통 기준 영상에 정합한다. TOPS 자료에서 여러 burst를 사용하면 azimuth 방향의 작은 정합 오차도 위상 일관성에 민감할 수 있어 ESD(Enhanced Spectral Diversity)로 정합을 보정하는 흐름이 쓰인다. 실제 적용 여부와 설정은 입력 자료와 그래프에서 확인해야 한다. [ESA Back-Geocoding operator](https://step.esa.int/main/wp-content/help/versions/13.0.0/snap-toolboxes/eu.esa.microwavetbx.sar.op.sentinel1.ui/operators/BackGeocodingOp.html)

![TOPS 공동등록 개념도](/assets/images/insar-seoul/05-coreg/tops-coregistration.png)

그림 1. **개념도.** 기준 영상과 보조 영상을 정합하고, 필요한 경우 burst 간 정합을 보정하는 순서를 단순화했다. 이 프로젝트의 실제 위치 오차나 ESD 잔차 그래프가 아니다.

## 124개 영상에서 확인할 항목

최종 글에는 master–secondary 123쌍의 실제 처리 목록, 각 입력의 동일 IW·VV·burst 범위, 궤도 파일 적용 상태, DEM 종류와 보간 설정, Back-Geocoding·ESD 출력 로그를 대조해 기록해야 한다. 성공 개수와 실패 목록, 출력 메타데이터 및 ESD 전후 잔차가 맞아야 처리 품질을 설명할 수 있다. 산출물 파일이 존재한다는 사실 하나만으로 전체 쌍의 정합 성공을 단정하지 않는다.

## 공개 전 필요한 자료

- SNAP 그래프와 버전, 처리 입력 목록
- master 및 각 secondary에 기록된 궤도 적용 상태
- burst 범위가 일치하는지 확인 가능한 출력 메타데이터
- 쌍별 실행 로그와 ESD 잔차 통계
- 실패한 쌍의 재처리 또는 제외 사유

이 자료를 확보하면 실제 설정과 실패 원인을 정리할 수 있다. 그 전까지 이 글은 이론·검증 항목 초안으로 남기고, 개념 그림을 측정 결과처럼 공개하지 않는다.
