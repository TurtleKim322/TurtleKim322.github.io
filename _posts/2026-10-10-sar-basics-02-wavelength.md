---
title: "SAR 기초 02 — 파장과 주파수: 10 GHz는 얼마나 짧은 파동일까?"
date: 2026-10-10
last_modified_at: 2026-10-10
date_format: "%Y년 %m월 %d일"
categories: [SAR, 신호처리]
tags: [SAR, Radar, Python, Signal Processing]
permalink: /sar-basics/02-wavelength/
series: sar-basics
series_order: 2
toc: true
toc_sticky: true
math: true
header:
  teaser: /assets/img/sar-basics/02_a.png
---

## 한 줄 요약

주파수는 1초에 몇 번 진동하는지, 파장은 공간에서 한 주기가 얼마나 긴지를 뜻한다. 같은 전파 속도에서 주파수가 높아질수록 파장은 짧아진다는 관계를 SAR 위상과 연결한다.

## 왜 중요한가

코드의 파장은 반송파 위상, 도플러 대역폭, 방위 chirp rate에 반복해서 등장한다. 주파수 10 GHz를 단순한 장비 숫자로 보는 대신 3 cm짜리 공간 주기로 해석하면 거리 변화가 왜 큰 위상 변화를 만드는지 이해하기 쉽다.

## 핵심 개념

한 주기에 걸리는 시간은 주파수의 역수다. 그 한 주기 동안 파동이 이동한 거리가 파장이므로 속도와 주기를 곱하면 파장을 얻는다. 물 위의 파동을 옆에서 보면 마루 사이의 간격이 파장이고, 한 점에서 기다리며 세는 마루의 횟수가 주파수에 해당한다.

반송파 주파수 fc와 변조 대역폭 B는 구별해야 한다. 이번 레이더는 중심 주파수가 10 GHz이고 chirp의 주파수 변화 범위가 200 MHz다. 거리 압축 해상도는 주로 B에, 거리 변화에 따른 반송파 위상은 fc 또는 λ에 연결된다.

기저대역 시뮬레이션에서는 10 GHz 진동 자체를 모든 시간 표본에 그리지 않는다. 빠른 반송파 진동을 제거한 복소수 표현을 쓰되, 전파 거리에 따른 반송파 위상은 남긴다.

## 핵심 수식

<div class="sar-math">
\[
T_c=\frac{1}{f_c},\qquad \lambda=cT_c=\frac{c}{f_c},\qquad \Delta\phi=-\frac{4\pi\Delta R}{\lambda}
\]
</div>

| 기호 | 의미 | 단위 |
|---|---|---|
| fc, Tc | 반송파 주파수, 주기 | Hz, s |
| λ | 공간에서의 한 주기 | m |
| ΔR | 편도 거리 변화 | m |
| Δφ | 그 변화에 따른 왕복 위상차 | rad |

## 수식의 물리적 의미

파장이 짧으면 같은 거리 변화가 더 많은 주기에 해당한다. 왕복 경로에서는 거리 변화 ΔR가 경로 길이 2ΔR가 되므로 위상 변화는 4πΔR/λ 규모다. 파장이 짧다는 사실만으로 거리 압축의 해상도가 좋아진다고 결론 내리면 안 된다.

## 현재 SAR 코드와 연결

```python
lam = C / fc
BW_fd = 2 * V / lam * np.deg2rad(Theta_h)
phase_range = np.exp(-1j * 2 * np.pi * fc * delay)
```

첫 줄은 m/s를 1/s로 나눠 m를 만든다. 둘째 줄은 짧은 파장일수록 같은 운동이 넓은 도플러 범위로 나타남을 보여 준다. 셋째 줄은 fc를 쓰지만 delay=2R/C를 대입하면 λ를 사용한 위상식과 같다. deg2rad는 각도를 무차원 라디안으로 바꾸는 필수 단계다.

코드 위치: `SAR_python.py` 21행 부근 / `SAR_m.m` 8행 부근. 본문의 짧은 코드는 해당 연산을 발췌하거나 설명을 위해 정리한 것이다. 분석 기준은 직접 실험한 점 표적 SAR 시뮬레이터다. 이 연재에서는 신호처리 원리와 수학에 집중한다.

## 시각적 설명

![두 주파수의 공간 파형]({{ '/assets/img/sar-basics/02_a.png' | relative_url }})

그림 A는 같은 공간 길이에서 5 GHz와 10 GHz 파동의 주기 수를 비교한다. 가로축은 시간 대신 거리다.

![주파수에 따른 파장]({{ '/assets/img/sar-basics/02_b.png' | relative_url }})

그림 B는 λ=c/fc의 역비례 관계다. 표시한 10 GHz 지점에서 3 cm를 읽을 수 있다.

## 그림 생성 코드

아래 코드는 [figures/fig_02_wavelength.py]({{ '/assets/code/sar-basics/fig_02_wavelength.py' | relative_url }})에도 저장되어 있다. NumPy와 Matplotlib만 사용하며, 해당 경로에 파일을 두고 실행하면 현재 작업 폴더와 관계없이 `assets/img/`에 PNG 두 개를 저장한다. 그림의 영문 축·단위는 본문 캡션과 함께 읽는다.

```python
# Output: assets/img/02_a.png and 02_b.png
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

fig,axes=plt.subplots(2,1,figsize=(9,5),layout="constrained",sharex=True)
x=np.linspace(0,.18,2000)
for ax,f in zip(axes,[5e9,10e9]):
    wave=C/f
    ax.plot(x*100,np.cos(2*np.pi*x/wave),color=BLUE)
    ax.annotate("",xy=(0,1.2),xytext=(wave*100,1.2),arrowprops=dict(arrowstyle="<->",color=ORANGE))
    ax.set(title=f"{f/1e9:g} GHz: wavelength {wave*100:g} cm",ylabel="Amplitude",ylim=(-1.4,1.5)); ax.grid(alpha=.2)
axes[-1].set_xlabel("Distance along wave (cm)"); save(fig,"02_a.png")
fig,ax=new("Wavelength is inversely proportional to frequency", "Carrier frequency (GHz)", "Wavelength (cm)")
f=np.linspace(1e9,20e9,400)
ax.plot(f/1e9,C/f*100,color=BLUE)
ax.scatter([10],[3],color=ORANGE,label="10 GHz -> 3 cm"); ax.legend(); save(fig,"02_b.png")
```

## 숫자 예제

3×10⁸/10¹⁰=0.03 m, 즉 3 cm다. 반송파 한 주기는 0.1 ns다. 거리 변화가 1 mm이면 왕복 위상차의 크기는 약 0.419 rad, 24°다. 위상은 2π마다 반복되므로 위상 하나만으로 절대 거리를 유일하게 정할 수는 없다.

## 직접 확인해 보기

반송파만 5 GHz로 바꾸고 대역폭을 그대로 유지하면 파장은 6 cm가 되고 같은 거리 변화의 위상 민감도는 절반이 된다. 이상적 거리 압축 해상도 c/(2B)는 그대로다.

## 요약 / 핵심 공식 / 코드 위치

- 주파수는 시간의 주기, 파장은 공간의 주기다.
- fc=10 GHz일 때 λ=3 cm다.
- 반송파와 대역폭은 서로 다른 역할을 한다.

**핵심 공식**

<div class="sar-math">
\[
T_c=\frac{1}{f_c},\qquad \lambda=cT_c=\frac{c}{f_c},\qquad \Delta\phi=-\frac{4\pi\Delta R}{\lambda}
\]
</div>

**코드 위치:** Python 21행 / MATLAB 8행 부근. 핵심 변수는 `lam`다.

## 다음 글과 관련 글

다음 글: [03 — 복소수와 위상: 크기만 저장하면 무엇을 잃을까?]({{ '/sar-basics/03-complex-phase/' | relative_url }}). 복소수 벡터의 합으로 위상 정렬을 이해한다는 과정을 이어서 살펴본다.

이전 글: [01 — 레이더는 거리를 어떻게 측정할까?]({{ '/sar-basics/01-distance/' | relative_url }})

[전체 시리즈 목차]({{ '/sar-basics/series/' | relative_url }})

기본 배경: [NASA — Get to Know SAR](https://science.nasa.gov/mission/nisar/get-to-know-sar/). 본문의 수치와 그림은 제공된 코드의 설정과 별도의 교육용 계산을 사용했다.
