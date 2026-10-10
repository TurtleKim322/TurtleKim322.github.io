---
title: "SAR 기초 16 — SAR focusing: 처리 단계들은 왜 이 순서일까?"
date: 2026-10-10
last_modified_at: 2026-10-10
date_format: "%Y년 %m월 %d일"
categories: [SAR, 신호처리]
tags: [SAR, Radar, Python, Signal Processing]
permalink: /sar-basics/16-focusing/
series: sar-basics
series_order: 16
toc: true
toc_sticky: true
math: true
header:
  teaser: /assets/img/sar-basics/16_a.png
description: "SAR focusing은 하나의 필터 이름이 아니라 원시 복소수 신호를 거리와 방위 위치에 모으는 전체 과정이다. 각 단계가 어떤 정보를 바꾸고 무엇을 보존하는지 따라가며 처리 순서를 정리한다."
---

## 한 줄 요약

SAR focusing은 하나의 필터 이름이 아니라 원시 복소수 신호를 거리와 방위 위치에 모으는 전체 과정이다. 각 단계가 어떤 정보를 바꾸고 무엇을 보존하는지 따라가며 처리 순서를 정리한다.

## 왜 중요한가

거리 압축, RCMC, 방위 압축을 각각 이해해도 연결 순서를 놓치면 코드 전체가 다시 복잡해 보인다. 단계별 배열의 축과 신호 표현을 적어 두면 중간 결과를 검토하고 오류가 시작되는 위치를 좁힐 수 있다.

## 핵심 개념

원시 데이터에는 긴 수신 펄스와 플랫폼 이동에 따른 위상 이력이 함께 들어 있다. 먼저 각 펄스 내부에서 기준 chirp와 상관하여 거리 방향 응답을 모은다. 그다음 관심 거리 구간을 선택하고 느린 시간 방향으로 FFT한다.

거리-도플러 영역에서는 도플러별 거리 이동을 보정한다. 이어 거리별 방위 기준 신호의 스펙트럼과 켤레 곱을 수행하고 역 FFT하여 방위 위치별 응답으로 돌아온다. 이때까지 복소수 신호를 유지한다.

마지막으로 좌표를 맞추고 진폭이나 dB로 표시한다. 표시용 절댓값과 clipping은 영상 형성 계산과 구분한다. 중간 스펙트럼에 밝은 무늬가 있다고 해서 이미 지상 위치별 영상이 완성된 것은 아니다.

## 핵심 수식

<div class="sar-math">
\[
X(t,\eta)\xrightarrow{\text{range correlation}}S_{rc}(r,\eta)\xrightarrow{\mathcal F_\eta}S_{RD}(r,f_D)\xrightarrow{\mathrm{RCMC}}S_c(r,f_D)\xrightarrow{\mathcal F_\eta^{-1}\{\cdot H_a\}}I(r,\eta)
\]
</div>

| 기호 | 의미 | 축 단위 |
|---|---|---|
| X | 원시 데이터 | t: s, η: s |
| Src | 거리 압축 결과 | r: m, η: s |
| SRD, Sc | 방위 FFT 결과와 이동 보정 결과 | r: m, fD: Hz |
| Ha | 방위 기준 스펙트럼의 켤레 | 정규화에 따름 |
| I | 집속된 복소수 영상 | r: m, η 또는 변환한 y |

## 수식의 물리적 의미

두 방향의 집속은 모두 신호의 예상 패턴을 이용해 위상을 정렬하는 과정이다. RCMC는 그 사이에서 신호가 위치한 거리 행을 맞춘다. 역 FFT는 주파수 표현을 다시 방위 표본으로 되돌리며, 물리적 거리와 위치의 원점은 별도 좌표 계산으로 붙인다.

## 현재 SAR 코드와 연결

```python
# Educational summary of the operations in the source.
range_spectrum = np.fft.fft(raw, n_range_fft, axis=0)
range_compressed = np.fft.ifft(range_spectrum * range_reference_conj[:, None], axis=0)
rd = np.fft.fft(range_compressed[range_slice], n_az_fft, axis=1)
# For each Doppler column: interpolate complex values at r / D(fd).
# For each range row: multiply by the conjugate azimuth reference spectrum.
image = np.fft.fftshift(np.fft.ifft(rd_corrected * azimuth_reference_conj, axis=1), axes=1)
```

이 코드는 원본의 처리 순서를 축이 드러나도록 요약한 의사코드이며, raw·필터·보정 배열을 정의하지 않은 채 단독 실행하는 프로그램은 아니다. 원본은 거리와 방위 처리를 반복문으로 수행한다. 실제 처리식과 별개로 글 아래의 그림 생성 코드는 독립 실행할 수 있다.

코드 위치: `SAR_python.py` 181행 부근 / `SAR_m.m` 93행 부근. 본문의 짧은 코드는 해당 연산을 발췌하거나 설명을 위해 정리한 것이다. 분석 기준은 직접 실험한 점 표적 SAR 시뮬레이터다. 이 연재에서는 신호처리 원리와 수학에 집중한다.

## 시각적 설명

![처리 블록 다이어그램]({{ '/assets/img/sar-basics/16_a.png' | relative_url }})

그림 A는 계산 순서를 정리한 블록 도식이다. 방위 필터와 역 FFT를 분리해 마지막 집속이 어디서 끝나는지 보이게 했다.

![시간·주파수 축의 변화]({{ '/assets/img/sar-basics/16_b.png' | relative_url }})

그림 B는 세 처리 영역의 축을 비교한다. 사각형은 배열의 좌표계를 나타내며 실제 관측 영상이나 처리 성능 그림이 아니다.

## 그림 생성 코드

아래 코드는 [figures/fig_16_focusing.py]({{ '/assets/code/sar-basics/fig_16_focusing.py' | relative_url }})에도 저장되어 있다. NumPy와 Matplotlib만 사용하며, 해당 경로에 파일을 두고 실행하면 현재 작업 폴더와 관계없이 `assets/img/`에 PNG 두 개를 저장한다. 그림의 영문 축·단위는 본문 캡션과 함께 읽는다.

```python
# Output: assets/img/16_a.png and 16_b.png
# Standalone educational figures; NumPy + Matplotlib only.
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parents[1] / "assets" / "img"
OUT.mkdir(parents=True, exist_ok=True)
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11,
    "axes.spines.top": False, "axes.spines.right": False,
    "figure.facecolor": "white", "savefig.facecolor": "white"})
C, FC, B, TP, FS, V = 3e8, 10e9, 200e6, 5e-6, 250e6, 100.
LAM = C / FC
THETA = np.deg2rad(3.)
BD = 2 * V * THETA / LAM
PRF, PRI = 1.5 * BD, 1 / (1.5 * BD)
R0 = 5025.
BLUE, PURPLE, ORANGE = "#087e8b", "#70549c", "#df8338"

def new(title, xlabel="", ylabel="", size=(9, 4.8)):
    fig, ax = plt.subplots(figsize=size, layout="constrained")
    ax.set(title=title, xlabel=xlabel, ylabel=ylabel)
    ax.grid(alpha=.18)
    return fig, ax

def save(fig, name):
    fig.savefig(OUT / name, dpi=200, bbox_inches="tight")
    plt.close(fig)

def db(z, floor=-80):
    a = np.abs(z)
    return np.maximum(20 * np.log10(np.maximum(a / max(a.max(), 1e-15), 1e-12)), floor)

def boxes(labels, name, title):
    fig, ax = plt.subplots(figsize=(11, 4.3), layout="constrained")
    ax.set(xlim=(-.6, 2.6), ylim=(-.6, 1.6), title=title)
    ax.axis("off")
    points = [(0,1),(1,1),(2,1),(2,0),(1,0),(0,0)]
    for i, (label, (x,y)) in enumerate(zip(labels, points)):
        if len(label) > 20:
            label = label.replace(" / ", chr(10) + "/ ")
        ax.text(x,y,label,ha="center",va="center",fontsize=12,
            bbox=dict(boxstyle="round,pad=.6",fc="#edf5f6",ec=BLUE))
        if i:
            px,py=points[i-1]
            dx,dy=x-px,y-py
            ax.annotate("",xy=(x-.3*dx,y-.2*dy),xytext=(px+.3*dx,py+.2*dy),
                arrowprops=dict(arrowstyle="->",lw=2,color=PURPLE))
    save(fig,name)

boxes(["Complex raw data", "Range correlation", "Azimuth FFT", "RCMC", "Azimuth filter", "IFFT -> image"], "16_a.png", "Range-Doppler processing order")
fig,axes=plt.subplots(1,3,figsize=(12,4),layout="constrained")
for ax,title,xlabel,ylabel in zip(axes,["Raw echoes","Range-Doppler","Focused image"],["Slow time eta","Doppler fD","Azimuth y"],["Fast time t","Range r","Range r"]):
    ax.add_patch(plt.Rectangle((.1,.1),.8,.8,facecolor="#edf5f6",edgecolor=BLUE,lw=2))
    ax.set(title=title,xlabel=xlabel,ylabel=ylabel,xticks=[],yticks=[],xlim=(0,1),ylim=(0,1))
    ax.text(.5,.5,"Complex samples",ha="center",va="center")
fig.suptitle("Coordinate domains, not three photographs"); save(fig,"16_b.png")
```

## 숫자 예제

실행한 Python의 배열 흐름은 2083×1642 → 4096×1642 → 251×1642 → 251×4096이다. 마지막 두 차원은 거리 행과 0 채우기를 포함한 방위 길이다. 복소수 영상에서 진폭을 꺼내 20log10으로 표시하며 최대값을 0 dB로 맞춘다.

## 직접 확인해 보기

각 단계에 들어가기 전에 배열의 shape와 좌표 길이를 출력해 보자. 거리 좌표 길이가 행 수와 같고 도플러 좌표 길이가 열 수와 같은지 확인하면 많은 축 오류를 빠르게 찾을 수 있다.

## 요약 / 핵심 공식 / 코드 위치

- 거리 압축 후 방위 FFT와 RCMC, 방위 압축이 이어진다.
- 마지막 표시 단계 전까지 복소수 정보를 유지한다.
- 단계마다 배열 크기와 축의 단위를 함께 기록한다.

**핵심 공식**

<div class="sar-math">
\[
X(t,\eta)\xrightarrow{\text{range correlation}}S_{rc}(r,\eta)\xrightarrow{\mathcal F_\eta}S_{RD}(r,f_D)\xrightarrow{\mathrm{RCMC}}S_c(r,f_D)\xrightarrow{\mathcal F_\eta^{-1}\{\cdot H_a\}}I(r,\eta)
\]
</div>

**코드 위치:** Python 181행 / MATLAB 93행 부근. 핵심 변수는 `pulse_compressed`다.

## 다음 글과 관련 글

다음 글: [17 — Hamming 창: 부엽을 줄이면 무엇을 포기할까?]({{ '/sar-basics/17-hamming/' | relative_url }}). 주엽 폭과 부엽의 상충관계를 설명한다는 과정을 이어서 살펴본다.

이전 글: [15 — 방위 chirp와 방위 압축: 이동 중 모은 신호 합치기]({{ '/sar-basics/15-azimuth-compression/' | relative_url }})

[전체 시리즈 목차]({{ '/sar-basics/series/' | relative_url }})

기본 배경: [NASA — Get to Know SAR](https://science.nasa.gov/mission/nisar/get-to-know-sar/). 본문의 수치와 그림은 제공된 코드의 설정과 별도의 교육용 계산을 사용했다.
