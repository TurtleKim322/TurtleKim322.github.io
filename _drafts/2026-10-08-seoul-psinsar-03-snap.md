---
title: "서울 Sentinel-1 PS-InSAR 분석 #3 - SNAP 전처리와 burst 검증 (검증 대기)"
date: 2026-10-08
permalink: /insar-seoul/03-snap/
categories: [위성]
tags: [Sentinel-1, SNAP, TOPS]
---

> **상태: 공개 전 검증 대기.** 이 초안은 전처리 단계의 기술적 맥락을 정리한다. 프로젝트의 실제 입력 범위와 파라미터를 재현할 SAFE annotation, SNAP GPT/XML 그래프와 실행 로그가 확인되기 전까지 아래 흐름을 완료된 작업으로 서술하지 않는다.

## 왜 TOPSAR-Split부터 확인하는가

Sentinel-1 IW SLC에는 IW1–IW3 subswath와 연속 burst가 들어 있다. 관심 영역에 맞는 subswath·편파·burst를 일관되게 선택해야 이후 영상끼리 공통 지상 범위를 비교할 수 있다. annotation의 burst 시간과 좌표, SNAP의 시작·끝 burst 설정을 함께 확인하지 않으면 설정값만으로 실제 footprint를 단정하기 어렵다.

이 프로젝트 기록에는 VV, IW2, burst 2–4가 적혀 있다. 이는 현재 확인되는 메모값이며, 원본 SAFE annotation과 실행 그래프를 다시 대조하지 못했다. 따라서 정확한 burst 경계와 처리 footprint는 확정하지 않는다.

## 재현 시 대조할 처리 순서

검증 대상은 Sentinel-1 SLC 읽기 → TOPSAR-Split → Apply-Orbit-File → master·secondary 제품의 동일 범위 확인 → 후속 정합 입력이다. 여러 장을 batch 처리할 경우 입력 목록의 날짜·상대궤도·편파·제품 타입과 출력 개수를 대조한다. SNAP GPT/XML은 작업을 반복 가능하게 하지만, 스크립트 파일만으로 해당 그래프가 특정 입력에 실제 실행되었다고 증명되지는 않는다. 각 단계의 로그, 출력 메타데이터와 예상 영상 수가 함께 필요하다. [ESA SNAP TOPS 간섭 튜토리얼](https://step.esa.int/docs/tutorials/S1TBX%20TOPSAR%20Interferometry%20with%20Sentinel-1%20Tutorial_v2.pdf)

## 공개 전 필요한 증거

- 실제 사용한 SAFE 제품 식별정보와 annotation의 IW2 burst 범위
- 실행한 GPT/XML의 정합된 사본 및 SNAP 버전
- 영상 124개 목록, 각 처리 단계 성공·실패 수와 로그
- 중간 산출물 메타데이터에서 확인한 편파·subswath·burst·날짜
- 개인 Windows 사용자명과 컴퓨터 이름을 제거한 재현 가능한 명령 예시

증거를 대조한 뒤 실제 설정과 실패 사례, 수정 전후를 기록하고 개념도와 처리 결과 이미지를 명확히 나누어 공개한다. 검증 전에는 프로젝트가 124장 전체를 이 순서로 성공 처리했다고 이 초안에서 주장하지 않는다.
