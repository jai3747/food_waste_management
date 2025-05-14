#database.py
import mysql.connector
from mysql.connector import Error
import pandas as pd
import datetime
import streamlit as st
import os

def get_db_connection():
    """Create a database connection to MySQL."""
    try:
        # Get MySQL connection parameters from environment variables or secrets
        # For local development, you can set these in Streamlit secrets.toml file
        # https://docs.streamlit.io/library/advanced-features/secrets-management
        
        # First try to get from Streamlit secrets
        if hasattr(st, 'secrets') and 'mysql' in st.secrets:
            db_config = {
                'host': st.secrets.mysql.host,
                'user': st.secrets.mysql.user,
                'password': st.secrets.mysql.password,
                'database': st.secrets.mysql.database,
                'port': st.secrets.mysql.port if 'port' in st.secrets.mysql else 3306
            }
        else:
            # Fallback to environment variables
            db_config = {
                'host': os.environ.get('MYSQL_HOST', 'localhost'),
                'user': os.environ.get('MYSQL_USER', 'root'),
                'password': os.environ.get('MYSQL_PASSWORD', 'Bootlabs@123'),
                'database': os.environ.get('MYSQL_DATABASE', 'food_waste'),
                'port': int(os.environ.get('MYSQL_PORT', 3306))
            }
        
        # Connect to MySQL server
        conn = mysql.connector.connect(**db_config)
        
        # Enable autocommit
        conn.autocommit = True
        
        return conn
    except Error as e:
        st.error(f"MySQL connection error: {str(e)}")
        return None

def create_database():
    """Create the database and populate it with sample data."""
    try:
        conn = get_db_connection()
        if not conn:
            st.error("Failed to establish database connection")
            return False
            
        cursor = conn.cursor()
        
        # Get database name from config
        database_name = os.environ.get('MYSQL_DATABASE', 'food_waste')
        
        # Create database if it doesn't exist
        try:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
            cursor.execute(f"USE {database_name}")
        except Error as e:
            st.error(f"Error creating database: {str(e)}")
            return False
        
        # Create tables
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS food_listings (
            Food_ID INT AUTO_INCREMENT PRIMARY KEY,
            Food_Name VARCHAR(255) NOT NULL,
            Quantity INT NOT NULL,
            Expiry_Date DATE NOT NULL,
            Provider_ID INT,
            Provider_Type VARCHAR(100),
            Location VARCHAR(255),
            Food_Type VARCHAR(100),
            Meal_Type VARCHAR(100),
            Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Check if data already exists to avoid duplicates
        cursor.execute("SELECT COUNT(*) FROM food_listings")
        count = cursor.fetchone()[0]
        
        if count == 0:  # Only insert if table is empty
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
            
            # MySQL uses %s as placeholder instead of ? in SQLite
            cursor.executemany('''
            INSERT INTO food_listings 
            (Food_Name, Quantity, Expiry_Date, Provider_ID, Provider_Type, Location, Food_Type, Meal_Type)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ''', sample_data)
            
            conn.commit()
            st.success("Database created and populated with sample data!")
        
        conn.close()
        return True
        
    except Error as e:
        st.error(f"Error creating database: {str(e)}")
        return False
