import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Business KPI Dashboard", layout="wide", page_icon="📊")

# --- Data Loading ---
@st.cache_data
def load_data():
    df = pd.read_csv("customer_churn_sample.csv")
    return df

df = load_data()

# --- Sidebar Filters ---
st.sidebar.header("Dashboard Filters")

# Contract Filter
contracts = df['ContractType'].unique().tolist()
selected_contracts = st.sidebar.multiselect("Select Contract Type", contracts, default=contracts)

# Payment Method Filter
payment_methods = df['PaymentMethod'].unique().tolist()
selected_payments = st.sidebar.multiselect("Select Payment Method", payment_methods, default=payment_methods)

# Tenure Filter
min_tenure, max_tenure = int(df['TenureMonths'].min()), int(df['TenureMonths'].max())
selected_tenure = st.sidebar.slider("Select Tenure (Months)", min_tenure, max_tenure, (min_tenure, max_tenure))

# --- Apply Filters ---
filtered_df = df[
    (df['ContractType'].isin(selected_contracts)) &
    (df['PaymentMethod'].isin(selected_payments)) &
    (df['TenureMonths'] >= selected_tenure[0]) &
    (df['TenureMonths'] <= selected_tenure[1])
]

# --- Title ---
st.title("📊 Business KPI Dashboard: Customer Churn & Retention")
st.markdown("Track and analyze customer churn, retention rates, and revenue at risk.")
st.divider()

# --- KPI Calculations ---
total_customers = len(filtered_df)
if total_customers > 0:
    churned_customers = len(filtered_df[filtered_df['Churn'] == 'Yes'])
    churn_rate = (churned_customers / total_customers) * 100
    retention_rate = 100 - churn_rate
    revenue_at_risk = filtered_df[filtered_df['Churn'] == 'Yes']['MonthlyCharges'].sum()
    avg_tenure = filtered_df['TenureMonths'].mean()
else:
    churn_rate = 0
    retention_rate = 0
    revenue_at_risk = 0
    avg_tenure = 0

# --- Top KPI Cards ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Churn Rate", value=f"{churn_rate:.1f}%")
with col2:
    st.metric(label="Retention Rate", value=f"{retention_rate:.1f}%")
with col3:
    st.metric(label="Revenue at Risk (Monthly)", value=f"${revenue_at_risk:,.2f}")
with col4:
    st.metric(label="Average Tenure", value=f"{avg_tenure:.1f} months")

st.divider()

# --- Visualizations ---

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Churn Rate by Contract Type")
    # Group by Contract Type and calculate churn rate
    contract_churn = filtered_df.groupby('ContractType')['Churn'].apply(lambda x: (x == 'Yes').mean() * 100).reset_index(name='Churn Rate (%)')
    fig_contract = px.bar(contract_churn, x='ContractType', y='Churn Rate (%)', 
                          color='ContractType', text_auto='.1f',
                          color_discrete_sequence=px.colors.qualitative.Pastel)
    fig_contract.update_layout(showlegend=False)
    st.plotly_chart(fig_contract, use_container_width=True)
    st.info("💡 **Insight:** Month-to-month contracts typically exhibit higher churn rates due to lack of long-term commitment. Encouraging users to switch to yearly plans can drastically improve retention.")

with col_right:
    st.subheader("Churn by Subscription Type")
    # Count churned customers by subscription type
    sub_churn = filtered_df[filtered_df['Churn'] == 'Yes'].groupby('SubscriptionType').size().reset_index(name='Count')
    fig_sub = px.pie(sub_churn, values='Count', names='SubscriptionType', hole=0.4,
                     color_discrete_sequence=px.colors.qualitative.Set2)
    st.plotly_chart(fig_sub, use_container_width=True)
    st.info("💡 **Insight:** Identifies which product tier needs the most retention focus. If basic plans have the highest churn, it might indicate a need to demonstrate more value early on.")

st.divider()

col_bottom_left, col_bottom_right = st.columns(2)

with col_bottom_left:
    st.subheader("Revenue Risk by Payment Method")
    pay_revenue = filtered_df[filtered_df['Churn'] == 'Yes'].groupby('PaymentMethod')['MonthlyCharges'].sum().reset_index(name='Revenue Lost')
    fig_pay = px.bar(pay_revenue, y='PaymentMethod', x='Revenue Lost', orientation='h',
                     color='PaymentMethod', text_auto='$.2s',
                     color_discrete_sequence=px.colors.qualitative.Safe)
    fig_pay.update_layout(showlegend=False)
    st.plotly_chart(fig_pay, use_container_width=True)
    st.info("💡 **Insight:** Highlights if certain payment gateways (like Bank Transfers vs Credit Cards) are correlated with higher revenue loss. Automated/recurring payment methods usually help reduce passive churn.")

with col_bottom_right:
    st.subheader("Tenure Distribution of Churned Customers")
    fig_tenure = px.histogram(filtered_df[filtered_df['Churn'] == 'Yes'], x='TenureMonths', nbins=20,
                              color_discrete_sequence=['#EF553B'])
    st.plotly_chart(fig_tenure, use_container_width=True)
    st.info("💡 **Insight:** Shows exactly when customers tend to drop off. A spike in early months suggests a poor onboarding experience, while later spikes might indicate customers outgrowing the product.")
