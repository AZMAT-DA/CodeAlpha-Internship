# ============================================================
# CodeAlpha Internship - Task 3: Data Visualization
# Dataset: books_dataset.csv (scraped in Task 1)
# ============================================================

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import numpy as np
import warnings
warnings.filterwarnings("ignore")

# Fix font to support all characters
plt.rcParams['font.family'] = 'DejaVu Sans'

print("=" * 55)
print("   CodeAlpha Internship - Task 3: Data Visualization")
print("=" * 55)

# ── LOAD DATASET ─────────────────────────────────────────────
df = pd.read_csv("books_dataset.csv")
print(f"\n✅ Dataset Loaded: {len(df)} books")

# ── ADD PRICE CATEGORY COLUMN ────────────────────────────────
def price_category(price):
    if price < 20:
        return "Budget (< 20)"
    elif price < 40:
        return "Mid-Range (20-40)"
    else:
        return "Premium (> 40)"

df["Price Category"] = df["Price (£)"].apply(price_category)

# ── STAR LABEL COLUMN ────────────────────────────────────────
df["Rating Label"] = df["Star Rating"].map({
    1: "1 Poor", 2: "2 Fair", 3: "3 Good",
    4: "4 Great", 5: "5 Excellent"
})

sns.set_theme(style="darkgrid")
COLORS = ["#E74C3C", "#E67E22", "#3498DB", "#2ECC71", "#9B59B6"]
STAR_LABELS = ["1 Poor", "2 Fair", "3 Good", "4 Great", "5 Excellent"]

# ════════════════════════════════════════════════════════════
# FIGURE 1 — Main Dashboard (2x3 grid)
# ════════════════════════════════════════════════════════════
fig1, axes = plt.subplots(2, 3, figsize=(20, 12))
fig1.suptitle("Books Dataset — Data Visualization Dashboard\nCodeAlpha Internship Task 3",
              fontsize=16, fontweight="bold", y=1.01)

# ── Chart 1: Pie Chart — Price Category Distribution ─────────
ax = axes[0, 0]
cat_counts = df["Price Category"].value_counts()
cat_colors = ["#3498DB", "#2ECC71", "#E74C3C"]
wedges, texts, autotexts = ax.pie(
    cat_counts.values,
    labels=cat_counts.index,
    autopct="%1.1f%%",
    colors=cat_colors,
    startangle=140,
    wedgeprops=dict(edgecolor="white", linewidth=2)
)
for text in autotexts:
    text.set_fontsize(10)
    text.set_fontweight("bold")
ax.set_title("Price Category Distribution", fontsize=13, fontweight="bold", pad=15)

# ── Chart 2: Horizontal Bar — Books per Rating ────────────────
ax = axes[0, 1]
rating_counts = df["Star Rating"].value_counts().sort_index()
bars = ax.barh(STAR_LABELS, rating_counts.values,
               color=COLORS, edgecolor="white", height=0.6)
ax.set_title("Book Count by Star Rating", fontsize=13, fontweight="bold", pad=12)
ax.set_xlabel("Number of Books", fontsize=11)
for bar in bars:
    ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height() / 2,
            str(int(bar.get_width())), va='center', fontsize=10, fontweight='bold')
ax.set_xlim(0, max(rating_counts.values) + 8)

# ── Chart 3: KDE — Price Density by Star Rating ───────────────
ax = axes[0, 2]
for star, color, label in zip(range(1, 6), COLORS, STAR_LABELS):
    subset = df[df["Star Rating"] == star]["Price (£)"]
    subset.plot.kde(ax=ax, color=color, linewidth=2.5,
                    label=f"{label} ({len(subset)})")
ax.set_title("Price Density by Star Rating", fontsize=13, fontweight="bold", pad=12)
ax.set_xlabel("Price (£)", fontsize=11)
ax.set_ylabel("Density", fontsize=11)
ax.legend(fontsize=9)
ax.set_xlim(0, 70)

# ── Chart 4: Grouped Bar — Price Category vs Star Rating ──────
ax = axes[1, 0]
cross = pd.crosstab(df["Star Rating"], df["Price Category"])
cross.plot(kind="bar", ax=ax,
           color=["#3498DB", "#2ECC71", "#E74C3C"],
           edgecolor="white", width=0.7)
ax.set_title("Price Category per Star Rating", fontsize=13, fontweight="bold", pad=12)
ax.set_xlabel("Star Rating", fontsize=11)
ax.set_ylabel("Number of Books", fontsize=11)
ax.set_xticklabels(["1", "2", "3", "4", "5"], rotation=0)
ax.legend(title="Price Category", fontsize=8, title_fontsize=9)

# ── Chart 5: Violin Plot — Price by Rating ───────────────────
ax = axes[1, 1]
violin_data = [df[df["Star Rating"] == i]["Price (£)"].values for i in range(1, 6)]
parts = ax.violinplot(violin_data, positions=[1, 2, 3, 4, 5],
                      showmedians=True, showmeans=False)
for i, pc in enumerate(parts['bodies']):
    pc.set_facecolor(COLORS[i])
    pc.set_alpha(0.7)
parts['cmedians'].set_color('white')
parts['cmedians'].set_linewidth(2)
ax.set_title("Price Distribution (Violin) by Rating", fontsize=13, fontweight="bold", pad=12)
ax.set_xlabel("Star Rating", fontsize=11)
ax.set_ylabel("Price (£)", fontsize=11)
ax.set_xticks([1, 2, 3, 4, 5])
ax.set_xticklabels(["1", "2", "3", "4", "5"])

# ── Chart 6: Line — Cumulative Books by Price ─────────────────
ax = axes[1, 2]
sorted_prices = df["Price (£)"].sort_values().reset_index(drop=True)
ax.plot(sorted_prices.values, range(1, len(sorted_prices) + 1),
        color="#9B59B6", linewidth=2.5)
ax.fill_betweenx(range(1, len(sorted_prices) + 1),
                 sorted_prices.values, alpha=0.15, color="#9B59B6")
ax.set_title("Cumulative Books by Price", fontsize=13, fontweight="bold", pad=12)
ax.set_xlabel("Price (£)", fontsize=11)
ax.set_ylabel("Cumulative Books", fontsize=11)
ax.axvline(x=df["Price (£)"].mean(), color="red",
           linestyle="--", linewidth=1.5,
           label=f"Mean £{df['Price (£)'].mean():.2f}")
ax.legend(fontsize=10)

plt.tight_layout()
fig1.savefig("task3_dashboard.png", dpi=150, bbox_inches="tight")
print("✅ Dashboard saved: task3_dashboard.png")

# ════════════════════════════════════════════════════════════
# FIGURE 2 — Heatmap & Scatter
# ════════════════════════════════════════════════════════════
fig2, axes2 = plt.subplots(1, 2, figsize=(16, 6))
fig2.suptitle("Books Dataset — Deep Insights\nCodeAlpha Internship Task 3",
              fontsize=15, fontweight="bold")

# ── Chart 7: Heatmap ─────────────────────────────────────────
ax = axes2[0]
heatmap_data = df.groupby(["Star Rating", "Price Category"])["Price (£)"].mean().unstack()
sns.heatmap(heatmap_data, ax=ax, annot=True, fmt=".1f",
            cmap="YlOrRd", linewidths=0.5,
            cbar_kws={"label": "Avg Price (£)"})
ax.set_title("Avg Price Heatmap\n(Star Rating vs Price Category)",
             fontsize=13, fontweight="bold", pad=12)
ax.set_xlabel("Price Category", fontsize=11)
ax.set_ylabel("Star Rating", fontsize=11)
ax.set_yticklabels(["1", "2", "3", "4", "5"], rotation=0)

# ── Chart 8: Scatter + Trend ──────────────────────────────────
ax = axes2[1]
for star, color, label in zip(range(1, 6), COLORS, STAR_LABELS):
    subset = df[df["Star Rating"] == star]
    ax.scatter(subset["Star Rating"], subset["Price (£)"],
               color=color, alpha=0.5, s=60, label=label)
z = np.polyfit(df["Star Rating"], df["Price (£)"], 1)
p = np.poly1d(z)
x_line = np.linspace(1, 5, 100)
ax.plot(x_line, p(x_line), color="black",
        linewidth=2, linestyle="--", label="Trend")
ax.set_title("Price vs Star Rating (Scatter + Trend)",
             fontsize=13, fontweight="bold", pad=12)
ax.set_xlabel("Star Rating", fontsize=11)
ax.set_ylabel("Price (£)", fontsize=11)
ax.set_xticks([1, 2, 3, 4, 5])
ax.legend(fontsize=9)

plt.tight_layout()
fig2.savefig("task3_insights.png", dpi=150, bbox_inches="tight")
print("✅ Insights chart saved: task3_insights.png")

plt.show()

print("\n Task 3 Complete!")
print("Files to upload to GitHub:")
print("   -> task3_visualization.py")
print("   -> task3_dashboard.png")
print("   -> task3_insights.png")
print("=" * 55)