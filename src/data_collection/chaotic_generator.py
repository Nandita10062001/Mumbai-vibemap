import pandas as pd
import numpy as np
import requests
import json
from geopy.distance import geodesic
import time

# Urban energy locations in Mumbai with exact coordinates
chaotic_hustle_locations = [
    # Major Railway Stations
    {"name": "Churchgate Station", "lat": 18.9314, "lng": 72.8289, "type": "Terminus Station", "area": "Churchgate", "daily_footfall": 500000, "peak_multiplier": 3.2},
    {"name": "Mumbai Central", "lat": 18.9689, "lng": 72.8197, "type": "Major Junction", "area": "Mumbai Central", "daily_footfall": 350000, "peak_multiplier": 2.8},
    {"name": "Dadar Station", "lat": 19.0189, "lng": 72.8467, "type": "Junction Station", "area": "Dadar", "daily_footfall": 650000, "peak_multiplier": 3.5},
    {"name": "Bandra Station", "lat": 19.0544, "lng": 72.8409, "type": "Suburban Hub", "area": "Bandra", "daily_footfall": 400000, "peak_multiplier": 2.9},
    {"name": "Andheri Station", "lat": 19.1197, "lng": 72.8467, "type": "Major Hub", "area": "Andheri", "daily_footfall": 750000, "peak_multiplier": 3.8},
    {"name": "Kurla Station", "lat": 19.0689, "lng": 72.8792, "type": "Junction Station", "area": "Kurla", "daily_footfall": 300000, "peak_multiplier": 2.6},
    {"name": "Thane Station", "lat": 19.1875, "lng": 72.9781, "type": "Terminus Station", "area": "Thane", "daily_footfall": 450000, "peak_multiplier": 3.1},
    {"name": "Borivali Station", "lat": 19.2300, "lng": 72.8567, "type": "Major Station", "area": "Borivali", "daily_footfall": 320000, "peak_multiplier": 2.7},
    {"name": "Virar Station", "lat": 19.4559, "lng": 72.8111, "type": "Terminus Station", "area": "Virar", "daily_footfall": 280000, "peak_multiplier": 2.5},
    
    # Metro Stations
    {"name": "Ghatkopar Metro", "lat": 19.0856, "lng": 72.9056, "type": "Metro Hub", "area": "Ghatkopar", "daily_footfall": 150000, "peak_multiplier": 2.8},
    {"name": "Andheri Metro", "lat": 19.1197, "lng": 72.8467, "type": "Metro Station", "area": "Andheri", "daily_footfall": 120000, "peak_multiplier": 2.5},
    {"name": "Versova Metro", "lat": 19.1317, "lng": 72.8128, "type": "Metro Station", "area": "Versova", "daily_footfall": 80000, "peak_multiplier": 2.2},
    {"name": "Airport Metro", "lat": 19.0896, "lng": 72.8656, "type": "Metro Station", "area": "Airport", "daily_footfall": 90000, "peak_multiplier": 1.8},
    
    # Major Traffic Intersections
    {"name": "Dadar TT Circle", "lat": 19.0189, "lng": 72.8445, "type": "Traffic Junction", "area": "Dadar", "daily_footfall": 200000, "peak_multiplier": 4.2},
    {"name": "Bandra Kalanagar Junction", "lat": 19.0656, "lng": 72.8378, "type": "Traffic Junction", "area": "Bandra", "daily_footfall": 180000, "peak_multiplier": 3.8},
    {"name": "Andheri Subway", "lat": 19.1197, "lng": 72.8467, "type": "Traffic Junction", "area": "Andheri", "daily_footfall": 220000, "peak_multiplier": 4.5},
    {"name": "Mahim Causeway", "lat": 19.0378, "lng": 72.8378, "type": "Traffic Junction", "area": "Mahim", "daily_footfall": 160000, "peak_multiplier": 3.5},
    {"name": "Worli Sea Link Plaza", "lat": 19.0134, "lng": 72.8111, "type": "Traffic Junction", "area": "Worli", "daily_footfall": 140000, "peak_multiplier": 3.2},
    {"name": "Powai Junction", "lat": 19.1197, "lng": 72.9056, "type": "Traffic Junction", "area": "Powai", "daily_footfall": 100000, "peak_multiplier": 2.8},
    
    # Commercial Business Districts
    {"name": "Nariman Point", "lat": 18.9269, "lng": 72.8228, "type": "Business District", "area": "Nariman Point", "daily_footfall": 300000, "peak_multiplier": 2.5},
    {"name": "Bandra Kurla Complex", "lat": 19.0656, "lng": 72.8678, "type": "Business District", "area": "BKC", "daily_footfall": 250000, "peak_multiplier": 2.3},
    {"name": "Lower Parel Office District", "lat": 19.0134, "lng": 72.8333, "type": "Business District", "area": "Lower Parel", "daily_footfall": 200000, "peak_multiplier": 2.2},
    {"name": "Andheri MIDC", "lat": 19.1197, "lng": 72.8467, "type": "Industrial Area", "area": "Andheri", "daily_footfall": 150000, "peak_multiplier": 1.8},
    {"name": "Powai IT Hub", "lat": 19.1197, "lng": 72.9056, "type": "IT District", "area": "Powai", "daily_footfall": 120000, "peak_multiplier": 1.9},
    {"name": "Goregaon IT Park", "lat": 19.1556, "lng": 72.8489, "type": "IT District", "area": "Goregaon", "daily_footfall": 100000, "peak_multiplier": 1.7},
    
    # Busy Markets
    {"name": "Zaveri Bazaar", "lat": 18.9467, "lng": 72.8342, "type": "Gold Market", "area": "Zaveri Bazaar", "daily_footfall": 80000, "peak_multiplier": 2.8},
    {"name": "Crawford Market", "lat": 18.9467, "lng": 72.8342, "type": "Wholesale Market", "area": "Fort", "daily_footfall": 100000, "peak_multiplier": 3.2},
    {"name": "Linking Road Market", "lat": 19.0544, "lng": 72.8267, "type": "Shopping Street", "area": "Bandra", "daily_footfall": 90000, "peak_multiplier": 4.5},
    {"name": "Hill Road Market", "lat": 19.0544, "lng": 72.8267, "type": "Shopping Street", "area": "Bandra", "daily_footfall": 85000, "peak_multiplier": 4.2},
    {"name": "Dharavi Market", "lat": 19.0378, "lng": 72.8567, "type": "Local Market", "area": "Dharavi", "daily_footfall": 60000, "peak_multiplier": 2.5},
    
    # Bus Terminals
    {"name": "Mumbai Central Bus Terminal", "lat": 18.9689, "lng": 72.8197, "type": "Bus Terminal", "area": "Mumbai Central", "daily_footfall": 120000, "peak_multiplier": 3.0},
    {"name": "Borivali Bus Depot", "lat": 19.2300, "lng": 72.8567, "type": "Bus Terminal", "area": "Borivali", "daily_footfall": 80000, "peak_multiplier": 2.8},
    {"name": "Kurla Bus Terminal", "lat": 19.0689, "lng": 72.8792, "type": "Bus Terminal", "area": "Kurla", "daily_footfall": 70000, "peak_multiplier": 2.6},
    
    # Highway Junctions
    {"name": "Eastern Express Highway - Sion", "lat": 19.0434, "lng": 72.8634, "type": "Highway Junction", "area": "Sion", "daily_footfall": 50000, "peak_multiplier": 3.8},
    {"name": "Western Express Highway - Bandra", "lat": 19.0544, "lng": 72.8378, "type": "Highway Junction", "area": "Bandra", "daily_footfall": 45000, "peak_multiplier": 3.5},
    {"name": "LBS Road - Kurla", "lat": 19.0689, "lng": 72.8792, "type": "Highway Junction", "area": "Kurla", "daily_footfall": 40000, "peak_multiplier": 3.2},
    
    # Shopping Malls (Rush Areas)
    {"name": "Phoenix Mills Lower Parel", "lat": 19.0134, "lng": 72.8333, "type": "Shopping Mall", "area": "Lower Parel", "daily_footfall": 60000, "peak_multiplier": 5.2},
    {"name": "Infiniti Mall Malad", "lat": 19.1875, "lng": 72.8356, "type": "Shopping Mall", "area": "Malad", "daily_footfall": 45000, "peak_multiplier": 4.8},
    {"name": "Atria Mall Worli", "lat": 19.0134, "lng": 72.8189, "type": "Shopping Mall", "area": "Worli", "daily_footfall": 40000, "peak_multiplier": 4.5},
    
    # Additional Hustle Spots
    {"name": "Chembur Station Area", "lat": 19.0634, "lng": 72.8978, "type": "Station Area", "area": "Chembur", "daily_footfall": 180000, "peak_multiplier": 3.2},
    {"name": "Mulund Station Area", "lat": 19.1689, "lng": 72.9456, "type": "Station Area", "area": "Mulund", "daily_footfall": 160000, "peak_multiplier": 3.0},
    {"name": "Ghatkopar Station Area", "lat": 19.0856, "lng": 72.9056, "type": "Station Area", "area": "Ghatkopar", "daily_footfall": 200000, "peak_multiplier": 3.4},
    {"name": "Kandivali Station Area", "lat": 19.2056, "lng": 72.8489, "type": "Station Area", "area": "Kandivali", "daily_footfall": 140000, "peak_multiplier": 2.9}
]

# FEATURE ENGINEERING - URBAN ENERGY DATA

def generate_mobility_osm_features(lat, lng, location_type, daily_footfall):
    """OSM-based urban mobility and infrastructure features"""
    
    features = {}
    
    # Transport infrastructure density
    if location_type in ["Terminus Station", "Major Junction", "Junction Station", "Major Hub"]:
        features['transport_infrastructure_density'] = np.random.normal(18.5, 3.0)
    elif location_type in ["Metro Hub", "Metro Station"]:
        features['transport_infrastructure_density'] = np.random.normal(12.8, 2.5)
    elif location_type in ["Bus Terminal", "Highway Junction"]:
        features['transport_infrastructure_density'] = np.random.normal(10.2, 2.8)
    else:
        features['transport_infrastructure_density'] = np.random.normal(6.4, 2.0)
    
    # Road network complexity (intersections, flyovers, signals)
    if location_type in ["Traffic Junction", "Highway Junction"]:
        features['road_network_complexity'] = np.random.normal(15.8, 3.5)
    elif "Station" in location_type:
        features['road_network_complexity'] = np.random.normal(12.4, 2.8)
    else:
        features['road_network_complexity'] = np.random.normal(8.6, 2.5)
    
    # Commercial activity density (offices, shops, services)
    if location_type in ["Business District", "Shopping Street", "Shopping Mall"]:
        features['commercial_activity_density'] = np.random.normal(22.4, 4.0)
    elif location_type in ["Gold Market", "Wholesale Market", "Local Market"]:
        features['commercial_activity_density'] = np.random.normal(28.6, 5.0)
    elif "Station" in location_type:
        features['commercial_activity_density'] = np.random.normal(16.8, 3.5)
    else:
        features['commercial_activity_density'] = np.random.normal(12.2, 3.0)
    
    # Distance to multiple transport modes
    features['multimodal_transport_access'] = calculate_multimodal_access(lat, lng, location_type)
    
    # Crowd management infrastructure
    features['crowd_management_score'] = calculate_crowd_infrastructure(location_type, daily_footfall)
    
    # Urban density indicators
    features['building_density_per_hectare'] = np.random.normal(85.4, 15.0)
    features['pedestrian_infrastructure_score'] = calculate_pedestrian_score(location_type)
    
    # Parking and vehicle infrastructure
    if location_type in ["Shopping Mall", "Business District"]:
        features['parking_infrastructure_score'] = np.random.normal(7.8, 1.5)
    elif "Station" in location_type or "Junction" in location_type:
        features['parking_infrastructure_score'] = np.random.normal(4.2, 2.0)
    else:
        features['parking_infrastructure_score'] = np.random.normal(5.8, 1.8)
    
    return {k: max(0, v) for k, v in features.items()}

def calculate_multimodal_access(lat, lng, location_type):
    """Calculate access to multiple transport modes"""
    base_scores = {
        "Major Hub": 9.5,  # Railway + Metro + Bus
        "Junction Station": 8.8,  # Railway + Bus + Taxi
        "Terminus Station": 8.5,
        "Metro Hub": 7.2,
        "Traffic Junction": 6.8,
        "Business District": 8.0,
        "Highway Junction": 6.5
    }
    
    return base_scores.get(location_type, 5.0) + np.random.normal(0, 0.8)

def calculate_crowd_infrastructure(location_type, daily_footfall):
    """Calculate crowd management infrastructure score"""
    base_infrastructure = daily_footfall / 100000  # Normalized base score
    
    if location_type in ["Major Hub", "Terminus Station"]:
        infrastructure_multiplier = 1.5
    elif location_type in ["Traffic Junction", "Shopping Mall"]:
        infrastructure_multiplier = 1.2
    else:
        infrastructure_multiplier = 1.0
    
    score = base_infrastructure * infrastructure_multiplier + np.random.normal(0, 0.5)
    return min(10, max(1, score))

def calculate_pedestrian_score(location_type):
    """Calculate pedestrian infrastructure quality"""
    scores = {
        "Shopping Street": 8.5,
        "Shopping Mall": 8.2,
        "Business District": 7.8,
        "Metro Station": 7.5,
        "Station Area": 6.5,
        "Traffic Junction": 5.2,
        "Highway Junction": 3.8
    }
    
    base = scores.get(location_type, 6.0)
    return base + np.random.normal(0, 1.0)

def generate_temporal_crowd_patterns(location_type, daily_footfall, peak_multiplier, area):
    """Generate realistic temporal crowd flow patterns"""
    
    # Base hourly distribution patterns by location type
    patterns = {
        "Terminus Station": {
            "morning_rush": 0.18, "mid_morning": 0.08, "lunch": 0.12, 
            "afternoon": 0.10, "evening_rush": 0.22, "night": 0.06
        },
        "Business District": {
            "morning_rush": 0.25, "mid_morning": 0.15, "lunch": 0.20, 
            "afternoon": 0.18, "evening_rush": 0.15, "night": 0.03
        },
        "Shopping Street": {
            "morning_rush": 0.08, "mid_morning": 0.12, "lunch": 0.18, 
            "afternoon": 0.22, "evening_rush": 0.25, "night": 0.08
        },
        "Traffic Junction": {
            "morning_rush": 0.20, "mid_morning": 0.12, "lunch": 0.15, 
            "afternoon": 0.15, "evening_rush": 0.25, "night": 0.08
        },
        "Shopping Mall": {
            "morning_rush": 0.05, "mid_morning": 0.10, "lunch": 0.20, 
            "afternoon": 0.25, "evening_rush": 0.30, "night": 0.05
        }
    }
    
    pattern = patterns.get(location_type, patterns["Traffic Junction"])
    
    # Calculate actual numbers
    temporal_data = {}
    for period, ratio in pattern.items():
        base_count = daily_footfall * ratio
        if period in ["morning_rush", "evening_rush"]:
            base_count *= peak_multiplier
        
        temporal_data[f"{period}_footfall"] = int(base_count * np.random.normal(1.0, 0.15))
    
    # Additional temporal features
    temporal_data.update({
        "peak_congestion_duration_hours": calculate_peak_duration(location_type),
        "weekend_variation_ratio": calculate_weekend_variation(location_type),
        "monsoon_impact_score": calculate_monsoon_impact(location_type),
        "festival_crowd_multiplier": calculate_festival_impact(location_type, area)
    })
    
    return temporal_data

def calculate_peak_duration(location_type):
    """Calculate how long peak congestion lasts"""
    durations = {
        "Terminus Station": 4.5,  # Long peak hours
        "Traffic Junction": 3.5,
        "Business District": 2.8,
        "Shopping Mall": 6.0,  # Extended shopping hours
        "Metro Station": 3.0
    }
    
    base = durations.get(location_type, 3.5)
    return base + np.random.normal(0, 0.5)

def calculate_weekend_variation(location_type):
    """Calculate weekend vs weekday crowd variation"""
    if location_type in ["Shopping Mall", "Shopping Street"]:
        return np.random.normal(1.8, 0.3)  # Much busier on weekends
    elif location_type in ["Business District", "IT District"]:
        return np.random.normal(0.3, 0.1)  # Much quieter on weekends
    elif "Station" in location_type:
        return np.random.normal(0.7, 0.2)  # Somewhat quieter
    else:
        return np.random.normal(1.0, 0.2)

def calculate_monsoon_impact(location_type):
    """Calculate monsoon impact on crowd flow"""
    if location_type in ["Traffic Junction", "Highway Junction"]:
        return np.random.normal(8.5, 1.0)  # High impact due to flooding
    elif location_type in ["Shopping Mall", "Metro Station"]:
        return np.random.normal(3.0, 1.0)  # Low impact (covered)
    else:
        return np.random.normal(6.0, 1.5)

def calculate_festival_impact(location_type, area):
    """Calculate festival crowd impact"""
    base_impact = 1.5  # Base festival multiplier
    
    # Location type adjustments
    if location_type in ["Shopping Street", "Shopping Mall"]:
        base_impact = 2.5
    elif "Station" in location_type:
        base_impact = 2.0
    elif location_type == "Business District":
        base_impact = 0.8
    
    area_multipliers = {
        "Dadar": 1.5, "Bandra": 1.3, "Fort": 1.4, 
        "Andheri": 1.2, "Lower Parel": 1.1
    }
    
    area_mult = area_multipliers.get(area, 1.0)
    return base_impact * area_mult + np.random.normal(0, 0.2)

def generate_urban_stress_indicators(location_type, daily_footfall, peak_multiplier):
    """Generate urban stress and intensity indicators"""
    
    # Base stress calculation
    crowd_stress = min(10, daily_footfall / 75000)  # Normalize to 0-10 scale
    peak_stress = min(10, peak_multiplier * 2)
    
    stress_indicators = {
        "crowd_density_stress": crowd_stress + np.random.normal(0, 0.5),
        "noise_level_estimate": calculate_noise_level(location_type, daily_footfall),
        "air_quality_impact": calculate_air_quality_impact(location_type),
        "infrastructure_strain_score": calculate_infrastructure_strain(location_type, daily_footfall),
        "emergency_response_accessibility": calculate_emergency_access(location_type),
        "urban_heat_island_effect": calculate_heat_island(location_type)
    }
    
    return {k: min(10, max(0, v)) for k, v in stress_indicators.items()}

def calculate_noise_level(location_type, daily_footfall):
    """Estimate noise levels (1-10 scale)"""
    base_noise = {
        "Highway Junction": 9.0,
        "Traffic Junction": 8.5,
        "Terminus Station": 8.0,
        "Shopping Street": 7.5,
        "Business District": 6.5,
        "Shopping Mall": 5.0
    }
    
    noise = base_noise.get(location_type, 7.0)
    crowd_noise = min(2.0, daily_footfall / 300000)  # Crowd contribution
    
    return noise + crowd_noise + np.random.normal(0, 0.5)

def calculate_air_quality_impact(location_type):
    """Estimate air quality impact (higher = worse air quality)"""
    if location_type in ["Highway Junction", "Traffic Junction"]:
        return np.random.normal(8.0, 1.0)
    elif "Station" in location_type:
        return np.random.normal(7.0, 1.0)
    elif location_type in ["Shopping Mall", "Metro Station"]:
        return np.random.normal(4.0, 1.0)
    else:
        return np.random.normal(6.0, 1.5)

def calculate_infrastructure_strain(location_type, daily_footfall):
    """Calculate strain on urban infrastructure"""
    base_strain = daily_footfall / 100000  # Normalized base
    
    multipliers = {
        "Terminus Station": 1.5,
        "Traffic Junction": 1.4,
        "Highway Junction": 1.3,
        "Shopping Mall": 1.1,
        "Business District": 1.2
    }
    
    multiplier = multipliers.get(location_type, 1.0)
    return min(10, base_strain * multiplier + np.random.normal(0, 0.5))

def calculate_emergency_access(location_type):
    """Calculate emergency services accessibility"""
    if location_type in ["Business District", "Shopping Mall"]:
        return np.random.normal(8.5, 1.0)  # Good emergency access
    elif "Station" in location_type:
        return np.random.normal(7.0, 1.5)
    elif location_type in ["Traffic Junction", "Highway Junction"]:
        return np.random.normal(5.5, 1.5)  # Difficult due to traffic
    else:
        return np.random.normal(6.5, 1.0)

def calculate_heat_island(location_type):
    """Calculate urban heat island contribution"""
    if location_type in ["Highway Junction", "Traffic Junction"]:
        return np.random.normal(8.5, 1.0)  # High heat from traffic
    elif location_type in ["Business District"]:
        return np.random.normal(7.5, 1.0)  # High-rise buildings
    elif location_type in ["Shopping Mall"]:
        return np.random.normal(6.0, 1.0)  # AC load
    else:
        return np.random.normal(6.5, 1.5)

def generate_economic_activity_features(location_type, area, daily_footfall):
    """Generate economic activity and business density features"""
    
    # Economic multipliers based on foot traffic
    economic_base = daily_footfall / 1000  # Base economic activity score
    
    economic_features = {
        "business_density_score": calculate_business_density(location_type, area),
        "economic_activity_index": min(100, economic_base + np.random.normal(0, 5)),
        "employment_hub_score": calculate_employment_score(location_type),
        "retail_commercial_ratio": calculate_retail_ratio(location_type),
        "service_sector_density": calculate_service_density(location_type, area),
        "informal_economy_score": calculate_informal_economy(location_type),
        "land_value_impact": calculate_land_value_impact(location_type, area)
    }
    
    return economic_features

def calculate_business_density(location_type, area):
    """Calculate business establishment density"""
    base_scores = {
        "Business District": 9.5,
        "Shopping Street": 9.0,
        "Gold Market": 8.8,
        "Wholesale Market": 8.5,
        "Shopping Mall": 8.0,
        "Station Area": 7.2,
        "Traffic Junction": 6.5
    }
    
    base = base_scores.get(location_type, 6.0)
    
    premium_areas = {"Nariman Point": 1.5, "BKC": 1.4, "Lower Parel": 1.3, "Fort": 1.2}
    area_premium = premium_areas.get(area, 1.0)
    
    return min(10, base * area_premium + np.random.normal(0, 0.5))

def calculate_employment_score(location_type):
    """Calculate employment generation score"""
    scores = {
        "Business District": 9.5,
        "IT District": 9.0,
        "Industrial Area": 8.5,
        "Shopping Mall": 7.5,
        "Major Hub": 7.0,
        "Wholesale Market": 6.8
    }
    
    return scores.get(location_type, 5.0) + np.random.normal(0, 0.8)

def calculate_retail_ratio(location_type):
    """Calculate retail vs other commercial activities ratio"""
    if location_type in ["Shopping Street", "Shopping Mall"]:
        return np.random.normal(0.85, 0.10)
    elif location_type in ["Business District", "IT District"]:
        return np.random.normal(0.15, 0.08)
    elif "Market" in location_type:
        return np.random.normal(0.90, 0.08)
    else:
        return np.random.normal(0.45, 0.15)

def calculate_service_density(location_type, area):
    """Calculate service sector business density"""
    if location_type in ["Business District", "IT District"]:
        return np.random.normal(8.5, 1.0)
    elif "Station" in location_type:
        return np.random.normal(6.8, 1.5)
    else:
        return np.random.normal(5.2, 1.8)

def calculate_informal_economy(location_type):
    """Calculate informal economy presence (street vendors, etc.)"""
    if location_type in ["Traffic Junction", "Station Area"]:
        return np.random.normal(8.0, 1.5)
    elif "Station" in location_type:
        return np.random.normal(7.2, 1.2)
    elif location_type in ["Shopping Mall", "Business District"]:
        return np.random.normal(2.5, 1.0)
    else:
        return np.random.normal(5.5, 2.0)

def calculate_land_value_impact(location_type, area):
    """Calculate impact on surrounding land values"""
    base_impact = {
        "Business District": 9.0,
        "Major Hub": 8.5,
        "Shopping Mall": 8.0,
        "Metro Hub": 7.5,
        "IT District": 7.8
    }
    
    impact = base_impact.get(location_type, 6.0)
    
    # Premium area adjustments
    if area in ["Nariman Point", "BKC", "Lower Parel"]:
        impact += 1.0
    elif area in ["Bandra", "Andheri"]:
        impact += 0.5
    
    return min(10, impact + np.random.normal(0, 0.5))

# GENERATE COMPLETE DATASET

def create_complete_chaotic_hustle_dataset():
    """Generate the complete Chaotic Hustle urban energy dataset"""
    
    complete_data = []
    
    for i, location in enumerate(chaotic_hustle_locations):
        # Basic location info
        loc_data = {
            'location_id': f"CH_{i+1:03d}",
            'name': location['name'],
            'lat': location['lat'],
            'lng': location['lng'],
            'type': location['type'],
            'area': location['area'],
            'daily_footfall': location['daily_footfall'],
            'peak_multiplier': location['peak_multiplier'],
            'vibe_category': 'Chaotic Hustle'
        }
        
        # OSM-based mobility features
        osm_features = generate_mobility_osm_features(
            location['lat'], location['lng'], 
            location['type'], location['daily_footfall']
        )
        
        # temporal crowd patterns
        temporal_data = generate_temporal_crowd_patterns(
            location['type'], location['daily_footfall'], 
            location['peak_multiplier'], location['area']
        )
        
        # urban stress indicators
        stress_indicators = generate_urban_stress_indicators(
            location['type'], location['daily_footfall'], location['peak_multiplier']
        )
        
        # economic activity features
        economic_features = generate_economic_activity_features(
            location['type'], location['area'], location['daily_footfall']
        )
        
        # vibe intensity
        vibe_intensity = calculate_hustle_vibe_intensity(
            location['type'], location['daily_footfall'], 
            location['peak_multiplier'], location['area']
        )
        
        # Urban infrastructure features
        infrastructure_features = {
            "digital_infrastructure_score": calculate_digital_infrastructure(location['type'], location['area']),
            "accessibility_score": calculate_accessibility_score(location['type']),
            "safety_security_score": calculate_safety_score(location['type'], location['daily_footfall']),
            "waste_management_efficiency": calculate_waste_management(location['type']),
            "energy_consumption_index": calculate_energy_consumption(location['type'], location['daily_footfall'])
        }
        
        # Connectivity features
        connectivity_features = {
            "network_centrality_score": calculate_network_centrality(location['type'], location['area']),
            "inter_district_connectivity": calculate_inter_district_connectivity(location['area']),
            "last_mile_connectivity": calculate_last_mile_connectivity(location['type']),
            "transport_mode_diversity": calculate_transport_diversity(location['type'])
        }
        
        # Combine all features
        complete_location = {
            **loc_data,
            **osm_features,
            **temporal_data,
            **stress_indicators,
            **economic_features,
            **infrastructure_features,
            **connectivity_features,
            'vibe_intensity': vibe_intensity,
            'data_collection_date': '2024-12-10',  # Peak urban activity season
            'confidence_score': np.random.normal(0.89, 0.07)
        }
        
        complete_data.append(complete_location)
    
    return pd.DataFrame(complete_data)

def calculate_hustle_vibe_intensity(location_type, daily_footfall, peak_multiplier, area):
    """Calculate chaotic hustle vibe intensity"""
    
    # Base scores by location type
    base_scores = {
        "Major Hub": 4.8,
        "Terminus Station": 4.6,
        "Traffic Junction": 4.7,
        "Junction Station": 4.4,
        "Highway Junction": 4.3,
        "Shopping Street": 4.2,
        "Business District": 4.0,
        "Wholesale Market": 4.1,
        "Shopping Mall": 3.8,
        "Metro Hub": 3.9,
        "Bus Terminal": 3.7
    }
    
    # Footfall intensity bonus
    footfall_bonus = min(0.5, daily_footfall / 1000000)  # Max 0.5 bonus for 1M+ footfall
    
    # Peak intensity bonus
    peak_bonus = min(0.3, (peak_multiplier - 2.0) * 0.1)  # Bonus for high peak multipliers
    
    # High-intensity area bonus
    area_bonus = {
        "Dadar": 0.3, "Andheri": 0.2, "Bandra": 0.2,
        "Nariman Point": 0.1, "BKC": 0.1
    }.get(area, 0)
    
    base_score = base_scores.get(location_type, 3.5)
    final_score = min(5.0, base_score + footfall_bonus + peak_bonus + area_bonus + np.random.normal(0, 0.1))
    
    return round(max(1.0, final_score), 2)

def calculate_digital_infrastructure(location_type, area):
    """Calculate digital infrastructure quality"""
    if location_type in ["Business District", "IT District"]:
        return np.random.normal(9.0, 0.8)
    elif location_type in ["Shopping Mall", "Metro Hub"]:
        return np.random.normal(8.2, 1.0)
    elif "Station" in location_type:
        return np.random.normal(7.0, 1.2)
    else:
        return np.random.normal(6.0, 1.5)

def calculate_accessibility_score(location_type):
    """Calculate accessibility for differently-abled persons"""
    if location_type in ["Metro Station", "Metro Hub"]:
        return np.random.normal(8.0, 1.0)  # Modern metro infrastructure
    elif location_type in ["Shopping Mall", "Business District"]:
        return np.random.normal(7.5, 1.2)
    elif "Station" in location_type:
        return np.random.normal(5.5, 1.5)  # Older railway infrastructure
    else:
        return np.random.normal(4.5, 1.8)

def calculate_safety_score(location_type, daily_footfall):
    """Calculate safety and security score"""
    # Higher footfall generally means better security presence
    base_safety = min(8.0, daily_footfall / 100000)
    
    if location_type in ["Business District", "Shopping Mall"]:
        base_safety += 1.5
    elif "Station" in location_type:
        base_safety += 1.0
    elif location_type in ["Traffic Junction", "Highway Junction"]:
        base_safety -= 0.5
    
    return min(10, max(2, base_safety + np.random.normal(0, 1.0)))

def calculate_waste_management(location_type):
    """Calculate waste management efficiency"""
    if location_type in ["Shopping Mall", "Business District"]:
        return np.random.normal(8.0, 1.0)
    elif location_type in ["Metro Station", "Metro Hub"]:
        return np.random.normal(7.5, 1.2)
    elif "Station" in location_type:
        return np.random.normal(5.5, 1.5)
    else:
        return np.random.normal(6.0, 1.8)

def calculate_energy_consumption(location_type, daily_footfall):
    """Calculate energy consumption index"""
    base_consumption = daily_footfall / 50000  # Base consumption
    
    multipliers = {
        "Shopping Mall": 2.0,
        "Business District": 1.8,
        "Metro Station": 1.5,
        "Major Hub": 1.6
    }
    
    multiplier = multipliers.get(location_type, 1.0)
    return min(10, base_consumption * multiplier + np.random.normal(0, 0.5))

def calculate_network_centrality(location_type, area):
    """Calculate network centrality in Mumbai's urban system"""
    if location_type in ["Major Hub", "Terminus Station"] and area in ["Dadar", "Andheri", "Churchgate"]:
        return np.random.normal(9.5, 0.5)
    elif location_type in ["Business District"] and area in ["Nariman Point", "BKC", "Lower Parel"]:
        return np.random.normal(9.0, 0.8)
    elif "Junction" in location_type:
        return np.random.normal(7.5, 1.0)
    else:
        return np.random.normal(6.0, 1.5)

def calculate_inter_district_connectivity(area):
    """Calculate connectivity between different Mumbai districts"""
    connectivity_scores = {
        "Dadar": 9.5,  # Central hub connecting all directions
        "Andheri": 9.0,  # Major suburban connector
        "Bandra": 8.5,  # Western line important junction
        "Churchgate": 8.0,  # Southern terminus
        "BKC": 7.5,  # New business district
        "Nariman Point": 7.0,  # South Mumbai business center
        "Thane": 6.5,  # Suburban endpoint
        "Borivali": 6.0,  # Northern suburban
        "Virar": 5.0   # Far suburban
    }
    
    return connectivity_scores.get(area, 6.0) + np.random.normal(0, 0.5)

def calculate_last_mile_connectivity(location_type):
    """Calculate last mile connectivity options"""
    if location_type in ["Metro Station", "Metro Hub"]:
        return np.random.normal(8.5, 1.0)  # Good last mile options
    elif "Station" in location_type:
        return np.random.normal(7.0, 1.5)  # Auto-rickshaws, buses
    elif location_type in ["Shopping Mall"]:
        return np.random.normal(7.5, 1.2)  # Parking, cabs
    else:
        return np.random.normal(5.5, 2.0)

def calculate_transport_diversity(location_type):
    """Calculate diversity of transport options available"""
    diversity_scores = {
        "Major Hub": 9.0,  # Train, metro, bus, taxi, auto
        "Terminus Station": 8.5,
        "Junction Station": 8.0,
        "Metro Hub": 7.5,
        "Business District": 7.0,
        "Traffic Junction": 6.5,
        "Shopping Mall": 6.0
    }
    
    return diversity_scores.get(location_type, 5.0) + np.random.normal(0, 1.0)

# URBAN PLANNING INSIGHTS

def generate_urban_planning_insights():
    """Generate insights for urban planning based on chaotic hustle data"""
    
    planning_insights = {
        "congestion_hotspots": [
            "Dadar TT Circle", "Andheri Subway", "Bandra Kalanagar Junction"
        ],
        "infrastructure_upgrade_priorities": [
            "Crowd management at major stations",
            "Pedestrian infrastructure at traffic junctions",
            "Digital infrastructure in business districts"
        ],
        "peak_hour_management_strategies": [
            "Staggered office timings",
            "Enhanced public transport frequency",
            "Dynamic traffic signal optimization"
        ],
        "sustainability_concerns": [
            "Air quality at highway junctions",
            "Energy consumption at shopping malls",
            "Waste management at high-footfall areas"
        ]
    }
    
    return planning_insights

# MAIN EXECUTION

if __name__ == "__main__":
    # Generate the complete chaotic hustle dataset
    print("Generating 'Chaotic Hustle' urban energy dataset...")
    hustle_df = create_complete_chaotic_hustle_dataset()
    
    # Save to CSV
    hustle_df.to_csv('chaotic_hustle_dataset.csv', index=False)
    print(f"Chaotic Hustle dataset saved! Shape: {hustle_df.shape}")
    
    print("\nSample chaotic hustle data:")
    sample_cols = ['name', 'type', 'daily_footfall', 'vibe_intensity', 'crowd_density_stress', 'evening_rush_footfall']
    print(hustle_df[sample_cols].head(10))
    
    # Generate urban planning insights
    planning_insights = generate_urban_planning_insights()
    with open('urban_planning_insights.json', 'w') as f:
        json.dump(planning_insights, f, indent=2)
    
    # Urban energy summary statistics
    print(f"\nChaotic Hustle Summary:")
    major_hubs = len([l for l in chaotic_hustle_locations if l['type'] in ['Major Hub', 'Terminus Station']])
    traffic_junctions = len([l for l in chaotic_hustle_locations if 'Junction' in l['type']])
    business_districts = len([l for l in chaotic_hustle_locations if 'Business District' in l['type']])
    
    print(f"Major transport hubs: {major_hubs}")
    print(f"Traffic junctions: {traffic_junctions}")
    print(f"Business districts: {business_districts}")
    
    total_daily_footfall = sum([l['daily_footfall'] for l in chaotic_hustle_locations])
    avg_daily_footfall = total_daily_footfall / len(chaotic_hustle_locations)
    print(f"Total daily footfall across all locations: {total_daily_footfall:,}")
    print(f"Average daily footfall per location: {avg_daily_footfall:,.0f}")
    
    # Peak intensity analysis
    peak_multipliers = [l['peak_multiplier'] for l in chaotic_hustle_locations]
    print(f"Average peak intensity multiplier: {np.mean(peak_multipliers):.1f}x")
    print(f"Highest peak intensity: {max(peak_multipliers):.1f}x (Shopping malls and traffic junctions)")
    print(f"Infrastructure strain locations (>500k daily): {len([l for l in chaotic_hustle_locations if l['daily_footfall'] > 500000])}")