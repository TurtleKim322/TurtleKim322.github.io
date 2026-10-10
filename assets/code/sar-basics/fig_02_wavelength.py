# Output: assets/img/02_a.png and 02_b.png
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

fig,axes=plt.subplots(2,1,figsize=(9,5),layout="constrained",sharex=True)
x=np.linspace(0,.18,2000)
for ax,f in zip(axes,[5e9,10e9]):
    wave=C/f
    ax.plot(x*100,np.cos(2*np.pi*x/wave),color=BLUE)
    ax.annotate("",xy=(0,1.2),xytext=(wave*100,1.2),arrowprops=dict(arrowstyle="<->",color=ORANGE))
    ax.set(title=f"{f/1e9:g} GHz: wavelength {wave*100:g} cm",ylabel="Amplitude",ylim=(-1.4,1.5)); ax.grid(alpha=.2)
axes[-1].set_xlabel("Distance along wave (cm)"); save(fig,"02_a.png")
fig,ax=new("Wavelength is inversely proportional to frequency", "Carrier frequency (GHz)", "Wavelength (cm)")
f=np.linspace(1e9,20e9,400)
ax.plot(f/1e9,C/f*100,color=BLUE)
ax.scatter([10],[3],color=ORANGE,label="10 GHz -> 3 cm"); ax.legend(); save(fig,"02_b.png")
