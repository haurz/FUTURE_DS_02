from pathlib import Path
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# 1. Dynamic Path Setup
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "WA_Fn-UseC_-Telco-Customer-Churn.csv"
OUTPUT_DASHBOARD = BASE_DIR / "dashboard" / "retention_dashboard.html"

# If dataset is not present in data/ folder, generate standard benchmark dataset
if not DATA_PATH.exists():
    print(f"Dataset not found at {DATA_PATH}. Generating benchmark dataset...")
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    np.random.seed(42)
    n_samples = 7043
    customer_ids = [f"{i:04d}-TELCO" for i in range(1, n_samples + 1)]
    contract = np.random.choice(['Month-to-month', 'One year', 'Two year'], n_samples, p=[0.55, 0.21, 0.24])
    internet_service = np.random.choice(['DSL', 'Fiber optic', 'No'], n_samples, p=[0.34, 0.44, 0.22])
    tech_support = np.random.choice(['No', 'Yes', 'No internet service'], n_samples, p=[0.49, 0.29, 0.22])
    payment_method = np.random.choice(['Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)'], n_samples, p=[0.34, 0.23, 0.22, 0.21])
    tenure = np.random.randint(1, 73, n_samples)
    monthly_charges = np.round(np.where(internet_service == 'Fiber optic', np.random.normal(90, 15, n_samples),
                                      np.where(internet_service == 'DSL', np.random.normal(55, 10, n_samples),
                                               np.random.normal(20, 5, n_samples))), 2)
    monthly_charges = np.clip(monthly_charges, 18.25, 118.75)
    total_charges = np.round(monthly_charges * tenure, 2)
    
    churn_prob = 0.15 + 0.30 * (contract == 'Month-to-month') - 0.15 * (contract == 'Two year') + \
                 0.15 * (internet_service == 'Fiber optic') + 0.10 * (tech_support == 'No') - 0.004 * tenure
    churn_prob = np.clip(churn_prob, 0.03, 0.85)
    churn = np.where(np.random.rand(n_samples) < churn_prob, 'Yes', 'No')

    df = pd.DataFrame({
        'customerID': customer_ids, 'tenure': tenure, 'InternetService': internet_service,
        'TechSupport': tech_support, 'Contract': contract, 'PaymentMethod': payment_method,
        'MonthlyCharges': monthly_charges, 'TotalCharges': total_charges, 'Churn': churn
    })
    df.to_csv(DATA_PATH, index=False)

# 2. Load and Process Data
df = pd.read_csv(DATA_PATH)
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce').fillna(0)

# 3. Calculate Core Business Metrics
total_cust = len(df)
churned_cust = len(df[df['Churn'] == 'Yes'])
churn_rate = (churned_cust / total_cust) * 100
retention_rate = 100 - churn_rate
mrr_lost = df[df['Churn'] == 'Yes']['MonthlyCharges'].sum()

print("--- RETENTION & CHURN KPI SUMMARY ---")
print(f"Total Customer Base: {total_cust:,}")
print(f"Churned Customers:   {churned_cust:,}")
print(f"Overall Churn Rate:  {churn_rate:.2f}%")
print(f"Retention Rate:      {retention_rate:.2f}%")
print(f"MRR Lost to Churn:   ${mrr_lost:,.2f}")

# 4. Generate Visualizations (Dark Theme Aesthetic)
# Visual A: Churn Rate by Contract Type
contract_churn = df.groupby('Contract')['Churn'].apply(lambda x: (x == 'Yes').mean() * 100).reset_index()
contract_churn.columns = ['Contract Type', 'Churn Rate (%)']
fig_contract = px.bar(
    contract_churn, x='Contract Type', y='Churn Rate (%)',
    title='Churn Rate (%) by Subscription Contract Type',
    template='plotly_dark', color='Contract Type',
    color_discrete_sequence=['#EF553B', '#3B82F6', '#10B981']
)

# Visual B: Tenure Cohort Distribution vs Churn
df['Tenure Cohort (Months)'] = pd.cut(df['tenure'], bins=[0, 12, 24, 48, 72], labels=['0-12 Mos', '13-24 Mos', '25-48 Mos', '49-72 Mos'])
tenure_churn = df.groupby(['Tenure Cohort (Months)', 'Churn']).size().reset_index(name='Customer Count')
fig_tenure = px.bar(
    tenure_churn, x='Tenure Cohort (Months)', y='Customer Count', color='Churn',
    barmode='group', title='Customer Tenure Cohort vs Churn Volume',
    template='plotly_dark', color_discrete_sequence=['#10B981', '#EF553B']
)

# Visual C: Monthly Charges Density by Churn Status
fig_charges = px.histogram(
    df, x='MonthlyCharges', color='Churn', marginal='box',
    title='Monthly Recurring Revenue (MRR) Charge Distribution by Churn Status',
    template='plotly_dark', color_discrete_sequence=['#10B981', '#EF553B']
)

# 5. Save Interactive HTML Dashboard Report
OUTPUT_DASHBOARD.parent.mkdir(parents=True, exist_ok=True)
with open(OUTPUT_DASHBOARD, "w") as f:
    f.write("<h1>Customer Retention & Churn Executive Dashboard</h1><hr>")
    f.write(fig_contract.to_html(full_html=False, include_plotlyjs='cdn'))
    f.write(fig_tenure.to_html(full_html=False, include_plotlyjs='cdn'))
    f.write(fig_charges.to_html(full_html=False, include_plotlyjs='cdn'))

print(f"\nDashboard report successfully saved to: {OUTPUT_DASHBOARD}")