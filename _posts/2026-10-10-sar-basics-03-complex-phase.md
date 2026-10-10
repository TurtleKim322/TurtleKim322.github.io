---
title: "SAR 기초 03 — 복소수와 위상: 크기만 저장하면 무엇을 잃을까?"
date: 2026-10-10
last_modified_at: 2026-10-10
date_format: "%Y년 %m월 %d일"
categories: [SAR, 신호처리]
tags: [SAR, Radar, Python, Signal Processing]
permalink: /sar-basics/03-complex-phase/
series: sar-basics
series_order: 3
toc: true
toc_sticky: true
math: true
header:
  teaser: /assets/img/sar-basics/03_a.png
---

## 한 줄 요약

복소수는 계산을 어렵게 만들기 위한 장치가 아니라 진폭과 위상을 함께 보관하는 방법이다. 회전 벡터와 파형을 연결하고, SAR에서 절댓값을 너무 일찍 취하면 왜 집속할 수 없는지 살펴본다.

## 왜 중요한가

원시 데이터는 complex128 배열이고 각 표적의 신호는 복소수로 더해진다. 마지막 영상 표시 직전까지 위상을 보존해야 거리와 방위 방향의 정합 처리가 가능하다. 진폭만 같아도 위상이 다르면 합쳐진 결과는 완전히 달라진다.

## 핵심 개념

복소평면의 가로축 I는 실수부, 세로축 Q는 허수부다. 길이가 A이고 각도가 φ인 벡터의 좌표는 A cosφ와 A sinφ다. 하나의 복소수로 이 두 값을 표현하면 파형의 크기와 위치를 함께 담을 수 있다.

같은 방향의 벡터 두 개를 더하면 길이가 두 배가 된다. 반대 방향이면 상쇄된다. 여러 플랫폼 위치에서 받은 표적 신호도 그대로 더하면 위상이 어긋나 서로 지울 수 있다. 집속은 표적에 맞는 예상 위상을 보정하여 같은 방향으로 합치는 일이다.

복소수 켤레는 허수부의 부호를 바꾼다. 단위원 신호의 경우 위상 부호가 뒤집히므로, 기준 신호의 켤레를 곱하면 같은 위상 패턴을 상쇄할 수 있다.

## 핵심 수식

<div class="sar-math">
\[
e^{j\phi}=\cos\phi+j\sin\phi,\quad z=Ae^{j\phi},\quad z^*=Ae^{-j\phi},\quad \lvert 1+e^{j\Delta\phi}\rvert=2\lvert\cos(\Delta\phi/2)\rvert
\]
</div>

| 기호 | 의미 | 단위 |
|---|---|---|
| j | 제곱하면 −1이 되는 허수 단위 | 없음 |
| A | 진폭 | 모델에서 상대값 |
| φ, Δφ | 위상, 두 신호의 위상차 | rad |
| z, z* | 복소수 신호, 그 켤레 | 상대 진폭 |

## 수식의 물리적 의미

두 신호의 진폭이 각각 1이라도 합의 크기는 0부터 2까지 달라진다. 에너지가 항상 같은 방식으로 더해지는 것이 아니라 위상 관계에 따라 간섭한다. `abs`는 벡터의 길이만 남기므로 그 뒤에는 회전 방향을 복원할 수 없다.

## 현재 SAR 코드와 연결

```python
RawData = np.zeros((num_range_samples, num_azimuth_samples), dtype=np.complex128)
phase_range = np.exp(-1j * 2 * np.pi * fc * delay)
RawData[idx[valid], p] += echo[valid]
```

배열은 처음부터 복소수형으로 만들어 허수부가 버려지지 않게 한다. exp의 음의 위상 부호는 이 코드의 신호 정의다. 마지막 줄은 각 표적의 복소수 기여를 합산한다. 반사 진폭은 단순화되어 있지만 거리 위상 때문에 합산 결과는 진폭 100의 일정한 값이 아니다.

코드 위치: `SAR_python.py` 104행 부근 / `SAR_m.m` 59행 부근. 본문의 짧은 코드는 해당 연산을 발췌하거나 설명을 위해 정리한 것이다. 분석 기준은 직접 실험한 점 표적 SAR 시뮬레이터다. 이 연재에서는 신호처리 원리와 수학에 집중한다.

## 시각적 설명

![복소평면 위상 벡터]({{ '/assets/img/sar-basics/03_a.png' | relative_url }})

그림 A의 벡터 길이는 모두 1이지만 I와 Q의 값이 다르다. 원은 가능한 위상의 위치를 나타낸다.

![위상차가 있는 파형]({{ '/assets/img/sar-basics/03_b.png' | relative_url }})

그림 B는 10 GHz 실수 파형의 위상만 바꾼 비교다. 실제 원시 데이터 저장은 이 빠른 진동을 직접 샘플링하는 대신 복소수 기저대역 표현을 사용한다.

## 그림 생성 코드

아래 코드는 [figures/fig_03_complex_phase.py]({{ '/assets/code/sar-basics/fig_03_complex_phase.py' | relative_url }})에도 저장되어 있다. NumPy와 Matplotlib만 사용하며, 해당 경로에 파일을 두고 실행하면 현재 작업 폴더와 관계없이 `assets/img/`에 PNG 두 개를 저장한다. 그림의 영문 축·단위는 본문 캡션과 함께 읽는다.

```python
# Output: assets/img/03_a.png and 03_b.png
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

fig,ax=new("Complex signal: projection on I and Q", "In-phase I", "Quadrature Q",size=(6,6))
u=np.linspace(0,2*np.pi,500)
ax.plot(np.cos(u),np.sin(u),color="gray",alpha=.5)
for phase,color in [(0,BLUE),(np.pi/3,ORANGE),(np.pi,PURPLE)]:
    z=np.exp(1j*phase)
    ax.arrow(0,0,z.real,z.imag,color=color,width=.009,length_includes_head=True,head_width=.08,label=f"Phase {phase/np.pi:.2g} pi")
ax.set(xlim=(-1.3,1.3),ylim=(-1.3,1.3)); ax.set_aspect("equal"); ax.legend(loc="lower left"); save(fig,"03_a.png")
fig,ax=new("Same frequency and amplitude, different phase", "Time (ns)", "Real part")
t=np.linspace(0,.35e-9,1000)
for phase,color in [(0,BLUE),(np.pi/2,ORANGE),(np.pi,PURPLE)]: ax.plot(t*1e9,np.cos(2*np.pi*FC*t+phase),color=color,label=f"Phase {phase/np.pi:.2g} pi")
ax.legend(); save(fig,"03_b.png")
```

## 숫자 예제

위상차가 0이면 두 단위 신호의 합은 2, π/2이면 √2, π이면 0이다. λ=3 cm에서 편도 거리차 7.5 mm는 왕복 위상차 π를 만든다. 이것은 간섭의 예시이며 7.5 mm의 영상 해상도를 의미하지 않는다.

## 직접 확인해 보기

`1 + np.exp(1j*phase)`를 phase=0, π/2, π에 대해 계산해 보자. 실수부, 허수부, 절댓값을 각각 출력하면 위의 벡터 합을 숫자로 확인할 수 있다.

## 요약 / 핵심 공식 / 코드 위치

- 복소수는 진폭과 위상을 함께 저장한다.
- 신호의 합은 위상차에 따라 강화되거나 상쇄된다.
- 절댓값은 표시할 때 사용하고 집속 계산에서는 위상을 보존한다.

**핵심 공식**

<div class="sar-math">
\[
e^{j\phi}=\cos\phi+j\sin\phi,\quad z=Ae^{j\phi},\quad z^*=Ae^{-j\phi},\quad \lvert 1+e^{j\Delta\phi}\rvert=2\lvert\cos(\Delta\phi/2)\rvert
\]
</div>

**코드 위치:** Python 104행 / MATLAB 59행 부근. 핵심 변수는 `RawData`다.

## 다음 글과 관련 글

다음 글: [04 — Chirp: 시간이 흐르면서 주파수가 달라지는 신호]({{ '/sar-basics/04-chirp/' | relative_url }}). 이차 위상의 미분이 선형 주파수가 됨을 이해한다는 과정을 이어서 살펴본다.

이전 글: [02 — 파장과 주파수: 10 GHz는 얼마나 짧은 파동일까?]({{ '/sar-basics/02-wavelength/' | relative_url }})

[전체 시리즈 목차]({{ '/sar-basics/series/' | relative_url }})
