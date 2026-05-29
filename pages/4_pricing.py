import streamlit as st
import pandas as pd
import plotly.express as px
from db_config import engine
from queries import pricing


st.title("Pricing and sales strategy analysis")
df=pd.read_sql(pricing, engine)

st.dataframe(df)
fig = px.bar(
    df,
    x="current_education",
    y="drop_percent",
    text="drop_percent",
    color="current_education",
    title="Affordability-Based Drop-off Percentage by Education"
)

st.plotly_chart(fig, use_container_width=True)


# Price issue count chart
fig2 = px.pie(
    df,
    names="current_education",
    values="price_issue",
    title="Contribution to Total Pricing-Related Drop-offs"
)

st.plotly_chart(fig2, use_container_width=True)
