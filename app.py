import streamlit as st

st.set_page_config(
    page_title="Student Lead Analytics Dashboard",
    layout="wide"
)

st.title("Student Lead Conversion Analytics Dashboard")

st.markdown("""
EXPLORE THE DATA: Dive into the data to understand student behavior and preferences. Analyze lead sources, regional engagement, and reasons for disinterest to identify patterns and trends.
""")

st.sidebar.success("Select analysis page")