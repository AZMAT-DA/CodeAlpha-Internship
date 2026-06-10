# ============================================================
# CodeAlpha Internship - Task 2: Exploratory Data Analysis
# Dataset: books_dataset.csv (scraped in Task 1)
# ============================================================

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

print("=" * 55)
print("   CodeAlpha Internship - Task 2: EDA")
print("=" * 55)

# ── 1. LOAD DATASET ──────────────────────────────────────────
df = pd.read_csv("books_dataset.csv")
print("\n✅ Dataset Loaded Successfully!")

# ── 2. BASIC STRUCTURE ───────────────────────────────────────
print("\n📋 DATASET STRUCTURE:")
print(f"   Rows    : {df.shape[0]}")
print(f"   Columns : {df.shape[1]}")
print(f"\n   Column Names: {list(df.columns)}")
print(f"\n   Data Types:\n{df.dtypes}")

# ── 3. MISSING VALUES ────────────────────────────────────────
print("\n🔍 MISSING VALUES:")
print(df.isnull().sum())

# ── 4. DUPLICATES ────────────────────────────────────────────
print(f"\n🔁 Duplicate Rows: {df.duplicated().sum()}")

# ── 5. STATISTICAL SUMMARY ───────────────────────────────────
print("\n📊 STATISTICAL SUMMARY:")
print(df.describe())

# ── 6. MEANINGFUL QUESTIONS ──────────────────────────────────
print("\n❓ MEANINGFUL QUESTIONS ANSWERED:")

print(f"\n   Q1: What is the average book price?")
print(f"   → £{df['Price (£)'].mean():.2f}")

print(f"\n   Q2: How many books are 5-star rated?")
print(f"   → {len(df[df['Star Rating'] == 5])} books")

print(f"\n   Q3: What is the most common star rating?")
print(f"   → {df['Star Rating'].mode()[0]} stars")

print(f"\n   Q4: Are there any out-of-stock books?")
out_of_stock = df[df['Availability'] != 'In stock']
print(f"   → {len(out_of_stock)} books out of stock")

print(f"\n   Q5: What is the price range?")
print(f"   → Min: £{df['Price (£)'].min():.2f}  |  Max: £{df['Price (£)'].max():.2f}")

print(f"\n   Q6: Which rating has the highest average price?")
avg_price_by_rating = df.groupby("Star Rating")["Price (£)"].mean()
best = avg_price_by_rating.idxmax()
print(f"   → {best}-Star books avg £{avg_price_by_rating[best]:.2f}")

# ── 7. TRENDS & PATTERNS ─────────────────────────────────────
print("\n📈 TRENDS & PATTERNS:")
print("\n   Average Price by Star Rating:")
print(avg_price_by_rating.to_string())
print("\n   Book Count by Star Rating:")
print(df['Star Rating'].value_counts().sort_index().to_string())

# ── 8. VISUALIZATIONS (FIXED) ────────────────────────────────
sns.set_theme(style="darkgrid")

fig = plt.figure(figsize=(18, 12))
fig.suptitle("CodeAlpha Internship - Task 2: EDA on Books Dataset",
             fontsize=16, fontweight="bold", y=0.98)

gs = gridspec.GridSpec(2, 2, figure=fig,
                       hspace=0.45,   # vertical space between rows
                       wspace=0.35)   # horizontal space between columns

# ── Plot 1: Price Distribution ────────────────────────────────
ax1 = fig.add_subplot(gs[0, 0])
ax1.hist(df["Price (£)"], bins=20, color="#4C72B0", edgecolor="white")
ax1.set_title("Price Distribution of Books", fontsize=13, pad=12)
ax1.set_xlabel("Price (£)", fontsize=11)
ax1.set_ylabel("Number of Books", fontsize=11)

# ── Plot 2: Star Rating Count (FIXED - all 5 bars visible) ───
ax2 = fig.add_subplot(gs[0, 1])
rating_counts = df["Star Rating"].value_counts().sort_index()
bars = ax2.bar(rating_counts.index, rating_counts.values,
               color=["#d9534f", "#f0ad4e", "#5bc0de", "#5cb85c", "#337ab7"],
               edgecolor="white", width=0.6)
ax2.set_title("Number of Books per Star Rating", fontsize=13, pad=12)
ax2.set_xlabel("Star Rating", fontsize=11)
ax2.set_ylabel("Count", fontsize=11)
ax2.set_xticks([1, 2, 3, 4, 5])
ax2.set_xlim(0.5, 5.5)   # ← FIX: ensures all 5 bars are fully visible
# Add value labels on top of each bar
for bar in bars:
    ax2.text(bar.get_x() + bar.get_width() / 2,
             bar.get_height() + 0.5,
             str(int(bar.get_height())),
             ha='center', va='bottom', fontsize=10, fontweight='bold')

# ── Plot 3: Avg Price by Star Rating ─────────────────────────
ax3 = fig.add_subplot(gs[1, 0])
avg_price = df.groupby("Star Rating")["Price (£)"].mean()
ax3.plot(avg_price.index, avg_price.values,
         marker="o", color="#2ecc71", linewidth=2.5, markersize=9)
ax3.fill_between(avg_price.index, avg_price.values, alpha=0.15, color="#2ecc71")
ax3.set_title("Average Price by Star Rating", fontsize=13, pad=12)
ax3.set_xlabel("Star Rating", fontsize=11)
ax3.set_ylabel("Average Price (£)", fontsize=11)
ax3.set_xticks([1, 2, 3, 4, 5])
ax3.set_xlim(0.5, 5.5)
# Add value labels on each point
for x, y in zip(avg_price.index, avg_price.values):
    ax3.annotate(f"£{y:.1f}", (x, y),
                 textcoords="offset points", xytext=(0, 10),
                 ha='center', fontsize=9)

# ── Plot 4: Boxplot Price by Rating (FIXED - all 5 visible) ──
ax4 = fig.add_subplot(gs[1, 1])
rating_groups = [df[df["Star Rating"] == i]["Price (£)"].values for i in range(1, 6)]
bp = ax4.boxplot(rating_groups,
                 labels=["1★", "2★", "3★", "4★", "5★"],
                 patch_artist=True,
                 boxprops=dict(facecolor="#AED6F1", color="#2980B9"),
                 medianprops=dict(color="red", linewidth=2),
                 whiskerprops=dict(color="#2980B9"),
                 capprops=dict(color="#2980B9"))
ax4.set_title("Price Spread by Star Rating", fontsize=13, pad=12)
ax4.set_xlabel("Star Rating", fontsize=11)
ax4.set_ylabel("Price (£)", fontsize=11)

plt.savefig("task2_eda_charts.png", dpi=150, bbox_inches="tight")
plt.show()

print("\n✅ EDA Complete!")
print("📊 Charts saved as: task2_eda_charts.png")
print("=" * 55)