# Output: assets/img/11_a.png and 11_b.png
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

t=(np.arange(1251)-625)/FS; ref=np.exp(1j*np.pi*(B/TP)*t*t)
x=np.zeros(2200,dtype=complex); offset=300; x[offset:offset+len(ref)]=ref
fig,ax=new("A delayed finite chirp before compression", "Record time (microseconds)", "Amplitude")
tr=np.arange(len(x))/FS
ax.plot(tr*1e6,x.real,color=BLUE,lw=.5,label="Real part")
ax.plot(tr*1e6,np.abs(x),color=ORANGE,label="Envelope")
ax.legend(); save(fig,"11_a.png")
nfft=1<<int(np.ceil(np.log2(len(x)+len(ref)-1)))
y=np.fft.ifft(np.fft.fft(x,nfft)*np.conj(np.fft.fft(ref*np.hamming(len(ref)),nfft)))
assert np.argmax(np.abs(y))==offset
lag=(np.arange(nfft)-offset)*C/(2*FS)
fig,ax=new("Range compression with a Hamming-weighted reference", "Range lag relative to true delay (m)", "Relative amplitude (dB)")
ax.plot(lag,db(y),color=BLUE); ax.set(xlim=(-10,10),ylim=(-70,2)); save(fig,"11_b.png")
