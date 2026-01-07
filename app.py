import streamlit as st
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(page_title="GZ Curve Analyzer - MV Del Monte", layout="wide")

# Title and description
st.title("GZ Curve Analyzer for MV Del Monte")
st.markdown("**Statical Stability Curve Analysis Tool**")
st.markdown("---")

# Hydrostatic data: Draft vs Displacement
# Draft in meters, Displacement in tonnes
HYDROSTATIC_DATA = {
    'draft': [2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0],
    'displacement': [1500, 2800, 4200, 5800, 7500, 9400, 11400, 13500, 15700, 18000, 20400, 22900, 25500]
}

# KN curve data: KN values at various displacements and heel angles
# Displacements in tonnes
DISPLACEMENTS = [2000, 5000, 8000, 11000, 14000, 17000, 20000, 23000, 26000]

# Heel angles in degrees
HEEL_ANGLES = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90]

# KN values (in meters) for each displacement at different heel angles
# Rows represent displacements, columns represent heel angles
KN_DATA = np.array([
    [0.00, 0.15, 0.31, 0.48, 0.65, 0.83, 1.01, 1.19, 1.37, 1.55, 1.72, 1.88, 2.03, 2.17, 2.29, 2.39, 2.47, 2.52, 2.55],
    [0.00, 0.18, 0.37, 0.58, 0.79, 1.01, 1.24, 1.47, 1.70, 1.93, 2.15, 2.36, 2.56, 2.75, 2.91, 3.05, 3.17, 3.25, 3.30],
    [0.00, 0.20, 0.42, 0.65, 0.89, 1.14, 1.40, 1.67, 1.94, 2.21, 2.47, 2.72, 2.96, 3.18, 3.38, 3.56, 3.70, 3.81, 3.88],
    [0.00, 0.22, 0.46, 0.71, 0.98, 1.26, 1.55, 1.85, 2.15, 2.45, 2.74, 3.02, 3.29, 3.54, 3.77, 3.97, 4.14, 4.27, 4.36],
    [0.00, 0.24, 0.49, 0.76, 1.05, 1.36, 1.68, 2.01, 2.34, 2.67, 2.99, 3.30, 3.60, 3.87, 4.13, 4.35, 4.54, 4.69, 4.80],
    [0.00, 0.25, 0.52, 0.81, 1.12, 1.45, 1.79, 2.14, 2.50, 2.86, 3.21, 3.55, 3.87, 4.17, 4.45, 4.69, 4.90, 5.07, 5.19],
    [0.00, 0.27, 0.55, 0.85, 1.18, 1.53, 1.89, 2.26, 2.64, 3.02, 3.40, 3.76, 4.11, 4.43, 4.73, 5.00, 5.22, 5.41, 5.54],
    [0.00, 0.28, 0.58, 0.90, 1.24, 1.60, 1.98, 2.37, 2.77, 3.17, 3.56, 3.95, 4.32, 4.66, 4.98, 5.27, 5.51, 5.71, 5.86],
    [0.00, 0.29, 0.60, 0.94, 1.30, 1.68, 2.07, 2.48, 2.89, 3.31, 3.72, 4.12, 4.51, 4.88, 5.22, 5.52, 5.78, 5.99, 6.15]
])


def interpolate_displacement(draft):
    """Interpolate displacement for a given draft."""
    # The slider ensures draft is within bounds, but we add a check for safety
    if draft < min(HYDROSTATIC_DATA['draft']) or draft > max(HYDROSTATIC_DATA['draft']):
        st.error(f"Draft must be between {min(HYDROSTATIC_DATA['draft'])}m and {max(HYDROSTATIC_DATA['draft'])}m")
        return None
    
    f = interp1d(HYDROSTATIC_DATA['draft'], HYDROSTATIC_DATA['displacement'], 
                 kind='linear')
    return float(f(draft))


def interpolate_kn_values(displacement):
    """Interpolate KN values for a given displacement across all heel angles."""
    # Check if displacement is within safe bounds
    if displacement < min(DISPLACEMENTS) or displacement > max(DISPLACEMENTS):
        st.warning(f"Displacement {displacement:.1f} tonnes is outside the KN data range ({min(DISPLACEMENTS)}-{max(DISPLACEMENTS)} tonnes). Results may be less accurate.")
    
    kn_values = []
    for angle_idx in range(len(HEEL_ANGLES)):
        # Get KN values for this angle across all displacements
        kn_at_angle = KN_DATA[:, angle_idx]
        # Interpolate for the given displacement
        # Use bounds_error=False and fill_value with boundary clamping
        f = interp1d(DISPLACEMENTS, kn_at_angle, kind='linear', bounds_error=False, 
                     fill_value=(kn_at_angle[0], kn_at_angle[-1]))
        kn_values.append(float(f(displacement)))
    return np.array(kn_values)


def calculate_gz_curve(kn_values, kg, heel_angles):
    """Calculate GZ values using the formula: GZ = KN - KG * sin(angle)."""
    angles_rad = np.radians(heel_angles)
    gz_values = kn_values - kg * np.sin(angles_rad)
    return gz_values


# Sidebar for inputs
st.sidebar.header("Vessel Data Input")

# Draft input with slider
draft = st.sidebar.slider(
    "Mean Draft (m)",
    min_value=2.0,
    max_value=14.0,
    value=8.0,
    step=0.1,
    help="Select the mean draft of the vessel"
)

# KG input with number field
kg = st.sidebar.number_input(
    "KG - Vertical Center of Gravity (m)",
    min_value=5.0,
    max_value=15.0,
    value=8.5,
    step=0.1,
    help="Enter the vertical center of gravity"
)

st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.info(
    "This tool calculates and visualizes the GZ curve (righting arm curve) "
    "for MV Del Monte based on the input draft and KG values."
)

# Main content area
# Calculate displacement first (before columns)
displacement = interpolate_displacement(draft)

# Initialize variables
kn_values = None
gz_values = None
max_gz = 0
max_angle = 0

# Only proceed if displacement is valid
if displacement is not None:
    # Interpolate KN values for the calculated displacement
    kn_values = interpolate_kn_values(displacement)
    
    # Calculate GZ curve
    gz_values = calculate_gz_curve(kn_values, kg, HEEL_ANGLES)
    
    # Calculate max GZ
    max_gz_idx = np.argmax(gz_values)
    max_gz = gz_values[max_gz_idx]
    max_angle = HEEL_ANGLES[max_gz_idx]

col1, col2 = st.columns([2, 1])

with col1:
    st.header("GZ Curve Visualization")
    
    if displacement is not None:
        # Create the plot
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(HEEL_ANGLES, gz_values, 'b-', linewidth=2, marker='o', markersize=4)
        ax.axhline(y=0, color='r', linestyle='--', linewidth=1, alpha=0.7)
        ax.grid(True, alpha=0.3)
        ax.set_xlabel('Heel Angle (degrees)', fontsize=12, fontweight='bold')
        ax.set_ylabel('GZ - Righting Arm (m)', fontsize=12, fontweight='bold')
        ax.set_title('Statical Stability Curve (GZ Curve)', fontsize=14, fontweight='bold')
        ax.set_xlim(0, 90)
        
        # Add annotation for max GZ
        ax.annotate(f'Max GZ: {max_gz:.3f}m\nat {max_angle}°', 
                    xy=(max_angle, max_gz), 
                    xytext=(max_angle + 10, max_gz),
                    arrowprops=dict(arrowstyle='->', color='red', lw=1.5),
                    fontsize=10, color='red', fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7))
        
        st.pyplot(fig)

with col2:
    st.header("Calculated Values")
    
    if displacement is not None:
        # Display displacement prominently
        st.metric(
            label="Displacement",
            value=f"{displacement:.1f} tonnes",
            help="Interpolated from hydrostatic data"
        )
        
        st.metric(
            label="Draft",
            value=f"{draft:.1f} m"
        )
        
        st.metric(
            label="KG",
            value=f"{kg:.1f} m"
        )
        
        st.metric(
            label="Max GZ",
            value=f"{max_gz:.3f} m",
            delta=f"at {max_angle}°"
        )

# Data points display
st.header("GZ Curve Data Points")

if displacement is not None:
    # Create DataFrame for display
    data_df = pd.DataFrame({
        'Heel Angle (°)': HEEL_ANGLES,
        'KN (m)': kn_values,
        'GZ (m)': gz_values
    })
    
    # Format the DataFrame for better display
    data_df['KN (m)'] = data_df['KN (m)'].map('{:.3f}'.format)
    data_df['GZ (m)'] = data_df['GZ (m)'].map('{:.3f}'.format)
    
    st.dataframe(data_df, use_container_width=True, height=400)

# Additional information
with st.expander("📊 Hydrostatic Data Reference"):
    hydro_df = pd.DataFrame(HYDROSTATIC_DATA)
    hydro_df.columns = ['Draft (m)', 'Displacement (tonnes)']
    st.dataframe(hydro_df, use_container_width=True)

with st.expander("ℹ️ About GZ Curve"):
    st.markdown("""
    ### What is a GZ Curve?
    
    The **GZ curve** (also known as the righting arm curve) is a fundamental tool in naval architecture 
    that represents a ship's stability characteristics. It shows the relationship between the heel angle 
    and the righting arm (GZ).
    
    ### Calculation Method
    
    The GZ value is calculated using the formula:
    
    **GZ = KN - KG × sin(θ)**
    
    Where:
    - **GZ** = Righting arm (meters)
    - **KN** = Cross-curve of stability value (meters)
    - **KG** = Vertical center of gravity (meters)
    - **θ** = Heel angle (degrees)
    
    ### Interpretation
    
    - **Positive GZ**: Ship has a righting moment that will tend to return it to upright
    - **Negative GZ**: Ship has a capsizing moment
    - **Maximum GZ**: Indicates the angle at which the ship has maximum stability
    - **Range of Stability**: The range of angles where GZ is positive
    """)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "GZ Curve Analyzer for MV Del Monte | Vessel Stability Analysis Tool"
    "</div>",
    unsafe_allow_html=True
)
