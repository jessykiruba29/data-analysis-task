import streamlit as st
import pandas as pd
import plotly.express as px
from db_config import engine
from queries import call_analysis

st.title("📞 Follow-Up Calls vs Successful Conversions")


df = pd.read_sql(call_analysis, engine)


st.markdown("""
This analysis evaluates how many follow-up calls are typically required before a student successfully enrolls.
The goal is to understand whether conversions happen quickly or require persistent engagement from the counseling team.
""")


st.dataframe(
    df,
    use_container_width=True
)

st.divider()


# ==================================================
# KPI SECTION
# ==================================================

best_calls = df.loc[
    df["converted_leads"].idxmax(),
    "total_calls"
]

best_conversions = df["converted_leads"].max()

total_conversions = df["converted_leads"].sum()

avg_calls = round(
    (df["total_calls"] * df["converted_leads"]).sum()
    / total_conversions,
    1
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "🏆 Peak Conversion Point",
    f"{best_calls} Calls"
)

col2.metric(
    "🎯 Max Conversions",
    best_conversions
)

col3.metric(
    "📈 Total Conversions",
    total_conversions
)

col4.metric(
    "☎️ Avg Calls to Convert",
    avg_calls
)

st.divider()

# ==================================================
# CHART 1
# ==================================================

fig1 = px.bar(
    df,
    x="total_calls",
    y="converted_leads",
    color="converted_leads",
    text="converted_leads",
    title="Successful Conversions by Number of Follow-Ups"
)

fig1.update_traces(
    textposition="outside"
)

fig1.update_layout(
    xaxis_title="Number of Calls",
    yaxis_title="Converted Students",
    height=500
)

st.plotly_chart(fig1, use_container_width=True)


# ==================================================
# CHART 3
# CONVERSION SHARE
# ==================================================

fig3 = px.pie(
    df,
    names="total_calls",
    values="converted_leads",
    hole=0.55,
    title="Contribution of Each Follow-Up Bucket"
)

st.plotly_chart(fig3, use_container_width=True)





# ==================================================
# INSIGHTS
# ==================================================

st.markdown("## 💡 Business Insights")

st.success("""
### Key Findings

• The largest number of successful enrollments occurred after **11 follow-up calls**, resulting in **33 conversions**.

• Students contacted **9 times** contributed another **21 conversions**, making it the second most productive follow-up bucket.

• Together, the 9-call and 11-call groups account for the majority of all successful enrollments.

• Very few students converted after only 7 or 8 interactions.
""")

st.info("""
### Student Decision-Making Behavior

• Students rarely make enrollment decisions immediately.

• Many prospects require multiple conversations to address affordability concerns, career goals, parental approval, and program comparisons.

• Repeated engagement appears to build trust and confidence before commitment.
""")

st.warning("""
### Business Risk

• Leads that are abandoned after only a few calls may represent lost revenue opportunities.

• The data suggests that many successful enrollments occur much later in the follow-up cycle.

• A short follow-up process may artificially reduce conversion rates.
""")

st.error("""
### Revenue Leakage Opportunity

• Students who eventually converted typically required sustained engagement.

• If counselors stop follow-ups too early, the business risks losing students who could have converted with additional nurturing.

• Lead acquisition costs have already been incurred, making follow-up optimization a high-ROI improvement area.
""")

st.markdown("""
###  Recommended Actions

- Establish a minimum follow-up threshold before marking leads inactive.

- Build automated follow-up schedules and reminders.

- Study high-converting counselors and replicate their engagement patterns.

- Monitor follow-up completion rates as a key sales KPI.

- Introduce lead nurturing workflows for students who remain undecided after initial interactions.
""")

st.success("""
### 💰 Business Impact

This analysis demonstrates that persistence directly influences enrollment outcomes.

Instead of focusing solely on acquiring additional leads, the business can increase revenue by improving follow-up consistency and counselor engagement.

Maximizing conversions from existing leads is significantly more cost-effective than generating new leads, making follow-up optimization a high-impact growth strategy.
""")