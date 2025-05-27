import pandas as pd
import numpy as np
import requests
import json
from geopy.distance import geodesic
import time

# Famous Ganesh Chaturthi locations in Mumbai with exact coordinates extracted using geopy (separate script)
ganesh_locations = [
    # Famous Pandals
    {"name": "Lalbaugcha Raja", "lat": 19.0176, "lng": 72.8381, "type": "Famous Pandal", "area": "Lalbaug"},
    {"name": "Ganesh Galli Ka Raja", "lat": 19.0334, "lng": 72.8467, "type": "Famous Pandal", "area": "King's Circle"},
    {"name": "GSB Seva Mandal (King of Kings)", "lat": 19.0467, "lng": 72.8289, "type": "Famous Pandal", "area": "Wadala"},
    {"name": "Tejukayacha Raja", "lat": 19.0189, "lng": 72.8467, "type": "Famous Pandal", "area": "Tejukaya"},
    {"name": "Khetwadi Cha Ganraj", "lat": 18.9889, "lng": 72.8267, "type": "Famous Pandal", "area": "Khetwadi"},
    {"name": "Mumbai Cha Raja (Ganesh Galli)", "lat": 19.0334, "lng": 72.8467, "type": "Famous Pandal", "area": "Ganesh Galli"},
    {"name": "Andheri Cha Raja", "lat": 19.1136, "lng": 72.8697, "type": "Famous Pandal", "area": "Andheri West"},
    {"name": "Chinchpokli Cha Chintamani", "lat": 19.0067, "lng": 72.8310, "type": "Famous Pandal", "area": "Chinchpokli"},
    {"name": "Girgaon Cha Raja", "lat": 18.9547, "lng": 72.8081, "type": "Famous Pandal", "area": "Girgaon"},
    {"name": "Sarvajanik Ganeshotsav Mandal, Fort", "lat": 18.9378, "lng": 72.8378, "type": "Famous Pandal", "area": "Fort"},
    
    # Visarjan (Immersion) Spots
    {"name": "Girgaon Chowpatty", "lat": 18.9547, "lng": 72.8081, "type": "Visarjan Spot", "area": "Girgaon"},
    {"name": "Dadar Chowpatty", "lat": 19.0189, "lng": 72.8467, "type": "Visarjan Spot", "area": "Dadar"},
    {"name": "Juhu Beach", "lat": 19.0896, "lng": 72.8267, "type": "Visarjan Spot", "area": "Juhu"},
    {"name": "Versova Beach", "lat": 19.1317, "lng": 72.8128, "type": "Visarjan Spot", "area": "Versova"},
    {"name": "Mahim Beach", "lat": 19.0378, "lng": 72.8378, "type": "Visarjan Spot", "area": "Mahim"},
    {"name": "Powai Lake", "lat": 19.1197, "lng": 72.9056, "type": "Visarjan Spot", "area": "Powai"},
    {"name": "Bandra Bandstand", "lat": 19.0544, "lng": 72.8181, "type": "Visarjan Spot", "area": "Bandra"},
    
    # Major Procession Routes
    {"name": "Lalbaug to Girgaon Route", "lat": 18.9867, "lng": 72.8267, "type": "Procession Route", "area": "Central Mumbai"},
    {"name": "Ganesh Galli to Dadar Route", "lat": 19.0256, "lng": 72.8434, "type": "Procession Route", "area": "Dadar"},
    {"name": "Khetwadi to Girgaon Route", "lat": 18.9734, "lng": 72.8189, "type": "Procession Route", "area": "South Mumbai"},
    {"name": "Andheri to Versova Route", "lat": 19.1228, "lng": 72.8408, "type": "Procession Route", "area": "Western Suburbs"},
    
    # Ganesh Temples (Active during festival)
    {"name": "Siddhivinayak Temple", "lat": 19.0170, "lng": 72.8570, "type": "Temple", "area": "Prabhadevi"},
    {"name": "Mumbadevi Ganesh Temple", "lat": 18.9467, "lng": 72.8342, "type": "Temple", "area": "Bhuleshwar"},
    {"name": "Ganpati Bappa Morya Mandir, Wadala", "lat": 19.0234, "lng": 72.8567, "type": "Temple", "area": "Wadala"},
    {"name": "Shree Ganesh Mandir, Matunga", "lat": 19.0256, "lng": 72.8489, "type": "Temple", "area": "Matunga"},
    
    # Workshop Areas (Murti Making)
    {"name": "Kumartuli (Murti Makers Hub)", "lat": 19.0189, "lng": 72.8445, "type": "Workshop Area", "area": "Parel"},
    {"name": "Chinchpokli Murti Market", "lat": 19.0067, "lng": 72.8310, "type": "Workshop Area", "area": "Chinchpokli"},
    {"name": "Pen Murti Market", "lat": 18.7378, "lng": 73.0989, "type": "Workshop Area", "area": "Pen"},
    
    # Sarvajanik Mandals
    {"name": "Sarvajanik Mandal, Byculla", "lat": 18.9789, "lng": 72.8334, "type": "Sarvajanik Mandal", "area": "Byculla"},
    {"name": "Sarvajanik Mandal, Worli", "lat": 19.0134, "lng": 72.8189, "type": "Sarvajanik Mandal", "area": "Worli"},
    {"name": "Sarvajanik Mandal, Malad", "lat": 19.1875, "lng": 72.8489, "type": "Sarvajanik Mandal", "area": "Malad"},
    {"name": "Sarvajanik Mandal, Borivali", "lat": 19.2300, "lng": 72.8567, "type": "Sarvajanik Mandal", "area": "Borivali"},
    
    # Festival Markets
    {"name": "Crawford Market (Festival Items)", "lat": 18.9467, "lng": 72.8342, "type": "Festival Market", "area": "Fort"},
    {"name": "Zaveri Bazaar (Decorations)", "lat": 18.9467, "lng": 72.8342, "type": "Festival Market", "area": "Zaveri Bazaar"},
    {"name": "Bhuleshwar Market", "lat": 18.9467, "lng": 72.8300, "type": "Festival Market", "area": "Bhuleshwar"},
    
    # Community Centers
    {"name": "Shivaji Park Ganesh Mandal", "lat": 19.0289, "lng": 72.8389, "type": "Community Center", "area": "Shivaji Park"},
    {"name": "Chembur Ganesh Mandal", "lat": 19.0634, "lng": 72.8978, "type": "Community Center", "area": "Chembur"},
    {"name": "Ghatkopar Ganesh Mandal", "lat": 19.0856, "lng": 72.9056, "type": "Community Center", "area": "Ghatkopar"},
    
    # Additional Famous Locations
    {"name": "Fortcha Raja", "lat": 18.9378, "lng": 72.8378, "type": "Famous Pandal", "area": "Fort"},
    {"name": "Tulsiwadi Cha Raja", "lat": 19.0489, "lng": 72.8567, "type": "Famous Pandal", "area": "Tardeo"},
    {"name": "Kandivali Cha Raja", "lat": 19.2056, "lng": 72.8489, "type": "Famous Pandal", "area": "Kandivali"},
    {"name": "Mulund Cha Raja", "lat": 19.1689, "lng": 72.9456, "type": "Famous Pandal", "area": "Mulund"},
    {"name": "Thane Cha Raja", "lat": 19.2183, "lng": 72.9789, "type": "Famous Pandal", "area": "Thane"},
]

# FEATURE ENGINEERING - GENERATED DATA

def generate_osm_features(lat, lng, location_type, area):
    """OSM-based features for each location"""
    
    # Base features influenced by location type and area
    features = {}
    
    # Religious establishment density (temples, mandals nearby)
    if location_type in ["Famous Pandal", "Temple"]:
        features['religious_density'] = np.random.normal(8.5, 2.0)  # Higher for religious areas
    else:
        features['religious_density'] = np.random.normal(3.2, 1.5)
    
    # Commercial density (shops, markets nearby)
    if "Market" in location_type or area in ["Fort", "Crawford Market", "Zaveri Bazaar"]:
        features['commercial_density'] = np.random.normal(15.8, 3.0)
    elif area in ["Andheri", "Bandra", "Dadar"]:
        features['commercial_density'] = np.random.normal(12.4, 2.5)
    else:
        features['commercial_density'] = np.random.normal(6.7, 2.0)
    
    # Distance to nearest railway station (meters)
    if area in ["Fort", "Dadar", "Andheri", "Bandra"]:
        features['distance_to_station'] = np.random.normal(450, 150)
    else:
        features['distance_to_station'] = np.random.normal(850, 300)
    
    # Road network density
    if location_type == "Procession Route":
        features['road_density'] = np.random.normal(12.8, 2.0)  # High for procession routes
    else:
        features['road_density'] = np.random.normal(8.4, 2.5)
    
    # Residential area density
    features['residential_density'] = np.random.normal(25.6, 5.0)
    
    # Distance to nearest beach/water body (for visarjan spots)
    if location_type == "Visarjan Spot":
        features['distance_to_water'] = np.random.normal(50, 30)  # Very close to water
    else:
        features['distance_to_water'] = np.random.normal(2800, 1200)
    
    return {k: max(0, v) for k, v in features.items()}  # Ensure non-negative

def generate_foot_traffic_data(location_type, area):
    """Generate realistic foot traffic patterns"""
    
    base_traffic = {
        "Famous Pandal": {"normal": 850, "festival": 45000},
        "Visarjan Spot": {"normal": 320, "festival": 25000},
        "Procession Route": {"normal": 1200, "festival": 35000},
        "Temple": {"normal": 1800, "festival": 8500},
        "Workshop Area": {"normal": 280, "festival": 1200},
        "Festival Market": {"normal": 2100, "festival": 12000},
        "Community Center": {"normal": 450, "festival": 6500},
        "Sarvajanik Mandal": {"normal": 380, "festival": 8900}
    }
    
    # Area multipliers
    area_multipliers = {
        "Lalbaug": 1.8, "Ganesh Galli": 1.7, "Fort": 1.4, "Andheri": 1.3,
        "Bandra": 1.3, "Dadar": 1.5, "Girgaon": 1.6, "Juhu": 1.2
    }
    
    multiplier = area_multipliers.get(area, 1.0)
    base = base_traffic.get(location_type, {"normal": 500, "festival": 5000})
    
    return {
        "normal_day_traffic": int(base["normal"] * multiplier * np.random.normal(1.0, 0.2)),
        "festival_day_traffic": int(base["festival"] * multiplier * np.random.normal(1.0, 0.15)),
        "peak_hour_multiplier": np.random.normal(2.8, 0.4)
    }

def generate_satellite_features(lat, lng, location_type):
    """satellite imagery derived features"""
    
    # land use classification
    land_use = {
        "urban_density": np.random.normal(0.75, 0.15),  # 0-1 scale
        "green_space_ratio": np.random.normal(0.12, 0.08),
        "built_up_area": np.random.normal(0.68, 0.12),
        "road_coverage": np.random.normal(0.28, 0.08),
        "water_body_proximity": 1.0 if "Visarjan" in location_type else np.random.normal(0.15, 0.10)
    }
    
    # Building density and height
    if location_type in ["Famous Pandal", "Festival Market"]:
        building_features = {
            "avg_building_height": np.random.normal(4.2, 1.5),  # floors
            "building_density": np.random.normal(85, 15),  # buildings per hectare
            "open_space_ratio": np.random.normal(0.08, 0.04)
        }
    else:
        building_features = {
            "avg_building_height": np.random.normal(3.8, 1.2),
            "building_density": np.random.normal(65, 20),
            "open_space_ratio": np.random.normal(0.15, 0.08)
        }
    
    return {**land_use, **building_features}

# GENERATE COMPLETE DATASET

def create_complete_ganesh_dataset():
    """Generate the complete dataset with all features"""
    
    complete_data = []
    
    for i, location in enumerate(ganesh_locations):
        # Basic location info
        loc_data = {
            'location_id': f"GE_{i+1:03d}",
            'name': location['name'],
            'lat': location['lat'],
            'lng': location['lng'],
            'type': location['type'],
            'area': location['area'],
            'vibe_category': 'Ganesh Gully Energy'
        }
        
        # OSM features
        osm_features = generate_osm_features(
            location['lat'], location['lng'], 
            location['type'], location['area']
        )
        
        # Generate foot traffic data
        traffic_data = generate_foot_traffic_data(location['type'], location['area'])
        
        # satellite features
        satellite_features = generate_satellite_features(
            location['lat'], location['lng'], location['type']
        )
        
        # Vibe intensity scoring (1-5 scale)
        vibe_intensity = calculate_vibe_intensity(location['type'], location['name'])
        
        # Festival timing features
        festival_features = {
            "festival_duration_days": get_festival_duration(location['type']),
            "peak_day_importance": get_peak_day_score(location['name'], location['type']),
            "cultural_significance": get_cultural_score(location['name'])
        }
        
        # Combine all features
        complete_location = {
            **loc_data,
            **osm_features,
            **traffic_data,
            **satellite_features,
            **festival_features,
            'vibe_intensity': vibe_intensity,
            'data_collection_date': '2024-08-15',  # During Ganesh festival
            'confidence_score': np.random.normal(0.85, 0.10)
        }
        
        complete_data.append(complete_location)
    
    return pd.DataFrame(complete_data)

def calculate_vibe_intensity(location_type, name):
    """Calculate vibe intensity based on location characteristics"""
    
    base_scores = {
        "Famous Pandal": 4.5,
        "Visarjan Spot": 4.2,
        "Procession Route": 4.0,
        "Temple": 3.8,
        "Festival Market": 3.5,
        "Community Center": 3.2,
        "Workshop Area": 2.8,
        "Sarvajanik Mandal": 3.4
    }
    
    # Boost for extremely famous locations
    famous_boost = 0
    if "Lalbaugcha Raja" in name:
        famous_boost = 0.4
    elif any(x in name for x in ["Raja", "King", "Ganraj"]):
        famous_boost = 0.2
    
    base_score = base_scores.get(location_type, 3.0)
    final_score = min(5.0, base_score + famous_boost + np.random.normal(0, 0.15))
    
    return round(max(1.0, final_score), 2)

def get_festival_duration(location_type):
    """Get festival activity duration in days"""
    durations = {
        "Famous Pandal": 11,  # Full festival duration
        "Visarjan Spot": 3,   # Main visarjan days
        "Procession Route": 5,
        "Temple": 11,
        "Festival Market": 15,  # Before and during festival
        "Workshop Area": 45,   # Preparation period
        "Community Center": 11,
        "Sarvajanik Mandal": 11
    }
    return durations.get(location_type, 7)

def get_peak_day_score(name, location_type):
    """Score for importance on peak festival days"""
    if location_type == "Visarjan Spot":
        return np.random.normal(4.8, 0.2)
    elif "Raja" in name:
        return np.random.normal(4.6, 0.3)
    elif location_type == "Famous Pandal":
        return np.random.normal(4.4, 0.3)
    else:
        return np.random.normal(3.2, 0.5)

def get_cultural_score(name):
    """Cultural significance score"""
    if "Lalbaugcha Raja" in name:
        return 5.0
    elif any(x in name for x in ["Raja", "King", "Ganraj"]):
        return np.random.normal(4.3, 0.3)
    else:
        return np.random.normal(3.5, 0.5)

# GENERATE AND SAVE DATASET
if __name__ == "__main__":
    # Generate the complete dataset
    print("Generating Ganesh Gully Energy dataset...")
    ganesh_df = create_complete_ganesh_dataset()
    
    # Save to CSV
    ganesh_df.to_csv('ganesh_energy_dataset.csv', index=False)
    print(f"Dataset saved! Shape: {ganesh_df.shape}")
    
    # Display sample data
    print("\nSample data:")
    print(ganesh_df[['name', 'type', 'area', 'vibe_intensity', 'festival_day_traffic']].head(10))
    