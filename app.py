import streamlit
import pandas as pd
import altair 


streamlit.title("My First Streamlit App")
streamlit.header("Data Overview")
data = pd.read_csv("transactions.csv")
streamlit.dataframe(data)

data['Type'] = data['Type'].str.strip().str.lower()

total_income = data[data['Type'] == 'income']['Amount'].sum()
total_expense = data[data['Type'] == 'expense']['Amount'].sum()
balance = total_income - total_expense

streamlit.subheader("Financial Summary")
streamlit.metric("Total Income", f"£{total_income:,.2f}")
streamlit.metric("Total Expense", f"£{total_expense:,.2f}")
streamlit.metric("Balance", f"£{balance:,.2f}")

streamlit.subheader("Spending by category")
chart = altair.Chart(data[data['Type'] == 'expense']).mark_bar().encode(
    x='Category',
    y='Amount',
)
streamlit.altair_chart(chart, use_container_width=True)
streamlit.subheader("Income by category")
chart_income = altair.Chart(data[data['Type'] == 'income']).mark_bar().encode(
    x='Category',
    y='Amount',
)
streamlit.altair_chart(chart_income, use_container_width=True)

streamlit.subheader("Balance Over Time")
data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
data = data.sort_values('Date')
data['Balance'] = (data.apply(lambda row: row['Amount'] if row['Type'] == 'income' else -row['Amount'], axis=1)).cumsum()
streamlit.line_chart(data.set_index('Date')['Balance'])