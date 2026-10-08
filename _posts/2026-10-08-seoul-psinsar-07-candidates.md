---
title: "서울 Sentinel-1 PS-InSAR 분석 #7 - 후보점과 patch 중복 검증"
date: 2026-10-08
permalink: /insar-seoul/07-candidates/
categories: [기술]
tags: [PS-InSAR, StaMPS]
author_profile: true
toc: true
---

20개 patch의 `pscands.1.ij` 행을 세면 총 3,539,547행이다. 이는 patch 경계 중복을 포함한 원시 행 수다. `ij`의 azimuth/range 좌표쌍으로 중복을 제거한 고유 후보는 2,572,868개다.

![patch별 원시 후보 행 수](/assets/images/insar-seoul/07-candidates/patch-candidate-count.png)

![patch 경계와 중첩 개념도](/assets/images/insar-seoul/07-candidates/patch-boundaries.png)

P14의 원시 행 수 463,633과 `ps1.mat`의 463,628개 사이에는 5개 차이가 있다. 후보 좌표 파일에서 이 다섯 행은 모두 `[NaN, NaN]` 지오코딩이며, `ps_load_initial_gamma.m`은 좌표나 위상이 NaN인 행을 제거한다. 나머지 patch에서 확인한 차이 8개도 같은 필터링으로 설명되어 전체 13개 차이가 정합된다.

AOI 내부 고유 후보 좌표쌍은 1,555,954개다. 전체 footprint와 AOI를 혼동하지 않도록 공간 분포 그림에는 AOI 경계를 함께 표시했다.

앞 글: [간섭 위상](/insar-seoul/06-interferogram/) · 다음: [Octave/C 처리 진단](/insar-seoul/08-debug/)
