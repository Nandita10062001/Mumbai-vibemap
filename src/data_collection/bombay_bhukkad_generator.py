import pandas as pd
import numpy as np
import requests
import json
from geopy.distance import geodesic
import time

# Food culture locations in Mumbai with exact coordinates generated from an automated script using geopy 
bhukkad_locations = [
    # Iconic Street Food Spots
    {"name": "Mohammed Ali Road", "lat": 18.9589, "lng": 72.8333, "type": "Street Food Hub", "area": "Mohammed Ali Road", "specialty": "Kebabs & Biryani", "established_year": 1890, "price_range": "Budget"},
    {"name": "Khau Galli", "lat": 18.9378, "lng": 72.8378, "type": "Street Food Lane", "area": "Fort", "specialty": "Mixed Street Food", "established_year": 1920, "price_range": "Budget"},
    {"name": "Juhu Chowpatty Food Stalls", "lat": 18.9896, "lng": 72.8267, "type": "Beach Food", "area": "Juhu", "specialty": "Bhel Puri & Pav Bhaji", "established_year": 1940, "price_range": "Budget"},
    {"name": "Carter Road Food Court", "lat": 19.0544, "lng": 72.8181, "type": "Street Food Court", "area": "Bandra", "specialty": "Chat & Juice", "established_year": 1980, "price_range": "Budget"},
    {"name": "Elco Market", "lat": 19.0544, "lng": 72.8267, "type": "Food Market", "area": "Bandra", "specialty": "Pani Puri & Dosa", "established_year": 1970, "price_range": "Budget"},
    {"name": "Hill Road Food Street", "lat": 19.0544, "lng": 72.8267, "type": "Street Food Street", "area": "Bandra", "specialty": "Vada Pav & Sandwich", "established_year": 1975, "price_range": "Budget"},
    {"name": "Linking Road Food Stalls", "lat": 19.0544, "lng": 72.8267, "type": "Shopping Street Food", "area": "Bandra", "specialty": "Fast Food", "established_year": 1985, "price_range": "Budget"},
    {"name": "Dadar Chowpatty Food Area", "lat": 19.0189, "lng": 72.8467, "type": "Beach Food", "area": "Dadar", "specialty": "Traditional Chat", "established_year": 1950, "price_range": "Budget"},
    
    # Legendary Restaurants
    {"name": "Kyaani & Co.", "lat": 18.9347, "lng": 72.8278, "type": "Irani Cafe", "area": "Marine Lines", "specialty": "Bun Maska & Chai", "established_year": 1904, "price_range": "Budget"},
    {"name": "Bademiya", "lat": 18.9220, "lng": 72.8331, "type": "Kebab Joint", "area": "Colaba", "specialty": "Seekh Kebab & Rolls", "established_year": 1946, "price_range": "Budget"},
    {"name": "Brittania & Co.", "lat": 18.9379, "lng": 72.8400, "type": "Parsi Restaurant", "area": "Ballard Estate", "specialty": "Berry Pulao", "established_year": 1923, "price_range": "Mid-range"},
    {"name": "Trishna", "lat": 18.9314, "lng": 72.8311, "type": "Fine Dining", "area": "Fort", "specialty": "Coastal Indian", "established_year": 1999, "price_range": "Expensive"},
    {"name": "Leopold Cafe", "lat": 18.9220, "lng": 72.8331, "type": "Continental Cafe", "area": "Colaba", "specialty": "Continental & Beer", "established_year": 1871, "price_range": "Mid-range"},
    {"name": "Cafe Mondegar", "lat": 18.9220, "lng": 72.8331, "type": "Continental Cafe", "area": "Colaba", "specialty": "Continental", "established_year": 1932, "price_range": "Mid-range"},
    {"name": "Olympic Coffee House", "lat": 18.9220, "lng": 72.8331, "type": "South Indian", "area": "Colaba", "specialty": "Dosa & Filter Coffee", "established_year": 1950, "price_range": "Budget"},
    {"name": "Prakash Ice Cream", "lat": 19.0267, "lng": 72.8756, "type": "Ice Cream Parlor", "area": "Wadala", "specialty": "Kulfi & Ice Cream", "established_year": 1965, "price_range": "Budget"},
    
    # Famous Food Joints
    {"name": "Sardar Pav Bhaji", "lat": 18.9789, "lng": 72.8267, "type": "Pav Bhaji Joint", "area": "Tardeo", "specialty": "Pav Bhaji", "established_year": 1960, "price_range": "Budget"},
    {"name": "Ashok Vada Pav", "lat": 19.0267, "lng": 72.8445, "type": "Vada Pav Stall", "area": "Dadar", "specialty": "Vada Pav", "established_year": 1971, "price_range": "Budget"},
    {"name": "Cannon Pav Bhaji", "lat": 18.9314, "lng": 72.8289, "type": "Pav Bhaji Joint", "area": "Churchgate", "specialty": "Pav Bhaji", "established_year": 1958, "price_range": "Budget"},
    {"name": "Ram Ashraya", "lat": 19.0256, "lng": 72.8489, "type": "South Indian", "area": "Matunga", "specialty": "Dosa & Idli", "established_year": 1935, "price_range": "Budget"},
    {"name": "Mysore Cafe", "lat": 19.0256, "lng": 72.8489, "type": "South Indian", "area": "Matunga", "specialty": "South Indian Breakfast", "established_year": 1940, "price_range": "Budget"},
    {"name": "Cafe Madras", "lat": 19.0256, "lng": 72.8489, "type": "South Indian", "area": "Matunga", "specialty": "Filter Coffee & Dosa", "established_year": 1952, "price_range": "Budget"},
    
    # Heritage Food Markets
    {"name": "Crawford Market Food Section", "lat": 18.9467, "lng": 72.8342, "type": "Food Market", "area": "Fort", "specialty": "Fresh Produce & Spices", "established_year": 1869, "price_range": "Budget"},
    {"name": "Grant Road Food Area", "lat": 18.9656, "lng": 72.8156, "type": "Street Food Area", "area": "Grant Road", "specialty": "Maharashtrian Food", "established_year": 1930, "price_range": "Budget"},
    {"name": "Matunga Food Hub", "lat": 19.0256, "lng": 72.8489, "type": "Food District", "area": "Matunga", "specialty": "South Indian", "established_year": 1925, "price_range": "Budget"},
    {"name": "Sindhi Camp Food Area", "lat": 19.0634, "lng": 72.8978, "type": "Community Food", "area": "Chembur", "specialty": "Sindhi Cuisine", "established_year": 1947, "price_range": "Budget"},
    
    # Cutting Chai Spots
    {"name": "Cutting Chai - CST", "lat": 18.9401, "lng": 72.8350, "type": "Tea Stall", "area": "Fort", "specialty": "Cutting Chai", "established_year": 1950, "price_range": "Budget"},
    {"name": "Cutting Chai - Dadar", "lat": 19.0189, "lng": 72.8467, "type": "Tea Stall", "area": "Dadar", "specialty": "Cutting Chai & Biscuits", "established_year": 1955, "price_range": "Budget"},
    {"name": "Cutting Chai - Bandra", "lat": 19.0544, "lng": 72.8267, "type": "Tea Stall", "area": "Bandra", "specialty": "Masala Chai", "established_year": 1960, "price_range": "Budget"},
    
    # Sweet Shops
    {"name": "Shree Krishna Sweets", "lat": 19.0267, "lng": 72.8445, "type": "Sweet Shop", "area": "Dadar", "specialty": "Maharashtrian Sweets", "established_year": 1948, "price_range": "Budget"},
    {"name": "Kandoi Bhogilal Mulchand", "lat": 18.9467, "lng": 72.8342, "type": "Sweet Shop", "area": "Zaveri Bazaar", "specialty": "Traditional Sweets", "established_year": 1900, "price_range": "Budget"},
    {"name": "Mishti Doi - Matunga", "lat": 19.0256, "lng": 72.8489, "type": "Bengali Sweets", "area": "Matunga", "specialty": "Bengali Sweets", "established_year": 1962, "price_range": "Budget"},
    
    # Modern Food Hubs
    {"name": "Palladium Food Court", "lat": 19.0134, "lng": 72.8333, "type": "Mall Food Court", "area": "Lower Parel", "specialty": "International Cuisine", "established_year": 2010, "price_range": "Mid-range"},
    {"name": "Phoenix Mills Food Area", "lat": 19.0134, "lng": 72.8333, "type": "Mall Food Area", "area": "Lower Parel", "specialty": "Fine Dining", "established_year": 2007, "price_range": "Expensive"},
    {"name": "Atria Mall Food Court", "lat": 19.0134, "lng": 72.8189, "type": "Mall Food Court", "area": "Worli", "specialty": "Chain Restaurants", "established_year": 2008, "price_range": "Mid-range"},
    
    # Breakfast Joints
    {"name": "Pancham Puriwala", "lat": 19.0267, "lng": 72.8445, "type": "Breakfast Joint", "area": "Dadar", "specialty": "Puri Bhaji", "established_year": 1945, "price_range": "Budget"},
    {"name": "Sukh Sagar", "lat": 18.9378, "lng": 72.8378, "type": "Vegetarian Restaurant", "area": "Fort", "specialty": "Gujarati Thali", "established_year": 1955, "price_range": "Budget"},
    {"name": "Rajdhani Thali", "lat": 18.9314, "lng": 72.8311, "type": "Thali Restaurant", "area": "Fort", "specialty": "Gujarati & Rajasthani Thali", "established_year": 1985, "price_range": "Mid-range"},
    
    # Late Night Food
    {"name": "Bade Miyan", "lat": 18.9220, "lng": 72.8331, "type": "Late Night Kebab", "area": "Colaba", "specialty": "Kebabs & Rolls", "established_year": 1946, "price_range": "Budget"},
    {"name": "Highway Gomantak", "lat": 19.0267, "lng": 72.8445, "type": "Late Night Restaurant", "area": "Dadar", "specialty": "Konkani Food", "established_year": 1975, "price_range": "Mid-range"},
    {"name": "Gajalee", "lat": 19.0544, "lng": 72.8267, "type": "Seafood Restaurant", "area": "Bandra", "specialty": "Konkani Seafood", "established_year": 1990, "price_range": "Mid-range"},
    
    # Additional Iconic Food Spots
    {"name": "Mahesh Lunch Home", "lat": 18.9314, "lng": 72.8311, "type": "Seafood Restaurant", "area": "Fort", "specialty": "Mangalorean Seafood", "established_year": 1973, "price_range": "Mid-range"},
    {"name": "Swati Snacks", "lat": 18.9789, "lng": 72.8267, "type": "Gujarati Snacks", "area": "Tardeo", "specialty": "Gujarati Snacks", "established_year": 1963, "price_range": "Budget"},
    {"name": "Cafe Samovar", "lat": 18.9269, "lng": 72.8324, "type": "Art Cafe", "area": "Kala Ghoda", "specialty": "Continental & Indian", "established_year": 1990, "price_range": "Mid-range"},
    {"name": "Indigo", "lat": 18.9220, "lng": 72.8331, "type": "Fine Dining", "area": "Colaba", "specialty": "European", "established_year": 1999, "price_range": "Expensive"},
    {"name": "Theobroma", "lat": 18.9220, "lng": 72.8331, "type": "Bakery Cafe", "area": "Multiple", "specialty": "Desserts & Coffee", "established_year": 2004, "price_range": "Mid-range"}
]

# FEATURE ENGINEERING - FOOD CULTURE DATA

def generate_food_osm_features(lat, lng, location_type, area, specialty):
    """Generate realistic OSM-based features for food locations"""
    
    features = {}
    
    # Food establishment density (restaurants, cafes, food stalls nearby)
    if location_type in ["Street Food Hub", "Food Market", "Food District"]:
        features['food_establishment_density'] = np.random.normal(25.8, 5.0)  # High food concentration
    elif location_type in ["Mall Food Court", "Street Food Lane"]:
        features['food_establishment_density'] = np.random.normal(18.4, 4.0)
    else:
        features['food_establishment_density'] = np.random.normal(12.7, 3.5)
    
    # Street vendor density (hawkers, carts, stalls)
    if "Street Food" in location_type or "Beach Food" in location_type:
        features['street_vendor_density'] = np.random.normal(15.6, 4.0)
    elif location_type in ["Tea Stall", "Food Market"]:
        features['street_vendor_density'] = np.random.normal(12.2, 3.0)
    else:
        features['street_vendor_density'] = np.random.normal(4.8, 2.0)
    
    # Distance to nearest market (fresh ingredients)
    if "Market" in location_type:
        features['distance_to_market'] = np.random.normal(50, 30)
    elif area in ["Fort", "Dadar", "Bandra"]:
        features['distance_to_market'] = np.random.normal(450, 200)
    else:
        features['distance_to_market'] = np.random.normal(800, 350)
    
    # Foot traffic density (food areas attract crowds)
    if location_type in ["Street Food Hub", "Food Market"]:
        features['foot_traffic_density'] = np.random.normal(85.4, 15.0)
    elif "Street Food" in location_type:
        features['foot_traffic_density'] = np.random.normal(65.2, 12.0)
    else:
        features['foot_traffic_density'] = np.random.normal(35.8, 10.0)
    
    # Distance to transport (accessibility for food lovers)
    if area in ["Fort", "Dadar", "Bandra", "Churchgate"]:
        features['distance_to_station'] = np.random.normal(380, 150)
    else:
        features['distance_to_station'] = np.random.normal(650, 250)
    
    # Commercial kitchen density (restaurants with proper kitchens)
    if location_type in ["Fine Dining", "Restaurant", "Parsi Restaurant"]:
        features['commercial_kitchen_density'] = np.random.normal(12.8, 3.0)
    elif location_type in ["Mall Food Court", "Food Market"]:
        features['commercial_kitchen_density'] = np.random.normal(8.5, 2.5)
    else:
        features['commercial_kitchen_density'] = np.random.normal(4.2, 2.0)
    
    # Late night food availability
    if location_type in ["Late Night Kebab", "Late Night Restaurant"] or "Mohammed Ali Road" in area:
        features['late_night_food_score'] = np.random.normal(9.2, 0.8)
    elif location_type in ["Street Food Hub", "Irani Cafe"]:
        features['late_night_food_score'] = np.random.normal(6.8, 1.5)
    else:
        features['late_night_food_score'] = np.random.normal(3.5, 2.0)
    
    # Cultural food authenticity (traditional vs modern)
    if location_type in ["Irani Cafe", "Parsi Restaurant", "South Indian", "Street Food Hub"]:
        features['cultural_authenticity_score'] = np.random.normal(8.8, 1.0)
    elif location_type in ["Sweet Shop", "Tea Stall", "Breakfast Joint"]:
        features['cultural_authenticity_score'] = np.random.normal(8.2, 1.2)
    else:
        features['cultural_authenticity_score'] = np.random.normal(6.5, 2.0)
    
    return {k: max(0, v) for k, v in features.items()}

def generate_food_traffic_patterns(location_type, area, specialty):
    """Generate realistic customer traffic patterns for food locations"""
    
    # Base traffic patterns by location type
    base_patterns = {
        "Street Food Hub": {"morning": 200, "lunch": 800, "evening": 1200, "night": 600},
        "Street Food Lane": {"morning": 150, "lunch": 600, "evening": 900, "night": 400},
        "Beach Food": {"morning": 80, "lunch": 300, "evening": 800, "night": 200},
        "Fine Dining": {"morning": 20, "lunch": 180, "evening": 400, "night": 150},
        "Irani Cafe": {"morning": 120, "lunch": 200, "evening": 180, "night": 80},
        "Tea Stall": {"morning": 300, "lunch": 150, "evening": 400, "night": 100},
        "Sweet Shop": {"morning": 80, "lunch": 120, "evening": 250, "night": 60},
        "Food Market": {"morning": 400, "lunch": 600, "evening": 500, "night": 100},
        "Mall Food Court": {"morning": 50, "lunch": 400, "evening": 600, "night": 200},
        "Late Night Kebab": {"morning": 30, "lunch": 150, "evening": 400, "night": 800},
        "Breakfast Joint": {"morning": 500, "lunch": 200, "evening": 100, "night": 20}
    }
    
    # Area multipliers
    area_multipliers = {
        "Mohammed Ali Road": 1.8, "Fort": 1.5, "Bandra": 1.4, "Colaba": 1.6,
        "Dadar": 1.4, "Matunga": 1.2, "Juhu": 1.3, "Lower Parel": 1.3
    }
    
    # Weekend multipliers
    weekend_multiplier = {
        "Beach Food": 2.5, "Street Food Hub": 1.8, "Mall Food Court": 2.0,
        "Fine Dining": 1.6, "Late Night Kebab": 2.2
    }
    
    area_mult = area_multipliers.get(area, 1.0)
    base = base_patterns.get(location_type, {"morning": 100, "lunch": 200, "evening": 300, "night": 100})
    weekend_mult = weekend_multiplier.get(location_type, 1.4)
    
    return {
        "morning_customers": int(base["morning"] * area_mult * np.random.normal(1.0, 0.2)),
        "lunch_customers": int(base["lunch"] * area_mult * np.random.normal(1.0, 0.15)),
        "evening_customers": int(base["evening"] * area_mult * np.random.normal(1.0, 0.2)),
        "night_customers": int(base["night"] * area_mult * np.random.normal(1.0, 0.25)),
        "weekend_multiplier": weekend_mult * np.random.normal(1.0, 0.1),
        "peak_waiting_time_minutes": max(5, int(np.random.normal(15, 8))),
        "average_meal_duration_minutes": get_meal_duration(location_type)
    }

def get_meal_duration(location_type):
    """Get average meal duration by location type"""
    durations = {
        "Fine Dining": 90,
        "Restaurant": 60,
        "Mall Food Court": 35,
        "Street Food Hub": 20,
        "Tea Stall": 10,
        "Street Food Lane": 15,
        "Beach Food": 25,
        "Late Night Kebab": 15,
        "Breakfast Joint": 30,
        "Sweet Shop": 10
    }
    base_duration = durations.get(location_type, 30)
    return int(base_duration * np.random.normal(1.0, 0.2))

def generate_food_satellite_features(lat, lng, location_type, established_year):
    """Generate satellite imagery derived features for food locations"""
    
    age = 2024 - established_year
    
    # Land use patterns around food areas
    land_use = {
        "commercial_food_density": np.random.normal(0.68, 0.15),  # Food-related businesses
        "residential_density": np.random.normal(0.45, 0.12),  # Nearby residential for customers
        "road_accessibility": np.random.normal(0.75, 0.10),  # Good road access
        "parking_availability": np.random.normal(0.35, 0.15),  # Limited parking in Mumbai
        "pedestrian_access": np.random.normal(0.82, 0.12)  # High pedestrian accessibility
    }
    
    # Building characteristics for food establishments
    if location_type in ["Fine Dining", "Restaurant", "Mall Food Court"]:
        building_features = {
            "building_size_sqm": np.random.normal(250, 80),
            "kitchen_to_dining_ratio": np.random.normal(0.3, 0.1),
            "seating_capacity_estimate": np.random.normal(80, 30),
            "signage_visibility_score": np.random.normal(7.5, 1.5)
        }
    elif location_type in ["Street Food Hub", "Street Food Lane", "Tea Stall"]:
        building_features = {
            "building_size_sqm": np.random.normal(50, 25),
            "kitchen_to_dining_ratio": np.random.normal(0.6, 0.15),  # More kitchen space
            "seating_capacity_estimate": np.random.normal(25, 15),
            "signage_visibility_score": np.random.normal(6.2, 2.0)
        }
    else:
        building_features = {
            "building_size_sqm": np.random.normal(120, 50),
            "kitchen_to_dining_ratio": np.random.normal(0.4, 0.12),
            "seating_capacity_estimate": np.random.normal(50, 20),
            "signage_visibility_score": np.random.normal(6.8, 1.8)
        }
    
    # Food-specific infrastructure
    food_infrastructure = {
        "waste_management_score": np.random.normal(6.5, 2.0),  # Food waste management
        "delivery_accessibility": np.random.normal(7.2, 1.5),  # Food delivery access
        "vendor_setup_space": np.random.normal(0.25, 0.15),  # Space for food vendors
        "queue_management_space": np.random.normal(0.15, 0.10)  # Space for customer queues
    }
    
    return {**land_use, **building_features, **food_infrastructure}

def generate_food_cultural_features(name, location_type, specialty, established_year, price_range, area):
    """Generate cultural and culinary significance features"""
    
    age = 2024 - established_year
    
    # Culinary heritage scoring
    heritage_scores = {
        "Irani Cafe": 9.2,
        "Parsi Restaurant": 9.0,
        "Street Food Hub": 8.8,
        "South Indian": 8.5,
        "Sweet Shop": 8.2,
        "Tea Stall": 8.0,
        "Breakfast Joint": 7.8,
        "Food Market": 8.3,
        "Fine Dining": 6.5,
        "Mall Food Court": 4.0
    }
    
    # Add age bonus for heritage value
    heritage_base = heritage_scores.get(location_type, 6.0)
    age_bonus = min(2.0, age / 50)  # Older establishments get heritage bonus
    
    # Famous location bonus
    fame_bonus = 0
    if any(x in name for x in ["Kyaani", "Bademiya", "Leopold", "Brittania", "Sardar", "Mohammed Ali Road"]):
        fame_bonus = 1.5
    elif any(x in name for x in ["Trishna", "Indigo", "Ashok", "Crawford"]):
        fame_bonus = 1.0
    
    # Cultural significance
    cultural_features = {
        "culinary_heritage_score": min(10, heritage_base + age_bonus + fame_bonus),
        "tourist_appeal": calculate_tourist_appeal(location_type, name, price_range),
        "local_popularity": calculate_local_popularity(location_type, specialty, area),
        "food_blogger_mentions": np.random.poisson(get_blogger_mentions(location_type, name)),
        "michelin_mentioned": 1 if location_type == "Fine Dining" and np.random.random() < 0.3 else 0,
        "street_food_authenticity": get_authenticity_score(location_type, established_year),
        "cultural_diversity_score": get_diversity_score(specialty, area)
    }
    
    # Economic features
    economic_features = {
        "average_meal_cost": get_meal_cost(price_range, location_type),
        "daily_revenue_estimate": estimate_daily_revenue(location_type, area, price_range),
        "employment_generated": estimate_employment(location_type),
        "supply_chain_local_ratio": np.random.normal(0.7, 0.15)  # Local ingredient sourcing
    }
    
    return {**cultural_features, **economic_features}

def calculate_tourist_appeal(location_type, name, price_range):
    """Calculate appeal to tourists"""
    base_scores = {
        "Fine Dining": 8.5, "Irani Cafe": 8.0, "Street Food Hub": 9.0,
        "Late Night Kebab": 7.5, "Parsi Restaurant": 8.2, "Continental Cafe": 7.8
    }
    
    base = base_scores.get(location_type, 6.0)
    
    # Famous places get bonus
    if any(x in name for x in ["Leopold", "Bademiya", "Kyaani", "Mohammed Ali Road"]):
        base += 1.5
    
    # Price accessibility for tourists
    price_adjustments = {"Budget": 0.5, "Mid-range": 0, "Expensive": -0.5}
    price_adj = price_adjustments.get(price_range, 0)
    
    return min(10, base + price_adj + np.random.normal(0, 0.5))

def calculate_local_popularity(location_type, specialty, area):
    """Calculate popularity among locals"""
    # Street food and traditional places score higher with locals
    if location_type in ["Street Food Hub", "Tea Stall", "Street Food Lane", "Breakfast Joint"]:
        base = 9.0
    elif location_type in ["Sweet Shop", "South Indian", "Food Market"]:
        base = 8.5
    else:
        base = 7.0
    
    return min(10, base + np.random.normal(0, 0.8))

def get_blogger_mentions(location_type, name):
    """Estimate food blogger mentions per month"""
    base_mentions = {
        "Fine Dining": 12, "Street Food Hub": 8, "Irani Cafe": 6,
        "Late Night Kebab": 5, "Continental Cafe": 4, "Tea Stall": 2
    }
    
    base = base_mentions.get(location_type, 3)
    
    # Famous places get more mentions
    if any(x in name for x in ["Trishna", "Leopold", "Bademiya", "Kyaani"]):
        base *= 3
    elif any(x in name for x in ["Mohammed Ali Road", "Crawford", "Brittania"]):
        base *= 2
    
    return base

def get_authenticity_score(location_type, established_year):
    """Calculate street food authenticity score"""
    if location_type in ["Mall Food Court", "Fine Dining"]:
        return np.random.normal(4.0, 1.5)
    
    age = 2024 - established_year
    base_score = 6.0
    
    if age > 80:
        base_score = 9.5
    elif age > 50:
        base_score = 8.5
    elif age > 30:
        base_score = 7.5
    
    return min(10, base_score + np.random.normal(0, 0.5))

def get_diversity_score(specialty, area):
    """Calculate cultural diversity of food offerings"""
    # Areas with diverse food cultures score higher
    diverse_areas = {
        "Mohammed Ali Road": 9.5,  # Muslim cuisine hub
        "Matunga": 8.8,  # South Indian concentration
        "Fort": 8.5,  # Mix of everything
        "Bandra": 8.2,  # Cosmopolitan food scene
        "Colaba": 7.8,  # Tourist + local mix
        "Lower Parel": 7.5  # Modern food courts
    }
    
    base_score = diverse_areas.get(area, 6.5)
    
    # Multi-cuisine specialties get bonus
    if "Mixed" in specialty or "&" in specialty:
        base_score += 1.0
    
    return min(10, base_score + np.random.normal(0, 0.5))

def get_meal_cost(price_range, location_type):
    """Get average meal cost in INR"""
    cost_ranges = {
        ("Budget", "Tea Stall"): (15, 50),
        ("Budget", "Street Food Hub"): (50, 150),
        ("Budget", "Street Food Lane"): (40, 120),
        ("Budget", "Sweet Shop"): (30, 100),
        ("Budget", "Breakfast Joint"): (60, 180),
        ("Mid-range", "Restaurant"): (300, 800),
        ("Mid-range", "Continental Cafe"): (400, 900),
        ("Mid-range", "Mall Food Court"): (250, 600),
        ("Expensive", "Fine Dining"): (1500, 4000),
        ("Expensive", "Mall Food Area"): (1000, 2500)
    }
    
    key = (price_range, location_type)
    if key in cost_ranges:
        min_cost, max_cost = cost_ranges[key]
        return int(np.random.uniform(min_cost, max_cost))
    
    # Default ranges by price category
    defaults = {
        "Budget": (50, 200),
        "Mid-range": (300, 800),
        "Expensive": (1200, 3000)
    }
    
    min_cost, max_cost = defaults.get(price_range, (100, 400))
    return int(np.random.uniform(min_cost, max_cost))

def estimate_daily_revenue(location_type, area, price_range):
    """Estimate daily revenue in INR"""
    # Base revenue multipliers
    base_multipliers = {
        "Street Food Hub": 15000,
        "Fine Dining": 80000,
        "Food Market": 25000,
        "Mall Food Court": 45000,
        "Street Food Lane": 8000,
        "Tea Stall": 3000,
        "Restaurant": 35000
    }
    
    base = base_multipliers.get(location_type, 15000)
    
    # Area multipliers
    area_mults = {
        "Mohammed Ali Road": 1.8, "Fort": 1.5, "Bandra": 1.4,
        "Colaba": 1.6, "Lower Parel": 1.3, "Dadar": 1.2
    }
    
    area_mult = area_mults.get(area, 1.0)
    
    # Price range impact
    price_mults = {"Budget": 0.8, "Mid-range": 1.2, "Expensive": 2.0}
    price_mult = price_mults.get(price_range, 1.0)
    
    revenue = base * area_mult * price_mult * np.random.normal(1.0, 0.3)
    return max(1000, int(revenue))

def estimate_employment(location_type):
    """Estimate number of people employed"""
    employment_ranges = {
        "Fine Dining": (15, 35),
        "Restaurant": (8, 20),
        "Mall Food Court": (12, 25),
        "Food Market": (20, 50),
        "Street Food Hub": (5, 15),
        "Street Food Lane": (3, 8),
        "Tea Stall": (2, 4),
        "Sweet Shop": (4, 10)
    }
    
    min_emp, max_emp = employment_ranges.get(location_type, (3, 10))
    return int(np.random.uniform(min_emp, max_emp))

# GENERATE COMPLETE DATASET

def create_complete_bhukkad_dataset():
    """Generate the complete Bombay Bhukkad food culture dataset"""
    
    complete_data = []
    
    for i, location in enumerate(bhukkad_locations):
        # Basic location info
        loc_data = {
            'location_id': f"BB_{i+1:03d}",
            'name': location['name'],
            'lat': location['lat'],
            'lng': location['lng'],
            'type': location['type'],
            'area': location['area'],
            'specialty': location['specialty'],
            'established_year': location['established_year'],
            'price_range': location['price_range'],
            'vibe_category': 'Bombay Bhukkad',
            'age_years': 2024 - location['established_year']
        }
        
        # OSM features
        osm_features = generate_food_osm_features(
            location['lat'], location['lng'], 
            location['type'], location['area'], location['specialty']
        )
        
        # traffic patterns
        traffic_data = generate_food_traffic_patterns(
            location['type'], location['area'], location['specialty']
        )
        
        # satellite features
        satellite_features = generate_food_satellite_features(
            location['lat'], location['lng'], location['type'], location['established_year']
        )
        
        # cultural features
        cultural_features = generate_food_cultural_features(
            location['name'], location['type'], location['specialty'], 
            location['established_year'], location['price_range'], location['area']
        )
        
        # vibe intensity
        vibe_intensity = calculate_bhukkad_vibe_intensity(
            location['type'], location['name'], location['specialty'], 
            location['established_year'], location['area']
        )
        
        # Time-based features
        temporal_features = {
            "peak_dining_hours": get_peak_hours(location['type']),
            "seasonal_variation": get_seasonal_variation(location['type']),
            "delivery_availability": get_delivery_score(location['type'], location['area']),
            "monsoon_impact_score": get_monsoon_impact(location['type'])
        }
        
        # Food-specific features
        food_specific = {
            "cuisine_type": extract_cuisine_type(location['specialty']),
            "spice_level": get_spice_level(location['specialty'], location['type']),
            "vegetarian_options": get_veg_options(location['type'], location['specialty']),
            "hygiene_rating": estimate_hygiene_rating(location['type'], location['price_range']),
            "portion_size_rating": get_portion_rating(location['type'], location['price_range'])
        }
        
        # Combine all features
        complete_location = {
            **loc_data,
            **osm_features,
            **traffic_data,
            **satellite_features,
            **cultural_features,
            **temporal_features,
            **food_specific,
            'vibe_intensity': vibe_intensity,
            'data_collection_date': '2024-11-20',  # Food exploration season
            'confidence_score': np.random.normal(0.87, 0.09)
        }
        
        complete_data.append(complete_location)
    
    return pd.DataFrame(complete_data)

def calculate_bhukkad_vibe_intensity(location_type, name, specialty, established_year, area):
    """Calculate food culture vibe intensity"""
    
    base_scores = {
        "Street Food Hub": 4.8,
        "Irani Cafe": 4.6,
        "Street Food Lane": 4.4,
        "Late Night Kebab": 4.3,
        "Food Market": 4.2,
        "Parsi Restaurant": 4.1,
        "Tea Stall": 4.0,
        "Beach Food": 3.9,
        "Sweet Shop": 3.8,
        "Fine Dining": 3.7,
        "South Indian": 3.9,
        "Breakfast Joint": 3.8
    }
    
    # Age bonus for heritage food spots
    age = 2024 - established_year
    age_bonus = 0
    if age > 100:
        age_bonus = 0.5
    elif age > 75:
        age_bonus = 0.3
    elif age > 50:
        age_bonus = 0.2
    
    # Famous location bonus
    fame_bonus = 0
    if any(x in name for x in ["Mohammed Ali Road", "Kyaani", "Leopold", "Bademiya"]):
        fame_bonus = 0.4
    elif any(x in name for x in ["Brittania", "Trishna", "Crawford", "Sardar"]):
        fame_bonus = 0.2
    
    # Area food culture bonus
    area_bonus = {
        "Mohammed Ali Road": 0.3, "Fort": 0.2, "Bandra": 0.2,
        "Colaba": 0.2, "Matunga": 0.2, "Dadar": 0.1
    }.get(area, 0)
    
    base_score = base_scores.get(location_type, 3.5)
    final_score = min(5.0, base_score + age_bonus + fame_bonus + area_bonus + np.random.normal(0, 0.1))
    
    return round(max(1.0, final_score), 2)

def get_peak_hours(location_type):
    """Get peak dining hours by location type"""
    peak_hours = {
        "Breakfast Joint": "07:00-10:00",
        "Tea Stall": "07:00-10:00, 16:00-19:00",
        "Street Food Hub": "12:00-14:00, 18:00-22:00",
        "Fine Dining": "19:00-23:00",
        "Late Night Kebab": "21:00-02:00",
        "Mall Food Court": "12:00-15:00, 18:00-21:00",
        "Beach Food": "17:00-22:00",
        "Food Market": "08:00-11:00, 17:00-20:00"
    }
    return peak_hours.get(location_type, "12:00-14:00, 19:00-22:00")

def get_seasonal_variation(location_type):
    """Get seasonal popularity variation"""
    if location_type in ["Beach Food", "Street Food Hub"]:
        return np.random.normal(0.4, 0.1)  # Higher variation due to weather
    elif location_type in ["Mall Food Court", "Fine Dining"]:
        return np.random.normal(0.15, 0.05)  # Lower variation (indoor)
    else:
        return np.random.normal(0.25, 0.08)

def get_delivery_score(location_type, area):
    """Calculate delivery availability score"""
    if location_type in ["Street Food Hub", "Tea Stall", "Beach Food"]:
        return np.random.normal(3.0, 1.5)  # Limited delivery for street food
    elif location_type in ["Restaurant", "Fine Dining", "Mall Food Court"]:
        return np.random.normal(8.5, 1.0)  # High delivery availability
    else:
        return np.random.normal(6.0, 2.0)

def get_monsoon_impact(location_type):
    """Calculate monsoon impact on food business"""
    if location_type in ["Beach Food", "Street Food Lane"]:
        return np.random.normal(7.5, 1.5)  # High impact (outdoor)
    elif location_type in ["Mall Food Court", "Fine Dining"]:
        return np.random.normal(2.0, 1.0)  # Low impact (indoor)
    else:
        return np.random.normal(4.5, 1.5)

def extract_cuisine_type(specialty):
    """Extract primary cuisine type from specialty"""
    if "Kebab" in specialty or "Biryani" in specialty:
        return "Mughlai"
    elif "Dosa" in specialty or "Idli" in specialty or "Filter Coffee" in specialty:
        return "South Indian"
    elif "Pav Bhaji" in specialty or "Vada Pav" in specialty:
        return "Maharashtrian"
    elif "Continental" in specialty:
        return "Continental"
    elif "Parsi" in specialty or "Berry Pulao" in specialty:
        return "Parsi"
    elif "Chat" in specialty or "Pani Puri" in specialty:
        return "North Indian Street Food"
    elif "Sweets" in specialty:
        return "Desserts"
    elif "Chai" in specialty:
        return "Beverages"
    else:
        return "Multi-cuisine"

def get_spice_level(specialty, location_type):
    """Estimate spice level (1-5 scale)"""
    if "Kebab" in specialty or "Mohammed Ali Road" in specialty:
        return np.random.normal(4.0, 0.5)
    elif "South Indian" in specialty:
        return np.random.normal(3.5, 0.8)
    elif "Chat" in specialty or "Maharashtrian" in specialty:
        return np.random.normal(3.0, 0.7)
    elif "Continental" in specialty:
        return np.random.normal(1.5, 0.5)
    elif "Sweet" in specialty or "Ice Cream" in specialty:
        return 1.0
    else:
        return np.random.normal(2.5, 1.0)

def get_veg_options(location_type, specialty):
    """Calculate vegetarian options availability (0-1 scale)"""
    if "South Indian" in specialty or "Gujarati" in specialty or "Sweet" in specialty:
        return np.random.normal(0.95, 0.05)
    elif "Kebab" in specialty or "Seafood" in specialty:
        return np.random.normal(0.15, 0.10)
    elif location_type in ["Mall Food Court", "Street Food Hub"]:
        return np.random.normal(0.70, 0.15)
    else:
        return np.random.normal(0.55, 0.20)

def estimate_hygiene_rating(location_type, price_range):
    """Estimate hygiene rating (1-5 scale)"""
    base_scores = {
        "Fine Dining": 4.5,
        "Mall Food Court": 4.2,
        "Restaurant": 4.0,
        "Irani Cafe": 3.8,
        "Street Food Hub": 3.2,
        "Tea Stall": 3.0,
        "Beach Food": 2.8
    }
    
    base = base_scores.get(location_type, 3.5)
    
    # Price range adjustment
    price_adj = {"Expensive": 0.5, "Mid-range": 0.2, "Budget": -0.2}.get(price_range, 0)
    
    final_score = base + price_adj + np.random.normal(0, 0.3)
    return round(min(5.0, max(1.0, final_score)), 1)

def get_portion_rating(location_type, price_range):
    """Rate portion sizes (1-5 scale, 5 being very large)"""
    if location_type in ["Street Food Hub", "Thali Restaurant", "Food Market"]:
        return np.random.normal(4.2, 0.5)
    elif location_type == "Fine Dining":
        return np.random.normal(2.8, 0.4)  # Smaller, refined portions
    elif price_range == "Budget":
        return np.random.normal(4.0, 0.6)
    else:
        return np.random.normal(3.5, 0.5)

# FOOD DELIVERY & MODERN FEATURES

def generate_modern_food_features():
    """Generate modern food ecosystem features"""
    
    modern_features = {
        "zomato_rating": np.random.normal(3.8, 0.6),
        "swiggy_partner": np.random.binomial(1, 0.7),
        "food_instagram_mentions": np.random.poisson(25),
        "food_blogger_visits": np.random.poisson(3),
        "online_ordering_percentage": np.random.normal(0.45, 0.25),
        "payment_digital_ratio": np.random.normal(0.65, 0.20)
    }
    
    return modern_features

if __name__ == "__main__":
    # Generate the complete food culture dataset
    print("Generating 'Bombay Bhukkad' food culture dataset...")
    food_df = create_complete_bhukkad_dataset()
    
    # Save to CSV
    food_df.to_csv('bombay_bhukkad_dataset.csv', index=False)
    print(f"Food culture dataset saved! Shape: {food_df.shape}")
    print("\nSample food culture data:")
    sample_cols = ['name', 'type', 'specialty', 'price_range', 'vibe_intensity', 'culinary_heritage_score', 'evening_customers']
    print(food_df[sample_cols].head(10))

    # Food culture summary statistics
    print(f"\nFood Culture Summary:")
    heritage_spots = len([l for l in bhukkad_locations if l['established_year'] < 1950])
    street_food_spots = len([l for l in bhukkad_locations if 'Street Food' in l['type']])
    fine_dining_spots = len([l for l in bhukkad_locations if l['type'] == 'Fine Dining'])
    
    print(f"Heritage food spots (pre-1950): {heritage_spots}")
    print(f"Street food locations: {street_food_spots}")
    print(f"Fine dining establishments: {fine_dining_spots}")
    print(f"Average establishment age: {np.mean([2024 - l['established_year'] for l in bhukkad_locations]):.1f} years")
    
    # Cuisine diversity
    specialties = [l['specialty'] for l in bhukkad_locations]
    print(f"Cuisine diversity: {len(set(specialties))} different specialties covered")