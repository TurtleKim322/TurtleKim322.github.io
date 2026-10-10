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
