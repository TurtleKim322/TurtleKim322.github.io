# Output: assets/img/03_a.png and 03_b.png
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

fig,ax=new("Complex signal: projection on I and Q", "In-phase I", "Quadrature Q",size=(6,6))
u=np.linspace(0,2*np.pi,500)
ax.plot(np.cos(u),np.sin(u),color="gray",alpha=.5)
for phase,color in [(0,BLUE),(np.pi/3,ORANGE),(np.pi,PURPLE)]:
    z=np.exp(1j*phase)
    ax.arrow(0,0,z.real,z.imag,color=color,width=.009,length_includes_head=True,head_width=.08,label=f"Phase {phase/np.pi:.2g} pi")
ax.set(xlim=(-1.3,1.3),ylim=(-1.3,1.3)); ax.set_aspect("equal"); ax.legend(loc="lower left"); save(fig,"03_a.png")
fig,ax=new("Same frequency and amplitude, different phase", "Time (ns)", "Real part")
t=np.linspace(0,.35e-9,1000)
for phase,color in [(0,BLUE),(np.pi/2,ORANGE),(np.pi,PURPLE)]: ax.plot(t*1e9,np.cos(2*np.pi*FC*t+phase),color=color,label=f"Phase {phase/np.pi:.2g} pi")
ax.legend(); save(fig,"03_b.png")
