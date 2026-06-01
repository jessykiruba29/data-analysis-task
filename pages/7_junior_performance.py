import streamlit as st
import pandas as pd
import plotly.express as px
from db_config import engine
from queries import junior_performance

st.title("📞 Junior Manager Performance Analysis")

# Load data
df = pd.read_sql(junior_performance, engine)

# Display raw data
st.dataframe(df)

# Bar chart: Conversion rate by junior manager (ascending = worst to best)
fig = px.bar(
    df,
    x="jnr_sm_id",
    y="conversion_rate",
    text="conversion_rate",
    color="conversion_rate",
    title="Junior Manager Conversion Rates (Worst to Best)",
    labels={
        "jnr_sm_id": "Junior Manager ID",
        "conversion_rate": "Conversion Rate (%)"
    },
    color_continuous_scale="RdYlGn_r"  # Red for low, Green for high
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

# Scatter plot: Volume vs Performance
fig2 = px.scatter(
    df,
    x="total_leads_handled",
    y="conversion_rate",
    size="total_leads_handled",
    text="jnr_sm_id",
    title="Lead Volume vs Conversion Rate",
    labels={
        "total_leads_handled": "Total Leads Handled",
        "conversion_rate": "Conversion Rate (%)"
    },
    color="conversion_rate",
    color_continuous_scale="RdYlGn_r",
    hover_data=['converted_leads']
)

fig2.update_traces(
    textposition='top center'
)

st.plotly_chart(fig2, use_container_width=True)

# Histogram: Distribution of conversion rates
fig3 = px.histogram(
    df,
    x="conversion_rate",
    nbins=20,
    title="Distribution of Junior Manager Conversion Rates",
    labels={
        "conversion_rate": "Conversion Rate (%)",
        "count": "Number of Junior Managers"
    },
    color_discrete_sequence=['#3B82F6']
)

fig3.update_layout(
    bargap=0.1
)

st.plotly_chart(fig3, use_container_width=True)

# Key insights
st.markdown("---")
st.subheader("📊 Performance Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    avg_cr = df['conversion_rate'].mean()
    st.metric(
        "📈 Average Conversion Rate",
        f"{avg_cr:.1f}%"
    )

with col2:
    median_cr = df['conversion_rate'].median()
    st.metric(
        "📊 Median Conversion Rate",
        f"{median_cr:.1f}%"
    )

with col3:
    total_converted = df['converted_leads'].sum()
    total_leads = df['total_leads_handled'].sum()
    st.metric(
        "🎯 Total Conversions",
        f"{total_converted:,}",
        f"out of {total_leads:,} leads"
    )

with col4:
    std_cr = df['conversion_rate'].std()
    st.metric(
        "📉 Performance Variance",
        f"±{std_cr:.1f}%",
        help="Higher variance = inconsistent team performance"
    )

st.markdown("---")

# Bottom performers (Critical)
st.subheader("🚨 Bottom Performers - Immediate Action Required")

bottom_3 = df.nsmallest(3, 'conversion_rate')

if not bottom_3.empty:
    for idx, row in bottom_3.iterrows():
        with st.expander(f"⚠️ {row['jnr_sm_id']} - {row['conversion_rate']:.1f}% conversion rate"):
            st.write(f"""
            - **Total leads handled**: {row['total_leads_handled']}
            - **Successful conversions**: {row['converted_leads']}
            - **Conversion rate**: {row['conversion_rate']:.1f}%
            
            **Recommended Actions**:
            1. Review last 10 call recordings
            2. Shadow a top performer for 2 days
            3. Daily check-ins for next 2 weeks
            4. Set target: Improve to {avg_cr:.0f}% within 30 days
            """)
else:
    st.success("✅ No critical bottom performers identified")

# Top performers
st.markdown("---")
st.subheader("⭐ Top Performers")

top_3 = df.nlargest(3, 'conversion_rate')

if not top_3.empty:
    cols = st.columns(3)
    for idx, (_, row) in enumerate(top_3.iterrows()):
        with cols[idx]:
            st.metric(
                f"🥇 #{idx+1}: {row['jnr_sm_id']}",
                f"{row['conversion_rate']:.1f}%",
                f"{row['converted_leads']}/{row['total_leads_handled']} converted"
            )
            st.caption(f"📞 Handled {row['total_leads_handled']} leads")
else:
    st.info("No top performers identified yet")

st.markdown("---")

st.markdown("## 📞 Junior Sales Manager Conversion Performance")

st.error("""
### Lowest Performing Sales Representatives

• JNR1011MG recorded the lowest conversion rate at **7.69%**, converting only **2 out of 26 assigned leads**.

• JNR1005MG, JNR1007MG, JNR1009MG, and JNR1013MG each converted only **10%** of their assigned leads.

• These managers collectively handled a significant number of leads but generated relatively few successful conversions.

• Low conversion rates may indicate issues with follow-up quality, objection handling, communication effectiveness, or lead nurturing.
""")

st.success("""
### Top Performing Sales Representatives

• JNR1002MG achieved the highest conversion rate at **35.00%**, converting **7 out of 20 leads**.

• JNR1003MG and JNR1016MG also demonstrated strong performance with conversion rates of **30.00%** and **29.63%** respectively.

• These counselors consistently convert a larger proportion of their assigned leads and may be following more effective sales practices.
""")

st.info("""
### Performance Gap Analysis

• The difference between the highest-performing counselor (**35%**) and the lowest-performing counselor (**7.69%**) is substantial.

• Since all counselors operate within the same business environment, such large performance differences suggest that individual sales practices significantly influence conversion outcomes.

• This indicates an opportunity to improve overall business performance through training and process standardization.
""")

st.warning("""
### Potential Revenue Leakage

• Many leads assigned to lower-performing counselors are not progressing to conversion.

• The business has already invested marketing resources to acquire these leads, making every unconverted lead a potential revenue loss.

• If the lowest-performing counselors could achieve even average conversion rates, the company could generate additional enrollments without increasing lead acquisition spend.
""")

st.markdown("""
###  Recommended Actions

- Conduct performance reviews for counselors with conversion rates below 15%.

- Analyze call recordings and follow-up patterns of top performers such as JNR1002MG and JNR1003MG.

- Create mentorship programs where high-performing counselors share successful strategies with lower-performing team members.

- Establish minimum performance benchmarks and monitor counselor conversion rates regularly.

- Investigate whether lead quality distribution is balanced across counselors before evaluating performance solely on conversion rates.
""")

st.success("""
### 💰 Business Impact

Improving the performance of the bottom-performing counselors represents a low-cost growth opportunity.

Rather than spending additional money to acquire new leads, the business can increase enrollments by improving how existing leads are managed and nurtured by the sales team.
""")
