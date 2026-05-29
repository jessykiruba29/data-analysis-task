import streamlit as st
import pandas as pd
import plotly.express as px
from db_config import engine
from queries import interest

st.title("Stage wise student drop off reasons analysis")
df=pd.read_sql(interest, engine)

st.dataframe(df)

fig = px.bar(
    df,
    x="stage",
    y="total_students",
    color="reason",
    barmode="group",
    text="total_students",
    title="Student Drop-off in each Stage"
)

st.plotly_chart(fig, use_container_width=True)


# Pie chart for overall reasons
overall_df = (
    df.groupby("reason")["total_students"]
    .sum()
    .reset_index()
)

fig2 = px.pie(
    overall_df,
    names="reason",
    values="total_students",
    title="Overall Distribution of Student Drop-off Reasons"
)

st.plotly_chart(fig2, use_container_width=True)
