---
title: "SAR 기초 13 — Range-Doppler 영역: 방위축을 주파수축으로 바꾸기"
date: 2026-10-10
last_modified_at: 2026-10-10
date_format: "%Y년 %m월 %d일"
categories: [SAR, 신호처리]
tags: [SAR, Radar, Python, Signal Processing]
permalink: /sar-basics/13-range-doppler/
series: sar-basics
series_order: 13
toc: true
toc_sticky: true
math: true
header:
  teaser: /assets/img/sar-basics/13_a.png
description: "Range-Doppler 영역은 거리축을 유지한 채 방위 시간축만 주파수로 바꾼 표현이다. 이름에 두 개의 단어가 들어간다고 해서 두 축을 모두 FFT한 결과는 아니다."
---

## 한 줄 요약

Range-Doppler 영역은 거리축을 유지한 채 방위 시간축만 주파수로 바꾼 표현이다. 이름에 두 개의 단어가 들어간다고 해서 두 축을 모두 FFT한 결과는 아니다.

## 왜 중요한가

RCMC는 이 영역에서 도플러별 거리 이동량을 계산한다. 각 열이 펄스 위치인지 도플러 bin인지 구별하지 않으면 보정식을 올바른 축에 적용할 수 없다. 변환 후의 데이터도 복소수라는 점 역시 중요하다.

## 핵심 개념

거리 압축을 마친 배열의 한 행에는 일정한 거리 위치의 신호가 느린 시간에 따라 기록되어 있다. 이 행에 FFT를 적용하면 그 신호의 도플러 성분이 나타난다. 같은 일을 모든 거리 행에 수행하면 거리-도플러 배열이 된다.

가로축의 한 칸은 이제 특정 시각이나 플랫폼 위치가 아니라 특정 도플러 주파수다. 세로축은 여전히 거리다. 따라서 이 그림을 지상의 위치를 나타내는 최종 영상으로 읽으면 안 된다.

단일 표적의 거리 이동은 이 표현에서도 도플러에 따라 달라지는 거리 위치로 나타난다. 이 구조를 이용하면 도플러 열마다 다른 거리 좌표를 읽어 응답을 정렬할 수 있다.

## 핵심 수식

<div class="sar-math">
\[
S_{\mathrm{RD}}(r,f_D)=\mathcal{F}_{\eta}\{s_{\mathrm{rc}}(r,\eta)\},\qquad f_D[k]=\operatorname{fftfreq}(N_{\eta},\mathrm{PRI})[k]
\]
</div>

| 기호 | 의미 | 단위 |
|---|---|---|
| r | 거리 압축 후 거리 좌표 | m |
| η | 느린 시간 | s |
| fD | 방위 도플러 주파수 | Hz |
| src | 거리 압축된 복소수 데이터 | 상대 진폭 |
| SRD | 방위 FFT 후 데이터 | 변환 정규화에 따름 |

## 수식의 물리적 의미

푸리에 변환은 같은 정보를 다른 좌표로 읽는 방법이다. 거리-도플러 그림의 세로축은 거리이지만 가로축은 위치가 아니므로 밝은 점을 곧바로 표적의 방위 좌표라고 해석할 수 없다. 방위 필터와 역변환을 거쳐야 위치별 응답으로 돌아온다.

## 현재 SAR 코드와 연결

```python
rd = np.fft.fft(pulse_compressed, az_fft_length, axis=1)
fd = np.fft.fftfreq(az_fft_length, d=PRI)
```

axis=1은 펄스가 쌓인 열 방향이다. 원본 배열 rd는 fftshift하지 않은 순서이므로 fd도 같은 순서를 사용한다. 시각화에서만 둘을 함께 이동시킬 수 있다. 그림 생성 코드의 fftshift는 읽기 쉬운 좌우 주파수 순서를 위한 표시 선택이다.

코드 위치: `SAR_python.py` 233행 부근 / `SAR_m.m` 115행 부근. 본문의 짧은 코드는 해당 연산을 발췌하거나 설명을 위해 정리한 것이다. 분석 기준은 직접 실험한 점 표적 SAR 시뮬레이터다. 이 연재에서는 신호처리 원리와 수학에 집중한다.

## 시각적 설명

![교육용 거리-느린 시간 데이터]({{ '/assets/img/sar-basics/13_a.png' | relative_url }})

그림 A는 움직이는 가우스형 거리 응답에 방위 chirp 위상을 붙인 단일 표적 교육용 모형이다. 원본 전체 시뮬레이션과 별도의 계산이다.

![같은 데이터의 거리-도플러 표현]({{ '/assets/img/sar-basics/13_b.png' | relative_url }})

그림 B는 바로 그 배열을 방위 FFT한 결과다. 같은 거리 범위를 유지하면서 가로축이 초에서 Hz로 바뀐다. 두 그림은 각자 최대값으로 정규화했으므로 절대 이득 비교용이 아니다.

## 그림 생성 코드

아래 코드는 [figures/fig_13_range_doppler.py]({{ '/assets/code/sar-basics/fig_13_range_doppler.py' | relative_url }})에도 저장되어 있다. NumPy와 Matplotlib만 사용하며, 해당 경로에 파일을 두고 실행하면 현재 작업 폴더와 관계없이 `assets/img/`에 PNG 두 개를 저장한다. 그림의 영문 축·단위는 본문 캡션과 함께 읽는다.

```python
# Output: assets/img/13_a.png and 13_b.png
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

# A single-target range-compressed model, not the original raw-data run.
eta=(np.arange(1024)-512)*PRI; rr=np.linspace(5023,5030,220)
r=np.sqrt(R0**2+(V*eta)**2); ka=2*V*V/(LAM*R0)
a=np.exp(-((rr[:,None]-r[None,:])/.45)**2)*np.exp(-1j*np.pi*ka*eta[None,:]**2)
a*= (np.abs(eta)<1.3)[None,:]
fig,ax=new("Illustrative range-compressed target", "Slow time (s)", "Range (m)")
ax.grid(False); im=ax.imshow(db(a,-45),origin="lower",aspect="auto",extent=[eta[0],eta[-1],rr[0],rr[-1]],cmap="magma",vmin=-45,vmax=0)
fig.colorbar(im,ax=ax,label="Relative amplitude (dB)"); save(fig,"13_a.png")
rd=np.fft.fftshift(np.fft.fft(a,axis=1),axes=1); fd=np.fft.fftshift(np.fft.fftfreq(len(eta),PRI))
fig,ax=new("Same model after azimuth FFT", "Azimuth Doppler frequency (Hz)", "Range (m)")
ax.grid(False); im=ax.imshow(db(rd,-45),origin="lower",aspect="auto",extent=[fd[0],fd[-1],rr[0],rr[-1]],cmap="magma",vmin=-45,vmax=0)
fig.colorbar(im,ax=ax,label="Relative amplitude (dB)"); save(fig,"13_b.png")
```

## 숫자 예제

관심 거리 구간을 선택한 배열은 251×1642다. 방위 FFT에 4096을 사용하면 RD 배열은 251×4096이 된다. 도플러 간격은 약 0.127832 Hz이고 0 Hz부터 양수, 음수 순으로 저장된다. 251개의 거리 좌표 자체는 이 FFT 때문에 바뀌지 않는다.

## 직접 확인해 보기

axis=0으로 바꾸면 어떤 일이 생길까? 거리축을 변환하므로 더 이상 같은 의미의 Range-Doppler 데이터가 아니다. 결과 배열의 크기뿐 아니라 축의 단위를 적어 보면 실수를 발견하기 쉽다.

## 요약 / 핵심 공식 / 코드 위치

- 거리-도플러 영역은 방위축만 변환한 것이다.
- 행은 거리, 열은 도플러다.
- FFT 저장 순서와 fd 좌표의 순서를 맞춰야 한다.

**핵심 공식**

<div class="sar-math">
\[
S_{\mathrm{RD}}(r,f_D)=\mathcal{F}_{\eta}\{s_{\mathrm{rc}}(r,\eta)\},\qquad f_D[k]=\operatorname{fftfreq}(N_{\eta},\mathrm{PRI})[k]
\]
</div>

**코드 위치:** Python 233행 / MATLAB 115행 부근. 핵심 변수는 `rd`다.

## 다음 글과 관련 글

다음 글: [14 — RCMC: 휘어진 표적 응답을 같은 거리로 맞추기]({{ '/sar-basics/14-rcmc/' | relative_url }}). 출력 거리에서 입력 거리로 역매핑하는 방향을 이해한다는 과정을 이어서 살펴본다.

이전 글: [12 — FFT: 신호를 주파수 성분으로 읽기]({{ '/sar-basics/12-fft/' | relative_url }})

[전체 시리즈 목차]({{ '/sar-basics/series/' | relative_url }})
