---
title: "SAR 기초 04 — Chirp: 시간이 흐르면서 주파수가 달라지는 신호"
date: 2026-10-10
last_modified_at: 2026-10-10
date_format: "%Y년 %m월 %d일"
categories: [SAR, 신호처리]
tags: [SAR, Radar, Python, Signal Processing]
permalink: /sar-basics/04-chirp/
series: sar-basics
series_order: 4
toc: true
toc_sticky: true
math: true
header:
  teaser: /assets/img/sar-basics/04_a.png
description: "Chirp는 시간이 흐르면서 순간 주파수가 변하는 신호다. SAR의 거리 방향 기준 신호에서는 위상이 시간의 제곱에 비례하며, 이를 미분하면 시간에 비례하는 주파수가 나온다."
---

## 한 줄 요약

Chirp는 시간이 흐르면서 순간 주파수가 변하는 신호다. SAR의 거리 방향 기준 신호에서는 위상이 시간의 제곱에 비례하며, 이를 미분하면 시간에 비례하는 주파수가 나온다.

## 왜 중요한가

긴 펄스는 신호 에너지를 확보하기 좋지만 도착 시간 구분에는 불리할 수 있다. Chirp는 긴 펄스 안에 주파수 변화를 넣어 두었다가 정합 처리로 짧은 응답을 만드는 방법이다. 코드의 exp 안에 왜 t²가 들어가는지 이해하는 것이 출발점이다.

## 핵심 개념

주파수가 일정한 파형은 위상이 시간에 일정한 속도로 증가한다. 주파수가 점점 높아지는 파형은 위상 증가 속도도 점점 빨라져야 한다. 선형 chirp에서는 주파수가 시간에 비례하므로 위상은 그 적분인 이차함수다.

이번 코드는 시간을 펄스 중심 기준으로 잡는다. 따라서 기저대역 주파수는 음수에서 0을 지나 양수로 바뀐다. 음의 주파수는 복소평면에서 반대 방향으로 회전한다는 뜻이다. 실수부만 보면 중심 부근에서 파형이 느려지고 양쪽 끝에서 빨라 보일 수 있다.

실제 펄스는 무한히 지속되지 않는다. 기준 신호는 길이 Tp 구간에만 존재한다. 간단한 지수함수 식 옆에 유한한 펄스 창이 있다는 사실을 함께 기억하자.

## 핵심 수식

<div class="sar-math">
\[
s(t)=\operatorname{rect}\!\left(\frac{t}{T_p}\right)e^{j\pi K_rt^2},\quad K_r=\frac{B}{T_p},\quad f_i(t)=\frac{1}{2\pi}\frac{d}{dt}(\pi K_rt^2)=K_rt
\]
</div>

| 기호 | 의미 | 단위 |
|---|---|---|
| t, Tp | 펄스 중심 기준 시간, 펄스 길이 | s |
| B | 주파수 변화 범위 | Hz |
| Kr | 거리 chirp rate | Hz/s |
| fi | 순간 기저대역 주파수 | Hz |
| rect | 펄스 안에서 1, 밖에서 0인 창 | 없음 |

## 수식의 물리적 의미

Kr를 크게 하면 같은 시간 동안 주파수가 더 많이 변한다. 위상 πKr t²는 무차원 rad이고, 시간 미분 후 2π로 나누면 Hz가 된다. 지수함수의 절댓값은 1이므로 chirp의 진폭이 커지는 것이 아니라 위상 변화 속도가 달라지는 것이다.

## 현재 SAR 코드와 연결

```python
Kr = BW / taup
t_ref = np.arange(-taup / 2, taup / 2 + dt * 0.5, dt)
ref = np.exp(1j * np.pi * Kr * t_ref**2)
```

첫 줄은 대역폭과 펄스 길이로 기울기를 정한다. t_ref는 약 −2.5~2.5 μs의 중심 기준 시간이다. 끝점 포함으로 1251표본을 만들며, 이것은 반개구간의 BT 계산과 표본 개수 정의를 구별해야 하는 예다. 마지막 줄은 각 표본의 위상을 복소수로 표현한다.

코드 위치: `SAR_python.py` 37행 부근 / `SAR_m.m` 21행 부근. 본문의 짧은 코드는 해당 연산을 발췌하거나 설명을 위해 정리한 것이다. 분석 기준은 직접 실험한 점 표적 SAR 시뮬레이터다. 이 연재에서는 신호처리 원리와 수학에 집중한다.

## 시각적 설명

![LFM 실수부 확대]({{ '/assets/img/sar-basics/04_a.png' | relative_url }})

그림 A는 중심 ±0.5 μs만 확대한 chirp 실수부다. 중앙에서 느리고 양쪽에서 빠르게 보이는 이유는 중심 기준의 부호 있는 주파수다.

![순간 주파수 변화]({{ '/assets/img/sar-basics/04_b.png' | relative_url }})

그림 B는 전체 5 μs 구간의 순간 주파수다. 반송파 fc를 더하기 전 기저대역 값이다.

## 그림 생성 코드

아래 코드는 [figures/fig_04_chirp.py]({{ '/assets/code/sar-basics/fig_04_chirp.py' | relative_url }})에도 저장되어 있다. NumPy와 Matplotlib만 사용하며, 해당 경로에 파일을 두고 실행하면 현재 작업 폴더와 관계없이 `assets/img/`에 PNG 두 개를 저장한다. 그림의 영문 축·단위는 본문 캡션과 함께 읽는다.

```python
# Output: assets/img/04_a.png and 04_b.png
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

fig,ax=new("Centered baseband LFM: real part (zoom)", "Fast time from pulse center (microseconds)", "Real part")
t=np.linspace(-.5e-6,.5e-6,5000)
ax.plot(t*1e6,np.cos(np.pi*(B/TP)*t*t),color=BLUE)
save(fig,"04_a.png")
fig,ax=new("Instantaneous frequency is the derivative of phase", "Fast time from pulse center (microseconds)", "Baseband frequency (MHz)")
t=np.linspace(-TP/2,TP/2,500)
ax.plot(t*1e6,(B/TP)*t/1e6,color=ORANGE)
ax.axhline(0,color="gray",lw=.8); save(fig,"04_b.png")
```

## 숫자 예제

B=200 MHz, Tp=5 μs이면 Kr=4×10¹³ Hz/s다. t=−2.5 μs에서는 −100 MHz, t=0에서는 0, t=2.5 μs에서는 +100 MHz다. 시간·대역폭 곱 BT=1000은 길게 송신하면서 짧은 압축 응답을 얻을 여지를 보여 주지만 창과 정규화까지 포함한 실제 처리 이득을 그대로 측정한 값은 아니다.

## 직접 확인해 보기

대역폭을 그대로 두고 펄스 길이를 10 μs로 늘리면 Kr는 절반이다. 주파수 양 끝은 그대로지만 그 사이를 이동하는 데 더 긴 시간이 걸린다.

## 요약 / 핵심 공식 / 코드 위치

- 선형 주파수 변화는 이차 위상으로 표현한다.
- Kr=B/Tp의 단위는 Hz/s다.
- 음의 기저대역 주파수는 복소수 회전 방향을 뜻한다.

**핵심 공식**

<div class="sar-math">
\[
s(t)=\operatorname{rect}\!\left(\frac{t}{T_p}\right)e^{j\pi K_rt^2},\quad K_r=\frac{B}{T_p},\quad f_i(t)=\frac{1}{2\pi}\frac{d}{dt}(\pi K_rt^2)=K_rt
\]
</div>

**코드 위치:** Python 37행 / MATLAB 21행 부근. 핵심 변수는 `Kr`다.

## 다음 글과 관련 글

다음 글: [05 — 거리 해상도: 대역폭이 넓으면 왜 더 잘 구분할까?]({{ '/sar-basics/05-range-resolution/' | relative_url }}). 해상도의 기준식과 실제 응답 폭을 구별한다는 과정을 이어서 살펴본다.

이전 글: [03 — 복소수와 위상: 크기만 저장하면 무엇을 잃을까?]({{ '/sar-basics/03-complex-phase/' | relative_url }})

[전체 시리즈 목차]({{ '/sar-basics/series/' | relative_url }})
