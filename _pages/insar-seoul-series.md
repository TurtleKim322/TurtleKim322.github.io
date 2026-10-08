---
title: "서울 Sentinel-1 PS-InSAR 기술 블로그 시리즈"
permalink: /insar-seoul/series/
author_profile: true
---

서울 지역 Sentinel-1 시계열을 StaMPS로 처리한 과정을 검증 가능한 자료와 설명용 개념도를 구분해 기록한다. P9 결과는 AOI 바깥에 놓인 진단 patch로 표시하고, 원본 로그가 없는 전처리/공동등록 단계는 검증 대기 상태로 둔다.

## 공개 글

1. [프로젝트 개요](/insar-seoul/01-overview/)
2. [AOI와 IW/Burst 후보 범위](/insar-seoul/02-aoi-burst/)
3. [마스터 영상과 수직 기준선](/insar-seoul/04-master/)
4. [간섭 위상 점검](/insar-seoul/06-interferogram/)
5. [후보점과 patch 중복 검증](/insar-seoul/07-candidates/)
6. [Octave와 C 처리 진단](/insar-seoul/08-debug/)
7. [StaMPS Step 1–2 진단 결과](/insar-seoul/09-step1-2/)
8. [당시 WSL 저장 공간과 데이터 관리](/insar-seoul/10-storage/)

## 검증 대기

- #3 SNAP 전처리: SAFE annotation, burst별 설정과 실제 processing graph 대조 필요.
- #5 TOPS 공동등록: ESD 잔차 로그와 실제 SNAP 그래프 대조 필요.

이 목차는 시리즈 전체가 완성되었다는 의미가 아니다. Step 3 이후의 전체 patch 분석과 LOS 변위 해석은 별도 검증 후 추가한다.
