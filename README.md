# Task 2: Customer Retention & Churn Analysis (`FUTURE_DS_02`)

## Executive Summary
This project evaluates customer subscription profiles, churn rates, and retention behaviors to identify primary attrition drivers. The goal is to provide actionable recommendations to reduce Monthly Recurring Revenue (MRR) loss and improve customer lifetime value.

## Key Performance Indicators (KPIs)
- **Total Customer Base**: 7,043
- **Active Retained Customers**: 5,121 (72.71%)
- **Churned Customers**: 1,922 (27.29%)
- **Monthly Recurring Revenue (MRR) Attrition**: $131,234.36 / month
- **Average Customer Retention Rate**: 72.71%

## Core Analytical Findings
1. **Contract Volatility**: Customers on **Month-to-month** subscription plans represent the highest proportion of lost users compared to 1-Year and 2-Year term commitments.
2. **Tenure Window Attrition**: Customer drop-off concentrates heavily in the **0–12 month tenure cohort**, showing that initial onboarding friction is the critical retention bottleneck.
3. **Price & Support Impact**: High Monthly Charge subscribers lacking technical support add-ons exhibit significantly higher churn rates.

## Strategic Retention Recommendations
- **Contract Transition Incentives**: Offer a 10% plan discount to encourage high-risk Month-to-month subscribers to transition into annual plans.
- **90-Day Customer Success Onboarding**: Implement structured user onboarding check-ins to boost retention through the vulnerable 0–12 month window.
- **Value-Add Feature Bundling**: Automatically bundle premium Tech Support with higher-tier internet plans to reduce price-sensitive churn.

## Project Structure
```text
FUTURE_DS_02/
├── data/
│   └── telco_customer_churn.csv
├── dashboard/
│   └── retention_dashboard.html
├── notebook/
│   └── churn_analysis.py
└── README.md
