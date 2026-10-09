---
title: "서울 Sentinel-1 PS-InSAR 분석 #7 - PS 후보를 고르고 PATCH 수를 세기"
date: 2026-10-08
permalink: /insar-seoul/07-candidates/
categories: [위성]
tags: [PS-InSAR, StaMPS]
author_profile: true
toc: true
---

도시의 모든 픽셀이 PS가 되는 것은 아니다. 같은 지점이 날짜가 바뀌어도 레이더 신호를 비교적 안정적으로 돌려주는지 먼저 살펴야 한다. 이 단계에서 뽑힌 위치를 PS candidate(PS 후보)라고 한다. 후보라는 말 그대로, 아직 최종 변위점으로 선택됐다는 뜻은 아니다.

이 프로젝트에서는 평균 진폭에 대한 진폭의 시간적 변동을 나타내는 amplitude dispersion을 후보 선별에 사용했다. 쉽게 말하면, 여러 장의 영상에서 밝기가 얼마나 흔들리는지를 평균 밝기와 비교하는 값이다. 값이 낮으면 반사 세기가 비교적 일정하다는 뜻이다. 기록된 후보 기준은 0.4였지만, 이것만으로 위상 안정성이나 최종 PS 여부까지 판정할 수는 없다.

처리 면적을 한 번에 다루지 않고 5×4, 모두 20개의 PATCH로 나누었다. 큰 자료를 작은 단위로 처리하기 위한 구성이다. PATCH 가장자리에서는 같은 위치가 이웃 영역에도 들어갈 수 있도록 range 방향 50, azimuth 방향 200의 overlap을 두었다. 그래서 PATCH별 행 수를 단순히 더하면 같은 위치가 여러 번 세어질 수 있다.

## 지도와 막대그래프에서 볼 것

아래 막대그래프는 PATCH마다 `pscands.1.ij`에 들어 있는 후보 좌표 행을 센 것이다. 색으로 구분된 PATCH 중 어느 영역의 행이 많은지 볼 수 있지만, 이 수치를 최종 PS 개수로 해석하면 안 된다.

![patch별 후보 행 수](/assets/images/insar-seoul/07-candidates/patch-candidate-count.png)

PATCH 경계 그림은 겹쳐 나누는 이유를 보여 주는 **개념도**다. 실제 처리 경계를 정밀한 좌표로 표시한 그림은 아니다.

![PATCH 경계 중첩 개념도](/assets/images/insar-seoul/07-candidates/patch-boundaries.png)

전체 후보 좌표를 AOI와 함께 그리면 처리 범위가 관심 영역보다 넓다는 것도 보인다. 색은 PATCH 번호를 나타내며 후보의 품질이나 이동량은 아니다.

![전체 PATCH 후보 분포와 AOI 경계](/assets/images/insar-seoul/07-candidates/ps-candidate-spatial-map.png)

## 세 숫자가 서로 다른 이유

PATCH의 `pscands.1.ij` 행을 모두 더하면 3,539,547행이다. 현재 `ps1.mat`의 patch별 `n_ps`를 합하면 3,539,534개다. 두 값의 13행 차이는 좌표를 변환했을 때 위경도가 [NaN, NaN]으로 나온 행이 후보를 불러오는 과정에서 빠진 것과 맞아떨어진다.

예전에 azimuth와 range 좌표쌍으로 중복을 제거한 집계는 2,572,868개였다. 이 값은 현재 `n_ps`의 합과 계산 시점도, 중복 처리 방식도 다르다. 따라서 세 숫자 중 하나를 “전체 고유 PS 수”라고 골라 부를 수 없다. 후보 행, patch별 후보 수, 좌표쌍 중복 제거 결과를 따로 봐야 한다.

후보가 만들어진 뒤에도 StaMPS는 위상 안정성을 추정하고 다시 선택한다. 다음 글에서는 실제 처리 중 입력 자료와 Octave 환경에서 문제가 어떻게 이어졌는지 기록한다.

앞 글: [처음 확인한 wrapped phase](/insar-seoul/06-interferogram/) · 다음: [StaMPS 실행 오류 따라가기](/insar-seoul/08-debug/)
