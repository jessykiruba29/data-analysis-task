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

st.markdown("---")

st.markdown("## 🎥 Demo Engagement vs Conversion Analysis")

st.info("""
### Key Findings

• Students who watched between **51% and 75%** of the demo achieved the highest conversion rate at **37.93%**.

• Surprisingly, students who watched **76% to 100%** of the demo converted at only **29.63%**, which is lower than the 51-75% segment.

• Students in the 0-25% and 26-50% buckets showed similar conversion rates of approximately **31%**, suggesting that even partially engaged students can still convert when followed up effectively.

• The difference in conversion rates across buckets is relatively small, indicating that demo watch percentage alone is not the sole factor driving conversions.
""")

st.warning("""
### Unexpected Observation

• Higher demo completion does not automatically translate into higher enrollment.

• The 76-100% bucket contains students who were highly engaged but still did not convert at the highest rate.

• This suggests that factors beyond demo engagement—such as pricing concerns, counselor follow-up quality, affordability, or preference for offline learning—may be influencing final enrollment decisions.
""")

st.error("""
### Potential Revenue Leakage

• The most concerning group is the students who watched more than 75% of the demo but did not convert.

• These students have already invested significant time in understanding the program and represent high-intent leads.

• Losing such students indicates that the business may be failing to address objections after generating interest.

• Marketing costs have already been incurred for these students, making them one of the most valuable recovery opportunities.
""")

st.success("""
### Recommended Actions

- Introduce special follow-up campaigns.

- Strengthen counselor follow-up for highly engaged students within 24 hours of demo completion.

- Review pricing, financing, and course format objections among high-engagement leads.
""")

st.markdown("""
### 💰 Business Impact

Students who watch more than half of the demo demonstrate clear interest in the program.

The business should focus less on acquiring additional leads and more on recovering highly engaged students who fail to convert, as these represent the lowest-cost opportunity for increasing enrollments and improving marketing ROI.
""")

