import streamlit as st
import pandas as pd
import plotly.express as px
from sympy import im
from db_config import engine
from queries import age_group

st.title("🎯 Lead Age Group Analysis")

st.markdown("""
This analysis identifies the dominant age groups among leads. Understanding the age distribution helps the marketing team create targeted campaigns, messaging, and content tailored to the largest audience segments.
""")

df = pd.read_sql(age_group, engine)

# KPIs
col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Largest Age Segment",
        df.loc[df["total_leads"].idxmax(), "age_group"]
    )

with col2:
    st.metric(
        "Highest Share",
        f"{df['percentage_of_leads'].max()}%"
    )

st.divider()

# Chart
fig = px.bar(
    df,
    x="age_group",
    y="total_leads",
    text="percentage_of_leads",
    title="Lead Distribution by Age Group"
)

fig.update_traces(
    texttemplate='%{text}%',
    textposition='outside'
)

fig.update_layout(
    xaxis_title="Age Group",
    yaxis_title="Number of Leads"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# Table
st.subheader("Data Summary")
st.dataframe(df, use_container_width=True)

# Insight
largest_group = df.loc[df["total_leads"].idxmax(), "age_group"]
largest_percent = df["percentage_of_leads"].max()

st.success(
    f"""
    **Business Insight**

    The majority of leads belong to the **{largest_group}** age group,
    accounting for **{largest_percent}%** of all leads.

    Marketing campaigns, creatives, demo content, and communication strategies
    should primarily target this segment to maximize engagement and conversion opportunities.
    """
)