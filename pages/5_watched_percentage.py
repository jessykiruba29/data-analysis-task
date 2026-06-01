import streamlit as st
import pandas as pd
import plotly.express as px
from db_config import engine
from queries import watched_percentage

st.title("⏱️ Demo Watch Time vs Conversion Analysis")

# Load data
df = pd.read_sql(watched_percentage, engine)

# Display raw data
st.dataframe(df)

# Bar chart: Watch bucket vs conversion rate
fig = px.bar(
    df,
    x="watch_bucket",
    y="conversion_rate",
    text="conversion_rate",
    color="watch_bucket",
    title="Conversion Rate by Demo Watch Percentage",
    labels={
        "watch_bucket": "Demo Watch Percentage",
        "conversion_rate": "Conversion Rate (%)"
    }
)

fig.update_traces(
    texttemplate='%{text:.1f}%',
    textposition='outside'
)
fig.update_layout(
    yaxis_range=[0, max(df['conversion_rate']) * 1.2],
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

# Pie chart: Distribution of total students across watch buckets
fig2 = px.pie(
    df,
    names="watch_bucket",
    values="total_students",
    title="Distribution of Students by Demo Watch Completion",
    color_discrete_sequence=px.colors.sequential.Blues_r
)

fig2.update_traces(
    textposition='inside',
    textinfo='percent+label'
)

st.plotly_chart(fig2, use_container_width=True)

# Optional: Add a third chart for volume vs conversion comparison
col1, col2 = st.columns(2)

with col1:
    fig3 = px.bar(
        df,
        x="watch_bucket",
        y="total_students",
        text="total_students",
        color="watch_bucket",
        title="Number of Students per Watch Bucket",
        labels={
            "watch_bucket": "Demo Watch Percentage",
            "total_students": "Number of Students"
        }
    )
    fig3.update_traces(textposition='outside')
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    fig4 = px.bar(
        df,
        x="watch_bucket",
        y="converted_students",
        text="converted_students",
        color="watch_bucket",
        title="Number of Conversions per Watch Bucket",
        labels={
            "watch_bucket": "Demo Watch Percentage",
            "converted_students": "Number of Conversions"
        }
    )
    fig4.update_traces(textposition='outside')
    st.plotly_chart(fig4, use_container_width=True)