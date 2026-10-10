---
title: "문서 비교 프로그램 #3 - HWPX와 HWP까지 지원하기"
date: 2026-10-11
permalink: /document-compare/03-hangul/
categories: [취미, 개인 프로젝트, 문서 비교 프로그램]
project: document-compare
project_order: 3
tags: ["HWPX", "HWP", "Python"]
author_profile: true
toc: true
toc_sticky: true
description: "한글 문서를 지원한다고 말하려면 HWP와 HWPX를 나누어 봐야 했다. 확장자가 비슷해도 읽는 경로와 설치 의존성이 다르기 때문이다. 한 형식이 열렸다는 이유로 다른 형식의 지면까지 지원한다고 설명할 수 없었다."
---

한글 문서를 지원한다고 말하려면 HWP와 HWPX를 나누어 봐야 했다. 확장자가 비슷해도 읽는 경로와 설치 의존성이 다르기 때문이다. 한 형식이 열렸다는 이유로 다른 형식의 지면까지 지원한다고 설명할 수 없었다.

## HWPX는 필요한 XML만 읽는다

현재 HWPX 파서는 ZIP 안의 Contents/section0.xml 같은 section 파일을 찾는다. 파일명에 포함된 번호를 숫자로 정렬해 section2가 section10보다 먼저 오게 하고, 문단·표 셀의 텍스트를 공통 블록으로 만든다.

모든 ZIP 항목을 풀 필요는 없다. 이미지가 많아 컨테이너가 커져도 텍스트 비교에 필요한 XML만 읽는다. 다만 필요한 항목만 읽는다는 이유로 압축 폭탄 방어를 없애지는 않았다. 비압축 합계, 항목 수, 큰 항목의 압축 비율, XML 깊이와 엔티티를 검사한다.

이 방식은 텍스트 추출에 한컴 설치를 요구하지 않는다. 대신 실제 지면, 서식, 이미지, 표 병합 구조를 그대로 재현하지 못한다. ZIP/XML을 읽었다는 것과 한글 문서를 화면 그대로 그렸다는 것은 별개의 성과다.

## HWP는 설치된 프로그램의 도움을 받는다

HWP 경로는 Windows의 Hancom Automation을 사용한다. 원본 대신 임시 사본을 열고 읽기 전용 상태에서 텍스트를 추출한다. 이 경로는 한컴 설치와 COM 등록 상태에 의존한다. 사용할 수 없으면 앱 전체를 종료하는 대신 HWPX나 PDF 사본으로 비교하도록 안내한다.

Automation이 전체 텍스트를 문자열로 반환할 수 있어 HWP를 완전한 스트리밍 처리라고 부르지도 않는다. 큰 파일은 작업 프로세스의 자원 한도와 해당 프로그램의 동작에 영향을 받는다.

## Text View와 Page View의 지원 조건

| 입력 | 텍스트 비교 | 원본 지면 보기 |
|---|---|---|
| HWPX | ZIP/XML 파서 | 한컴 PDF 변환 필요 |
| HWP | 한컴 Automation 필요 | 한컴 PDF 변환 필요 |

개발 PC에는 한컴이 없어 HWP/HWPX 실제 지면 변환을 검증하지 못했다. 코드 경로가 있다는 사실과 해당 환경에서 성공을 확인했다는 사실을 구분해 두었다.

저장소의 HWPX 예제도 같은 주의가 필요하다. 직접 생성한 최소 ZIP/XML 파서 fixture여서 텍스트 파서를 확인하는 데 쓰며, 한컴이 작성한 완전한 문서나 PDF 변환 검증 자료로 취급하지 않는다.

## 공통 모델 덕분에 유지한 것

형식별 읽기 방법은 달라도 출력은 Document와 Block이다. HWPX 전용 Diff나 HWP 전용 UI를 따로 만들지 않고, 같은 변경 목록과 검색·문맥 화면을 사용할 수 있었다. 그 다음 문제는 서로 다른 형식에서 만들어진 블록을 어떻게 짝지을지였다.

---

[시리즈 목차](/projects/document-compare/) · 이전: [#2 DOCX와 PDF 비교 엔진 만들기](/document-compare/02-engine/) · 다음: [#4 서로 다른 파일 형식 비교하기](/document-compare/04-cross-format/)
