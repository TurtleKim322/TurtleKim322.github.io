---
title: "SAR 기초 15 — 방위 chirp와 방위 압축: 이동 중 모은 신호 합치기"
date: 2026-10-10
last_modified_at: 2026-10-10
date_format: "%Y년 %m월 %d일"
categories: [SAR, 신호처리]
tags: [SAR, Radar, Python, Signal Processing]
permalink: /sar-basics/15-azimuth-compression/
series: sar-basics
series_order: 15
toc: true
toc_sticky: true
math: true
header:
  teaser: /assets/img/sar-basics/15_a.png
---

## 한 줄 요약

거리의 변화는 느린 시간에 대해 거의 이차적인 위상을 만든다. 이것이 방위 chirp이며, 그 위상 이력에 맞는 기준 신호와 상관하면 여러 펄스에 퍼진 표적이 한 위치로 모인다.

## 왜 중요한가

거리 압축과 RCMC를 마쳐도 표적은 방위 방향으로 퍼져 있다. 방위 압축은 이동 중 얻은 합성 개구의 정보를 사용하여 이 응답을 좁히는 단계다. 기준 신호의 부호와 거리별 chirp rate가 맞아야 올바르게 합쳐진다.

## 핵심 개념

최근접 시각을 η0로 두면 R(η)는 제곱근 형태다. 플랫폼의 진행방향 이동 거리가 R0에 비해 작을 때 제곱근을 이차항까지 근사할 수 있다. 그 거리를 반송파 위상에 대입하면 상수 위상과 η²에 비례하는 항으로 나뉜다.

상수 위상은 전체 표적 응답을 같은 각도로 돌리지만 방위 집속의 중심 형태를 바꾸지 않는다. 반면 시간에 따라 달라지는 이차 위상은 상관 처리로 보정해야 한다. 코드에서는 Ka를 양의 크기로 정하고 실제 chirp에는 음의 부호를 사용한다.

Ka는 R0에 반비례한다. 그래서 다른 거리 행에 동일한 기준 신호를 무조건 사용하기보다 각 거리에서 예상되는 위상 이력을 계산한다.

## 핵심 수식

<div class="sar-math">
\[
R(\eta)\approx R_0+\frac{V^2(\eta-\eta_0)^2}{2R_0},\quad K_a=\frac{2V^2}{\lambda R_0},\quad s_{az}(\eta)=w_a(\eta)e^{-j\pi K_a\eta^2}
\]
</div>

| 기호 | 의미 | 단위 |
|---|---|---|
| R0 | 최근접 거리 | m |
| η, η0 | 느린 시간, 최근접 시각 | s |
| Ka | 방위 chirp rate의 양의 크기 | Hz/s |
| V, λ | 속도, 파장 | m/s, m |
| wa | 유한 관측 구간의 방위 창 | 없음 |

## 수식의 물리적 의미

거리 함수를 −4π/λ로 곱하면 위상이고, 이차 거리항은 −πKaη²가 된다. 따라서 도플러의 근사는 −Kaη다. 기준 chirp와 수신 신호의 회전 패턴을 맞춰 켤레 상관하면 각 관측의 위상이 정렬된다. 관측 시간은 한정되어 있으므로 점 응답도 유한 폭을 가진다.

## 현재 SAR 코드와 연결

```python
Ka = 2 * V**2 / (range_value * lam)
window = np.hamming(len(slow_time))
az_ref[insert_idx[valid]] = np.exp(-1j * np.pi * Ka * slow_time[valid]**2) * window[valid]
f_az_ref = np.fft.fft(az_ref, az_fft_length)
```

range_value는 현재 거리 행이다. 기준 신호는 음의 이차 위상을 가지며 Hamming 창을 곱한다. 이후 rd에 f_az_ref의 켤레를 곱하고 역 FFT한다. 기준 신호를 배열 중앙 부근에 삽입하므로 결과의 상관 원점과 물리적 방위 원점을 따로 맞춰야 한다.

코드 위치: `SAR_python.py` 313행 부근 / `SAR_m.m` 149행 부근. 본문의 짧은 코드는 해당 연산을 발췌하거나 설명을 위해 정리한 것이다. 분석 기준은 직접 실험한 점 표적 SAR 시뮬레이터다. 이 연재에서는 신호처리 원리와 수학에 집중한다.

## 시각적 설명

![방위 위상 이력]({{ '/assets/img/sar-basics/15_a.png' | relative_url }})

그림 A는 wrap하지 않은 이차 위상이다. 실제 np.angle 값처럼 −π~π 사이로 접힌 위상과 구별한다.

![방위 정합 필터 출력]({{ '/assets/img/sar-basics/15_b.png' | relative_url }})

그림 B는 독립적인 방위 chirp의 가중 자기상관이다. RCMC를 포함한 전체 시뮬레이션의 성능 측정이 아니라 방위 압축 자체를 보여 주는 실험이다.

## 그림 생성 코드

아래 코드는 [figures/fig_15_azimuth_compression.py]({{ '/assets/code/sar-basics/fig_15_azimuth_compression.py' | relative_url }})에도 저장되어 있다. NumPy와 Matplotlib만 사용하며, 해당 경로에 파일을 두고 실행하면 현재 작업 폴더와 관계없이 `assets/img/`에 PNG 두 개를 저장한다. 그림의 영문 축·단위는 본문 캡션과 함께 읽는다.

```python
# Output: assets/img/15_a.png and 15_b.png
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

ka=2*V*V/(LAM*R0); eta=np.arange(-680,681)*PRI
s=np.exp(-1j*np.pi*ka*eta**2)
fig,ax=new("Azimuth phase relative to closest approach", "Slow time eta (s)", "Unwrapped phase (rad)")
ax.plot(eta,-np.pi*ka*eta**2,color=PURPLE); save(fig,"15_a.png")
y=np.correlate(s,s*np.hamming(len(s)),mode="full")
dy=np.arange(-len(s)+1,len(s))*V*PRI
fig,ax=new("Azimuth correlation focuses the chirp", "Azimuth lag (m)", "Relative amplitude (dB)")
ax.plot(dy,db(y),".-",color=BLUE); ax.set(xlim=(-4,4),ylim=(-70,2)); save(fig,"15_b.png")
```

## 숫자 예제

R0=5025 m, V=100 m/s, λ=0.03 m이면 Ka≈132.669983 Hz/s다. 최근접 1초 뒤의 상대 이차 위상은 약 −416.8 rad이고 선형 도플러 근사는 −132.67 Hz다. 원본의 방위 표본 간격은 약 0.191 m지만 실제 응답 폭은 유효 개구와 창에 의존한다.

## 직접 확인해 보기

R0만 두 배가 되면 Ka는 절반이다. 같은 시간 구간에서 위상 휘어짐이 줄어든다. 다만 실제 빔 관측 시간도 거리와 함께 달라지므로 영상 해상도를 Ka 하나만 보고 단정하지 않는다.

## 요약 / 핵심 공식 / 코드 위치

- 이차 거리 근사에서 방위 chirp가 나온다.
- Ka의 크기와 실제 위상의 부호를 구별한다.
- 거리별 기준 신호와 출력 좌표의 원점을 확인한다.

**핵심 공식**

<div class="sar-math">
\[
R(\eta)\approx R_0+\frac{V^2(\eta-\eta_0)^2}{2R_0},\quad K_a=\frac{2V^2}{\lambda R_0},\quad s_{az}(\eta)=w_a(\eta)e^{-j\pi K_a\eta^2}
\]
</div>

**코드 위치:** Python 313행 / MATLAB 149행 부근. 핵심 변수는 `Ka`다.

## 다음 글과 관련 글

다음 글: [16 — SAR focusing: 처리 단계들은 왜 이 순서일까?]({{ '/sar-basics/16-focusing/' | relative_url }}). 복소수 정보를 유지하며 처리 영역을 연결한다는 과정을 이어서 살펴본다.

이전 글: [14 — RCMC: 휘어진 표적 응답을 같은 거리로 맞추기]({{ '/sar-basics/14-rcmc/' | relative_url }})

[전체 시리즈 목차]({{ '/sar-basics/series/' | relative_url }})

추가 학습: [NASA/JPL — Radar Short Course](https://science.nasa.gov/mission/nisar/radar-short-course/). 거리 처리, 도플러, 방위 처리, 거리 이동의 학습 주제를 함께 확인할 수 있다.
