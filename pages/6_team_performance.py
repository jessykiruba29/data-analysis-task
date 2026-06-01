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


