---
title: "문서 비교 프로그램 #9 - Page View가 느린 문제를 해결하기"
date: 2026-10-11
permalink: /document-compare/09-page-performance/
categories: [취미, 개인 프로젝트, 문서 비교 프로그램]
project: document-compare
project_order: 9
tags: ["PyMuPDF", "PyQt6", "Performance"]
author_profile: true
toc: true
toc_sticky: true
description: "Text View에서는 빠르게 움직이던 앱이 Page View에서는 페이지를 넘길 때마다 기다리게 했다. 먼저 시간을 나눠 측정했다. PDF 열기, raster/Pixmap 생성, PNG 저장과 읽기, QImage/QPixmap, overlay와 widget update, 캐시 확인을 따로 살펴봤다."
---

Text View에서는 빠르게 움직이던 앱이 Page View에서는 페이지를 넘길 때마다 기다리게 했다. 먼저 시간을 나눠 측정했다. PDF 열기, raster/Pixmap 생성, PNG 저장과 읽기, QImage/QPixmap, overlay와 widget update, 캐시 확인을 따로 살펴봤다.

## 이미 lazy였는데 왜 느렸을까

이전 버전도 모든 페이지를 미리 그리지 않았다. 지연 렌더링과 제한된 캐시가 있었지만, 미캐시 페이지마다 작업 프로세스를 만들고 PDF를 다시 연 뒤 PNG 임시 파일을 거쳤다. “처음에는 전체 페이지를 렌더했다”는 설명은 실제 코드와 다르다.

120DPI 한 페이지의 컴포넌트 검사에서 native raster는 약 4.3ms였고 PNG 저장은 16.5ms, QImage 디코딩은 12.3ms였다. QPixmap 변환 자체는 약 0.012ms로 작았다. 전체 페이지 이동에는 프로세스 시작과 전달·준비 비용도 들어 있으므로 이 숫자만 합쳐 총 지연이라고 부를 수는 없다.

## 프로세스와 PDF 핸들을 재사용하기

0.4.2는 세션당 격리된 렌더 프로세스 하나를 유지하고 최대 두 PDF 핸들을 재사용한다. MuPDF 작업은 GUI 스레드에서 하지 않는다. PNG 파일 경로 대신 RGB 버퍼를 전달하고 QImage가 소유하는 복사를 만든다. 버퍼 수명 때문에 필요한 복사까지 무리하게 없애지는 않았다.

최종 QPixmap도 캐시한다. 키에는 좌우 구분, PDF 경로와 fingerprint, 페이지, 해상도 단계가 들어간다. LRU는 QImage와 QPixmap 추정 메모리 48MiB 또는 단일 페이지 6개 중 먼저 도달하는 한도로 제한한다. 현재 화면과 작업 프로세스 메모리는 별도다.

## 사용자가 고른 페이지부터

현재 페이지를 먼저 보여 주고 다음 변경 페이지와 인접 페이지 중 최대 두 쌍을 준비한다. 빠른 이동에서는 최신 현재 요청만 남긴다. 늦게 끝난 결과는 캐시에 넣을 수 있어도 현재 화면을 덮지 못하게 했다. 진행 중인 preload 한 작업은 끝날 때까지 기다릴 수 있지만 오래된 요청이 수십 개 쌓이지는 않는다.

확대 중에는 기존 이미지가 즉시 늘어나고 220ms 동안 조작이 멈추면 새 해상도로 렌더한다. resize도 debounce한다. 해상도는 DPR과 표시 폭을 반영해 단계화했다. overlay는 별도 layer라 ON/OFF 때 원본 PDF를 다시 그리지 않는다.

## 같은 조건의 전후 측정

150페이지 합성 PDF 쌍에서 100페이지를 탐색했다. 앱 시작과 텍스트 비교 완료 이후의 개발 환경 측정이며 각 항목 한 번의 실측이다.

| 항목 | 0.4.1 | 0.4.2 |
|---|---:|---:|
| 첫 Page View 진입 | 862ms | 368ms |
| 다음 미캐시 페이지 | 363ms | 44ms |
| 캐시 페이지 | 3.7ms | 1.0ms |
| 이전 페이지 | 5.1ms | 4.9ms |
| 다음 변경 | 422ms | 57ms |
| 확대 preview | 2.7ms | 15.6ms |
| 최대 GUI RSS | 210MiB | 184MiB |

확대 preview는 이 측정에서 빨라지지 않았다. 대신 새 버전에는 후속 고품질 렌더가 생겼다. GUI 메모리는 렌더 자식의 peak를 포함하지 않는다. 50/100페이지 후 GUI+자식 RSS는 약 221/221MiB였고 계속 누적되는 양상은 없었다.

## EXE에서도 따로 확인하기

단일 EXE는 첫 진입 약 242ms, 다음 페이지 44ms, 캐시 약 0.9ms였다. 폴더형은 각각 240/29/0.9ms였다. 앱 시작은 별도로 3회 측정해 중앙값 1.574초와 0.713초를 얻었다. 재부팅 직후 cold start 결과는 아니다.

Word 첫 변환은 여전히 수초가 걸린다. 한컴 지면 변환은 환경 부재로 측정하지 못했다. 더 빠른 수치만 고르기보다 어디까지 줄였고 어떤 비용이 남았는지 구분하는 것이 이번 개선의 결과다.

---

[시리즈 목차](/projects/document-compare/) · 이전: [#8 1GB 입력을 위한 대용량 대응](/document-compare/08-large-documents/) · 다음: [#10 비교 정확도와 성능 최적화 방향](/document-compare/10-accuracy/)
