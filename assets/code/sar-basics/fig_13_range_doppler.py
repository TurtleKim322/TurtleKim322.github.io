# Output: assets/img/13_a.png and 13_b.png
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

# A single-target range-compressed model, not the original raw-data run.
eta=(np.arange(1024)-512)*PRI; rr=np.linspace(5023,5030,220)
r=np.sqrt(R0**2+(V*eta)**2); ka=2*V*V/(LAM*R0)
a=np.exp(-((rr[:,None]-r[None,:])/.45)**2)*np.exp(-1j*np.pi*ka*eta[None,:]**2)
a*= (np.abs(eta)<1.3)[None,:]
fig,ax=new("Illustrative range-compressed target", "Slow time (s)", "Range (m)")
ax.grid(False); im=ax.imshow(db(a,-45),origin="lower",aspect="auto",extent=[eta[0],eta[-1],rr[0],rr[-1]],cmap="magma",vmin=-45,vmax=0)
fig.colorbar(im,ax=ax,label="Relative amplitude (dB)"); save(fig,"13_a.png")
rd=np.fft.fftshift(np.fft.fft(a,axis=1),axes=1); fd=np.fft.fftshift(np.fft.fftfreq(len(eta),PRI))
fig,ax=new("Same model after azimuth FFT", "Azimuth Doppler frequency (Hz)", "Range (m)")
ax.grid(False); im=ax.imshow(db(rd,-45),origin="lower",aspect="auto",extent=[fd[0],fd[-1],rr[0],rr[-1]],cmap="magma",vmin=-45,vmax=0)
fig.colorbar(im,ax=ax,label="Relative amplitude (dB)"); save(fig,"13_b.png")
