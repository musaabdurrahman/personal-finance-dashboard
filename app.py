import streamlit
import pandas as pd

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