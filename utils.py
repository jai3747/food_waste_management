import sqlite3
import pandas as pd
import streamlit as st
import os
import datetime

# Database connection function
def get_connection():
    try:
        # Use an absolute path to your database or ensure it's in the correct directory
        conn = sqlite3.connect('food_waste.db', check_same_thread=False)
        return conn
    except Exception as e:
        st.error(f"Database connection error: {str(e)}")
        return None

# Initialize database with tables
def init_db():
    try:
        conn = get_connection()
        if not conn:
            return False
            
        cursor = conn.cursor()
        
        # Create tables if they don't exist
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS food_listings (
            Food_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Food_Name TEXT NOT NULL,
            Quantity INTEGER NOT NULL,
            Expiry_Date DATE NOT NULL,
            Provider_ID INTEGER NOT NULL,
            Provider_Type TEXT,
            Location TEXT,
            Food_Type TEXT,
            Meal_Type TEXT,
            Listed_Date DATE DEFAULT CURRENT_DATE
        )
        ''')
        
        # Check if the table is empty, if so, add sample data
        cursor.execute("SELECT COUNT(*) FROM food_listings")
        count = cursor.fetchone()[0]
        
        if count == 0:
            # Add sample data
            today = datetime.date.today()
            
            # Sample data with varied expiry dates
            sample_data = [
                ("Fresh Vegetables", 10, (today + datetime.timedelta(days=3)).isoformat(), 1, "Farm", "Downtown Market", "Vegetarian", "Dinner"),
                ("Bread Loaves", 20, (today + datetime.timedelta(days=1)).isoformat(), 2, "Bakery", "Main Street", "Vegan", "Breakfast"),
                ("Milk Cartons", 15, (today + datetime.timedelta(days=5)).isoformat(), 3, "Grocery Store", "North District", "Dairy", "Breakfast"),
                ("Cooked Pasta", 25, (today + datetime.timedelta(days=2)).isoformat(), 4, "Restaurant", "Downtown", "Vegetarian", "Lunch"),
                ("Fresh Fruits", 30, (today + datetime.timedelta(days=4)).isoformat(), 1, "Farm", "East Market", "Organic", "Snacks"),
                ("Chicken Curry", 8, (today + datetime.timedelta(days=1)).isoformat(), 5, "Restaurant", "South District", "Non-Vegetarian", "Dinner"),
                ("Pastries", 12, (today + datetime.timedelta(days=2)).isoformat(), 2, "Bakery", "West End", "Vegetarian", "Dessert"),
                ("Rice Bags", 5, (today + datetime.timedelta(days=30)).isoformat(), 6, "Supermarket", "Central Area", "Gluten-Free", "Dinner"),
                ("Fresh Juice", 18, (today + datetime.timedelta(days=3)).isoformat(), 7, "Juice Bar", "Market Square", "Organic", "Beverage"),
                ("Vegetable Soup", 15, (today + datetime.timedelta(days=2)).isoformat(), 4, "Restaurant", "Downtown", "Vegan", "Lunch")
            ]
            
            cursor.executemany('''
            INSERT INTO food_listings 
            (Food_Name, Quantity, Expiry_Date, Provider_ID, Provider_Type, Location, Food_Type, Meal_Type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', sample_data)
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Database initialization error: {str(e)}")
        return False

# Load food data from database - updated to not use ttl cache which can cause stale data
def load_food_data():
    try:
        conn = get_connection()
        if not conn:
            return pd.DataFrame()
            
        query = "SELECT * FROM food_listings ORDER BY Food_ID DESC"
        data = pd.read_sql_query(query, conn)
        conn.close()
        
        # Convert date strings to datetime objects
        if 'Expiry_Date' in data.columns and not data.empty:
            data['Expiry_Date'] = pd.to_datetime(data['Expiry_Date']).dt.date
        
        if 'Listed_Date' in data.columns and not data.empty:
            data['Listed_Date'] = pd.to_datetime(data['Listed_Date']).dt.date
            
        return data
    except Exception as e:
        st.error(f"Error loading food data: {str(e)}")
        return pd.DataFrame()

# Run a custom SQL query
def run_query(query):
    try:
        conn = get_connection()
        if not conn:
            return pd.DataFrame()
            
        result = pd.read_sql_query(query, conn)
        conn.close()
        return result
    except Exception as e:
        st.error(f"Error running query: {str(e)}")
        return pd.DataFrame()