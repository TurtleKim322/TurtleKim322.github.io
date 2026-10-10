---
title: "SAR 기초 12 — FFT: 신호를 주파수 성분으로 읽기"
date: 2026-10-10
last_modified_at: 2026-10-10
date_format: "%Y년 %m월 %d일"
categories: [SAR, 신호처리]
tags: [SAR, Radar, Python, Signal Processing]
permalink: /sar-basics/12-fft/
series: sar-basics
series_order: 12
toc: true
toc_sticky: true
math: true
header:
  teaser: /assets/img/sar-basics/12_a.png
description: "FFT는 표본 신호의 DFT를 빠르게 계산하는 알고리즘이다. 시간 신호를 주파수 성분으로 읽는 방법, bin 간격, 배열의 주파수 순서를 함께 알아본다."
---

## 한 줄 요약

FFT는 표본 신호의 DFT를 빠르게 계산하는 알고리즘이다. 시간 신호를 주파수 성분으로 읽는 방법, bin 간격, 배열의 주파수 순서를 함께 알아본다.

## 왜 중요한가

SAR 코드에서 FFT는 상관 계산을 빠르게 하고, 방위 시간을 도플러로 바꾸며, 다시 영상으로 돌아오는 데 사용된다. 함수 이름만 익히는 대신 어떤 축과 어떤 표본 간격을 넣었는지 확인해야 각 결과의 단위를 올바르게 해석할 수 있다.

## 핵심 개념

서로 다른 음이 합쳐진 소리에서 각 음의 강도를 분리해 듣는 것처럼, DFT는 신호를 여러 복소수 진동 성분으로 분해한다. 각 주파수 후보와 신호를 비교해 그 성분이 얼마나 포함되어 있는지 계산한다.

N개의 표본으로 얻는 N개의 주파수 칸을 bin이라 한다. FFT 배열은 보통 0 Hz부터 양의 주파수를 지나 음의 주파수 순서로 저장된다. 화면에서 음수부터 양수로 보고 싶으면 데이터와 주파수축 모두에 fftshift를 적용한다.

FFT 자체는 데이터의 물리적 의미를 알지 못한다. 같은 함수라도 빠른 시간에 적용하면 수신 신호의 주파수, 느린 시간에 적용하면 방위 도플러를 나타낸다. 이 구분은 호출하는 축과 표본 주기가 만든다.

## 핵심 수식

<div class="sar-math">
\[
X[k]=\sum_{n=0}^{N-1}x[n]e^{-j2\pi kn/N},\qquad \Delta f=\frac{f_s}{N_{\mathrm{FFT}}},\qquad x[n]=\frac1N\sum_{k=0}^{N-1}X[k]e^{j2\pi kn/N}
\]
</div>

| 기호 | 의미 | 단위 |
|---|---|---|
| n, k | 시간 표본 번호, 주파수 bin 번호 | 없음 |
| N | 변환 길이 | 표본 수 |
| fs | 입력 축의 샘플링 주파수 | Hz |
| Δf | FFT 주파수 격자 간격 | Hz |
| X | 주파수 계수 | 입력 진폭과 변환 정규화에 따름 |

## 수식의 물리적 의미

복소수 지수는 각 주파수의 기준 진동이다. 입력 신호와 회전 속도가 맞으면 합이 커지고 맞지 않으면 상쇄된다. 기본 NumPy 정의에서 정변환에는 1/N이 없고 역변환에 1/N이 있으므로 진폭을 비교할 때 이 정규화를 알아야 한다.

## 현재 SAR 코드와 연결

```python
f_sig = np.fft.fft(RawData[:, p], fft_len)
rd = np.fft.fft(pulse_compressed, az_fft_length, axis=1)
fd = np.fft.fftfreq(az_fft_length, d=PRI)
```

첫 FFT는 한 열의 빠른 시간을 변환한다. 둘째 FFT는 모든 행의 느린 시간을 변환한다. 셋째 줄은 후자의 주파수축을 만든다. 복소수 원시 데이터를 rfft로 바꾸면 실수 입력 가정을 잘못 적용하게 된다. 또한 fftshift는 값의 순서를 바꾸는 연산이지 추가 주파수 분석이 아니다.

코드 위치: `SAR_python.py` 189행 부근 / `SAR_m.m` 96행 부근. 본문의 짧은 코드는 해당 연산을 발췌하거나 설명을 위해 정리한 것이다. 분석 기준은 직접 실험한 점 표적 SAR 시뮬레이터다. 이 연재에서는 신호처리 원리와 수학에 집중한다.

## 시각적 설명

![시간 파형과 주파수 성분]({{ '/assets/img/sar-basics/12_a.png' | relative_url }})

그림 A는 30 MHz와 70 MHz 복소수 톤의 실수부 및 FFT 진폭을 비교한다. 유한 관측창과 bin 불일치 때문에 주파수 에너지가 한 칸에만 모이지 않을 수 있다.

![DFT bin의 간격과 순서]({{ '/assets/img/sar-basics/12_b.png' | relative_url }})

그림 B는 30 MHz 부근 bin을 확대했다. 더 긴 FFT의 촘촘한 격자가 더 긴 실제 관측을 의미하는 것은 아니다.

## 그림 생성 코드

아래 코드는 [figures/fig_12_fft.py]({{ '/assets/code/sar-basics/fig_12_fft.py' | relative_url }})에도 저장되어 있다. NumPy와 Matplotlib만 사용하며, 해당 경로에 파일을 두고 실행하면 현재 작업 폴더와 관계없이 `assets/img/`에 PNG 두 개를 저장한다. 그림의 영문 축·단위는 본문 캡션과 함께 읽는다.

```python
# Output: assets/img/12_a.png and 12_b.png
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

n=256; t=np.arange(n)/FS
x=np.exp(2j*np.pi*30e6*t)+.6*np.exp(2j*np.pi*70e6*t)
fig,axes=plt.subplots(1,2,figsize=(11,4.5),layout="constrained")
axes[0].plot(t[:80]*1e9,x[:80].real,color=BLUE); axes[0].set(title="Two complex tones: real part",xlabel="Time (ns)",ylabel="Amplitude")
f=np.fft.fftshift(np.fft.fftfreq(n,1/FS)); spec=np.fft.fftshift(np.fft.fft(x))
axes[1].plot(f/1e6,np.abs(spec)/n,color=PURPLE); axes[1].set(title="DFT amplitude",xlabel="Frequency (MHz)",ylabel="Amplitude / N")
for ax in axes: ax.grid(alpha=.2)
save(fig,"12_a.png")
fig,ax=new("DFT bins are samples of a spectrum", "Frequency (MHz)", "Amplitude / N")
sel=(f>23e6)&(f<37e6)
ax.stem(f[sel]/1e6,np.abs(spec[sel])/n)
ax.text(.03,.9,f"Bin spacing = fs/N = {FS/n/1e6:.4f} MHz",transform=ax.transAxes)
save(fig,"12_b.png")
```

## 숫자 예제

거리 FFT 길이 4096에서 bin 간격은 250 MHz/4096≈61.035 kHz다. 방위 FFT 길이 4096에서는 PRF/4096≈0.127832 Hz다. 두 변환 길이가 같아도 입력 시간 간격이 다르므로 주파수 간격은 전혀 다르다. 그림은 원리를 보기 쉽게 256표본의 두 복소수 톤을 사용한다.

## 직접 확인해 보기

np.fft.ifft(np.fft.fft(x))가 원래 복소수 x와 수치 오차 범위에서 같은지 확인하자. 진폭이 달라진다면 추가 정규화나 축 선택을 점검한다. 정의와 순서는 [NumPy FFT 문서](https://numpy.org/doc/stable/reference/routines.fft.html)에서 확인할 수 있다.

## 요약 / 핵심 공식 / 코드 위치

- FFT는 DFT의 빠른 계산법이다.
- bin 간격은 입력 샘플링 주파수와 FFT 길이로 정해진다.
- 주파수축과 신호축에 같은 순서 변경을 적용해야 한다.

**핵심 공식**

<div class="sar-math">
\[
X[k]=\sum_{n=0}^{N-1}x[n]e^{-j2\pi kn/N},\qquad \Delta f=\frac{f_s}{N_{\mathrm{FFT}}},\qquad x[n]=\frac1N\sum_{k=0}^{N-1}X[k]e^{j2\pi kn/N}
\]
</div>

**코드 위치:** Python 189행 / MATLAB 96행 부근. 핵심 변수는 `f_sig`다.

## 다음 글과 관련 글

다음 글: [13 — Range-Doppler 영역: 방위축을 주파수축으로 바꾸기]({{ '/sar-basics/13-range-doppler/' | relative_url }}). 방위 FFT 후에도 거리축은 유지됨을 설명한다는 과정을 이어서 살펴본다.

이전 글: [11 — 거리 압축: 긴 chirp를 좁은 응답으로 모으기]({{ '/sar-basics/11-range-compression/' | relative_url }})

[전체 시리즈 목차]({{ '/sar-basics/series/' | relative_url }})
