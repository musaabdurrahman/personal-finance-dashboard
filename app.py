import streamlit
import pandas as pd

streamlit.title("My First Streamlit App")
streamlit.header("Data Overview")
data = pd.read_csv("data.csv")
streamlit.dataframe(data)