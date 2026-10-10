---
title: "SAR 기초 01 — 레이더는 거리를 어떻게 측정할까?"
date: 2026-10-10
last_modified_at: 2026-10-10
date_format: "%Y년 %m월 %d일"
categories: [SAR, 신호처리]
tags: [SAR, Radar, Python, Signal Processing]
permalink: /sar-basics/01-distance/
series: sar-basics
series_order: 1
toc: true
toc_sticky: true
math: true
header:
  teaser: /assets/img/sar-basics/01_a.png
---

## 한 줄 요약

레이더의 가장 기본적인 거리 정보는 신호가 돌아오는 데 걸린 시간이다. 왕복 시간과 편도 거리를 연결하는 식에서 출발해, 코드의 시간 지연과 배열 위치가 어떤 뜻인지 알아본다.

## 왜 중요한가

SAR 원시 데이터를 생성하려면 각 표적의 반사 신호를 올바른 시간에 넣어야 한다. 지연을 잘못 계산하면 이후의 압축이 아무리 정확해도 표적의 거리 위치가 틀어진다. 신호가 두 번 이동한다는 사실이 거리축 전체의 출발점이다.

## 핵심 개념

플랫폼이 신호를 보낸 뒤 표적이 반사하고, 그 신호가 다시 플랫폼으로 돌아온다고 하자. 플랫폼과 표적 사이가 R이라면 전체 이동 경로는 2R이다. 속도가 c인 파동의 이동 시간은 거리 나누기 속도로 계산한다.

초기 설명에서는 송신과 수신 사이 플랫폼 이동을 무시한다. 이른바 stop-and-go 근사에 해당한다. 이번 수치에서는 약 33 μs 동안 100 m/s로 이동한 거리가 약 3.3 mm여서 거시적 기하 설명에는 작지만, 실제 고정밀 시스템에서는 이 근사의 적합성을 별도로 확인해야 한다.

도착 시간을 표본 번호로 바꾸려면 수신 창의 시작 시각도 알아야 한다. 송신 시각 기준 지연과 수신 배열의 첫 번째 표본은 같은 원점이 아니다.

## 핵심 수식

<div class="sar-math">
\[
\tau=\frac{2R}{c},\qquad R=\frac{c\tau}{2},\qquad n\approx\frac{\tau-t_{\mathrm{start}}}{\Delta t}
\]
</div>

| 기호 | 의미 | 단위 |
|---|---|---|
| R | 편도 표적 거리 | m |
| τ | 송신부터 수신까지의 왕복 시간 | s |
| c | 전파 속도 | m/s |
| t_start, Δt | 수신 창 시작 시각, 표본 주기 | s |
| n | 배열 위치에 대응하는 표본 번호 | 무차원 |

## 수식의 물리적 의미

시간에 c를 곱하면 왕복 경로 길이가 나온다. 우리가 원하는 것은 편도 거리이므로 다시 2로 나눈다. 반대로 거리 차이 1 m는 왕복 시간 차이 약 6.67 ns가 된다. 작은 거리 차이를 읽으려면 신호의 시간 구조를 세밀하게 다루어야 한다.

## 현재 SAR 코드와 연결

```python
delay = 2 * R[nt] / C
idx1 = int(np.ceil((delay - SWST) / dt))
idx = np.arange(len(t)) + idx1
```

delay는 초 단위다. SWST를 빼면 수신 창 시작에 대한 상대 시간이고, dt로 나누면 표본 단위가 된다. ceil은 그 지연 이후의 첫 격자 위치를 고른다. idx는 chirp 전체를 놓을 구간이다. 원본은 유한 길이 기준 chirp의 시작을 이 위치에 넣고, 후속 상관 지연으로 거리를 읽으므로 원시 펄스의 중앙을 곧바로 표적 거리라고 해석하지 않는다.

코드 위치: `SAR_python.py` 130행 부근 / `SAR_m.m` 75행 부근. 본문의 짧은 코드는 해당 연산을 발췌하거나 설명을 위해 정리한 것이다. 분석 기준은 직접 실험한 점 표적 SAR 시뮬레이터다. 이 연재에서는 신호처리 원리와 수학에 집중한다.

## 시각적 설명

![송신·반사·수신 시간축]({{ '/assets/img/sar-basics/01_a.png' | relative_url }})

그림 A는 송신 0 μs, 반사 16.667 μs, 수신 33.333 μs를 나눠 그린 시간 도식이다. 세로 위치는 사건을 구별하기 위한 표시다.

![거리와 왕복 시간의 관계]({{ '/assets/img/sar-basics/01_b.png' | relative_url }})

그림 B의 기울기는 2/c다. 거리가 두 배이면 왕복 시간도 두 배가 되는 선형 관계를 보여 준다.

## 그림 생성 코드

아래 코드는 [figures/fig_01_distance.py]({{ '/assets/code/sar-basics/fig_01_distance.py' | relative_url }})에도 저장되어 있다. NumPy와 Matplotlib만 사용하며, 해당 경로에 파일을 두고 실행하면 현재 작업 폴더와 관계없이 `assets/img/`에 PNG 두 개를 저장한다. 그림의 영문 축·단위는 본문 캡션과 함께 읽는다.

```python
# Output: assets/img/01_a.png and 01_b.png
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

fig,ax=new("Transmit, reflect, receive: R = 5 km", "Time from transmit (microseconds)", "Event")
times=np.array([0,5000/C,10000/C])*1e6
ax.scatter(times,[0,1,0],s=110,color=[BLUE,ORANGE,PURPLE],zorder=3)
ax.plot(times,[0,1,0],color=BLUE)
for x,y,label in zip(times,[0,1,0],["Transmit","Reflect","Receive"]): ax.annotate(label,(x,y),xytext=(0,14),textcoords="offset points",ha="center")
ax.set(ylim=(-.3,1.4),yticks=[]); save(fig,"01_a.png")
fig,ax=new("Round-trip delay grows linearly with range", "Range (km)", "Round-trip delay (microseconds)")
r=np.linspace(0,10000,300)
ax.plot(r/1000,2*r/C*1e6,color=BLUE)
ax.scatter([5],[2*5000/C*1e6],color=ORANGE,label="5 km -> 33.33 us")
ax.legend(); save(fig,"01_b.png")
```

## 숫자 예제

R=5000 m이면 τ=33.333333 μs다. SWST=32 μs, dt=4 ns라면 상대 지연은 약 333.333 표본이고 ceil로 고른 시작 인덱스는 334다. 반대로 SWST 자체에 대응하는 거리 좌표는 4800 m다. 소수 표본 지연은 chirp 시간 변수의 보정에도 반영된다.

## 직접 확인해 보기

표적이 15 m 더 멀어지면 왕복 시간은 얼마나 늘어날까? 답은 100 ns다. 250 MHz 샘플링에서는 25표본에 해당한다. 이는 표본 위치 변화이지, 아직 두 표적을 분리할 수 있다는 보장은 아니다.

## 요약 / 핵심 공식 / 코드 위치

- 왕복 지연은 2R/c다.
- 거리 변환에서는 왕복 경로 때문에 2로 나눈다.
- 수신 표본 번호에는 창 시작 시각과 표본 주기가 필요하다.

**핵심 공식**

<div class="sar-math">
\[
\tau=\frac{2R}{c},\qquad R=\frac{c\tau}{2},\qquad n\approx\frac{\tau-t_{\mathrm{start}}}{\Delta t}
\]
</div>

**코드 위치:** Python 130행 / MATLAB 75행 부근. 핵심 변수는 `delay`다.

## 다음 글과 관련 글

다음 글: [02 — 파장과 주파수: 10 GHz는 얼마나 짧은 파동일까?]({{ '/sar-basics/02-wavelength/' | relative_url }}). 시간 주파수와 공간 파장을 연결한다는 과정을 이어서 살펴본다.

이전 글: [00 — SAR 입문 시리즈를 시작하며: 신호에서 영상까지]({{ '/sar-basics/00-start/' | relative_url }})

[전체 시리즈 목차]({{ '/sar-basics/series/' | relative_url }})

기본 배경: [NASA — Get to Know SAR](https://science.nasa.gov/mission/nisar/get-to-know-sar/). 본문의 수치와 그림은 제공된 코드의 설정과 별도의 교육용 계산을 사용했다.
