import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from db_config import engine
from queries import junior_neglect

st.title("🚫 Junior Manager Lead Neglect Analysis")

# Load data
df = pd.read_sql(junior_neglect, engine)

# Display raw data
st.dataframe(df)

# Bar chart: Neglect rate by junior manager (highest first)
fig = px.bar(
    df,
    x="jnr_sm_id",
    y="neglect_rate_percent",
    text="neglect_rate_percent",
    color="neglect_rate_percent",
    title="Lead Neglect Rate by Junior Manager (Worst Offenders First)",
    labels={
        "jnr_sm_id": "Junior Manager ID",
        "neglect_rate_percent": "Neglect Rate (%)"
    },
    color_continuous_scale="Reds",
    range_color=[0, 10]
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

# Dual metric bar chart: Assigned vs Contacted
fig2 = go.Figure()

fig2.add_trace(go.Bar(
    name="Leads Assigned",
    x=df["jnr_sm_id"],
    y=df["total_assigned"],
    marker_color="#EF4444",
    text=df["total_assigned"],
    textposition="inside"
))

fig2.add_trace(go.Bar(
    name="Leads Contacted",
    x=df["jnr_sm_id"],
    y=df["total_contacted"],
    marker_color="#22C55E",
    text=df["total_contacted"],
    textposition="inside"
))

fig2.update_layout(
    title="Assigned vs Contacted Leads by Junior Manager",
    xaxis_title="Junior Manager ID",
    yaxis_title="Number of Leads",
    barmode="group",
    xaxis_tickangle=-45,
    hovermode="x unified"
)

st.plotly_chart(fig2, use_container_width=True)



# Key metrics
st.markdown("---")
st.subheader("📊 Company-wide Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_juniors = len(df)
    st.metric(
        "👥 Juniors Analyzed",
        total_juniors
    )

with col2:
    total_assigned_all = df['total_assigned'].sum()
    st.metric(
        "📋 Total Leads Assigned",
        f"{total_assigned_all:,}"
    )

with col3:
    total_ignored_all = df['never_touched'].sum()
    ignore_rate_all = (total_ignored_all / total_assigned_all * 100) if total_assigned_all > 0 else 0
    st.metric(
        "🚫 Total Leads Ignored",
        f"{total_ignored_all:,}",
        f"{ignore_rate_all:.1f}% of all leads"
    )

with col4:
    avg_neglect = df['neglect_rate_percent'].mean()
    st.metric(
        "📊 Avg Neglect Rate",
        f"{avg_neglect:.1f}%"
    )

st.markdown("---")

