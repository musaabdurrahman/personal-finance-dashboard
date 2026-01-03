import streamlit as st
import pandas as pd
import altair as alt

st.title("Personal Finance Dashboard")
st.write("A simple dashboard to explore income, expenses, and balance from a CSV file.")

st.header("Data Overview")
data = pd.read_csv("transactions.csv")
st.dataframe(data)

data['Type'] = data['Type'].str.strip().str.lower()

total_income = data[data['Type'] == 'income']['Amount'].sum()
total_expense = data[data['Type'] == 'expense']['Amount'].sum()
balance = total_income - total_expense

st.subheader("Financial Summary")
st.metric("Total Income", f"£{total_income:,.2f}")
st.metric("Total Expense", f"£{total_expense:,.2f}")
st.metric("Balance", f"£{balance:,.2f}")

avg_transaction = data['Amount'].mean()
st.metric("Average Transaction", f"£{avg_transaction:,.2f}")

st.header("Visualisations")
st.subheader("Spending by category")
chart = alt.Chart(data[data['Type'] == 'expense']).mark_bar().encode(
    x='Category',
    y='Amount',
)
st.altair_chart(chart, use_container_width=True)
st.subheader("Income by category")
chart_income = alt.Chart(data[data['Type'] == 'income']).mark_bar().encode(
    x='Category',
    y='Amount',
)
st.altair_chart(chart_income, use_container_width=True)

st.subheader("Balance Over Time")
data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
data = data.sort_values('Date')
data['Balance'] = (data.apply(lambda row: row['Amount'] if row['Type'] == 'income' else -row['Amount'], axis=1)).cumsum()
st.line_chart(data.set_index('Date')['Balance'])