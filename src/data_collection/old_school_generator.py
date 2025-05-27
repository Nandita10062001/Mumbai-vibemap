import pandas as pd
import numpy as np
import requests
import json
from geopy.distance import geodesic
import time

# KICKIN' IT OLD SCHOOL - COMPLETE DATASET

# Colonial and Heritage locations in Mumbai with exact coordinates
old_school_locations = [
    # Colonial Architecture
    {"name": "Gateway of India", "lat": 18.9220, "lng": 72.8347, "type": "Colonial Monument", "area": "Colaba", "built_year": 1924, "heritage_status": "UNESCO World Heritage"},
    {"name": "Chhatrapati Shivaji Terminus", "lat": 18.9401, "lng": 72.8350, "type": "Colonial Railway", "area": "Fort", "built_year": 1887, "heritage_status": "UNESCO World Heritage"},
    {"name": "Taj Mahal Palace Hotel", "lat": 18.9216, "lng": 72.8331, "type": "Colonial Hotel", "area": "Colaba", "built_year": 1903, "heritage_status": "Grade I Heritage"},
    {"name": "High Court of Bombay", "lat": 18.9292, "lng": 72.8317, "type": "Colonial Government", "area": "Fort", "built_year": 1878, "heritage_status": "Grade I Heritage"},
    {"name": "University of Mumbai", "lat": 18.9292, "lng": 72.8317, "type": "Colonial Education", "area": "Fort", "built_year": 1857, "heritage_status": "Grade I Heritage"},
    {"name": "Mumbai Municipal Corporation Building", "lat": 18.9314, "lng": 72.8311, "type": "Colonial Government", "area": "Fort", "built_year": 1893, "heritage_status": "Grade I Heritage"},
    {"name": "St. Thomas Cathedral", "lat": 18.9314, "lng": 72.8311, "type": "Colonial Church", "area": "Fort", "built_year": 1718, "heritage_status": "Grade I Heritage"},
    {"name": "Asiatic Society Library", "lat": 18.9270, "lng": 72.8324, "type": "Colonial Library", "area": "Fort", "built_year": 1804, "heritage_status": "Grade II Heritage"},
    {"name": "General Post Office", "lat": 18.9379, "lng": 72.8354, "type": "Colonial Post", "area": "Fort", "built_year": 1913, "heritage_status": "Grade II Heritage"},
    {"name": "Prince of Wales Museum", "lat": 18.9269, "lng": 72.8324, "type": "Colonial Museum", "area": "Fort", "built_year": 1922, "heritage_status": "Grade I Heritage"},
    
    # Art Deco Buildings
    {"name": "Eros Cinema", "lat": 18.9314, "lng": 72.8289, "type": "Art Deco Cinema", "area": "Churchgate", "built_year": 1938, "heritage_status": "UNESCO World Heritage"},
    {"name": "Liberty Cinema", "lat": 18.9347, "lng": 72.8278, "type": "Art Deco Cinema", "area": "Marine Lines", "built_year": 1947, "heritage_status": "UNESCO World Heritage"},
    {"name": "Metro Cinema", "lat": 18.9347, "lng": 72.8278, "type": "Art Deco Cinema", "area": "Marine Lines", "built_year": 1938, "heritage_status": "UNESCO World Heritage"},
    {"name": "Regal Cinema", "lat": 18.9220, "lng": 72.8331, "type": "Art Deco Cinema", "area": "Colaba", "built_year": 1933, "heritage_status": "UNESCO World Heritage"},
    {"name": "Marine Drive Buildings", "lat": 18.9436, "lng": 72.8228, "type": "Art Deco Residential", "area": "Marine Drive", "built_year": 1940, "heritage_status": "UNESCO World Heritage"},
    {"name": "Oval Maidan Buildings", "lat": 18.9269, "lng": 72.8289, "type": "Art Deco Residential", "area": "Churchgate", "built_year": 1935, "heritage_status": "UNESCO World Heritage"},
    {"name": "Backbay Reclamation Buildings", "lat": 18.9380, "lng": 72.8250, "type": "Art Deco Residential", "area": "Nariman Point", "built_year": 1942, "heritage_status": "UNESCO World Heritage"},
    {"name": "New India Assurance Building", "lat": 18.9314, "lng": 72.8289, "type": "Art Deco Commercial", "area": "Fort", "built_year": 1936, "heritage_status": "Grade II Heritage"},
    
    # Industrial Heritage (Mills)
    {"name": "Phoenix Mills", "lat": 19.0134, "lng": 72.8333, "type": "Textile Mill", "area": "Lower Parel", "built_year": 1905, "heritage_status": "Converted Heritage"},
    {"name": "Century Mills", "lat": 19.0089, "lng": 72.8267, "type": "Textile Mill", "area": "Worli", "built_year": 1897, "heritage_status": "Industrial Heritage"},
    {"name": "Swadeshi Mills", "lat": 19.0178, "lng": 72.8356, "type": "Textile Mill", "area": "Parel", "built_year": 1886, "heritage_status": "Industrial Heritage"},
    {"name": "Standard Mills", "lat": 19.0145, "lng": 72.8334, "type": "Textile Mill", "area": "Lower Parel", "built_year": 1922, "heritage_status": "Industrial Heritage"},
    {"name": "Matulya Mills", "lat": 19.0089, "lng": 72.8267, "type": "Textile Mill", "area": "Lower Parel", "built_year": 1925, "heritage_status": "Industrial Heritage"},
    {"name": "Tata Mills", "lat": 19.0267, "lng": 72.8445, "type": "Textile Mill", "area": "Dadar", "built_year": 1912, "heritage_status": "Industrial Heritage"},
    
    # Historic Forts
    {"name": "Sewri Fort", "lat": 19.0067, "lng": 72.8556, "type": "Colonial Fort", "area": "Sewri", "built_year": 1680, "heritage_status": "ASI Protected"},
    {"name": "Mahim Fort", "lat": 19.0378, "lng": 72.8356, "type": "Colonial Fort", "area": "Mahim", "built_year": 1540, "heritage_status": "ASI Protected"},
    {"name": "Worli Fort", "lat": 19.0089, "lng": 72.8111, "type": "Colonial Fort", "area": "Worli", "built_year": 1675, "heritage_status": "ASI Protected"},
    {"name": "Sion Fort", "lat": 19.0434, "lng": 72.8634, "type": "Colonial Fort", "area": "Sion", "built_year": 1669, "heritage_status": "ASI Protected"},
    
    # Heritage Markets
    {"name": "Crawford Market", "lat": 18.9467, "lng": 72.8342, "type": "Colonial Market", "area": "Fort", "built_year": 1869, "heritage_status": "Grade I Heritage"},
    {"name": "Zaveri Bazaar", "lat": 18.9467, "lng": 72.8342, "type": "Historic Market", "area": "Zaveri Bazaar", "built_year": 1700, "heritage_status": "Historic Market"},
    {"name": "Mangaldas Market", "lat": 18.9467, "lng": 72.8300, "type": "Historic Market", "area": "Bhuleshwar", "built_year": 1850, "heritage_status": "Historic Market"},
    {"name": "Chor Bazaar", "lat": 18.9589, "lng": 72.8333, "type": "Historic Market", "area": "Chor Bazaar", "built_year": 1840, "heritage_status": "Historic Market"},
    
    # Colonial Clubs & Heritage Hotels
    {"name": "Bombay Gymkhana", "lat": 18.9269, "lng": 72.8289, "type": "Colonial Club", "area": "Fort", "built_year": 1875, "heritage_status": "Grade I Heritage"},
    {"name": "Royal Bombay Yacht Club", "lat": 18.9178, "lng": 72.8289, "type": "Colonial Club", "area": "Apollo Bunder", "built_year": 1846, "heritage_status": "Grade I Heritage"},
    {"name": "Wellington Club", "lat": 18.9269, "lng": 72.8289, "type": "Colonial Club", "area": "Fort", "built_year": 1860, "heritage_status": "Grade II Heritage"},
    
    # Additional Heritage Sites
    {"name": "Rajabai Clock Tower", "lat": 18.9292, "lng": 72.8317, "type": "Colonial Tower", "area": "Fort", "built_year": 1878, "heritage_status": "Grade I Heritage"},
    {"name": "Flora Fountain", "lat": 18.9314, "lng": 72.8311, "type": "Colonial Monument", "area": "Fort", "built_year": 1869, "heritage_status": "Grade I Heritage"},
    {"name": "Afghan Church", "lat": 18.9269, "lng": 72.8324, "type": "Colonial Church", "area": "Navy Nagar", "built_year": 1847, "heritage_status": "Grade I Heritage"},
    {"name": "Ballard Estate", "lat": 18.9379, "lng": 72.8400, "type": "Colonial District", "area": "Ballard Estate", "built_year": 1908, "heritage_status": "Heritage Precinct"},
    {"name": "Horniman Circle", "lat": 18.9314, "lng": 72.8311, "type": "Colonial Garden", "area": "Fort", "built_year": 1872, "heritage_status": "Grade I Heritage"},
    
    # Railway Heritage
    {"name": "Byculla Railway Workshop", "lat": 18.9789, "lng": 72.8334, "type": "Railway Heritage", "area": "Byculla", "built_year": 1860, "heritage_status": "Railway Heritage"},
    {"name": "Churchgate Railway Station", "lat": 18.9314, "lng": 72.8289, "type": "Colonial Railway", "area": "Churchgate", "built_year": 1930, "heritage_status": "Heritage Station"},
    {"name": "Grant Road Station", "lat": 18.9656, "lng": 72.8156, "type": "Colonial Railway", "area": "Grant Road", "built_year": 1925, "heritage_status": "Heritage Station"},
    
    # Additional Colonial Buildings
    {"name": "Reserve Bank of India", "lat": 18.9314, "lng": 72.8311, "type": "Colonial Bank", "area": "Fort", "built_year": 1939, "heritage_status": "Grade II Heritage"},
    {"name": "Customs House", "lat": 18.9379, "lng": 72.8400, "type": "Colonial Government", "area": "Ballard Estate", "built_year": 1720, "heritage_status": "Grade I Heritage"},
    {"name": "David Sassoon Library", "lat": 18.9589, "lng": 72.8333, "type": "Colonial Library", "area": "Kala Ghoda", "built_year": 1870, "heritage_status": "Grade I Heritage"},
    {"name": "Watson's Hotel", "lat": 18.9379, "lng": 72.8400, "type": "Colonial Hotel", "area": "Kala Ghoda", "built_year": 1869, "heritage_status": "Grade I Heritage"}
]

# FEATURE ENGINEERING - GENERATED DATA

def generate_heritage_osm_features(lat, lng, location_type, built_year, heritage_status):
    """Generate realistic OSM-based features for heritage locations"""
    
    features = {}
    
    # Calculate building age
    building_age = 2024 - built_year
    
    # Heritage building density (other heritage structures nearby)
    if heritage_status in ["UNESCO World Heritage", "Grade I Heritage"]:
        features['heritage_density'] = np.random.normal(12.5, 3.0)  # High heritage concentration
    elif heritage_status in ["Grade II Heritage", "ASI Protected"]:
        features['heritage_density'] = np.random.normal(8.2, 2.5)
    else:
        features['heritage_density'] = np.random.normal(4.1, 2.0)
    
    # Tourist attraction density
    if location_type in ["Colonial Monument", "Colonial Museum", "Art Deco Cinema"]:
        features['tourist_attraction_density'] = np.random.normal(15.8, 3.5)
    else:
        features['tourist_attraction_density'] = np.random.normal(6.4, 2.0)
    
    # Distance to nearest heritage precinct (meters)
    if heritage_status == "Heritage Precinct" or "Fort" in location_type:
        features['distance_to_heritage_precinct'] = np.random.normal(150, 80)
    else:
        features['distance_to_heritage_precinct'] = np.random.normal(850, 400)
    
    # Historical significance score (based on age and type)
    if building_age > 150:
        historical_base = 9.5
    elif building_age > 100:
        historical_base = 8.2
    elif building_age > 80:
        historical_base = 7.1
    else:
        historical_base = 5.8
    
    features['historical_significance'] = historical_base + np.random.normal(0, 0.8)
    
    # Commercial density (modern vs heritage balance)
    if "Fort" in location_type or "Market" in location_type:
        features['commercial_density'] = np.random.normal(18.5, 4.0)
    else:
        features['commercial_density'] = np.random.normal(8.7, 3.0)
    
    # Distance to nearest metro/railway (accessibility)
    if location_type in ["Colonial Railway", "Heritage Station"]:
        features['distance_to_transport'] = np.random.normal(100, 50)
    else:
        features['distance_to_transport'] = np.random.normal(650, 250)
    
    # Green space ratio (gardens, maidan nearby)
    if "Garden" in location_type or "Maidan" in str(lat):
        features['green_space_density'] = np.random.normal(25.4, 5.0)
    else:
        features['green_space_density'] = np.random.normal(8.9, 3.0)
    
    # Pedestrian area density
    features['pedestrian_area_density'] = np.random.normal(12.3, 4.0)
    
    # Conservation status score
    conservation_scores = {
        "UNESCO World Heritage": 9.8,
        "Grade I Heritage": 8.5,
        "ASI Protected": 7.8,
        "Grade II Heritage": 6.9,
        "Heritage Precinct": 7.5,
        "Industrial Heritage": 6.2,
        "Converted Heritage": 5.8,
        "Railway Heritage": 6.5,
        "Historic Market": 5.5,
        "Heritage Station": 6.8
    }
    
    features['conservation_score'] = conservation_scores.get(heritage_status, 5.0) + np.random.normal(0, 0.3)
    
    return {k: max(0, v) for k, v in features.items()}

def generate_heritage_foot_traffic(location_type, heritage_status, area):
    """Generate realistic foot traffic for heritage locations"""
    
    base_traffic = {
        "Colonial Monument": {"weekday": 2500, "weekend": 8500, "tourist_season": 15000},
        "Colonial Museum": {"weekday": 1800, "weekend": 4200, "tourist_season": 7500},
        "Art Deco Cinema": {"weekday": 850, "weekend": 2100, "tourist_season": 3200},
        "Colonial Railway": {"weekday": 25000, "weekend": 18000, "tourist_season": 28000},
        "Textile Mill": {"weekday": 450, "weekend": 1200, "tourist_season": 2800},
        "Colonial Fort": {"weekday": 380, "weekend": 1500, "tourist_season": 3500},
        "Historic Market": {"weekday": 5500, "weekend": 8900, "tourist_season": 12000},
        "Colonial Club": {"weekday": 280, "weekend": 450, "tourist_season": 680},
        "Art Deco Residential": {"weekday": 1200, "weekend": 2800, "tourist_season": 4500},
        "Colonial Government": {"weekday": 2100, "weekend": 800, "tourist_season": 1500},
        "Colonial Church": {"weekday": 450, "weekend": 1800, "tourist_season": 2200},
        "Colonial Library": {"weekday": 650, "weekend": 400, "tourist_season": 850},
        "Heritage Station": {"weekday": 15000, "weekend": 12000, "tourist_season": 18000}
    }
    
    # Area multipliers for different parts of Mumbai
    area_multipliers = {
        "Fort": 1.8, "Colaba": 1.6, "Churchgate": 1.5, "Marine Drive": 1.4,
        "Kala Ghoda": 1.7, "Ballard Estate": 1.2, "Lower Parel": 1.3
    }
    
    # Heritage status multipliers
    heritage_multipliers = {
        "UNESCO World Heritage": 1.8,
        "Grade I Heritage": 1.4,
        "ASI Protected": 1.2,
        "Grade II Heritage": 1.1,
        "Heritage Precinct": 1.3
    }
    
    area_mult = area_multipliers.get(area, 1.0)
    heritage_mult = heritage_multipliers.get(heritage_status, 1.0)
    
    base = base_traffic.get(location_type, {"weekday": 500, "weekend": 800, "tourist_season": 1200})
    
    return {
        "weekday_visitors": int(base["weekday"] * area_mult * heritage_mult * np.random.normal(1.0, 0.2)),
        "weekend_visitors": int(base["weekend"] * area_mult * heritage_mult * np.random.normal(1.0, 0.15)),
        "tourist_season_visitors": int(base["tourist_season"] * area_mult * heritage_mult * np.random.normal(1.0, 0.25)),
        "guided_tour_frequency": np.random.poisson(heritage_mult * 3),  # tours per day
        "photography_permits_daily": np.random.poisson(heritage_mult * 2)
    }

def generate_heritage_satellite_features(lat, lng, location_type, built_year):
    """Generate satellite imagery derived features for heritage sites"""
    
    building_age = 2024 - built_year
    
    # Land use classification with heritage considerations
    land_use = {
        "historic_building_density": np.random.normal(0.65, 0.15),  # 0-1 scale
        "modern_development_ratio": max(0, np.random.normal(0.4, 0.2)),  # Less modern development
        "green_heritage_space": np.random.normal(0.18, 0.12),  # Heritage gardens, courtyards
        "stone_masonry_coverage": np.random.normal(0.45, 0.15),  # Heritage building materials
        "tourist_infrastructure": np.random.normal(0.25, 0.10)  # Parking, signs, etc.
    }
    
    # Building characteristics
    if location_type in ["Colonial Monument", "Colonial Government", "Art Deco Cinema"]:
        building_features = {
            "avg_building_height": np.random.normal(5.8, 2.0),  # Heritage buildings often taller
            "heritage_building_density": np.random.normal(75, 20),  # Heritage buildings per hectare
            "architectural_uniformity": np.random.normal(0.78, 0.15),  # Similar architectural styles
            "facade_preservation_score": np.random.normal(0.82, 0.12)
        }
    elif location_type in ["Textile Mill", "Industrial Heritage"]:
        building_features = {
            "avg_building_height": np.random.normal(3.2, 1.0),  # Industrial buildings lower
            "heritage_building_density": np.random.normal(45, 15),
            "architectural_uniformity": np.random.normal(0.65, 0.18),
            "facade_preservation_score": np.random.normal(0.65, 0.20)
        }
    else:
        building_features = {
            "avg_building_height": np.random.normal(4.5, 1.5),
            "heritage_building_density": np.random.normal(60, 18),
            "architectural_uniformity": np.random.normal(0.72, 0.16),
            "facade_preservation_score": np.random.normal(0.75, 0.15)
        }
    
    # Heritage-specific features
    heritage_features = {
        "courtyard_open_space": np.random.normal(0.12, 0.08),
        "heritage_signage_density": np.random.normal(8.5, 3.0),  # Heritage plaques, signs per sq km
        "restoration_activity": np.random.normal(0.15, 0.10),  # Ongoing restoration work
        "tourist_pathway_density": np.random.normal(12.3, 4.0)  # Designated tourist paths
    }
    
    return {**land_use, **building_features, **heritage_features}

def generate_heritage_cultural_features(name, location_type, built_year, heritage_status):
    """Generate cultural and historical significance features"""
    
    # Calculate various cultural metrics
    building_age = 2024 - built_year
    
    # Architectural significance
    architectural_scores = {
        "Colonial Monument": 9.2,
        "Art Deco Cinema": 8.8,
        "Colonial Government": 8.5,
        "Colonial Railway": 8.2,
        "Textile Mill": 7.1,
        "Colonial Fort": 8.7,
        "Historic Market": 6.8,
        "Colonial Club": 7.5,
        "Art Deco Residential": 8.1
    }
    
    # Historical importance
    historical_importance = architectural_scores.get(location_type, 6.0)
    
    # Add significance for famous landmarks
    if "Gateway" in name or "Chhatrapati" in name or "Taj Mahal" in name:
        historical_importance += 1.5
    elif "University" in name or "High Court" in name:
        historical_importance += 1.0
    
    # Tourism appeal
    tourism_features = {
        "international_tourist_appeal": min(10, historical_importance + np.random.normal(0, 0.5)),
        "domestic_tourist_appeal": min(10, historical_importance - 0.5 + np.random.normal(0, 0.5)),
        "photography_popularity": np.random.normal(7.8, 1.5),
        "educational_value": np.random.normal(8.2, 1.2),
        "cultural_events_frequency": np.random.poisson(3),  # Events per month
        "heritage_walk_inclusion": 1 if heritage_status in ["UNESCO World Heritage", "Grade I Heritage"] else np.random.binomial(1, 0.6)
    }
    
    # Preservation metrics
    preservation_features = {
        "structural_integrity": np.random.normal(7.5, 1.5),
        "maintenance_frequency": np.random.normal(4.2, 1.0),  # Times per year
        "restoration_budget_index": np.random.normal(6.8, 2.0),  # 1-10 scale
        "conservation_priority": heritage_importance_score(heritage_status)
    }
    
    return {**tourism_features, **preservation_features, "architectural_significance": historical_importance}

def heritage_importance_score(heritage_status):
    """Calculate heritage importance score"""
    scores = {
        "UNESCO World Heritage": 9.8,
        "Grade I Heritage": 8.5,
        "ASI Protected": 8.0,
        "Grade II Heritage": 7.2,
        "Heritage Precinct": 7.8,
        "Industrial Heritage": 6.5,
        "Railway Heritage": 6.8,
        "Historic Market": 6.0,
        "Converted Heritage": 5.5,
        "Heritage Station": 7.0
    }
    return scores.get(heritage_status, 5.0) + np.random.normal(0, 0.3)

# GENERATE COMPLETE DATASET

def create_complete_old_school_dataset():
    """Generate the complete old school heritage dataset"""
    
    complete_data = []
    
    for i, location in enumerate(old_school_locations):
        # Basic location info
        loc_data = {
            'location_id': f"OS_{i+1:03d}",
            'name': location['name'],
            'lat': location['lat'],
            'lng': location['lng'],
            'type': location['type'],
            'area': location['area'],
            'built_year': location['built_year'],
            'heritage_status': location['heritage_status'],
            'vibe_category': 'Kickin\' it old school',
            'building_age': 2024 - location['built_year']
        }
        
        # OSM features
        osm_features = generate_heritage_osm_features(
            location['lat'], location['lng'], 
            location['type'], location['built_year'], location['heritage_status']
        )
        
        # foot traffic data
        traffic_data = generate_heritage_foot_traffic(
            location['type'], location['heritage_status'], location['area']
        )
        
        # satellite features
        satellite_features = generate_heritage_satellite_features(
            location['lat'], location['lng'], location['type'], location['built_year']
        )
        
        # cultural features
        cultural_features = generate_heritage_cultural_features(
            location['name'], location['type'], location['built_year'], location['heritage_status']
        )
        
        # vibe intensity
        vibe_intensity = calculate_heritage_vibe_intensity(
            location['type'], location['heritage_status'], location['name']
        )
        
        # Time-based features
        temporal_features = {
            "peak_visiting_hours": "10:00-17:00" if location['type'] != "Colonial Railway" else "07:00-22:00",
            "seasonal_variation": np.random.normal(0.3, 0.1),  # Higher in winter tourist season
            "guided_tour_availability": 1 if location['heritage_status'] in ["UNESCO World Heritage", "Grade I Heritage"] else np.random.binomial(1, 0.4)
        }
        
        # Combine all features
        complete_location = {
            **loc_data,
            **osm_features,
            **traffic_data,
            **satellite_features,
            **cultural_features,
            **temporal_features,
            'vibe_intensity': vibe_intensity,
            'data_collection_date': '2024-10-15',  # Cool heritage exploration season
            'confidence_score': np.random.normal(0.88, 0.08)
        }
        
        complete_data.append(complete_location)
    
    return pd.DataFrame(complete_data)

def calculate_heritage_vibe_intensity(location_type, heritage_status, name):
    """Calculate heritage vibe intensity based on location characteristics"""
    
    base_scores = {
        "Colonial Monument": 4.7,
        "Art Deco Cinema": 4.4,
        "Colonial Railway": 4.2,
        "Colonial Government": 4.0,
        "Textile Mill": 3.8,
        "Colonial Fort": 4.1,
        "Historic Market": 3.6,
        "Colonial Club": 3.9,
        "Art Deco Residential": 4.3,
        "Colonial Museum": 4.5,
        "Colonial Church": 3.9,
        "Colonial Library": 3.7,
        "Heritage Station": 3.8
    }
    
    # Heritage status boost
    status_boost = {
        "UNESCO World Heritage": 0.5,
        "Grade I Heritage": 0.3,
        "ASI Protected": 0.2,
        "Grade II Heritage": 0.1,
        "Heritage Precinct": 0.25
    }
    
    # Famous landmark boost
    famous_boost = 0
    if any(x in name for x in ["Gateway", "Chhatrapati", "Taj Mahal", "Marine Drive"]):
        famous_boost = 0.4
    elif any(x in name for x in ["University", "High Court", "Rajabai"]):
        famous_boost = 0.2
    
    base_score = base_scores.get(location_type, 3.5)
    heritage_boost = status_boost.get(heritage_status, 0)
    
    final_score = min(5.0, base_score + heritage_boost + famous_boost + np.random.normal(0, 0.12))
    
    return round(max(1.0, final_score), 2)
# HERITAGE WALK & TOUR DATA

def generate_heritage_walk_data():
    """Generate data about heritage walks and tours"""
    
    heritage_walks = [
        {
            "walk_name": "Fort Heritage Walk",
            "duration_hours": 3,
            "locations_covered": ["Gateway of India", "Taj Mahal Palace", "University of Mumbai", "High Court"],
            "difficulty": "Easy",
            "best_time": "Morning",
            "frequency_per_week": 14
        },
        {
            "walk_name": "Art Deco Architecture Tour",
            "duration_hours": 2.5,
            "locations_covered": ["Marine Drive Buildings", "Eros Cinema", "Liberty Cinema", "Oval Maidan"],
            "difficulty": "Easy",
            "best_time": "Evening",
            "frequency_per_week": 7
        },
        {
            "walk_name": "Mill District Heritage Tour",
            "duration_hours": 4,
            "locations_covered": ["Phoenix Mills", "Standard Mills", "Century Mills", "Swadeshi Mills"],
            "difficulty": "Moderate",
            "best_time": "Morning",
            "frequency_per_week": 5
        },
        {
            "walk_name": "Colonial Forts Trail",
            "duration_hours": 5,
            "locations_covered": ["Sewri Fort", "Mahim Fort", "Worli Fort", "Sion Fort"],
            "difficulty": "Moderate",
            "best_time": "Morning",
            "frequency_per_week": 3
        },
        {
            "walk_name": "Markets & Bazaars Heritage Walk",
            "duration_hours": 3.5,
            "locations_covered": ["Crawford Market", "Zaveri Bazaar", "Chor Bazaar", "Mangaldas Market"],
            "difficulty": "Easy",
            "best_time": "Morning",
            "frequency_per_week": 10
        }
    ]
    
    return heritage_walks

# MAIN EXECUTION

if __name__ == "__main__":
    # Generate the complete heritage dataset
    print("Generating 'Kickin' it old school' heritage dataset...")
    heritage_df = create_complete_old_school_dataset()
    
    # Save to CSV
    heritage_df.to_csv('old_school_heritage_dataset.csv', index=False)
    print(f"Heritage dataset saved! Shape: {heritage_df.shape}")

    print("\nSample heritage data:")
    print(heritage_df[['name', 'type', 'built_year', 'heritage_status', 'vibe_intensity', 'weekend_visitors']].head(10))
    
    # Generate heritage walks data
    heritage_walks = generate_heritage_walk_data()
    walks_df = pd.DataFrame(heritage_walks)
    walks_df.to_csv('heritage_walks_data.csv', index=False)
    print(f"\nHeritage walks data saved! {len(heritage_walks)} different walks available")
    # Summary statistics
    print(f"\nDataset Summary:")
    print(f"UNESCO World Heritage sites: {len([l for l in old_school_locations if l['heritage_status'] == 'UNESCO World Heritage'])}")
    print(f"Grade I Heritage sites: {len([l for l in old_school_locations if l['heritage_status'] == 'Grade I Heritage'])}")
    print(f"Colonial era buildings (pre-1850): {len([l for l in old_school_locations if l['built_year'] < 1850])}")
    print(f"Art Deco buildings (1920-1950): {len([l for l in old_school_locations if 1920 <= l['built_year'] <= 1950])}")
    print(f"Average building age: {np.mean([2024 - l['built_year'] for l in old_school_locations]):.1f} years")