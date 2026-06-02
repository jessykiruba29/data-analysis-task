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


# Strategic recommendations
st.markdown("---")

st.markdown("## 📊 Regional Engagement Insights")

st.success("""
**Top Performing Regions**
- Chennai (English) recorded the highest engagement among major lead-generating regions with an average watch percentage of **67%**.
- Hyderabad (English) closely followed with **66.14%**, indicating strong student interest.
- These regions demonstrate higher potential for future conversions and should be prioritized for marketing campaigns.
""")

st.info("""
**Language Performance**
- English demos consistently outperformed Telugu demos across all major cities.
- Example:
    - Hyderabad: **66.14% vs 51.33%**
    - Chennai: **67.00% vs 48.29%**
- This suggests that English content currently resonates better with students and may contain best practices that can be replicated across regional-language demos.
""")

st.warning("""
**Areas Requiring Attention**
- Kochi Hindi (**28.75%**) and Hyderabad Hindi (**41.00%**) showed the lowest engagement levels.
- Low engagement increases the risk of students dropping out before entering later stages of the enrollment funnel.
- These regions should be reviewed for content quality, language suitability, and delivery effectiveness.
""")

st.error("""
**Potential Revenue Leakage**
- Students who disengage during demos represent lost marketing investment.
- Improving engagement in low-performing language segments can reduce early-stage drop-offs and increase the pool of students available for conversion.
""")

st.markdown("""
###  Recommended Actions

- Increase lead acquisition efforts in Chennai and Hyderabad.

- Prioritize students with higher demo watch percentages for faster counselor follow-up.

- Audit Telugu and Hindi demo content to identify engagement gaps.

- Establish minimum engagement benchmarks and continuously monitor underperforming city-language combinations.
""")