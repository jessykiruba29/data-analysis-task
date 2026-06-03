import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import text

from db_config import engine
from queries import regional_conversions

st.title("🌍 City-wise Conversion Analysis")

st.markdown("""
This analysis evaluates how effectively leads from different cities are converted into enrolled students.
The objective is to identify high-performing regions where marketing and sales efforts are yielding strong results, as well as cities that may require a different engagement strategy.
""")

df = pd.read_sql(text(regional_conversions), engine)


st.dataframe(
    df,
    use_container_width=True
)

st.divider()


# =====================================
# KPI SECTION
# =====================================

best_city = df.loc[df["conversion_rate"].idxmax(), "current_city"]
best_rate = df["conversion_rate"].max()

total_leads = df["total_leads"].sum()
total_converted = df["converted_students"].sum()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "🏆 Best City",
        best_city
    )

with col2:
    st.metric(
        "📈 Highest Conversion",
        f"{best_rate}%"
    )

with col3:
    st.metric(
        "🎯 Total Conversions",
        total_converted
    )

with col4:
    st.metric(
        "🌍 Cities Analyzed",
        len(df)
    )

st.divider()

# =====================================
# CHART 1
# CONVERSION RATE
# =====================================

fig1 = px.bar(
    df,
    x="current_city",
    y="conversion_rate",
    color="conversion_rate",
    text="conversion_rate",
    title="City-wise Conversion Rate Ranking"
)

fig1.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig1.update_layout(
    xaxis_title="City",
    yaxis_title="Conversion Rate (%)",
    height=500
)

st.plotly_chart(fig1, use_container_width=True)

# =====================================
# CHART 2
# LEADS VS CONVERSIONS
# =====================================

comparison_df = df.melt(
    id_vars="current_city",
    value_vars=[
        "total_leads",
        "converted_students"
    ],
    var_name="Metric",
    value_name="Count"
)

fig2 = px.bar(
    comparison_df,
    x="current_city",
    y="Count",
    color="Metric",
    barmode="group",
    title="Total Leads vs Converted Students"
)

fig2.update_layout(
    height=500
)

st.plotly_chart(fig2, use_container_width=True)




# =====================================
# INSIGHTS
# =====================================

st.markdown("## 💡 Business Insights")

st.success("""
### Top Performing Cities

• Bengaluru achieved the highest conversion rate at **29.41%**, converting **15 out of 51 leads**.

• Visakhapatnam also delivered strong results with **15 successful conversions** and a conversion rate of **19.74%**.

• These cities demonstrate the strongest ability to convert acquired leads into enrolled students.
""")

st.info("""
### Market Performance Comparison

• Hyderabad generated the highest number of leads (**77**) but achieved a conversion rate of only **16.88%**.

• Bengaluru generated fewer leads but converted them significantly more effectively.

• This suggests that conversion quality matters more than lead volume alone.
""")

st.warning("""
### Underperforming Regions

• Mumbai recorded the lowest conversion rate at **10.42%**, converting only **5 out of 48 leads**.

• Kochi achieved only **13.43%** conversion despite generating a healthy lead volume.

• These markets require further investigation into counselor performance, demo engagement, affordability concerns, and student intent.
""")

st.error("""
### Revenue Leakage

• Hyderabad and Mumbai generated substantial lead volumes but failed to convert a proportional number of students.

• Marketing investment is already being made to acquire these leads.

• Improving conversion efficiency in these cities can increase revenue without increasing acquisition costs.

• Lost conversions in these markets represent the largest untapped revenue opportunity.
""")

st.markdown("""
### 🚀 Recommended Actions

✅ Study Bengaluru's sales and counseling process and replicate successful practices across other cities.

✅ Conduct focused reviews for Mumbai and Kochi to identify conversion bottlenecks.

✅ Compare demo engagement, affordability concerns, and sales effectiveness across regions.

✅ Allocate future marketing budgets based on conversion efficiency rather than lead volume alone.

✅ Develop city-specific enrollment strategies instead of a single national approach.
""")

st.success("""
### 💰 Business Impact

Bengaluru demonstrates that strong conversion performance is achievable with the current lead generation model.

Rather than focusing solely on acquiring more leads, improving conversion rates in Hyderabad, Mumbai, and Kochi can significantly increase enrollments while keeping acquisition costs unchanged.

Even a small improvement in conversion efficiency across lower-performing cities could generate meaningful additional revenue.
""")