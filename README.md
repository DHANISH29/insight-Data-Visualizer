# Insight — Interactive Data Visualization Dashboard

## Problem
Turn a raw dataset into a filterable, explorable dashboard without hardcoding a fixed set of charts — closes out Week 2 (EDA → SQL → cleaning → ETL → visualization is the full data-handling pipeline).

## How it works
Upload any CSV (or use the built-in sample sales dataset). Auto-generated filters (categorical multiselects + a date range picker) narrow the dataset live — filter columns are chosen automatically, skipping high-cardinality ID/name-like columns that would produce an unusable 50-option dropdown. KPI cards adapt to the data: sales-style metrics (revenue, orders, AOV, top category) when those columns exist, or generic dataset stats (rows, columns, numeric column count, missing %) otherwise. Charts follow the same pattern — 3 sales-specific charts for the sample schema, or an auto-generated overview (grouped bar chart, distribution histogram, trend line) built from whichever numeric/categorical/date columns your actual file has, picking genuinely categorical columns over ID-like ones for grouping. A **custom chart builder** below lets you pick any chart type, X-axis, Y-axis, and color grouping from your real columns regardless of dataset shape.

## How to run
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy it live
Push to GitHub, deploy on https://streamlit.io/cloud pointing at `app.py`.

## What I'd improve
- The auto-chart selection only picks the *first* qualifying numeric/categorical column — a v2 could let users pick which columns drive the auto-dashboard instead of always defaulting to the first match.
- No chart export (PNG/SVG) yet — Plotly supports this natively, worth adding.
- Cardinality thresholds (20 for auto-charts, 30 for filters) are fixed heuristics — could be made adjustable for edge-case datasets.
