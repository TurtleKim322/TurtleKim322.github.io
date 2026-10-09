---
title: "서울 Sentinel-1 PS-InSAR 분석 #2 - 서울이 들어가는 IW와 Burst 찾기"
date: 2026-10-08
permalink: /insar-seoul/02-aoi-burst/
categories: [프로그래밍, 신호처리]
tags: [Sentinel-1, SAR, PS-InSAR]
author_profile: true
toc: true
---

서울 좌표만 정하면 바로 영상 처리를 시작할 수 있을 것 같았다. 그런데 Sentinel-1 IW SLC 한 장은 사진 한 장처럼 단순하지 않다. IW1, IW2, IW3라는 세 개의 subswath(관측 띠)로 나뉘고, 각 띠 안에는 짧은 구간의 영상인 burst가 이어져 있다. 관심 지역이 어느 띠와 burst에 들어가는지 알아야 불필요한 자료를 줄이고, 날짜가 다른 영상에서도 같은 범위를 비교할 수 있다.

프로젝트 기록에는 VV 편파와 IW2, burst 2–4를 선택한 것으로 적혀 있다. 편파는 레이더파를 보내고 받는 방향 조합을 뜻한다. 다만 현재 원본 SAFE annotation과 SNAP 그래프는 찾지 못했다. 그래서 이 설정은 당시 기록으로 소개하고, 실제 burst 경계나 footprint를 원본에서 다시 확인했다고 말하지 않는다.

![IW2 burst 선택 개념도](/assets/images/insar-seoul/02-burst/iw2-burst-selection.png)

그림 1은 burst 선택이 어떤 과정인지 보여 주는 **개념도**다. 서울의 실제 위성 촬영 footprint나 burst 경계를 그린 지도가 아니다. 원본 annotation을 확보하면 경도·위도 좌표와 burst 시간 정보를 대조해 다시 확인해야 한다.

## AOI 사각형과 처리 범위가 달랐다

관심 영역(AOI)은 분석하고 싶은 곳을 좌표로 둘러싼 범위다. 이 프로젝트에서는 경도 126.75–127.20°, 위도 37.40–37.72°로 기록했다. 하지만 후보점 좌표를 지도에 올려 보니 AOI 바깥에도 점들이 남아 있었다. 후보점이 만들어진 영상 영역 전체가 AOI와 정확히 일치하지 않았기 때문이다.

![전체 PATCH 후보 분포와 AOI 경계](/assets/images/insar-seoul/07-candidates/ps-candidate-spatial-map.png)

그림 2에서 점의 색은 PATCH를 구분하기 위한 것이고, 높이나 움직임의 크기가 아니다. 점은 처리 과정에서 뽑힌 후보 위치이므로 최종 PS나 변위 측정 결과로 보면 안 된다. 점 분포가 AOI 바깥까지 이어지는 것도 그 이유다.

처음 좌표를 확인할 때 특히 주의할 점은 후보 좌표 파일이 radar coordinate(영상의 행·열 위치)인지 geographic coordinate(위도·경도)인지 구분하는 것이다. `ij`의 행과 열만으로 위경도를 읽을 수 없다. 이 지도는 변환된 지리 좌표를 사용한다. 원본 SAFE annotation과 SNAP 처리 기록을 대조하기 전까지는 이 자료만으로 IW2 burst의 정확한 경계를 단정할 수 없다.

## 이 단계가 끝나면

IW와 burst를 고르면 master와 나머지 영상이 비교할 공통 범위를 정할 수 있다. 다음에는 기준 영상(master)을 정한다. 기준 영상을 바꾼다고 지표가 움직이는 것은 아니지만, 어떤 영상쌍을 만들고 비교할지에 영향을 준다.

앞 글: [서울을 레이더로 살펴보기](/insar-seoul/01-overview/) · 다음 공개 글: [기준 영상과 수직 기준선](/insar-seoul/04-master/)
