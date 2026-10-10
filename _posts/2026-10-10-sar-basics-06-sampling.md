---
title: "SAR 기초 06 — 샘플링: 거리 표본 간격과 해상도는 다르다"
date: 2026-10-10
last_modified_at: 2026-10-10
date_format: "%Y년 %m월 %d일"
categories: [SAR, 신호처리]
tags: [SAR, Radar, Python, Signal Processing]
permalink: /sar-basics/06-sampling/
series: sar-basics
series_order: 6
toc: true
toc_sticky: true
math: true
header:
  teaser: /assets/img/sar-basics/06_a.png
description: "샘플링은 연속 신호를 일정한 시간 간격의 숫자로 저장하는 일이다. 표본을 거리로 환산하는 방법과 aliasing을 이해하고, 더 촘촘한 표본이 곧 더 좋은 해상도는 아니라는 점을 확인한다."
---

## 한 줄 요약

샘플링은 연속 신호를 일정한 시간 간격의 숫자로 저장하는 일이다. 표본을 거리로 환산하는 방법과 aliasing을 이해하고, 더 촘촘한 표본이 곧 더 좋은 해상도는 아니라는 점을 확인한다.

## 왜 중요한가

원시 배열의 크기, 표적 신호를 넣는 인덱스, 거리축 r은 모두 dt에 의존한다. 또한 신호 대역을 충분히 빠르게 샘플링하지 못하면 서로 다른 주파수가 같은 표본을 만들기 때문에 이후 처리로 원래 신호를 구별할 수 없다.

## 핵심 개념

필름의 프레임 수가 적으면 빠르게 도는 바퀴가 느리거나 반대로 도는 것처럼 보인다. 신호에서도 표본 간격 사이의 변화를 충분히 관찰하지 못하면 다른 주파수를 같은 것으로 오해한다. 이를 aliasing이라 한다.

실수 저역통과 신호는 최고 주파수 fmax에 대해 fs>2fmax가 기본 조건이다. 복소수 기저대역의 경우 전체 관심 대역이 길이 fs인 주파수 구간 안에 겹치지 않게 들어가야 한다. 이번 chirp의 중심 대역은 −100~+100 MHz이고 fs=250 MHz는 ±125 MHz 구간을 제공한다.

유한 시간의 펄스는 스펙트럼이 완벽히 잘린 신호가 아니다. 실제 장비에는 아날로그 필터와 여유 대역이 필요하다. 시뮬레이션의 단순 대역 비교를 모든 실제 시스템의 충분조건으로 확대하지는 않는다.

## 핵심 수식

<div class="sar-math">
\[
\Delta t=\frac{1}{f_s},\qquad \Delta r=\frac{c\Delta t}{2},\qquad x[n]=x(n\Delta t),\qquad e^{j2\pi(f+kf_s)n/f_s}=e^{j2\pi fn/f_s}
\]
</div>

| 기호 | 의미 | 단위 |
|---|---|---|
| fs, Δt | 시간 샘플링 주파수, 주기 | Hz, s |
| Δr | 거리축 표본 간격 | m |
| n, k | 표본 번호, 임의의 정수 | 없음 |
| f | 입력 주파수 | Hz |

## 수식의 물리적 의미

시간차 Δt를 왕복 이동 거리로 바꾸면 cΔt이고, 편도 거리 표본 간격은 그 절반이다. 마지막 식은 fs의 정수배만큼 다른 복소수 주파수가 같은 표본을 만든다는 뜻이다. 잃어버린 정보는 단순히 FFT 길이를 늘린다고 복원되지 않는다.

## 현재 SAR 코드와 연결

```python
fs = 250e6
dt = 1 / fs
dr = C * dt / 2
r = C * SWST / 2 + np.arange(pulse_compressed.shape[0]) * dr
```

dt는 초, dr는 미터다. r은 시작 거리 C*SWST/2에서 dr씩 증가하는 축이다. 원본의 전체 FFT 결과에는 상관의 유효하지 않은 구간이나 감긴 음수 지연도 있으므로, 만들어진 r의 모든 끝부분을 실제 관측 거리로 해석하지 않는다. 관심 구간을 선택하는 이유도 여기에 있다.

코드 위치: `SAR_python.py` 39행 부근 / `SAR_m.m` 23행 부근. 본문의 짧은 코드는 해당 연산을 발췌하거나 설명을 위해 정리한 것이다. 분석 기준은 직접 실험한 점 표적 SAR 시뮬레이터다. 이 연재에서는 신호처리 원리와 수학에 집중한다.

## 시각적 설명

![연속 파형과 표본]({{ '/assets/img/sar-basics/06_a.png' | relative_url }})

그림 A는 40 MHz 연속 코사인과 4 ns 간격 표본이다. 표본 사이의 선은 실제 관측값을 추가한 것이 아니다.

![동일한 표본을 만드는 두 주파수]({{ '/assets/img/sar-basics/06_b.png' | relative_url }})

그림 B의 180 MHz와 70 MHz는 서로 다른 연속 파형이지만 주황 표본에서 일치한다. 실제 chirp의 대역을 바꾼 실험이 아니라 aliasing 설명용 단일 주파수 예시다.

## 그림 생성 코드

아래 코드는 [figures/fig_06_sampling.py]({{ '/assets/code/sar-basics/fig_06_sampling.py' | relative_url }})에도 저장되어 있다. NumPy와 Matplotlib만 사용하며, 해당 경로에 파일을 두고 실행하면 현재 작업 폴더와 관계없이 `assets/img/`에 PNG 두 개를 저장한다. 그림의 영문 축·단위는 본문 캡션과 함께 읽는다.

```python
# Output: assets/img/06_a.png and 06_b.png
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

fig,ax=new("Samples at 250 MHz: 4 ns apart", "Fast time (ns)", "Amplitude")
t=np.linspace(0,80e-9,3000); ts=np.arange(21)/FS; f=40e6
ax.plot(t*1e9,np.cos(2*np.pi*f*t),color=BLUE,label="40 MHz wave")
ax.scatter(ts*1e9,np.cos(2*np.pi*f*ts),color=ORANGE,label="Samples",zorder=3)
ax.legend(); save(fig,"06_a.png")
fig,ax=new("Aliasing example: real cosines with identical samples", "Fast time (ns)", "Amplitude")
t=np.linspace(0,40e-9,4000); ts=np.arange(11)/FS
ax.plot(t*1e9,np.cos(2*np.pi*180e6*t),color=PURPLE,alpha=.7,label="180 MHz")
ax.plot(t*1e9,np.cos(2*np.pi*70e6*t),color=BLUE,label="70 MHz alias")
ax.scatter(ts*1e9,np.cos(2*np.pi*180e6*ts),color=ORANGE,zorder=4,label="250 MHz sampling")
assert np.allclose(np.cos(2*np.pi*180e6*ts),np.cos(2*np.pi*70e6*ts))
ax.legend(); save(fig,"06_b.png")
```

## 숫자 예제

fs=250 MHz이면 dt=4 ns, dr=0.60 m다. 대역폭 200 MHz의 이상적 해상도 0.75 m와는 다르다. 별도의 실수 코사인 예시에서는 180 MHz가 250 MHz로 샘플링될 때 70 MHz 코사인과 동일한 표본을 만든다. 복소수 회전까지 보존하면 180 MHz의 alias는 −70 MHz다.

## 직접 확인해 보기

fs만 500 MHz로 늘리면 dr는 0.30 m가 되지만 B가 그대로라면 기준 해상도는 0.75 m다. 표본은 촘촘해졌지만 점 응답의 물리적 폭을 만드는 대역폭은 변하지 않았다.

## 요약 / 핵심 공식 / 코드 위치

- dt=1/fs, dr=c/(2fs)다.
- 복소수 기저대역의 전체 폭과 실수 신호의 최고 주파수 조건을 구별한다.
- 더 촘촘한 표본은 관측 대역폭 자체를 넓히지 않는다.

**핵심 공식**

<div class="sar-math">
\[
\Delta t=\frac{1}{f_s},\qquad \Delta r=\frac{c\Delta t}{2},\qquad x[n]=x(n\Delta t),\qquad e^{j2\pi(f+kf_s)n/f_s}=e^{j2\pi fn/f_s}
\]
</div>

**코드 위치:** Python 39행 / MATLAB 23행 부근. 핵심 변수는 `dt`다.

## 다음 글과 관련 글

다음 글: [07 — SAR 관측 기하: 움직이는 플랫폼과 고정된 표적]({{ '/sar-basics/07-geometry/' | relative_url }}). 2차원 거리 함수와 관측 빔 범위를 계산한다는 과정을 이어서 살펴본다.

이전 글: [05 — 거리 해상도: 대역폭이 넓으면 왜 더 잘 구분할까?]({{ '/sar-basics/05-range-resolution/' | relative_url }})

[전체 시리즈 목차]({{ '/sar-basics/series/' | relative_url }})
