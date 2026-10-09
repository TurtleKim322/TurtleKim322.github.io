---
layout: single
title: "서울 Sentinel-1 PS-InSAR 기술 블로그 시리즈"
permalink: /insar-seoul/series/
categories: [취미, 개인 프로젝트, 서울 PS-InSAR]
project: seoul-psinsar
author_profile: true
toc: true
---

서울 Sentinel-1 시계열을 StaMPS로 처리한 과정을 데이터 근거, 개념 설명, 검증 상태로 나누어 기록한다. 각 결과 그림에는 patch와 측정량을 적고, AOI 전체 결과인지 진단용 patch인지 구별한다. 시리즈에 글이 있다는 사실을 전체 처리가 끝났다는 의미로 해석하지 않는다.

## 공개 글

- **#1** [프로젝트 범위와 처리 환경](/insar-seoul/01-overview/)
- **#2** [AOI와 IW/Burst 범위](/insar-seoul/02-aoi-burst/)
- **#4** [기준 영상과 수직 기준선](/insar-seoul/04-master/)
- **#6** [간섭 위상과 wrapped phase](/insar-seoul/06-interferogram/)
- **#7** [후보점, patch 중첩과 집계](/insar-seoul/07-candidates/)
- **#8** [StaMPS 실행 오류 진단](/insar-seoul/08-debug/)
- **#9** [P9 StaMPS Step 1–3 진단 결과](/insar-seoul/09-step1-2/)
- **#10** [당시 WSL 저장공간과 복구 기록](/insar-seoul/10-storage/)

## 검증 대기

- **#3 SNAP 전처리:** 검증 초안은 비공개 상태다. SAFE annotation, 실행한 GPT/XML, 124개 영상의 성공·실패 로그 대조가 필요하다.
- **#5 TOPS 공동등록:** 검증 초안은 비공개 상태다. 실제 master–secondary 쌍 목록, Back-Geocoding 설정과 ESD 잔차 로그 대조가 필요하다.

P9와 P14 로그에서 Step 3의 선택 완료 기록을 확인했지만, 이것은 해당 patch들의 기록이다. 나머지 PATCH의 처리 상태와 최종 LOS 시계열은 별도로 검증해야 하며, 현재 공개 글은 서울 전체의 변위 제품을 주장하지 않는다.
