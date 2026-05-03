import streamlit as st
from views.sidebar_view import render_sidebar
from views.home_view import render_home
from views.analysis_view import display_street_analysis
from utils.css_utils import load_custom_css

st.set_page_config(
    page_title="StreetWise - AI Street Scoring",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_custom_css()

# ----------------------
# Sidebar
# ----------------------
with st.sidebar:
    render_sidebar()

# ----------------------
# Main Content
# ----------------------
if st.session_state.get("street_analysis_complete"):
    display_street_analysis()
else:
    render_home()
