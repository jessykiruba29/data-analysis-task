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


st.markdown("---")

st.markdown("## 🌍 City-wise Conversion Performance")

st.success("""
### Top Performing Cities

• Bengaluru achieved the highest conversion rate at **29.41%**, converting **15 out of 51 leads**.

• Visakhapatnam also delivered strong results with **15 successful conversions** and a conversion rate of **19.74%**.

• These cities demonstrate the strongest ability to convert acquired leads into enrolled students.
""")

st.info("""
### Market Performance Comparison

• Although Hyderabad generated the highest number of leads (**77**), its conversion rate remained at **16.88%**.

• Visakhapatnam generated a similar number of leads (**76**) but achieved a noticeably higher conversion rate (**19.74%**).

• Bengaluru generated fewer leads than Hyderabad and Visakhapatnam, yet produced the highest conversion efficiency, indicating stronger lead quality or more effective sales engagement.
""")

st.warning("""
### Underperforming Regions

• Mumbai recorded the lowest conversion rate at **10.42%**, converting only **5 out of 48 leads**.

• Kochi also showed relatively weak conversion performance at **13.43%** despite generating a reasonable number of leads.

• These regions may require additional investigation to identify factors affecting enrollment decisions.
""")

st.error("""
### Potential Revenue Leakage

• Hyderabad and Mumbai generated a large number of leads but converted a relatively small percentage of them.

• This suggests that a significant amount of marketing effort and acquisition cost is not translating into enrollments.

• Improving conversion performance in these cities could generate substantial additional revenue without increasing lead acquisition spending.
""")

st.markdown("""
###  Recommended Actions

- Study Bengaluru's sales process and replicate successful practices in other cities.

- Prioritize counselor coaching and conversion optimization efforts in Mumbai and Kochi.

- Investigate whether affordability concerns, demo engagement, or counselor performance differ across cities.

- Allocate future marketing budgets based not only on lead volume but also on conversion efficiency.

- Develop city-specific strategies instead of using a uniform enrollment approach across all regions.
""")

st.success("""
### 💰 Business Impact

Bengaluru demonstrates that strong conversion performance is achievable with the existing lead generation process.

Rather than focusing solely on acquiring more leads, improving conversion rates in lower-performing cities could significantly increase enrollments and maximize the return on marketing investments.

Even a small improvement in Hyderabad, Mumbai, or Kochi could result in a meaningful increase in overall revenue due to their existing lead volumes.
""")