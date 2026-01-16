# Simple personal finance dashboard built with Streamlit, pandas, and Altair
import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Personal Finance Dashboard", layout="centered")

#title and description
st.title("Personal Finance Dashboard")
st.caption("A simple dashboard to explore income, expenses, and balance from a CSV file.")

data = pd.read_csv("transactions.csv") # transactions.csv contains Date, Category, Type (income/expense), and Amount
data['Type'] = data['Type'].str.strip().str.lower()

#sidebar filters
# Filters allow users to interactively subset the data by date and category

st.sidebar.header("Filters")
data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
data = data.sort_values('Date')
data = data.dropna(subset=['Date'])
min_date = data['Date'].min()
max_date = data['Date'].max()
start_date, end_date = st.sidebar.date_input(
    "Select date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)
filtered_data = data[
    (data['Date'] >= pd.to_datetime(start_date)) &
    (data['Date'] <= pd.to_datetime(end_date))
]
categories = st.sidebar.multiselect(
    "Categories",
    options=sorted(filtered_data['Category'].unique()),
    default=sorted(filtered_data['Category'].unique())
)
filtered_data = filtered_data[
    filtered_data['Category'].isin(categories)
]
if filtered_data.empty:
    st.warning("No data for selected filters.")
    st.stop()


#main dashboard
st.header("Data Overview")
st.dataframe(filtered_data)

#summary metrics
total_income = filtered_data[filtered_data['Type'] == 'income']['Amount'].sum()
total_expense = filtered_data[filtered_data['Type'] == 'expense']['Amount'].sum()
balance = total_income - total_expense

st.divider()

st.subheader("Financial Summary")
st.metric("Total Income", f"£{total_income:,.2f}")
st.metric("Total Expense", f"£{total_expense:,.2f}")
st.metric("Balance", f"£{balance:,.2f}")

avg_transaction = filtered_data['Amount'].mean()
st.metric("Average Transaction", f"£{avg_transaction:,.2f}")

st.divider()

#visualisations
st.header("Visualisations")
st.subheader("Spending by category")
chart = alt.Chart(filtered_data[filtered_data['Type'] == 'expense']).mark_bar().encode(
    x='Category',
    y='Amount',
)
st.altair_chart(chart, use_container_width=True)
st.subheader("Income by category")
chart_income = alt.Chart(filtered_data[filtered_data['Type'] == 'income']).mark_bar().encode(
    x='Category',
    y='Amount',
)
st.altair_chart(chart_income, use_container_width=True)

st.subheader("Balance Over Time")
filtered_data['Balance'] = (filtered_data.apply(lambda row: row['Amount'] if row['Type'] == 'income' else -row['Amount'], axis=1)).cumsum()
st.line_chart(data.set_index('Date')['Balance'], use_container_width=True)