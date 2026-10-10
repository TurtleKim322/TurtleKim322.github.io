---
title: "서울 Sentinel-1 PS-InSAR 분석 #10 - WSL 저장공간이 부족해졌을 때"
date: 2026-10-08
permalink: /insar-seoul/10-storage/
categories: [취미, 개인 프로젝트, 서울 PS-InSAR, 프로그래밍, 신호처리]
project: seoul-psinsar
project_order: 8
tags: [PS-InSAR, WSL2, 데이터 관리]
author_profile: true
toc: true
description: "Step 2를 돌리던 중 Octave에서 Input/output error와 Bus error가 나오기 시작했다. 처음에는 계산 문제라고 생각했다. 그런데 WSL 안에서 df -h를 확인했을 때는 공간이 충분해 보였다. 이상해서 Windows C: 드라이브의 여유 공간을 따로 봤고, 그쪽이 거의 바닥난 상태라는 걸 알게 됐다."
---

Step 2를 돌리던 중 Octave에서 `Input/output error`와 `Bus error`가 나오기 시작했다. 처음에는 계산 문제라고 생각했다. 그런데 WSL 안에서 `df -h`를 확인했을 때는 공간이 충분해 보였다. 이상해서 Windows C: 드라이브의 여유 공간을 따로 봤고, 그쪽이 거의 바닥난 상태라는 걸 알게 됐다.

WSL2의 Ubuntu는 Windows 안의 가상 디스크 파일 `ext4.vhdx`에 저장된다. Linux에서 보는 파일시스템 여유 공간과 Windows가 실제로 확보해야 하는 C: 공간은 같은 숫자가 아니다. Linux에서 파일을 지우면 내부에서는 빈 공간이 생겨도, 가상 디스크 파일 크기가 바로 줄어든다고 보장할 수 없다.

![WSL과 Windows 저장공간의 관계](/assets/images/insar-seoul/10-storage/wsl-storage-architecture.png)

그림은 두 공간의 관계를 보여 주는 **개념도**다. 실제 디스크 사용량을 측정한 결과나 복구 명령 실행 화면은 아니다.

## 계산이 커지며 어디에 쌓였나

124개 영상과 PATCH를 처리하면서 입력·중간 자료가 많이 필요했다. 당시 기록에는 `ZIP124`가 약 546.3 GB, 작업 복사본 `stamps_final`이 약 192 GB로 적혀 있다. C:의 여유 공간은 약 1 GB까지 줄었고, 중간 파일을 정리한 뒤 약 762 GB를 확보했다는 메모가 남아 있다. 지금의 PC 용량이나 파일 크기를 나타내는 숫자는 아니다.

당시 흐름을 다시 보면, 산출물이 늘면서 ext4.vhdx가 커졌고 C: 공간이 부족해졌다. 그 뒤 입력·출력 오류와 Bus error가 나와서 WSL 상태와 저장공간을 함께 확인했다. Linux의 `df -h`만 봐서는 Windows 쪽 문제가 잘 드러나지 않았던 셈이다.

비슷한 상황에서 먼저 읽기 전용으로 확인할 수 있는 명령은 다음과 같다.

```bash
df -h
du -sh ~/seoul_stamps_work
```

첫 명령은 Linux 파일시스템의 사용량을, 두 번째는 작업 폴더의 크기를 본다. 둘 다 파일을 바꾸거나 지우지 않는다. Windows 드라이브 여유 공간은 Windows에서도 별도로 확인해야 한다.

## 정리할 때 더 조심하게 된 부분

공간이 부족하다고 바로 파일을 지우면 안 된다. 중간 파일처럼 보여도 아직 처리 중인 작업의 입력일 수 있고, 다시 만들 수 없는 유일한 결과일 수도 있다. 정리 전에 경로와 크기, 해당 파일을 사용하는 단계, 백업 여부를 확인해야 한다. WSL을 종료하거나 가상 디스크를 축소하는 작업도 실행 중인 분석에 영향을 줄 수 있으므로 여기서는 현재 따라 할 명령으로 싣지 않는다.

이 기록의 숫자는 과거 상황을 설명할 뿐, 지금도 같은 파일을 정리해야 한다는 뜻이 아니다. 이 시리즈도 모든 PATCH의 변위 분석까지 끝난 것은 아니다. 확인된 입력, 처리 로그와 일부 patch 결과를 차례로 공개하고, 아직 자료가 없는 단계는 검증 대기라고 남겨 둔다.

앞 글: [P9 후보 안정성 확인](/insar-seoul/09-step1-2/) · [시리즈 목차](/insar-seoul/series/)
