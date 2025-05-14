import streamlit as st
import pandas as pd
from database_utils import run_query

# SQL Queries for reports - updated for MySQL syntax differences
queries = {
    "Food Expiring Soon (Next 3 Days)": 
        """SELECT Food_ID, Food_Name, Quantity, Expiry_Date, Provider_Type, Location 
           FROM food_listings 
           WHERE DATE(Expiry_Date) BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 3 DAY) 
           ORDER BY Expiry_Date""",
    
    "Food Available by Type": 
        """SELECT Food_Type, COUNT(*) as Count, SUM(Quantity) as Total_Quantity 
           FROM food_listings 
           GROUP BY Food_Type 
           ORDER BY Total_Quantity DESC""",
    
    "Provider Contribution Summary": 
        """SELECT Provider_Type, COUNT(*) as Listings, SUM(Quantity) as Total_Quantity 
           FROM food_listings 
           GROUP BY Provider_Type 
           ORDER BY Total_Quantity DESC""",
    
    "Food by Meal Type": 
        """SELECT Meal_Type, COUNT(*) as Count, SUM(Quantity) as Total_Quantity 
           FROM food_listings 
           GROUP BY Meal_Type 
           ORDER BY Total_Quantity DESC""",
    
    "Location Distribution": 
        """SELECT Location, COUNT(*) as Count, SUM(Quantity) as Total_Quantity 
           FROM food_listings 
           GROUP BY Location 
           ORDER BY Count DESC"""
}

def show_queries():
    """Run predefined SQL queries for analysis."""
    st.subheader("📊 Query-Based Analysis")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        option = st.selectbox("Choose a report", list(queries.keys()))
    
    with col2:
        run_button = st.button("Run Query", use_container_width=True)
    
    if run_button:
        try:
            result = run_query(queries[option])
            if not result.empty:
                st.dataframe(result, use_container_width=True)
                
                # Offer to download results as CSV
                csv = result.to_csv(index=False)
                st.download_button(
                    label="Download Results",
                    data=csv,
                    file_name=f"{option}_report.csv",
                    mime="text/csv",
                )
            else:
                st.info("No data available for this query.")
        except Exception as e:
            st.error(f"Error running query: {str(e)}")
            st.code(queries[option])
