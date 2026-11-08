import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "sekiller")
os.makedirs(OUT, exist_ok=True)

BLUE, ORANGE = "#2a78d6", "#eb6834"
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e4e3df"
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 9, "axes.edgecolor": INK2,
    "axes.labelcolor": INK, "xtick.color": INK2, "ytick.color": INK2,
    "axes.spines.top": False, "axes.spines.right": False, "axes.linewidth": 0.6,
    "xtick.major.width": 0.6, "ytick.major.width": 0.6, "hatch.linewidth": 0.6,
    "hatch.color": "white", "savefig.dpi": 300, "savefig.bbox": "tight",
})
HATCH = "////"
from matplotlib.ticker import FuncFormatter
TRF = FuncFormatter(lambda v, _: f"{v:.1f}".replace(".", ","))

def save(fig, name):
    fig.savefig(f"{OUT}/{name}.png"); fig.savefig(f"{OUT}/{name}.pdf"); plt.close(fig)

# ---- Şekil 1: Tekrar oranı -------------------------------------------------
classes = ["BENIGN", "DoS", "RPM", "SPEED", "STEERING_WHEEL", "GAS"]
total = [1_223_737, 74_663, 54_900, 24_951, 19_977, 9_991]
uniq = [3_547, 21, 10, 5, 3, 2]
y = np.arange(len(classes))[::-1]
fig, ax = plt.subplots(figsize=(6.0, 2.9))
h = 0.36
ax.barh(y + h/2, total, h, color=BLUE, label="Toplam satır", edgecolor="white", linewidth=1)
ax.barh(y - h/2, uniq, h, color=ORANGE, hatch=HATCH, label="Benzersiz çerçeve", edgecolor="white", linewidth=1)
ax.set_xscale("log"); ax.set_xlim(1, 1e7)
for yi, t, u in zip(y, total, uniq):
    ax.text(t * 1.15, yi + h/2, f"{t:,}".replace(",", "."), va="center", fontsize=7.5, color=INK2)
    ax.text(u * 1.15, yi - h/2, f"{u:,}".replace(",", "."), va="center", fontsize=7.5, color=INK)
ax.set_yticks(y, classes); ax.tick_params(axis="y", length=0)
ax.set_xlabel("Satır sayısı (log ölçek)")
ax.grid(axis="x", color=GRID, linewidth=0.6); ax.set_axisbelow(True)
ax.legend(frameon=False, loc="lower right", fontsize=8)
save(fig, "sekil1_tekrar_orani")

# ---- Şekil 2: Rastgele ve sıralı bölmede modeller ve temel çizgiler ----
models = ["Ezber tablosu*", "Yalnızca CAN ID*", "Lojistik regresyon", "Karar ağacı",
          "Random Forest", "MLP", "LightGBM"]
f1_rnd = [1.0000, 0.7950, 0.8596, 1.0000, 1.0000, 1.0000, 1.0000]
f1_seq = [0.5189, 0.6266, 0.6614, 0.8026, 0.7212, 0.6911, 0.8026]
sd_seq = [0, 0, 0, 0, 0.0754, 0, 0]
y = np.arange(len(models))[::-1]; h = 0.38
fig, ax = plt.subplots(figsize=(6.0, 3.3))
ax.barh(y + h/2, f1_rnd, h, color=BLUE, edgecolor="white", linewidth=1, label="Rastgele %80/20 (literatür)")
ax.barh(y - h/2, f1_seq, h, color=ORANGE, hatch=HATCH, edgecolor="white", linewidth=1, label="Sıralı %80/20 (orijinal makale)")
for yi, b, sd in zip(y, f1_seq, sd_seq):
    if sd > 0:
        ax.errorbar(b, yi - h/2, xerr=sd, fmt="none", ecolor=INK2, elinewidth=0.8, capsize=2)
for yi, a, b, sd in zip(y, f1_rnd, f1_seq, sd_seq):
    ax.text(a + 0.01, yi + h/2, f"{a:.3f}".replace(".", ","), va="center", fontsize=7, color=INK)
    ax.text(b + sd + 0.01, yi - h/2, f"{b:.3f}".replace(".", ","), va="center", fontsize=7, color=INK)
ax.axvline(0.76, color=INK2, linewidth=0.8, linestyle=(0, (3, 3)))
ax.text(0.765, y[-1] - 0.75, "Neto vd. RF: 0,76", fontsize=7, color=INK2, va="center")
ax.set_yticks(y, models); ax.tick_params(axis="y", length=0)
ax.set_xlim(0, 1.12); ax.set_ylim(y[-1] - 1.0, y[0] + 0.6)
ax.set_xlabel("Makro F1 (5 tohum ortalaması; * önemsiz temel çizgi)")
ax.xaxis.set_major_formatter(TRF)
ax.grid(axis="x", color=GRID, linewidth=0.6); ax.set_axisbelow(True)
ax.legend(frameon=False, loc="lower center", ncol=2, fontsize=7.5, bbox_to_anchor=(0.5, 1.0))
save(fig, "sekil2_as2_temel_cizgiler")

# ---- Şekil 3: Protokole göre saldırı tespit oranı -------------------------
rows = [
    ("Random Forest — rastgele bölme\n(saldırılar eğitimde görülmüş)", 1.000, None),
    ("ID beyaz listesi (kural)", 1.000, "ID"),
    ("LOF, tek sınıflı", 0.937, "ID"),
    ("LOF, tek sınıflı", 0.337, "veri"),
    ("Random Forest, saldırı dışarıda", 0.568, "ID"),
    ("Random Forest, saldırı dışarıda", 0.365, "veri"),
]
fig, ax = plt.subplots(figsize=(6.0, 3.0))
y = np.arange(len(rows))[::-1].astype(float)
y[0] += 0.35
for yi, (lab, v, fs) in zip(y, rows):
    if fs is None:
        col, hat = "#6b6a66", None
    elif fs == "ID":
        col, hat = BLUE, None
    else:
        col, hat = ORANGE, HATCH
    ax.barh(yi, v, 0.6, color=col, hatch=hat, edgecolor="white", linewidth=1)
    ax.text(v + 0.01, yi, f"%{v*100:.1f}".replace(".", ","), va="center", fontsize=7.5, color=INK)
labels = [r[0] for r in rows]
ax.set_yticks(y, labels); ax.tick_params(axis="y", length=0)
ax.axhline(y[0] - 0.6, color=INK2, linewidth=0.6, linestyle=(0, (3, 3)))
ax.text(1.12, y[0] - 0.75, "görülmemiş saldırılar ↓", ha="right", va="top", fontsize=7.5, color=INK2)
ax.set_xlim(0, 1.15); ax.set_xlabel("Saldırı tespit oranı"); ax.xaxis.set_major_formatter(TRF)
ax.grid(axis="x", color=GRID, linewidth=0.6); ax.set_axisbelow(True)
ax.legend(handles=[Patch(facecolor=BLUE, label="ID + veri baytları"),
                   Patch(facecolor=ORANGE, hatch=HATCH, edgecolor="white", label="Yalnızca veri baytları")],
          frameon=False, loc="lower right", fontsize=8)
save(fig, "sekil3_protokol_karsilastirma")

# ---- Şekil 4: Saldırı türüne göre ID'li / ID'siz tespit -------------------
att = ["DoS", "GAS", "RPM", "SPEED", "STEERING\nWHEEL"]
lof_id = [1.0, 0.5, 0.84, 1.0, 1.0]; lof_pl = [0.0, 0.5, 0.70, 1.0, 0.267]
rf_id = [0.667, 0.5, 0.30, 0.84, 0.533]; rf_pl = [0.057, 0.0, 0.30, 0.80, 0.667]
fig, axes = plt.subplots(1, 2, figsize=(6.4, 2.6), sharey=True)
x = np.arange(len(att)); w = 0.38
for ax, (a, b, title) in zip(axes, [(lof_id, lof_pl, "(a) LOF, tek sınıflı anomali tespiti"),
                                    (rf_id, rf_pl, "(b) Random Forest, saldırı dışarıda bırakılarak")]):
    ax.bar(x - w/2, a, w, color=BLUE, edgecolor="white", linewidth=1)
    ax.bar(x + w/2, b, w, color=ORANGE, hatch=HATCH, edgecolor="white", linewidth=1)
    for xi, v in zip(x - w/2, a):
        ax.text(xi, v + 0.02, f"{v*100:.0f}", ha="center", fontsize=6.5, color=INK)
    for xi, v in zip(x + w/2, b):
        ax.text(xi, v + 0.02, f"{v*100:.0f}", ha="center", fontsize=6.5, color=INK)
    ax.set_xticks(x, att, fontsize=7.5); ax.tick_params(axis="x", length=0)
    ax.set_ylim(0, 1.12); ax.set_title(title, fontsize=8.5, color=INK, loc="left")
    ax.grid(axis="y", color=GRID, linewidth=0.6); ax.set_axisbelow(True)
axes[0].set_ylabel("Tespit oranı")
axes[0].set_yticks([0, .25, .5, .75, 1], ["0", "0,25", "0,50", "0,75", "1"])
fig.legend(handles=[Patch(facecolor=BLUE, label="ID + veri baytları"),
                    Patch(facecolor=ORANGE, hatch=HATCH, edgecolor="white", label="Yalnızca veri baytları")],
           frameon=False, loc="lower center", ncol=2, fontsize=8, bbox_to_anchor=(0.5, -0.08))
fig.tight_layout(rect=(0, 0.05, 1, 1))
save(fig, "sekil4_sinif_bazinda_tespit")
print("ok")
