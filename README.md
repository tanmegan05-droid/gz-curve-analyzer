# GZ Curve Analyzer - MV Del Monte

A Streamlit-based web application for analyzing and visualizing the statical stability curve (GZ curve) for MV Del Monte. This interactive tool allows users to calculate the vessel's stability characteristics based on draft and vertical center of gravity (KG) inputs.

## Features

- **Interactive Input Controls:**
  - Draft slider (2.0m - 14.0m)
  - KG number input field (5.0m - 15.0m)

- **Automatic Calculations:**
  - Displacement interpolation from hydrostatic data
  - GZ curve generation using KN curve data
  - Maximum GZ and corresponding angle identification

- **Visual Output:**
  - Line graph showing the GZ curve (heel angle vs. righting arm)
  - Data points table with heel angles, KN, and GZ values
  - Key metrics display (displacement, draft, KG, max GZ)

- **Pre-loaded Data:**
  - Hydrostatic data (draft vs. displacement)
  - KN curve data for multiple displacements and heel angles

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Step 1: Clone the Repository

```bash
git clone https://github.com/tanmegan05-droid/gz-curve-analyzer.git
cd gz-curve-analyzer
```

### Step 2: Create a Virtual Environment (Recommended)

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

## Running the Application Locally

Once you have installed the dependencies, run the application using:

```bash
streamlit run app.py
```

The application will automatically open in your default web browser. If it doesn't, navigate to the URL shown in the terminal (typically `http://localhost:8501`).

## Usage Instructions

1. **Set the Mean Draft:**
   - Use the slider in the sidebar to select the vessel's draft (2.0m to 14.0m)
   
2. **Enter KG Value:**
   - Input the vertical center of gravity in the number field (5.0m to 15.0m)
   - Default value is 8.5m

3. **View Results:**
   - The GZ curve will be automatically calculated and displayed
   - Check the calculated displacement and maximum GZ values
   - Review the data points table for detailed angle-by-angle values

4. **Explore Additional Information:**
   - Expand "Hydrostatic Data Reference" to view the underlying draft-displacement data
   - Expand "About GZ Curve" to learn about the calculation methodology

## Deployment

### Deploy to Streamlit Cloud

1. Push your code to a GitHub repository
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Sign in with your GitHub account
4. Click "New app"
5. Select your repository, branch, and `app.py` as the main file
6. Click "Deploy"

### Deploy to Other Platforms

The application can also be deployed to other platforms that support Python web applications:

- **Heroku:** Create a `Procfile` with: `web: streamlit run app.py --server.port=$PORT`
- **AWS/GCP/Azure:** Use their respective Python web app hosting services
- **Docker:** Create a Dockerfile with Streamlit installation

## Technical Details

### GZ Calculation Formula

```
GZ = KN - KG × sin(θ)
```

Where:
- **GZ** = Righting arm (meters)
- **KN** = Cross-curve of stability value (meters)
- **KG** = Vertical center of gravity (meters)
- **θ** = Heel angle (degrees)

### Data Interpolation

The application uses linear interpolation (via SciPy) to:
- Calculate displacement for any draft within the range
- Determine KN values for any displacement at all heel angles

## Project Structure

```
gz-curve-analyzer/
│
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
└── README.md             # Project documentation
```

## Dependencies

- **streamlit**: Web application framework
- **numpy**: Numerical computations
- **pandas**: Data manipulation and display
- **scipy**: Scientific interpolation functions
- **matplotlib**: Graph plotting and visualization

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Contact

For questions or support, please open an issue in the GitHub repository.

## Acknowledgments

This tool is designed for the MV Del Monte vessel and uses standard naval architecture stability analysis principles.
