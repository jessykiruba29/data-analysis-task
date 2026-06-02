# Student Lead Conversion Analytics Dashboard

## Overview

The Student Lead Conversion Analytics Dashboard is a business intelligence project developed to analyze the complete student enrollment funnel, identify conversion bottlenecks, evaluate marketing effectiveness, and generate actionable business insights.

The project uses SQL for data analysis and Streamlit for interactive visualization, transforming raw lead and sales data into meaningful insights that can support marketing, sales, and operational decision-making.

---

## Objectives

* Understand student acquisition patterns.
* Measure effectiveness of different lead generation channels.
* Analyze student engagement with demo sessions.
* Identify major drop-off points in the sales funnel.
* Discover reasons behind lead loss.
* Evaluate affordability-related challenges.
* Measure regional performance and conversion trends.
* Assess follow-up effectiveness in the conversion process.
* Provide actionable recommendations to improve enrollments.

---

## Dataset Description

The project uses five datasets:

### 1. Lead Basic Details

Contains demographic and acquisition information.

Columns:

* lead_id
* age
* gender
* current_city
* current_education
* parent_occupation
* lead_gen_source

### 2. Demo Watched Details

Tracks demo session engagement.

Columns:

* lead_id
* demo_watched_date
* language
* watched_percentage

### 3. Lead Interaction Details

Contains counselor interactions and lead progression.

Columns:

* lead_id
* lead_stage
* call_done_date
* call_status
* call_reason
* jnr_sm_id

### 4. Reasons for No Interest

Stores reasons for dropping out at different stages.

Columns:

* lead_id
* reasons_for_not_interested_in_demo
* reasons_for_not_interested_to_consider
* reasons_for_not_interested_to_convert

### 5. Sales Manager Assignment Details

Tracks lead assignments to sales teams.

Columns:

* snr_sm_id
* jnr_sm_id
* assigned_date
* cycle
* lead_id

---

## Technology Stack

### Database

* MySQL

### Data Analysis

* SQL

### Backend Connectivity

* SQLAlchemy
* PyMySQL

### Dashboard

* Streamlit

### Visualization

* Plotly

### Data Processing

* Pandas

---

## Project Architecture

```text
Student-Lead-Analytics/
│
├── app.py
├── db_config.py
├── requirements.txt
├── README.md
│
├── pages/
│   ├── 1_regional_demo.py
│   ├── 2_conversion_source.py
│   ├── 3_dropoff_analysis.py
│   ├── ...
│
├── data/
│   ├── leads_basic_details.csv
│   ├── leads_demo_watched_details.csv
│   ├── leads_interaction_details.csv
│   ├── leads_reasons_for_no_interest.csv
│   └── sales_managers_assigned_leads_details.csv
│
└── .gitignore
```

---

## Key Business Problems Addressed

### Marketing Optimization

* Which channels generate the highest quality leads?
* Which channels produce the best conversion rates?

### Regional Strategy

* Which cities perform best?
* Which language segments are most engaged?

### Sales Effectiveness

* How many follow-ups are required before conversion?
* Which sales representatives require coaching?

### Student Retention

* Why are students leaving the funnel?
* At which stage do most students drop off?

### Pricing Strategy

* Which student segments are most price-sensitive?

---

## Major Findings

### Lead Source Performance

Email marketing and social media channels generated the highest conversion rates.

### Demo Engagement

Students with higher demo watch percentages showed stronger conversion tendencies.

### Funnel Analysis

The majority of lead losses occurred during the demo stage.

### Affordability Concerns

Price sensitivity emerged as one of the most common reasons for non-conversion.

### Regional Insights

Certain cities demonstrated significantly stronger conversion rates, indicating opportunities for localized marketing campaigns.

### Follow-Up Strategy

Most successful conversions occurred after multiple counselor interactions, highlighting the importance of persistent engagement.

---

## Business Impact

This dashboard helps organizations:

* Improve marketing ROI.
* Reduce lead leakage.
* Optimize sales follow-up strategies.
* Identify high-performing regions.
* Understand student behavior patterns.
* Prioritize investment opportunities.
* Increase overall enrollment conversions.

---

## Future Enhancements

* Predictive lead scoring.
* Conversion forecasting.
* Student churn prediction.
* Automated recommendation engine.
* Real-time dashboard integration.
* AI-powered lead prioritization.

---

# Titles of the 12 Analyses

1.	**Which Cities and Languages Show the Highest Demo Engagement?**
2.	**Which Lead Source Generates the Highest Conversion Rate?**
3.	**Why Do Students Drop Off at Each Stage of the Funnel?**
4.	**Which Education Groups Face the Most Affordability Issues?** 
5.	**Does Higher Demo Watch Percentage Lead to Better Conversions?** 
6.	**How Do Senior Managers Compare in Team Conversion Performance?**
7.	**Which Junior Sales Managers Have the Lowest Conversion Performance?** 
8.	**Which Cities Have the Highest Percentage of Uncontacted Leads?**
9.	**Which Junior Sales Managers Are Not Following Up on Assigned Leads?** 
10.	**How Does Age Group Influence Student Conversion Rates?**
11.	**How Many Follow-Up Calls Are Needed to Convert a Student?** 
12.	**Which Cities Deliver the Highest Conversion Rates?**
13. **Demo Follow-Up Delay vs Conversion Analysis**

