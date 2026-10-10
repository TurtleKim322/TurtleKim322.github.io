---
title: "SAR 기초 09 — PRF와 PRI: 레이더는 얼마나 자주 신호를 보낼까?"
date: 2026-10-10
last_modified_at: 2026-10-10
date_format: "%Y년 %m월 %d일"
categories: [SAR, 신호처리]
tags: [SAR, Radar, Python, Signal Processing]
permalink: /sar-basics/09-prf-pri/
series: sar-basics
series_order: 9
toc: true
toc_sticky: true
math: true
header:
  teaser: /assets/img/sar-basics/09_a.png
description: "PRF는 1초에 보내는 펄스 수, PRI는 펄스 사이의 시간이다. 반복 송신이 플랫폼 이동의 표본 간격을 어떻게 결정하는지 계산하고, 펄스 폭과 반복 주기를 구별한다."
---

## 한 줄 요약

PRF는 1초에 보내는 펄스 수, PRI는 펄스 사이의 시간이다. 반복 송신이 플랫폼 이동의 표본 간격을 어떻게 결정하는지 계산하고, 펄스 폭과 반복 주기를 구별한다.

## 왜 중요한가

PRF는 도플러를 샘플링하는 속도이자 방위 위치를 얼마나 촘촘히 관측하는지를 결정한다. 값이 부족하면 관심 도플러 대역이 겹칠 수 있지만, 무조건 높이면 모든 문제가 해결되는 것은 아니다. 실제 장비에서는 거리 모호성 등과 함께 선택한다.

## 핵심 개념

메트로놈처럼 일정한 간격으로 신호를 보낸다고 생각하자. 1초에 500번 보내면 간격은 2 ms다. 그 사이 플랫폼이 움직이므로 각 펄스가 약간 다른 위치에서 표적을 본다. 이 이동량이 합성 개구를 구성하는 공간 표본이다.

펄스 폭은 한 번 신호가 지속되는 길이이고, PRI는 다음 펄스가 시작할 때까지의 간격이다. 두 값은 보통 크게 다르다. 이번 코드에서는 펄스 길이가 5 μs인 반면 PRI는 약 1.91 ms다.

코드는 소각도 도플러 대역폭을 먼저 추정한 뒤 그 1.5배를 PRF로 잡는다. 이는 도플러 중심이 0 부근인 broadside 모델의 설계 예시이며, 다른 관측 방향에서도 항상 같은 계수를 쓰는 보편 규칙은 아니다.

## 핵심 수식

<div class="sar-math">
\[
\mathrm{PRF}=\frac{1}{\mathrm{PRI}},\qquad \Delta y=V\,\mathrm{PRI}=\frac{V}{\mathrm{PRF}},\qquad B_D\approx\frac{2V\Theta}{\lambda}
\]
</div>

| 기호 | 의미 | 단위 |
|---|---|---|
| PRF, PRI | 펄스 반복 주파수, 반복 주기 | Hz, s |
| Δy | 이웃 펄스 사이 플랫폼 이동 거리 | m |
| V | 플랫폼 속도 | m/s |
| BD | 전체 도플러 대역폭의 근사 | Hz |
| Θ | 전체 방위 빔폭 | rad |

## 수식의 물리적 의미

시간 간격과 주파수는 역수 관계다. 플랫폼 속도에 시간 간격을 곱하면 이웃 관측 위치의 간격이 된다. 이 간격은 센서가 신호를 수집한 격자이고, 방위 압축 후 두 표적을 구별하는 능력은 아니다.

## 현재 SAR 코드와 연결

```python
BW_fd = 2 * V / lam * np.deg2rad(Theta_h)
PRF = BW_fd * 1.5
PRI = 1 / PRF
azimuth_sampling_interval = PRI * V
```

각도 3°를 라디안으로 바꾼 후 BD를 계산한다. 그다음 PRF와 PRI가 서로 역수임을 보존한다. 마지막 줄은 코드의 방위 표본 간격이다. 이후 np.fft.fftfreq에서는 d=PRI를 사용해야 Hz 단위의 도플러축이 나온다.

코드 위치: `SAR_python.py` 26행 부근 / `SAR_m.m` 13행 부근. 본문의 짧은 코드는 해당 연산을 발췌하거나 설명을 위해 정리한 것이다. 분석 기준은 직접 실험한 점 표적 SAR 시뮬레이터다. 이 연재에서는 신호처리 원리와 수학에 집중한다.

## 시각적 설명

![반복 펄스 시간축]({{ '/assets/img/sar-basics/09_a.png' | relative_url }})

그림 A는 실제 5 μs 펄스 폭을 ms 축에 그렸다. 펄스가 아주 가늘게 보이는 것은 오류가 아니라 펄스 폭과 PRI가 크게 다르기 때문이다.

![펄스 위치와 이동 거리]({{ '/assets/img/sar-basics/09_b.png' | relative_url }})

그림 B는 같은 반복 송신을 공간 축으로 바꾼 것이다. 점 사이가 약 19.1 cm지만 이것을 방위 해상도라고 부르지는 않는다.

## 그림 생성 코드

아래 코드는 [figures/fig_09_prf_pri.py]({{ '/assets/code/sar-basics/fig_09_prf_pri.py' | relative_url }})에도 저장되어 있다. NumPy와 Matplotlib만 사용하며, 해당 경로에 파일을 두고 실행하면 현재 작업 폴더와 관계없이 `assets/img/`에 PNG 두 개를 저장한다. 그림의 영문 축·단위는 본문 캡션과 함께 읽는다.

```python
# Output: assets/img/09_a.png and 09_b.png
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

fig,ax=new("Pulse repetition: 5 us pulses separated by 1.91 ms", "Transmit time (ms)", "Pulse marker")
p=np.arange(6)*PRI
for tp in p: ax.axvspan(tp*1e3,(tp+TP)*1e3,color=BLUE,lw=1)
ax.set(ylim=(0,1),yticks=[])
ax.annotate("PRI",xy=(p[0]*1e3,.5),xytext=(p[1]*1e3,.5),arrowprops=dict(arrowstyle="<->"),ha="center")
save(fig,"09_a.png")
fig,ax=new("One pulse every 0.191 m along the track", "Along-track distance (m)", "")
y=np.arange(8)*V*PRI
ax.plot(y,np.zeros(8),"o-",color=BLUE)
for i,yi in enumerate(y): ax.text(yi,.06,f"p={i}",ha="center")
ax.set(ylim=(-.2,.3),yticks=[]); save(fig,"09_b.png")
```

## 숫자 예제

Θ=3°=0.0523599 rad, V=100 m/s, λ=0.03 m이면 BD=349.065850 Hz다. PRF=523.598776 Hz, PRI=1.909859 ms, Δy=0.190986 m다. 펄스가 차지하는 시간 비율 Tp/PRI는 약 0.262%다.

## 직접 확인해 보기

플랫폼 속도를 두 배로 바꾸면 코드의 설계식에서는 BD와 PRF도 두 배가 된다. 이 경우 V/PRF는 그대로다. PRF를 고정한 채 속도만 바꾸는 경우와 결과가 다르다.

## 요약 / 핵심 공식 / 코드 위치

- PRF와 PRI는 역수다.
- 방위 표본 간격은 V/PRF다.
- 펄스 폭, PRI, 방위 해상도는 서로 다른 양이다.

**핵심 공식**

<div class="sar-math">
\[
\mathrm{PRF}=\frac{1}{\mathrm{PRI}},\qquad \Delta y=V\,\mathrm{PRI}=\frac{V}{\mathrm{PRF}},\qquad B_D\approx\frac{2V\Theta}{\lambda}
\]
</div>

**코드 위치:** Python 26행 / MATLAB 13행 부근. 핵심 변수는 `PRF`다.

## 다음 글과 관련 글

다음 글: [10 — 도플러: 거리 변화가 주파수로 보이는 이유]({{ '/sar-basics/10-doppler/' | relative_url }}). 거리 미분으로 도플러의 크기와 부호를 구한다는 과정을 이어서 살펴본다.

이전 글: [08 — Fast time과 Slow time: 배열의 두 축 읽기]({{ '/sar-basics/08-fast-slow-time/' | relative_url }})

[전체 시리즈 목차]({{ '/sar-basics/series/' | relative_url }})
