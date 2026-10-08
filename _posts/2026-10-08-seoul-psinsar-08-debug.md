---
title: "서울 Sentinel-1 PS-InSAR 분석 #8 - Octave와 C 처리 진단"
date: 2026-10-08
permalink: /insar-seoul/08-debug/
categories: [기술]
tags: [PS-InSAR, StaMPS]
author_profile: true
toc: true
---

StaMPS 처리 중에는 입력 바이너리의 자료형과 byte order, 후보점 행 정합, Octave 함수 및 컴파일된 보조 프로그램을 함께 확인해야 한다. 이 프로젝트에서는 big-endian 입력 검증과 보정 작업이 진행되었다는 실행 기록이 남아 있다. 원본 RSLC 파일은 현재 제거되어 있어 이 글에서 원시 바이너리를 독립 재검증했다고 주장하지 않는다.

현재 확인 가능한 소스에는 `calamp.c`, `selpsc_patch.c`, `selsbc_patch.c`가 있으며 관련 swap 함수의 반환형은 `void`다. Octave signal 패키지 1.4.7도 설치 목록에서 확인했다. 파라미터 파일은 텍스트 `parms`와 실행 시 읽는 `parms.mat`를 구분해야 한다. 현재 `getparm.m`은 `parms.mat`를 가리킨다.

진단 순서는 입력 파일 크기와 행 수 확인, 좌표/위상 결측 정합, 자료형 및 endian 확인, Octave 패키지와 파라미터 확인, 마지막으로 patch 단위 로그 확인이다. 대용량 `pm1.mat`는 이 검증 과정에서 전체 메모리로 읽지 않았다.

![처리 파이프라인 개요](/assets/images/insar-seoul/01-environment/pipeline-overview.png)

앞 글: [후보점 정합](/insar-seoul/07-candidates/) · 다음: [Step 1–2 진단 산출물](/insar-seoul/09-step1-2/)
