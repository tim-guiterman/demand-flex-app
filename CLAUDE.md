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

Follows **Flex System Design** (`/Users/tim/Documents/claude-input-files/flex-system-design.skill`).

### Design Tokens
- Primary brand colors: Primary-700 (#3D2F90), Primary-800 (#282765)
- Interactive elements: Primary-600 (#4D43BF) default, Primary-700 on hover
- Typography: Inter font family, Medium 500 weight for headings
- See `app.py` COLORS dict for full token implementation

### Content Guidelines
- Professional, understated tone
- No emojis anywhere in the UI (including section headers)
- No playful or tutorial-style language
- Emojis allowed only in `st.warning()` and `st.error()` messages
