---
title: "SAR 기초 17 — Hamming 창: 부엽을 줄이면 무엇을 포기할까?"
date: 2026-10-10
last_modified_at: 2026-10-10
date_format: "%Y년 %m월 %d일"
categories: [SAR, 신호처리]
tags: [SAR, Radar, Python, Signal Processing]
permalink: /sar-basics/17-hamming/
series: sar-basics
series_order: 17
toc: true
toc_sticky: true
math: true
header:
  teaser: /assets/img/sar-basics/17_a.png
---

## 한 줄 요약

Hamming 창은 유한한 기준 신호의 양 끝을 완만하게 줄이는 가중치다. 부엽을 낮추는 이점과 주엽이 넓어지는 대가를 비교하고, 창을 사용한 영상의 해상도를 어떻게 읽어야 하는지 알아본다.

## 왜 중요한가

강한 표적의 부엽은 주변의 약한 표적을 가릴 수 있다. 원본이 거리·방위 기준 신호에 Hamming 창을 곱하는 이유는 이 영향을 줄이기 위해서다. 그러나 창을 쓰면 모든 성능이 동시에 좋아지는 것은 아니다.

## 핵심 개념

신호를 유한 길이로 끊는 것은 사각 창을 곱하는 것과 같다. 갑자기 잘린 경계는 주파수 영역에서 넓은 부엽을 만든다. 창 함수는 양 끝의 비중을 줄여 경계의 급격함을 완화한다.

Hamming 창은 중앙 표본을 크게, 양 끝을 작게 가중한다. 실제로 이용하는 유효 시간·대역폭 분포가 달라지면서 응답의 중심 폭은 넓어진다. 강한 점 주변의 부엽을 낮추는 목적과 가까운 두 점을 분리하는 목적 사이의 선택이 생긴다.

Hamming은 양 끝이 완전히 0인 창이 아니다. 표준 대칭 형태의 끝값은 0.08이다. 이름이 비슷한 다른 창과 식을 혼동하지 않도록 확인한다.

## 핵심 수식

<div class="sar-math">
\[
w[n]=0.54-0.46\cos\!\left(\frac{2\pi n}{N-1}\right),\quad 0\le n\lt N,\qquad H(f)=\mathcal F\{s(t)w(t)\}^*
\]
</div>

| 기호 | 의미 | 단위 |
|---|---|---|
| n, N | 표본 번호, 창 길이 | 없음 |
| w | 표본별 가중치 | 없음 |
| s | 기준 신호 | 상대 진폭 |
| H | 가중 기준 신호의 켤레 스펙트럼 | 정규화에 따름 |

## 수식의 물리적 의미

가중치를 곱하면 경계 쪽 표본의 영향이 줄어든다. 부엽 억제는 간섭을 줄이는 데 도움이 되지만 같은 최대 높이로 정규화한 그림에서는 줄어든 전체 이득이 보이지 않는다. 주엽 폭, 최대값, 부엽을 목적에 맞게 따로 비교해야 한다.

## 현재 SAR 코드와 연결

```python
win = np.hamming(len(ref))
f_ref = np.conj(np.fft.fft(ref * win, fft_len))
window = np.hamming(len(slow_time))
```

거리 기준의 길이와 방위 기준의 길이는 다르지만 둘 다 대칭 Hamming 창을 사용한다. 창은 수신 신호에 무조건 곱하는 것이 아니라 코드가 지정한 기준 신호에 적용된다. np.hamming의 정의와 출력 길이를 확인하면 기준 chirp와 같은 길이로 맞출 수 있다.

코드 위치: `SAR_python.py` 177행 부근 / `SAR_m.m` 90행 부근. 본문의 짧은 코드는 해당 연산을 발췌하거나 설명을 위해 정리한 것이다. 분석 기준은 직접 실험한 점 표적 SAR 시뮬레이터다. 이 연재에서는 신호처리 원리와 수학에 집중한다.

## 시각적 설명

![사각 창과 Hamming 창]({{ '/assets/img/sar-basics/17_a.png' | relative_url }})

그림 A는 길이 128의 사각 창과 대칭 Hamming 창이다. 창 모양을 잘 보기 위해 기준 chirp보다 짧은 길이를 사용했다.

![정규화된 창 스펙트럼 비교]({{ '/assets/img/sar-basics/17_b.png' | relative_url }})

그림 B는 두 창 자체의 스펙트럼을 각 최대값으로 정규화한 비교다. Hamming의 넓은 주엽과 낮은 부엽을 보여 주며 실제 최종 영상의 정량 성능 곡선은 아니다.

## 그림 생성 코드

아래 코드는 [figures/fig_17_hamming.py]({{ '/assets/code/sar-basics/fig_17_hamming.py' | relative_url }})에도 저장되어 있다. NumPy와 Matplotlib만 사용하며, 해당 경로에 파일을 두고 실행하면 현재 작업 폴더와 관계없이 `assets/img/`에 PNG 두 개를 저장한다. 그림의 영문 축·단위는 본문 캡션과 함께 읽는다.

```python
# Output: assets/img/17_a.png and 17_b.png
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

n=128; w=np.hamming(n); x=np.arange(n)
fig,ax=new("Reference weights: rectangular vs symmetric Hamming", "Sample index n", "Weight")
ax.plot(x,np.ones(n),color=ORANGE,label="Rectangular"); ax.plot(x,w,color=BLUE,label="Hamming")
ax.set_ylim(0,1.12); ax.legend(); save(fig,"17_a.png")
fig,ax=new("Lower sidelobes, wider mainlobe (window spectra)", "Frequency in original DFT-bin units", "Relative amplitude (dB)")
nf=65536; freq=np.fft.fftshift(np.fft.fftfreq(nf))*n
for win,label,color in [(np.ones(n),"Rectangular",ORANGE),(w,"Hamming",BLUE)]: ax.plot(freq,db(np.fft.fftshift(np.fft.fft(win,nf))),color=color,label=label)
ax.set(xlim=(-12,12),ylim=(-80,2)); ax.legend(); save(fig,"17_b.png")
```

## 숫자 예제

창 길이가 1251이면 양 끝값은 0.08이고 중앙값은 1이다. 가운데 표본과 비교해 끝의 진폭 가중치는 약 −21.94 dB다. 이 숫자는 창의 끝값에 대한 값이며, 최종 SAR 영상의 부엽 레벨이나 PSLR 측정값과 같지 않다.

## 직접 확인해 보기

그림 B의 주파수 범위를 중앙 ±3 bin으로 좁혀 보자. 부엽 비교만 할 때 놓치기 쉬운 주엽 폭 차이를 확인할 수 있다. 그다음 정규화를 제거해 최대값도 비교해 보자.

## 요약 / 핵심 공식 / 코드 위치

- 창은 표본의 비중을 조절한다.
- 부엽 감소와 주엽 확대가 함께 나타난다.
- 정규화한 스펙트럼만으로 절대 이득을 비교하지 않는다.

**핵심 공식**

<div class="sar-math">
\[
w[n]=0.54-0.46\cos\!\left(\frac{2\pi n}{N-1}\right),\quad 0\le n\lt N,\qquad H(f)=\mathcal F\{s(t)w(t)\}^*
\]
</div>

**코드 위치:** Python 177행 / MATLAB 90행 부근. 핵심 변수는 `win`다.

## 다음 글과 관련 글

다음 글: [18 — dB 영상: 약한 표적을 보이게 만드는 표시 방법]({{ '/sar-basics/18-db/' | relative_url }}). 진폭·전력 dB와 표시 하한을 구별한다는 과정을 이어서 살펴본다.

이전 글: [16 — SAR focusing: 처리 단계들은 왜 이 순서일까?]({{ '/sar-basics/16-focusing/' | relative_url }})

[전체 시리즈 목차]({{ '/sar-basics/series/' | relative_url }})
