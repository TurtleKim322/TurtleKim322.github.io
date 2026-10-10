---
title: "SAR 기초 07 — SAR 관측 기하: 움직이는 플랫폼과 고정된 표적"
date: 2026-10-10
last_modified_at: 2026-10-10
date_format: "%Y년 %m월 %d일"
categories: [SAR, 신호처리]
tags: [SAR, Radar, Python, Signal Processing]
permalink: /sar-basics/07-geometry/
series: sar-basics
series_order: 7
toc: true
toc_sticky: true
math: true
header:
  teaser: /assets/img/sar-basics/07_a.png
---

## 한 줄 요약

플랫폼이 직선을 따라 이동하면 고정 표적까지의 거리는 어떻게 변할까? 피타고라스 정리로 거리 함수를 만들고, 빔 안에서 표적이 보이는 구간을 기하적으로 계산한다.

## 왜 중요한가

거리 변화는 도착 시간, 반송파 위상, 도플러, 거리 이동을 모두 만든다. 기하식을 이해하면 나중에 나오는 방위 chirp나 RCMC가 갑자기 추가된 보정이 아니라 같은 거리 함수의 다른 표현임을 알 수 있다.

## 핵심 개념

플랫폼 경로를 y축으로 두고 플랫폼의 가로 위치를 x=0으로 정하자. 표적 좌표는 (xt, yt), 플랫폼 위치는 (0, yp)다. 두 점 사이 가로 차이는 xt이고 세로 차이는 yt−yp이므로 거리 R은 직각삼각형의 빗변이다.

yp=yt일 때 세로 차이가 0이 되어 거리가 최소다. 이 값을 R0=xt로 쓸 수 있다. 이 단순 모델의 xt는 최근접 거리 역할을 하며, 고도와 입사각이 있는 실제 지상 거리로 곧바로 바꾸어 읽을 수는 없다.

안테나가 진행 방향에 수직으로 바라본다고 가정하면 표적이 빔 안에 들어오는 범위는 각도 θ로 정한다. 코드에서는 빔 경계를 기준으로 신호를 완전히 포함하거나 제외하는 단순 창을 사용한다.

## 핵심 수식

<div class="sar-math">
\[
R=\sqrt{x_t^2+(y_t-y_p)^2},\qquad \theta=\tan^{-1}\!\left(\frac{y_p-y_t}{x_t}\right),\qquad y_p=y_t\pm x_t\tan(\Theta/2)
\]
</div>

| 기호 | 의미 | 단위 |
|---|---|---|
| xt, yt | 표적의 가로·진행방향 좌표 | m |
| yp | 플랫폼 진행방향 위치 | m |
| R | 플랫폼-표적 직선 거리 | m |
| θ, Θ | 중심에서 벗어난 관측각, 전체 빔폭 | rad 또는 명시한 degree |

## 수식의 물리적 의미

플랫폼이 표적에 접근할수록 R이 줄고, 최근접 지점을 지나면 다시 늘어난다. 그래서 거리는 대칭적인 곡선을 만든다. 빔폭이 좁으면 그 곡선의 중앙 부근만 관측한다. 작은 관측각에서 이 곡선을 이차식으로 근사할 수 있다는 사실이 방위 압축으로 이어진다.

## 현재 SAR 코드와 연결

```python
R = np.sqrt(TargetPosition[:, 0]**2 + (TargetPosition[:, 1] - y[p])**2)
theta = np.rad2deg(np.arctan((y[p] - TargetPosition[:, 1]) / TargetPosition[:, 0]))
visible = np.where(np.abs(theta) < Theta_h / 2)[0]
```

첫 줄은 모든 표적까지의 거리를 벡터로 계산한다. 둘째 줄은 중심 관측 방향에서 벗어난 각도를 degree로 바꾼다. 마지막 줄은 ±1.5° 안의 표적 인덱스만 선택한다. 배열의 첫 열과 둘째 열이 무엇을 뜻하는지 확인하지 않고 축 이름만 보고 표적 위치를 해석하면 좌표가 뒤바뀔 수 있다.

코드 위치: `SAR_python.py` 116행 부근 / `SAR_m.m` 69행 부근. 본문의 짧은 코드는 해당 연산을 발췌하거나 설명을 위해 정리한 것이다. 분석 기준은 직접 실험한 점 표적 SAR 시뮬레이터다. 이 연재에서는 신호처리 원리와 수학에 집중한다.

## 시각적 설명

![플랫폼 경로와 시선 거리]({{ '/assets/img/sar-basics/07_a.png' | relative_url }})

그림 A는 플랫폼 경로, 표적, 세 개의 시선 거리를 그린 도식이다. 가로·세로 축척을 다르게 사용했으므로 그림에서 각도를 직접 재면 안 된다.

![이동 위치별 거리 곡선]({{ '/assets/img/sar-basics/07_b.png' | relative_url }})

그림 B는 정확한 거리 함수를 사용한다. 색칠한 부분이 3° 빔 안의 관측 구간이며, 세로축은 R 자체가 아니라 R−R0다.

## 그림 생성 코드

아래 코드는 [figures/fig_07_geometry.py]({{ '/assets/code/sar-basics/fig_07_geometry.py' | relative_url }})에도 저장되어 있다. NumPy와 Matplotlib만 사용하며, 해당 경로에 파일을 두고 실행하면 현재 작업 폴더와 관계없이 `assets/img/`에 PNG 두 개를 저장한다. 그림의 영문 축·단위는 본문 캡션과 함께 읽는다.

```python
# Output: assets/img/07_a.png and 07_b.png
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

fig,ax=new("Broadside geometry (schematic; unequal axis scales)", "Cross-track x (m)", "Along-track y (m)")
yp=np.array([-130,0,130]); ax.plot([0,0],[-170,170],color=BLUE,lw=2,label="Platform path")
ax.scatter(np.zeros(3),yp,color=BLUE); ax.scatter([R0],[0],color=ORANGE,s=100,label="Fixed target")
for p in yp: ax.plot([0,R0],[p,0],ls="--",alpha=.6,label="Slant range" if p==-130 else None)
ax.annotate("Velocity V",xy=(0,160),xytext=(600,115),arrowprops=dict(arrowstyle="->"))
ax.legend(loc="lower right"); save(fig,"07_a.png")
fig,ax=new("Range changes along the flight path", "Platform y relative to target (m)", "R - R0 (m)")
y=np.linspace(-180,180,600); ax.plot(y,np.sqrt(R0**2+y*y)-R0,color=BLUE)
edge=R0*np.tan(THETA/2)
ax.axvspan(-edge,edge,alpha=.13,color=ORANGE,label="Inside 3-degree beam")
ax.legend(); save(fig,"07_b.png")
```

## 숫자 예제

R0=5025 m, 전체 빔폭 3°에서 빔 경계의 진행방향 거리는 약 ±131.584 m다. 전체 관측 길이는 약 263.169 m, 100 m/s로 지나는 시간은 약 2.632 s다. 경계에서 최단 거리보다 약 1.723 m 더 멀어진다.

## 직접 확인해 보기

표적의 yt만 25 m 옮기면 거리 곡선은 y축 방향으로 25 m 이동한다. 최근접 거리와 곡선 모양은 같고, 가장 가까이 지나는 플랫폼 위치만 바뀐다.

## 요약 / 핵심 공식 / 코드 위치

- 거리 함수는 피타고라스 정리에서 나온다.
- 최근접 위치에서 R0=xt다.
- 이 모델의 거리축은 실제 지상 지도 좌표와 동일하지 않다.

**핵심 공식**

<div class="sar-math">
\[
R=\sqrt{x_t^2+(y_t-y_p)^2},\qquad \theta=\tan^{-1}\!\left(\frac{y_p-y_t}{x_t}\right),\qquad y_p=y_t\pm x_t\tan(\Theta/2)
\]
</div>

**코드 위치:** Python 116행 / MATLAB 69행 부근. 핵심 변수는 `R`다.

## 다음 글과 관련 글

다음 글: [08 — Fast time과 Slow time: 배열의 두 축 읽기]({{ '/sar-basics/08-fast-slow-time/' | relative_url }}). 빠른 시간과 느린 시간을 배열 인덱스에 연결한다는 과정을 이어서 살펴본다.

이전 글: [06 — 샘플링: 거리 표본 간격과 해상도는 다르다]({{ '/sar-basics/06-sampling/' | relative_url }})

[전체 시리즈 목차]({{ '/sar-basics/series/' | relative_url }})

기본 배경: [NASA — Get to Know SAR](https://science.nasa.gov/mission/nisar/get-to-know-sar/). 본문의 수치와 그림은 제공된 코드의 설정과 별도의 교육용 계산을 사용했다.
