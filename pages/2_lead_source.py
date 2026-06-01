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

# Volume vs Conversion Rate comparison
st.markdown("---")
