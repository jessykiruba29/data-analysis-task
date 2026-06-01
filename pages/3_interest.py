import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from db_config import engine
from queries import interest

st.set_page_config(page_title="Drop Reasons Analysis", layout="wide")
st.title("📉 Lead Drop-off Reasons Analysis")

# Load data
df = pd.read_sql(interest, engine)

# Display raw data
st.dataframe(df)

# Overall bar chart: Top drop reasons across all stages
st.subheader("🏆 Top Drop-off Reasons (All Stages Combined)")

# Aggregate by reason across stages
top_reasons = df.groupby('reason')['total_students'].sum().reset_index()
top_reasons = top_reasons.sort_values('total_students', ascending=False).head(10)

fig = px.bar(
    top_reasons,
    x="reason",
    y="total_students",
    text="total_students",
    color="total_students",
    title="Top 10 Reasons for Lead Drop-off (All Funnel Stages)",
    labels={
        "reason": "Drop-off Reason",
        "total_students": "Number of Leads"
    },
    color_continuous_scale="Reds"
)

fig.update_traces(
    textposition='outside'
)
fig.update_layout(
    xaxis_tickangle=-45,
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

# Stage-wise breakdown
st.markdown("---")
st.subheader("📊 Drop-off Reasons by Funnel Stage")

# Create three columns for different stages
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### 🔵 Demo Stage")
    demo_data = df[df['stage'] == 'Demo Stage'].sort_values('total_students', ascending=False)
    if not demo_data.empty:
        fig_demo = px.pie(
            demo_data,
            names="reason",
            values="total_students",
            title="Demo Stage Drop Reasons",
            color_discrete_sequence=px.colors.qualitative.Set1
        )
        fig_demo.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_demo, use_container_width=True)
    else:
        st.info("No demo stage drop data")

with col2:
    st.markdown("#### 🟡 Consideration Stage")
    consider_data = df[df['stage'] == 'Consideration Stage'].sort_values('total_students', ascending=False)
    if not consider_data.empty:
        fig_consider = px.pie(
            consider_data,
            names="reason",
            values="total_students",
            title="Consideration Stage Drop Reasons",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_consider.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_consider, use_container_width=True)
    else:
        st.info("No consideration stage drop data")

with col3:
    st.markdown("#### 🟢 Conversion Stage")
    conversion_data = df[df['stage'] == 'Conversion Stage'].sort_values('total_students', ascending=False)
    if not conversion_data.empty:
        fig_conversion = px.pie(
            conversion_data,
            names="reason",
            values="total_students",
            title="Conversion Stage Drop Reasons",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_conversion.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_conversion, use_container_width=True)
    else:
        st.info("No conversion stage drop data")



# Key metrics
st.markdown("---")
st.subheader("📊 Key Drop-off Statistics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_drops = df['total_students'].sum()
    st.metric("📉 Total Drop-offs", f"{total_drops:,}")

with col2:
    demo_drops = df[df['stage'] == 'Demo Stage']['total_students'].sum()
    demo_pct = (demo_drops / total_drops * 100) if total_drops > 0 else 0
    st.metric("🎬 Demo Stage Drops", f"{demo_drops:,}", f"{demo_pct:.1f}%")

with col3:
    consider_drops = df[df['stage'] == 'Consideration Stage']['total_students'].sum()
    consider_pct = (consider_drops / total_drops * 100) if total_drops > 0 else 0
    st.metric("🤔 Consideration Stage Drops", f"{consider_drops:,}", f"{consider_pct:.1f}%")

with col4:
    conversion_drops = df[df['stage'] == 'Conversion Stage']['total_students'].sum()
    conversion_pct = (conversion_drops / total_drops * 100) if total_drops > 0 else 0
    st.metric("💸 Conversion Stage Drops", f"{conversion_drops:,}", f"{conversion_pct:.1f}%")

st.markdown("---")

st.markdown("## 🚨 Student Drop-Off Reason Analysis")

st.error("""
### Major Causes of Student Loss

• The largest drop-off occurs during the Demo Stage, indicating that the business is losing students very early in the enrollment funnel.

• The most common reason for student loss is a preference for offline classes (**56 students**) followed closely by affordability concerns (**48 students**) during the Demo Stage itself.

• Combined across all stages, Affordability Issues account for **99 student drop-offs**, making it the single largest barrier to enrollment.

• Preference for Offline Classes contributed to **91 student drop-offs**, making it the second largest cause of student loss.
""")

st.warning("""
### Funnel Leakage Analysis

• A significant number of students are leaving before reaching the Conversion Stage.

• Since most losses occur during the Demo and Consideration stages, marketing money spent on acquiring these leads is not translating into enrollments.

• Students who leave due to affordability or learning format preferences represent potentially recoverable leads because they are not rejecting the domain itself.

• Only a smaller portion of students leave because they are not interested in the domain, suggesting that the course offering itself is not the primary issue.
""")

st.info("""
### High-Value Recovery Opportunities

• Nearly 190 student losses are attributed to only two reasons:
    - Affordability Issues (99)
    - Preference for Offline Classes (91)

• These students have already shown interest in the program but are prevented from converting due to external barriers.

• Recovering even a small percentage of these students could significantly increase enrollments without increasing marketing spend.
""")

st.success("""
### Recommended Business Actions

- Introduce EMI, installment, or scholarship options to address affordability concerns.

- Strengthen communication around placement outcomes and ROI to justify course pricing.

- Conduct surveys with students preferring offline classes to understand whether the concern is interaction, mentorship, networking, or learning effectiveness.

- Explore hybrid learning models, periodic offline workshops, or community events to address offline-learning preferences.

- Create separate follow-up campaigns for affordability-related and offline-preference leads instead of marking them as permanently lost.

- Prioritize recovery campaigns for these students before investing additional budget into acquiring new leads.
""")

st.markdown("""
### 💰 Profitability Impact

The company is currently spending money to acquire leads that are being lost primarily due to affordability and learning-format concerns.

Addressing these two barriers alone has the potential to recover the largest number of lost students, increase enrollment volume, and improve overall marketing ROI without increasing acquisition costs.
""")