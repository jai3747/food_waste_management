#database_utils.py
import streamlit as st
from database_utils import initialize_app, load_food_data

# Initialize the application (set up database)
initialize_app()

def main():
    st.title("Food Waste Reduction App")
    
    # Load food data
    food_data = load_food_data()
    
    # Display food listings
    if not food_data.empty:
        st.dataframe(food_data)
    else:
        st.warning("No food listings found.")

if __name__ == "__main__":
    main()
