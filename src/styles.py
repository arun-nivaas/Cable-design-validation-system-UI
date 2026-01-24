import streamlit as st
import json


def load_branding():
    try:
        with open("assets/branding.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "primary_color": "#2563EB",
            "secondary_color": "#3B82F6",
            "background_color": "#FFFFFF",
            "text_color": "#1E293B",
        }


def inject_custom_css():
    branding = load_branding()
    primary_color = branding.get("primary_color", "#2563EB")

    # Minimal CSS for specific elements that need branding tweaks
    # Streamlit's config.toml handles the main theme (bg, primary color, font)

    css = f"""
    <style>
        /* Import Inter font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        html, body, [class*="css"] {{
            font-family: 'Inter', sans-serif;
        }}

        /* Main Background */
        .stApp {{
            background-color: #FFFFFF;
        }}

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {{
            background-color: #F8FAFC;
            border-right: 1px solid #E2E8F0;
        }}
        
        /* Custom styling for the Validate button */
        div.stButton > button:first-child {{
            background: linear-gradient(135deg, {primary_color} 0%, {branding.get("secondary_color", "#3B82F6")} 100%);
            color: white;
            border-radius: 12px;
            height: 3.5em;
            width: 100%;
            font-weight: 600;
            border: none;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
            transition: all 0.3s ease;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            font-size: 0.9rem;
        }}
        div.stButton > button:first-child:hover {{
            box-shadow: 0 8px 20px rgba(37, 99, 235, 0.4);
            transform: translateY(-2px);
            color: white;
        }}
        
        /* Glassmorphism Hero Card */
        .glass-hero {{
            background: linear-gradient(135deg, rgba(37, 99, 235, 0.9), rgba(59, 130, 246, 0.8));
            border-radius: 24px;
            padding: 40px;
            text-align: center;
            color: white;
            box-shadow: 0 20px 40px -10px rgba(37, 99, 235, 0.3);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            margin-bottom: 30px;
            position: relative;
            overflow: hidden;
        }}
        
        /* Shine effect for glass card */
        .glass-hero::before {{
            content: '';
            position: absolute;
            top: 0;
            left: -50%;
            width: 100%;
            height: 100%;
            background: linear-gradient(to right, transparent, rgba(255,255,255,0.2), transparent);
            transform: skewX(-25deg);
            animation: shine 6s infinite;
        }}
        
        @keyframes shine {{
            0% {{ left: -50%; }}
            20% {{ left: 150%; }}
            100% {{ left: 150%; }}
        }}

        .hero-score {{
            font-size: 6rem;
            font-weight: 800;
            line-height: 1;
            margin-bottom: 10px;
            text-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }}
        
        .hero-label {{
            font-size: 1.2rem;
            font-weight: 500;
            opacity: 0.9;
            letter-spacing: 1px;
            text-transform: uppercase;
        }}

        /* Metric Cards */
        .metric-card {{
            background: white;
            border: 1px solid #E2E8F0;
            border-radius: 16px;
            padding: 20px;
            display: flex;
            align-items: center;
            gap: 15px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            transition: transform 0.2s;
        }}
        .metric-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
        }}
        .metric-icon {{
            width: 48px;
            height: 48px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
        }}
        
        /* Input Fields Styling */
        .stSelectbox > div > div {{
            background-color: white;
            border-radius: 10px;
            border: 1px solid #E2E8F0;
        }}
        .stNumberInput > div > div > input {{
            background-color: white;
            border-radius: 10px;
            border: 1px solid #E2E8F0;
        }}
        
        /* Table Styling */
        .stDataFrame {{
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        }}
        
        /* Status Badges */
        .status-badge {{
            padding: 4px 12px;
            border-radius: 9999px;
            font-size: 0.85rem;
            font-weight: 600;
            display: inline-block;
        }}
        .status-pass {{ background-color: #DCFCE7; color: #166534; }}
        .status-fail {{ background-color: #FEE2E2; color: #991B1B; }}
        .status-warn {{ background-color: #FEF3C7; color: #92400E; }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
