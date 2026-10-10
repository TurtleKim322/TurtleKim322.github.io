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
