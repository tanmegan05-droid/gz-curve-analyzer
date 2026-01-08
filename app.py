import streamlit as st
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(
    page_title="GZ Curve Analyzer - MV Del Monte", 
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "GZ Curve Analyzer for vessel stability analysis"
    }
)

# Custom CSS for better aesthetics
st.markdown("""
<style>
    /* Main title styling */
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1e3a8a;
        text-align: center;
        margin-bottom: 0.5rem;
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Subtitle styling */
    .subtitle {
        font-size: 1.2rem;
        color: #64748b;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 500;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%);
    }
    
    /* Input labels in sidebar */
    [data-testid="stSidebar"] label {
        font-weight: 600;
        color: #334155;
    }
    
    /* Metric card styling */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        color: #1e3a8a;
        font-weight: 700;
    }
    
    /* Headers */
    h2 {
        color: #1e40af;
        font-weight: 600;
        border-bottom: 3px solid #3b82f6;
        padding-bottom: 0.5rem;
        margin-top: 1.5rem;
    }
    
    h3 {
        color: #475569;
        font-weight: 600;
    }
    
    /* Info box styling */
    .stAlert {
        background-color: #dbeafe;
        border-left: 4px solid #3b82f6;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #f1f5f9;
        border-radius: 8px;
        font-weight: 600;
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        border: none;
        box-shadow: 0 4px 6px rgba(59, 130, 246, 0.3);
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        box-shadow: 0 6px 8px rgba(59, 130, 246, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Title and description with custom styling
st.markdown('<h1 class="main-title">⚓ GZ Curve Analyzer for MV Del Monte</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">🌊 Statical Stability Curve Analysis Tool</p>', unsafe_allow_html=True)
st.markdown("---")

# Hydrostatic data: Draft vs Displacement
# Draft in meters, Displacement in tonnes
HYDROSTATIC_DATA = {
    'draft': [2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0],
    'displacement': [10497, 12250, 14100, 16050, 18100, 20250, 22500, 24850, 27300, 29850, 32500, 35250, 38100]
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
st.sidebar.markdown("## 📋 Vessel Data Input")
st.sidebar.markdown("")

# Draft input with number field
draft = st.sidebar.number_input(
    "⚓ Mean Draft (m)",
    min_value=2.0,
    max_value=14.0,
    value=8.0,
    step=0.1,
    help="Enter the mean draft of the vessel"
)

# KG input with number field
kg = st.sidebar.number_input(
    "📏 KG - Vertical Center of Gravity (m)",
    min_value=5.0,
    max_value=15.0,
    value=8.5,
    step=0.1,
    help="Enter the vertical center of gravity"
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 💡 About This Tool")
st.sidebar.info(
    "This tool calculates and visualizes the GZ curve (righting arm curve) "
    "for MV Del Monte based on the input draft and KG values.\n\n"
    "**Features:**\n"
    "- Real-time GZ curve calculation\n"
    "- Interactive visualizations\n"
    "- Comprehensive stability analysis"
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
    
    # Calculate max GZ (or least negative if all values are negative)
    max_gz_idx = np.argmax(gz_values)
    max_gz = gz_values[max_gz_idx]
    max_angle = HEEL_ANGLES[max_gz_idx]
    
    # Warn if max GZ is negative (indicates poor stability)
    if max_gz < 0:
        st.warning(f"⚠️ All GZ values are negative. The vessel has negative stability at this KG ({kg}m). Consider reducing the KG value.")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("## 📈 GZ Curve Visualization")
    
    if displacement is not None:
        # Create the plot with improved styling
        fig, ax = plt.subplots(figsize=(10, 6), facecolor='white')
        
        # Set style
        ax.set_facecolor('#f8fafc')
        
        # Plot the GZ curve with gradient color
        ax.plot(HEEL_ANGLES, gz_values, 
                color='#3b82f6', linewidth=3, 
                marker='o', markersize=6, 
                markerfacecolor='#60a5fa', 
                markeredgecolor='#1e40af',
                markeredgewidth=1.5,
                label='GZ Curve',
                alpha=0.9)
        
        # Zero line
        ax.axhline(y=0, color='#ef4444', linestyle='--', linewidth=2, alpha=0.7, label='Zero Line')
        
        # Grid styling
        ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.8, color='#94a3b8')
        
        # Labels with better styling
        ax.set_xlabel('Heel Angle (degrees)', fontsize=13, fontweight='600', color='#1e293b')
        ax.set_ylabel('GZ - Righting Arm (m)', fontsize=13, fontweight='600', color='#1e293b')
        ax.set_title('Statical Stability Curve (GZ Curve)', 
                     fontsize=15, fontweight='700', color='#1e3a8a', pad=15)
        ax.set_xlim(0, 90)
        
        # Add legend
        ax.legend(loc='best', frameon=True, shadow=True, fancybox=True)
        
        # Add annotation for max GZ with improved styling
        ax.annotate(f'🎯 Max GZ: {max_gz:.3f}m\nat {max_angle}°', 
                    xy=(max_angle, max_gz), 
                    xytext=(max_angle + 15, max_gz + 0.3),
                    arrowprops=dict(arrowstyle='->', color='#dc2626', lw=2, 
                                  connectionstyle='arc3,rad=0.3'),
                    fontsize=11, color='#1e3a8a', fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.7', 
                             facecolor='#fef3c7', 
                             edgecolor='#f59e0b',
                             linewidth=2,
                             alpha=0.95))
        
        # Improve tick styling
        ax.tick_params(colors='#475569', labelsize=10)
        
        # Add border
        for spine in ax.spines.values():
            spine.set_edgecolor('#cbd5e1')
            spine.set_linewidth(1.5)
        
        plt.tight_layout()
        st.pyplot(fig)

with col2:
    st.markdown("## 📊 Calculated Values")
    
    if displacement is not None:
        # Display displacement prominently with custom styling
        st.markdown("""
        <div style='background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); 
                    padding: 1.5rem; border-radius: 12px; 
                    border-left: 5px solid #3b82f6; margin-bottom: 1rem;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            <p style='color: #64748b; font-size: 0.9rem; margin: 0; font-weight: 600;'>🚢 Displacement</p>
            <p style='color: #1e3a8a; font-size: 2rem; margin: 0.3rem 0 0 0; font-weight: 700;'>{:.1f} <span style='font-size: 1.2rem;'>tonnes</span></p>
        </div>
        """.format(displacement), unsafe_allow_html=True)
        
        # Other metrics in a cleaner style
        col2_1, col2_2 = st.columns(2)
        
        with col2_1:
            st.markdown("""
            <div style='background: #f1f5f9; padding: 1rem; border-radius: 8px; 
                        text-align: center; border: 2px solid #cbd5e1;'>
                <p style='color: #64748b; font-size: 0.85rem; margin: 0; font-weight: 600;'>⚓ Draft</p>
                <p style='color: #1e3a8a; font-size: 1.5rem; margin: 0.2rem 0 0 0; font-weight: 700;'>{:.1f} m</p>
            </div>
            """.format(draft), unsafe_allow_html=True)
            
        with col2_2:
            st.markdown("""
            <div style='background: #f1f5f9; padding: 1rem; border-radius: 8px; 
                        text-align: center; border: 2px solid #cbd5e1;'>
                <p style='color: #64748b; font-size: 0.85rem; margin: 0; font-weight: 600;'>📏 KG</p>
                <p style='color: #1e3a8a; font-size: 1.5rem; margin: 0.2rem 0 0 0; font-weight: 700;'>{:.1f} m</p>
            </div>
            """.format(kg), unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Max GZ with special highlight
        max_gz_color = '#10b981' if max_gz > 0 else '#ef4444'
        st.markdown("""
        <div style='background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); 
                    padding: 1.5rem; border-radius: 12px; 
                    border-left: 5px solid #f59e0b;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            <p style='color: #78716c; font-size: 0.9rem; margin: 0; font-weight: 600;'>🎯 Maximum GZ</p>
            <p style='color: {}; font-size: 1.8rem; margin: 0.3rem 0 0 0; font-weight: 700;'>{:.3f} m</p>
            <p style='color: #57534e; font-size: 0.9rem; margin: 0.3rem 0 0 0;'>at {} degrees</p>
        </div>
        """.format(max_gz_color, max_gz, max_angle), unsafe_allow_html=True)

# Data points display
st.markdown("## 📑 GZ Curve Data Points")

if displacement is not None:
    # Create DataFrame for display
    data_df = pd.DataFrame({
        'Heel Angle (°)': HEEL_ANGLES,
        'KN (m)': kn_values,
        'GZ (m)': gz_values
    })
    
    # Display with formatting (using styling for proper numerical preservation)
    st.dataframe(
        data_df.style.format({
            'KN (m)': '{:.3f}',
            'GZ (m)': '{:.3f}'
        }).set_properties(**{
            'background-color': '#f8fafc',
            'color': '#1e293b',
            'border-color': '#cbd5e1'
        }).set_table_styles([
            {'selector': 'th', 'props': [
                ('background-color', '#3b82f6'),
                ('color', 'white'),
                ('font-weight', '600'),
                ('text-align', 'center'),
                ('padding', '12px')
            ]},
            {'selector': 'td', 'props': [
                ('text-align', 'center'),
                ('padding', '10px')
            ]}
        ]),
        use_container_width=True,
        height=400
    )

# Additional information with improved styling
st.markdown("<br>", unsafe_allow_html=True)

col_exp1, col_exp2 = st.columns(2)

with col_exp1:
    with st.expander("📊 Hydrostatic Data Reference", expanded=False):
        hydro_df = pd.DataFrame(HYDROSTATIC_DATA)
        hydro_df.columns = ['Draft (m)', 'Displacement (tonnes)']
        st.dataframe(hydro_df, use_container_width=True)

with col_exp2:
    with st.expander("ℹ️ About GZ Curve", expanded=False):
        st.markdown("""
        ### What is a GZ Curve?
        
        The **GZ curve** (righting arm curve) is fundamental in naval architecture, 
        showing the relationship between heel angle and righting arm (GZ).
        
        ### Calculation Formula
        
        ```
        GZ = KN - KG × sin(θ)
        ```
        
        **Where:**
        - **GZ** = Righting arm (meters)
        - **KN** = Cross-curve of stability (meters)
        - **KG** = Vertical center of gravity (meters)
        - **θ** = Heel angle (degrees)
        
        ### Interpretation
        
        - ✅ **Positive GZ**: Righting moment returns ship upright
        - ⚠️ **Negative GZ**: Capsizing moment
        - 🎯 **Maximum GZ**: Angle of maximum stability
        """)

# Footer with improved styling
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 2rem 0 1rem 0;'>
    <p style='color: #94a3b8; font-size: 0.95rem; margin: 0;'>
        <strong style='color: #475569;'>⚓ GZ Curve Analyzer for MV Del Monte</strong>
    </p>
    <p style='color: #cbd5e1; font-size: 0.85rem; margin: 0.5rem 0 0 0;'>
        🌊 Vessel Stability Analysis Tool | Built with Streamlit
    </p>
</div>
""", unsafe_allow_html=True)
