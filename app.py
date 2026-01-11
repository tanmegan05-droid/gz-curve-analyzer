"""
GZ Curve Analyzer for MV Del Monte
A Streamlit web application to calculate and visualize the statical stability curve (GZ curve)
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

# Corrected Hydrostatic Data for MV Del Monte
# Formula: Displacement = 258.73*T² + 1982.54*T + 5000
HYDROSTATIC_DATA = {
    2.0: 10000,
    3.0: 13276,
    4.0: 17070,
    5.0: 21381,
    6.0: 26210,
    7.0: 31556,
    8.0: 37419,
    9.0: 43800,
    10.0: 50698,
    11.0: 58114,
    12.0: 66048,
    13.0: 74498,
    14.0: 83467
}

def calculate_displacement(draft):
    """
    Calculate displacement for a given draft using quadratic interpolation.
    Formula: D = 258.73*T² + 1982.54*T + 5000
    """
    return 258.73 * draft**2 + 1982.54 * draft + 5000

def calculate_gz(draft, kg, heel_angle):
    """
    Calculate GZ (righting lever) for given parameters.
    
    GZ = (GM) * sin(heel_angle) for small angles
    For larger angles, more complex calculations would be needed.
    
    Parameters:
    - draft: vessel draft in meters
    - kg: height of center of gravity above keel in meters
    - heel_angle: heel angle in degrees
    
    Returns:
    - GZ value in meters
    """
    # Get displacement for the draft
    displacement = calculate_displacement(draft)
    
    # Estimate KB (center of buoyancy) - typically about 0.52 * draft for typical cargo vessels
    kb = 0.52 * draft
    
    # Estimate BM (metacentric radius) - simplified calculation
    # BM = I / V where I is second moment of area, V is volume
    # For a typical cargo vessel: BM ≈ (draft^2) / 2
    bm = (draft ** 2) / 2
    
    # Calculate KM (height of metacenter above keel)
    km = kb + bm
    
    # Calculate GM (metacentric height)
    gm = km - kg
    
    # Convert heel angle to radians
    heel_rad = math.radians(heel_angle)
    
    # Calculate GZ (simplified for small angles)
    # For more accuracy, this would need to account for the actual hull form
    if abs(heel_angle) <= 15:
        gz = gm * math.sin(heel_rad)
    else:
        # For larger angles, use a more complex approximation
        gz = gm * math.sin(heel_rad) - 0.5 * (draft / 10) * math.sin(heel_rad)**2 * heel_angle / 15
    
    return gz, gm

def main():
    st.set_page_config(page_title="GZ Curve Analyzer - MV Del Monte", layout="wide")
    
    st.title("🚢 GZ Curve Analyzer for MV Del Monte")
    st.markdown("Calculate and visualize the statical stability curve (GZ curve)")
    
    # Sidebar for inputs
    st.sidebar.header("Vessel Parameters")
    
    draft = st.sidebar.slider(
        "Draft (m)",
        min_value=2.0,
        max_value=14.0,
        value=10.0,
        step=0.5,
        help="Select the vessel's draft"
    )
    
    kg = st.sidebar.number_input(
        "KG - Height of Center of Gravity (m)",
        min_value=0.0,
        max_value=20.0,
        value=8.0,
        step=0.5,
        help="Enter the height of center of gravity above keel"
    )
    
    # Display hydrostatic data
    st.header("📊 Corrected Hydrostatic Data")
    st.markdown("**Draft vs. Displacement for MV Del Monte**")
    
    # Create DataFrame for hydrostatic data
    hydro_df = pd.DataFrame(list(HYDROSTATIC_DATA.items()), columns=['Draft (m)', 'Displacement (tonnes)'])
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.dataframe(hydro_df, hide_index=True, width='stretch')
        
        # Highlight the current draft
        current_displacement = calculate_displacement(draft)
        st.metric(
            label=f"Displacement at {draft}m draft",
            value=f"{current_displacement:,.0f} tonnes"
        )
    
    with col2:
        # Plot hydrostatic curve
        fig1, ax1 = plt.subplots(figsize=(8, 6))
        ax1.plot(hydro_df['Draft (m)'], hydro_df['Displacement (tonnes)'], 'b-', linewidth=2, marker='o')
        ax1.axvline(x=draft, color='r', linestyle='--', label=f'Current Draft: {draft}m')
        ax1.axhline(y=current_displacement, color='r', linestyle='--', alpha=0.5)
        ax1.set_xlabel('Draft (m)', fontsize=12)
        ax1.set_ylabel('Displacement (tonnes)', fontsize=12)
        ax1.set_title('Hydrostatic Curve - Draft vs Displacement', fontsize=14, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        st.pyplot(fig1)
    
    # GZ Curve Calculation
    st.header("📈 GZ Curve Analysis")
    
    # Calculate GZ for various heel angles
    heel_angles = list(range(0, 91, 5))  # 0 to 90 degrees in 5-degree increments
    gz_values = []
    
    for angle in heel_angles:
        gz, gm = calculate_gz(draft, kg, angle)
        gz_values.append(gz)
    
    # Get GM for display
    _, gm = calculate_gz(draft, kg, 0)
    
    # Display GM
    st.metric(
        label="GM - Metacentric Height",
        value=f"{gm:.3f} m",
        help="Positive GM indicates initial stability"
    )
    
    if gm > 0:
        st.success("✅ Vessel has positive initial stability")
    else:
        st.error("⚠️ Warning: Negative GM - Vessel is unstable!")
    
    # Plot GZ curve
    fig2, ax2 = plt.subplots(figsize=(12, 6))
    ax2.plot(heel_angles, gz_values, 'g-', linewidth=2, marker='o', markersize=4)
    ax2.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
    ax2.axvline(x=0, color='k', linestyle='-', linewidth=0.5)
    ax2.set_xlabel('Heel Angle (degrees)', fontsize=12)
    ax2.set_ylabel('GZ - Righting Lever (m)', fontsize=12)
    ax2.set_title('GZ Curve - Statical Stability Curve', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(0, 90)
    
    # Find and mark maximum GZ
    max_gz = max(gz_values)
    max_gz_angle = heel_angles[gz_values.index(max_gz)]
    ax2.plot(max_gz_angle, max_gz, 'r*', markersize=15, label=f'Max GZ: {max_gz:.3f}m at {max_gz_angle}°')
    ax2.legend()
    
    st.pyplot(fig2)
    
    # Display GZ values table
    st.subheader("GZ Values at Different Heel Angles")
    gz_df = pd.DataFrame({
        'Heel Angle (°)': heel_angles,
        'GZ (m)': [f"{gz:.4f}" for gz in gz_values]
    })
    
    # Display in columns for better readability
    col1, col2, col3 = st.columns(3)
    rows_per_col = len(gz_df) // 3 + 1
    
    with col1:
        st.dataframe(gz_df.iloc[:rows_per_col], hide_index=True, width='stretch')
    with col2:
        st.dataframe(gz_df.iloc[rows_per_col:2*rows_per_col], hide_index=True, width='stretch')
    with col3:
        st.dataframe(gz_df.iloc[2*rows_per_col:], hide_index=True, width='stretch')
    
    # Footer with information
    st.markdown("---")
    st.markdown("""
    ### About the Hydrostatic Data
    The hydrostatic data has been corrected based on the accurate displacement values for MV Del Monte.
    - **14.0m draft**: 83,467 tonnes (corrected from 38,100 tonnes)
    - **Formula**: Displacement = 258.73 × Draft² + 1982.54 × Draft + 5000
    
    ### Notes
    - GZ calculations use simplified formulas suitable for preliminary stability analysis
    - For detailed stability assessments, consult the vessel's stability booklet
    - The analysis assumes calm water conditions
    """)

if __name__ == "__main__":
    main()
