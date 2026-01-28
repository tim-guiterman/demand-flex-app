# Energy Data Analyzer

Streamlit app for automated energy data cleaning and natural language analysis.

## Run

```bash
python3 -m streamlit run app.py
```

Requires `ANTHROPIC_API_KEY` in environment or Streamlit secrets for AI analysis features.

## Dependencies

- streamlit
- pandas
- numpy
- matplotlib
- anthropic

## Key Features

- CSV/Excel upload with auto-detection of header rows and sheet selection
- Auto-detects timestamp and energy columns
- Cleans data: fills missing values (forward-fill), flags outliers (z-score > 3 std dev)
- Generates data provenance document
- AI-powered natural language queries (10 query limit per session)

## Sample Data

Use `sample_data/grocery_spokane_sample.csv` for testing.

## UI Guidelines

- Professional, understated tone - no playful/tutorial language
- No emojis except warning symbol in `st.warning()` and `st.error()` messages
- Uses Inter font family
- Query counter shows "X of 10 queries used" (not "X remaining")
