"""
IPL Analysis — analysis.py
===========================
Run this script to reproduce all findings and charts.

Requirements:
    pip install pandas matplotlib seaborn
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

# ── Theme ─────────────────────────────────────────────────────────
sns.set_theme(style="darkgrid")
BG      = "#0D0D0D"
ORANGE  = "#FF6B00"
YELLOW  = "#FFD700"
TEXT    = "#F0F0F0"
MUTED   = "#888888"
CARD    = "#1A1A1A"

def style_ax(ax, title):
    ax.set_facecolor(BG)
    ax.set_title(title, color=TEXT, fontsize=13, fontweight="bold", pad=12)
    ax.tick_params(colors=TEXT)
    ax.xaxis.label.set_color(TEXT)
    ax.yaxis.label.set_color(TEXT)
    for spine in ax.spines.values():
        spine.set_edgecolor("#333")

# ── 1. Load Data ───────────────────────────────────────────────────
print("📂  Loading datasets …")
matches     = pd.read_csv("data/matches.csv")
deliveries  = pd.read_csv("data/deliveries.csv")

print(f"   Matches : {len(matches):,} rows")
print(f"   Deliveries: {len(deliveries):,} rows")

# ── 2. Clean ──────────────────────────────────────────────────────
print("🧹  Cleaning …")
matches.dropna(subset=["winner"], inplace=True)
matches["season"] = matches["season"].astype(int)

# ── 3. Chart 1 — Matches per Season ───────────────────────────────
print("📊  Chart 1: Matches per season …")
matches_per_season = matches.groupby("season").size().reset_index(name="matches")

fig, ax = plt.subplots(figsize=(12, 5), facecolor=BG)
bars = ax.bar(matches_per_season["season"], matches_per_season["matches"],
              color=ORANGE, edgecolor="none", width=0.6)
for bar in bars:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
            str(int(bar.get_height())), ha="center", va="bottom",
            color=TEXT, fontsize=8)
style_ax(ax, "IPL Matches Played per Season")
ax.set_xlabel("Season")
ax.set_ylabel("Number of Matches")
plt.tight_layout()
plt.savefig("outputs/01_matches_per_season.png", dpi=150,
            bbox_inches="tight", facecolor=BG)
print("   ✅  Saved outputs/01_matches_per_season.png")
plt.close()

# ── 4. Chart 2 — Top 10 Run Scorers ───────────────────────────────
print("📊  Chart 2: Top 10 run scorers …")
top_batsmen = (
    deliveries.groupby("batsman")["batsman_runs"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)
top_batsmen.columns = ["batsman", "runs"]

fig, ax = plt.subplots(figsize=(11, 6), facecolor=BG)
colors = [YELLOW if i == 0 else ORANGE for i in range(len(top_batsmen))]
bars = ax.barh(top_batsmen["batsman"][::-1], top_batsmen["runs"][::-1],
               color=colors[::-1], edgecolor="none")
for bar in bars:
    ax.text(bar.get_width() + 50, bar.get_y() + bar.get_height()/2,
            f"{int(bar.get_width()):,}", va="center", color=TEXT, fontsize=9)
style_ax(ax, "Top 10 Run Scorers — All Time IPL")
ax.set_xlabel("Total Runs")
plt.tight_layout()
plt.savefig("outputs/02_top_batsmen.png", dpi=150,
            bbox_inches="tight", facecolor=BG)
print("   ✅  Saved outputs/02_top_batsmen.png")
plt.close()

# ── 5. Chart 3 — Top 10 Wicket Takers ────────────────────────────
print("📊  Chart 3: Top 10 wicket takers …")
dismissals = ["caught", "bowled", "lbw", "stumped",
              "caught and bowled", "hit wicket"]
wickets = (
    deliveries[deliveries["dismissal_kind"].isin(dismissals)]
    .groupby("bowler")["dismissal_kind"]
    .count()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)
wickets.columns = ["bowler", "wickets"]

fig, ax = plt.subplots(figsize=(11, 6), facecolor=BG)
colors = [YELLOW if i == 0 else ORANGE for i in range(len(wickets))]
bars = ax.barh(wickets["bowler"][::-1], wickets["wickets"][::-1],
               color=colors[::-1], edgecolor="none")
for bar in bars:
    ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
            str(int(bar.get_width())), va="center", color=TEXT, fontsize=9)
style_ax(ax, "Top 10 Wicket Takers — All Time IPL")
ax.set_xlabel("Total Wickets")
plt.tight_layout()
plt.savefig("outputs/03_top_bowlers.png", dpi=150,
            bbox_inches="tight", facecolor=BG)
print("   ✅  Saved outputs/03_top_bowlers.png")
plt.close()

# ── 6. Chart 4 — Most Successful Teams ───────────────────────────
print("📊  Chart 4: Team wins …")
team_wins = (
    matches["winner"]
    .value_counts()
    .head(10)
    .reset_index()
)
team_wins.columns = ["team", "wins"]

# shorten long team names
team_wins["team"] = team_wins["team"].str.replace(
    "Royal Challengers Bangalore", "RCB").str.replace(
    "Kolkata Knight Riders", "KKR").str.replace(
    "Chennai Super Kings", "CSK").str.replace(
    "Mumbai Indians", "MI").str.replace(
    "Sunrisers Hyderabad", "SRH").str.replace(
    "Delhi Capitals", "DC").str.replace(
    "Delhi Daredevils", "DD").str.replace(
    "Kings XI Punjab", "KXIP").str.replace(
    "Rajasthan Royals", "RR").str.replace(
    "Deccan Chargers", "DC2")

fig, ax = plt.subplots(figsize=(12, 5), facecolor=BG)
bar_colors = [YELLOW if i == 0 else ORANGE for i in range(len(team_wins))]
bars = ax.bar(team_wins["team"], team_wins["wins"],
              color=bar_colors, edgecolor="none", width=0.6)
for bar in bars:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
            str(int(bar.get_height())), ha="center", color=TEXT, fontsize=9)
style_ax(ax, "Most Successful Teams — Total IPL Wins")
ax.set_ylabel("Number of Wins")
plt.tight_layout()
plt.savefig("outputs/04_team_wins.png", dpi=150,
            bbox_inches="tight", facecolor=BG)
print("   ✅  Saved outputs/04_team_wins.png")
plt.close()

# ── 7. Chart 5 — Toss Analysis ────────────────────────────────────
print("📊  Chart 5: Toss analysis …")
toss = matches["toss_decision"].value_counts()

fig, ax = plt.subplots(figsize=(7, 7), facecolor=BG)
wedges, texts, autotexts = ax.pie(
    toss, labels=toss.index, autopct="%1.1f%%",
    colors=[ORANGE, YELLOW],
    textprops={"color": TEXT},
    startangle=140,
    wedgeprops={"edgecolor": BG, "linewidth": 3}
)
for at in autotexts:
    at.set_fontsize(12)
    at.set_fontweight("bold")
ax.set_facecolor(BG)
ax.set_title("Toss Decision — Bat vs Field", color=TEXT,
             fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig("outputs/05_toss_analysis.png", dpi=150,
            bbox_inches="tight", facecolor=BG)
print("   ✅  Saved outputs/05_toss_analysis.png")
plt.close()

# ── 8. Chart 6 — Top Venues ───────────────────────────────────────
print("📊  Chart 6: Top venues …")
top_venues = (
    matches["venue"]
    .value_counts()
    .head(10)
    .reset_index()
)
top_venues.columns = ["venue", "matches"]
top_venues["venue"] = top_venues["venue"].str.split(",").str[0]

fig, ax = plt.subplots(figsize=(12, 6), facecolor=BG)
bars = ax.barh(top_venues["venue"][::-1], top_venues["matches"][::-1],
               color=ORANGE, edgecolor="none")
for bar in bars:
    ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
            str(int(bar.get_width())), va="center", color=TEXT, fontsize=9)
style_ax(ax, "Top 10 IPL Venues by Matches Hosted")
ax.set_xlabel("Number of Matches")
plt.tight_layout()
plt.savefig("outputs/06_venue_analysis.png", dpi=150,
            bbox_inches="tight", facecolor=BG)
print("   ✅  Saved outputs/06_venue_analysis.png")
plt.close()

# ── 9. Key Insights ───────────────────────────────────────────────
print("\n" + "="*52)
print("  KEY INSIGHTS")
print("="*52)
print(f"  Total seasons analyzed : {matches['season'].nunique()}")
print(f"  Total matches          : {len(matches):,}")
print(f"  Total deliveries       : {len(deliveries):,}")
print(f"  Most successful team   : {matches['winner'].value_counts().idxmax()}")
print(f"  Top run scorer         : {top_batsmen.iloc[0]['batsman']} ({top_batsmen.iloc[0]['runs']:,} runs)")
print(f"  Top wicket taker       : {wickets.iloc[0]['bowler']} ({wickets.iloc[0]['wickets']} wickets)")
print(f"  Toss preference        : {toss.idxmax()} ({toss.max()} times)")
print("="*52)
print("\n🎉  All 6 charts saved to outputs/")
