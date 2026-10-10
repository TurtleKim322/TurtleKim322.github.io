---
title: "SAR 기초 00 — SAR 입문 시리즈를 시작하며: 신호에서 영상까지"
date: 2026-10-10
last_modified_at: 2026-10-10
date_format: "%Y년 %m월 %d일"
categories: [SAR, 신호처리]
tags: [SAR, Radar, Python, Signal Processing]
permalink: /sar-basics/00-start/
series: sar-basics
series_order: 0
toc: true
toc_sticky: true
math: true
header:
  teaser: /assets/img/sar-basics/00_a.png
---

## 한 줄 요약

SAR는 여러 위치에서 받은 반사 신호를 모아 영상을 만드는 레이더다. 이 시리즈는 점 표적 시뮬레이터를 길잡이로 삼아, 거리 측정부터 복소수 위상과 영상 집속까지 한 번에 한 개념씩 공부한다.

## 왜 중요한가

코드를 처음 열면 FFT, 보간, 복소수 지수함수가 한꺼번에 나타난다. 이들을 별개의 계산법으로 외우면 처리 순서를 설명하기 어렵다. 먼저 각 계산이 어떤 물리적 질문에 답하는지 알아두면 이후의 수식이 서로 연결된다.

## 핵심 개념

레이더는 신호가 돌아온 시간으로 거리를 구한다. 그러나 하나의 긴 펄스나 한 번의 관측만으로는 가까운 표적들을 충분히 구분하기 어렵다. 거리 방향에서는 chirp와 정합 필터를 쓰고, 진행 방향에서는 이동 중 쌓인 위상 이력을 이용한다.

플랫폼이 표적을 지나갈 때 거리는 조금씩 달라진다. 그래서 같은 표적의 신호도 거리 표본을 옮겨 다니고 위상이 계속 회전한다. RCMC는 거리 위치를 맞추는 역할을, 방위 압축은 위상 이력을 맞춰 합치는 역할을 한다. 두 처리는 목적이 다르다.

이 시리즈의 장면은 2차원 평면 위의 정지 점 표적이다. 실제 위성의 궤도·지형·잡음까지 해석하는 단계에 앞서, 가장 단순한 경우에서 처리 원리를 확인한다.

## 핵심 수식

<div class="sar-math">
\[
\tau=\frac{2R}{c},\qquad \phi=-\frac{4\pi R}{\lambda},\qquad \lambda=\frac{c}{f_c}
\]
</div>

| 기호 | 의미 | 단위 |
|---|---|---|
| R, λ | 표적 거리, 파장 | m |
| τ | 왕복 시간 | s |
| c, fc | 빛의 속도, 반송파 주파수 | m/s, Hz |
| φ | 복소수 신호의 위상 | rad |

## 수식의 물리적 의미

같은 거리 R이 도착 시간과 위상을 동시에 결정한다. 시간은 어느 거리 부근에서 신호를 찾을지를 알려 주고, 위상은 여러 관측을 어떻게 합칠지를 알려 준다. 위상 변화에 민감하다는 사실과 두 표적을 분리하는 영상 해상도는 서로 다른 이야기다.

## 현재 SAR 코드와 연결

```python
delay = 2 * R[nt] / C
phase_range = np.exp(-1j * 2 * np.pi * fc * delay)
echo = np.exp(1j * np.pi * Kr * t**2) * phase_range
```

첫 줄은 표적 하나의 왕복 시간을 계산한다. 둘째 줄은 왕복 거리를 단위원 위의 복소수 회전으로 바꾼다. 마지막 줄은 chirp의 시간 변화와 거리 위상을 곱한다. 이 신호들이 플랫폼 위치별로 쌓여 원시 데이터가 된다.

코드 위치: `SAR_python.py` 130행 부근 / `SAR_m.m` 75행 부근. 본문의 짧은 코드는 해당 연산을 발췌하거나 설명을 위해 정리한 것이다. 분석 기준은 직접 실험한 점 표적 SAR 시뮬레이터다. 이 연재에서는 신호처리 원리와 수학에 집중한다.

## 시각적 설명

![신호의 왕복과 영상 집속]({{ '/assets/img/sar-basics/00_a.png' | relative_url }})

그림 A는 개념의 연결을 보여 주는 학습용 흐름도다. 실제 원시 데이터를 처리한 결과 영상은 아니다.

![전체 학습 경로]({{ '/assets/img/sar-basics/00_b.png' | relative_url }})

그림 B는 최단 거리 5025 m인 표적에 대해 플랫폼 위치가 달라지면 거리가 어떻게 변하는지 직접 계산한 곡선이다.

## 그림 생성 코드

아래 코드는 [figures/fig_00_start.py]({{ '/assets/code/sar-basics/fig_00_start.py' | relative_url }})에도 저장되어 있다. NumPy와 Matplotlib만 사용하며, 해당 경로에 파일을 두고 실행하면 현재 작업 폴더와 관계없이 `assets/img/`에 PNG 두 개를 저장한다. 그림의 영문 축·단위는 본문 캡션과 함께 읽는다.

```python
# Output: assets/img/00_a.png and 00_b.png
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

boxes(["Distance / delay", "Wavelength / phase", "Two sampled axes", "Range compression", "RCMC", "Azimuth focus"], "00_a.png", "A route from echoes to images")
fig,ax=new("Same target, different platform positions", "Platform azimuth y (m)", "Slant range R (m)")
y=np.linspace(-140,140,600)
ax.plot(y,np.sqrt(R0**2+y*y),color=BLUE)
ax.axhline(R0,color=ORANGE,ls="--",label="Closest approach")
ax.legend(); save(fig,"00_b.png")
```

## 숫자 예제

5 km 표적의 왕복 시간은 약 33.333 μs다. 반송파 10 GHz의 파장은 3 cm다. 대역폭 200 MHz의 이상적 거리 해상도 기준은 0.75 m이고, 샘플링 250 MHz의 거리 표본 간격은 0.60 m다. 이 네 숫자가 같은 종류의 성능값이 아니라는 점부터 구별하자.

## 직접 확인해 보기

먼저 01–03편에서 거리·파장·위상을 연결하고, 04–10편에서 chirp와 샘플링·기하를 익힌다. 11–16편에서 실제 처리 흐름을 읽은 뒤, 17–19편에서 결과를 해석할 때의 함정을 확인한다. 20편은 복습 로드맵, 21편은 전체 코드 점검용이다.

## 요약 / 핵심 공식 / 코드 위치

- 거리는 도착 시간과 위상을 함께 결정한다.
- 거리 압축, RCMC, 방위 압축은 서로 다른 문제를 해결한다.
- 이 시리즈는 이상화된 2차원 모델을 기준으로 설명한다.

**핵심 공식**

<div class="sar-math">
\[
\tau=\frac{2R}{c},\qquad \phi=-\frac{4\pi R}{\lambda},\qquad \lambda=\frac{c}{f_c}
\]
</div>

**코드 위치:** Python 130행 / MATLAB 75행 부근. 핵심 변수는 `delay`다.

## 다음 글과 관련 글

다음 글: [01 — 레이더는 거리를 어떻게 측정할까?]({{ '/sar-basics/01-distance/' | relative_url }}). 왕복 지연을 거리로 바꾸고 2로 나누는 이유를 설명한다는 과정을 이어서 살펴본다.

[전체 시리즈 목차]({{ '/sar-basics/series/' | relative_url }})

기본 배경: [NASA — Get to Know SAR](https://science.nasa.gov/mission/nisar/get-to-know-sar/). 본문의 수치와 그림은 제공된 코드의 설정과 별도의 교육용 계산을 사용했다.
