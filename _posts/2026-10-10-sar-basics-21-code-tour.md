---
title: "SAR 기초 21 — 전체 코드 다시 읽기: 입력부터 SAR 영상까지"
date: 2026-10-10
last_modified_at: 2026-10-10
date_format: "%Y년 %m월 %d일"
categories: [SAR, 신호처리]
tags: [SAR, Radar, Python, Signal Processing]
permalink: /sar-basics/21-code-tour/
series: sar-basics
series_order: 21
toc: true
toc_sticky: true
math: true
header:
  teaser: /assets/img/sar-basics/21_a.png
description: "마지막으로 원본 코드의 입력부터 출력까지 다시 연결한다. 처리 공식뿐 아니라 배열 크기, 범위 선택, 좌표 원점, 검증 범위를 함께 살펴보며 어떤 결과를 확인했고 무엇은 아직 확인하지 않았는지 정리한다."
---

## 한 줄 요약

마지막으로 원본 코드의 입력부터 출력까지 다시 연결한다. 처리 공식뿐 아니라 배열 크기, 범위 선택, 좌표 원점, 검증 범위를 함께 살펴보며 어떤 결과를 확인했고 무엇은 아직 확인하지 않았는지 정리한다.

## 왜 중요한가

실행이 끝났다는 사실만으로 영상이 정확하다고 결론 낼 수는 없다. 코드에는 특정 장면을 전제로 고정한 구간과 진단용 확대가 들어 있다. 조건을 바꿀 때 어디를 다시 확인해야 하는지 아는 것이 재사용의 출발점이다.

## 핵심 개념

입력은 100개의 가상 점 표적과 레이더 파라미터다. 플랫폼 위치별 거리를 계산해 빔 안의 표적 신호를 더하고, 거리 상관과 관심 구간 선택을 거쳐 방위 FFT를 수행한다. 각 도플러 열을 보간한 뒤 거리별 방위 기준과 상관하여 영상을 만든다.

원본 Python은 난수 시드 0을 사용하므로 같은 환경에서 같은 표적 위치를 다시 만든다. 반면 MATLAB 원본은 시드를 고정하지 않은 rand를 사용한다. 두 언어의 결과 영상을 픽셀 단위로 비교하려면 먼저 입력 표적 자체를 일치시켜야 한다. 이번 분석은 MATLAB을 실행한 수치 동등성 검증이 아니다.

또한 원본 방위축은 기준 신호 중심에 대한 상대 좌표다. 입력 표적 좌표와 비교할 때 중심 펄스의 플랫폼 위치를 더해야 한다. FFT의 0 채우기로 늘어난 구간을 실제로 추가 관측한 개구로 읽어서도 안 된다.

## 핵심 수식

<div class="sar-math">
\[
y_{physical}[q]=\left(q-\frac{N_{FFT}}2\right)\Delta y+y\!\left[\left\lfloor\frac{N_p}{2}\right\rfloor\right],\qquad r[k]=\frac{c\,\mathrm{SWST}}2+k\Delta r
\]
</div>

| 기호 | 의미 | 단위 |
|---|---|---|
| q, k | 출력 방위 인덱스, 원래 거리축 인덱스 | 없음 |
| NFFT, Np | 방위 FFT 길이, 실제 펄스 수 | 없음 |
| Δy, Δr | 방위·거리 표본 간격 | m |
| y[·] | 해당 펄스의 플랫폼 위치 | m |
| SWST | 수신 창 시작 시각 | s |

## 수식의 물리적 의미

상관 기준의 중심을 배열 어디에 넣었는지가 출력 지연의 기준을 결정한다. fftshift 후의 중앙을 단순히 물리 좌표 0이라고 정하면 입력 표적과 어긋난다. 위 식은 이 원본의 기준 배치에서 나온 좌표식이며 모든 SAR 코드에 동일하게 적용할 공식은 아니다.

## 현재 SAR 코드와 연결

```python
# Coordinate interpretation used for the verified source run.
physical_azimuth = az + y[num_azimuth_samples // 2]
peak_row, peak_col = np.unravel_index(np.abs(SAR_img).argmax(), SAR_img.shape)
peak_range = r1[peak_row]
peak_azimuth = physical_azimuth[peak_col]
```

이 코드는 원본 출력 변수에 적용하는 진단용 코드다. 표적 하나만 놓은 경우에 전체 최대점과 참 위치를 비교한다. 여러 표적이 있는 기본 장면에서 최대점 하나를 찾는 것은 전체 표적 검출률 검증이 아니다. 원본 마지막의 고정된 64×64 확대 영역도 자동 단일 표적 검사와 구별한다.

코드 위치: `SAR_python.py` 355행 부근 / `SAR_m.m` 168행 부근. 본문의 짧은 코드는 해당 연산을 발췌하거나 설명을 위해 정리한 것이다. 분석 기준은 직접 실험한 점 표적 SAR 시뮬레이터다. 이 연재에서는 신호처리 원리와 수학에 집중한다.

## 시각적 설명

![처리 단계별 배열 크기]({{ '/assets/img/sar-basics/21_a.png' | relative_url }})

그림 A는 검증 실행에서 기록한 배열 크기를 complex128의 16바이트로 환산했다. 한 배열의 저장량이며 전체 실행 메모리 최대값이 아니다.

![검증된 표본 격자와 표적 위치]({{ '/assets/img/sar-basics/21_b.png' | relative_url }})

그림 B는 단일 표적 실행에서 기록한 최대점과 표본 격자를 표시한다. 그림 스크립트 자체가 원본 시뮬레이션을 다시 실행하는 것은 아니며, 기록의 근거는 validation 폴더에 보관했다.

## 그림 생성 코드

아래 코드는 [figures/fig_21_code_tour.py]({{ '/assets/code/sar-basics/fig_21_code_tour.py' | relative_url }})에도 저장되어 있다. NumPy와 Matplotlib만 사용하며, 해당 경로에 파일을 두고 실행하면 현재 작업 폴더와 관계없이 `assets/img/`에 PNG 두 개를 저장한다. 그림의 영문 축·단위는 본문 캡션과 함께 읽는다.

```python
# Output: assets/img/21_a.png and 21_b.png
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

# Dimensions recorded in the verified seed-0 Python run.
labels=["Raw (2083 x 1642)","Range correlation (4096 x 1642)","Cropped range (251 x 1642)","Doppler / image (251 x 4096)"]
shapes=[(2083,1642),(4096,1642),(251,1642),(251,4096)]
fig,ax=new("Complex128 array sizes for this input", "Single-array storage (MiB)", "",size=(10,5))
memory=np.array([r*c*16/2**20 for r,c in shapes]); ax.barh(labels,memory,color=BLUE)
for i,m in enumerate(memory): ax.text(m+1,i,f"{m:.1f}",va="center")
ax.set_xlim(0,memory.max()*1.18); ax.invert_yaxis(); save(fig,"21_a.png")
fig,ax=new("Verified isolated-target peak vs physical sample grid", "Azimuth relative to true target (m)", "Range relative to true target (m)",size=(7,5))
dr=C/(2*FS); dy=V*PRI
xx,yy=np.meshgrid(np.arange(-3,4)*dy+.0050510632,np.arange(-3,4)*dr)
ax.scatter(xx,yy,s=15,c="#b8cbd1",label="Sample centers")
ax.scatter([0],[0],s=130,marker="+",c=ORANGE,label="True target (5025 m, 25 m)",zorder=4)
ax.scatter([.0050510632],[0],s=80,marker="x",c=PURPLE,label="Recorded peak (5025 m, 25.005051 m)",zorder=5)
ax.legend(fontsize=9); save(fig,"21_b.png")
```

## 숫자 예제

검증한 기본 Python 입력의 크기는 RawData 2083×1642, 거리 상관 4096×1642, 거리 선택 후 251×1642, 최종 영상 251×4096이다. 거리 선택 199:450은 4919.4~5069.4 m에 해당한다. 별도의 단일 표적 (5025 m, 25 m)에서는 최대점이 (5025 m, 25.005051 m)에 나타나 두 축 모두 한 표본 이내였다.

## 직접 확인해 보기

다음 실험은 고립된 표적에서 −3 dB 폭, PSLR, ISLR을 명확한 정의로 측정하는 것이다. RCMC 전후를 같은 조건으로 비교하고 경계 부근의 표적도 점검하면 좋다. 원본 depth_of_focus 출력은 이번 연재에서 검증한 성능 지표로 사용하지 않았다.

## 요약 / 핵심 공식 / 코드 위치

- 크기·축·좌표 원점을 공식과 함께 확인한다.
- 단일 표적 위치 검증은 전체 영상 성능 검증과 다르다.
- 고정 거리 구간과 진단 위치는 입력 변경 시 다시 검토한다.

**핵심 공식**

<div class="sar-math">
\[
y_{physical}[q]=\left(q-\frac{N_{FFT}}2\right)\Delta y+y\!\left[\left\lfloor\frac{N_p}{2}\right\rfloor\right],\qquad r[k]=\frac{c\,\mathrm{SWST}}2+k\Delta r
\]
</div>

**코드 위치:** Python 355행 / MATLAB 168행 부근. 핵심 변수는 `az`다.

## 다음 글과 관련 글

이 시리즈의 설명은 여기서 마친다. 다음 실험에서는 단일 표적의 응답 폭과 부엽을 정량적으로 측정하고, 잡음과 경계 표적을 추가해 볼 수 있다.

이전 글: [20 — SAR 코드를 읽기 위한 수학·신호처리 로드맵]({{ '/sar-basics/20-roadmap/' | relative_url }})

[전체 시리즈 목차]({{ '/sar-basics/series/' | relative_url }})
