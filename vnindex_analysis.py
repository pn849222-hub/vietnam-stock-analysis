# Vietnam Stock Market Analysis - VN-Index
# Author: [BenDTA]

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from vnstock import Vnstock
import warnings
warnings.filterwarnings("ignore")

# ── Config ───────────────────────────────────────────────
OUTPUT_DIR = "outputs"
import os
os.makedirs(OUTPUT_DIR, exist_ok=True)

plt.style.use("seaborn-v0_8-whitegrid")

# ── 1. Load VN-Index data ─────────────────────────────────
print("Loading VN-Index data...")

stock = Vnstock().stock(symbol="VNINDEX", source="VCI")
df = stock.quote.history(start="2020-01-01", end="2024-12-31")

print("Shape:", df.shape)
print("\nColumns:", df.columns.tolist())
print("\nFirst 5 rows:")
print(df.head())
print("\nMissing values:")
print(df.isnull().sum())
# ── 2. DATA CLEANING ─────────────────────────────────────
df["time"] = pd.to_datetime(df["time"])
df = df.sort_values("time").reset_index(drop=True)
df["year"]          = df["time"].dt.year
df["month"]         = df["time"].dt.month
df["daily_return"]  = df["close"].pct_change() * 100

print("\n── After Cleaning ──")
print("Date range:", df["time"].min().date(), "→", df["time"].max().date())
print("Years:", sorted(df["year"].unique()))

# ── 3. VISUALIZATION ─────────────────────────────────────
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("VN-Index Analysis (2020–2024)", fontsize=16, fontweight="bold")

# Chart 1: Price trend
axes[0, 0].plot(df["time"], df["close"], color="#2196F3", linewidth=1)
axes[0, 0].set_title("VN-Index Price Trend")
axes[0, 0].set_xlabel("Date")
axes[0, 0].set_ylabel("Index Points")
axes[0, 0].tick_params(axis="x", rotation=45)

# Chart 2: Volume
axes[0, 1].bar(df["time"], df["volume"], color="#4CAF50", alpha=0.6, width=1)
axes[0, 1].set_title("Trading Volume")
axes[0, 1].set_xlabel("Date")
axes[0, 1].set_ylabel("Volume")
axes[0, 1].tick_params(axis="x", rotation=45)

# Chart 3: Yearly average
yearly_avg = df.groupby("year")["close"].mean()
axes[1, 0].bar(yearly_avg.index.astype(str), yearly_avg.values, color="#FF9800")
axes[1, 0].set_title("Yearly Average Index")
axes[1, 0].set_xlabel("Year")
axes[1, 0].set_ylabel("Avg Points")

# Chart 4: Daily returns distribution
axes[1, 1].hist(df["daily_return"].dropna(), bins=50, color="#9C27B0", alpha=0.7)
axes[1, 1].axvline(x=0, color="red", linestyle="--")
axes[1, 1].set_title("Daily Returns Distribution")
axes[1, 1].set_xlabel("Daily Return (%)")
axes[1, 1].set_ylabel("Frequency")

plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/vnindex_overview.png", dpi=150, bbox_inches="tight")
plt.show()
print("\nChart saved! ✓")

# ── 4. KEY INSIGHTS ───────────────────────────────────────
print("\n" + "="*50)
print("KEY INSIGHTS - VN-INDEX")
print("="*50)
print(f"\n[1] All-time high : {df['close'].max():.2f} points ({df.loc[df['close'].idxmax(), 'time'].date()})")
print(f"[2] All-time low  : {df['close'].min():.2f} points ({df.loc[df['close'].idxmin(), 'time'].date()})")
print(f"[3] Avg daily return: {df['daily_return'].mean():.3f}%")
print(f"[4] Most volatile year: {df.groupby('year')['daily_return'].std().idxmax()}")
print(f"[5] Avg daily volume: {df['volume'].mean():,.0f}")