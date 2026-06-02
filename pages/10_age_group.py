import streamlit as st
import pandas as pd
import plotly.express as px
from db_config import engine
from queries import age_group

st.title("🎯 Lead Age Group Analysis")

st.markdown("""
This analysis identifies the dominant age groups among leads and evaluates which age segments contribute the most conversions.

Understanding age-based behavior helps the business optimize marketing campaigns, content strategy, counselor engagement, and budget allocation.
""")

# =====================================
# DATA
# =====================================

df = pd.read_sql(age_group, engine)

# Conversion data from analysis
conversion_df = pd.DataFrame({
    "age_group": ["16-20", "21-25", "31+"],
    "conversion_share": [47.78, 51.67, 0.56]
})

# =====================================
# KPI SECTION
# =====================================

largest_group = df.loc[df["total_leads"].idxmax(), "age_group"]
largest_percent = df["percentage_of_leads"].max()

total_leads = df["total_leads"].sum()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "🎯 Largest Age Segment",
        largest_group
    )

with col2:
    st.metric(
        "📈 Highest Share",
        f"{largest_percent}%"
    )

with col3:
    st.metric(
        "👥 Total Leads",
        total_leads
    )

st.divider()

# =====================================
# CHART 1
# LEAD DISTRIBUTION
# =====================================

fig1 = px.bar(
    df,
    x="age_group",
    y="total_leads",
    color="total_leads",
    text="percentage_of_leads",
    title="Lead Distribution Across Age Groups"
)

fig1.update_traces(
    texttemplate="%{text}%",
    textposition="outside"
)

fig1.update_layout(
    xaxis_title="Age Group",
    yaxis_title="Number of Leads",
    height=500
)

st.plotly_chart(fig1, use_container_width=True)

# =====================================
# CHART 2
# AUDIENCE SHARE DONUT
# =====================================

fig2 = px.pie(
    df,
    names="age_group",
    values="total_leads",
    hole=0.55,
    title="Audience Composition by Age Group"
)

fig2.update_layout(height=550)

st.plotly_chart(fig2, use_container_width=True)


# =====================================
# DATA TABLE
# =====================================

st.subheader("📋 Age Group Summary")

st.dataframe(
    df,
    use_container_width=True
)

st.divider()

# =====================================
# INSIGHTS
# =====================================

st.markdown("## 💡 Business Insights")

st.success("""
### Primary Target Audience

• Students aged **21–25 years** contribute **51.67% of all conversions**, making them the most valuable customer segment.

• This group is typically focused on employment opportunities, career advancement, and upskilling initiatives.

• Marketing campaigns targeted at this audience are likely to generate the highest return on investment.
""")

st.info("""
### Strong Secondary Segment

• Students aged **16–20 years** contribute **47.78% of conversions**, making them another highly valuable audience.

• These students are generally preparing for internships, placements, and future career opportunities.

• Early engagement with this segment can create long-term enrollment opportunities and increase lifetime value.
""")

st.warning("""
### Low-Converting Segment

• Students aged **31+** account for only **0.56% of conversions**.

• Current marketing messages and course offerings may not strongly resonate with older learners.

• This audience currently contributes very little to overall enrollment numbers.
""")

st.error("""
### Marketing Efficiency Opportunity

• More than **99% of conversions come from students aged 16–25 years**.

• Marketing budgets distributed across broader demographics may reduce overall efficiency.

• Concentrating acquisition efforts on the 16–25 age range can significantly improve conversion outcomes while lowering acquisition costs.
""")

st.markdown("""
###  Recommended Actions

- Prioritize marketing campaigns targeting students aged **21–25 years**.

- Create career-focused messaging emphasizing placements, salary growth, and industry readiness.

- Continue nurturing the **16–20 age group** through educational content, internships, and skill-building narratives.

- Evaluate whether marketing spend directed toward older age groups is generating sufficient returns.

- Develop age-specific landing pages, ad creatives, and communication strategies rather than using a single campaign approach.
""")

st.success("""
### 💰 Business Impact

The analysis clearly shows that students aged **16–25 years drive virtually all enrollments**.

By aligning marketing investments, counselor efforts, and content strategies around these high-converting segments, the business can increase enrollment efficiency, improve conversion rates, and maximize the return on marketing spend.

Focusing resources on the most responsive audience segments will likely produce better results than increasing overall lead acquisition volume.
""")