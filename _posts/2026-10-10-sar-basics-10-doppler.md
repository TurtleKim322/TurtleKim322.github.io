---
title: "SAR 기초 10 — 도플러: 거리 변화가 주파수로 보이는 이유"
date: 2026-10-10
last_modified_at: 2026-10-10
date_format: "%Y년 %m월 %d일"
categories: [SAR, 신호처리]
tags: [SAR, Radar, Python, Signal Processing]
permalink: /sar-basics/10-doppler/
series: sar-basics
series_order: 10
toc: true
toc_sticky: true
math: true
header:
  teaser: /assets/img/sar-basics/10_a.png
---

## 한 줄 요약

표적에 가까워지거나 멀어질 때 수신 신호의 위상 변화 속도가 달라진다. 도플러는 그 위상 변화율을 주파수로 읽은 값이며, 거리 함수를 미분하면 직접 구할 수 있다.

## 왜 중요한가

SAR는 이동 중 얻은 도플러와 위상 이력을 활용해 진행 방향의 표적을 구분한다. 접근과 이탈의 부호 정의를 일관되게 사용해야 방위 기준 신호가 실제 신호와 맞는다. 단방향 통신의 도플러와 달리 레이더는 왕복 경로 때문에 2가 붙는다.

## 핵심 개념

다가오는 구급차의 소리가 높게 들리는 현상처럼, 관측자와 파원 사이의 거리 변화는 주파수에 나타난다. 레이더에서는 플랫폼에서 표적까지 갔다가 돌아오는 신호의 위상을 추적한다.

이 글에서는 접근 속도 vr를 −dR/dη로 정의한다. 거리가 줄어드는 접근 시 vr가 양수이며, 코드의 음의 왕복 위상 정의에서는 도플러가 양수다. 문헌마다 속도나 위상 부호 정의가 다를 수 있으므로 공식의 부호만 따로 비교하지 않는다.

진행 속도 V 전체가 시선 방향 속도인 것은 아니다. 최근접 지점에서는 플랫폼이 계속 움직이더라도 그 순간의 거리 변화율은 0이므로 도플러가 0이다.

## 핵심 수식

<div class="sar-math">
\[
v_r=-\frac{dR}{d\eta},\qquad f_D=\frac{2v_r}{\lambda}=-\frac{2}{\lambda}\frac{dR}{d\eta}=-\frac{2V^2(\eta-\eta_0)}{\lambda\sqrt{R_0^2+V^2(\eta-\eta_0)^2}}
\]
</div>

| 기호 | 의미 | 단위 |
|---|---|---|
| vr | 접근을 양수로 정의한 시선 방향 속도 | m/s |
| V | 경로를 따라 이동하는 플랫폼 속도 | m/s |
| fD | 도플러 주파수 | Hz |
| η, η0 | 느린 시간, 최근접 시각 | s |
| R0, λ | 최근접 거리, 파장 | m |

## 수식의 물리적 의미

왕복 위상 −4πR/λ를 시간으로 미분하고 2π로 나누면 도플러가 된다. 즉 도플러는 거리 변화의 다른 표현이다. 최근접 부근에서는 R을 R0로 근사할 수 있어 fD가 시간에 거의 선형으로 변한다.

## 현재 SAR 코드와 연결

```python
phase_range = np.exp(-1j * 2 * np.pi * fc * delay)
BW_fd = 2 * V / lam * np.deg2rad(Theta_h)
fd = np.fft.fftfreq(az_fft_length, d=PRI)
```

원시 신호 생성에는 별도의 도플러 코사인을 더하지 않는다. 플랫폼 위치별 delay가 달라지므로 phase_range의 변화 안에 이미 도플러가 포함된다. BW_fd는 관심 대역의 폭이고 fd는 FFT 각 칸의 주파수 좌표다. 표적의 순간 fD, 전체 대역폭, FFT 좌표는 서로 다른 용도다.

코드 위치: `SAR_python.py` 149행 부근 / `SAR_m.m` 12행 부근. 본문의 짧은 코드는 해당 연산을 발췌하거나 설명을 위해 정리한 것이다. 분석 기준은 직접 실험한 점 표적 SAR 시뮬레이터다. 이 연재에서는 신호처리 원리와 수학에 집중한다.

## 시각적 설명

![접근·최근접·이탈 거리]({{ '/assets/img/sar-basics/10_a.png' | relative_url }})

그림 A에서 거리가 감소하는 왼쪽은 접근, 증가하는 오른쪽은 이탈이다. 색은 부호를 구분하는 표시다.

![도플러 곡선과 선형 근사]({{ '/assets/img/sar-basics/10_b.png' | relative_url }})

그림 B는 정확한 거리 미분과 최근접 부근의 선형 근사를 비교한다. 좁은 빔 구간에서 두 곡선이 가까운 이유를 볼 수 있다.

## 그림 생성 코드

아래 코드는 [figures/fig_10_doppler.py]({{ '/assets/code/sar-basics/fig_10_doppler.py' | relative_url }})에도 저장되어 있다. NumPy와 Matplotlib만 사용하며, 해당 경로에 파일을 두고 실행하면 현재 작업 폴더와 관계없이 `assets/img/`에 PNG 두 개를 저장한다. 그림의 영문 축·단위는 본문 캡션과 함께 읽는다.

```python
# Output: assets/img/10_a.png and 10_b.png
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

eta=np.linspace(-1.3,1.3,700); r=np.sqrt(R0**2+(V*eta)**2)
fig,ax=new("Approach -> closest approach -> departure", "Slow time from closest approach (s)", "R - R0 (m)")
ax.plot(eta,r-R0,color=BLUE)
ax.axvspan(-1.3,0,color=BLUE,alpha=.1,label="Approach: closing speed > 0")
ax.axvspan(0,1.3,color=ORANGE,alpha=.1,label="Departure: closing speed < 0")
ax.legend(); save(fig,"10_a.png")
fig,ax=new("Doppler: fD = -2 (dR/deta) / wavelength", "Slow time (s)", "Doppler frequency (Hz)")
fd=-2*V*V*eta/(LAM*r); ka=2*V*V/(LAM*R0)
ax.plot(eta,fd,color=BLUE,label="Exact geometric derivative")
ax.plot(eta,-ka*eta,"--",color=ORANGE,label="Linear approximation")
ax.axhline(0,color="gray",lw=.8); ax.legend(); save(fig,"10_b.png")
```

## 숫자 예제

R0=5025 m에서 최근접 시각보다 1초 전에는 fD가 약 +132.64 Hz, 1초 후에는 약 −132.64 Hz다. 최근접에서 0 Hz다. 3° 빔의 끝에서는 대략 ±174.5 Hz로, 전체 대역폭이 약 349 Hz가 된다.

## 직접 확인해 보기

왜 진행 속도 100 m/s를 그대로 2V/λ에 넣으면 약 6667 Hz가 나오는데 실제 관측 대역은 훨씬 좁을까? 시선 방향으로 투영된 속도가 V보다 훨씬 작기 때문이다.

## 요약 / 핵심 공식 / 코드 위치

- 이 글은 접근 속도를 양수로 정의한다.
- 왕복 레이더 도플러는 2vr/λ다.
- 최근접 지점에서는 진행 속도가 0이 아니어도 도플러는 0이다.

**핵심 공식**

<div class="sar-math">
\[
v_r=-\frac{dR}{d\eta},\qquad f_D=\frac{2v_r}{\lambda}=-\frac{2}{\lambda}\frac{dR}{d\eta}=-\frac{2V^2(\eta-\eta_0)}{\lambda\sqrt{R_0^2+V^2(\eta-\eta_0)^2}}
\]
</div>

**코드 위치:** Python 149행 / MATLAB 12행 부근. 핵심 변수는 `phase_range`다.

## 다음 글과 관련 글

다음 글: [11 — 거리 압축: 긴 chirp를 좁은 응답으로 모으기]({{ '/sar-basics/11-range-compression/' | relative_url }}). 상관과 정합 필터, 켤레의 역할을 설명한다는 과정을 이어서 살펴본다.

이전 글: [09 — PRF와 PRI: 레이더는 얼마나 자주 신호를 보낼까?]({{ '/sar-basics/09-prf-pri/' | relative_url }})

[전체 시리즈 목차]({{ '/sar-basics/series/' | relative_url }})
