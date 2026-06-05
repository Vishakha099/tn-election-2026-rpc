# Tamil Nadu Assembly Election 2026 — Data Analysis
### Codebasics Resume Project Challenge (RPC)

A data-driven analysis comparing the 2021 and 2026 Tamil Nadu Assembly Election results, built as a submission for the [Codebasics Resume Project Challenge](https://codebasics.io/challenge/codebasics-resume-project-challenge).

---

## Key Findings

- **TVK won 108 seats** in 2026 — a party founded in 2024 became the single largest party
- **69.7% of constituencies flipped** their winning party between 2021 and 2026 (163 out of 234)
- **DMK dropped from 133 → 59 seats**; AIADMK from 66 → 47
- **South region** had the most flips (38 seats); Delta was the most stable (15 flips)
- Dominant wins (>50% vote share) collapsed from **68 → 13** — races became far closer
- **Tiruppattur** was decided by just **1 vote** — the closest race in the dataset

---

## Project Structure

```
tn-election-2026-rpc/
│
├── tn_election_analysis.py       ← Complete Python analysis (all stories)
├── TN_Election_2026_Analysis.pptx ← 10-slide stakeholder deck
├── constituency_summary.xlsx     ← Constituency-level comparison table (output)
├── README.md                     ← This file
│
└── data/
    ├── tn_2021_results.csv       ← 2021 candidate-level results (4,232 rows)
    ├── tn_2026_results.csv       ← 2026 candidate-level results (4,257 rows)
    └── constituency_master.csv  ← Master list of 234 constituencies with region & reservation
```

---

## Stories Covered

### Story 1 — Who Won What? (Q1 + overall)
Seat distribution by party across 2021 and 2026, broken down by all 6 geographic regions: Chennai Metro, North, Central, Kongu, South, Delta.

### Story 2 — The Flip Story (Q2)
Which constituencies changed their winning party? Analysis of 163 flipped seats, most common party switches, and regional concentration of flips.

### Story 3 — Margins of Victory (Q6)
How dominant were the wins? Distribution of winner vote share, comparison of dominant vs close races, top 10 biggest wins and closest races.

---

## Data Sources

| File | Source |
|------|--------|
| `tn_2021_results.csv` | Tamil Nadu Election Commission via Codebasics RPC dataset |
| `tn_2026_results.csv` | Tamil Nadu Election Commission via Codebasics RPC dataset |
| `constituency_master.csv` | Codebasics RPC dataset |

---

## How to Reproduce

### Requirements
```
Python 3.8+
pandas
matplotlib
seaborn
```

### Install dependencies
```bash
pip install pandas matplotlib seaborn openpyxl
```

### Run the analysis
```bash
python tn_election_analysis.py
```

Make sure the 3 CSV files are in the same folder as the script, or update the file paths at the top of Section 2.

### Output files generated
- `chart1_party_seats.png` — Seats won by party: 2021 vs 2026
- `chart2_flips.png` — Constituency flips by region and party switches
- `chart3_margins.png` — Distribution of winner vote share
- `chart4_regions.png` — Seats per region by party
- `constituency_summary.csv` — Full constituency-level data table
- `constituency_summary.xlsx` — Same table in Excel format

---

## Data Limitations

1. **2026 turnout data is missing** — the `turnout` column in `tn_2026_results.csv` is blank. No turnout comparisons between years are made in this analysis.
2. **TVK did not contest in 2021** — TVK was founded in 2024. All TVK 2026 wins are counted as flips from the previous winning party.
3. **Alliance context not in data** — seat-sharing arrangements between parties are not reflected in the raw results data.
4. **No causal claims** — this analysis describes what happened, not why. Voter motivation, campaign factors, and socioeconomic drivers are outside the scope of this dataset.

---

## Tools Used

- **Python** (pandas, matplotlib, seaborn) — data analysis and chart generation
- **Google Colab** — development environment
- **PptxGenJS** — slide deck generation
- **PowerPoint** — final deck formatting

---

## Author

Submitted for Codebasics Resume Project Challenge
**Deadline:** 28 May 2026
