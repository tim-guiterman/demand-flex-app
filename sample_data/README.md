# Sample Data Directory

## How to Use This Folder

Place your test AMI interval data CSV files here to keep your project organized.

## Getting Sample Data

### From Your Jupyter Notebook

Export the grocery Spokane data from your notebook by adding this cell:

```python
# Export sample data for app testing
thedata.to_csv('grocery_ami_data.csv', index=True)
print("Sample data exported to grocery_ami_data.csv")
```

Then copy the generated CSV file to this `sample_data/` folder.

### Creating Synthetic Test Data

If you need to create test data, here's a Python script:

```python
import pandas as pd
import numpy as np

# Create 30 days of 15-minute interval data
dates = pd.date_range('2024-01-01', periods=2880, freq='15min')

# Simulate realistic building load profile
# Base load + time-of-day pattern + some randomness
hour = dates.hour
base_load = 250
time_pattern = 50 * np.sin((hour - 6) * np.pi / 12)  # Peak in afternoon
random_variation = np.random.normal(0, 10, len(dates))
kw = base_load + time_pattern + random_variation

# Create DataFrame
df = pd.DataFrame({
    'ts': dates,
    'kw': kw.clip(min=150)  # Ensure positive values
})

# Save to CSV
df.to_csv('sample_data/synthetic_test_data.csv', index=False)
print("Created synthetic_test_data.csv")
```

## Expected CSV Format

Your CSV files should look like this:

```csv
ts,kw
2024-01-01 00:00:00,236.0
2024-01-01 00:15:00,236.0
2024-01-01 00:30:00,238.4
2024-01-01 00:45:00,247.2
2024-01-01 01:00:00,249.6
...
```

**Requirements:**
- Column 1: Timestamp (named `ts`, `timestamp`, `time`, or `datetime`)
- Column 2: Demand in kW (any numeric column name)
- At least 30 days of data recommended
- 15-minute or hourly intervals

## Files You Can Add Here

- `grocery_ami_data.csv` - Real building data from your notebook
- `synthetic_test_data.csv` - Generated test data
- `building_A.csv`, `building_B.csv` - Multiple building datasets for testing
- Any other AMI interval data you want to analyze

---

**Note:** This folder is included in `.gitignore` to prevent accidentally committing sensitive building data to version control.
