import streamlit as st
import pandas as pd
import plotly.express as px
from db_config import engine
from queries import regional_demo

st.title("Regional Student Engagement Analysis")
df=pd.read_sql(regional_demo, engine)

st.dataframe(df)

fig=px.bar(
    df,
    x="current_city",
    y="avgtime",
    color="language",
    barmode="group",
    text="avgtime",
    title="Average Demo Watch Percentage by City and Language"
)

st.plotly_chart(fig, use_container_width=True)