import streamlit as st
import pandas as pd
from src.styles import inject_custom_css, load_branding
from src.api_service import ApiService

# Page Configuration
st.set_page_config(
    page_title="Cable Design Validation System",
    page_icon="🔌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inject Minimal CSS
inject_custom_css()
branding = load_branding()

# Initialize API Service
api_service = ApiService()

# Sidebar - Input Parameters
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2920/2920349.png", width=50)
    st.title("Cable Parameters")
    
    # Input Mode Selection
    input_mode = st.radio(
        "Input Source", 
        ["Manual Entry", "Database/JSON Record", "AI / Semi-Free-Text Input"],
        index=0
    )
    st.markdown("---")
    
    # Initialize defaults for display to prevent scope errors
    standard = "IS 1554-1"
    voltage = "N/A"
    conductor_mat = "N/A"
    csa = 0
    
    request_data = None
    
    if input_mode == "Manual Entry":
        standard = st.selectbox("Standard", ["IS 1554-1"])
        voltage = st.selectbox("Voltage Rating", ["0.6/1 kV", "1.8/3 kV", "3.6/6 kV"])
        
        st.markdown("### Conductor")
        conductor_mat = st.selectbox("Material", ["Cu", "Al"])
        conductor_class = st.selectbox("Class", ["Class 1", "Class 2", "Class 5"])
        csa = st.number_input("CSA (mm²)", value=10.0, step=1.0)
        
        st.markdown("### Insulation")
        insulation_mat = st.selectbox("Material", ["PVC", "XLPE", "EPR"])
        thickness = st.number_input("Thickness (mm)", value=1.0, step=0.1)
        
        request_data = {
            "standard": standard,
            "voltage": voltage,
            "conductor_material": conductor_mat,
            "conductor_class": conductor_class,
            "csa": csa,
            "insulation_material": insulation_mat,
            "insulation_thickness": thickness
        }

    elif input_mode == "Database/JSON Record":
        st.info("Simulate fetching a structured record from a database.")
        default_json = """{
  "standard": "IS 1554-1",
  "voltage": "0.6/1 kV",
  "conductor_material": "Cu",
  "conductor_class": "Class 2",
  "csa": 10,
  "insulation_material": "PVC",
  "insulation_thickness": 1.0
}"""
        json_input = st.text_area("JSON Record", value=default_json, height=250)
        try:
            import json
            request_data = json.loads(json_input)
            # Update display variables from JSON
            standard = request_data.get("standard", standard)
            voltage = request_data.get("voltage", voltage)
            conductor_mat = request_data.get("conductor_material", conductor_mat)
            csa = request_data.get("csa", csa)
        except json.JSONDecodeError:
            st.error("Invalid JSON format")
            request_data = None

    elif input_mode == "AI / Semi-Free-Text Input":
        st.info("Paste a raw cable description or requirement.")
        default_text = "IS 1554-1 cable, 10 sqmm Cu Class 2, PVC insulation 1.0 mm, LV 0.6/1 kV"
        text_input = st.text_area("Description", value=default_text, height=150)
        request_data = text_input

    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("🚀 Run Validation", use_container_width=True):
        if request_data:
            with st.spinner("Analyzing design..."):
                response = api_service.validate_cable_design(request_data)
                st.session_state.validation_result = response
        else:
            st.warning("Please provide valid input parameters.")


# Main Content Area
# Header
st.markdown("""
    <div style='display: flex; align-items: center; gap: 15px; margin-bottom: 20px;'>
        <h1 style='margin: 0; font-size: 2.5rem; font-weight: 800; color: #1E293B;'>AI-Driven Indian Standard Cable Design Validator</h1>
    </div>
""", unsafe_allow_html=True)

# Get Result
result = st.session_state.get("validation_result", None)

if result:
    # 1. Check for Out of Scope
    if result.get("is_out_of_scope", False):
        explanation = result.get("out_of_scope_explanation", "The provided input is outside the supported validation scope.")
        st.error(f"⚠️ Validation Restricted: {explanation}")
        st.stop() # Stop rendering the dashboard

    # 2. Parse Success Response
    # Confidence Score (Handle nested dict or flat value if legacy)
    confidence_data = result.get("confidence", {})
    if isinstance(confidence_data, dict):
        score_val = confidence_data.get("overall", 0)
    else:
        score_val = confidence_data # fallback if simple float
    
    # Convert 0.91 -> 91
    score_pct = int(float(score_val) * 100)
    
    # Hero Section - Glassmorphism Card
    st.markdown(f"""
        <div class="glass-hero">
            <div class="hero-score">{score_pct}%</div>
            <div class="hero-label">Confidence Score</div>
            <div style='margin-top: 15px; font-size: 0.9rem; opacity: 0.8;'>
                Analysis Complete
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Key Metrics Grid
    # Try to get interpreted fields from response, fallback to processing vars
    fields = result.get("fields", {})
    disp_voltage = fields.get("voltage", voltage)
    disp_cond = fields.get("conductor_material", conductor_mat)
    disp_csa = fields.get("csa", csa)
    
    col1, col2, col3 = st.columns(3)

    status = "Pass" if score_pct >= 90 else "Review"
    status_color = "#DCFCE7" if status == "Pass" else "#FEF3C7"
    status_text = "#166534" if status == "Pass" else "#92400E"

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon" style="background-color: {status_color}; color: {status_text};">
                {'✓' if status == 'Pass' else '⚠'}
            </div>
            <div>
                <div style="color: #64748B; font-size: 0.85rem; font-weight: 600; text-transform: uppercase;">Status</div>
                <div style="color: #1E293B; font-size: 1.25rem; font-weight: 700;">{status}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon" style="background-color: #DBEAFE; color: #1E40AF;">
                ⚡
            </div>
            <div>
                <div style="color: #64748B; font-size: 0.85rem; font-weight: 600; text-transform: uppercase;">Voltage</div>
                <div style="color: #1E293B; font-size: 1.25rem; font-weight: 700;">{disp_voltage}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon" style="background-color: #F3E8FF; color: #6B21A8;">
                📏
            </div>
            <div>
                <div style="color: #64748B; font-size: 0.85rem; font-weight: 600; text-transform: uppercase;">Conductor</div>
                <div style="color: #1E293B; font-size: 1.25rem; font-weight: 700;">{disp_cond} / {disp_csa}mm²</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Results Table
    st.markdown("### 📊 Detailed Analysis")
    
    if "error" in result and not isinstance(result["error"], dict):
         st.error(f"Validation Failed: {result['error']}")
    else:
        # Check validation list
        validation_items = result.get("validation", [])
        if validation_items:
            # Map new structure to table
            table_data = []
            for item in validation_items:
                table_data.append({
                    "Component": item.get("field", "Unknown"),
                    "Status": item.get("status", "UNKNOWN").upper(), # Ensure uppercase for styler
                    "Expected": item.get("expected", "-"),
                    "Comment": item.get("comment", "")
                })
                
            df = pd.DataFrame(table_data)
            
            # Use Styler for pill badges
            def style_status(val):
                s = str(val).upper()
                if 'PASS' in s:
                    return 'background-color: #DCFCE7; color: #166534; padding: 4px 12px; border-radius: 99px; font-weight: 600;'
                elif 'FAIL' in s:
                    return 'background-color: #FEE2E2; color: #991B1B; padding: 4px 12px; border-radius: 99px; font-weight: 600;'
                return 'background-color: #FEF3C7; color: #92400E; padding: 4px 12px; border-radius: 99px; font-weight: 600;'

            st.dataframe(
                df.style.map(style_status, subset=['Status']),
                use_container_width=True,
                hide_index=True,
                height=300
            )
            st.caption("**Note:** This system can make mistakes, so please double-check the results.")
        else:
            st.info("No detailed validation steps returned.")
            
else:
    # 3-Step Instruction Flow using Native Streamlit Components
    st.info("👈 Enter parameters in the sidebar and click 'Run Validation' to start.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Create 3 columns for the instruction boxes
    col1, col2, col3 = st.columns(3)
    
    with col1:
        with st.container():
            st.markdown("""
                <div style='text-align: center; padding: 20px; background-color: #EFF6FF; border-radius: 10px; border: 1px solid #BFDBFE;'>
                    <div style='font-size: 40px; margin-bottom: 10px;'>📝</div>
                    <h4 style='color: #1E40AF; margin-bottom: 8px;'>1. Input Parameters</h4>
                    <p style='color: #64748B; font-size: 0.9rem;'>Fill in the cable details in the sidebar.</p>
                </div>
            """, unsafe_allow_html=True)
    
    with col2:
        with st.container():
            st.markdown("""
                <div style='text-align: center; padding: 20px; background-color: #EFF6FF; border-radius: 10px; border: 1px solid #BFDBFE;'>
                    <div style='font-size: 40px; margin-bottom: 10px;'>🚀</div>
                    <h4 style='color: #1E40AF; margin-bottom: 8px;'>2. Run Validation</h4>
                    <p style='color: #64748B; font-size: 0.9rem;'>Click the validation button to process.</p>
                </div>
            """, unsafe_allow_html=True)
    
    with col3:
        with st.container():
            st.markdown("""
                <div style='text-align: center; padding: 20px; background-color: #EFF6FF; border-radius: 10px; border: 1px solid #BFDBFE;'>
                    <div style='font-size: 40px; margin-bottom: 10px;'>📊</div>
                    <h4 style='color: #1E40AF; margin-bottom: 8px;'>3. View Results</h4>
                    <p style='color: #64748B; font-size: 0.9rem;'>Get instant feedback and analysis.</p>
                </div>
            """, unsafe_allow_html=True)

