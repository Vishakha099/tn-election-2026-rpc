# ============================================================
#  TAMIL NADU ELECTION 2021 vs 2026 — COMPLETE ANALYSIS CODE
#  For: Codebasics Resume Project Challenge



# These are tools that help us work with data and make charts
import pandas as pd           # for reading and working with tables (like Excel)
import matplotlib.pyplot as plt  # for making charts
import os
os.chdir('/content/')
import matplotlib.patches as mpatches  # for chart legends
import seaborn as sns         # for prettier charts
import warnings
warnings.filterwarnings('ignore')  # hide unimportant warning messages

# Make all charts look clean and big
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 12

print("✅ Libraries loaded successfully!")


# ============================================================
# SECTION 2 — LOAD DATA FILES
# ============================================================

# Read the 3 CSV files into DataFrames

df21 = pd.read_csv('/content/tn_2021_results.csv')    # 2021 election results
df26 = pd.read_csv('/content/tn_2026_results.csv')    # 2026 election results
master = pd.read_csv('/content/constituency_master.csv')  # list of all 234 seats

# Let's quickly look at what the data looks like
print("=== 2021 Data — First 3 rows ===")
print(df21.head(3))
print(f"\nTotal rows: {len(df21)} | Total columns: {len(df21.columns)}")
print(f"Columns: {df21.columns.tolist()}")

print("\n=== 2026 Data — First 3 rows ===")
print(df26.head(3))
print(f"\nTotal rows: {len(df26)}")


print("\n✅ Data loaded!")
print(f"Regions: {df21['region'].unique()}")
print(f"Reservation types: {df21['reserved'].unique()}")


# ============================================================
# SECTION 3 — FIND THE WINNER IN EACH CONSTITUENCY
# ============================================================
# Each constituency has many rows (one per candidate).
# We need to find the ONE winner (highest votes) per seat.

# Sort by ac_number and votes (descending), then keep only rank #1
winners_21 = (
    df21.sort_values(['ac_number', 'votes'], ascending=[True, False])
        .groupby('ac_number')          # group by constituency
        .first()                        # take the top row (highest votes) = winner
        .reset_index()
)

winners_26 = (
    df26.sort_values(['ac_number', 'votes'], ascending=[True, False])
        .groupby('ac_number')
        .first()
        .reset_index()
)

print(f"2021: {len(winners_21)} winners found")
print(f"2026: {len(winners_26)} winners found")
print("\n2021 Sample winners:")
print(winners_21[['constituency', 'candidate', 'party', 'votes']].head(5))

print("\n2026 Sample winners:")
print(winners_26[['constituency', 'candidate', 'party', 'votes']].head(5))

print("\n✅ Winners identified!")


# ============================================================
# SECTION 4 — STORY 1: HOW MANY SEATS DID EACH PARTY WIN?
# ============================================================
# Simple count: how many seats did each party win in each year?

seats_21 = winners_21['party'].value_counts().reset_index()
seats_21.columns = ['party', 'seats_2021']

seats_26 = winners_26['party'].value_counts().reset_index()
seats_26.columns = ['party', 'seats_2026']

# Show top 10 parties
print("=== 2021 Top Parties by Seats Won ===")
print(seats_21.head(10))

print("\n=== 2026 Top Parties by Seats Won ===")
print(seats_26.head(10))

# --- CHART: Top parties comparison ---
# Focus on top 6 parties only (others are small independents)
top_parties = ['DMK', 'AIADMK', 'TVK', 'PMK', 'BJP', 'INC']

# Get seats for each party (use 0 if they didn't win any)
seats_data = []
for party in top_parties:
    s21 = seats_21[seats_21['party'] == party]['seats_2021'].values
    s26 = seats_26[seats_26['party'] == party]['seats_2026'].values
    seats_data.append({
        'party': party,
        '2021': int(s21[0]) if len(s21) > 0 else 0,
        '2026': int(s26[0]) if len(s26) > 0 else 0
    })

seats_compare = pd.DataFrame(seats_data)
print("\n=== Party Seat Comparison ===")
print(seats_compare)

# Draw a grouped bar chart
x = range(len(top_parties))
width = 0.35

fig, ax = plt.subplots(figsize=(12, 6))
bars1 = ax.bar([i - width/2 for i in x], seats_compare['2021'], width, label='2021', color='#2196F3')
bars2 = ax.bar([i + width/2 for i in x], seats_compare['2026'], width, label='2026', color='#FF5722')

# Add numbers on top of each bar
for bar in bars1:
    if bar.get_height() > 0:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                str(int(bar.get_height())), ha='center', va='bottom', fontweight='bold')
for bar in bars2:
    if bar.get_height() > 0:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                str(int(bar.get_height())), ha='center', va='bottom', fontweight='bold')

ax.set_xticks(list(x))
ax.set_xticklabels(top_parties, fontsize=13)
ax.set_ylabel('Number of Seats Won')
ax.set_title('Seats Won by Party: 2021 vs 2026', fontsize=15, fontweight='bold')
ax.legend(fontsize=12)
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('chart1_party_seats.png', dpi=150, bbox_inches='tight')
plt.show()
print("✅ Chart 1 saved as 'chart1_party_seats.png'")


# ============================================================
# SECTION 5 — STORY 2: WHICH CONSTITUENCIES FLIPPED PARTY?
# ============================================================
# A "flip" = the winning party changed between 2021 and 2026

# Merge the two winner tables side by side using ac_number as the key
# (like a VLOOKUP in Excel)
comparison = pd.merge(
    winners_21[['ac_number', 'constituency', 'party', 'votes', 'region', 'reserved']],
    winners_26[['ac_number', 'party', 'votes']],
    on='ac_number',
    suffixes=('_2021', '_2026')   # adds _2021 and _2026 to same-named columns
)

# A flip is where the party changed
comparison['flipped'] = comparison['party_2021'] != comparison['party_2026']

# Calculate winning margin for each year
# Total votes per constituency
total_21 = df21.groupby('ac_number')['votes'].sum().reset_index()
total_21.columns = ['ac_number', 'total_votes_2021']
total_26 = df26.groupby('ac_number')['votes'].sum().reset_index()
total_26.columns = ['ac_number', 'total_votes_2026']

comparison = pd.merge(comparison, total_21, on='ac_number')
comparison = pd.merge(comparison, total_26, on='ac_number')

# How many seats flipped?
flipped = comparison[comparison['flipped'] == True].copy()
stayed = comparison[comparison['flipped'] == False].copy()

print(f"Total constituencies: {len(comparison)}")
print(f"Seats that FLIPPED (changed party): {len(flipped)}")
print(f"Seats that STAYED with same party: {len(stayed)}")
print(f"\nFlip rate: {len(flipped)/len(comparison)*100:.1f}%")

print("\n=== Flipped Seats (sample) ===")
print(flipped[['constituency', 'region', 'party_2021', 'party_2026']].head(15).to_string(index=False))

# How many flips happened in each region?
flips_by_region = flipped.groupby('region').size().reset_index()
flips_by_region.columns = ['region', 'flips']
flips_by_region = flips_by_region.sort_values('flips', ascending=False)
print("\n=== Flips by Region ===")
print(flips_by_region)

# What were the most common flip directions?
flipped['flip_direction'] = flipped['party_2021'] + ' → ' + flipped['party_2026']
flip_directions = flipped['flip_direction'].value_counts().head(10)
print("\n=== Most Common Flip Directions ===")
print(flip_directions)

# --- CHART: Flips by Region ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Left chart: flips by region
colors = ['#E53935', '#FB8C00', '#FDD835', '#43A047', '#1E88E5', '#8E24AA']
ax1.barh(flips_by_region['region'], flips_by_region['flips'], color=colors[:len(flips_by_region)])
for i, (val, reg) in enumerate(zip(flips_by_region['flips'], flips_by_region['region'])):
    ax1.text(val + 0.2, i, str(val), va='center', fontweight='bold')
ax1.set_xlabel('Number of Flipped Seats')
ax1.set_title('Constituency Flips by Region', fontweight='bold')
ax1.grid(axis='x', alpha=0.3)

# Right chart: top flip directions
top_flips = flip_directions.head(6)
ax2.barh(top_flips.index, top_flips.values, color='#5C6BC0')
for i, val in enumerate(top_flips.values):
    ax2.text(val + 0.1, i, str(val), va='center', fontweight='bold')
ax2.set_xlabel('Number of Constituencies')
ax2.set_title('Most Common Party Switches', fontweight='bold')
ax2.grid(axis='x', alpha=0.3)

plt.suptitle('Which Constituencies Changed Winning Party? (2021 → 2026)',
             fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('chart2_flips.png', dpi=150, bbox_inches='tight')
plt.show()
print("✅ Chart 2 saved as 'chart2_flips.png'")


# ============================================================
# SECTION 6 — STORY 3: MARGINS OF VICTORY
# ============================================================
# Margin = Winner votes − Runner-up votes
# A big margin = dominant win. A small margin = very close race.

# Find runner-up (2nd place) in each constituency
runnerup_21 = (
    df21.sort_values(['ac_number', 'votes'], ascending=[True, False])
        .groupby('ac_number')
        .nth(1)      # nth(1) = second row = runner-up
        .reset_index()
)
runnerup_26 = (
    df26.sort_values(['ac_number', 'votes'], ascending=[True, False])
        .groupby('ac_number')
        .nth(1)
        .reset_index()
)

# Add runner-up votes to comparison table
comparison = pd.merge(
    comparison,
    runnerup_21[['ac_number', 'votes']].rename(columns={'votes': 'runnerup_votes_2021'}),
    on='ac_number'
)
comparison = pd.merge(
    comparison,
    runnerup_26[['ac_number', 'votes']].rename(columns={'votes': 'runnerup_votes_2026'}),
    on='ac_number'
)

# Calculate margins and vote share
comparison['margin_2021'] = comparison['votes_2021'] - comparison['runnerup_votes_2021']
comparison['margin_2026'] = comparison['votes_2026'] - comparison['runnerup_votes_2026']
comparison['voteshare_2021'] = (comparison['votes_2021'] / comparison['total_votes_2021'] * 100).round(1)
comparison['voteshare_2026'] = (comparison['votes_2026'] / comparison['total_votes_2026'] * 100).round(1)

# Summary statistics
print("=== Margin of Victory Summary ===")
print(f"Average margin 2021: {comparison['margin_2021'].mean():,.0f} votes")
print(f"Average margin 2026: {comparison['margin_2026'].mean():,.0f} votes")
print(f"\nAverage winner vote share 2021: {comparison['voteshare_2021'].mean():.1f}%")
print(f"Average winner vote share 2026: {comparison['voteshare_2026'].mean():.1f}%")

# Winners with >50% vote share (very dominant wins)
dominant_21 = (comparison['voteshare_2021'] > 50).sum()
dominant_26 = (comparison['voteshare_2026'] > 50).sum()
print(f"\nSeats won with >50% vote share — 2021: {dominant_21} | 2026: {dominant_26}")

# Very close races (<35% vote share)
close_21 = (comparison['voteshare_2021'] < 35).sum()
close_26 = (comparison['voteshare_2026'] < 35).sum()
print(f"Seats won with <35% vote share (close races) — 2021: {close_21} | 2026: {close_26}")

# Top 10 biggest winning margins in 2026
print("\n=== Top 10 Biggest Wins in 2026 ===")
top_margins = comparison.nlargest(10, 'margin_2026')[
    ['constituency', 'region', 'party_2026', 'votes_2026', 'margin_2026', 'voteshare_2026']
]
print(top_margins.to_string(index=False))

# Top 10 closest races in 2026
print("\n=== Top 10 Closest Races in 2026 ===")
close_races = comparison.nsmallest(10, 'margin_2026')[
    ['constituency', 'region', 'party_2026', 'votes_2026', 'margin_2026', 'voteshare_2026']
]
print(close_races.to_string(index=False))

# --- CHART: Vote Share Distribution ---
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Left: histogram of vote share 2021 vs 2026
axes[0].hist(comparison['voteshare_2021'], bins=20, alpha=0.6, label='2021', color='#2196F3')
axes[0].hist(comparison['voteshare_2026'], bins=20, alpha=0.6, label='2026', color='#FF5722')
axes[0].axvline(x=50, color='black', linestyle='--', linewidth=1.5, label='50% mark')
axes[0].axvline(x=35, color='gray', linestyle='--', linewidth=1.5, label='35% mark')
axes[0].set_xlabel('Winner Vote Share (%)')
axes[0].set_ylabel('Number of Constituencies')
axes[0].set_title('Distribution of Winner Vote Share', fontweight='bold')
axes[0].legend()
axes[0].grid(alpha=0.3)

# Right: bar chart — dominant vs close vs normal wins
categories = ['Dominant\n(>50%)', 'Normal\n(35-50%)', 'Close\n(<35%)']
vals_21 = [dominant_21, len(comparison)-dominant_21-close_21, close_21]
vals_26 = [dominant_26, len(comparison)-dominant_26-close_26, close_26]

x = range(3)
axes[1].bar([i - 0.2 for i in x], vals_21, 0.35, label='2021', color='#2196F3')
axes[1].bar([i + 0.2 for i in x], vals_26, 0.35, label='2026', color='#FF5722')
for i, (v21, v26) in enumerate(zip(vals_21, vals_26)):
    axes[1].text(i - 0.2, v21 + 0.5, str(v21), ha='center', fontweight='bold')
    axes[1].text(i + 0.2, v26 + 0.5, str(v26), ha='center', fontweight='bold')
axes[1].set_xticks(list(x))
axes[1].set_xticklabels(categories)
axes[1].set_ylabel('Number of Constituencies')
axes[1].set_title('Win Category Breakdown: 2021 vs 2026', fontweight='bold')
axes[1].legend()
axes[1].grid(axis='y', alpha=0.3)

plt.suptitle('How Dominant Were the Wins? (Margin of Victory Analysis)',
             fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('chart3_margins.png', dpi=150, bbox_inches='tight')
plt.show()
print("✅ Chart 3 saved as 'chart3_margins.png'")


# ============================================================
# SECTION 7 — STORY 1 PART 2: SEATS BY REGION
# ============================================================
# How did seat wins shift across the 6 geographic regions?

# Focus on main parties
main_parties = ['DMK', 'AIADMK', 'TVK', 'PMK', 'BJP']

region_21 = (
    winners_21[winners_21['party'].isin(main_parties)]
    .groupby(['region', 'party'])
    .size()
    .reset_index(name='seats')
)
region_21['year'] = '2021'

region_26 = (
    winners_26[winners_26['party'].isin(main_parties)]
    .groupby(['region', 'party'])
    .size()
    .reset_index(name='seats')
)
region_26['year'] = '2026'

region_all = pd.concat([region_21, region_26])

print("=== Seats by Region and Party ===")
print(region_all.pivot_table(index=['region', 'year'], columns='party', values='seats', fill_value=0))

# --- CHART: Regional breakdown ---
regions = ['Chennai Metro', 'North', 'Central', 'Kongu', 'South', 'Delta']
party_colors = {'DMK': '#E53935', 'AIADMK': '#1E88E5', 'TVK': '#43A047',
                'PMK': '#FB8C00', 'BJP': '#FF8F00'}

fig, axes = plt.subplots(2, 3, figsize=(16, 10))
axes = axes.flatten()

for idx, region in enumerate(regions):
    ax = axes[idx]
    r21 = region_21[region_21['region'] == region].set_index('party')['seats']
    r26 = region_26[region_26['region'] == region].set_index('party')['seats']

    all_parties_in_region = list(set(r21.index.tolist() + r26.index.tolist()))
    all_parties_in_region = [p for p in main_parties if p in all_parties_in_region]

    v21 = [r21.get(p, 0) for p in all_parties_in_region]
    v26 = [r26.get(p, 0) for p in all_parties_in_region]

    x = range(len(all_parties_in_region))
    ax.bar([i - 0.2 for i in x], v21, 0.35, label='2021', color='#2196F3', alpha=0.8)
    ax.bar([i + 0.2 for i in x], v26, 0.35, label='2026', color='#FF5722', alpha=0.8)
    ax.set_xticks(list(x))
    ax.set_xticklabels(all_parties_in_region, fontsize=10)
    ax.set_title(region, fontweight='bold', fontsize=12)
    ax.legend(fontsize=9)
    ax.grid(axis='y', alpha=0.3)
    ax.set_ylabel('Seats')

plt.suptitle('Seats Won Per Region by Party: 2021 vs 2026',
             fontsize=15, fontweight='bold')
plt.tight_layout()
plt.savefig('chart4_regions.png', dpi=150, bbox_inches='tight')
plt.show()
print("✅ Chart 4 saved as 'chart4_regions.png'")


# ============================================================
# SECTION 8 — SAVE FINAL SUMMARY TABLE
# ============================================================
# Save the full constituency-level comparison to Excel
# This is your supporting data file

output_cols = [
    'ac_number', 'constituency', 'region', 'reserved',
    'party_2021', 'votes_2021', 'voteshare_2021', 'margin_2021',
    'party_2026', 'votes_2026', 'voteshare_2026', 'margin_2026',
    'flipped'
]
final_table = comparison[output_cols].copy()
final_table['flipped'] = final_table['flipped'].map({True: 'YES', False: 'NO'})
final_table = final_table.sort_values('ac_number')

final_table.to_csv('constituency_summary.csv', index=False)
final_table.to_excel('constituency_summary.xlsx', index=False)

print("✅ Summary tables saved!")
print(f"   → constituency_summary.csv")
print(f"   → constituency_summary.xlsx")
print("\n=== Sample of Final Table ===")
print(final_table.head(10).to_string(index=False))


# ============================================================
# SECTION 9 — STORY HEADLINES
# ============================================================

print("""
╔══════════════════════════════════════════════════════════╗
║           KEY FINDINGS             ║
╚══════════════════════════════════════════════════════════╝

1. OVERALL RESULT:
   →  In 2026, TVK won 108 seats out of 234,
      compared to DMK seats in 2021.

2. THE FLIP STORY:
   →  163 out of 234 constituencies changed their
      winning party between 2021 and 2026.
   →  The south region saw the most flips with 38 seats.

3. THE MARGIN STORY:
   →  Winners with >50% vote share went from 68 in 2021
      to 13 in 2026 — suggesting more dominant wins.""")



print("🎉 All analysis complete! charts are saved as PNG files.")
