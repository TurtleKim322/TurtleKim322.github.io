---
title: "SAR 기초 18 — dB 영상: 약한 표적을 보이게 만드는 표시 방법"
date: 2026-10-10
last_modified_at: 2026-10-10
date_format: "%Y년 %m월 %d일"
categories: [SAR, 신호처리]
tags: [SAR, Radar, Python, Signal Processing]
permalink: /sar-basics/18-db/
series: sar-basics
series_order: 18
toc: true
toc_sticky: true
math: true
header:
  teaser: /assets/img/sar-basics/18_a.png
---

## 한 줄 요약

SAR 영상의 진폭은 강한 응답과 약한 응답의 차이가 커서 선형 색상으로 보기 어렵다. dB는 비율을 로그로 바꾸는 표시 방법이며, 정규화와 표시 하한이 무엇을 바꾸는지 알아야 그림을 정확히 읽을 수 있다.

## 왜 중요한가

원본의 마지막 단계는 복소수 영상의 절댓값을 취하고 dB로 변환한 다음 최대값을 빼고 −60 dB에서 자른다. 이 과정을 방사 보정된 반사율이나 잡음 제거로 착각하면 결과의 의미가 달라진다.

## 핵심 개념

진폭 1, 0.01, 0.001인 세 응답을 선형 축에 그리면 작은 두 응답이 바닥에 붙어 잘 보이지 않는다. 로그를 취하면 각각 0, −40, −60 dB로 떨어져 약한 구조를 볼 수 있다. 새로운 정보를 만든 것이 아니라 기존 값의 표현 간격을 바꾼 것이다.

진폭에는 20log10, 전력에는 10log10을 사용한다. 전력이 진폭의 제곱에 비례하기 때문에 두 표현이 일치한다. 단위를 가진 양의 로그를 다룰 때는 기준값에 대한 비율을 명시하는 것이 좋다.

최대 진폭을 기준으로 정규화하면 각 영상의 가장 밝은 곳은 항상 0 dB다. 따라서 서로 다른 영상의 0 dB가 같은 절대 강도라는 뜻은 아니다.

## 핵심 수식

<div class="sar-math">
\[
A_{dB}=20\log_{10}\frac{\lvert S\rvert}{A_{ref}},\quad P_{dB}=10\log_{10}\frac{P}{P_{ref}},\quad P=\lvert S\rvert^2,\quad A_{display}=\max(A_{dB},L)
\]
</div>

| 기호 | 의미 | 단위 |
|---|---|---|
| S | 복소수 영상 | 모델의 상대 진폭 |
| Aref | 진폭 기준값, 여기서는 영상 최대값 | S와 같은 단위 |
| P, Pref | 전력과 전력 기준 | 진폭 제곱에 비례 |
| L | 표시 하한 | dB |

## 수식의 물리적 의미

−20 dB는 기준 진폭의 0.1배, −40 dB는 0.01배다. −60 dB 아래를 모두 같은 색으로 표시해도 그 값이 계산상 사라지는 것은 아니다. 다만 원본은 표시용 배열 자체를 잘라 저장하므로 원래 복소수 SAR_img와 표시용 SAR_img_dB를 구별해야 한다.

## 현재 SAR 코드와 연결

```python
eps = np.finfo(float).eps
SAR_img_dB = 20 * np.log10(np.maximum(np.abs(SAR_img), eps))
mv = np.max(SAR_img_dB)
SAR_img_dB -= mv
SAR_img_dB[SAR_img_dB < -60] = -60
```

eps는 log10(0)을 피하는 수치적 바닥값이지 측정된 잡음 수준이 아니다. 최대 dB를 빼는 것은 최대 진폭으로 나눠 정규화하는 것과 대응한다. 마지막 줄은 표시 범위를 제한한다. 원본 데이터가 0뿐인 경우의 처리 의미도 별도로 고려해야 하며, 현재 시뮬레이션은 0이 아닌 표적 신호를 갖는다.

코드 위치: `SAR_python.py` 348행 부근 / `SAR_m.m` 163행 부근. 본문의 짧은 코드는 해당 연산을 발췌하거나 설명을 위해 정리한 것이다. 분석 기준은 직접 실험한 점 표적 SAR 시뮬레이터다. 이 연재에서는 신호처리 원리와 수학에 집중한다.

## 시각적 설명

![선형 진폭과 dB 비교]({{ '/assets/img/sar-basics/18_a.png' | relative_url }})

그림 A는 같은 교육용 세 응답을 선형 진폭과 dB로 표시한다. 약한 두 점이 로그 축에서 드러난다.

![동적 범위 clipping 비교]({{ '/assets/img/sar-basics/18_b.png' | relative_url }})

그림 B는 −20, −40, −60 dB에서 각각 자른 결과다. 곡선의 평평한 바닥은 실제 신호가 일정하다는 뜻이 아니라 표시 하한이다.

## 그림 생성 코드

아래 코드는 [figures/fig_18_db.py]({{ '/assets/code/sar-basics/fig_18_db.py' | relative_url }})에도 저장되어 있다. NumPy와 Matplotlib만 사용하며, 해당 경로에 파일을 두고 실행하면 현재 작업 폴더와 관계없이 `assets/img/`에 PNG 두 개를 저장한다. 그림의 영문 축·단위는 본문 캡션과 함께 읽는다.

```python
# Output: assets/img/18_a.png and 18_b.png
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

x=np.linspace(-8,8,1200)
a=np.exp(-((x+3)/.6)**2)+.01*np.exp(-(x/.6)**2)+.001*np.exp(-((x-3)/.6)**2)
fig,axes=plt.subplots(1,2,figsize=(11,4.5),layout="constrained")
axes[0].plot(x,a,color=BLUE); axes[0].set(title="Linear amplitude",xlabel="Illustrative position (m)",ylabel="Amplitude")
axes[1].plot(x,db(a),color=PURPLE); axes[1].set(title="Same data in dB",xlabel="Illustrative position (m)",ylabel="Relative amplitude (dB)",ylim=(-80,2))
for ax in axes: ax.grid(alpha=.2)
save(fig,"18_a.png")
fig,ax=new("Clipping changes display, not underlying signal", "Illustrative position (m)", "Displayed amplitude (dB)")
for floor in [-20,-40,-60]: ax.plot(x,db(a,floor),label=f"Display floor {floor} dB")
ax.set_ylim(-65,2); ax.legend(); save(fig,"18_b.png")
```

## 숫자 예제

진폭 [1, 0.1, 0.01, 0.001]은 [0, −20, −40, −60] dB다. 진폭비 0.1의 전력비는 0.01이고 10log10(0.01)=−20 dB로 일치한다. 원본의 −60 dB 하한은 최대 진폭 대비 0.001 이하를 같은 표시값으로 만든다.

## 직접 확인해 보기

−40 dB의 약한 응답을 표시 하한 −20 dB로 그리면 어떻게 될까? 주변 바닥과 구별되지 않을 수 있다. 같은 데이터를 여러 표시 범위로 확인하는 이유다.

## 요약 / 핵심 공식 / 코드 위치

- 진폭비에는 20log10, 전력비에는 10log10을 사용한다.
- 영상별 최대값 정규화는 절대 강도 비교에 적합하지 않다.
- clipping은 표시 선택이지 집속이나 잡음 제거가 아니다.

**핵심 공식**

<div class="sar-math">
\[
A_{dB}=20\log_{10}\frac{\lvert S\rvert}{A_{ref}},\quad P_{dB}=10\log_{10}\frac{P}{P_{ref}},\quad P=\lvert S\rvert^2,\quad A_{display}=\max(A_{dB},L)
\]
</div>

**코드 위치:** Python 348행 / MATLAB 163행 부근. 핵심 변수는 `SAR_img_dB`다.

## 다음 글과 관련 글

다음 글: [19 — Zero padding: 표본은 늘어나도 정보는 늘지 않는다]({{ '/sar-basics/19-zero-padding/' | relative_url }}). 격자 보간과 물리적 분해능 향상을 구별한다는 과정을 이어서 살펴본다.

이전 글: [17 — Hamming 창: 부엽을 줄이면 무엇을 포기할까?]({{ '/sar-basics/17-hamming/' | relative_url }})

[전체 시리즈 목차]({{ '/sar-basics/series/' | relative_url }})
