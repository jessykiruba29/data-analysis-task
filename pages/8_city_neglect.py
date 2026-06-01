import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from db_config import engine
from queries import city_neglect

st.title("📍 City-wise Lead Neglect Analysis")

# Load data
df = pd.read_sql(city_neglect, engine)

# Display raw data
st.dataframe(df)

# Bar chart: Contact rate by city (worst first)
fig = px.bar(
    df,
    x="current_city",
    y="contact_rate",
    text="contact_rate",
    color="contact_rate",
    title="Lead Contact Rate by City (Worst to Best)",
    labels={
        "current_city": "City",
        "contact_rate": "Contact Rate (%)"
    },
    color_continuous_scale="RdYlGn_r"  # Red for low contact, Green for high
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

# Stacked bar: Contacted vs Ignored leads
fig2 = go.Figure()

fig2.add_trace(go.Bar(
    name="Leads Contacted",
    x=df["current_city"],
    y=df["leads_contacted"],
    marker_color="#22C55E",
    text=df["leads_contacted"],
    textposition="inside"
))

fig2.add_trace(go.Bar(
    name="Leads Ignored",
    x=df["current_city"],
    y=df["leads_ignored"],
    marker_color="#EF4444",
    text=df["leads_ignored"],
    textposition="inside"
))

fig2.update_layout(
    title="Lead Assignment vs Contact by City",
    xaxis_title="City",
    yaxis_title="Number of Leads",
    barmode="stack",
    xaxis_tickangle=-45,
    hovermode="x unified"
)

st.plotly_chart(fig2, use_container_width=True)

# Scatter plot: Leads assigned vs Contact rate
fig3 = px.scatter(
    df,
    x="leads_assigned",
    y="contact_rate",
    size="unique_juniors_assigned",
    text="current_city",
    title="Lead Volume vs Contact Rate by City",
    labels={
        "leads_assigned": "Total Leads Assigned",
        "contact_rate": "Contact Rate (%)",
        "unique_juniors_assigned": "Number of Juniors Assigned"
    },
    color="contact_rate",
    color_continuous_scale="RdYlGn_r",
    hover_data=['leads_ignored', 'leads_contacted']
)

fig3.update_traces(
    textposition='top center'
)

st.plotly_chart(fig3, use_container_width=True)

# Key metrics
st.markdown("---")
st.subheader("📊 National Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_cities = len(df)
    st.metric(
        "🏙️ Cities Analyzed",
        total_cities
    )

with col2:
    total_leads = df['leads_assigned'].sum()
    st.metric(
        "📋 Total Leads Assigned",
        f"{total_leads:,}"
    )

with col3:
    total_ignored = df['leads_ignored'].sum()
    ignore_rate = (total_ignored / total_leads * 100) if total_leads > 0 else 0
    st.metric(
        "🚫 Total Leads Ignored",
        f"{total_ignored:,}",
        f"{ignore_rate:.1f}% of all leads"
    )

with col4:
    avg_contact_rate = df['contact_rate'].mean()
    st.metric(
        "📞 Avg Contact Rate",
        f"{avg_contact_rate:.1f}%"
    )

st.markdown("---")

# Critical cities (bottom performers)
st.subheader("🚨 Critical Cities - Immediate Attention Required")

critical_cities = df.nsmallest(5, 'contact_rate')

if not critical_cities.empty:
    for idx, row in critical_cities.iterrows():
        if row['contact_rate'] < 100:  
            with st.expander(f"⚠️ {row['current_city']} - Only {row['contact_rate']:.1f}% contact rate"):
                st.write(f"""
                - **Leads assigned**: {row['leads_assigned']:,}
                - **Leads contacted**: {row['leads_contacted']:,}
                - **Leads ignored**: {row['leads_ignored']:,} ({(row['leads_ignored']/row['leads_assigned']*100):.1f}% ignored)
                - **Juniors assigned**: {row['unique_juniors_assigned']}
                
                **Estimated Revenue Loss**:
                - Assuming {row['leads_ignored']} ignored leads
                - At 10% expected conversion rate
                - At $500 per conversion
                - **Potential loss**: ${row['leads_ignored'] * 0.1 * 500:,.0f}
                
                **Recommended Actions**:
                1. Assign dedicated junior manager for this city
                2. Check if phone numbers have wrong area codes
                3. Consider local language support
                4. Run targeted re-engagement campaign for ignored leads
                """)
else:
    st.success("✅ No critical cities identified")

# Opportunity cities (high volume, low contact)
st.markdown("---")
st.markdown("## ☎️ City-wise Lead Contact Coverage Analysis")

st.warning("""
### Key Findings

• Chennai and Visakhapatnam recorded uncontacted leads, indicating that not every acquired student received sales outreach.

• Every uncontacted lead represents a student who never entered the conversion funnel despite the business investing resources to acquire them.

• Unlike affordability or interest-related drop-offs, these losses occur before the business has an opportunity to influence the student's decision.
""")

st.error("""
### Revenue Leakage

• A missed lead is a preventable loss.

• Marketing expenses have already been incurred to acquire these students, yet no sales effort was made to engage them.

• Uncontacted leads provide zero opportunity for conversion, making them one of the most avoidable forms of revenue leakage.

• Even a single neglected lead can represent a lost enrollment opportunity.
""")

st.info("""
### Business Implications

• Contact coverage should ideally be 100% across all cities.

• The presence of uncontacted leads indicates gaps in lead assignment, follow-up tracking, or counselor accountability.

• While affordability or domain interest may be outside the company's control, lead neglect is entirely controllable through process improvements.
""")

st.success("""
### Recommended Actions

- Establish a strict policy that every assigned lead must receive an initial contact attempt.

- Implement automated alerts for leads that remain untouched beyond a predefined time limit.

- Monitor counselor-level contact coverage as a key performance metric.

- Conduct periodic audits to identify and eliminate operational gaps causing lead neglect.

- Treat every uncontacted lead as a recoverable opportunity rather than a normal business loss.
""")

st.markdown("""
### 💰 Business Impact

Reducing lead neglect directly improves the utilization of marketing spend.

Unlike other drop-off reasons that may require pricing or product changes, preventing lead neglect is an operational improvement that can be addressed immediately through better processes and accountability.
""")