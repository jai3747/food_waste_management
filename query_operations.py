import streamlit as st
import pandas as pd
from database_utils import run_query

# SQL Queries for reports - 21 comprehensive queries
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
           ORDER BY Count DESC""",
           
    "Expired Food Items": 
        """SELECT Food_ID, Food_Name, Quantity, Expiry_Date, Provider_Type, Location 
           FROM food_listings 
           WHERE DATE(Expiry_Date) < CURDATE() 
           ORDER BY Expiry_Date DESC""",
           
    "Food Items with Longest Shelf Life": 
        """SELECT Food_ID, Food_Name, Quantity, Expiry_Date, 
           DATEDIFF(Expiry_Date, CURDATE()) as Days_Until_Expiry
           FROM food_listings 
           WHERE DATE(Expiry_Date) > CURDATE()
           ORDER BY Days_Until_Expiry DESC 
           LIMIT 20""",
           
    "Low Quantity Items (Less than 10)": 
        """SELECT Food_ID, Food_Name, Quantity, Expiry_Date, Provider_Type, Location 
           FROM food_listings 
           WHERE Quantity < 10 AND DATE(Expiry_Date) > CURDATE() 
           ORDER BY Quantity""",
           
    "Monthly Contribution Trends": 
        """SELECT DATE_FORMAT(Date_Added, '%Y-%m') as Month, 
           COUNT(*) as Listings, SUM(Quantity) as Total_Quantity 
           FROM food_listings 
           GROUP BY DATE_FORMAT(Date_Added, '%Y-%m') 
           ORDER BY Month DESC""",
           
    "Top 10 Providers by Quantity": 
        """SELECT Provider_Name, COUNT(*) as Listings, SUM(Quantity) as Total_Quantity 
           FROM food_listings 
           GROUP BY Provider_Name 
           ORDER BY Total_Quantity DESC 
           LIMIT 10""",
           
    "Food Diversity by Location": 
        """SELECT Location, COUNT(DISTINCT Food_Type) as Food_Type_Count 
           FROM food_listings 
           GROUP BY Location 
           ORDER BY Food_Type_Count DESC""",
           
    "Average Shelf Life by Food Type": 
        """SELECT Food_Type, 
           AVG(DATEDIFF(Expiry_Date, Date_Added)) as Avg_Shelf_Life_Days 
           FROM food_listings 
           GROUP BY Food_Type 
           ORDER BY Avg_Shelf_Life_Days DESC""",
           
    "Items Added in Last 7 Days": 
        """SELECT Food_ID, Food_Name, Quantity, Date_Added, Provider_Type, Location 
           FROM food_listings 
           WHERE Date_Added >= DATE_SUB(CURDATE(), INTERVAL 7 DAY) 
           ORDER BY Date_Added DESC""",
           
    "Nutritional Value Distribution": 
        """SELECT Nutritional_Value, COUNT(*) as Count, SUM(Quantity) as Total_Quantity 
           FROM food_listings 
           GROUP BY Nutritional_Value 
           ORDER BY Total_Quantity DESC""",
           
    "Food Storage Requirements Analysis": 
        """SELECT Storage_Requirements, COUNT(*) as Count, SUM(Quantity) as Total_Quantity 
           FROM food_listings 
           GROUP BY Storage_Requirements 
           ORDER BY Total_Quantity DESC""",
           
    "Items Needing Special Handling": 
        """SELECT Food_ID, Food_Name, Special_Handling_Instructions, Quantity, Location 
           FROM food_listings 
           WHERE Special_Handling_Instructions IS NOT NULL 
           AND Special_Handling_Instructions != '' 
           ORDER BY Location""",
           
    "Food Allergen Tracking": 
        """SELECT Contains_Allergens, COUNT(*) as Count, SUM(Quantity) as Total_Quantity 
           FROM food_listings 
           GROUP BY Contains_Allergens 
           ORDER BY Total_Quantity DESC""",
           
    "Food Expiring in 4-7 Days": 
        """SELECT Food_ID, Food_Name, Quantity, Expiry_Date, Provider_Type, Location 
           FROM food_listings 
           WHERE DATE(Expiry_Date) BETWEEN DATE_ADD(CURDATE(), INTERVAL 4 DAY) AND DATE_ADD(CURDATE(), INTERVAL 7 DAY) 
           ORDER BY Expiry_Date""",
           
    "Quarterly Inventory Trends": 
        """SELECT 
           CONCAT(YEAR(Date_Added), '-Q', QUARTER(Date_Added)) as Quarter, 
           COUNT(*) as Listings, 
           SUM(Quantity) as Total_Quantity 
           FROM food_listings 
           GROUP BY Quarter 
           ORDER BY YEAR(Date_Added) DESC, QUARTER(Date_Added) DESC""",
           
    "Location Capacity Analysis": 
        """SELECT Location, 
           SUM(Quantity) as Current_Quantity,
           MAX(Location_Capacity) as Max_Capacity,
           (SUM(Quantity) / MAX(Location_Capacity)) * 100 as Capacity_Used_Percentage
           FROM food_listings
           JOIN locations ON food_listings.Location = locations.Location_Name
           GROUP BY Location
           ORDER BY Capacity_Used_Percentage DESC""",
           
    "Provider Consistency Analysis": 
        """SELECT Provider_Name, 
           COUNT(DISTINCT DATE_FORMAT(Date_Added, '%Y-%m')) as Months_Active,
           COUNT(*) as Total_Donations,
           COUNT(*) / COUNT(DISTINCT DATE_FORMAT(Date_Added, '%Y-%m')) as Avg_Monthly_Donations
           FROM food_listings
           GROUP BY Provider_Name
           HAVING Months_Active > 1
           ORDER BY Avg_Monthly_Donations DESC"""
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
