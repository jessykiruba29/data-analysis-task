import streamlit as st
import pandas as pd
import plotly.express as px
from db_config import engine
from queries import lead_source



st.title("Lead Source Conversion Analysis")
df=pd.read_sql(lead_source, engine)

st.dataframe(df)


fig = px.bar(
    df,
    x="source",
    y="converted_rate",
    text="converted_rate",
    title="Conversion Rate by Lead Source"
)

st.plotly_chart(fig, use_container_width=True)


fig2 = px.pie(
    df,
    names="source",
    values="successful_conversions",
    title="Contribution to Total Successful Conversions"
)

st.plotly_chart(fig2, use_container_width=True)