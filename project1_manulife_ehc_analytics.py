"""
Manulife Financial Project 1: Extended Health Care Claims & Paramedical Analytics
XmR (EHC PMPM) + p-chart (paramedical utilization rate) + PMPM breakdown bar
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

np.random.seed(31)

def ehc_xmr(n=24):
    base  = 142.4
    noise = np.random.normal(0, 5.5, n)
    x = base + noise
    x[5]  = 184.2
    x[13] = 178.4
    x[19] = 102.4
    mr     = np.abs(np.diff(x))
    mr_bar = mr.mean()
    x_bar  = x.mean()
    sigma  = mr_bar / 1.128
    ucl    = x_bar + 3 * sigma
    lcl    = max(0, x_bar - 3 * sigma)
    return x, x_bar, ucl, lcl

def util_pchart(n=24):
    p_bar = 0.584
    ni    = 6500000 // 12
    ucl   = p_bar + 3 * np.sqrt(p_bar * (1 - p_bar) / ni)
    lcl   = max(0, p_bar - 3 * np.sqrt(p_bar * (1 - p_bar) / ni))
    base  = np.random.normal(p_bar, 0.001, n)
    p     = np.clip(base, p_bar - 0.003, p_bar + 0.003)
    p[6]  = 0.614
    p[14] = 0.628
    return p, p_bar, ucl, lcl

def plot_charts():
    months = [f"M{i+1}" for i in range(24)]
    x_vals, x_bar, ucl_x, lcl_x = ehc_xmr()
    p_vals, p_bar, ucl_p, lcl_p = util_pchart()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4))
    fig.patch.set_facecolor("white")

    ax1.set_facecolor(LGREY)
    ax1.plot(range(24), x_vals, color=BLUE, marker="o", markersize=4, linewidth=1.6, zorder=3)
    ax1.axhline(x_bar, color=TEAL, linestyle="--", linewidth=1.2, label=f"X-bar=${x_bar:.1f}")
    ax1.axhline(ucl_x, color=RED,  linestyle=":",  linewidth=1.2, label=f"UCL=${ucl_x:.1f}")
    ax1.axhline(lcl_x, color=RED,  linestyle=":",  linewidth=1.2, label=f"LCL=${lcl_x:.1f}")

    ooc = [i for i in range(24) if x_vals[i] > ucl_x or x_vals[i] < lcl_x]
    for i in ooc:
        ax1.plot(i, x_vals[i], "o", color=ORANGE, markersize=9, zorder=4)

    ann = {5: "Deferred Care\nReturn", 13: "Psychology\nMax Expansion", 19: "Jan Deductible\nReset"}
    for i, lbl in ann.items():
        offset = 10 if x_vals[i] > x_bar else -28
        ax1.annotate(lbl, (i, x_vals[i]), textcoords="offset points",
                     xytext=(0, offset), fontsize=6.5, ha="center", color=ORANGE, fontweight="bold")

    ax1.set_xticks(range(24))
    ax1.set_xticklabels(months, fontsize=6.5, rotation=45)
    ax1.set_ylabel("EHC Claims (CAD PMPM)", fontsize=8)
    ax1.set_title("EHC Claims PMPM XmR\n(24 Months | X-bar=142.4 PMPM | Psychology +184% PMPM)", fontsize=9, fontweight="bold", color=BLUE)
    ax1.legend(fontsize=7)
    ax1.grid(axis="y", alpha=0.4)
    ax1.tick_params(axis="y", labelsize=8)

    ax2.set_facecolor(LGREY)
    ax2.plot(range(24), p_vals * 100, color=BLUE, marker="o", markersize=4, linewidth=1.6, zorder=3)
    ax2.axhline(p_bar * 100, color=TEAL, linestyle="--", linewidth=1.2, label=f"p-bar={p_bar*100:.1f}%")
    ax2.axhline(ucl_p * 100, color=RED,  linestyle=":",  linewidth=1.2, label=f"UCL={ucl_p*100:.1f}%")
    ax2.axhline(lcl_p * 100, color=RED,  linestyle=":",  linewidth=1.2, label=f"LCL={lcl_p*100:.1f}%")

    ooc_p = [i for i in range(24) if p_vals[i] > ucl_p or p_vals[i] < lcl_p]
    for i in ooc_p:
        ax2.plot(i, p_vals[i] * 100, "o", color=ORANGE, markersize=9, zorder=4)

    ann_p = {6: "Post-COVID\nReturn", 14: "Psychology\nExpansion"}
    for i, lbl in ann_p.items():
        ax2.annotate(lbl, (i, p_vals[i] * 100), textcoords="offset points",
                     xytext=(0, 8), fontsize=6.5, ha="center", color=ORANGE, fontweight="bold")

    para = ["Physio\n$42.4", "Massage\n$28.4", "Psych\n$24.4", "Chiro\n$18.4"]
    p_pm = [42.4, 28.4, 24.4, 18.4]
    p_co = [TEAL, BLUE, ORANGE, RED]
    for j, (lbl, val, col) in enumerate(zip(para, p_pm, p_co)):
        ax2.bar(17.0 + j * 1.7, val * 0.085, 1.3, bottom=55.5,
                color=col, alpha=0.82, zorder=3)
        ax2.text(17.0 + j * 1.7, 55.5 + val * 0.085 + 0.08, f"${val:.0f}",
                 ha="center", fontsize=6, fontweight="bold")
        ax2.text(17.0 + j * 1.7, 55.0, lbl.split("\n")[0], ha="center", fontsize=5.5, color=col)

    ax2.set_xticks(range(24))
    ax2.set_xticklabels(months, fontsize=6.5, rotation=45)
    ax2.set_ylabel("Annual Paramedical Utilization Rate (%)", fontsize=8)
    ax2.set_ylim(54, 66)
    ax2.set_title("Paramedical Utilization p-Chart\n(p-bar=58.4% | 2K Psych Plans 72.4% vs 500 Plans 44.4%)", fontsize=9, fontweight="bold", color=BLUE)
    ax2.legend(fontsize=7, loc="upper left")
    ax2.grid(axis="y", alpha=0.4)
    ax2.tick_params(axis="y", labelsize=8)

    fig.text(0.5, 0.01, "Nicholas Steven - github.com/nicholasstevenr",
             ha="center", fontsize=7, color="#888888", style="italic")
    plt.tight_layout(rect=[0, 0.04, 1, 1])
    out = "/sessions/focused-epic-turing/mnt/job application/Applications/Manulife/chart_p1.png"
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {out}")

if __name__ == "__main__":
    plot_charts()
