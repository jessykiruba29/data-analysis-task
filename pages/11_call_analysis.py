import streamlit as st
import pandas as pd
import plotly.express as px
from db_config import engine
from queries import call_analysis

st.title("📞 Follow-Up Calls vs Conversions")

st.markdown("""
This analysis examines how many follow-up calls were required before a student successfully converted.

The objective is to understand whether conversions happen quickly or require sustained engagement from the sales team.
""")


df = pd.read_sql(call_analysis, engine)

# KPI Section
col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Most Common Call Count",
        df.loc[df["converted_leads"].idxmax(), "total_calls"]
    )

with col2:
    st.metric(
        "Maximum Conversions",
        df["converted_leads"].max()
    )

st.divider()

# Chart
fig = px.bar(
    df,
    x="total_calls",
    y="converted_leads",
    text="converted_leads",
    title="Converted Leads by Number of Follow-Up Calls"
)

fig.update_traces(textposition="outside")

fig.update_layout(
    xaxis_title="Number of Calls",
    yaxis_title="Converted Leads",
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# Table
st.subheader("Underlying Data")
st.dataframe(df, use_container_width=True)

# Business Insight
max_calls = df.loc[df["converted_leads"].idxmax(), "total_calls"]
max_conv = df["converted_leads"].max()

st.success(
    f"""
### Key Insight

The highest number of successful conversions (**{max_conv} students**) occurred after **{max_calls} follow-up calls**.

This indicates that students typically require multiple interactions before making an enrollment decision. The sales process appears to benefit from persistent follow-ups rather than relying on early-stage conversions.

**Recommendation:** Establish a structured follow-up strategy and avoid closing leads prematurely, as many successful enrollments occur only after repeated engagement.
"""
)