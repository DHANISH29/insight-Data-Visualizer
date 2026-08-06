import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ---------- Sample dataset ----------
def load_sample_dataset():
    np.random.seed(11)
    n = 600
    categories = ["Electronics", "Clothing", "Home", "Sports", "Books"]
    regions = ["North", "South", "East", "West"]
    dates = pd.date_range("2026-01-01", "2026-07-31", freq="D")

    df = pd.DataFrame({
        "order_id": range(1, n + 1),
        "order_date": np.random.choice(dates, n),
        "category": np.random.choice(categories, n, p=[0.28, 0.22, 0.2, 0.18, 0.12]),
        "region": np.random.choice(regions, n),
        "price": np.round(np.random.gamma(4, 15, n), 2),
        "quantity": np.random.randint(1, 6, n),
        "customer_age": np.random.randint(18, 70, n),
        "rating": np.round(np.clip(np.random.normal(4, 0.8, n), 1, 5), 1),
    })
    df["revenue"] = np.round(df["price"] * df["quantity"], 2)
    df = df.sort_values("order_date").reset_index(drop=True)
    return df

# ---------- Page config ----------
st.set_page_config(page_title="Insight", page_icon="📊", layout="wide")

# ---------- CSS ----------
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;700&display=swap" rel="stylesheet">
<style>
    /* Global Reset & Typography */
    html, body, [class*="css"]  { 
        font-family: 'Inter', sans-serif; 
        background-color: #000000; 
        color: #bbbbbb; 
    }
    .stApp, .main, .block-container { 
        background-color: #000000; 
    }
    h1, h2, h3, h4, h5, h6 { 
        font-family: 'Inter', sans-serif !important; 
        color: #ffffff; 
        text-transform: uppercase; 
        font-weight: 700; 
        letter-spacing: -0.5px; 
    }
    
    /* Header Typography */
    .app-title {
        font-family: 'Inter', sans-serif; 
        font-weight: 700; 
        font-size: 80px; 
        color: #ffffff; 
        margin-bottom: 0;
        line-height: 1.0;
        text-transform: uppercase;
        letter-spacing: -0.5px;
    }
    .app-subtitle {
        font-family: 'Inter', sans-serif; 
        color: #e6e6e6; 
        font-size: 20px; 
        font-weight: 300;
        line-height: 1.4;
        margin-top: 16px; 
        margin-bottom: 64px;
    }

    /* M Stripe Divider */
    .m-stripe {
        display: flex; height: 4px; width: 100%; margin-bottom: 40px;
    }
    .m-stripe > div { flex: 1; }
    .m-blue-light { background-color: #0066b1; }
    .m-blue-dark { background-color: #1c69d4; }
    .m-red { background-color: #e22718; }

    /* KPI Cards */
    .stat-card {
        background: #0d0d0d; 
        border-radius: 0px; 
        padding: 24px;
        border: 1px solid #3c3c3c;
    }
    .stat-label { 
        font-size: 14px; 
        color: #7e7e7e; 
        text-transform: uppercase; 
        letter-spacing: 1.5px; 
        font-weight: 700; 
    }
    .stat-value { 
        font-family: 'Inter', sans-serif; 
        font-size: 32px; 
        font-weight: 700; 
        color: #ffffff; 
        margin-top: 8px; 
        text-transform: uppercase;
    }
    .card { background: #1a1a1a; border-radius: 0px; padding: 24px; border: 1px solid #3c3c3c; }

    /* Buttons */
    .stButton button, .stDownloadButton button { 
        background-color: transparent !important; 
        color: #ffffff !important; 
        border-radius: 0px !important; 
        font-weight: 700 !important; 
        border: 1px solid #ffffff !important; 
        padding: 16px 32px !important; 
        text-transform: uppercase !important;
        letter-spacing: 1.5px !important;
        font-size: 14px !important;
        height: 48px !important;
        transition: none !important;
    }
    .stButton button:hover, .stButton button:active, .stButton button:focus,
    .stDownloadButton button:hover, .stDownloadButton button:active, .stDownloadButton button:focus { 
        background-color: #ffffff !important; 
        color: #000000 !important; 
        border-color: #ffffff !important;
    }
    
    /* Streamlit overrides for dark mode feel */
    [data-testid="stExpander"] { border: 1px solid #3c3c3c; border-radius: 0px; background-color: #1a1a1a; }
    div[data-testid="stExpanderDetails"] { background-color: #000000; }
    
    /* Dataframes and tables */
    [data-testid="stDataFrame"] { border: 1px solid #3c3c3c; }
    [data-testid="stDataFrame"] > div { border-radius: 0px !important; }

    /* Forms */
    .stMultiSelect div[data-baseweb="select"] { background-color: #1a1a1a; border-radius: 0px; border: 1px solid #3c3c3c; }
    .stSelectbox div[data-baseweb="select"] { background-color: #1a1a1a; border-radius: 0px; border: 1px solid #3c3c3c; }
    .stTextInput input, .stDateInput input { background-color: #1a1a1a; border-radius: 0px; border: 1px solid #3c3c3c; color: #ffffff; }
    
    /* Typography Overrides */
    p, .stMarkdown p { font-weight: 300; }
    label p { font-weight: 700 !important; font-size: 14px !important; letter-spacing: 1.5px; text-transform: uppercase; color: #ffffff; }
    
</style>
""", unsafe_allow_html=True)

PALETTE = ["#ffffff", "#0066b1", "#1c69d4", "#e22718", "#7e7e7e", "#2b2b2b"]

# ---------- Header ----------
st.markdown('<div class="app-title">INSIGHT</div>', unsafe_allow_html=True)
st.markdown('<div class="app-subtitle">Upload your own CSV — filters, KPIs, and charts generate automatically. Or explore the sample dataset.</div>', unsafe_allow_html=True)
st.markdown('<div class="m-stripe"><div class="m-blue-light"></div><div class="m-blue-dark"></div><div class="m-red"></div></div>', unsafe_allow_html=True)

# ---------- Data source ----------
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
use_sample = st.checkbox("Or use a sample sales dataset instead", value=not uploaded_file)

df = None
if uploaded_file is not None and not use_sample:
    try:
        df = pd.read_csv(uploaded_file)
        date_cols = [c for c in df.columns if "date" in c.lower()]
        for c in date_cols:
            df[c] = pd.to_datetime(df[c], errors="coerce")
    except Exception as e:
        st.error(f"Couldn't read that CSV: {e}")
elif use_sample:
    df = load_sample_dataset()

st.write("")

if df is not None:
    # ---------- Filters ----------
    with st.expander("🔍 Filters", expanded=True):
        filter_cols = st.columns(3)
        filtered_df = df.copy()

        categorical_cols = df.select_dtypes(exclude=np.number).select_dtypes(exclude="datetime").columns.tolist()
        date_cols = df.select_dtypes(include="datetime").columns.tolist()
        # Only offer low-cardinality columns as filters — a 50-option dropdown for an ID/name column isn't usable
        filterable_cats = [c for c in categorical_cols if 1 < df[c].nunique() <= 30]

        col_idx = 0
        for cat_col in filterable_cats[:2]:
            with filter_cols[col_idx % 3]:
                options = sorted(df[cat_col].dropna().unique().tolist())
                selected = st.multiselect(f"{cat_col}", options, default=options)
                if selected:
                    filtered_df = filtered_df[filtered_df[cat_col].isin(selected)]
            col_idx += 1

        if date_cols:
            with filter_cols[col_idx % 3]:
                d_col = date_cols[0]
                min_d, max_d = df[d_col].min(), df[d_col].max()
                date_range = st.date_input(f"{d_col} range", value=(min_d, max_d))
                if len(date_range) == 2:
                    filtered_df = filtered_df[
                        (filtered_df[d_col] >= pd.Timestamp(date_range[0])) &
                        (filtered_df[d_col] <= pd.Timestamp(date_range[1]))
                    ]

    st.write("")

    numeric_cols = filtered_df.select_dtypes(include=np.number).columns.tolist()
    all_cols = filtered_df.columns.tolist()

    # ---------- KPI cards ----------
    if "revenue" in filtered_df.columns:
        total_revenue = filtered_df["revenue"].sum()
        total_orders = len(filtered_df)
        avg_order = filtered_df["revenue"].mean() if total_orders else 0
        top_cat = filtered_df.groupby("category")["revenue"].sum().idxmax() if "category" in filtered_df.columns and not filtered_df.empty else "—"

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f"""<div class="stat-card"><div class="stat-label">Total Revenue</div>
            <div class="stat-value">₹{total_revenue:,.0f}</div></div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""<div class="stat-card"><div class="stat-label">Total Orders</div>
            <div class="stat-value">{total_orders:,}</div></div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""<div class="stat-card"><div class="stat-label">Avg Order Value</div>
            <div class="stat-value">₹{avg_order:,.0f}</div></div>""", unsafe_allow_html=True)
        with c4:
            st.markdown(f"""<div class="stat-card"><div class="stat-label">Top Category</div>
            <div class="stat-value">{top_cat}</div></div>""", unsafe_allow_html=True)
        st.write("")
    else:
        # Generic KPIs for any uploaded dataset that doesn't match the sample schema
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f"""<div class="stat-card"><div class="stat-label">Rows</div>
            <div class="stat-value">{len(filtered_df):,}</div></div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""<div class="stat-card"><div class="stat-label">Columns</div>
            <div class="stat-value">{filtered_df.shape[1]}</div></div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""<div class="stat-card"><div class="stat-label">Numeric Columns</div>
            <div class="stat-value">{len(numeric_cols)}</div></div>""", unsafe_allow_html=True)
        with c4:
            missing_pct = (filtered_df.isna().sum().sum() / (filtered_df.shape[0] * filtered_df.shape[1]) * 100) if not filtered_df.empty else 0
            st.markdown(f"""<div class="stat-card"><div class="stat-label">Missing Data</div>
            <div class="stat-value">{missing_pct:.1f}%</div></div>""", unsafe_allow_html=True)
        st.write("")

    if filtered_df.empty:
        st.warning("No data matches the current filters.")
    else:
        # ---------- Built-in dashboard charts ----------
        if "order_date" in filtered_df.columns and "revenue" in filtered_df.columns:
            st.markdown("#### Revenue over time")
            trend = filtered_df.groupby(filtered_df["order_date"].dt.to_period("W"))["revenue"].sum().reset_index()
            trend["order_date"] = trend["order_date"].astype(str)
            fig_trend = px.line(trend, x="order_date", y="revenue", markers=True,
                                 color_discrete_sequence=PALETTE)
            fig_trend.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                                     font=dict(family="Inter", color="#bbbbbb"), margin=dict(t=20, b=20, l=20, r=20), height=320)
            st.plotly_chart(fig_trend, width="stretch")
            st.write("")

        chart_row1_left, chart_row1_right = st.columns(2)
        if "category" in filtered_df.columns and "revenue" in filtered_df.columns:
            with chart_row1_left:
                st.markdown("#### Revenue by category")
                by_cat = filtered_df.groupby("category")["revenue"].sum().reset_index().sort_values("revenue", ascending=False)
                fig_cat = px.bar(by_cat, x="category", y="revenue", color="category",
                                  color_discrete_sequence=PALETTE)
                fig_cat.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", showlegend=False,
                                       font=dict(family="Inter", color="#bbbbbb"), margin=dict(t=20, b=20, l=20, r=20), height=320)
                st.plotly_chart(fig_cat, width="stretch")

        if "region" in filtered_df.columns and "revenue" in filtered_df.columns:
            with chart_row1_right:
                st.markdown("#### Revenue share by region")
                by_region = filtered_df.groupby("region")["revenue"].sum().reset_index()
                fig_region = px.pie(by_region, names="region", values="revenue", hole=0.55,
                                     color_discrete_sequence=PALETTE)
                fig_region.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(family="Inter", color="#bbbbbb"),
                                          margin=dict(t=20, b=20, l=20, r=20), height=320)
                st.plotly_chart(fig_region, width="stretch")

        # ---------- Generic auto-charts for any uploaded dataset ----------
        # Only trigger when the sample-specific columns above didn't already cover this data
        has_sample_schema = "revenue" in filtered_df.columns and ("category" in filtered_df.columns or "region" in filtered_df.columns)
        if not has_sample_schema:
            st.markdown("#### Auto-generated overview")
            gen_left, gen_right = st.columns(2)

            first_numeric = numeric_cols[0] if numeric_cols else None
            # Prefer a genuinely categorical column (low cardinality) over ID/name-like columns
            # (e.g. a "student_name" column with 50 unique values in 50 rows makes an unreadable chart)
            chartable_cats = [c for c in categorical_cols if 1 < filtered_df[c].nunique() <= min(20, max(2, len(filtered_df) // 2))]
            first_cat = min(chartable_cats, key=lambda c: filtered_df[c].nunique()) if chartable_cats else None

            if first_cat and first_numeric:
                with gen_left:
                    st.markdown(f"##### {first_numeric} by {first_cat}")
                    by_group = filtered_df.groupby(first_cat)[first_numeric].sum().reset_index().sort_values(first_numeric, ascending=False).head(15)
                    fig_gen_bar = px.bar(by_group, x=first_cat, y=first_numeric, color=first_cat,
                                          color_discrete_sequence=PALETTE)
                    fig_gen_bar.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", showlegend=False,
                                               font=dict(family="Inter", color="#bbbbbb"), margin=dict(t=20, b=20, l=20, r=20), height=320)
                    st.plotly_chart(fig_gen_bar, width="stretch")
            elif first_cat:
                with gen_left:
                    st.markdown(f"##### Count by {first_cat}")
                    counts = filtered_df[first_cat].value_counts().head(15).reset_index()
                    counts.columns = [first_cat, "count"]
                    fig_gen_bar = px.bar(counts, x=first_cat, y="count", color=first_cat,
                                          color_discrete_sequence=PALETTE)
                    fig_gen_bar.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", showlegend=False,
                                               font=dict(family="Inter", color="#bbbbbb"), margin=dict(t=20, b=20, l=20, r=20), height=320)
                    st.plotly_chart(fig_gen_bar, width="stretch")

            if first_numeric:
                with gen_right:
                    st.markdown(f"##### Distribution of {first_numeric}")
                    fig_gen_hist = px.histogram(filtered_df, x=first_numeric, nbins=30,
                                                 color_discrete_sequence=PALETTE)
                    fig_gen_hist.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                                                font=dict(family="Inter", color="#bbbbbb"), margin=dict(t=20, b=20, l=20, r=20), height=320)
                    st.plotly_chart(fig_gen_hist, width="stretch")

            if date_cols and first_numeric:
                st.markdown(f"##### {first_numeric} over time")
                d_col = date_cols[0]
                trend_generic = filtered_df.groupby(filtered_df[d_col].dt.to_period("W"))[first_numeric].sum().reset_index()
                trend_generic[d_col] = trend_generic[d_col].astype(str)
                fig_gen_trend = px.line(trend_generic, x=d_col, y=first_numeric, markers=True,
                                         color_discrete_sequence=PALETTE)
                fig_gen_trend.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                                             font=dict(family="Inter", color="#bbbbbb"), margin=dict(t=20, b=20, l=20, r=20), height=320)
                st.plotly_chart(fig_gen_trend, width="stretch")

            if not first_numeric and not first_cat:
                st.info("Couldn't detect numeric or categorical columns to auto-chart — use the custom chart builder below.")

        st.write("")

        # ---------- Custom chart builder ----------
        st.markdown("#### 🛠️ Build your own chart")
        b1, b2, b3, b4 = st.columns(4)
        with b1:
            chart_type = st.selectbox("Chart type", ["Bar", "Line", "Scatter", "Box"])
        with b2:
            x_axis = st.selectbox("X-axis", all_cols)
        with b3:
            y_options = numeric_cols if numeric_cols else all_cols
            y_axis = st.selectbox("Y-axis", y_options)
        with b4:
            color_options = ["None"] + all_cols
            color_by = st.selectbox("Color by", color_options)
        color_arg = None if color_by == "None" else color_by

        try:
            if chart_type == "Bar":
                fig_custom = px.bar(filtered_df, x=x_axis, y=y_axis, color=color_arg, color_discrete_sequence=PALETTE)
            elif chart_type == "Line":
                fig_custom = px.line(filtered_df.sort_values(x_axis), x=x_axis, y=y_axis, color=color_arg, color_discrete_sequence=PALETTE)
            elif chart_type == "Scatter":
                fig_custom = px.scatter(filtered_df, x=x_axis, y=y_axis, color=color_arg, color_discrete_sequence=PALETTE)
            else:
                fig_custom = px.box(filtered_df, x=x_axis, y=y_axis, color=color_arg, color_discrete_sequence=PALETTE)

            fig_custom.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                                      font=dict(family="Inter", color="#bbbbbb"), margin=dict(t=20, b=20, l=20, r=20), height=380)
            st.plotly_chart(fig_custom, width="stretch")
        except Exception as e:
            st.error(f"Couldn't build that chart: {e}")

        st.write("")
        st.markdown("#### Filtered data")
        st.dataframe(filtered_df.head(50), width="stretch")
        csv = filtered_df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download filtered data as CSV", csv, "filtered_data.csv", "text/csv")

else:
    st.info("Upload a CSV above, or check the sample dataset box to explore the dashboard.")
