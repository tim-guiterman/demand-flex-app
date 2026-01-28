# Edo Demand Flexibility Assessment Tool

Streamlit app for automated peak demand analysis and flexibility quantification for commercial buildings.

## Run

```bash
streamlit run app.py
```

## Dependencies

- streamlit
- pandas
- numpy
- plotly

## Key Features

- CSV upload with auto-detection of timestamp and demand columns
- Peak demand metrics and flexibility opportunity quantification
- Interactive time series chart with zoom/range selector
- Load duration curve visualization
- Monthly peak summary table
- Economic value estimation with configurable demand charge rates
- Exportable reports (CSV, TXT)

## Sample Data

Use `sample_data/grocery_spokane_sample.csv` for testing.

## UI Guidelines

- Professional, understated tone
- No emojis in code except warning symbols in `st.warning()` and `st.error()`
- Uses Inter font family
