---
layout: single
title: "SAR 입문: 신호에서 영상까지"
permalink: /sar-basics/series/
author_profile: true
toc: true
toc_sticky: true
---

레이더가 거리를 측정하는 원리부터 SAR 영상이 초점을 맺는 과정까지, 점 표적 시뮬레이터를 따라 차근차근 공부하는 22편의 연재입니다. 각 글에는 수식과 단위, 직접 계산하는 예제, 설명 그림 두 개, 그림을 다시 만드는 Python 코드가 있습니다.

처음에는 아래 순서대로 읽고, 이후에는 필요한 주제를 골라 보세요. 예제는 이상적인 점 표적과 단순화한 기하를 사용합니다. 실제 위성 자료의 전체 처리 절차를 대신하지는 않습니다.

## 전체 목차

| 순서 | 주제 |
|---|---|
| 00 | [SAR 입문 시리즈를 시작하며: 신호에서 영상까지]({{ '/sar-basics/00-start/' | relative_url }}) |
| 01 | [레이더는 거리를 어떻게 측정할까?]({{ '/sar-basics/01-distance/' | relative_url }}) |
| 02 | [파장과 주파수: 10 GHz는 얼마나 짧은 파동일까?]({{ '/sar-basics/02-wavelength/' | relative_url }}) |
| 03 | [복소수와 위상: 크기만 저장하면 무엇을 잃을까?]({{ '/sar-basics/03-complex-phase/' | relative_url }}) |
| 04 | [Chirp: 시간이 흐르면서 주파수가 달라지는 신호]({{ '/sar-basics/04-chirp/' | relative_url }}) |
| 05 | [거리 해상도: 대역폭이 넓으면 왜 더 잘 구분할까?]({{ '/sar-basics/05-range-resolution/' | relative_url }}) |
| 06 | [샘플링: 거리 표본 간격과 해상도는 다르다]({{ '/sar-basics/06-sampling/' | relative_url }}) |
| 07 | [SAR 관측 기하: 움직이는 플랫폼과 고정된 표적]({{ '/sar-basics/07-geometry/' | relative_url }}) |
| 08 | [Fast time과 Slow time: 배열의 두 축 읽기]({{ '/sar-basics/08-fast-slow-time/' | relative_url }}) |
| 09 | [PRF와 PRI: 레이더는 얼마나 자주 신호를 보낼까?]({{ '/sar-basics/09-prf-pri/' | relative_url }}) |
| 10 | [도플러: 거리 변화가 주파수로 보이는 이유]({{ '/sar-basics/10-doppler/' | relative_url }}) |
| 11 | [거리 압축: 긴 chirp를 좁은 응답으로 모으기]({{ '/sar-basics/11-range-compression/' | relative_url }}) |
| 12 | [FFT: 신호를 주파수 성분으로 읽기]({{ '/sar-basics/12-fft/' | relative_url }}) |
| 13 | [Range-Doppler 영역: 방위축을 주파수축으로 바꾸기]({{ '/sar-basics/13-range-doppler/' | relative_url }}) |
| 14 | [RCMC: 휘어진 표적 응답을 같은 거리로 맞추기]({{ '/sar-basics/14-rcmc/' | relative_url }}) |
| 15 | [방위 chirp와 방위 압축: 이동 중 모은 신호 합치기]({{ '/sar-basics/15-azimuth-compression/' | relative_url }}) |
| 16 | [SAR focusing: 처리 단계들은 왜 이 순서일까?]({{ '/sar-basics/16-focusing/' | relative_url }}) |
| 17 | [Hamming 창: 부엽을 줄이면 무엇을 포기할까?]({{ '/sar-basics/17-hamming/' | relative_url }}) |
| 18 | [dB 영상: 약한 표적을 보이게 만드는 표시 방법]({{ '/sar-basics/18-db/' | relative_url }}) |
| 19 | [Zero padding: 표본은 늘어나도 정보는 늘지 않는다]({{ '/sar-basics/19-zero-padding/' | relative_url }}) |
| 20 | [SAR 코드를 읽기 위한 수학·신호처리 로드맵]({{ '/sar-basics/20-roadmap/' | relative_url }}) |
| 21 | [전체 코드 다시 읽기: 입력부터 SAR 영상까지]({{ '/sar-basics/21-code-tour/' | relative_url }}) |

## 그림을 직접 만들어 보기

Python 3 환경에서 필요한 라이브러리를 설치합니다.

```text
python -m pip install numpy matplotlib
```

각 글에서 그림 생성 코드를 내려받아 아래처럼 `figures/` 폴더에 저장하세요. 예를 들어 1편은 `python figures/fig_01_distance.py`로 실행합니다. 그림은 `assets/img/`에 저장됩니다. 그림 생성에는 원본 SAR 시뮬레이터가 필요하지 않습니다.

```text
sar-study/
├── figures/
│   └── fig_01_distance.py
└── assets/
    └── img/
        ├── 01_a.png
        └── 01_b.png
```

## 시뮬레이션 결과와 함께 읽기

- [Python SAR 시뮬레이터 — 점 표적에서 영상까지]({{ '/sar-python/01-simulation/' | relative_url }})
- [Python SAR 시뮬레이터 — 신호를 영상으로 만드는 수학]({{ '/sar-python/02-mathematics/' | relative_url }})
