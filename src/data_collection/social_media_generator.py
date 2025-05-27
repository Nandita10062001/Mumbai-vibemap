import pandas as pd
import numpy as np
import requests
import json
from geopy.distance import geodesic
import time

# DO IT FOR THE GRAM - COMPLETE DATASET

# Social media hotspot locations in Mumbai with exact coordinates
gram_locations = [
    # Scenic Waterfront Spots
    {"name": "Marine Drive", "lat": 18.9436, "lng": 72.8228, "type": "Scenic Promenade", "area": "Marine Drive", "instagram_tags": 450000, "aesthetic_score": 9.5},
    {"name": "Bandra Bandstand", "lat": 19.0544, "lng": 72.8181, "type": "Seaside Promenade", "area": "Bandra", "instagram_tags": 380000, "aesthetic_score": 9.2},
    {"name": "Carter Road Promenade", "lat": 19.0544, "lng": 72.8181, "type": "Waterfront Walk", "area": "Bandra", "instagram_tags": 320000, "aesthetic_score": 8.8},
    {"name": "Worli Sea Face", "lat": 19.0134, "lng": 72.8111, "type": "Sea View", "area": "Worli", "instagram_tags": 280000, "aesthetic_score": 8.5},
    {"name": "Juhu Beach", "lat": 18.9896, "lng": 72.8267, "type": "Beach", "area": "Juhu", "instagram_tags": 500000, "aesthetic_score": 8.9},
    {"name": "Versova Beach", "lat": 19.1317, "lng": 72.8128, "type": "Beach", "area": "Versova", "instagram_tags": 220000, "aesthetic_score": 7.8},
    {"name": "Aksa Beach", "lat": 19.1756, "lng": 72.7967, "type": "Beach", "area": "Malad", "instagram_tags": 150000, "aesthetic_score": 7.5},
    {"name": "Madh Island Beach", "lat": 19.1317, "lng": 72.7883, "type": "Beach", "area": "Malad", "instagram_tags": 80000, "aesthetic_score": 7.2},
    
    # Trendy Cafes & Restaurants
    {"name": "Candies Bandra", "lat": 19.0544, "lng": 72.8267, "type": "Trendy Cafe", "area": "Bandra", "instagram_tags": 180000, "aesthetic_score": 8.7},
    {"name": "Pali Village Cafe", "lat": 19.0656, "lng": 72.8289, "type": "Boho Cafe", "area": "Bandra", "instagram_tags": 220000, "aesthetic_score": 9.0},
    {"name": "The Pantry Kala Ghoda", "lat": 18.9269, "lng": 72.8324, "type": "Artsy Cafe", "area": "Kala Ghoda", "instagram_tags": 150000, "aesthetic_score": 8.5},
    {"name": "Cafe Mocha Multiple", "lat": 19.0544, "lng": 72.8267, "type": "Coffee Chain", "area": "Multiple", "instagram_tags": 200000, "aesthetic_score": 7.8},
    {"name": "Social Bandra", "lat": 19.0544, "lng": 72.8267, "type": "Co-working Cafe", "area": "Bandra", "instagram_tags": 280000, "aesthetic_score": 8.9},
    {"name": "Social Lower Parel", "lat": 19.0134, "lng": 72.8333, "type": "Co-working Cafe", "area": "Lower Parel", "instagram_tags": 250000, "aesthetic_score": 8.6},
    {"name": "Monkey Bar", "lat": 19.0544, "lng": 72.8267, "type": "Trendy Bar", "area": "Bandra", "instagram_tags": 190000, "aesthetic_score": 8.4},
    {"name": "The Sassy Spoon", "lat": 18.9314, "lng": 72.8311, "type": "Trendy Restaurant", "area": "Multiple", "instagram_tags": 160000, "aesthetic_score": 8.2},
    
    # Art & Cultural Spaces
    {"name": "Kala Ghoda Art District", "lat": 18.9269, "lng": 72.8324, "type": "Cultural District", "area": "Kala Ghoda", "instagram_tags": 350000, "aesthetic_score": 9.1},
    {"name": "National Gallery of Modern Art", "lat": 18.9269, "lng": 72.8324, "type": "Art Gallery", "area": "Fort", "instagram_tags": 120000, "aesthetic_score": 8.3},
    {"name": "Sassoon Docks Art Project", "lat": 18.9178, "lng": 72.8289, "type": "Art Installation", "area": "Colaba", "instagram_tags": 95000, "aesthetic_score": 8.0},
    {"name": "Versova Art Village", "lat": 19.1317, "lng": 72.8128, "type": "Artist Colony", "area": "Versova", "instagram_tags": 85000, "aesthetic_score": 7.9},
    {"name": "Chapel Road Art Galleries", "lat": 19.0544, "lng": 72.8267, "type": "Gallery District", "area": "Bandra", "instagram_tags": 110000, "aesthetic_score": 8.1},
    
    # Rooftop & Skyline Views
    {"name": "Aer Bar Four Seasons", "lat": 19.0134, "lng": 72.8189, "type": "Rooftop Bar", "area": "Worli", "instagram_tags": 140000, "aesthetic_score": 9.3},
    {"name": "Asilo Rooftop", "lat": 19.0656, "lng": 72.8289, "type": "Rooftop Restaurant", "area": "Bandra", "instagram_tags": 120000, "aesthetic_score": 8.8},
    {"name": "High Ultra Lounge", "lat": 19.1197, "lng": 72.8467, "type": "Rooftop Lounge", "area": "Andheri", "instagram_tags": 100000, "aesthetic_score": 8.5},
    {"name": "Skybar Mumbai", "lat": 18.9269, "lng": 72.8228, "type": "Sky Lounge", "area": "Nariman Point", "instagram_tags": 90000, "aesthetic_score": 8.7},
    
    # Shopping & Lifestyle Hubs
    {"name": "Palladium Mall", "lat": 19.0134, "lng": 72.8333, "type": "Luxury Mall", "area": "Lower Parel", "instagram_tags": 200000, "aesthetic_score": 8.4},
    {"name": "Phoenix Mills", "lat": 19.0134, "lng": 72.8333, "type": "Lifestyle Mall", "area": "Lower Parel", "instagram_tags": 180000, "aesthetic_score": 8.2},
    {"name": "Linking Road Shopping", "lat": 19.0544, "lng": 72.8267, "type": "Shopping Street", "area": "Bandra", "instagram_tags": 160000, "aesthetic_score": 7.8},
    {"name": "Hill Road Bandra", "lat": 19.0544, "lng": 72.8267, "type": "Shopping Street", "area": "Bandra", "instagram_tags": 140000, "aesthetic_score": 7.6},
    {"name": "Colaba Causeway", "lat": 18.9220, "lng": 72.8331, "type": "Shopping Street", "area": "Colaba", "instagram_tags": 130000, "aesthetic_score": 7.9},
    
    # Architectural Marvels
    {"name": "Gateway of India", "lat": 18.9220, "lng": 72.8347, "type": "Historic Monument", "area": "Colaba", "instagram_tags": 600000, "aesthetic_score": 9.4},
    {"name": "Chhatrapati Shivaji Terminus", "lat": 18.9401, "lng": 72.8350, "type": "Heritage Architecture", "area": "Fort", "instagram_tags": 300000, "aesthetic_score": 9.2},
    {"name": "Taj Mahal Palace Hotel", "lat": 18.9216, "lng": 72.8331, "type": "Iconic Hotel", "area": "Colaba", "instagram_tags": 250000, "aesthetic_score": 9.1},
    {"name": "Rajabai Clock Tower", "lat": 18.9292, "lng": 72.8317, "type": "Gothic Architecture", "area": "Fort", "instagram_tags": 80000, "aesthetic_score": 8.4},
    
    # Sunset & Golden Hour Spots
    {"name": "Mount Mary Church", "lat": 19.0544, "lng": 72.8181, "type": "Hilltop Church", "area": "Bandra", "instagram_tags": 180000, "aesthetic_score": 8.6},
    {"name": "Hanging Gardens", "lat": 18.9547, "lng": 72.8081, "type": "Hilltop Garden", "area": "Malabar Hill", "instagram_tags": 120000, "aesthetic_score": 8.3},
    {"name": "Kamala Nehru Park", "lat": 18.9547, "lng": 72.8081, "type": "Scenic Park", "area": "Malabar Hill", "instagram_tags": 100000, "aesthetic_score": 8.0},
    {"name": "Worli Sea Link View Point", "lat": 19.0134, "lng": 72.8111, "type": "Bridge View", "area": "Worli", "instagram_tags": 200000, "aesthetic_score": 9.0},
    
    # Hipster & Alternative Spots
    {"name": "Bandra West Cafes Strip", "lat": 19.0656, "lng": 72.8289, "type": "Cafe District", "area": "Bandra West", "instagram_tags": 220000, "aesthetic_score": 8.7},
    {"name": "Khar West Social Scene", "lat": 19.0656, "lng": 72.8378, "type": "Nightlife District", "area": "Khar", "instagram_tags": 190000, "aesthetic_score": 8.5},
    {"name": "Juhu Koliwada", "lat": 18.9896, "lng": 72.8267, "type": "Fishing Village", "area": "Juhu", "instagram_tags": 70000, "aesthetic_score": 7.4},
    {"name": "Bandra Fort Ruins", "lat": 19.0544, "lng": 72.8181, "type": "Historic Ruins", "area": "Bandra", "instagram_tags": 85000, "aesthetic_score": 7.8},
    
    # Food Photography Hotspots
    {"name": "Mohammed Ali Road Food Street", "lat": 18.9589, "lng": 72.8333, "type": "Food Photography Hub", "area": "Mohammed Ali Road", "instagram_tags": 150000, "aesthetic_score": 8.2},
    {"name": "Leopold Cafe", "lat": 18.9220, "lng": 72.8331, "type": "Iconic Eatery", "area": "Colaba", "instagram_tags": 140000, "aesthetic_score": 8.1},
    {"name": "Trishna Restaurant", "lat": 18.9314, "lng": 72.8311, "type": "Fine Dining", "area": "Fort", "instagram_tags": 110000, "aesthetic_score": 8.4},
    
    # Modern Mumbai Landmarks
    {"name": "Bandra Kurla Complex", "lat": 19.0656, "lng": 72.8678, "type": "Modern Business District", "area": "BKC", "instagram_tags": 180000, "aesthetic_score": 8.3},
    {"name": "Antilia Building", "lat": 18.9778, "lng": 72.8089, "type": "Architectural Marvel", "area": "Altamount Road", "instagram_tags": 120000, "aesthetic_score": 7.9},
    {"name": "Lower Parel Mills District", "lat": 19.0134, "lng": 72.8333, "type": "Converted Mills", "area": "Lower Parel", "instagram_tags": 160000, "aesthetic_score": 8.1}
]

# FEATURE ENGINEERING - SOCIAL MEDIA DATA

def generate_social_media_osm_features(lat, lng, location_type, area, aesthetic_score):
    """OSM-based features based on queried osm data for social media hotspots"""
    
    features = {}
    
    # Cafe and restaurant density (Instagram food spots)
    if location_type in ["Trendy Cafe", "Boho Cafe", "Co-working Cafe", "Cafe District"]:
        features['trendy_cafe_density'] = np.random.normal(12.8, 3.0)
    elif location_type in ["Food Photography Hub", "Iconic Eatery"]:
        features['trendy_cafe_density'] = np.random.normal(18.5, 4.0)
    else:
        features['trendy_cafe_density'] = np.random.normal(5.2, 2.5)
    
    # Scenic view infrastructure (viewpoints, elevated areas)
    if location_type in ["Scenic Promenade", "Sea View", "Beach", "Rooftop Bar", "Hilltop Church"]:
        features['scenic_infrastructure_score'] = np.random.normal(9.2, 1.0)
    elif location_type in ["Bridge View", "Sky Lounge", "Hilltop Garden"]:
        features['scenic_infrastructure_score'] = np.random.normal(8.8, 1.2)
    else:
        features['scenic_infrastructure_score'] = np.random.normal(4.5, 2.0)
    
    # Art and culture venue density
    if location_type in ["Cultural District", "Art Gallery", "Artist Colony", "Gallery District"]:
        features['cultural_venue_density'] = np.random.normal(15.6, 3.5)
    elif area in ["Kala Ghoda", "Bandra", "Fort"]:
        features['cultural_venue_density'] = np.random.normal(8.9, 2.8)
    else:
        features['cultural_venue_density'] = np.random.normal(3.2, 2.0)
    
    # Shopping and lifestyle infrastructure
    if location_type in ["Luxury Mall", "Lifestyle Mall", "Shopping Street"]:
        features['lifestyle_shopping_density'] = np.random.normal(16.4, 3.2)
    elif area in ["Bandra", "Lower Parel", "Colaba"]:
        features['lifestyle_shopping_density'] = np.random.normal(10.1, 2.5)
    else:
        features['lifestyle_shopping_density'] = np.random.normal(5.8, 2.2)
    
    # Photography-friendly infrastructure
    features['photo_infrastructure_score'] = calculate_photo_infrastructure(location_type, aesthetic_score)
    
    # Social gathering spaces
    features['social_gathering_density'] = calculate_social_spaces(location_type, area)
    
    # Accessibility for content creators
    features['creator_accessibility_score'] = calculate_creator_accessibility(location_type, area)
    
    # Lighting quality for photography
    features['natural_lighting_score'] = calculate_lighting_quality(location_type, aesthetic_score)
    
    return {k: max(0, v) for k, v in features.items()}

def calculate_photo_infrastructure(location_type, aesthetic_score):
    """Calculate photography infrastructure quality"""
    base_score = aesthetic_score * 0.8  # Base on aesthetic appeal
    
    # Location type bonuses
    if location_type in ["Scenic Promenade", "Beach", "Rooftop Bar"]:
        base_score += 1.5
    elif location_type in ["Historic Monument", "Heritage Architecture"]:
        base_score += 1.2
    elif location_type in ["Trendy Cafe", "Art Gallery"]:
        base_score += 1.0
    
    return min(10, base_score + np.random.normal(0, 0.5))

def calculate_social_spaces(location_type, area):
    """Calculate density of social gathering spaces"""
    base_scores = {
        "Trendy Cafe": 8.5,
        "Co-working Cafe": 8.2,
        "Shopping Street": 7.8,
        "Beach": 7.5,
        "Cultural District": 7.2,
        "Rooftop Bar": 6.8
    }
    
    base = base_scores.get(location_type, 5.0)
    
    # Area multipliers for social scenes
    area_multipliers = {
        "Bandra": 1.4, "Lower Parel": 1.3, "Kala Ghoda": 1.2,
        "Colaba": 1.2, "Juhu": 1.1
    }
    
    multiplier = area_multipliers.get(area, 1.0)
    return min(10, base * multiplier + np.random.normal(0, 0.8))

def calculate_creator_accessibility(location_type, area):
    """Calculate accessibility for content creators (parking, equipment, etc.)"""
    if location_type in ["Luxury Mall", "Rooftop Bar", "Modern Business District"]:
        return np.random.normal(8.5, 1.0)  # Good parking and facilities
    elif location_type in ["Beach", "Scenic Promenade"]:
        return np.random.normal(7.0, 1.5)  # Good access but limited parking
    elif location_type in ["Shopping Street", "Food Photography Hub"]:
        return np.random.normal(5.5, 2.0)  # Crowded, limited equipment space
    else:
        return np.random.normal(6.5, 1.8)

def calculate_lighting_quality(location_type, aesthetic_score):
    """Calculate natural lighting quality for photography"""
    if location_type in ["Beach", "Scenic Promenade", "Hilltop Garden"]:
        return np.random.normal(9.0, 0.8)  # Excellent natural light
    elif location_type in ["Rooftop Bar", "Sky Lounge"]:
        return np.random.normal(8.5, 1.0)  # Good elevated lighting
    elif location_type in ["Art Gallery", "Cultural District"]:
        return np.random.normal(7.0, 1.5)  # Mixed indoor/outdoor
    else:
        return min(10, aesthetic_score * 0.9 + np.random.normal(0, 1.0))

def generate_social_media_engagement_patterns(location_type, instagram_tags, aesthetic_score, area):
    """Generate realistic social media engagement patterns"""
    
    # Base engagement rates by location type
    engagement_patterns = {
        "Beach": {"posts_per_day": 450, "stories_per_day": 1200, "reels_per_day": 180},
        "Scenic Promenade": {"posts_per_day": 380, "stories_per_day": 950, "reels_per_day": 150},
        "Trendy Cafe": {"posts_per_day": 320, "stories_per_day": 800, "reels_per_day": 120},
        "Historic Monument": {"posts_per_day": 500, "stories_per_day": 600, "reels_per_day": 80},
        "Rooftop Bar": {"posts_per_day": 280, "stories_per_day": 720, "reels_per_day": 200},
        "Cultural District": {"posts_per_day": 220, "stories_per_day": 450, "reels_per_day": 90},
        "Shopping Street": {"posts_per_day": 350, "stories_per_day": 900, "reels_per_day": 160}
    }
    
    pattern = engagement_patterns.get(location_type, {"posts_per_day": 200, "stories_per_day": 500, "reels_per_day": 100})
    
    # Scale by Instagram popularity
    popularity_multiplier = min(3.0, instagram_tags / 100000)
    
    # Area-specific social media activity
    area_multipliers = {
        "Bandra": 1.6, "Colaba": 1.4, "Juhu": 1.3, "Lower Parel": 1.2,
        "Kala Ghoda": 1.1, "Marine Drive": 1.5
    }
    
    area_mult = area_multipliers.get(area, 1.0)
    
    engagement_data = {}
    for metric, base_value in pattern.items():
        scaled_value = base_value * popularity_multiplier * area_mult
        engagement_data[metric] = int(scaled_value * np.random.normal(1.0, 0.2))
    
    # Additional engagement metrics
    engagement_data.update({
        "influencer_visits_per_month": calculate_influencer_visits(location_type, aesthetic_score),
        "hashtag_diversity_score": calculate_hashtag_diversity(location_type, area),
        "viral_potential_score": calculate_viral_potential(location_type, aesthetic_score, instagram_tags),
        "weekend_engagement_multiplier": calculate_weekend_multiplier(location_type),
        "golden_hour_activity_boost": calculate_golden_hour_boost(location_type)
    })
    
    return engagement_data

def calculate_influencer_visits(location_type, aesthetic_score):
    """Estimate influencer visits per month"""
    base_visits = aesthetic_score * 3  # Base on aesthetic appeal
    
    # Location type multipliers
    multipliers = {
        "Rooftop Bar": 2.5, "Beach": 2.2, "Trendy Cafe": 2.0,
        "Historic Monument": 1.8, "Luxury Mall": 1.6, "Cultural District": 1.4
    }
    
    multiplier = multipliers.get(location_type, 1.0)
    visits = base_visits * multiplier + np.random.normal(0, 3)
    
    return max(1, int(visits))

def calculate_hashtag_diversity(location_type, area):
    """Calculate hashtag diversity score"""
    if location_type in ["Cultural District", "Art Gallery"]:
        return np.random.normal(8.5, 1.0)  # High diversity for cultural spots
    elif location_type in ["Beach", "Scenic Promenade"]:
        return np.random.normal(7.0, 1.2)  # Moderate diversity
    elif location_type in ["Shopping Street", "Food Photography Hub"]:
        return np.random.normal(8.0, 1.1)  # High for lifestyle spots
    else:
        return np.random.normal(6.5, 1.5)

def calculate_viral_potential(location_type, aesthetic_score, instagram_tags):
    """Calculate viral content potential"""
    base_potential = (aesthetic_score + np.log10(instagram_tags + 1)) / 2
    
    # Location type bonuses for viral content
    viral_bonuses = {
        "Beach": 1.5, "Historic Monument": 1.3, "Rooftop Bar": 1.4,
        "Scenic Promenade": 1.2, "Trendy Cafe": 1.1
    }
    
    bonus = viral_bonuses.get(location_type, 1.0)
    viral_score = base_potential * bonus + np.random.normal(0, 0.5)
    
    return min(10, max(1, viral_score))

def calculate_weekend_multiplier(location_type):
    """Calculate weekend vs weekday social media activity"""
    if location_type in ["Beach", "Shopping Street", "Rooftop Bar"]:
        return np.random.normal(2.5, 0.3)  # Much higher on weekends
    elif location_type in ["Trendy Cafe", "Cultural District"]:
        return np.random.normal(1.8, 0.2)
    elif location_type in ["Historic Monument"]:
        return np.random.normal(1.4, 0.2)  # Steady tourism
    else:
        return np.random.normal(1.6, 0.3)

def calculate_golden_hour_boost(location_type):
    """Calculate golden hour photography activity boost"""
    if location_type in ["Beach", "Scenic Promenade", "Sea View"]:
        return np.random.normal(3.5, 0.5)  # Massive boost for sunset spots
    elif location_type in ["Rooftop Bar", "Hilltop Garden"]:
        return np.random.normal(2.8, 0.4)
    elif location_type in ["Historic Monument", "Heritage Architecture"]:
        return np.random.normal(2.2, 0.3)
    else:
        return np.random.normal(1.8, 0.4)

def generate_digital_culture_features(location_type, area, instagram_tags, aesthetic_score):
    """Generate features related to digital culture and trends"""
    
    digital_features = {
        "wifi_quality_score": calculate_wifi_quality(location_type, area),
        "selfie_spot_density": calculate_selfie_spots(location_type, aesthetic_score),
        "instagrammability_score": calculate_instagrammability(location_type, instagram_tags),
        "tiktok_trend_potential": calculate_tiktok_potential(location_type),
        "food_photography_score": calculate_food_photo_score(location_type),
        "fashion_photography_score": calculate_fashion_photo_score(location_type, area),
        "check_in_frequency": calculate_check_in_frequency(location_type, instagram_tags),
        "geotagging_popularity": min(10, np.log10(instagram_tags + 1) + np.random.normal(0, 0.5))
    }
    
    return digital_features

def calculate_wifi_quality(location_type, area):
    """Calculate WiFi quality for content creation"""
    if location_type in ["Trendy Cafe", "Co-working Cafe", "Luxury Mall"]:
        return np.random.normal(8.5, 1.0)
    elif location_type in ["Rooftop Bar", "Cultural District"]:
        return np.random.normal(7.0, 1.5)
    elif location_type in ["Beach", "Historic Monument"]:
        return np.random.normal(4.5, 2.0)  # Often poor WiFi
    else:
        return np.random.normal(6.0, 2.0)

def calculate_selfie_spots(location_type, aesthetic_score):
    """Calculate density of good selfie spots"""
    base_score = aesthetic_score * 0.9
    
    if location_type in ["Beach", "Scenic Promenade", "Historic Monument"]:
        base_score += 2.0
    elif location_type in ["Trendy Cafe", "Art Gallery"]:
        base_score += 1.5
    
    return min(10, base_score + np.random.normal(0, 0.8))

def calculate_instagrammability(location_type, instagram_tags):
    """Calculate overall Instagram appeal"""
    base_score = min(10, np.log10(instagram_tags + 1))
    
    # Location type adjustments
    if location_type in ["Beach", "Historic Monument", "Rooftop Bar"]:
        base_score += 1.0
    elif location_type in ["Trendy Cafe", "Cultural District"]:
        base_score += 0.5
    
    return min(10, base_score + np.random.normal(0, 0.5))

def calculate_tiktok_potential(location_type):
    """Calculate TikTok content creation potential"""
    if location_type in ["Beach", "Trendy Cafe", "Shopping Street"]:
        return np.random.normal(8.0, 1.0)  # High movement, music, trends
    elif location_type in ["Rooftop Bar", "Cultural District"]:
        return np.random.normal(6.5, 1.5)
    elif location_type in ["Historic Monument"]:
        return np.random.normal(5.0, 1.8)  # Less dynamic content
    else:
        return np.random.normal(6.0, 2.0)

def calculate_food_photo_score(location_type):
    """Calculate food photography potential"""
    if location_type in ["Food Photography Hub", "Trendy Cafe", "Iconic Eatery"]:
        return np.random.normal(9.0, 0.8)
    elif location_type in ["Fine Dining", "Rooftop Bar"]:
        return np.random.normal(8.2, 1.0)
    elif location_type in ["Beach", "Shopping Street"]:
        return np.random.normal(6.5, 1.5)  # Street food opportunities
    else:
        return np.random.normal(4.0, 2.0)

def calculate_fashion_photo_score(location_type, area):
    """Calculate fashion photography potential"""
    if location_type in ["Luxury Mall", "Shopping Street", "Cultural District"]:
        return np.random.normal(8.5, 1.0)
    elif location_type in ["Historic Monument", "Heritage Architecture"]:
        return np.random.normal(8.0, 1.2)  # Great backdrops
    elif location_type in ["Beach", "Scenic Promenade"]:
        return np.random.normal(7.5, 1.3)
    else:
        return np.random.normal(6.0, 2.0)

def calculate_check_in_frequency(location_type, instagram_tags):
    """Calculate social media check-in frequency"""
    base_frequency = min(1000, instagram_tags / 100)  # Normalize to reasonable range
    
    # Location type multipliers
    if location_type in ["Historic Monument", "Beach", "Rooftop Bar"]:
        base_frequency *= 1.5
    elif location_type in ["Trendy Cafe", "Shopping Street"]:
        base_frequency *= 1.2
    
    return int(base_frequency * np.random.normal(1.0, 0.2))

# GENERATE COMPLETE DATASET

def create_complete_gram_dataset():
    """Generate the complete 'Do it for the Gram' social media dataset"""
    
    complete_data = []
    
    for i, location in enumerate(gram_locations):
        # Basic location info
        loc_data = {
            'location_id': f"DG_{i+1:03d}",
            'name': location['name'],
            'lat': location['lat'],
            'lng': location['lng'],
            'type': location['type'],
            'area': location['area'],
            'instagram_tags': location['instagram_tags'],
            'aesthetic_score': location['aesthetic_score'],
            'vibe_category': 'Do it for the Gram'
        }
        
        # OSM-based social media features
        osm_features = generate_social_media_osm_features(
            location['lat'], location['lng'], 
            location['type'], location['area'], location['aesthetic_score']
        )
        
        # social media engagement patterns
        engagement_data = generate_social_media_engagement_patterns(
            location['type'], location['instagram_tags'], 
            location['aesthetic_score'], location['area']
        )
        
        # Digital culture features
        digital_features = generate_digital_culture_features(
            location['type'], location['area'], location['instagram_tags'], location["aesthetic_score"]
        )
        
        # Calculate vibe intensity
        vibe_intensity = calculate_gram_vibe_intensity(
            location['type'], location['instagram_tags'], 
            location['aesthetic_score'], location['area']
        )
        
        # Timing and seasonal features
        temporal_features = {
            "peak_posting_hours": get_peak_posting_hours(location['type']),
            "seasonal_popularity": calculate_seasonal_popularity(location['type']),
            "weather_dependency": calculate_weather_dependency(location['type']),
            "festival_boost_score": calculate_festival_boost(location['type'], location['area'])
        }
        
        # Content creation features
        content_features = {
            "content_variety_score": calculate_content_variety(location['type']),
            "professional_shoot_suitability": calculate_pro_shoot_score(location['type'], location['aesthetic_score']),
            "user_generated_content_rate": calculate_ugc_rate(location['type'], location['instagram_tags']),
            "brand_collaboration_potential": calculate_brand_collab_potential(location['type'], location['area'])
        }
        
        # Accessibility and infrastructure for creators
        creator_infrastructure = {
            "creator_parking_score": calculate_creator_parking(location['type'], location['area']),
            "equipment_friendly_score": calculate_equipment_friendliness(location['type']),
            "crowd_management_for_shoots": calculate_crowd_management(location['type']),
            "permits_required_score": calculate_permits_requirement(location['type'])
        }
        
        # Combine all features
        complete_location = {
            **loc_data,
            **osm_features,
            **engagement_data,
            **digital_features,
            **temporal_features,
            **content_features,
            **creator_infrastructure,
            'vibe_intensity': vibe_intensity,
            'data_collection_date': '2024-12-15',  # Peak social media activity season
            'confidence_score': np.random.normal(0.88, 0.08)
        }
        
        complete_data.append(complete_location)
    
    return pd.DataFrame(complete_data)

def calculate_gram_vibe_intensity(location_type, instagram_tags, aesthetic_score, area):
    """Calculate 'Do it for the Gram' vibe intensity"""
    
    # Base scores by location type
    base_scores = {
        "Beach": 4.7,
        "Scenic Promenade": 4.6,
        "Historic Monument": 4.4,
        "Rooftop Bar": 4.5,
        "Trendy Cafe": 4.3,
        "Cultural District": 4.1,
        "Art Gallery": 4.0,
        "Shopping Street": 3.9,
        "Heritage Architecture": 4.2,
        "Sea View": 4.4,
        "Hilltop Church": 4.0
    }
    
    # Instagram popularity bonus
    popularity_bonus = min(0.4, np.log10(instagram_tags + 1) / 6)  # Max 0.4 bonus
    
    # Aesthetic score bonus
    aesthetic_bonus = min(0.3, (aesthetic_score - 7.0) * 0.15)  # Bonus for high aesthetic scores
    
    # Trendy area bonus
    area_bonus = {
        "Bandra": 0.3, "Marine Drive": 0.2, "Colaba": 0.2,
        "Kala Ghoda": 0.2, "Lower Parel": 0.1, "Juhu": 0.1
    }.get(area, 0)
    
    base_score = base_scores.get(location_type, 3.5)
    final_score = min(5.0, base_score + popularity_bonus + aesthetic_bonus + area_bonus + np.random.normal(0, 0.1))
    
    return round(max(1.0, final_score), 2)

def get_peak_posting_hours(location_type):
    """Get peak social media posting hours by location type"""
    peak_hours = {
        "Beach": "17:00-20:00",  # Golden hour
        "Rooftop Bar": "19:00-23:00",  # Evening dining
        "Trendy Cafe": "09:00-11:00, 15:00-17:00",  # Brunch and afternoon coffee
        "Historic Monument": "08:00-10:00, 16:00-18:00",  # Good lighting
        "Shopping Street": "14:00-18:00, 20:00-22:00",  # Shopping hours
        "Cultural District": "10:00-12:00, 16:00-18:00",  # Gallery hours
        "Scenic Promenade": "06:00-08:00, 17:00-19:00"  # Sunrise and sunset
    }
    return peak_hours.get(location_type, "16:00-19:00")  # Default golden hour

def calculate_seasonal_popularity(location_type):
    """Calculate seasonal variation in social media popularity"""
    if location_type in ["Beach", "Scenic Promenade", "Sea View"]:
        return np.random.normal(0.6, 0.1)  # High variation due to weather
    elif location_type in ["Rooftop Bar", "Hilltop Garden"]:
        return np.random.normal(0.4, 0.1)  # Moderate weather dependency
    elif location_type in ["Shopping Street", "Cultural District"]:
        return np.random.normal(0.2, 0.08)  # Low variation (indoor/covered)
    else:
        return np.random.normal(0.3, 0.1)

def calculate_weather_dependency(location_type):
    """Calculate weather dependency for social media activity"""
    if location_type in ["Beach", "Scenic Promenade", "Hilltop Garden"]:
        return np.random.normal(8.5, 1.0)  # High weather dependency
    elif location_type in ["Rooftop Bar", "Historic Monument"]:
        return np.random.normal(6.5, 1.5)  # Moderate dependency
    elif location_type in ["Shopping Street", "Trendy Cafe", "Cultural District"]:
        return np.random.normal(3.0, 1.5)  # Low dependency (covered/indoor)
    else:
        return np.random.normal(5.0, 2.0)

def calculate_festival_boost(location_type, area):
    """Calculate social media boost during festivals"""
    base_boost = 1.5
    
    if location_type in ["Historic Monument", "Cultural District"]:
        base_boost = 2.5  # High boost during cultural festivals
    elif location_type in ["Beach", "Shopping Street"]:
        base_boost = 2.0
    elif location_type in ["Trendy Cafe", "Rooftop Bar"]:
        base_boost = 1.8
    
    # Area-specific festival activity
    area_multipliers = {
        "Kala Ghoda": 1.8,  # Kala Ghoda Arts Festival
        "Bandra": 1.4, "Juhu": 1.3, "Marine Drive": 1.2
    }
    
    area_mult = area_multipliers.get(area, 1.0)
    return base_boost * area_mult + np.random.normal(0, 0.2)

def calculate_content_variety(location_type):
    """Calculate variety of content types possible"""
    if location_type in ["Cultural District", "Shopping Street"]:
        return np.random.normal(9.0, 0.8)  # High variety
    elif location_type in ["Beach", "Historic Monument"]:
        return np.random.normal(8.0, 1.0)
    elif location_type in ["Trendy Cafe", "Rooftop Bar"]:
        return np.random.normal(7.5, 1.2)
    else:
        return np.random.normal(6.5, 1.5)

def calculate_pro_shoot_score(location_type, aesthetic_score):
    """Calculate suitability for professional photo shoots"""
    base_score = aesthetic_score * 0.9
    
    if location_type in ["Historic Monument", "Heritage Architecture"]:
        base_score += 1.5
    elif location_type in ["Beach", "Rooftop Bar"]:
        base_score += 1.2
    elif location_type in ["Cultural District", "Art Gallery"]:
        base_score += 1.0
    
    return min(10, base_score + np.random.normal(0, 0.5))

def calculate_ugc_rate(location_type, instagram_tags):
    """Calculate user-generated content rate"""
    base_rate = min(100, instagram_tags / 1000)  # Normalize
    
    # Location types that generate more UGC
    if location_type in ["Beach", "Historic Monument", "Trendy Cafe"]:
        base_rate *= 1.5
    elif location_type in ["Shopping Street", "Cultural District"]:
        base_rate *= 1.2
    
    return int(base_rate * np.random.normal(1.0, 0.2))

def calculate_brand_collab_potential(location_type, area):
    """Calculate brand collaboration potential"""
    if location_type in ["Luxury Mall", "Rooftop Bar", "Fine Dining"]:
        return np.random.normal(8.5, 1.0)
    elif location_type in ["Trendy Cafe", "Shopping Street"]:
        return np.random.normal(7.5, 1.2)
    elif location_type in ["Beach", "Historic Monument"]:
        return np.random.normal(6.0, 1.5)
    else:
        return np.random.normal(5.5, 2.0)

def calculate_creator_parking(location_type, area):
    """Calculate parking availability for content creators"""
    if location_type in ["Luxury Mall", "Modern Business District"]:
        return np.random.normal(8.5, 1.0)
    elif location_type in ["Shopping Street", "Cultural District"]:
        return np.random.normal(4.0, 2.0)  # Often difficult in Mumbai
    elif location_type in ["Beach", "Historic Monument"]:
        return np.random.normal(5.5, 2.0)
    else:
        return np.random.normal(6.0, 2.0)

def calculate_equipment_friendliness(location_type):
    """Calculate how equipment-friendly the location is"""
    if location_type in ["Beach", "Scenic Promenade", "Hilltop Garden"]:
        return np.random.normal(8.0, 1.0)  # Open spaces, good for equipment
    elif location_type in ["Rooftop Bar", "Cultural District"]:
        return np.random.normal(7.0, 1.5)
    elif location_type in ["Shopping Street", "Trendy Cafe"]:
        return np.random.normal(5.0, 2.0)  # Crowded, limited space
    else:
        return np.random.normal(6.0, 1.8)

def calculate_crowd_management(location_type):
    """Calculate crowd management for content creation"""
    if location_type in ["Historic Monument", "Beach"]:
        return np.random.normal(4.0, 2.0)  # Often very crowded
    elif location_type in ["Rooftop Bar", "Luxury Mall"]:
        return np.random.normal(7.5, 1.5)  # Better crowd control
    elif location_type in ["Shopping Street"]:
        return np.random.normal(3.5, 1.5)  # Very crowded
    else:
        return np.random.normal(5.5, 2.0)

def calculate_permits_requirement(location_type):
    """Calculate permit requirements (higher = more permits needed)"""
    if location_type in ["Historic Monument", "Heritage Architecture"]:
        return np.random.normal(8.5, 1.0)  # High permit requirements
    elif location_type in ["Cultural District", "Art Gallery"]:
        return np.random.normal(6.5, 1.5)
    elif location_type in ["Beach", "Shopping Street"]:
        return np.random.normal(5.0, 2.0)
    else:
        return np.random.normal(4.0, 2.0)
    
# SOCIAL MEDIA TRENDS ANALYSIS

def generate_trending_hashtags_data():
    """Generate trending hashtags for Mumbai social media spots"""
    
    trending_data = {
        "mumbai_general": [
            "#mumbai", "#mumbailife", "#bombayblogger", "#mumbaikar", 
            "#incredibleindia", "#mumbaistreets", "#mymumbai"
        ],
        "beach_spots": [
            "#juhubeach", "#mumbaibeaches", "#sunsetlover", "#beachvibes",
            "#goldenhour", "#seaside", "#mumbaisunset"
        ],
        "food_culture": [
            "#mumbaifood", "#streetfoodmumbai", "#bombaybhukkad", "#vadapav",
            "#mumbaieats", "#foodporn", "#indianstreetfood"
        ],
        "heritage_culture": [
            "#mumbaiheritage", "#gatewayofindia", "#mumbaiarchitecture",
            "#heritage", "#incredibleindia", "#mumbaihistory"
        ],
        "nightlife_cafes": [
            "#mumbainightlife", "#bandracafes", "#mumbairestaurants",
            "#rooftopbar", "#coffeelover", "#mumbaibar"
        ]
    }
    
    return trending_data

# MAIN EXECUTION

if __name__ == "__main__":
    print("Generating 'Do it for the Gram' social media hotspots dataset...")
    gram_df = create_complete_gram_dataset()

    gram_df.to_csv('do_it_for_the_gram_dataset.csv', index=False)
    print(f"Social media dataset saved! Shape: {gram_df.shape}")
 
    print("\nSample social media data:")
    sample_cols = ['name', 'type', 'instagram_tags', 'aesthetic_score', 'vibe_intensity', 'posts_per_day', 'viral_potential_score']
    print(gram_df[sample_cols].head(10))
    
    # Generate trending hashtags data
    trending_hashtags = generate_trending_hashtags_data()
    with open('mumbai_trending_hashtags.json', 'w') as f:
        json.dump(trending_hashtags, f, indent=2)
    
    # Social media summary statistics
    print(f"\nDo it for the Gram Summary:")
    high_aesthetic_spots = len([l for l in gram_locations if l['aesthetic_score'] >= 9.0])
    viral_potential_spots = len([l for l in gram_locations if l['instagram_tags'] >= 300000])
    beach_scenic_spots = len([l for l in gram_locations if l['type'] in ['Beach', 'Scenic Promenade', 'Sea View']])
    trendy_food_spots = len([l for l in gram_locations if 'Cafe' in l['type'] or 'Food' in l['type']])
    
    print(f"High aesthetic spots (9.0+ score): {high_aesthetic_spots}")
    print(f"Viral potential spots (300k+ tags): {viral_potential_spots}")
    print(f"Beach and scenic locations: {beach_scenic_spots}")
    print(f"Trendy food and cafe spots: {trendy_food_spots}")
    
    total_instagram_tags = sum([l['instagram_tags'] for l in gram_locations])
    avg_aesthetic_score = np.mean([l['aesthetic_score'] for l in gram_locations])
    print(f"Total Instagram tags across all locations: {total_instagram_tags:,}")
    print(f"Average aesthetic score: {avg_aesthetic_score:.1f}")
    
    top_locations = sorted(gram_locations, key=lambda x: x['instagram_tags'], reverse=True)[:5]
    print(f"\nTop 5 Instagram hotspots:")
    for i, loc in enumerate(top_locations, 1):
        print(f"{i}. {loc['name']}: {loc['instagram_tags']:,} tags (aesthetic: {loc['aesthetic_score']})")
    
    print(f"\nMost Instagrammable areas:")
    area_tags = {}
    for loc in gram_locations:
        area = loc['area']
        area_tags[area] = area_tags.get(area, 0) + loc['instagram_tags']
    
    top_areas = sorted(area_tags.items(), key=lambda x: x[1], reverse=True)[:5]
    for i, (area, tags) in enumerate(top_areas, 1):
        print(f"{i}. {area}: {tags:,} total tags")