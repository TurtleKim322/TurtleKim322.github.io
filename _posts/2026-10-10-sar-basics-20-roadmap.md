---
title: "SAR 기초 20 — SAR 코드를 읽기 위한 수학·신호처리 로드맵"
date: 2026-10-10
last_modified_at: 2026-10-10
date_format: "%Y년 %m월 %d일"
categories: [SAR, 신호처리]
tags: [SAR, Radar, Python, Signal Processing]
permalink: /sar-basics/20-roadmap/
series: sar-basics
series_order: 20
toc: true
toc_sticky: true
math: true
header:
  teaser: /assets/img/sar-basics/20_a.png
---

## 한 줄 요약

SAR 수학을 공부할 때 모든 분야를 처음부터 끝까지 끝내고 코드를 읽을 필요는 없다. 코드에서 실제로 쓰는 연산을 기준으로 선행 지식을 연결하고, 각 단계마다 손으로 확인할 작은 과제를 정한다.

## 왜 중요한가

공식 목록만 보면 복소수·미분·FFT·보간이 서로 별개로 느껴진다. 이들을 코드의 질문과 연결하면 무엇을 먼저 공부해야 하는지, 어디까지 이해했는지 판단할 기준이 생긴다. 이 글은 이전 글을 읽지 않았어도 학습 계획을 세울 수 있도록 구성했다.

## 핵심 개념

첫 단계는 삼각함수와 복소수다. 복소수 벡터의 회전, 켤레, 위상차에 따른 합산을 설명할 수 있어야 한다. 다음은 표본 간격과 단위다. 시간·거리·주파수의 단위를 오가는 과정에서 실수가 자주 발생한다.

그다음 DFT와 FFT를 배운다. DFT의 정의, 주파수축의 순서, 정·역변환 정규화를 손으로 작은 배열에 적용해 본다. 컨볼루션과 상관의 차이를 익힌 뒤 정합 필터를 보면 켤레가 왜 등장하는지 이해할 수 있다.

기하와 미분은 도플러 및 방위 chirp로 연결된다. 피타고라스 정리로 거리 함수를 쓰고, 미분으로 도플러를 구하며, 테일러 근사로 이차 위상을 얻는다. 마지막으로 보간과 창 함수를 배워 RCMC 및 응답 해석을 다룬다. 이 순서는 실용적인 경로이지 유일한 엄격한 선후관계는 아니다.

## 핵심 수식

<div class="sar-math">
\[
e^{j\phi}=\cos\phi+j\sin\phi,\quad \Delta r=\frac{c}{2f_s},\quad y=\mathcal F^{-1}\{X S^*\},\quad f_D=-\frac{2}{\lambda}\frac{dR}{d\eta}
\]
</div>

| 단계 | 수학 개념 | 코드에서 답할 질문 |
|---|---|---|
| 1 | 복소수·삼각함수 | 위상을 어떻게 저장하고 더하는가? |
| 2 | 샘플링·단위 | 표본 번호가 몇 m, 몇 Hz인가? |
| 3 | DFT·컨볼루션·상관 | 왜 FFT와 켤레를 곱하는가? |
| 4 | 기하·미분·테일러 근사 | 이동이 어떤 위상 이력을 만드는가? |
| 5 | 보간·창·로그 | 위치를 맞추고 결과를 어떻게 표시하는가? |

## 수식의 물리적 의미

이 글의 핵심 공식은 전체 이론을 압축하려는 것이 아니라 각 학습 단계의 도착점이다. 위상은 rad, 거리 표본은 m, 시간 미분은 m/s, 도플러는 Hz로 단위를 연결할 수 있어야 한다. 수식을 말로 설명하고 작은 숫자 예제로 검산할 수 있으면 다음 단계로 진행하기 좋다.

## 현재 SAR 코드와 연결

```python
# Small independent checks, not the full SAR processor.
lam = 3e8 / 10e9
dr = 3e8 / (2 * 250e6)
z = np.exp(1j * np.pi)
x = np.array([1, 2j, -1, 0], dtype=complex)
assert np.allclose(np.fft.ifft(np.fft.fft(x)), x)
assert np.isclose(abs(1 + z), 0)
```

이 코드는 파장과 거리 표본을 계산하고, 반대 위상의 합과 FFT 왕복을 확인한다. 각 검사는 한 개념에만 집중한다. 원본 코드에서는 같은 연산이 큰 배열과 반복문 안에 있어 원리를 놓치기 쉬우므로 작은 검산으로 분리해 보는 것이 도움이 된다.

코드 위치: `SAR_python.py` 149행 부근 / `SAR_m.m` 26행 부근. 본문의 짧은 코드는 해당 연산을 발췌하거나 설명을 위해 정리한 것이다. 분석 기준은 직접 실험한 점 표적 SAR 시뮬레이터다. 이 연재에서는 신호처리 원리와 수학에 집중한다.

## 시각적 설명

![개념 의존 관계]({{ '/assets/img/sar-basics/20_a.png' | relative_url }})

그림 A는 공부 순서의 한 예다. 삼각함수와 복소수는 함께 공부하고, FFT와 컨볼루션은 서로 오가며 확인해도 된다.

![개념과 처리 단계의 대응표]({{ '/assets/img/sar-basics/20_b.png' | relative_url }})

그림 B는 개념이 처리 단계에서 사용되는 위치를 표시한 교육용 대응표다. 색은 중요도의 수치 점수가 아니라 해당 개념이 관여한다는 표시다.

## 그림 생성 코드

아래 코드는 [figures/fig_20_roadmap.py]({{ '/assets/code/sar-basics/fig_20_roadmap.py' | relative_url }})에도 저장되어 있다. NumPy와 Matplotlib만 사용하며, 해당 경로에 파일을 두고 실행하면 현재 작업 폴더와 관계없이 `assets/img/`에 PNG 두 개를 저장한다. 그림의 영문 축·단위는 본문 캡션과 함께 읽는다.

```python
# Output: assets/img/20_a.png and 20_b.png
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

boxes(["Complex / trig", "Sampling", "Fourier transform", "Convolution / correlation", "Matched filtering", "Doppler / RCMC"], "20_a.png", "A practical study route (not a strict prerequisite graph)")
matrix=np.array([[1,1,1,1],[1,1,1,1],[0,1,1,1],[0,1,0,1],[1,0,1,1],[0,0,1,0]])
fig,ax=new("Which concepts appear in each processing stage?", "", "",size=(9,5.6))
ax.grid(False); ax.imshow(matrix,cmap="Blues",vmin=0,vmax=1,aspect="auto")
ax.set(xticks=range(4),xticklabels=["Raw echo","Range filter","RCMC","Azimuth filter"],yticks=range(6),yticklabels=["Complex phase","Sampling","FFT","Correlation","Geometry / Doppler","Interpolation"])
for row,col in zip(*np.where(matrix)): ax.text(col,row,"Used",ha="center",va="center",color="white")
save(fig,"20_b.png")
```

## 숫자 예제

다음 값을 스스로 계산할 수 있는지 확인하자. λ=3 cm, dt=4 ns, Δr=0.60 m, 이상적 거리 해상도=0.75 m, PRI≈1.909859 ms, Δy≈0.190986 m다. 숫자가 맞아도 각각의 이름과 단위를 설명하지 못하면 아직 구분이 필요한 상태다.

## 직접 확인해 보기

복습 과제는 세 가지다. ① 두 위상 벡터의 합을 직접 계산한다. ② 시간 영역 상관과 FFT 상관의 지연축을 맞춘다. ③ fD=0일 때 RCMC가 항등 변환인지 확인한다. 각각 답을 예상한 다음 실행 결과와 비교하자.

## 요약 / 핵심 공식 / 코드 위치

- 공식 암기보다 단위·축·부호를 설명하는 것이 우선이다.
- 작은 독립 예제로 각 연산을 확인한다.
- 원시 데이터부터 단일 표적 검증까지 단계별로 연결한다.

**핵심 공식**

<div class="sar-math">
\[
e^{j\phi}=\cos\phi+j\sin\phi,\quad \Delta r=\frac{c}{2f_s},\quad y=\mathcal F^{-1}\{X S^*\},\quad f_D=-\frac{2}{\lambda}\frac{dR}{d\eta}
\]
</div>

**코드 위치:** Python 149행 / MATLAB 26행 부근. 핵심 변수는 `phase_range`다.

## 다음 글과 관련 글

다음 글: [21 — 전체 코드 다시 읽기: 입력부터 SAR 영상까지]({{ '/sar-basics/21-code-tour/' | relative_url }}). 배열 크기·좌표·검증 한계를 묶어 코드 흐름을 점검한다는 과정을 이어서 살펴본다.

이전 글: [19 — Zero padding: 표본은 늘어나도 정보는 늘지 않는다]({{ '/sar-basics/19-zero-padding/' | relative_url }})

[전체 시리즈 목차]({{ '/sar-basics/series/' | relative_url }})

추가 학습: [NASA/JPL — Radar Short Course](https://science.nasa.gov/mission/nisar/radar-short-course/). 거리 처리, 도플러, 방위 처리, 거리 이동의 학습 주제를 함께 확인할 수 있다.
