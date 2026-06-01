import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from db_config import engine
from queries import lead_source

st.set_page_config(page_title="Lead Source Analysis", layout="wide")
st.title("📊 Lead Source Conversion Analysis")

# Load data
df = pd.read_sql(lead_source, engine)

# Display raw data
st.dataframe(df)

# Bar chart: Conversion rate by lead source
fig = px.bar(
    df,
    x="source",
    y="converted_rate",
    text="converted_rate",
    color="converted_rate",
    title="Conversion Rate by Lead Source",
    labels={
        "source": "Lead Source",
        "converted_rate": "Conversion Rate (%)"
    },
    color_continuous_scale="Viridis"
)

fig.update_traces(
    texttemplate='%{text:.1f}%',
    textposition='outside'
)
fig.update_layout(
    xaxis_tickangle=-45,
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

# Pie chart: Contribution to total conversions
fig2 = px.pie(
    df,
    names="source",
    values="successful_conversions",
    title="Contribution to Total Successful Conversions",
    color_discrete_sequence=px.colors.qualitative.Set2,
    hole=0.3
)

fig2.update_traces(
    textposition='inside',
    textinfo='percent+label'
)

st.plotly_chart(fig2, use_container_width=True)

# Additional valuable charts
st.markdown("---")

# Scatter plot: Volume vs Conversion Rate
fig3 = px.scatter(
    df,
    x="totalleads",
    y="converted_rate",
    size="successful_conversions",
    text="source",
    title="Lead Volume vs Conversion Rate by Source",
    labels={
        "totalleads": "Total Leads Received",
        "converted_rate": "Conversion Rate (%)",
        "successful_conversions": "Conversions"
    },
    color="converted_rate",
    color_continuous_scale="Viridis"
)

fig3.update_traces(
    textposition='top center'
)

st.plotly_chart(fig3, use_container_width=True)

# Bar chart: Total leads by source
fig4 = px.bar(
    df,
    x="source",
    y="totalleads",
    text="totalleads",
    color="totalleads",
    title="Total Leads by Source",
    labels={
        "source": "Lead Source",
        "totalleads": "Number of Leads"
    },
    color_continuous_scale="Blues"
)

fig4.update_traces(
    textposition='outside'
)
fig4.update_layout(
    xaxis_tickangle=-45,
    showlegend=False
)

st.plotly_chart(fig4, use_container_width=True)

# Key metrics row
st.markdown("---")
st.subheader("📊 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_sources = len(df)
    st.metric("📡 Total Sources", total_sources)

with col2:
    total_leads_all = df['totalleads'].sum()
    st.metric("📋 Total Leads", f"{total_leads_all:,}")

with col3:
    total_conversions_all = df['successful_conversions'].sum()
    st.metric("🎯 Total Conversions", f"{total_conversions_all:,}")

with col4:
    overall_cr = (total_conversions_all / total_leads_all * 100) if total_leads_all > 0 else 0
    st.metric("📈 Overall Conversion Rate", f"{overall_cr:.1f}%")

st.markdown("---")

# Source performance analysis
st.subheader("⭐ Source Performance Analysis")

# Best and worst sources
col1, col2 = st.columns(2)

with col1:
    best_idx = df['converted_rate'].idxmax()
    best_source = df.loc[best_idx]
    st.markdown("#### 🏆 Best Performing Source")
    st.metric(
        best_source['source'],
        f"{best_source['converted_rate']:.1f}% conversion",
        f"{best_source['successful_conversions']} conversions from {best_source['totalleads']} leads"
    )
    
    # Calculate efficiency
    if best_source['successful_conversions'] > 0:
        leads_per_conversion = best_source['totalleads'] / best_source['successful_conversions']
        st.caption(f"📊 Efficiency: 1 conversion per {leads_per_conversion:.0f} leads")

with col2:
    worst_idx = df['converted_rate'].idxmin()
    worst_source = df.loc[worst_idx]
    st.markdown("#### ⚠️ Worst Performing Source")
    st.metric(
        worst_source['source'],
        f"{worst_source['converted_rate']:.1f}% conversion",
        f"{worst_source['successful_conversions']} conversions from {worst_source['totalleads']} leads",
        delta_color="inverse"
    )

st.markdown("---")

st.markdown("## 🎯 Lead Source Conversion Analysis")

st.success("""
### Top Performing Lead Sources

• Email Marketing achieved the highest conversion rate (**26.03%**) while also generating a strong lead volume (**73 leads**).

• Social Media generated the highest number of leads (**87 leads**) and maintained a healthy conversion rate (**19.54%**).

• SEO delivered a competitive conversion rate (**18.92%**) with a substantial lead volume (**74 leads**).

These channels are currently the strongest contributors to student enrollments and should remain a key focus area for marketing investments.
""")

st.info("""
### Marketing Effectiveness

• Email Marketing is currently the most efficient acquisition channel, converting approximately **1 in every 4 leads** into a successful enrollment.

• Social Media and SEO are performing at similar conversion levels, indicating that digital channels collectively play a significant role in driving enrollments.

• User Referrals and Website leads generate comparatively lower conversion rates, suggesting that students from these channels may require stronger nurturing and follow-up.
""")

st.warning("""
### Areas Requiring Attention

• Website-generated leads have the lowest conversion rate (**10.34%**), despite generating **58 leads**.

• User Referrals convert at only **12.12%**, which is significantly lower than Email Marketing.

• These channels may be generating awareness but are less effective at bringing highly qualified prospects into the enrollment funnel.
""")

st.error("""
### Potential Revenue Leakage

• If Website leads converted at the same rate as Email Marketing, the business could potentially achieve substantially more enrollments without increasing lead acquisition costs.

• Low-performing lead sources consume marketing resources while contributing fewer successful conversions, reducing overall marketing ROI.
""")

st.markdown("""
###  Recommended Actions

- Increase investment in Email Marketing campaigns due to the highest conversion efficiency.

- Continue scaling Social Media and SEO campaigns as they provide both strong lead volume and healthy conversion rates.

- Audit Website and Referral lead journeys to identify where students are disengaging.

- Implement channel-specific nurturing strategies for lower-converting sources.

- Analyze the characteristics of Email Marketing leads and replicate successful targeting strategies across other acquisition channels.
""")
