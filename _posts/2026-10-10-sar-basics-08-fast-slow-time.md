---
title: "SAR 기초 08 — Fast time과 Slow time: 배열의 두 축 읽기"
date: 2026-10-10
last_modified_at: 2026-10-10
date_format: "%Y년 %m월 %d일"
categories: [SAR, 신호처리]
tags: [SAR, Radar, Python, Signal Processing]
permalink: /sar-basics/08-fast-slow-time/
series: sar-basics
series_order: 8
toc: true
toc_sticky: true
math: true
header:
  teaser: /assets/img/sar-basics/08_a.png
description: "SAR 데이터에는 서로 다른 의미의 시간축이 두 개 있다. 한 펄스 안의 수신 시각을 fast time, 여러 펄스가 반복되는 관측 시간을 slow time이라 하며, 둘은 배열의 행과 열로 구분된다."
---

## 한 줄 요약

SAR 데이터에는 서로 다른 의미의 시간축이 두 개 있다. 한 펄스 안의 수신 시각을 fast time, 여러 펄스가 반복되는 관측 시간을 slow time이라 하며, 둘은 배열의 행과 열로 구분된다.

## 왜 중요한가

FFT를 어느 축으로 수행하는지에 따라 전혀 다른 계산이 된다. 거리 압축에서 사용할 샘플링 주파수는 fs이고 방위 FFT에서 사용할 값은 PRF다. 두 축을 혼동하면 주파수 단위, 좌표, 보간 방향이 모두 틀어진다.

## 핵심 개념

한 번 신호를 보낸 뒤 짧은 시간 동안 수신 기록을 만든다고 생각하자. 이 기록 안에서 언제 에너지가 도착했는지가 거리 정보다. 플랫폼이 이동하며 같은 일을 반복하면 기록이 여러 열로 쌓인다. 각 열은 서로 다른 플랫폼 위치에서 관측한 결과다.

원본 배열은 행이 빠른 시간 표본, 열이 펄스 번호다. 한 열을 아래로 읽으면 한 펄스의 시간 기록이고, 한 행을 옆으로 읽으면 일정한 수신 시간 위치가 펄스마다 어떻게 달라졌는지 본다.

fast time을 거리, slow time을 방위라고 흔히 부르지만 동일한 말은 아니다. 원시 데이터의 한 행이 집속된 하나의 거리 셀을 뜻하는 것은 아니며, 방위 시간도 플랫폼 위치와 연결하고 원점을 맞춰야 물리적 좌표가 된다.

## 핵심 수식

<div class="sar-math">
\[
t_n=t_{\mathrm{start}}+n\Delta t,\qquad \eta_p=p\,\mathrm{PRI},\qquad y_p=y_{\mathrm{start}}+V\eta_p,\qquad X[n,p]\in\mathbb{C}
\]
</div>

| 기호 | 의미 | 단위 |
|---|---|---|
| tn, ηp | 빠른 시간, 느린 시간 | s |
| n, p | 거리 표본 번호, 펄스 번호 | 없음 |
| Δt, PRI | 두 축의 시간 표본 간격 | s |
| yp, V | 플랫폼 위치, 속도 | m, m/s |
| X | 복소수 원시 데이터 행렬 | 상대 진폭 |

## 수식의 물리적 의미

빠른 시간은 한 번의 왕복을 세밀하게 나누는 시간이고, 느린 시간은 서로 다른 관측을 구별하는 시간이다. 펄스 번호가 커질수록 플랫폼이 이동하여 거리와 위상이 달라진다. 한 표적은 보통 여러 열에 걸쳐 기록된다.

## 현재 SAR 코드와 연결

```python
RawData = np.zeros((num_range_samples, num_azimuth_samples), dtype=np.complex128)
f_sig = np.fft.fft(RawData[:, p], fft_len)
rd = np.fft.fft(pulse_compressed, az_fft_length, axis=1)
```

첫 줄에서 행·열 순서가 확정된다. `[:, p]`는 p번째 펄스 한 열을 뽑으므로 빠른 시간 FFT다. 마지막 줄은 axis=1로 열 방향을 변환하므로 방위 FFT다. 원시 배열을 화면에 표시할 때 가로·세로를 바꾸어 그릴 수 있어도 실제 계산의 축 정의는 변하지 않는다.

코드 위치: `SAR_python.py` 104행 부근 / `SAR_m.m` 59행 부근. 본문의 짧은 코드는 해당 연산을 발췌하거나 설명을 위해 정리한 것이다. 분석 기준은 직접 실험한 점 표적 SAR 시뮬레이터다. 이 연재에서는 신호처리 원리와 수학에 집중한다.

## 시각적 설명

![교육용 원시 데이터 행렬]({{ '/assets/img/sar-basics/08_a.png' | relative_url }})

그림 A는 두 축을 보기 위한 가우스형 수신 포락선 모형이다. 실제 원본의 복소수 원시 데이터가 아니며, 계산 축과 거리 곡선을 설명하기 위한 그림이다.

![두 시간 간격 비교]({{ '/assets/img/sar-basics/08_b.png' | relative_url }})

그림 B는 한 펄스 내부의 표본과 펄스 사이 표본을 각각 ns와 ms 단위로 그렸다. 막대 높이는 진폭 측정값이 아니라 표본 위치 표시다.

## 그림 생성 코드

아래 코드는 [figures/fig_08_fast_slow_time.py]({{ '/assets/code/sar-basics/fig_08_fast_slow_time.py' | relative_url }})에도 저장되어 있다. NumPy와 Matplotlib만 사용하며, 해당 경로에 파일을 두고 실행하면 현재 작업 폴더와 관계없이 `assets/img/`에 PNG 두 개를 저장한다. 그림의 영문 축·단위는 본문 캡션과 함께 읽는다.

```python
# Output: assets/img/08_a.png and 08_b.png
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

# Educational envelope matrix, not output from the original simulator.
eta=(np.arange(301)-150)*PRI
t=np.linspace(32e-6,35e-6,400)
delay=2*np.sqrt(R0**2+(V*eta)**2)/C
a=np.exp(-((t[:,None]-delay[None,:])/.12e-6)**2)
fig,ax=new("Illustrative echo matrix: rows vs columns", "Slow time eta (s)", "Fast time t (microseconds)")
ax.grid(False); im=ax.imshow(a,origin="lower",aspect="auto",extent=[eta[0],eta[-1],t[0]*1e6,t[-1]*1e6],cmap="magma")
fig.colorbar(im,ax=ax,label="Illustrative envelope"); save(fig,"08_a.png")
fig,axes=plt.subplots(1,2,figsize=(11,4.5),layout="constrained")
axes[0].stem(np.arange(8)/FS*1e9,np.ones(8)); axes[0].set(title="Inside one received pulse",xlabel="Fast time offset (ns)",ylabel="Sample marker")
axes[1].stem(np.arange(8)*PRI*1e3,np.ones(8)); axes[1].set(title="Across repeated pulses",xlabel="Slow time (ms)",ylabel="Pulse marker")
for ax in axes: ax.set_ylim(0,1.4); ax.grid(alpha=.2)
save(fig,"08_b.png")
```

## 숫자 예제

기본 실행은 원시 배열 2083×1642를 만들었다. 빠른 시간 간격은 4 ns이고 펄스 사이 간격은 약 1.909859 ms로 약 477,465배 차이가 난다. 펄스의 내부 길이 5 μs와 펄스 반복 주기 약 1.91 ms도 구별해야 한다.

## 직접 확인해 보기

한 행과 한 열을 각각 뽑아 길이를 확인해 보자. 행은 1642개, 열은 2083개다. 이 단순한 확인은 축을 뒤집어 처리하는 실수를 찾는 데 도움이 된다.

## 요약 / 핵심 공식 / 코드 위치

- fast time은 한 펄스 내부, slow time은 펄스 사이의 시간이다.
- 원시 배열의 행은 거리 표본, 열은 펄스다.
- 거리 FFT는 fs, 방위 FFT는 PRF로 주파수축을 만든다.

**핵심 공식**

<div class="sar-math">
\[
t_n=t_{\mathrm{start}}+n\Delta t,\qquad \eta_p=p\,\mathrm{PRI},\qquad y_p=y_{\mathrm{start}}+V\eta_p,\qquad X[n,p]\in\mathbb{C}
\]
</div>

**코드 위치:** Python 104행 / MATLAB 59행 부근. 핵심 변수는 `RawData`다.

## 다음 글과 관련 글

다음 글: [09 — PRF와 PRI: 레이더는 얼마나 자주 신호를 보낼까?]({{ '/sar-basics/09-prf-pri/' | relative_url }}). 펄스 반복과 플랫폼 이동 표본을 연결한다는 과정을 이어서 살펴본다.

이전 글: [07 — SAR 관측 기하: 움직이는 플랫폼과 고정된 표적]({{ '/sar-basics/07-geometry/' | relative_url }})

[전체 시리즈 목차]({{ '/sar-basics/series/' | relative_url }})
