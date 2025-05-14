#sql_queries.py
queries = {
    # SQL queries updated for MySQL syntax
    
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
    
    # More complex queries using MySQL-specific syntax
    
    "providers_per_city": 
        """SELECT city, COUNT(*) AS total_providers
           FROM food_providers
           GROUP BY city
           ORDER BY total_providers DESC""",
    
    "receivers_per_city": 
        """SELECT city, COUNT(*) AS total_receivers
           FROM food_receivers
           GROUP BY city
           ORDER BY total_receivers DESC""",
    
    "most_contributing_type": 
        """SELECT type, COUNT(*) AS contributions
           FROM food_providers
           JOIN food_listings ON food_providers.Provider_ID = food_listings.Provider_ID
           GROUP BY type
           ORDER BY contributions DESC""",
    
    "top_providers": 
        """SELECT p.Provider_ID, p.Name, p.Type, COUNT(*) AS listings_count
           FROM food_providers p
           JOIN food_listings f ON p.Provider_ID = f.Provider_ID
           GROUP BY p.Provider_ID
           ORDER BY listings_count DESC
           LIMIT 5""",
    
    "popular_food_types": 
        """SELECT fl.Food_Type, COUNT(*) AS claim_count
           FROM food_claims c
           JOIN food_listings fl ON c.Food_ID = fl.Food_ID
           GROUP BY fl.Food_Type
           ORDER BY claim_count DESC""",
    
    "meal_type_distribution": 
        """SELECT Meal_Type, COUNT(*) AS count
           FROM food_listings
           GROUP BY Meal_Type
           ORDER BY count DESC""",
    
    "claims_status": 
        """SELECT Status, COUNT(*) AS count
           FROM food_claims
           GROUP BY Status
           ORDER BY count DESC""",
    
    "city_food_availability": 
        """SELECT Location, SUM(Quantity) AS total_quantity
           FROM food_listings
           GROUP BY Location
           ORDER BY total_quantity DESC""",
    
    "most_active_receivers": 
        """SELECT r.Receiver_ID, r.Name, r.Type, COUNT(*) AS claim_count
           FROM food_receivers r
           JOIN food_claims c ON r.Receiver_ID = c.Receiver_ID
           GROUP BY r.Receiver_ID
           ORDER BY claim_count DESC
           LIMIT 10""",
    
    "avg_quantity_by_food_type": 
        """SELECT Food_Type, AVG(Quantity) AS avg_quantity
           FROM food_listings
           GROUP BY Food_Type
           ORDER BY avg_quantity DESC""",
    
    "unclaimed_food": 
        """SELECT fl.*
           FROM food_listings fl
           LEFT JOIN food_claims c ON fl.Food_ID = c.Food_ID
           WHERE c.Food_ID IS NULL
           ORDER BY fl.Expiry_Date""",
    
    "monthly_claim_trends": 
        """SELECT DATE_FORMAT(Timestamp, '%Y-%m') AS month, COUNT(*) AS claim_count
           FROM food_claims
           GROUP BY month
           ORDER BY month""",
    
    "provider_receiver_connections": 
        """SELECT p.Name AS provider_name, r.Name AS receiver_name, COUNT(*) AS connection_count
           FROM food_claims c
           JOIN food_listings fl ON c.Food_ID = fl.Food_ID
           JOIN food_providers p ON fl.Provider_ID = p.Provider_ID
           JOIN food_receivers r ON c.Receiver_ID = r.Receiver_ID
           GROUP BY p.Provider_ID, r.Receiver_ID
           ORDER BY connection_count DESC
           LIMIT 20""",
    
    "food_waste_reduction": 
        """SELECT
               'Total Available' AS category,
               SUM(fl.Quantity) AS total_quantity
           FROM food_listings fl
           
           UNION ALL
           
           SELECT
               'Claimed' AS category,
               SUM(fl.Quantity) AS total_quantity
           FROM food_listings fl
           JOIN food_claims c ON fl.Food_ID = c.Food_ID
           
           UNION ALL
           
           SELECT
               'Unclaimed' AS category,
               SUM(fl.Quantity) AS total_quantity
           FROM food_listings fl
           LEFT JOIN food_claims c ON fl.Food_ID = c.Food_ID
           WHERE c.Claim_ID IS NULL""",
    
    "receiver_type_distribution": 
        """SELECT Type, COUNT(*) AS count
           FROM food_receivers
           GROUP BY Type
           ORDER BY count DESC""",
    
    "claim_processing_time": 
        """SELECT 
               c.Claim_ID,
               c.Food_ID,
               r.Name AS receiver_name,
               p.Name AS provider_name,
               c.Status,
               c.Timestamp,
               DATEDIFF(c.Timestamp, fl.Expiry_Date) AS days_before_expiry
           FROM food_claims c
           JOIN food_listings fl ON c.Food_ID = fl.Food_ID
           JOIN food_providers p ON fl.Provider_ID = p.Provider_ID
           JOIN food_receivers r ON c.Receiver_ID = r.Receiver_ID
           ORDER BY days_before_expiry""",
    
    "local_distribution": 
        """SELECT 
               p.City AS provider_city,
               COUNT(*) AS local_claims_count
           FROM food_claims c
           JOIN food_listings fl ON c.Food_ID = fl.Food_ID
           JOIN food_providers p ON fl.Provider_ID = p.Provider_ID
           JOIN food_receivers r ON c.Receiver_ID = r.Receiver_ID
           WHERE p.City = r.City
           GROUP BY p.City
           ORDER BY local_claims_count DESC""",
    
    "top_food_receiver_combinations": 
        """SELECT 
               r.Name AS receiver_name, 
               fl.Food_Type,
               COUNT(*) AS claim_count
           FROM food_claims c
           JOIN food_listings fl ON c.Food_ID = fl.Food_ID
           JOIN food_receivers r ON c.Receiver_ID = r.Receiver_ID
           GROUP BY r.Receiver_ID, fl.Food_Type
           ORDER BY claim_count DESC
           LIMIT 15""",
    
    "seasonal_donation_trends": 
        """SELECT 
               DATE_FORMAT(fl.Expiry_Date, '%m') AS month,
               COUNT(*) AS listing_count,
               SUM(fl.Quantity) AS total_quantity,
               AVG(fl.Quantity) AS avg_quantity_per_listing
           FROM food_listings fl
           GROUP BY month
           ORDER BY month""",
    
    "food_shelf_life_efficiency": 
        """SELECT
               fl.Food_Type,
               COUNT(*) AS item_count,
               AVG(CASE WHEN c.Claim_ID IS NOT NULL THEN 1 ELSE 0 END) * 100 AS claim_percentage,
               AVG(fl.Quantity) AS avg_quantity_per_item
           FROM food_listings fl
           LEFT JOIN food_claims c ON fl.Food_ID = c.Food_ID
           GROUP BY fl.Food_Type
           ORDER BY claim_percentage DESC""",
    
    "food_waste_reduction_by_location": 
        """SELECT
               fl.Location,
               COUNT(fl.Food_ID) AS total_listings,
               COUNT(c.Claim_ID) AS claimed_listings,
               ROUND(COUNT(c.Claim_ID) * 100.0 / COUNT(fl.Food_ID), 1) AS claimed_percentage,
               SUM(fl.Quantity) AS total_quantity,
               SUM(CASE WHEN c.Claim_ID IS NOT NULL THEN fl.Quantity ELSE 0 END) AS claimed_quantity
           FROM food_listings fl
           LEFT JOIN food_claims c ON fl.Food_ID = c.Food_ID
           GROUP BY fl.Location
           ORDER BY claimed_percentage DESC"""
}
