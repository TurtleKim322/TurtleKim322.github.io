---
title: "SAR 기초 19 — Zero padding: 표본은 늘어나도 정보는 늘지 않는다"
date: 2026-10-10
last_modified_at: 2026-10-10
date_format: "%Y년 %m월 %d일"
categories: [SAR, 신호처리]
tags: [SAR, Radar, Python, Signal Processing]
permalink: /sar-basics/19-zero-padding/
series: sar-basics
series_order: 19
toc: true
toc_sticky: true
math: true
header:
  teaser: /assets/img/sar-basics/19_a.png
---

## 한 줄 요약

배열 뒤에 0을 붙여 FFT 길이를 늘리면 주파수 격자는 촘촘해진다. 하지만 실제 관측 시간이나 신호 대역폭이 늘지는 않는다. 시간 영역 0 채우기와 주파수 영역 0 채우기의 차이도 함께 구별한다.

## 왜 중요한가

원본은 선형 상관을 위해 FFT 길이를 늘리고, 마지막에는 작은 영상의 스펙트럼을 큰 배열에 넣어 보간한다. 둘 다 0을 채우지만 목적이 다르다. 확대된 영상이 매끈해 보인다는 이유로 해상도가 높아졌다고 설명하면 안 된다.

## 핵심 개념

N개 관측값 뒤에 0을 붙여 M개로 FFT하면 같은 유한 신호의 스펙트럼을 더 많은 주파수 지점에서 평가한다. 곡선은 매끈해지고 최대점 위치를 읽기 쉬워질 수 있지만, 원래 겹쳐 있던 성분을 분리하는 새로운 관측 정보는 생기지 않는다.

실제 관측 시간을 늘리면 더 많은 위상 변화를 관찰하므로 주파수 분리 능력이 달라질 수 있다. 그림에서는 같은 짧은 신호의 0 채우기와 실제로 더 오래 관측한 신호를 비교한다.

반대로 주파수 스펙트럼 사이에 0을 넣고 역 FFT하면 시간 또는 공간 영역의 band-limited 보간이 된다. 중심 배치, 양·음 주파수 순서, 정규화가 중요하고 짝수 길이의 Nyquist 성분도 다루어야 한다.

## 핵심 수식

<div class="sar-math">
\[
\Delta f_{grid}=\frac{f_s}{N_{FFT}},\qquad T_{obs}=\frac{N_{obs}}{f_s},\qquad \delta f\sim\frac{1}{T_{obs}},\qquad N_{FFT}\ge N_x+N_h-1
\]
</div>

| 기호 | 의미 | 단위 |
|---|---|---|
| Nobs, NFFT | 실제 관측 표본 수, FFT 길이 | 없음 |
| Tobs | 관측 시간 규모 | s |
| Δfgrid | 표시·계산 격자 간격 | Hz |
| δf | 유한 관측창의 주파수 분리 규모 | Hz |
| Nx, Nh | 선형 컨볼루션에 사용한 두 신호 길이 | 없음 |

## 수식의 물리적 의미

격자 간격은 값을 어디에서 계산하느냐이고, 분해능은 두 성분을 얼마나 구별할 수 있느냐다. FFT 길이만 늘리면 전자는 바뀌지만 후자의 관측 조건은 그대로다. 또한 선형 컨볼루션에서는 신호 끝이 반대쪽으로 감기는 순환 중첩을 막기 위해 충분한 0 채우기가 필요하다.

## 현재 SAR 코드와 연결

```python
conv_len = len(ref) + num_range_samples - 1
fft_len = 1 << int(np.ceil(np.log2(conv_len)))
a = np.fft.fftshift(np.fft.fft2(target_img))
b = np.zeros((1024, 1024), dtype=np.complex128)
```

앞의 두 줄은 상관을 위한 길이 확보다. 뒤의 두 줄은 작은 영상의 스펙트럼을 큰 격자로 옮기기 위한 준비다. 원본 마지막 분석은 고정된 위치를 잘라 내며 중심 배치와 진폭 정규화가 정량 검증되지 않았다. 이 글의 예제는 그 결과를 해상도 개선 증거로 사용하지 않는다.

코드 위치: `SAR_python.py` 173행 부근 / `SAR_m.m` 89행 부근. 본문의 짧은 코드는 해당 연산을 발췌하거나 설명을 위해 정리한 것이다. 분석 기준은 직접 실험한 점 표적 SAR 시뮬레이터다. 이 연재에서는 신호처리 원리와 수학에 집중한다.

## 시각적 설명

![0 채우기 전후 FFT]({{ '/assets/img/sar-basics/19_a.png' | relative_url }})

그림 A는 같은 64개 표본에 대한 FFT다. 점 사이를 더 촘촘히 계산해도 중심 응답 자체가 좁아지지는 않는다.

![관측 시간 증가와 0 채우기 비교]({{ '/assets/img/sar-basics/19_b.png' | relative_url }})

그림 B의 파란 선은 512개를 실제로 관측한 결과다. 두 톤 10 Hz와 10.6 Hz를 구별하는 변화는 0 채우기가 아니라 긴 관측에서 나온다. 100 Hz는 설명용 샘플링이며 원본 250 MHz와 별개다.

## 그림 생성 코드

아래 코드는 [figures/fig_19_zero_padding.py]({{ '/assets/code/sar-basics/fig_19_zero_padding.py' | relative_url }})에도 저장되어 있다. NumPy와 Matplotlib만 사용하며, 해당 경로에 파일을 두고 실행하면 현재 작업 폴더와 관계없이 `assets/img/`에 PNG 두 개를 저장한다. 그림의 영문 축·단위는 본문 캡션과 함께 읽는다.

```python
# Output: assets/img/19_a.png and 19_b.png
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

# Deliberately slow 100 Hz toy signal for readable spectra.
fs=100.; n=64; t=np.arange(n)/fs
x=np.exp(2j*np.pi*10*t)+np.exp(2j*np.pi*10.6*t)
fig,ax=new("Same 64 observations, more frequency-grid samples", "Frequency (Hz)", "Amplitude / 64")
for nf,style,label in [(64,"o","64-point FFT"),(4096,"-","4096-point FFT (zeros appended)")]:
    f=np.fft.fftfreq(nf,1/fs); y=np.abs(np.fft.fft(x,nf))/n
    mask=(f>=5)&(f<=16); ax.plot(f[mask],y[mask],style,label=label)
ax.legend(); save(fig,"19_a.png")
fig,ax=new("Longer observation adds information; padding alone does not", "Frequency (Hz)", "Amplitude / observed sample count")
for nn,color in [(64,ORANGE),(512,BLUE)]:
    t=np.arange(nn)/fs; xx=np.exp(2j*np.pi*10*t)+np.exp(2j*np.pi*10.6*t)
    ff=np.fft.fftfreq(8192,1/fs); yy=np.abs(np.fft.fft(xx,8192))/nn
    m=(ff>8)&(ff<13); ax.plot(ff[m],yy[m],color=color,label=f"{nn} observed samples ({nn/fs:g} s)")
ax.legend(); save(fig,"19_b.png")
```

## 숫자 예제

Nobs=64, fs=100 Hz인 교육용 신호의 관측 시간 규모는 0.64 s이고 1/T는 1.5625 Hz다. FFT를 4096으로 늘리면 bin 간격은 0.024414 Hz지만 관측 시간은 그대로다. 512개를 실제 관측하면 5.12 s가 되어 1/T 규모가 약 0.1953 Hz로 줄어든다.

## 직접 확인해 보기

원본의 64×64 스펙트럼을 1024×1024로 단순 삽입해 역 FFT하면 NumPy 기본 정규화만으로 진폭 척도가 바뀐다. 주파수 성분을 그대로 유지하는 이상적 경우, 진폭 보존에는 각 축 길이비의 곱인 256배 보정이 필요하다. 이것도 해상도 개선이 아니라 정규화 문제다.

## 요약 / 핵심 공식 / 코드 위치

- 0 채우기는 격자와 계산 길이를 바꾼다.
- 주파수 분리 능력에는 실제 관측 시간이 중요하다.
- 공간 보간과 SAR의 물리적 영상 해상도는 같은 개념이 아니다.

**핵심 공식**

<div class="sar-math">
\[
\Delta f_{grid}=\frac{f_s}{N_{FFT}},\qquad T_{obs}=\frac{N_{obs}}{f_s},\qquad \delta f\sim\frac{1}{T_{obs}},\qquad N_{FFT}\ge N_x+N_h-1
\]
</div>

**코드 위치:** Python 173행 / MATLAB 89행 부근. 핵심 변수는 `conv_len`다.

## 다음 글과 관련 글

다음 글: [20 — SAR 코드를 읽기 위한 수학·신호처리 로드맵]({{ '/sar-basics/20-roadmap/' | relative_url }}). 선행 지식과 단계별 학습 과제를 연결한다는 과정을 이어서 살펴본다.

이전 글: [18 — dB 영상: 약한 표적을 보이게 만드는 표시 방법]({{ '/sar-basics/18-db/' | relative_url }})

[전체 시리즈 목차]({{ '/sar-basics/series/' | relative_url }})
