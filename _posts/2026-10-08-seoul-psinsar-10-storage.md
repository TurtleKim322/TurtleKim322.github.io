---
title: "서울 Sentinel-1 PS-InSAR 분석 #10 - 당시 WSL 저장 공간과 데이터 관리"
date: 2026-10-08
permalink: /insar-seoul/10-storage/
categories: [기술]
tags: [PS-InSAR, StaMPS]
author_profile: true
toc: true
---

이 글의 용량 수치는 현재 디스크 상태가 아니라 프로젝트 작업 당시 기록이다. 당시 WSL의 ext4 가상 디스크가 커지면서 Windows C: 여유 공간이 약 1 GB까지 줄어든 상황을 조사했다. 기록에는 ZIP124 약 546.3 GB, `stamps_final` 약 192 GB가 적혀 있다.

![WSL과 Windows 저장 구조 개념도](/assets/images/insar-seoul/10-storage/wsl-storage-architecture.png)

작업 기록에는 불필요한 중간 파일을 정리한 뒤 약 762 GB 여유 공간을 확보했다고 되어 있다. 이 수치들은 당시 메모를 옮긴 것이며 현재 용량이나 파일 존재를 나타내지 않는다. 재현 가능한 운영 절차에는 삭제 전 경로·용량 확인, 처리 중인 입력/출력 보존, 결과 백업과 실제 사용량 재측정이 포함되어야 한다.

앞 글: [P9 Step 1–2 진단](/insar-seoul/09-step1-2/) · [시리즈 목차](/insar-seoul/series/)
