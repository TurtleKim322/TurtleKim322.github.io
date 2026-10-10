---
title: "SAR 기초 14 — RCMC: 휘어진 표적 응답을 같은 거리로 맞추기"
date: 2026-10-10
last_modified_at: 2026-10-10
date_format: "%Y년 %m월 %d일"
categories: [SAR, 신호처리]
tags: [SAR, Radar, Python, Signal Processing]
permalink: /sar-basics/14-rcmc/
series: sar-basics
series_order: 14
toc: true
toc_sticky: true
math: true
header:
  teaser: /assets/img/sar-basics/14_a.png
---

## 한 줄 요약

한 표적까지의 거리는 플랫폼 이동에 따라 변하므로 표적 응답이 여러 거리 셀을 지나간다. RCMC는 도플러별로 입력 거리 위치를 다시 읽어, 같은 최단 거리의 응답으로 정렬하는 단계다.

## 왜 중요한가

거리 압축은 각 펄스의 긴 신호를 좁혀 주지만 펄스마다 달라지는 표적 거리까지 고정하지는 않는다. 그 이동을 무시하면 이후 방위 압축에서 같은 거리 행으로 합쳐야 할 신호가 흩어질 수 있다.

## 핵심 개념

표적의 거리 곡선이 휘어 있다는 것은 같은 표적의 최대 응답이 열마다 다른 행에 놓일 수 있다는 뜻이다. 거리-도플러 영역에서도 도플러에 따라 응답의 거리 위치가 달라진다. 등속 broadside 기하에서 이 위치를 최단 거리와 도플러의 함수로 쓸 수 있다.

보정은 결과의 각 거리 r를 채우기 위해 입력의 어디를 읽을지 정하는 역매핑이다. 원본 식 ri=r/D에서 r는 원하는 출력 좌표이고 ri는 읽어야 하는 입력 좌표다. 입력을 무조건 ri로 밀어 넣는 전방 이동과 혼동하면 부호나 방향이 뒤집힌다.

ri는 대개 정수 표본 위치와 일치하지 않는다. 그래서 주변 표본을 이용해 값을 추정하는 보간이 필요하다. 복소수 신호는 실수부와 허수부를 보존한 채 보간해야 한다.

## 핵심 수식

<div class="sar-math">
\[
D(f_D)=\sqrt{1-\left(\frac{f_D\lambda}{2V}\right)^2},\qquad r_i=\frac{r}{D(f_D)},\qquad S_{\mathrm{out}}(r,f_D)=S_{\mathrm{in}}(r_i,f_D)
\]
</div>

| 기호 | 의미 | 단위 |
|---|---|---|
| r | 원하는 출력 거리, 최단 거리 좌표 | m |
| ri | 같은 도플러에서 읽을 입력 거리 | m |
| fD, λ, V | 도플러, 파장, 플랫폼 속도 | Hz, m, m/s |
| D | 기하에 따른 거리 축척 | 없음 |

## 수식의 물리적 의미

도플러 0에서는 D=1이므로 이동이 없다. 도플러 절댓값이 커지면 D가 작아져 입력의 더 먼 거리를 읽는다. 이는 최근접에서 멀어진 관측일수록 실제 거리가 길어진다는 기하와 일치한다. 식은 해당 운동 모델의 도플러-기하 대응을 사용하며 모든 관측 조건의 오차를 해결하는 보편식은 아니다.

## 현재 SAR 코드와 연결

```python
inside = 1.0 - (fd[a] * lam / (2 * V))**2
ri = r1 / np.sqrt(inside)
cs_real = CubicSpline(r1, rd[:, a].real, extrapolate=False)
cs_imag = CubicSpline(r1, rd[:, a].imag, extrapolate=False)
interp_vals = cs_real(ri) + 1j * cs_imag(ri)
```

a는 도플러 열이다. 원본은 inside가 양수인지 먼저 검사하고, 실수부와 허수부를 cubic spline으로 보간한다. 범위 밖 값은 후속 처리에서 0으로 바꾼다. 아래 교육용 그림은 방향을 명확히 보여 주기 위해 NumPy의 선형 보간을 사용하며 원본 spline과 수치적으로 같다고 주장하지 않는다.

코드 위치: `SAR_python.py` 253행 부근 / `SAR_m.m` 120행 부근. 본문의 짧은 코드는 해당 연산을 발췌하거나 설명을 위해 정리한 것이다. 분석 기준은 직접 실험한 점 표적 SAR 시뮬레이터다. 이 연재에서는 신호처리 원리와 수학에 집중한다.

## 시각적 설명

![보정 전후의 이상화된 도플러 trace]({{ '/assets/img/sar-basics/14_a.png' | relative_url }})

그림 A는 이상화한 RD 응답을 만든 뒤 실제 역매핑 보간을 수행한 결과다. 전후에 같은 색 범위를 사용한다. 실제 원시 신호에서 얻은 RCMC 성능 검증은 아니다.

![분수 표본 위치의 보간]({{ '/assets/img/sar-basics/14_b.png' | relative_url }})

그림 B는 한 도플러 열을 확대해 r=5025 m의 출력을 채우려면 약 5026.7 m의 입력을 읽는다는 점을 보여 준다.

## 그림 생성 코드

아래 코드는 [figures/fig_14_rcmc.py]({{ '/assets/code/sar-basics/fig_14_rcmc.py' | relative_url }})에도 저장되어 있다. NumPy와 Matplotlib만 사용하며, 해당 경로에 파일을 두고 실행하면 현재 작업 폴더와 관계없이 `assets/img/`에 PNG 두 개를 저장한다. 그림의 영문 축·단위는 본문 캡션과 함께 읽는다.

```python
# Output: assets/img/14_a.png and 14_b.png
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

# Idealized Range-Doppler response: controlled interpolation demonstration.
rr=np.arange(5022,5030,.15); fd=np.linspace(-175,175,301)
D=np.sqrt(1-(fd*LAM/(2*V))**2); center=R0/D
before=np.exp(-((rr[:,None]-center[None,:])/.3)**2)
after=np.column_stack([np.interp(rr/D[k],rr,before[:,k],left=0,right=0) for k in range(len(fd))])
fig,axes=plt.subplots(1,2,figsize=(11,4.5),layout="constrained",sharey=True)
for ax,a,title in zip(axes,[before,after],["Before RCMC (model)","After inverse mapping"]):
    ax.imshow(a,origin="lower",aspect="auto",extent=[fd[0],fd[-1],rr[0],rr[-1]],cmap="magma",vmin=0,vmax=1)
    ax.axhline(R0,color="cyan",ls="--",lw=.8); ax.set(title=title,xlabel="Doppler (Hz)",ylabel="Range (m)")
save(fig,"14_a.png")
fig,ax=new("Read input r/D to fill output r: one Doppler column", "Input range (m)", "Amplitude")
k=-1; ax.plot(rr,before[:,k],"o-",color=BLUE,label="Input samples")
query=R0/D[k]; value=np.interp(query,rr,before[:,k])
ax.scatter([query],[value],color=ORANGE,s=90,label=f"Read at {query:.3f} m for output 5025 m",zorder=4)
ax.axvline(query,color=ORANGE,ls="--"); ax.set_xlim(5025,5028); ax.legend(fontsize=9); save(fig,"14_b.png")
```

## 숫자 예제

r=5025 m, fD≈174.533 Hz에서 D≈0.999657이고 ri−r≈1.723 m다. 원본 거리 표본 0.60 m로 약 2.87칸을 이동하는 규모다. 이만큼의 입력 거리 여유가 필요하므로 표적 바로 주변만 좁게 잘라내면 보정 과정에서 정보를 잃을 수 있다.

## 직접 확인해 보기

fD=0을 넣으면 그림의 이동량이 정확히 0이어야 한다. 또한 ±fD의 이동량은 제곱 항 때문에 같다. 이 두 대칭성은 구현 방향을 확인하는 간단한 기준이다.

## 요약 / 핵심 공식 / 코드 위치

- RCMC는 거리 압축과 별개의 정렬 단계다.
- 출력 r를 위해 입력 r/D를 읽는다.
- 범위 밖 보간, 복소수 보존, 유효 주파수 범위를 점검한다.

**핵심 공식**

<div class="sar-math">
\[
D(f_D)=\sqrt{1-\left(\frac{f_D\lambda}{2V}\right)^2},\qquad r_i=\frac{r}{D(f_D)},\qquad S_{\mathrm{out}}(r,f_D)=S_{\mathrm{in}}(r_i,f_D)
\]
</div>

**코드 위치:** Python 253행 / MATLAB 120행 부근. 핵심 변수는 `ri`다.

## 다음 글과 관련 글

다음 글: [15 — 방위 chirp와 방위 압축: 이동 중 모은 신호 합치기]({{ '/sar-basics/15-azimuth-compression/' | relative_url }}). 거리의 이차 근사에서 방위 chirp rate를 구한다는 과정을 이어서 살펴본다.

이전 글: [13 — Range-Doppler 영역: 방위축을 주파수축으로 바꾸기]({{ '/sar-basics/13-range-doppler/' | relative_url }})

[전체 시리즈 목차]({{ '/sar-basics/series/' | relative_url }})
