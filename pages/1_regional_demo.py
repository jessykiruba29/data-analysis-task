import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from db_config import engine
from queries import regional_demo

st.title("🌍 Region-Wise Language & Demo Watch Analysis")

# Load data
df = pd.read_sql(regional_demo, engine)

# Display raw data
st.dataframe(df)

# Bar chart: Total leads by region and language
fig = px.bar(
    df,
    x="current_city",
    y="totalleads",
    color="language",
    text="totalleads",
    title="Demo Watchers by City and Language",
    labels={
        "current_city": "City",
        "totalleads": "Number of Leads",
        "language": "Demo Language"
    },
    barmode="group"
)

fig.update_traces(
    textposition='outside'
)
fig.update_layout(
    xaxis_tickangle=-45,
    legend_title_text="Language"
)

st.plotly_chart(fig, use_container_width=True)

# Heatmap: City vs Language matrix
pivot_df = df.pivot(index="current_city", columns="language", values="totalleads").fillna(0)

fig2 = px.imshow(
    pivot_df,
    text_auto=True,
    aspect="auto",
    title="Heatmap: Lead Distribution by City & Language",
    labels={
        "x": "Language",
        "y": "City",
        "color": "Number of Leads"
    },
    color_continuous_scale="Viridis"
)

st.plotly_chart(fig2, use_container_width=True)



# Key metrics
st.markdown("---")
st.subheader("📊 Key Insights")

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_demo_watchers = df['totalleads'].sum()
    st.metric(
        "🎬 Total Demo Watchers",
        f"{total_demo_watchers:,}"
    )

with col2:
    unique_cities = df['current_city'].nunique()
    st.metric(
        "🏙️ Cities Covered",
        unique_cities
    )

with col3:
    languages = df['language'].nunique()
    st.metric(
        "🌐 Languages Available",
        languages
    )

with col4:
    overall_avg_time = (df['totalleads'] * df['avgtime']).sum() / df['totalleads'].sum()
    st.metric(
        "⏱️ Overall Avg Watch Time",
        f"{overall_avg_time:.1f}%"
    )

st.markdown("---")

# Language performance by city
st.subheader("🎯 Language Performance by City")

# Find best language per city
best_lang_per_city = df.loc[df.groupby('current_city')['avgtime'].idxmax()]

col1, col2 = st.columns(2)

with col1:
    fig4 = px.bar(
        best_lang_per_city,
        x="current_city",
        y="avgtime",
        color="language",
        text="avgtime",
        title="Best Performing Language by City (Highest Watch Time)",
        labels={
            "current_city": "City",
            "avgtime": "Average Watch Time (%)",
            "language": "Best Language"
        }
    )
    fig4.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig4.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig4, use_container_width=True)

with col2:
    # Language distribution pie
    lang_summary = df.groupby('language')['totalleads'].sum().reset_index()
    fig5 = px.pie(
        lang_summary,
        names="language",
        values="totalleads",
        title="Overall Language Distribution",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig5.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig5, use_container_width=True)





# Language preference analysis
st.markdown("---")
st.subheader("🗺️ Language Preference by City")

# Create a stacked bar chart showing language distribution per city
lang_pivot = df.pivot(index="current_city", columns="language", values="totalleads").fillna(0)

# Calculate percentages
lang_pivot_pct = lang_pivot.div(lang_pivot.sum(axis=1), axis=0) * 100

fig6 = px.bar(
    lang_pivot_pct,
    x=lang_pivot_pct.index,
    y=lang_pivot_pct.columns,
    title="Language Preference (% of Leads) by City",
    labels={
        "index": "City",
        "value": "Percentage of Leads (%)",
        "variable": "Language"
    },
    barmode="stack"
)

fig6.update_layout(
    xaxis_tickangle=-45,
    yaxis_title="Percentage (%)",
    legend_title_text="Language"
)

st.plotly_chart(fig6, use_container_width=True)

# Strategic recommendations
st.markdown("---")
