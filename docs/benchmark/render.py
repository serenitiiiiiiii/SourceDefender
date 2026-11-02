"""Render the published Zero Trust benchmark from results.csv (requires matplotlib)."""
import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, MultipleLocator

HERE = Path(__file__).resolve().parent
EFFORTS = ("low", "medium", "high", "xhigh", "max", "ultra")
MARKERS = ("o", "s", "^", "D", "P", "X")
MODELS = (
    ("gpt-6.1-terra", "GPT-6.1 Terra", "#70a7ff"),
    ("gpt-6.1-sol", "GPT-6.1 Sol", "#ffbd70"),
    ("gpt-6-astra", "GPT-6 Astra", "#7de1bf"),
    ("gpt-daybreak-blue-latest", "Daybreak Blue", "#f28bb4"),
)

with (HERE / "results.csv").open(encoding="utf-8", newline="") as handle:
    rows = list(csv.DictReader(handle))
points = {(r["model"], r["effort"]): r for r in rows if r["result"] == "contained"}
if len(points) != len(rows) or set(points) != {(m[0], e) for m in MODELS for e in EFFORTS}:
    raise ValueError("Expected exactly one contained result per model and effort")

bg, panel, ink, muted, grid = "#0b101a", "#111926", "#edf3fa", "#9eabbc", "#283446"
plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": ink, "axes.labelcolor": ink,
                     "xtick.color": muted, "ytick.color": muted, "savefig.facecolor": bg})
fig = plt.figure(figsize=(16, 9.8), facecolor=bg)
fig.text(.06, .941, "SOURCEDEFENDER   /   MODEL BENCHMARK", color="#8fdacb", fontsize=10, weight="bold")
fig.text(.06, .881, "Score vs. time", fontsize=29, weight="bold")
fig.text(.06, .84, "ZERO TRUST   /   ORBITAL UPLINK   /   NO GIT HISTORY", color=muted, fontsize=10)
fig.text(.94, .916, "24 / 24", fontsize=21, weight="bold", ha="right")
fig.text(.94, .886, "CONFIGURATIONS CONTAINED", color=muted, fontsize=8, ha="right")

ax = fig.add_axes((.075, .215, .625, .56), facecolor=panel)
for spine in ax.spines.values():
    spine.set_visible(False)
ax.grid(color=grid, linewidth=.8, zorder=0)
ax.tick_params(axis="both", length=0, pad=11, labelsize=10)
ax.xaxis.set_major_locator(MultipleLocator(1000))
ax.xaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value:,.0f}"))
ax.yaxis.set_major_locator(MultipleLocator(10))
ax.set_xlim(18750, 13750)
ax.set_ylim(10, 76)
ax.set_xlabel("SOURCEDEFENDER SCORE     /     HIGHER IS BETTER  ←", fontsize=9, weight="bold", labelpad=20)
ax.set_ylabel("SCORED TIME  /  MINUTES", fontsize=9, weight="bold", labelpad=19)

for model, _, color in MODELS:
    group = [points[(model, effort)] for effort in EFFORTS]
    xs = [float(r["score"]) for r in group]
    ys = [float(r["scored_seconds"]) / 60 for r in group]
    # Lines show effort order, not a fit or an extrapolation between models.
    ax.plot(xs, ys, color=color, alpha=.65, linewidth=1.6, zorder=2)
    for x, y, marker in zip(xs, ys, MARKERS):
        ax.scatter(x, y, marker=marker, s=83, c=[color], edgecolor=panel, linewidth=1.2, zorder=3)

side = fig.add_axes((.735, .215, .205, .56), facecolor=panel)
side.set_xticks([]); side.set_yticks([])
for spine in side.spines.values():
    spine.set_visible(False)
side.text(.10, .94, "MODEL", color=muted, fontsize=9, weight="bold", transform=side.transAxes, va="top")
for index, (_, name, color) in enumerate(MODELS):
    y = .855 - index * .075
    side.plot([.10, .22], [y, y], color=color, linewidth=2, transform=side.transAxes)
    side.scatter([.16], [y], color=color, s=35, transform=side.transAxes, zorder=3)
    side.text(.27, y, name, fontsize=10, va="center", transform=side.transAxes)
side.plot([.10, .90], [.53, .53], color=grid, linewidth=1, transform=side.transAxes)
side.text(.10, .48, "REASONING EFFORT", color=muted, fontsize=9, weight="bold", transform=side.transAxes, va="top")
for index, (effort, marker) in enumerate(zip(EFFORTS, MARKERS)):
    col, row = divmod(index, 3)
    x, y = .12 + col * .43, .385 - row * .075
    side.scatter([x], [y], marker=marker, s=45, color=ink, transform=side.transAxes)
    side.text(x + .075, y, effort, fontsize=9, va="center", transform=side.transAxes)
side.text(.10, .10, "Lines connect effort levels\nin order: low → ultra.", color=muted,
          fontsize=8, linespacing=1.5, transform=side.transAxes, va="top")

fig.text(.06, .145, "READING THE CHART", color="#8fdacb", fontsize=9, weight="bold")
fig.text(.06, .110, "Time includes validation and hint penalties. Score uses time and penalties, so the axes are related.",
         color=muted, fontsize=9)
fig.text(.06, .082, "One incident and one run per setting; parallel load affects timing. Lines connect observations, not a fitted trend.",
         color=muted, fontsize=9)
fig.text(.06, .045, "SOURCEDEFENDER   ·   LOCAL AGENT PRACTICE", color="#6e7e92", fontsize=8, weight="bold")
fig.text(.94, .045, "METHODOLOGY & DATA: docs/benchmark", color="#6e7e92", fontsize=8, ha="right")
fig.savefig(HERE / "score-vs-time.png", dpi=200, facecolor=bg)
plt.close(fig)
