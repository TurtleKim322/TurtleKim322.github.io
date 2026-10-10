---
title: "SAR 기초 11 — 거리 압축: 긴 chirp를 좁은 응답으로 모으기"
date: 2026-10-10
last_modified_at: 2026-10-10
date_format: "%Y년 %m월 %d일"
categories: [SAR, 신호처리]
tags: [SAR, Radar, Python, Signal Processing]
permalink: /sar-basics/11-range-compression/
series: sar-basics
series_order: 11
toc: true
toc_sticky: true
math: true
header:
  teaser: /assets/img/sar-basics/11_a.png
description: "거리 압축은 수신 chirp와 기준 chirp의 모양이 잘 맞는 지연을 찾는 처리다. 복소수 상관을 정합 필터로 표현하고, FFT 곱셈이 같은 계산을 효율적으로 수행하는 이유를 살펴본다."
---

## 한 줄 요약

거리 압축은 수신 chirp와 기준 chirp의 모양이 잘 맞는 지연을 찾는 처리다. 복소수 상관을 정합 필터로 표현하고, FFT 곱셈이 같은 계산을 효율적으로 수행하는 이유를 살펴본다.

## 왜 중요한가

원시 데이터에서 한 표적의 신호는 긴 펄스에 걸쳐 퍼져 있다. 단순히 가장 큰 원시 표본 하나를 고르는 대신 펄스 전체의 패턴을 이용해야 도착 시간을 더 정확하게 구별할 수 있다. 거리 압축은 영상 형성의 첫 번째 집속 단계다.

## 핵심 개념

긴 열쇠 모양을 옆으로 움직여 자물쇠와 맞는 위치를 찾는다고 생각하자. 상관은 기준 신호를 여러 지연으로 옮기면서 수신 신호와 얼마나 일치하는지 계산한다. 위상이 맞는 지연에서는 켤레 곱의 위상이 정렬되어 큰 값으로 합쳐진다.

상관을 컨볼루션 형태로 구현하려면 기준 신호를 시간 반전하고 켤레를 취한다. 코드에서는 상관의 푸리에 성질을 사용하여 수신 스펙트럼과 기준 스펙트럼의 켤레를 곱한다.

알려진 신호와 백색잡음 조건에서 이상적인 정합 필터는 특정 시점의 출력 SNR을 최대화한다. 원본은 Hamming 창으로 기준을 가중하므로 이상적인 무가중 정합 필터와 주엽 폭 및 이득이 같지는 않다.

## 핵심 수식

<div class="sar-math">
\[
h(t)=s^*(-t),\quad y(t)=x(t)*h(t),\quad y(u)=\int x(t)s^*(t-u)\,dt,\quad Y(f)=X(f)S^*(f)
\]
</div>

| 기호 | 의미 | 단위 |
|---|---|---|
| x, s | 수신 신호, 기준 신호 | 상대 진폭 |
| h | 정합 필터의 임펄스 응답 | 정규화에 따름 |
| t, u | 시간, 비교하는 지연 | s |
| * | 함수 사이에서는 컨볼루션, 위첨자에서는 켤레 | 연산 |
| X, S, Y | 대응하는 푸리에 변환 | 변환 정의에 따름 |

## 수식의 물리적 의미

맞는 지연에서는 기준과 수신 chirp의 이차 위상 패턴이 지워지고 신호가 같은 방향으로 더해진다. 맞지 않는 지연에서는 위상이 남아 합산 과정에서 일부 상쇄된다. 긴 펄스가 짧은 응답으로 모인다는 것은 원시 신호를 잘라 버리는 것이 아니라 전체 패턴을 이용해 지연을 추정한다는 뜻이다.

## 현재 SAR 코드와 연결

```python
win = np.hamming(len(ref))
f_ref = np.conj(np.fft.fft(ref * win, fft_len))
f_sig = np.fft.fft(RawData[:, p], fft_len)
pulse_compressed[:, p] = np.fft.ifft(f_sig * f_ref)
```

ref에 창을 곱하고 FFT한 뒤 켤레를 취한다. p번째 열의 수신 신호도 같은 길이로 FFT한다. 주파수별로 곱한 뒤 역변환하면 상관 결과를 얻는다. 시간 반전을 다시 추가하면 다른 연산이 될 수 있으므로 시간 영역 구현과 주파수 영역 구현의 정의를 맞춰야 한다.

코드 위치: `SAR_python.py` 179행 부근 / `SAR_m.m` 91행 부근. 본문의 짧은 코드는 해당 연산을 발췌하거나 설명을 위해 정리한 것이다. 분석 기준은 직접 실험한 점 표적 SAR 시뮬레이터다. 이 연재에서는 신호처리 원리와 수학에 집중한다.

## 시각적 설명

![지연된 긴 chirp]({{ '/assets/img/sar-basics/11_a.png' | relative_url }})

그림 A는 교육용으로 300표본 늦게 시작시킨 chirp다. 실수부와 포락선을 함께 표시한다.

![정합 필터 출력 peak]({{ '/assets/img/sar-basics/11_b.png' | relative_url }})

그림 B는 같은 신호의 상관 결과를 참 지연 주변 거리축으로 표시한다. 진폭은 최대값 기준 dB이고, 창 때문에 응답 폭과 부엽이 달라진다.

## 그림 생성 코드

아래 코드는 [figures/fig_11_range_compression.py]({{ '/assets/code/sar-basics/fig_11_range_compression.py' | relative_url }})에도 저장되어 있다. NumPy와 Matplotlib만 사용하며, 해당 경로에 파일을 두고 실행하면 현재 작업 폴더와 관계없이 `assets/img/`에 PNG 두 개를 저장한다. 그림의 영문 축·단위는 본문 캡션과 함께 읽는다.

```python
# Output: assets/img/11_a.png and 11_b.png
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

t=(np.arange(1251)-625)/FS; ref=np.exp(1j*np.pi*(B/TP)*t*t)
x=np.zeros(2200,dtype=complex); offset=300; x[offset:offset+len(ref)]=ref
fig,ax=new("A delayed finite chirp before compression", "Record time (microseconds)", "Amplitude")
tr=np.arange(len(x))/FS
ax.plot(tr*1e6,x.real,color=BLUE,lw=.5,label="Real part")
ax.plot(tr*1e6,np.abs(x),color=ORANGE,label="Envelope")
ax.legend(); save(fig,"11_a.png")
nfft=1<<int(np.ceil(np.log2(len(x)+len(ref)-1)))
y=np.fft.ifft(np.fft.fft(x,nfft)*np.conj(np.fft.fft(ref*np.hamming(len(ref)),nfft)))
assert np.argmax(np.abs(y))==offset
lag=(np.arange(nfft)-offset)*C/(2*FS)
fig,ax=new("Range compression with a Hamming-weighted reference", "Range lag relative to true delay (m)", "Relative amplitude (dB)")
ax.plot(lag,db(y),color=BLUE); ax.set(xlim=(-10,10),ylim=(-70,2)); save(fig,"11_b.png")
```

## 숫자 예제

원시 길이 2083과 기준 길이 1251의 선형 상관에 필요한 길이는 3333이다. 코드는 4096을 사용한다. 그림용 실험에서는 기준 chirp를 300표본 지연해 놓았고, 출력 최대점이 정확히 300번째 지연에서 생기는지 검사한다. 300표본은 이 실험의 상대 거리 180 m이며 실제 표적 절대 거리 5 km와는 별개다.

## 직접 확인해 보기

지연 표본을 300에서 350으로 바꾸면 최대점도 50표본, 즉 상대 거리 30 m만큼 이동해야 한다. 필터를 바꾸지 않고 위치만 변하는지 확인해 보자.

## 요약 / 핵심 공식 / 코드 위치

- 정합 필터는 기준 신호와 맞는 지연을 찾는다.
- 상관은 기준 스펙트럼의 켤레 곱으로 계산할 수 있다.
- FFT 길이와 상관 지연축의 원점을 함께 맞춰야 한다.

**핵심 공식**

<div class="sar-math">
\[
h(t)=s^*(-t),\quad y(t)=x(t)*h(t),\quad y(u)=\int x(t)s^*(t-u)\,dt,\quad Y(f)=X(f)S^*(f)
\]
</div>

**코드 위치:** Python 179행 / MATLAB 91행 부근. 핵심 변수는 `f_ref`다.

## 다음 글과 관련 글

다음 글: [12 — FFT: 신호를 주파수 성분으로 읽기]({{ '/sar-basics/12-fft/' | relative_url }}). DFT 주파수 bin과 FFT 축을 구별한다는 과정을 이어서 살펴본다.

이전 글: [10 — 도플러: 거리 변화가 주파수로 보이는 이유]({{ '/sar-basics/10-doppler/' | relative_url }})

[전체 시리즈 목차]({{ '/sar-basics/series/' | relative_url }})

추가 학습: [NASA/JPL — Radar Short Course](https://science.nasa.gov/mission/nisar/radar-short-course/). 거리 처리, 도플러, 방위 처리, 거리 이동의 학습 주제를 함께 확인할 수 있다.
