---
title: "서울 Sentinel-1 PS-InSAR 분석 #9 - StaMPS Step 1–2 진단 결과"
date: 2026-10-08
permalink: /insar-seoul/09-step1-2/
categories: [기술]
tags: [StaMPS, Step 1, Step 2, Coherence, Height]
author_profile: true
toc: true
---

여기 소개하는 coherence, K, height 산출물은 P9 patch의 기존 출력 그림이다. P9 좌표 범위는 경도 126.5181–126.7532°, 위도 37.3654–37.5279°다. 프로젝트 AOI와 대부분 겹치지 않으므로 서울 AOI 전체의 결과로 해석하지 않고, P9 처리 진단 예시로만 제시한다.

![P9 Step 2 coherence histogram](/assets/images/insar-seoul/09-stamps-step1-2/step2-coherence-histogram.png)

![P9 Step 2 coherence map](/assets/images/insar-seoul/09-stamps-step1-2/step2-coherence-map.png)

![P9 K parameter map](/assets/images/insar-seoul/09-stamps-step1-2/step2-kps-map.png)

![P9 candidate height map](/assets/images/insar-seoul/09-stamps-step1-2/candidate-height-map.png)

P9의 Step 2 완료 기록을 확인했다. Step 3도 P9에서 선택 후보 302,481개로 완료됐고 P14에서는 460,353개 선택 기록이 있다. 이것은 모든 patch의 Step 3가 끝났다는 뜻은 아니다. height 파일에는 −32768 sentinel이 포함되므로 이 값을 실제 고도로 해석하지 않는다.

앞 글: [Octave/C 진단](/insar-seoul/08-debug/) · 다음: [당시 저장 공간 기록](/insar-seoul/10-storage/)
