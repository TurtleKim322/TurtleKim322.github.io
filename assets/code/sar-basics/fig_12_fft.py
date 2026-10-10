# Output: assets/img/12_a.png and 12_b.png
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

n=256; t=np.arange(n)/FS
x=np.exp(2j*np.pi*30e6*t)+.6*np.exp(2j*np.pi*70e6*t)
fig,axes=plt.subplots(1,2,figsize=(11,4.5),layout="constrained")
axes[0].plot(t[:80]*1e9,x[:80].real,color=BLUE); axes[0].set(title="Two complex tones: real part",xlabel="Time (ns)",ylabel="Amplitude")
f=np.fft.fftshift(np.fft.fftfreq(n,1/FS)); spec=np.fft.fftshift(np.fft.fft(x))
axes[1].plot(f/1e6,np.abs(spec)/n,color=PURPLE); axes[1].set(title="DFT amplitude",xlabel="Frequency (MHz)",ylabel="Amplitude / N")
for ax in axes: ax.grid(alpha=.2)
save(fig,"12_a.png")
fig,ax=new("DFT bins are samples of a spectrum", "Frequency (MHz)", "Amplitude / N")
sel=(f>23e6)&(f<37e6)
ax.stem(f[sel]/1e6,np.abs(spec[sel])/n)
ax.text(.03,.9,f"Bin spacing = fs/N = {FS/n/1e6:.4f} MHz",transform=ax.transAxes)
save(fig,"12_b.png")
