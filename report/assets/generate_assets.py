#!/usr/bin/env python3
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from pathlib import Path
OUT = Path(__file__).parent
plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.size"] = 11
BLUE = "#1a3a6b"
LIGHT_BLUE = "#eef3ff"
GREEN = "#2a6b2a"
LIGHT_GREEN = "#eef7ee"
ORANGE = "#8a5a2a"
LIGHT_ORANGE = "#fff7e8"
GRAY = "#6b7a90"
def save(fig, name):
    path = OUT / name
    fig.tight_layout()
    fig.savefig(path, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved {path}")
def gen_dataset():
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.5))
    axes[0].pie([354, 354], labels=["Fail 354", "Pass 354"], autopct="%1.0f%%", colors=["#ff9999", "#8aa4cc"], startangle=90, wedgeprops=dict(edgecolor="white"), textprops=dict(fontsize=9))
    axes[0].set_title("Class Balance (50/50)", fontsize=10, weight="bold", color=BLUE)
    axes[1].bar(["Numerical", "Categorical"], [3, 4], color=["#8aa4cc", "#ffcc99"], edgecolor="white", width=0.5)
    for i, v in enumerate([3,4]):
        axes[1].text(i, v+0.1, str(v), ha="center", fontsize=10, weight="bold")
    axes[1].set_ylim(0,5)
    axes[1].set_title("Feature Types (7 total)", fontsize=10, weight="bold", color=BLUE)
    axes[1].grid(axis="y", linestyle="--", alpha=0.4)
    fig.tight_layout()
    save(fig, "dataset_overview.png")
def gen_acc():
    labels = ["Baseline\nGini", "Gini\ndepth=4", "Entropy\ndepth=4"]
    test_acc = [67.80, 76.84, 75.14]
    train_acc = [100.0, 85.50, 84.18]
    x = np.arange(len(labels))
    width = 0.36
    fig, ax = plt.subplots(figsize=(8, 4.2))
    ax.bar(x - width/2, train_acc, width, label="Train", color="#8aa4cc", edgecolor="#2a5db0")
    ax.bar(x + width/2, test_acc, width, label="Test", color=["#ff8a8a", "#4a9a4a", "#e8a04a"], edgecolor="white")
    for i in range(len(labels)):
        ax.text(x[i]-width/2, train_acc[i]+1, f"{train_acc[i]:.1f}%", ha="center", fontsize=8, weight="bold")
        ax.text(x[i]+width/2, test_acc[i]+1, f"{test_acc[i]:.1f}%", ha="center", fontsize=8, weight="bold", color="#1a3a6b")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=9)
    ax.set_ylim(0, 110)
    ax.set_ylabel("Accuracy (%)", fontsize=10)
    ax.set_title("Accuracy: Training vs Testing", fontsize=11, weight="bold", color=BLUE, pad=10)
    ax.legend(frameon=True, facecolor="white", edgecolor="#d0dbe8")
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    save(fig, "comparison_accuracy.png")
def gen_nodes():
    labels = ["Baseline", "Gini d=4", "Entropy d=4"]
    nodes = [171, 35, 29]
    leaves = [93, 19, 17]
    x = np.arange(len(labels))
    width = 0.36
    fig, ax = plt.subplots(figsize=(7, 3.8))
    ax.bar(x - width/2, nodes, width, label="Nodes", color="#2a5db0", edgecolor="white")
    ax.bar(x + width/2, leaves, width, label="Leaves", color="#8aa4cc", edgecolor="white")
    for i in range(len(labels)):
        ax.text(x[i]-width/2, nodes[i]+3, str(nodes[i]), ha="center", fontsize=8, weight="bold")
        ax.text(x[i]+width/2, leaves[i]+3, str(leaves[i]), ha="center", fontsize=8, weight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=9)
    ax.set_ylabel("Count", fontsize=10)
    ax.set_title("Model Complexity: Nodes and Leaves", fontsize=11, weight="bold", color=BLUE, pad=10)
    ax.legend()
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    save(fig, "comparison_nodes.png")
def gen_confusion():
    cms = {"Baseline (67.80%)": np.array([[79, 9],[48, 41]]),"Gini d=4 (76.84%)": np.array([[74, 14],[27, 62]]),"Entropy d=4 (75.14%)": np.array([[64, 24],[20, 69]])}
    fig, axes = plt.subplots(1, 3, figsize=(9, 3.2), sharey=True)
    for ax, (title, cm) in zip(axes, cms.items()):
        im = ax.imshow(cm, cmap="Blues", vmin=0, vmax=80)
        ax.set_title(title, fontsize=8, weight="bold", color=BLUE)
        ax.set_xticks([0,1])
        ax.set_xticklabels(["Fail", "Pass"], fontsize=8)
        ax.set_yticks([0,1])
        ax.set_yticklabels(["Fail", "Pass"], fontsize=8)
        ax.set_xlabel("Predicted", fontsize=7)
        if ax == axes[0]:
            ax.set_ylabel("Actual", fontsize=7)
        for i in range(2):
            for j in range(2):
                ax.text(j, i, str(cm[i, j]), ha="center", va="center", fontsize=9, weight="bold", color="white" if cm[i,j] > 40 else "black")
    fig.suptitle("Confusion Matrices on Test Set (Fail 88, Pass 89)", fontsize=10, weight="bold", color=BLUE, y=1.02)
    fig.tight_layout()
    save(fig, "confusion_test.png")
    fig, ax = plt.subplots(figsize=(6, 3.5))
    gaps = [32.20, 8.66, 9.04]
    labels = ["Baseline", "Gini d=4", "Entropy d=4"]
    colors = ["#c0392b", "#4a9a4a", "#e67e22"]
    ax.barh(labels, gaps, color=colors, edgecolor="white", height=0.5)
    for i, v in enumerate(gaps):
        ax.text(v+0.5, i, f"{v:.2f} pp", va="center", fontsize=9, weight="bold")
    ax.set_xlabel("Generalization Gap (Train - Test, pp)", fontsize=9)
    ax.set_title("Generalization Gap Shrinks After Pruning", fontsize=11, weight="bold", color=BLUE, pad=10)
    ax.grid(axis="x", linestyle="--", alpha=0.4)
    save(fig, "gap.png")
if __name__ == "__main__":
    gen_dataset()
    gen_acc()
    gen_nodes()
    gen_confusion()
    print("All assets generated")
