---
title: "SAR 기초 05 — 거리 해상도: 대역폭이 넓으면 왜 더 잘 구분할까?"
date: 2026-10-10
last_modified_at: 2026-10-10
date_format: "%Y년 %m월 %d일"
categories: [SAR, 신호처리]
tags: [SAR, Radar, Python, Signal Processing]
permalink: /sar-basics/05-range-resolution/
series: sar-basics
series_order: 5
toc: true
toc_sticky: true
math: true
header:
  teaser: /assets/img/sar-basics/05_a.png
description: "거리 해상도는 가까이 있는 두 표적을 구별하는 능력이다. 긴 chirp를 압축한 응답의 폭이 왜 대역폭에 반비례하는지, 그리고 그 값이 거리 표본 간격과 왜 다른지 알아본다."
---

## 한 줄 요약

거리 해상도는 가까이 있는 두 표적을 구별하는 능력이다. 긴 chirp를 압축한 응답의 폭이 왜 대역폭에 반비례하는지, 그리고 그 값이 거리 표본 간격과 왜 다른지 알아본다.

## 왜 중요한가

코드는 dR=C/(2*BW)를 계산해 거리 해상도를 출력한다. 이 숫자를 그대로 영상의 픽셀 크기나 측정된 −3 dB 폭으로 읽으면 해석이 틀어진다. 해상도 기준식, 창 함수, 표적 간섭을 구분해야 결과를 과장하지 않을 수 있다.

## 핵심 개념

하나의 점 표적도 처리 후에는 수학적인 한 점이 아니라 일정한 폭을 가진 응답으로 나타난다. 두 표적의 응답이 지나치게 겹치면 구별하기 어렵다. 넓은 주파수 대역을 함께 사용하면 짧은 시간에 집중된 응답을 만들 수 있어 거리 구분 능력이 좋아진다.

사각 대역을 이상화하면 압축 응답은 sinc 형태다. 중심에서 첫 영점까지의 시간 간격이 대략 1/B이므로 왕복 거리로 바꾸면 c/(2B)가 된다. 여기서 말하는 해상도 규모와 중심 양쪽을 포함한 전체 영점 간 폭은 서로 다르다.

실제 시뮬레이터는 Hamming 가중을 사용한다. 부엽이 줄어드는 대신 주엽은 넓어진다. 따라서 0.75 m라는 기준식만으로 실제 영상에서 두 점이 항상 분리된다고 말할 수 없다.

## 핵심 수식

<div class="sar-math">
\[
\delta R\approx\frac{c}{2B},\qquad p(r)\approx\operatorname{sinc}^2\!\left(\frac{r}{\delta R}\right),\qquad \operatorname{sinc}(x)=\frac{\sin(\pi x)}{\pi x}
\]
</div>

| 기호 | 의미 | 단위 |
|---|---|---|
| δR | 이상적인 거리 해상도 규모 | m |
| B | 처리 대역폭 | Hz |
| r | 응답 중심에서의 거리차 | m |
| p | 이상화한 정규화 전력 응답 | 없음 |

## 수식의 물리적 의미

대역폭이 두 배이면 서로 다른 주파수 성분들이 더 짧은 시간 범위에서만 같은 위상으로 겹친다. 따라서 응답 폭이 대략 절반으로 줄어든다. 반송파의 한 주기가 짧다는 것과 압축 응답이 좁다는 것은 같은 말이 아니다.

## 현재 SAR 코드와 연결

```python
dR = C / (2 * BW)
win = np.hamming(len(ref))
f_ref = np.conj(np.fft.fft(ref * win, fft_len))
```

dR는 BW로부터 얻은 기준값이다. 뒤의 두 줄은 실제 처리에서는 기준 chirp에 창을 곱한다는 사실을 보여 준다. 원본 콘솔은 소수점 한 자리로 출력하므로 0.75 m가 0.8 m로 보인다. 문서에서는 계산값 0.75 m를 보존하고 측정한 해상도와 구분한다.

코드 위치: `SAR_python.py` 29행 부근 / `SAR_m.m` 16행 부근. 본문의 짧은 코드는 해당 연산을 발췌하거나 설명을 위해 정리한 것이다. 분석 기준은 직접 실험한 점 표적 SAR 시뮬레이터다. 이 연재에서는 신호처리 원리와 수학에 집중한다.

## 시각적 설명

![두 표적의 이상적 응답]({{ '/assets/img/sar-basics/05_a.png' | relative_url }})

그림 A는 같은 1.5 m 간격 표적에 대해 대역폭만 바꾼 이상적 전력 합산 모형이다. 주황 점선은 실제 표적 위치다.

![대역폭별 점 응답 폭]({{ '/assets/img/sar-basics/05_b.png' | relative_url }})

그림 B는 표적 하나의 응답이다. 정규화 높이는 같고 폭만 달라지므로 대역폭의 효과를 분리해 볼 수 있다.

## 그림 생성 코드

아래 코드는 [figures/fig_05_range_resolution.py]({{ '/assets/code/sar-basics/fig_05_range_resolution.py' | relative_url }})에도 저장되어 있다. NumPy와 Matplotlib만 사용하며, 해당 경로에 파일을 두고 실행하면 현재 작업 폴더와 관계없이 `assets/img/`에 PNG 두 개를 저장한다. 그림의 영문 축·단위는 본문 캡션과 함께 읽는다.

```python
# Output: assets/img/05_a.png and 05_b.png
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

r=np.linspace(-5,5,3000); separation=1.5
fig,axes=plt.subplots(1,2,figsize=(11,4.4),layout="constrained",sharey=True)
for ax,bw in zip(axes,[50e6,200e6]):
    dr=C/(2*bw)
    # Noncoherent sum of two ideal sinc-squared power responses.
    power=sum(np.sinc((r-offset)/dr)**2 for offset in [-separation/2,separation/2])
    ax.plot(r,power,color=BLUE)
    for p in [-separation/2,separation/2]: ax.axvline(p,color=ORANGE,ls="--",alpha=.6)
    ax.set(title=f"B = {bw/1e6:g} MHz; scale {dr:g} m",xlabel="Range offset (m)",ylabel="Relative summed power"); ax.grid(alpha=.2)
fig.suptitle("Ideal illustration: two targets 1.5 m apart (noncoherent power sum)"); save(fig,"05_a.png")
fig,ax=new("Larger bandwidth narrows the ideal point response", "Range offset (m)", "Normalized power")
for bw in [50e6,100e6,200e6]: ax.plot(r,np.sinc(r/(C/(2*bw)))**2,label=f"{bw/1e6:g} MHz")
ax.set_xlim(-3,3); ax.legend(); save(fig,"05_b.png")
```

## 숫자 예제

B=50, 100, 200 MHz에 대해 δR는 각각 3, 1.5, 0.75 m다. 두 표적 간격이 1.5 m인 교육용 예에서는 50 MHz 응답이 많이 겹치고 200 MHz에서 분리가 더 잘 보인다. 그림은 위상 간섭을 제외한 두 이상적 전력 응답의 합이므로 원본 복소수 표적 합산의 정량 검증은 아니다.

## 직접 확인해 보기

B를 400 MHz로 바꾸면 기준 해상도는 0.375 m다. 하지만 현재 fs=250 MHz로는 그 복소수 기저대역 전체를 담지 못한다. 대역폭 변경은 샘플링 조건도 함께 검토해야 한다.

## 요약 / 핵심 공식 / 코드 위치

- 거리 해상도 기준은 c/(2B)다.
- Hamming 창을 쓰면 실제 주엽 폭이 달라진다.
- 표본 간격과 해상도, 위상 민감도는 구별해야 한다.

**핵심 공식**

<div class="sar-math">
\[
\delta R\approx\frac{c}{2B},\qquad p(r)\approx\operatorname{sinc}^2\!\left(\frac{r}{\delta R}\right),\qquad \operatorname{sinc}(x)=\frac{\sin(\pi x)}{\pi x}
\]
</div>

**코드 위치:** Python 29행 / MATLAB 16행 부근. 핵심 변수는 `dR`다.

## 다음 글과 관련 글

다음 글: [06 — 샘플링: 거리 표본 간격과 해상도는 다르다]({{ '/sar-basics/06-sampling/' | relative_url }}). 샘플링 간격과 aliasing 조건을 설명한다는 과정을 이어서 살펴본다.

이전 글: [04 — Chirp: 시간이 흐르면서 주파수가 달라지는 신호]({{ '/sar-basics/04-chirp/' | relative_url }})

[전체 시리즈 목차]({{ '/sar-basics/series/' | relative_url }})
