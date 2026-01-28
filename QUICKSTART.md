# Quick Start Guide - Get Running in 5 Minutes

## Step 1: Install Dependencies (2 minutes)

Open your terminal and navigate to this folder:

```bash
cd /Users/tim/Documents/claude-projects-local/demand-flex-potential-app
```

Create a virtual environment and install packages:

```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # Mac/Linux
# OR
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

## Step 2: Prepare Your Data (1 minute)

You need a CSV file with AMI interval data. You have two options:

### Option A: Export from Your Jupyter Notebook

Add this to your notebook and run it:

```python
# Export your grocery Spokane data
thedata.to_csv('grocery_ami_data.csv', index=True)
```

Then move the CSV to the `sample_data/` folder.

### Option B: Use Any AMI CSV You Have

Just make sure it has:
- A timestamp column (named `ts`, `timestamp`, `time`, or `datetime`)
- A numeric kW column
- At least a few weeks of data

## Step 3: Run the App (1 minute)

```bash
streamlit run app.py
```

Your browser should automatically open to `http://localhost:8501`

If it doesn't, manually open that URL in Chrome or Firefox.

## Step 4: Upload and Analyze (1 minute)

1. Click "Browse files" in the sidebar
2. Select your CSV file
3. Watch the magic happen! ✨

You'll instantly see:
- Peak demand metrics
- Interactive time series chart
- Load duration curve
- Monthly peak summary
- Downloadable reports

## Troubleshooting

**"Command not found: streamlit"**
- Make sure you activated the virtual environment: `source venv/bin/activate`
- Try: `pip install streamlit` again

**"Could not find timestamp column"**
- Check your CSV has a column named `ts`, `timestamp`, `time`, or `datetime`
- The app shows you which columns it found - adjust your CSV if needed

**Charts not showing**
- Try refreshing the browser
- Make sure you're using Chrome, Firefox, or Safari
- Check that plotly installed: `pip list | grep plotly`

## Next Steps

### Share with Colleagues

**For Today (Screen Share):**
- Just share your screen while the app is running
- Walk through the analysis together

**For Tomorrow (Public URL):**
1. Deploy to Streamlit Cloud (see README.md for details)
2. Get a public URL like `https://edo-demand-flex.streamlit.app`
3. Share the link with anyone

### Customize

- **Change demand charge rate**: Use the sidebar slider
- **Add more buildings**: Just upload different CSV files
- **Modify calculations**: Edit `app.py` (well-commented code)

### Add Features

See the "Future Enhancements" section in README.md for ideas like:
- Weather data integration
- Day-of-week overlays
- Multi-building comparison

---

## That's It!

You now have a working demand flexibility assessment tool. Total time: ~5 minutes.

**Questions?** Check the full README.md or the app's built-in help text.

Happy analyzing! ⚡
