---
title: "서울 Sentinel-1 PS-InSAR 분석 #7 - 후보점, patch 중첩과 집계 기준"
date: 2026-10-08
permalink: /insar-seoul/07-candidates/
categories: [위성]
tags: [PS-InSAR, StaMPS]
author_profile: true
toc: true
---

PS 후보 수는 어떤 파일과 처리 단계를 세었는지에 따라 달라진다. 이 프로젝트는 20개 PATCH의 `pscands.1.ij` 행, 좌표쌍 중복 제거 결과, 그리고 `ps1.mat`의 patch별 `n_ps`라는 서로 다른 집계를 갖고 있다. 이 값들을 같은 “고유 PS 총수”로 합치지 않고 각각의 의미를 분리한다.

## 세 가지 집계, 세 가지 의미

| 집계 | 확인된 값 | 해석 |
|---|---:|---|
| 20개 PATCH의 `pscands.1.ij` 행 합 | 3,539,547 | patch별 후보 좌표 행의 합. patch 간 중첩을 포함할 수 있음 |
| 좌표쌍을 기준으로 한 과거 중복 제거 | 2,572,868 | azimuth/range 좌표쌍 기준의 이전 집계. 처리 단계와 입력 시점이 현재 `ps1.mat`과 다를 수 있음 |
| 현재 `ps1.mat`의 `n_ps` 합 | 3,539,534 | patch별 StaMPS 초기자료에 기록된 후보 수의 합. patch별 값이며 전체 고유 위치 수가 아님 |

첫 번째와 세 번째 합의 차이는 13행이다. 확인 가능한 좌표 자료에서는 결측 지리좌표 행들이 후보 로딩 과정에서 제외된 차이와 일치한다. 반면 2,572,868은 좌표쌍을 중복 키로 사용한 과거 결과다. patch 경계, 중복 처리 시점과 입력 단계가 다르므로 현재 총 `n_ps`와 일대일로 비교할 수 없다. 이 자료만으로 “서울 전체의 고유 PS가 정확히 몇 개”라고 결론내릴 수는 없다.

## patch 분포와 후보 수

![patch별 원시 후보 행 수](/assets/images/insar-seoul/07-candidates/patch-candidate-count.png)

그림 1. PATCH별 `pscands.1.ij` 행 수. 개수는 후보 행이며, 서로 다른 PATCH 사이에 같은 위치가 포함될 수 있다. 분류된 PS 수나 변위 측정 수를 뜻하지 않는다.

![patch 경계와 중첩 개념도](/assets/images/insar-seoul/07-candidates/patch-boundaries.png)

그림 2. **개념도.** PATCH를 겹치게 나누는 이유와 경계 중복 가능성을 설명한다. 실제 patch 경계의 정밀 좌표 자료는 아니다.

![전체 PATCH 후보 분포와 AOI](/assets/images/insar-seoul/07-candidates/ps-candidate-spatial-map.png)

그림 3. 후보 좌표를 patch별 색으로 표시한 분포. 점은 위상 안정성 선택과 최종 변위 검증이 모두 끝난 결과가 아니다. AOI 사각형 바깥의 후보도 포함되어 있어 서울 AOI 전체 분석 결과와 혼동하지 않도록 했다.

## 후보에서 PS 측정점까지

`pscands.1.ij`는 처리 입력에서 만들어진 좌표 인덱스 행을 담고, `ps1.mat`은 StaMPS가 읽은 후보점과 영상별 보조 정보를 저장한다. 후보점이 있다고 해서 모두 최종 PS로 선택되거나 유효한 시계열을 갖는 것은 아니다. Step 2 gamma 추정과 Step 3의 coherence 기반 선택 같은 후속 처리가 후보를 다시 평가한다. 즉 후보 수, 선택된 점 수, 시계열로 해석 가능한 점 수는 다른 단계의 지표다.

P14에서는 `pscands.1.ij` 행 합과 `ps1.mat`의 `n_ps` 사이에 5행 차이가 확인됐으며, 해당 행들은 지리 좌표가 `[NaN, NaN]`이었다. 다른 patch에서 확인한 결측 행까지 합하면 전체 13행 차이가 맞아떨어진다. 이 관계는 자료 정합 점검에는 유용하지만, patch 중복 집계 문제까지 해소하지는 않는다.

후보점 통계를 재현하려면 같은 자료 버전에서 patch별 입력 행 수, 결측 제거 수, 선택 단계 결과를 따로 남기고, 좌표쌍 중복 제거 키와 순서를 명시해야 한다. 이 시리즈에서는 검증된 결과가 추가되기 전까지 합계 하나를 “전체 고유 PS 수”라고 표기하지 않는다.

앞 글: [wrapped phase 점검](/insar-seoul/06-interferogram/) · 다음: [Octave와 C 처리 진단](/insar-seoul/08-debug/)
