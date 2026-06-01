import streamlit as st
import pandas as pd
import plotly.express as px
from sympy import im
from db_config import engine
from queries import age_group

st.title("🎯 Lead Age Group Analysis")

st.markdown("""
This analysis identifies the dominant age groups among leads. Understanding the age distribution helps the marketing team create targeted campaigns, messaging, and content tailored to the largest audience segments.
""")

df = pd.read_sql(age_group, engine)

# KPIs
col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Largest Age Segment",
        df.loc[df["total_leads"].idxmax(), "age_group"]
    )

with col2:
    st.metric(
        "Highest Share",
        f"{df['percentage_of_leads'].max()}%"
    )

st.divider()

# Chart
fig = px.bar(
    df,
    x="age_group",
    y="total_leads",
    text="percentage_of_leads",
    title="Lead Distribution by Age Group"
)

fig.update_traces(
    texttemplate='%{text}%',
    textposition='outside'
)

fig.update_layout(
    xaxis_title="Age Group",
    yaxis_title="Number of Leads"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# Table
st.subheader("Data Summary")
st.dataframe(df, use_container_width=True)

# Insight
largest_group = df.loc[df["total_leads"].idxmax(), "age_group"]
largest_percent = df["percentage_of_leads"].max()

st.success(
    f"""
    **Business Insight**

    The majority of leads belong to the **{largest_group}** age group,
    accounting for **{largest_percent}%** of all leads.

    Marketing campaigns, creatives, demo content, and communication strategies
    should primarily target this segment to maximize engagement and conversion opportunities.
    """
)

st.markdown("---")

st.markdown("## 🎯 Age Group vs Conversion Analysis")

st.success("""
### Highest Converting Age Segment

• Students aged **21-25 years** account for the largest share of conversions at **51.67%**.

• This age group appears to be the primary target audience for the program, likely due to their strong focus on career growth, skill development, and job opportunities.

• Marketing efforts targeted toward this segment are likely to generate the highest return on investment.
""")

st.info("""
### Secondary Opportunity Segment

• Students aged **16-20 years** contribute **47.78%** of total conversions.

• Although slightly lower than the 21-25 segment, this group still represents a significant portion of successful enrollments.

• These students may be more focused on building skills early in their academic journey and can be nurtured through long-term engagement campaigns.
""")

st.warning("""
### Underrepresented Segment

• Students aged **31+** account for only **0.56%** of conversions.

• This suggests that the current offering, messaging, or marketing channels may not strongly resonate with older learners.

• Given the extremely low conversion contribution, this segment currently represents a lower-priority target audience.
""")

st.markdown("""
###  Recommended Actions

- Prioritize marketing campaigns targeting students aged 21-25 years.

- Develop career-focused messaging, placement success stories, and salary-growth narratives for this segment.

- Continue nurturing the 16-20 age group through educational content and early career guidance.

- Evaluate whether marketing spend directed toward older age groups is generating sufficient returns.

- Build age-specific campaigns instead of using a single communication strategy for all students.
""")

st.success("""
### 💰 Business Impact

Nearly all conversions come from students aged between 16 and 25 years.

Focusing acquisition and nurturing efforts on these high-converting age groups can improve marketing efficiency, increase enrollments, and reduce spending on low-return audience segments.
""")