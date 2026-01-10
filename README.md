# GZ Curve Analyzer for MV Del Monte

A Streamlit web application to calculate and visualize the statical stability curve (GZ curve) for MV Del Monte using corrected hydrostatic data.

## Features

- **Corrected Hydrostatic Data**: Displays accurate draft vs. displacement values for MV Del Monte
- **GZ Curve Visualization**: Calculates and plots the righting lever (GZ) curve for different heel angles
- **Interactive Parameters**: Adjust vessel draft and center of gravity (KG) to see stability changes
- **Stability Metrics**: Shows metacentric height (GM) and maximum GZ values

## Hydrostatic Data

The application uses corrected hydrostatic data with the following key points:

| Draft (m) | Displacement (tonnes) |
|-----------|----------------------|
| 2.0 | 10,000 |
| 3.0 | 13,276 |
| 4.0 | 17,070 |
| 5.0 | 21,381 |
| 6.0 | 26,210 |
| 7.0 | 31,556 |
| 8.0 | 37,419 |
| 9.0 | 43,800 |
| 10.0 | 50,698 |
| 11.0 | 58,114 |
| 12.0 | 66,048 |
| 13.0 | 74,498 |
| 14.0 | 83,467 |

**Note**: The 14.0m draft displacement has been corrected from 38,100 tonnes to **83,467 tonnes** based on accurate vessel specifications.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/tanmegan05-droid/gz-curve-analyzer.git
cd gz-curve-analyzer
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the Streamlit application:
```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

## How to Use

1. **Adjust Draft**: Use the slider in the sidebar to select the vessel's draft (2.0m - 14.0m)
2. **Set KG**: Enter the height of the center of gravity above the keel
3. **View Results**: 
   - See the hydrostatic curve showing displacement vs draft
   - View the GZ curve showing stability at different heel angles
   - Check the GM (metacentric height) for initial stability
   - Review the detailed GZ values table

## Technical Details

The displacement values are calculated using the formula:
```
Displacement (tonnes) = 258.73 × Draft² + 1982.54 × Draft + 5000
```

This quadratic relationship accurately represents the hydrostatic properties of MV Del Monte.

## License

This project is open source and available for educational and professional use.
