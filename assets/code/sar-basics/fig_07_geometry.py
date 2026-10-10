# Output: assets/img/07_a.png and 07_b.png
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

fig,ax=new("Broadside geometry (schematic; unequal axis scales)", "Cross-track x (m)", "Along-track y (m)")
yp=np.array([-130,0,130]); ax.plot([0,0],[-170,170],color=BLUE,lw=2,label="Platform path")
ax.scatter(np.zeros(3),yp,color=BLUE); ax.scatter([R0],[0],color=ORANGE,s=100,label="Fixed target")
for p in yp: ax.plot([0,R0],[p,0],ls="--",alpha=.6,label="Slant range" if p==-130 else None)
ax.annotate("Velocity V",xy=(0,160),xytext=(600,115),arrowprops=dict(arrowstyle="->"))
ax.legend(loc="lower right"); save(fig,"07_a.png")
fig,ax=new("Range changes along the flight path", "Platform y relative to target (m)", "R - R0 (m)")
y=np.linspace(-180,180,600); ax.plot(y,np.sqrt(R0**2+y*y)-R0,color=BLUE)
edge=R0*np.tan(THETA/2)
ax.axvspan(-edge,edge,alpha=.13,color=ORANGE,label="Inside 3-degree beam")
ax.legend(); save(fig,"07_b.png")
