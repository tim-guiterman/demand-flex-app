import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import os
from anthropic import Anthropic

# Page config with Flex branding
st.set_page_config(
    page_title="Edo Flex - Demand Flexibility Assessment",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Flex System Design Tokens
COLORS = {
    # Primary Brand Colors
    'primary_700': '#3D2F90',
    'primary_800': '#282765',
    'primary_600': '#4D43BF',
    'primary_500': '#6661CF',
    'primary_100': '#DED7F7',
    'primary_50': '#F1EFFE',

    # Grays
    'gray_50': '#F7F9FC',
    'gray_200': '#E2E7F0',
    'gray_400': '#A0ABC0',
    'gray_500': '#717D96',
    'gray_600': '#5C677E',
    'gray_700': '#4A5468',
    'gray_800': '#2E3340',

    # Status Colors
    'green_600': '#439C56',
    'green_50': '#F2FCF4',
    'red_600': '#9D3B3B',
    'red_50': '#FAECEC',
    'mustard_500': '#B88343',
    'mustard_50': '#FFF8F2',
    'aqua_600': '#2EAAA2',
    'aqua_50': '#EAFFFE',

    # Data Viz
    'blue_300': '#678DFF',
    'orange_400': '#F2A244',
}

# Custom CSS with Flex Design System
st.markdown(f"""
<style>
    /* Global Styles */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }}

    /* Main content area */
    .main {{
        background-color: {COLORS['gray_50']};
    }}

    /* Headers */
    h1 {{
        font-weight: 500 !important;
        font-size: 32px !important;
        line-height: 1.3 !important;
        letter-spacing: -0.04em !important;
    }}

    /* Main content headers (not in custom divs) */
    .main h1 {{
        color: {COLORS['primary_800']} !important;
    }}

    h2 {{
        color: {COLORS['gray_800']} !important;
        font-weight: 500 !important;
        font-size: 24px !important;
        line-height: 1.4 !important;
    }}

    h3 {{
        color: {COLORS['gray_700']} !important;
        font-weight: 500 !important;
        font-size: 20px !important;
        line-height: 1.4 !important;
    }}

    /* Body text */
    p, .stMarkdown {{
        color: {COLORS['gray_600']} !important;
        font-size: 16px !important;
        line-height: 1.5 !important;
    }}

    /* Metrics */
    [data-testid="stMetricValue"] {{
        color: {COLORS['primary_700']} !important;
        font-size: 28px !important;
        font-weight: 600 !important;
    }}

    [data-testid="stMetricLabel"] {{
        color: {COLORS['gray_600']} !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }}

    [data-testid="stMetricDelta"] {{
        font-size: 14px !important;
        font-weight: 600 !important;
    }}

    /* Cards / Containers */
    .element-container {{
        background-color: white;
        border-radius: 8px;
    }}

    /* Sidebar */
    [data-testid="stSidebar"] {{
        background-color: white !important;
        border-right: 1px solid {COLORS['gray_200']};
    }}

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {{
        color: {COLORS['gray_800']} !important;
    }}

    /* File uploader */
    [data-testid="stFileUploader"] {{
        background-color: {COLORS['primary_50']};
        border: 2px dashed {COLORS['primary_500']};
        border-radius: 8px;
        padding: 20px;
    }}

    /* Buttons */
    .stButton > button {{
        background-color: {COLORS['primary_600']} !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 12px 24px !important;
        font-weight: 500 !important;
        font-size: 16px !important;
        transition: background-color 0.2s ease !important;
    }}

    .stButton > button:hover {{
        background-color: {COLORS['primary_700']} !important;
    }}

    .stButton > button:active {{
        background-color: {COLORS['primary_800']} !important;
    }}

    /* Download buttons */
    .stDownloadButton > button {{
        background-color: white !important;
        color: {COLORS['primary_700']} !important;
        border: 1px solid {COLORS['primary_600']} !important;
        border-radius: 6px !important;
        padding: 10px 20px !important;
        font-weight: 500 !important;
        font-size: 14px !important;
    }}

    .stDownloadButton > button:hover {{
        background-color: {COLORS['primary_50']} !important;
    }}

    /* Info boxes */
    .stAlert {{
        border-radius: 8px !important;
        border: none !important;
    }}

    /* Success messages */
    .stSuccess {{
        background-color: {COLORS['green_50']} !important;
        color: {COLORS['green_600']} !important;
        border-left: 4px solid {COLORS['green_600']} !important;
    }}

    /* Error messages */
    .stError {{
        background-color: {COLORS['red_50']} !important;
        color: {COLORS['red_600']} !important;
        border-left: 4px solid {COLORS['red_600']} !important;
    }}

    /* Info messages */
    .stInfo {{
        background-color: {COLORS['aqua_50']} !important;
        color: {COLORS['aqua_600']} !important;
        border-left: 4px solid {COLORS['aqua_600']} !important;
    }}

    /* Warning messages */
    .stWarning {{
        background-color: {COLORS['mustard_50']} !important;
        color: {COLORS['mustard_500']} !important;
        border-left: 4px solid {COLORS['mustard_500']} !important;
    }}

    /* Dataframes */
    .stDataFrame {{
        border: 1px solid {COLORS['gray_200']} !important;
        border-radius: 8px !important;
    }}

    /* Expander */
    .streamlit-expanderHeader {{
        background-color: {COLORS['primary_50']} !important;
        color: {COLORS['primary_800']} !important;
        border-radius: 6px !important;
        font-weight: 500 !important;
    }}

    /* Number input */
    input[type="number"] {{
        border: 1px solid {COLORS['gray_200']} !important;
        border-radius: 6px !important;
        padding: 8px 12px !important;
        font-size: 16px !important;
    }}

    input[type="number"]:focus {{
        border-color: {COLORS['primary_600']} !important;
        outline: none !important;
        box-shadow: 0 0 0 3px {COLORS['primary_50']} !important;
    }}

    /* Dividers */
    hr {{
        border-color: {COLORS['gray_200']} !important;
        margin: 24px 0 !important;
    }}

    /* Plotly charts - custom colors */
    .js-plotly-plot {{
        border-radius: 8px !important;
        background-color: white !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
        padding: 16px !important;
    }}

    /* Hero header - force white text */
    .hero-header h1,
    .hero-header p {{
        color: white !important;
    }}
</style>
""", unsafe_allow_html=True)

# Header with branding
st.markdown(f"""
<div class="hero-header" style="background: linear-gradient(135deg, {COLORS['primary_800']} 0%, {COLORS['primary_700']} 100%);
            padding: 32px 24px; border-radius: 12px; margin-bottom: 24px; box-shadow: 0 4px 12px rgba(61, 47, 144, 0.15);">
    <div style="color: white;">
        <h1 style="color: white !important; margin: 0 !important;">
            Edo Flex - Demand Flexibility Assessment
        </h1>
        <p style="color: {COLORS['primary_100']} !important; margin: 8px 0 0 0 !important;">
            Automated peak demand analysis and flexibility quantification for commercial buildings
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar for configuration
with st.sidebar:
    st.markdown(f"""
    <h2 style="color: {COLORS['gray_800']}; font-size: 20px; font-weight: 500; margin-bottom: 16px;">
        Configuration
    </h2>
    """, unsafe_allow_html=True)

    # File upload
    uploaded_file = st.file_uploader(
        "Upload AMI Interval Data",
        type=["csv", "xlsx", "xls"],
        help="CSV or Excel file with timestamp and kW columns"
    )

    # Optional: Demand charge rate for economic analysis
    st.markdown("---")
    st.markdown(f"""
    <p style="color: {COLORS['gray_700']}; font-size: 14px; font-weight: 500;
              text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 12px;">
        Economic Analysis
    </p>
    """, unsafe_allow_html=True)

    demand_charge = st.number_input(
        "Utility Demand Charge ($/kW/month)",
        min_value=0.0,
        value=15.0,
        step=0.50,
        help="Enter your utility's demand charge rate"
    )

if uploaded_file:
    try:
        # Detect file type and read accordingly
        file_extension = uploaded_file.name.split('.')[-1].lower()

        if file_extension in ['xlsx', 'xls']:
            df = pd.read_excel(uploaded_file)
        else:  # csv
            df = pd.read_csv(uploaded_file)

        # Clean up - drop completely empty columns
        df = df.dropna(axis=1, how='all')  # Remove columns that are all NaN
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]  # Remove unnamed columns

        # Try to find timestamp column (flexible matching)
        ts_col = None
        timestamp_keywords = ['ts', 'timestamp', 'time', 'datetime', 'date']

        for col in df.columns:
            col_lower = col.lower().strip()
            # Check if column name contains any timestamp keyword
            if any(keyword in col_lower for keyword in timestamp_keywords):
                ts_col = col
                break

        if ts_col is None:
            st.error("Could not find timestamp column. Expected column name containing: 'ts', 'timestamp', 'time', or 'datetime'")
            st.info("Available columns: " + ", ".join(df.columns.tolist()))
            st.stop()

        # Parse timestamp with flexible format handling
        # This handles various formats: "2023-04-17 00:00:00", "05/15/2023 15:15 EDT", etc.
        try:
            df[ts_col] = pd.to_datetime(df[ts_col], infer_datetime_format=True)
        except:
            # If that fails, try removing timezone strings first
            df[ts_col] = df[ts_col].str.replace(r'\s+(EDT|EST|PDT|PST|CDT|CST|MDT|MST)', '', regex=True)
            df[ts_col] = pd.to_datetime(df[ts_col], infer_datetime_format=True)

        df.set_index(ts_col, inplace=True)

        # Find kW column (flexible matching)
        # Look for columns with keywords like 'kw', 'power', 'demand', 'value'
        kw_keywords = ['kw', 'power', 'demand', 'value', 'load']
        meterID = None

        # First, try to find column with kW-related keywords
        for col in df.columns:
            col_lower = col.lower().strip()
            if any(keyword in col_lower for keyword in kw_keywords):
                # Check if it's numeric
                try:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                    if df[col].notna().sum() > 0:  # Has some valid numeric values
                        meterID = col
                        break
                except:
                    continue

        # If still not found, just take the first numeric column
        if meterID is None:
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            if len(numeric_cols) == 0:
                st.error("No numeric columns found in the CSV file")
                st.stop()
            meterID = numeric_cols[0]

        # Clean the data - remove any NaN values
        df = df[[meterID]].dropna()

        st.success(f"✅ Loaded {len(df):,} data points from {df.index.min().strftime('%Y-%m-%d')} to {df.index.max().strftime('%Y-%m-%d')}")

        # --- ANALYTICS ---

        # Basic stats
        peak_load = df[meterID].max()
        avg_load = df[meterID].mean()
        min_load = df[meterID].min()

        # Flexibility potential (simple: peak - 90th percentile)
        baseline = df[meterID].quantile(0.90)
        flex_kw = peak_load - baseline
        flex_pct = (flex_kw / peak_load) * 100

        # Calculate top percentile hours for economic analysis
        top_1_pct = df[meterID].quantile(0.99)
        top_1_pct_count = len(df[df[meterID] >= top_1_pct])

        # Economic value
        annual_savings = flex_kw * demand_charge * 12

        # Monthly peaks
        peaks = df.resample("ME").max()
        peaktimes = df.resample("ME")[[meterID]].idxmax()

        # Build peak summary table
        peakdf = peaktimes.copy()
        peakdf['Year'] = peakdf[meterID].dt.year
        peakdf['Month'] = peakdf[meterID].dt.month_name()
        peakdf['Peak Day'] = peakdf[meterID].dt.day
        peakdf['Peak Day of Week'] = peakdf[meterID].dt.day_name()
        peakdf['Peak Time'] = peakdf[meterID].dt.time
        peakdf['Peak kW'] = peaks[meterID].values
        peakdf.reset_index(drop=True, inplace=True)

        # Clean up columns
        if meterID in peakdf.columns:
            peakdf.drop(meterID, axis=1, inplace=True)

        # --- DISPLAY ---

        # Key metrics with Flex styling
        st.markdown("---")
        st.markdown(f"""
        <h2 style="color: {COLORS['gray_800']}; font-size: 24px; font-weight: 500; margin-bottom: 20px;">
            Key Metrics
        </h2>
        """, unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Peak Demand", f"{peak_load:.1f} kW")
        with col2:
            st.metric("Average Load", f"{avg_load:.1f} kW")
        with col3:
            st.metric("Flexibility Opportunity", f"{flex_kw:.1f} kW", f"{flex_pct:.0f}%")
        with col4:
            st.metric("Est. Annual Savings", f"${annual_savings:,.0f}/yr")

        # Explanatory text
        with st.expander("ℹ️ How are these metrics calculated?"):
            st.markdown(f"""
            - **Peak Demand**: Maximum 15-minute interval demand across entire dataset ({peak_load:.1f} kW)
            - **Average Load**: Mean demand across all intervals ({avg_load:.1f} kW)
            - **Flexibility Opportunity**: Difference between peak and 90th percentile ({baseline:.1f} kW).
              This represents potential kW reduction during highest demand periods.
            - **Est. Annual Savings**: Based on reducing peak demand by flexibility opportunity
              ({flex_kw:.1f} kW × ${demand_charge}/kW/month × 12 months)

            **Top 1% Hours**: The highest {top_1_pct_count} intervals exceed {top_1_pct:.1f} kW.
            Targeting these hours for demand response can maximize savings.
            """)

        # Chart 1: Interactive time series
        st.markdown("---")
        st.markdown(f"""
        <h2 style="color: {COLORS['gray_800']}; font-size: 24px; font-weight: 500; margin-bottom: 16px;">
            Demand Profile - Interactive Time Series
        </h2>
        """, unsafe_allow_html=True)

        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(
            x=list(df.index),
            y=list(df[meterID]),
            mode='lines',
            name='Demand (kW)',
            line=dict(color=COLORS['blue_300'], width=1.5)
        ))

        # Add peak line
        fig1.add_hline(
            y=peak_load,
            line_dash="dash",
            line_color=COLORS['red_600'],
            annotation_text=f"Peak: {peak_load:.1f} kW",
            annotation_font_color=COLORS['red_600']
        )

        # Add baseline line
        fig1.add_hline(
            y=baseline,
            line_dash="dash",
            line_color=COLORS['green_600'],
            annotation_text=f"90th Percentile: {baseline:.1f} kW",
            annotation_font_color=COLORS['green_600']
        )

        fig1.update_layout(
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=7, label="1w", step="day", stepmode="backward"),
                        dict(count=1, label="1m", step="month", stepmode="backward"),
                        dict(count=6, label="6m", step="month", stepmode="backward"),
                        dict(count=1, label="1y", step="year", stepmode="backward"),
                        dict(step="all", label="All")
                    ]),
                    bgcolor=COLORS['gray_50'],
                    activecolor=COLORS['primary_600'],
                    font=dict(color=COLORS['gray_700'])
                ),
                rangeslider=dict(visible=True, bgcolor=COLORS['gray_50']),
                type="date",
                gridcolor=COLORS['gray_200']
            ),
            yaxis_title="kW",
            yaxis=dict(gridcolor=COLORS['gray_200']),
            height=500,
            hovermode='x unified',
            font=dict(family='Inter', size=14, color=COLORS['gray_600']),
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        st.plotly_chart(fig1, use_container_width=True)

        st.markdown(f"""
        <p style="color: {COLORS['gray_600']}; font-size: 14px; margin-top: -12px;">
        <strong>Use the range selector buttons or drag the slider</strong> to explore different time periods.
        <span style="color: {COLORS['red_600']};">Red line</span> shows peak demand;
        <span style="color: {COLORS['green_600']};">green line</span> shows 90th percentile baseline.
        </p>
        """, unsafe_allow_html=True)

        # Chart 2: Load duration curve
        st.markdown("---")
        st.markdown(f"""
        <h2 style="color: {COLORS['gray_800']}; font-size: 24px; font-weight: 500; margin-bottom: 16px;">
            Load Duration Curve - Peak Shaving Visualization
        </h2>
        """, unsafe_allow_html=True)

        sorted_df = df.sort_values(by=meterID, ascending=False).reset_index()

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=list(range(len(sorted_df))),
            y=sorted_df[meterID],
            fill='tozeroy',
            name='Load',
            line=dict(color=COLORS['primary_600']),
            fillcolor=f"rgba(77, 67, 191, 0.2)",
            hovertemplate='Interval: %{x}<br>Demand: %{y:.1f} kW<extra></extra>'
        ))

        # Add line showing flexibility threshold (90th percentile)
        fig2.add_hline(
            y=baseline,
            line_dash="dash",
            line_color=COLORS['green_600'],
            annotation_text=f"Target Baseline: {baseline:.1f} kW",
            annotation_font_color=COLORS['green_600']
        )

        # Highlight top 1% area
        top_1_pct_intervals = int(len(sorted_df) * 0.01)
        fig2.add_vrect(
            x0=0, x1=top_1_pct_intervals,
            fillcolor=f"rgba(157, 59, 59, 0.15)",
            layer="below",
            line_width=0,
            annotation_text=f"Top 1%<br>({top_1_pct_intervals} intervals)",
            annotation_position="top left",
            annotation_font_color=COLORS['red_600']
        )

        fig2.update_layout(
            title=dict(
                text="Load Duration Curve (All Intervals Sorted by Demand)",
                font=dict(size=18, color=COLORS['gray_700'])
            ),
            xaxis_title="15-minute periods at or above kW",
            yaxis_title="kW",
            xaxis=dict(gridcolor=COLORS['gray_200']),
            yaxis=dict(gridcolor=COLORS['gray_200']),
            height=400,
            hovermode='closest',
            font=dict(family='Inter', size=14, color=COLORS['gray_600']),
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        st.plotly_chart(fig2, use_container_width=True)

        st.markdown(f"""
        <p style="color: {COLORS['gray_600']}; font-size: 14px; margin-top: -12px;">
        The load duration curve shows all {len(sorted_df):,} demand intervals sorted from highest to lowest.
        The <strong style="color: {COLORS['red_600']};">shaded red area</strong> represents the top 1% of hours - prime targets for demand response.
        The area above the <span style="color: {COLORS['green_600']};">green dashed line</span> represents total peak shaving opportunity.
        </p>
        """, unsafe_allow_html=True)

        # Table: Monthly peaks
        st.markdown("---")
        st.markdown(f"""
        <h2 style="color: {COLORS['gray_800']}; font-size: 24px; font-weight: 500; margin-bottom: 16px;">
            📅 Monthly Peak Demand Summary
        </h2>
        """, unsafe_allow_html=True)

        # Format the table for better display
        display_df = peakdf.copy()
        display_df['Peak kW'] = display_df['Peak kW'].round(1)

        st.dataframe(display_df, use_container_width=True, hide_index=True)

        # Peak timing analysis
        peak_hours = peakdf['Peak Time'].apply(lambda x: x.hour)
        most_common_hour = peak_hours.mode()[0] if len(peak_hours.mode()) > 0 else int(peak_hours.mean())

        peak_days = peakdf['Peak Day of Week'].value_counts()
        most_common_day = peak_days.index[0] if len(peak_days) > 0 else "N/A"

        col1, col2 = st.columns(2)
        with col1:
            st.info(f"🕐 **Most Common Peak Hour**: {most_common_hour}:00 - {most_common_hour+1}:00")
        with col2:
            st.info(f"📆 **Most Common Peak Day**: {most_common_day}")

        # Downloads
        st.markdown("---")
        st.markdown(f"""
        <h2 style="color: {COLORS['gray_800']}; font-size: 24px; font-weight: 500; margin-bottom: 16px;">
            Export Data & Reports
        </h2>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            csv_peaks = display_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Monthly Peaks (CSV)",
                data=csv_peaks,
                file_name="monthly_peaks.csv",
                mime="text/csv"
            )

        with col2:
            csv_all = df.to_csv()
            st.download_button(
                label="📥 Download Full Dataset (CSV)",
                data=csv_all,
                file_name="full_demand_data.csv",
                mime="text/csv"
            )

        with col3:
            # Summary report
            summary_text = f"""Edo Flex - Demand Flexibility Assessment Summary Report

Building Analysis Summary
Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}

Data Period: {df.index.min().strftime('%Y-%m-%d')} to {df.index.max().strftime('%Y-%m-%d')}
Total Intervals: {len(df):,}

KEY METRICS
-----------
Peak Demand: {peak_load:.1f} kW
Average Load: {avg_load:.1f} kW
Minimum Load: {min_load:.1f} kW
Load Factor: {(avg_load/peak_load)*100:.1f}%

FLEXIBILITY ANALYSIS
-------------------
90th Percentile Baseline: {baseline:.1f} kW
Flexibility Opportunity: {flex_kw:.1f} kW ({flex_pct:.0f}% reduction from peak)
Top 1% Threshold: {top_1_pct:.1f} kW
Top 1% Interval Count: {top_1_pct_count} periods

ECONOMIC VALUE
--------------
Demand Charge Rate: ${demand_charge}/kW/month
Estimated Annual Savings: ${annual_savings:,.0f}/year
(Based on reducing peak by {flex_kw:.1f} kW)

PEAK TIMING PATTERNS
-------------------
Most Common Peak Hour: {most_common_hour}:00
Most Common Peak Day: {most_common_day}

RECOMMENDATIONS
--------------
1. Focus demand response efforts on top 1% of hours ({top_1_pct_count} intervals)
2. Target demand reduction during {most_common_hour}:00 hour on {most_common_day}s
3. Establish baseline at {baseline:.1f} kW (90th percentile)
4. Potential annual savings of ${annual_savings:,.0f} through peak shaving

Generated by Edo Flex - Demand Flexibility Assessment Tool
"""
            st.download_button(
                label="📄 Download Summary Report (TXT)",
                data=summary_text,
                file_name="flexibility_assessment_summary.txt",
                mime="text/plain"
            )

        # AI Chat Section
        st.markdown("---")
        st.markdown(f"""
        <h2 style="color: {COLORS['gray_800']}; font-size: 24px; font-weight: 500; margin-bottom: 16px;">
            Ask Questions About Your Data
        </h2>
        """, unsafe_allow_html=True)

        # Initialize Anthropic client
        api_key = os.environ.get("ANTHROPIC_API_KEY") or st.secrets.get("ANTHROPIC_API_KEY", None)

        if not api_key:
            st.warning("⚠️ Add ANTHROPIC_API_KEY to environment or Streamlit secrets to enable AI chat.")
        else:
            # Initialize chat history in session state
            if "chat_messages" not in st.session_state:
                st.session_state.chat_messages = []

            # Prepare data context for the AI
            data_context = f"""You are analyzing energy demand data for a commercial building.

DATA SUMMARY:
- Data period: {df.index.min().strftime('%Y-%m-%d')} to {df.index.max().strftime('%Y-%m-%d')}
- Total intervals: {len(df):,}
- Peak demand: {peak_load:.1f} kW
- Average load: {avg_load:.1f} kW
- Minimum load: {min_load:.1f} kW
- Load factor: {(avg_load/peak_load)*100:.1f}%
- 90th percentile baseline: {baseline:.1f} kW
- Flexibility opportunity: {flex_kw:.1f} kW ({flex_pct:.0f}% reduction from peak)
- Top 1% threshold: {top_1_pct:.1f} kW
- Top 1% interval count: {top_1_pct_count} periods
- Most common peak hour: {most_common_hour}:00
- Most common peak day: {most_common_day}
- Demand charge rate: ${demand_charge}/kW/month
- Estimated annual savings: ${annual_savings:,.0f}/year

MONTHLY PEAKS:
{display_df.to_string()}

Answer questions about this energy demand data concisely and professionally. Focus on insights relevant to demand flexibility and peak shaving opportunities."""

            # Display chat history
            for message in st.session_state.chat_messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            # Chat input
            if prompt := st.chat_input("Ask a question about your energy data..."):
                # Add user message to history
                st.session_state.chat_messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)

                # Get AI response
                with st.chat_message("assistant"):
                    with st.spinner("Analyzing..."):
                        try:
                            client = Anthropic(api_key=api_key)

                            # Build messages with context
                            messages = [{"role": "user", "content": data_context}]
                            messages.append({"role": "assistant", "content": "I understand. I have the energy demand data loaded and ready to answer questions about peak demand patterns, flexibility opportunities, and optimization strategies."})

                            # Add chat history
                            for msg in st.session_state.chat_messages:
                                messages.append({"role": msg["role"], "content": msg["content"]})

                            response = client.messages.create(
                                model="claude-sonnet-4-20250514",
                                max_tokens=1024,
                                messages=messages
                            )

                            assistant_message = response.content[0].text
                            st.markdown(assistant_message)
                            st.session_state.chat_messages.append({"role": "assistant", "content": assistant_message})

                        except Exception as chat_error:
                            st.error(f"Error getting response: {chat_error}")

    except Exception as e:
        st.error(f"Error processing file: {e}")
        st.info("Expected format: CSV with timestamp column ('ts', 'timestamp', 'time', or 'datetime') and numeric kW column")

        # Show error details in expander
        with st.expander("🔍 Error Details"):
            st.code(str(e))

else:
    # Welcome screen with Flex branding
    st.info("👆 Upload an AMI interval data file (CSV or Excel) to begin analysis")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(f"""
        <div style="background-color: white; padding: 24px; border-radius: 8px; border: 1px solid {COLORS['gray_200']}; margin-bottom: 20px;">
            <h3 style="color: {COLORS['gray_800']}; font-size: 20px; font-weight: 500; margin-bottom: 16px;">
                Expected Data Format
            </h3>
            <p style="color: {COLORS['gray_600']}; margin-bottom: 12px;">Your file should have:</p>
            <ul style="color: {COLORS['gray_600']}; line-height: 1.8;">
                <li><strong>Format</strong>: CSV or Excel (.xlsx, .xls)</li>
                <li><strong>Timestamp column</strong>: Any column containing 'timestamp', 'time', or 'date'</li>
                <li><strong>Demand column</strong>: Numeric values (column with 'kW', 'power', 'demand', or 'value')</li>
                <li><strong>Interval</strong>: 15-minute or hourly readings</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        **Example formats supported:**
        ```
        # Format 1
        ts,kw
        2023-04-17 00:00:00,236.0
        2023-04-17 00:15:00,236.0

        # Format 2
        Timestamp,Value (kW)
        05/15/2023 15:15 EDT,0.81
        05/15/2023 15:30 EDT,0.81
        ```
        """)

    with col2:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, {COLORS['primary_100']} 0%, {COLORS['primary_50']} 100%);
                    padding: 24px; border-radius: 8px; border: 1px solid {COLORS['primary_600']};">
            <h3 style="color: {COLORS['primary_800']}; font-size: 18px; font-weight: 500; margin-bottom: 16px;">
                Quick Tip
            </h3>
            <p style="color: {COLORS['primary_800']}; font-size: 14px; line-height: 1.6;">
                Use the sample data in the <code>sample_data/</code> folder to test the application.
                You'll find <strong>grocery_spokane_sample.csv</strong> ready to upload!
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown(f"""
    <h2 style="color: {COLORS['gray_800']}; font-size: 24px; font-weight: 500; margin-bottom: 16px;">
        What This Tool Does
    </h2>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <p style="color: {COLORS['gray_600']}; font-size: 16px; line-height: 1.6; margin-bottom: 24px;">
        This application automates demand flexibility assessment for commercial buildings by:
    </p>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        <div style="background-color: {COLORS['green_50']}; padding: 20px; border-radius: 8px;
                    border-left: 4px solid {COLORS['green_600']}; margin-bottom: 16px;">
            <h4 style="color: {COLORS['green_600']}; font-size: 16px; font-weight: 600; margin-bottom: 8px;">
                1. Analyzing Peak Demand Patterns
            </h4>
            <p style="color: {COLORS['gray_600']}; font-size: 14px; margin: 0;">
                Identifies when and how often peaks occur
            </p>
        </div>

        <div style="background-color: {COLORS['aqua_50']}; padding: 20px; border-radius: 8px;
                    border-left: 4px solid {COLORS['aqua_600']}; margin-bottom: 16px;">
            <h4 style="color: {COLORS['aqua_600']}; font-size: 16px; font-weight: 600; margin-bottom: 8px;">
                2. Quantifying Flexibility Potential
            </h4>
            <p style="color: {COLORS['gray_600']}; font-size: 14px; margin: 0;">
                Calculates how much demand can be reduced
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style="background-color: {COLORS['primary_50']}; padding: 20px; border-radius: 8px;
                    border-left: 4px solid {COLORS['primary_600']}; margin-bottom: 16px;">
            <h4 style="color: {COLORS['primary_700']}; font-size: 16px; font-weight: 600; margin-bottom: 8px;">
                3. Visualizing Load Profiles
            </h4>
            <p style="color: {COLORS['gray_600']}; font-size: 14px; margin: 0;">
                Interactive charts to explore demand patterns
            </p>
        </div>

        <div style="background-color: {COLORS['mustard_50']}; padding: 20px; border-radius: 8px;
                    border-left: 4px solid {COLORS['mustard_500']}; margin-bottom: 16px;">
            <h4 style="color: {COLORS['mustard_500']}; font-size: 16px; font-weight: 600; margin-bottom: 8px;">
                4. Estimating Economic Value
            </h4>
            <p style="color: {COLORS['gray_600']}; font-size: 14px; margin: 0;">
                Projects annual savings from demand response
            </p>
        </div>
        """, unsafe_allow_html=True)

# Footer with Flex branding
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; padding: 24px; background-color: {COLORS['gray_50']}; border-radius: 8px;'>
    <p style='color: {COLORS['gray_700']}; font-weight: 500; font-size: 16px; margin-bottom: 8px;'>
        Edo Flex - Demand Flexibility Assessment Tool
    </p>
    <p style='color: {COLORS['gray_500']}; font-size: 14px; margin: 0;'>
        Making buildings grid-interactive through intelligent demand management
    </p>
</div>
""", unsafe_allow_html=True)
