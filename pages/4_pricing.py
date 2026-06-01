import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from db_config import engine
from queries import pricing

st.set_page_config(page_title="Education & Price Sensitivity", layout="wide")
st.title("🎓 Education Level vs Price Sensitivity Analysis")

# Load data
df = pd.read_sql(pricing, engine)

# Display raw data
st.dataframe(df)

# Bar chart: Drop percentage by education
fig = px.bar(
    df,
    x="current_education",
    y="drop_percent",
    text="drop_percent",
    color="drop_percent",
    title="Price-Related Drop-off Percentage by Education Level",
    labels={
        "current_education": "Education Level",
        "drop_percent": "Drop-off Due to Price (%)"
    },
    color_continuous_scale="Reds",
    range_color=[0, df['drop_percent'].max() * 1.1]
)

fig.update_traces(
    texttemplate='%{text:.0f}%',
    textposition='outside'
)
fig.update_layout(
    xaxis_tickangle=-45,
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

# Stacked bar: Total leads vs Price issue leads
fig2 = go.Figure()

fig2.add_trace(go.Bar(
    name="No Price Issue",
    x=df["current_education"],
    y=df["totalleads"] - df["price_issue"],
    marker_color="#22C55E",
    text=df["totalleads"] - df["price_issue"],
    textposition="inside"
))

fig2.add_trace(go.Bar(
    name="Price Issue",
    x=df["current_education"],
    y=df["price_issue"],
    marker_color="#EF4444",
    text=df["price_issue"],
    textposition="inside"
))

fig2.update_layout(
    title="Price Sensitivity Breakdown by Education",
    xaxis_title="Education Level",
    yaxis_title="Number of Leads",
    barmode="stack",
    xaxis_tickangle=-45,
    hovermode="x unified"
)

st.plotly_chart(fig2, use_container_width=True)

# Pie chart: Distribution of price issues across education levels
fig3 = px.pie(
    df,
    names="current_education",
    values="price_issue",
    title="Contribution to Total Price-Related Drop-offs by Education",
    color_discrete_sequence=px.colors.qualitative.Set2,
    hole=0.3
)

fig3.update_traces(
    textposition='inside',
    textinfo='percent+label'
)

st.plotly_chart(fig3, use_container_width=True)

# Scatter plot: Total leads vs Price issue percentage
fig4 = px.scatter(
    df,
    x="totalleads",
    y="drop_percent",
    size="price_issue",
    text="current_education",
    title="Lead Volume vs Price Sensitivity",
    labels={
        "totalleads": "Total Leads",
        "drop_percent": "Price-Related Drop %",
        "price_issue": "Price Issue Count"
    },
    color="drop_percent",
    color_continuous_scale="Reds",
    size_max=60
)

fig4.update_traces(
    textposition='top center'
)

st.plotly_chart(fig4, use_container_width=True)

# Key metrics
st.markdown("---")
st.subheader("📊 Key Insights")

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_leads_all = df['totalleads'].sum()
    st.metric("📋 Total Leads Analyzed", f"{total_leads_all:,}")

with col2:
    total_price_issues = df['price_issue'].sum()
    st.metric("💰 Total Price Issues", f"{total_price_issues:,}")

with col3:
    overall_drop_pct = (total_price_issues / total_leads_all * 100) if total_leads_all > 0 else 0
    st.metric("📉 Overall Price Sensitivity", f"{overall_drop_pct:.1f}%")

with col4:
    avg_deal_value = 500  # Adjust as needed
    revenue_loss = total_price_issues * avg_deal_value
    st.metric("💸 Estimated Revenue Loss", f"${revenue_loss:,.0f}")

st.markdown("---")

# Most and least price-sensitive groups
st.subheader("🎯 Target Segment Analysis")

col1, col2 = st.columns(2)

with col1:
    most_sensitive = df.loc[df['drop_percent'].idxmax()]
    st.markdown("#### 🔴 Most Price-Sensitive")
    st.metric(
        most_sensitive['current_education'],
        f"{most_sensitive['drop_percent']:.0f}% drop rate",
        f"{most_sensitive['price_issue']} of {most_sensitive['totalleads']} leads"
    )
    
    # Revenue impact for this segment
    segment_loss = most_sensitive['price_issue'] * avg_deal_value
    st.caption(f"💰 Revenue at risk in this segment: ${segment_loss:,.0f}")

with col2:
    least_sensitive = df.loc[df['drop_percent'].idxmin()]
    st.markdown("#### 🟢 Least Price-Sensitive")
    st.metric(
        least_sensitive['current_education'],
        f"{least_sensitive['drop_percent']:.0f}% drop rate",
        f"{least_sensitive['price_issue']} of {least_sensitive['totalleads']} leads",
        delta_color="inverse"
    )
    
    # Opportunity for this segment
    segment_opportunity = least_sensitive['totalleads'] - least_sensitive['price_issue']
    st.caption(f"💡 Opportunity: {segment_opportunity} leads who didn't cite price")

st.markdown("---")

st.markdown("## 💰 Education vs Pricing Sensitivity Analysis")

st.error("""
### Most Price-Sensitive Student Segments

• Students who are currently Looking for a Job show the highest affordability-related drop-off rate at **55%**.

• More than half of all job-seeking students who dropped out cited pricing as a major concern.

• Degree students are the second most price-sensitive group, with **35%** of students dropping due to affordability issues.

• B.Tech students generated the largest lead volume (**112 students**), but only **23%** dropped due to pricing concerns.

• Intermediate students showed the lowest pricing sensitivity at **16%**.
""")

st.warning("""
### Revenue Leakage Analysis

• The company is losing a significant number of interested students due to affordability concerns rather than lack of interest.

• The most critical segment is job-seeking students, where **53 out of 97 students** dropped because of pricing barriers.

• These students have already demonstrated interest in career growth and are likely to convert if financial barriers are reduced.

• Losing students at this stage means marketing and counselor efforts are not generating maximum return.
""")

st.info("""
### Student Behavior Insights

• Job-seeking students are likely evaluating the course as an investment and may hesitate without confidence in immediate returns.

• B.Tech students appear less affected by pricing, possibly due to stronger parental support or greater awareness of career benefits.

• Degree students represent a middle-ground segment where targeted financial assistance could significantly improve conversion rates.
""")

st.success("""
### Recommended Business Actions

- Introduce EMI and installment payment options specifically for job-seeking students.

- Create placement-focused marketing campaigns highlighting salary growth and career outcomes.

- Offer scholarships, referral discounts, or limited-time financial incentives for highly interested students.

- Train counselors to emphasize ROI and placement success when interacting with price-sensitive segments.

- Create separate nurturing campaigns for affordability-related leads instead of treating them as permanently lost.
""")

st.markdown("""
### 📈 Potential Business Impact

More than half of job-seeking students are being lost due to affordability concerns.

Reducing pricing-related drop-offs within this segment could unlock one of the largest conversion opportunities in the entire enrollment funnel without increasing lead acquisition costs.

This analysis suggests that pricing strategy may have a greater impact on conversions than generating additional leads.
""")