queries = {
    # 1. Providers per city
    "providers_per_city": """
        SELECT city, COUNT(*) AS total_providers
        FROM food_providers
        GROUP BY city
        ORDER BY total_providers DESC
    """,
    
    # 2. Receivers per city
    "receivers_per_city": """
        SELECT city, COUNT(*) AS total_receivers
        FROM food_receivers
        GROUP BY city
        ORDER BY total_receivers DESC
    """,
    
    # 3. Most contributing provider type
    "most_contributing_type": """
        SELECT type, COUNT(*) AS contributions
        FROM food_providers
        JOIN food_listings ON food_providers.Provider_ID = food_listings.Provider_ID
        GROUP BY type
        ORDER BY contributions DESC
    """,
    
    # 4. Top 5 providers by number of food listings
    "top_providers": """
        SELECT p.Provider_ID, p.Name, p.Type, COUNT(*) AS listings_count
        FROM food_providers p
        JOIN food_listings f ON p.Provider_ID = f.Provider_ID
        GROUP BY p.Provider_ID
        ORDER BY listings_count DESC
        LIMIT 5
    """,
    
    # 5. Most claimed food types
    "popular_food_types": """
        SELECT fl.Food_Type, COUNT(*) AS claim_count
        FROM food_claims c
        JOIN food_listings fl ON c.Food_ID = fl.Food_ID
        GROUP BY fl.Food_Type
        ORDER BY claim_count DESC
    """,
    
    # 6. Distribution of meal types
    "meal_type_distribution": """
        SELECT Meal_Type, COUNT(*) AS count
        FROM food_listings
        GROUP BY Meal_Type
        ORDER BY count DESC
    """,
    
    # 7. Claims status distribution
    "claims_status": """
        SELECT Status, COUNT(*) AS count
        FROM food_claims
        GROUP BY Status
        ORDER BY count DESC
    """,
    
    # 8. City with highest food availability
    "city_food_availability": """
        SELECT Location, SUM(Quantity) AS total_quantity
        FROM food_listings
        GROUP BY Location
        ORDER BY total_quantity DESC
    """,
    
    # 9. Most active receivers (by claim count)
    "most_active_receivers": """
        SELECT r.Receiver_ID, r.Name, r.Type, COUNT(*) AS claim_count
        FROM food_receivers r
        JOIN food_claims c ON r.Receiver_ID = c.Receiver_ID
        GROUP BY r.Receiver_ID
        ORDER BY claim_count DESC
        LIMIT 10
    """,
    
    # 10. Average quantity per food type
    "avg_quantity_by_food_type": """
        SELECT Food_Type, AVG(Quantity) AS avg_quantity
        FROM food_listings
        GROUP BY Food_Type
        ORDER BY avg_quantity DESC
    """,
    
    # 11. Unclaimed food items
    "unclaimed_food": """
        SELECT fl.*
        FROM food_listings fl
        LEFT JOIN food_claims c ON fl.Food_ID = c.Food_ID
        WHERE c.Food_ID IS NULL
        ORDER BY fl.Expiry_Date
    """,
    
    # 12. Monthly claim trends
    "monthly_claim_trends": """
        SELECT strftime('%Y-%m', Timestamp) AS month, COUNT(*) AS claim_count
        FROM food_claims
        GROUP BY month
        ORDER BY month
    """,
    
    # 13. Provider-receiver connections
    "provider_receiver_connections": """
        SELECT p.Name AS provider_name, r.Name AS receiver_name, COUNT(*) AS connection_count
        FROM food_claims c
        JOIN food_listings fl ON c.Food_ID = fl.Food_ID
        JOIN food_providers p ON fl.Provider_ID = p.Provider_ID
        JOIN food_receivers r ON c.Receiver_ID = r.Receiver_ID
        GROUP BY p.Provider_ID, r.Receiver_ID
        ORDER BY connection_count DESC
        LIMIT 20
    """,
    
    # 14. Food waste reduction metrics
    "food_waste_reduction": """
        SELECT
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
        WHERE c.Claim_ID IS NULL
    """,
    
    # 15. Receiver type distribution
    "receiver_type_distribution": """
        SELECT Type, COUNT(*) AS count
        FROM food_receivers
        GROUP BY Type
        ORDER BY count DESC
    """,
    
    # 16. Claims processing time
    "claim_processing_time": """
        SELECT 
            c.Claim_ID,
            c.Food_ID,
            r.Name AS receiver_name,
            p.Name AS provider_name,
            c.Status,
            c.Timestamp,
            julianday(c.Timestamp) - julianday(fl.Expiry_Date) AS days_before_expiry
        FROM food_claims c
        JOIN food_listings fl ON c.Food_ID = fl.Food_ID
        JOIN food_providers p ON fl.Provider_ID = p.Provider_ID
        JOIN food_receivers r ON c.Receiver_ID = r.Receiver_ID
        ORDER BY days_before_expiry
    """,
    
    # 17. Provider and receiver in same city
    "local_distribution": """
        SELECT 
            p.City AS provider_city,
            COUNT(*) AS local_claims_count
        FROM food_claims c
        JOIN food_listings fl ON c.Food_ID = fl.Food_ID
        JOIN food_providers p ON fl.Provider_ID = p.Provider_ID
        JOIN food_receivers r ON c.Receiver_ID = r.Receiver_ID
        WHERE p.City = r.City
        GROUP BY p.City
        ORDER BY local_claims_count DESC
    """,
    
    # 18. Top food-receiver combinations
    "top_food_receiver_combinations": """
        SELECT 
            r.Name AS receiver_name, 
            fl.Food_Type,
            COUNT(*) AS claim_count
        FROM food_claims c
        JOIN food_listings fl ON c.Food_ID = fl.Food_ID
        JOIN food_receivers r ON c.Receiver_ID = r.Receiver_ID
        GROUP BY r.Receiver_ID, fl.Food_Type
        ORDER BY claim_count DESC
        LIMIT 15
    """,
    
    # 19. Seasonal trends in food donations
    "seasonal_donation_trends": """
        SELECT 
            strftime('%m', fl.Expiry_Date) AS month,
            COUNT(*) AS listing_count,
            SUM(fl.Quantity) AS total_quantity,
            AVG(fl.Quantity) AS avg_quantity_per_listing
        FROM food_listings fl
        GROUP BY month
        ORDER BY month
    """,
    
    # 20. Food shelf-life efficiency tracking
    "food_shelf_life_efficiency": """
        SELECT
            fl.Food_Type,
            COUNT(*) AS item_count,
            AVG(CASE WHEN c.Claim_ID IS NOT NULL THEN 1 ELSE 0 END) * 100 AS claim_percentage,
            AVG(fl.Quantity) AS avg_quantity_per_item
        FROM food_listings fl
        LEFT JOIN food_claims c ON fl.Food_ID = c.Food_ID
        GROUP BY fl.Food_Type
        ORDER BY claim_percentage DESC
    """,
    
    # 21. Food waste reduction by location
    "food_waste_reduction_by_location": """
        SELECT
            fl.Location,
            COUNT(fl.Food_ID) AS total_listings,
            COUNT(c.Claim_ID) AS claimed_listings,
            ROUND(COUNT(c.Claim_ID) * 100.0 / COUNT(fl.Food_ID), 1) AS claimed_percentage,
            SUM(fl.Quantity) AS total_quantity,
            SUM(CASE WHEN c.Claim_ID IS NOT NULL THEN fl.Quantity ELSE 0 END) AS claimed_quantity
        FROM food_listings fl
        LEFT JOIN food_claims c ON fl.Food_ID = c.Food_ID
        GROUP BY fl.Location
        ORDER BY claimed_percentage DESC
    """
}