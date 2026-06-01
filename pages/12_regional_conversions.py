import streamlit as st
import pandas as pd
import plotly.express as px
from db_config import engine
from queries import regional_conversions

st.title("🌍 City-wise Conversion Analysis")

st.markdown("""
This analysis evaluates how effectively leads from different cities are converted into enrolled students.

The objective is to identify high-performing regions where marketing and sales efforts are yielding strong results, as well as cities that may require a different engagement strategy.
""")



df = pd.read_sql(regional_conversions, engine)

# KPIs
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Best Performing City",
        df.iloc[0]["current_city"]
    )

with col2:
    st.metric(
        "Highest Conversion Rate",
        f"{df['conversion_rate'].max()}%"
    )

with col3:
    st.metric(
        "Cities Analyzed",
        len(df)
    )

st.divider()

# Conversion Rate Chart
fig = px.bar(
    df,
    x="current_city",
    y="conversion_rate",
    text="conversion_rate",
    title="City-wise Conversion Rate (%)"
)

fig.update_traces(
    texttemplate="%{text}%",
    textposition="outside"
)

fig.update_layout(
    xaxis_title="City",
    yaxis_title="Conversion Rate (%)"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# Detailed Table
st.subheader("City Conversion Summary")
st.dataframe(df, use_container_width=True)

# Insights
best_city = df.iloc[0]["current_city"]
best_rate = df.iloc[0]["conversion_rate"]

st.success(f"""
### Key Business Insight

**{best_city}** has the highest conversion rate at **{best_rate}%**, making it the most effective market among the analyzed cities.

Cities with higher conversion rates represent strong opportunities for increased marketing investment, localized campaigns, and targeted sales efforts. Conversely, cities with lower conversion rates may require improvements in lead qualification, messaging, or sales engagement strategies.
""")