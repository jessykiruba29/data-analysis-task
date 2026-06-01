import streamlit as st
import pandas as pd
import plotly.express as px
from db_config import engine
from queries import team_performance

st.title("👥 Senior Manager Team Performance Analysis")

# Load data
df = pd.read_sql(team_performance, engine)

# Display raw data
st.dataframe(df)

# Bar chart: Average team conversion by senior manager
fig = px.bar(
    df,
    x="snr_sm_id",
    y="avg_team_conversion",
    text="avg_team_conversion",
    color="avg_team_conversion",
    title="Average Team Conversion Rate by Senior Manager",
    labels={
        "snr_sm_id": "Senior Manager ID",
        "avg_team_conversion": "Average Team Conversion Rate (%)"
    },
    color_continuous_scale="Viridis"
)

fig.update_traces(
    texttemplate='%{text:.1f}%',
    textposition='outside'
)
fig.update_layout(
    yaxis_range=[0, max(df['avg_team_conversion']) * 1.2],
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

# Scatter plot: Team size vs performance
fig2 = px.scatter(
    df,
    x="total_juniors",
    y="avg_team_conversion",
    size="total_juniors",
    text="snr_sm_id",
    title="Team Size vs Average Conversion Rate",
    labels={
        "total_juniors": "Number of Junior Managers",
        "avg_team_conversion": "Average Team Conversion Rate (%)"
    },
    color="avg_team_conversion",
    color_continuous_scale="Viridis"
)

fig2.update_traces(
    textposition='top center',
    marker=dict(sizeref=2.*max(df['total_juniors'])/(40.**2), sizemin=4)
)

st.plotly_chart(fig2, use_container_width=True)

# Range chart: Best vs worst junior performance within each senior's team
fig3 = px.bar(
    df,
    x="snr_sm_id",
    y=["lowest_conversion", "highest_conversion"],
    title="Conversion Rate Range Within Each Senior Manager's Team",
    labels={
        "snr_sm_id": "Senior Manager ID",
        "value": "Conversion Rate (%)",
        "variable": "Performance"
    },
    barmode="group"
)

fig3.update_layout(
    yaxis_range=[0, max(df['highest_conversion']) * 1.2]
)

st.plotly_chart(fig3, use_container_width=True)

# Key insights
st.markdown("---")
st.subheader("📊 Key Performance Insights")

col1, col2, col3 = st.columns(3)

with col1:
    best_snr = df.loc[df['avg_team_conversion'].idxmax()]
    st.metric(
        "🏆 Best Senior Manager",
        best_snr['snr_sm_id'],
        f"{best_snr['avg_team_conversion']:.1f}% avg conversion"
    )
    st.caption(f"Managing {best_snr['total_juniors']} junior managers")

with col2:
    worst_snr = df.loc[df['avg_team_conversion'].idxmin()]
    st.metric(
        "⚠️ Needs Improvement",
        worst_snr['snr_sm_id'],
        f"{worst_snr['avg_team_conversion']:.1f}% avg conversion",
        delta_color="inverse"
    )
    st.caption(f"Range: {worst_snr['lowest_conversion']:.1f}% - {worst_snr['highest_conversion']:.1f}%")



st.markdown("---")
st.markdown("## 👥 Senior Manager Team Performance Analysis")

st.success("""
### Top Performing Team

• SNR501MG leads the highest-performing team with an average conversion rate of **25.66%**.

• The team's lowest-performing junior still achieves **17.65%**, indicating consistently strong performance across the team.

• This suggests effective coaching, lead allocation, and sales management practices.
""")

st.info("""
### Team Performance Comparison

• SNR504MG achieved the second-highest average conversion rate (**18.48%**).

• SNR502MG and SNR503MG lag behind with average team conversion rates of **15.00%** and **12.41%** respectively.

• The gap between the best and worst-performing teams exceeds **13 percentage points**, indicating substantial differences in team effectiveness.
""")

st.warning("""
### Performance Consistency

• SNR504MG shows the largest performance gap between juniors (**10.00% to 29.63%**).

• This suggests that while some team members perform exceptionally well, others may require additional training or support.

• Large variations within the same team often indicate inconsistent sales processes or coaching practices.
""")

st.error("""
### Potential Revenue Leakage

• Teams under SNR502MG and SNR503MG are converting significantly fewer students compared to SNR501MG.

• If lower-performing teams could achieve conversion rates similar to the top-performing team, the business could generate substantially more enrollments from the same lead volume.

• This represents a process and performance gap rather than a lead acquisition problem.
""")

st.markdown("""
### Recommended Actions

- Study the sales practices, follow-up strategies, and coaching methods used by SNR501MG's team.

- Conduct knowledge-sharing sessions between high-performing and low-performing teams.

- Review lead allocation fairness to ensure performance differences are not caused by lead quality.

- Provide targeted coaching to juniors in teams showing large performance variation.

- Establish standardized sales playbooks across all teams to reduce performance inconsistency.
""")

st.success("""
### 💰 Business Impact

The data suggests that conversion performance is influenced not only by lead quality but also by team effectiveness.

Improving the performance of lower-performing teams could increase enrollments without requiring additional marketing spend, making this one of the most cost-effective opportunities for business growth.
""")