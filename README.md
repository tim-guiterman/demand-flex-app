# Edo Demand Flexibility Assessment Tool

Automated peak demand analysis and flexibility quantification for commercial buildings.

## What This Does

This Streamlit application analyzes AMI (Advanced Metering Infrastructure) interval data to:
- Identify peak demand patterns and timing
- Quantify demand flexibility potential
- Visualize load profiles interactively
- Estimate economic value from demand response
- Generate exportable reports

Built for Edo Energy to rapidly assess buildings for utility demand flexibility programs.

---

## Quick Start

### 1. Install Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Mac/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### 2. Run the Application

```bash
streamlit run app.py
```

This will open the application in your default browser at `http://localhost:8501`

### 3. Upload Your Data

- Click "Browse files" in the sidebar
- Upload a CSV file with AMI interval data
- See instant analysis and visualizations

---

## Data Format Requirements

Your CSV file should have:

**Required Columns:**
- **Timestamp column**: Named `ts`, `timestamp`, `time`, or `datetime`
- **Demand column**: Numeric values in kilowatts (kW)

**Supported Intervals:**
- 15-minute intervals (preferred)
- Hourly intervals
- Any regular interval

**Example CSV:**
```csv
ts,kw
2023-04-17 00:00:00,236.0
2023-04-17 00:15:00,236.0
2023-04-17 00:30:00,238.4
2023-04-17 00:45:00,247.2
```

**Tips:**
- At least 30 days of data recommended for meaningful analysis
- More data (1-2 years) provides better seasonal insights
- Missing data gaps < 2 hours will be handled automatically

---

## Features

### Key Metrics Dashboard
- **Peak Demand**: Maximum interval demand
- **Average Load**: Mean demand across all intervals
- **Flexibility Opportunity**: Reduction potential (peak - 90th percentile)
- **Economic Value**: Estimated annual savings from peak shaving

### Interactive Visualizations
1. **Time Series Chart**: Full demand profile with range selector and zoom
2. **Load Duration Curve**: All intervals sorted by demand, showing peak shaving opportunity
3. **Monthly Peak Table**: Summary of peak events by month

### Export Capabilities
- Monthly peaks summary (CSV)
- Full analyzed dataset (CSV)
- Executive summary report (TXT)

### Analysis Features
- Automatic percentile-based flexibility quantification
- Peak timing pattern detection (hour of day, day of week)
- Top 1% hour identification for targeted demand response
- Economic value calculation with configurable demand charge rates

### AI Chat
- Ask natural language questions about your data
- Get insights on peak patterns, flexibility opportunities, and optimization strategies
- Requires `ANTHROPIC_API_KEY` (add to `.streamlit/secrets.toml` locally or Streamlit Cloud Secrets)

---

## Sharing Your Demo

### Option 1: Screen Share (Easiest)
1. Run the app locally: `streamlit run app.py`
2. Share your screen in Zoom/Teams/Google Meet
3. Walk through the analysis live

### Option 2: Deploy to Streamlit Cloud (Free!)

1. **Push to GitHub:**
```bash
git init
git add .
git commit -m "Initial Edo demand flex app"
git push origin main
```

2. **Deploy:**
- Go to [share.streamlit.io](https://share.streamlit.io)
- Sign in with GitHub
- Click "New app"
- Select your repository
- App will be live at: `https://your-app.streamlit.app`

**Time:** 5-10 minutes | **Cost:** Free for public apps

### Option 3: Ngrok Tunnel (Share from Your Machine)

```bash
# While app is running locally
ngrok http 8501
```

This gives you a public URL (e.g., `https://abc123.ngrok.io`) that anyone can access temporarily.

---

## Project Structure

```
demand-flex-potential-app/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── sample_data/              # Sample CSV files for testing
│   └── (add your test data here)
└── .gitignore               # Git ignore file (optional)
```

---

## Customization

### Change Demand Charge Rate
Use the sidebar input to adjust the $/kW/month rate for your utility

### Modify Flexibility Threshold
Currently uses 90th percentile as baseline. To change, edit line 66 in `app.py`:
```python
baseline = df[meterID].quantile(0.90)  # Change 0.90 to desired percentile
```

### Add Weather Data
Future enhancement - add second file uploader for weather CSV and merge on timestamp

---

## Troubleshooting

### "Could not find timestamp column"
- Ensure your CSV has a column named `ts`, `timestamp`, `time`, or `datetime`
- Check that timestamp values are in a recognizable format (YYYY-MM-DD HH:MM:SS)

### "No numeric columns found"
- Verify your CSV has at least one numeric column for kW demand values
- Check for non-numeric characters in the demand column

### App won't start
- Verify all dependencies installed: `pip install -r requirements.txt`
- Check Python version: Requires Python 3.8+
- Try: `streamlit --version` to confirm Streamlit is installed

### Charts not displaying
- Check browser console for JavaScript errors
- Try a different browser (Chrome recommended)
- Ensure plotly is installed: `pip install plotly`

---

## Future Enhancements

**Planned Features:**
- Weather data integration and correlation analysis
- Day-of-week overlay profiles
- Multi-building portfolio comparison
- BAS trend data overlay
- Advanced ML-based peak forecasting
- Automated report generation (PDF)
- API integration for live data feeds

---

## About Edo Energy

Edo recruits commercial buildings into utility-sponsored demand flexibility programs by connecting to building automation systems and monitoring all building systems. This tool focuses on the critical first step: assessing demand flexibility potential through interval meter data analysis.

**Contact:** For questions or support, contact the Edo development team.

---

## License

Internal tool for Edo Energy. Not for external distribution.

---

## Development Notes

**Built with:**
- Streamlit 1.30+ (web framework)
- Pandas 2.0+ (data processing)
- Plotly 5.18+ (interactive visualizations)
- NumPy 1.24+ (numerical operations)

**Based on:** Proven Jupyter notebook methodology for demand flexibility assessment

**Development Time:** MVP built in 1 day for rapid "art of the possible" demonstration
