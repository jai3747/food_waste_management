import streamlit as st
from sql_queries import queries
from utils import run_query

st.write("Welcome to the platform!")
st.title("🍱 Local Food Wastage Management System")

st.sidebar.header("🔍 Select Analysis")
option = st.sidebar.selectbox("Choose a report", list(queries.keys()))

if st.sidebar.button("Run Query"):
    result = run_query(queries[option])
    st.dataframe(result)
