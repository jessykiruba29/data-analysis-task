import streamlit as st

st.set_page_config(
    page_title="Student Lead Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>

/* Main Title */
.dashboard-title {
    font-size: 3.5rem;
    font-weight: 800;
    text-align: center;
    background: linear-gradient(90deg, #4F46E5, #06B6D4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.2rem;
}

/* Subtitle */
.dashboard-subtitle {
    text-align: center;
    font-size: 1.1rem;
    color: #A1A1AA;
    margin-bottom: 3rem;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #111827;
}

[data-testid="stSidebar"] .st-emotion-cache-16txtl3 {
    padding-top: 1rem;
}

/* Sidebar Header */
.sidebar-title {
    font-size: 1.4rem;
    font-weight: 700;
    color: #60A5FA;
    text-align: center;
    margin-bottom: 1rem;
}

</style>
""", unsafe_allow_html=True)

# Main Page
st.markdown(
    '<div class="dashboard-title">Student Lead Analytics Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="dashboard-subtitle">Business Intelligence & Conversion Funnel Analysis</div>',
    unsafe_allow_html=True
)



st.sidebar.success("Select an analysis page")