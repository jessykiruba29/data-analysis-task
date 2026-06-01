import streamlit as st
import pandas as pd
import plotly.express as px
from db_config import engine
from queries import call_analysis

st.title("📞 Follow-Up Calls vs Conversions")

st.markdown("""
This analysis examines how many follow-up calls were required before a student successfully converted.

The objective is to understand whether conversions happen quickly or require sustained engagement from the sales team.
""")


df = pd.read_sql(call_analysis, engine)

# KPI Section
col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Most Common Call Count",
        df.loc[df["converted_leads"].idxmax(), "total_calls"]
    )

with col2:
    st.metric(
        "Maximum Conversions",
        df["converted_leads"].max()
    )

st.divider()

# Chart
fig = px.bar(
    df,
    x="total_calls",
    y="converted_leads",
    text="converted_leads",
    title="Converted Leads by Number of Follow-Up Calls"
)

fig.update_traces(textposition="outside")

fig.update_layout(
    xaxis_title="Number of Calls",
    yaxis_title="Converted Leads",
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# Table
st.subheader("Underlying Data")
st.dataframe(df, use_container_width=True)

# Business Insight
max_calls = df.loc[df["converted_leads"].idxmax(), "total_calls"]
max_conv = df["converted_leads"].max()

st.success(
    f"""
### Key Insight

The highest number of successful conversions (**{max_conv} students**) occurred after **{max_calls} follow-up calls**.

This indicates that students typically require multiple interactions before making an enrollment decision. The sales process appears to benefit from persistent follow-ups rather than relying on early-stage conversions.

**Recommendation:** Establish a structured follow-up strategy and avoid closing leads prematurely, as many successful enrollments occur only after repeated engagement.
"""
)

st.markdown("---")

st.markdown("## 📞 Follow-Up Calls vs Successful Conversions")

st.success("""
### Key Findings

• The highest number of successful conversions occurred after **11 follow-up calls**, resulting in **33 converted students**.

• Students contacted **9 times** contributed the second-highest number of conversions with **21 successful enrollments**.

• Very few students converted after only 7 or 8 calls, suggesting that early follow-ups alone are often insufficient to secure enrollment.

• The data indicates that successful conversions frequently require sustained engagement rather than a small number of interactions.
""")

st.info("""
### Student Behavior Insights

• Students may require multiple interactions before making an enrollment decision due to pricing concerns, family discussions, career evaluation, or comparison with alternative options.

• Conversion appears to improve significantly after repeated counselor engagement.

• This suggests that persistence and consistent follow-up play a critical role in the enrollment process.
""")

st.warning("""
### Common Mistake to Avoid

• Counselors may be tempted to stop pursuing leads after only a few unsuccessful attempts.

• The data shows that most successful enrollments occur much later in the follow-up cycle.

• Prematurely abandoning leads could result in losing students who may have converted with additional engagement.
""")

st.markdown("""
###  Recommended Actions

- Establish a structured follow-up process with a minimum outreach threshold.

- Encourage counselors to continue nurturing interested students beyond the initial few calls.

- Analyze the quality and timing of follow-ups performed by high-converting counselors.

- Use automated reminders to ensure follow-up schedules are maintained consistently.

- Monitor lead drop-off after each follow-up stage to identify optimal engagement strategies.
""")

st.success("""
### 💰 Business Impact

The analysis suggests that persistence directly contributes to successful enrollments.

Rather than increasing marketing spend to acquire more leads, the business may achieve better results by improving counselor follow-up consistency and ensuring promising leads are nurtured through multiple touchpoints.

This can increase conversions while maximizing the value of already acquired leads.
""")