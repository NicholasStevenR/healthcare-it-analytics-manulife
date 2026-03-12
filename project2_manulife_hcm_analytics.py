"""
Manulife Financial Project 2: High-Cost Member Predictive Analytics & Care Navigation ROI
XmR (monthly model AUC) + grouped bar (care navigation PMPM by tier) + c-chart inset
Author: Nicholas Steven | github.com/nicholasstevenr
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BLUE   = "#1F4E79"
ORANGE = "#E36C09"
TEAL   = "#00B0A8"
RED    = "#C00000"
LGREY  = "#F2F2F2"

np.random.seed(52)

def auc_xmr(n=24):
    base  = 0.824
    noise = np.random.normal(0, 0.008, n)
    x = np.clip(base + noise, 0.76, 0.90)
    x[6]  = 0.764   # COVID drift
    x[14] = 0.884   # feature enhancement
    x[21] = 0.771   # GLP-1 phenotype gap
    mr     = np.abs(np.diff(x))
    mr_bar = mr.mean()
    x_bar  = x.mean()
    sigma  = mr_bar / 1.128
    ucl    = min(1.0, x_bar + 3 * sigma)
    lcl    = max(0.5, x_bar - 3 * sigma)
    return x, x_bar, ucl, lcl

def escalation_cchart(n=24):
    c_bar = 84.2
    ucl   = c_bar + 3 * np.sqrt(c_bar)
    lcl   = max(0, c_bar - 3 * np.sqrt(c_bar))
    base  = np.random.normal(c_bar, 6.0, n)
    c     = np.clip(base, 40, 108)
    c[10] = 124.0   # cancer surge
    c[18] = 48.0    # tier-down stabilization
    return c, c_bar, ucl, lcl

def plot_charts():
    months = [f"M{i+1}" for i in range(24)]
    x_vals, x_bar, ucl_x, lcl_x = auc_xmr()
    c_vals, c_bar, ucl_c, lcl_c = escalation_cchart()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4))
    fig.patch.set_facecolor("white")

    # Left: AUC XmR
    ax1.set_facecolor(LGREY)
    ax1.plot(range(24), x_vals, color=BLUE, marker="o", markersize=4, linewidth=1.6, zorder=3)
    ax1.axhline(x_bar, color=TEAL, linestyle="--", linewidth=1.2, label=f"X-bar={x_bar:.3f}")
    ax1.axhline(ucl_x, color=RED,  linestyle=":",  linewidth=1.2, label=f"UCL={ucl_x:.3f}")
    ax1.axhline(lcl_x, color=RED,  linestyle=":",  linewidth=1.2, label=f"LCL={lcl_x:.3f}")
    ax1.axhline(0.8,   color="#888888", linestyle="-", linewidth=0.7, alpha=0.5, label="AUC=0.80 Threshold")

    ooc = [i for i in range(24) if x_vals[i] > ucl_x or x_vals[i] < lcl_x]
    for i in ooc:
        ax1.plot(i, x_vals[i], "o", color=ORANGE, markersize=9, zorder=4)

    ann = {6: "COVID\nDrift", 14: "Feature\nEnhancement", 21: "GLP-1\nPhenotype Gap"}
    for i, lbl in ann.items():
        offset = 10 if x_vals[i] > x_bar else -28
        ax1.annotate(lbl, (i, x_vals[i]), textcoords="offset points",
                     xytext=(0, offset), fontsize=6.5, ha="center", color=ORANGE, fontweight="bold")

    ax1.set_xticks(range(24))
    ax1.set_xticklabels(months, fontsize=6.5, rotation=45)
    ax1.set_ylabel("HCM Model AUC (Monthly)", fontsize=8)
    ax1.set_ylim(0.72, 0.92)
    ax1.set_title("HCM Predictive Model AUC XmR\n(X-bar=0.824 | COVID Drift + GLP-1 Gap Detected)", fontsize=9, fontweight="bold", color=BLUE)
    ax1.legend(fontsize=7, loc="upper left")
    ax1.grid(axis="y", alpha=0.4)
    ax1.tick_params(axis="y", labelsize=8)

    # Right: Care Nav PMPM bars + escalation c-chart
    ax2.set_facecolor(LGREY)

    # Escalation c-chart (primary)
    ax2.plot(range(24), c_vals, color=BLUE, marker="o", markersize=4, linewidth=1.6, zorder=3)
    ax2.axhline(c_bar, color=TEAL, linestyle="--", linewidth=1.2, label=f"c-bar={c_bar:.1f}")
    ax2.axhline(ucl_c, color=RED,  linestyle=":",  linewidth=1.2, label=f"UCL={ucl_c:.1f}")
    ax2.axhline(lcl_c, color=RED,  linestyle=":",  linewidth=1.2, label=f"LCL={lcl_c:.1f}")

    ooc_c = [i for i in range(24) if c_vals[i] > ucl_c or c_vals[i] < lcl_c]
    for i in ooc_c:
        ax2.plot(i, c_vals[i], "o", color=ORANGE, markersize=9, zorder=4)

    ann_c = {10: "Cancer\nDiagnosis Surge", 18: "Tier-Down\nStabilization"}
    for i, lbl in ann_c.items():
        offset = 10 if c_vals[i] > c_bar else -28
        ax2.annotate(lbl, (i, c_vals[i]), textcoords="offset points",
                     xytext=(0, offset), fontsize=6.5, ha="center", color=ORANGE, fontweight="bold")

    # Care Nav ROI inset bars
    tiers  = ["T3\nIntensive", "T2\nNavigator", "T1\nDigital", "Control\nDeclined"]
    pmpm   = [1684, 2184, 2842, 3842]
    t_cols = [TEAL, BLUE, ORANGE, RED]
    for j, (lbl, val, col) in enumerate(zip(tiers, pmpm, t_cols)):
        ax2.bar(17.0 + j * 1.7, val / 80, 1.3, bottom=36,
                color=col, alpha=0.82, zorder=3)
        ax2.text(17.0 + j * 1.7, 36 + val / 80 + 0.5, f"${val//1000}K",
                 ha="center", fontsize=6.5, fontweight="bold")
        ax2.text(17.0 + j * 1.7, 34.5, lbl.split("\n")[0], ha="center", fontsize=5.5, color=col)
    ax2.text(19.55, 36 + 3842 / 80 + 3, "PMPM Fwd Claims\nby Nav Tier", ha="center",
             fontsize=6, color=BLUE, style="italic")

    ax2.set_xticks(range(24))
    ax2.set_xticklabels(months, fontsize=6.5, rotation=45)
    ax2.set_ylabel("Monthly Care Nav Escalations", fontsize=8)
    ax2.set_ylim(25, 135)
    ax2.set_title("Care Nav Escalation c-Chart\n(c-bar=84.2 | T3 Intensive -56.2% PMPM vs Control)", fontsize=9, fontweight="bold", color=BLUE)
    ax2.legend(fontsize=7, loc="upper left")
    ax2.grid(axis="y", alpha=0.4)
    ax2.tick_params(axis="y", labelsize=8)

    fig.text(0.5, 0.01, "Nicholas Steven - github.com/nicholasstevenr",
             ha="center", fontsize=7, color="#888888", style="italic")
    plt.tight_layout(rect=[0, 0.04, 1, 1])
    out = "/sessions/focused-epic-turing/mnt/job application/Applications/Manulife/chart_p2.png"
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {out}")

if __name__ == "__main__":
    plot_charts()
