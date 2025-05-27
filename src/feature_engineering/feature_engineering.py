import pandas as pd
import numpy as np
import json
from geopy.distance import geodesic
import time
from datetime import datetime, timedelta

class EnhancedMumbaiVibeFeatureEngineering:
    
    def __init__(self, heritage_walks_path="data/raw/heritage_walks_data.csv", 
                 hashtags_path="data/raw/mumbai_trending_hashtags.json",
                 busy_areas_path="data/raw/busy_areas.json"):

        self.heritage_walks_df = pd.read_csv(heritage_walks_path)
        
        with open(hashtags_path, 'r') as f:
            self.trending_hashtags = json.load(f)
        
        with open(busy_areas_path, 'r') as f:
            self.busy_areas_data = json.load(f)
        self._process_heritage_walks_data()

        self._process_congestion_data()
        
        self.mumbai_knowledge = {
            # Original knowledge + enhanced from contextual data
            'major_ganesh_areas': [
                (19.0176, 72.8381),  # Lalbaugcha Raja
                (19.0334, 72.8467),  # Ganesh Galli
                (18.9547, 72.8081),  # Girgaon Chowpatty
                (19.0189, 72.8467)   # Dadar Chowpatty
            ],
            
            'heritage_districts': [
                (18.9314, 72.8311),  # Fort
                (18.9379, 72.8400),  # Ballard Estate
                (18.9269, 72.8324),  # Kala Ghoda
                (18.9436, 72.8228)   # Marine Drive (Art Deco)
            ],
            
            'food_hubs': [
                (18.9589, 72.8333),  # Mohammed Ali Road
                (18.9378, 72.8378),  # Khau Galli
                (19.0256, 72.8489),  # Matunga (South Indian)
                (19.0544, 72.8267)   # Bandra food scene
            ],
            
            'hustle_centers': [
                (19.0189, 72.8467),  # Dadar junction
                (19.1197, 72.8467),  # Andheri hub
                (18.9314, 72.8289),  # Churchgate
                (19.0656, 72.8678)   # BKC
            ],
            
            'gram_spots': [
                (18.9436, 72.8228),  # Marine Drive
                (19.0544, 72.8181),  # Bandra Bandstand
                (18.9896, 72.8267),  # Juhu Beach
                (18.9269, 72.8324)   # Kala Ghoda
            ],
            
            'water_bodies': [
                (18.9547, 72.8081),  # Girgaon Chowpatty
                (19.0189, 72.8467),  # Dadar Chowpatty
                (18.9896, 72.8267),  # Juhu Beach
                (19.1317, 72.8128)   # Versova Beach
            ],
            
            # From busy_areas.json
            'congestion_hotspots': self.congestion_coordinates,
            'heritage_walk_routes': self.heritage_walk_coordinates
        }
    
    def _process_heritage_walks_data(self):
        """Process heritage walks data to extract coordinates"""
        
        # Map heritage walk locations to approximate coordinates
        heritage_location_coords = {
            'Gateway of India': (18.9220, 72.8347),
            'Taj Mahal Palace': (18.9216, 72.8331),
            'University of Mumbai': (18.9292, 72.8317),
            'High Court': (18.9292, 72.8317),
            'Marine Drive Buildings': (18.9436, 72.8228),
            'Eros Cinema': (18.9314, 72.8289),
            'Liberty Cinema': (18.9347, 72.8278),
            'Oval Maidan': (18.9269, 72.8289),
            'Phoenix Mills': (19.0134, 72.8333),
            'Standard Mills': (19.0145, 72.8334),
            'Century Mills': (19.0089, 72.8267),
            'Swadeshi Mills': (19.0178, 72.8356),
            'Sewri Fort': (19.0067, 72.8556),
            'Mahim Fort': (19.0378, 72.8356),
            'Worli Fort': (19.0089, 72.8111),
            'Sion Fort': (19.0434, 72.8634),
            'Crawford Market': (18.9467, 72.8342),
            'Zaveri Bazaar': (18.9467, 72.8342),
            'Chor Bazaar': (18.9589, 72.8333),
            'Mangaldas Market': (18.9467, 72.8300)
        }
        
        # Create heritage walk coordinate mapping
        self.heritage_walk_coordinates = {}
        
        for _, walk in self.heritage_walks_df.iterrows():
            walk_name = walk['walk_name']
            locations_str = walk['locations_covered']

            locations = eval(locations_str)
            coords = []
            
            for location in locations:
                if location in heritage_location_coords:
                    coords.append(heritage_location_coords[location])
            
            self.heritage_walk_coordinates[walk_name] = {
                'coordinates': coords,
                'duration': walk['duration_hours'],
                'difficulty': walk['difficulty'],
                'frequency': walk['frequency_per_week']
            }
    
    def _process_congestion_data(self):
        """Process congestion data to extract coordinates"""
        
        # Map congestion hotspots to coordinates
        congestion_coords_map = {
            "Dadar TT Circle": (19.0189, 72.8445),
            "Andheri Subway": (19.1197, 72.8467),
            "Bandra Kalanagar Junction": (19.0656, 72.8378)
        }
        
        self.congestion_coordinates = []
        for hotspot in self.busy_areas_data['congestion_hotspots']:
            if hotspot in congestion_coords_map:
                self.congestion_coordinates.append(congestion_coords_map[hotspot])
    
    def extract_enhanced_smart_features(self, df, vibe_category):
        """
        Extract enhanced smart features including contextual data
        """
        
        print(f"\nEnhanced Smart Feature Engineering for {vibe_category}")
        print(f"Processing {len(df)} locations with contextual intelligence...")
        
        enhanced_df = df.copy()
        
        # Original vibe-specific features
        if vibe_category == "Ganesh Gully Energy":
            enhanced_df = self._extract_ganesh_enhanced_features(enhanced_df)
        elif vibe_category == "Kickin' it old school":
            enhanced_df = self._extract_heritage_enhanced_features(enhanced_df)
        elif vibe_category == "Bombay Bhukkad":
            enhanced_df = self._extract_food_enhanced_features(enhanced_df)
        elif vibe_category == "Chaotic Hustle":
            enhanced_df = self._extract_urban_enhanced_features(enhanced_df)
        elif vibe_category == "Do it for the Gram":
            enhanced_df = self._extract_social_enhanced_features(enhanced_df)
        
        # Add contextual features from additional data
        enhanced_df = self._add_heritage_walks_features(enhanced_df, vibe_category)
        enhanced_df = self._add_hashtag_intelligence_features(enhanced_df, vibe_category)
        enhanced_df = self._add_congestion_intelligence_features(enhanced_df, vibe_category)
        
        # Smart temporal features
        enhanced_df = self._add_smart_temporal_features(enhanced_df, vibe_category)
        
        # SCalculate final enhanced vibe intensity
        enhanced_df = self._calculate_contextual_vibe_intensity(enhanced_df, vibe_category)
        
        return enhanced_df
    
    def _extract_ganesh_enhanced_features(self, df):
        """Enhanced Ganesh features"""
        print(" Extracting enhanced Ganesh-specific features...")
        df['distance_to_major_ganesh_area'] = df.apply(
            lambda row: self._min_distance_to_areas(
                row['lat'], row['lng'], self.mumbai_knowledge['major_ganesh_areas']
            ), axis=1
        )
        
        df['distance_to_visarjan_spot'] = df.apply(
            lambda row: self._min_distance_to_areas(
                row['lat'], row['lng'], self.mumbai_knowledge['water_bodies']
            ), axis=1
        )
        
        df['festival_infrastructure_score'] = df['type'].map({
            'Famous Pandal': 9.5, 'Visarjan Spot': 9.0, 'Procession Route': 8.5,
            'Temple': 8.0, 'Workshop Area': 7.0, 'Festival Market': 7.5,
            'Community Center': 6.5, 'Sarvajanik Mandal': 7.8
        }).fillna(5.0)
        
        if 'festival_day_traffic' in df.columns:
            df['crowd_capacity_score'] = np.log10(df['festival_day_traffic'] + 1)
        else:
            df['crowd_capacity_score'] = 5.0
        
        df['cultural_significance_multiplier'] = df['name'].apply(
            lambda name: 2.0 if 'Lalbaugcha Raja' in name 
                         else 1.5 if any(x in name for x in ['Raja', 'King', 'Ganraj'])
                         else 1.0
        )
        
        return df
    
    def _extract_heritage_enhanced_features(self, df):
        """Enhanced Heritage features"""
        print("Extracting enhanced Heritage-specific features...")
        
        df['distance_to_heritage_district'] = df.apply(
            lambda row: self._min_distance_to_areas(
                row['lat'], row['lng'], self.mumbai_knowledge['heritage_districts']
            ), axis=1
        )
        
        if 'built_year' in df.columns:
            df['architectural_era_score'] = df['built_year'].apply(
                lambda year: 9.5 if year < 1850 else 8.5 if year < 1900 
                             else 8.0 if year < 1920 else 7.5 if year < 1950 else 5.0
            )
            df['heritage_age_significance'] = (2024 - df['built_year']).apply(
                lambda age: min(10, age / 20)
            )
        else:
            df['architectural_era_score'] = 7.0
            df['heritage_age_significance'] = 7.0
        
        df['heritage_importance_score'] = df.get('heritage_status', 'Unknown').map({
            'UNESCO World Heritage': 10.0, 'Grade I Heritage': 9.0, 'ASI Protected': 8.5,
            'Grade II Heritage': 7.5, 'Heritage Precinct': 8.0, 'Industrial Heritage': 6.5,
            'Railway Heritage': 7.0, 'Historic Market': 6.0
        }).fillna(5.0)
        
        return df
    
    def _extract_food_enhanced_features(self, df):
        """Enhanced Food features"""
        print("Extracting enhanced Food-specific features...")
        
        df['distance_to_food_hub'] = df.apply(
            lambda row: self._min_distance_to_areas(
                row['lat'], row['lng'], self.mumbai_knowledge['food_hubs']
            ), axis=1
        )
        
        if 'established_year' in df.columns:
            df['culinary_heritage_score'] = df['established_year'].apply(
                lambda year: 10.0 if year < 1920 else 8.5 if year < 1950 
                             else 7.0 if year < 1980 else 5.0
            )
        else:
            df['culinary_heritage_score'] = 6.0
        
        df['food_authenticity_score'] = df['type'].map({
            'Street Food Hub': 9.5, 'Irani Cafe': 9.0, 'Street Food Lane': 9.0,
            'Parsi Restaurant': 8.5, 'Tea Stall': 8.5, 'Sweet Shop': 8.0,
            'Mall Food Court': 3.0, 'Fine Dining': 5.0
        }).fillna(6.0)
        
        return df
    
    def _extract_urban_enhanced_features(self, df):
        """Enhanced Urban Energy features"""
        print("Extracting enhanced Urban Energy-specific features...")
        
        df['distance_to_hustle_center'] = df.apply(
            lambda row: self._min_distance_to_areas(
                row['lat'], row['lng'], self.mumbai_knowledge['hustle_centers']
            ), axis=1
        )
        
        if 'daily_footfall' in df.columns and 'peak_multiplier' in df.columns:
            df['peak_chaos_intensity'] = np.log10(df['daily_footfall'] * df['peak_multiplier'])
        else:
            df['peak_chaos_intensity'] = 5.0
        
        df['transport_stress_score'] = df['type'].map({
            'Major Hub': 10.0, 'Terminus Station': 9.5, 'Junction Station': 9.0,
            'Traffic Junction': 8.5, 'Highway Junction': 8.0, 'Metro Hub': 7.5,
            'Bus Terminal': 7.0, 'Business District': 6.0, 'Shopping Mall': 5.0
        }).fillna(5.0)
        
        return df
    
    def _extract_social_enhanced_features(self, df):
        """Enhanced Social Media features"""
        print("Extracting enhanced Social Media-specific features...")
        
        df['distance_to_gram_hotspot'] = df.apply(
            lambda row: self._min_distance_to_areas(
                row['lat'], row['lng'], self.mumbai_knowledge['gram_spots']
            ), axis=1
        )
        
        if 'instagram_tags' in df.columns and 'aesthetic_score' in df.columns:
            df['virality_potential'] = (
                np.log10(df['instagram_tags'] + 1) * 0.6 + 
                df['aesthetic_score'] * 0.4
            )
        else:
            df['virality_potential'] = 6.0
        
        df['content_creation_score'] = df['type'].map({
            'Beach': 9.5, 'Scenic Promenade': 9.0, 'Historic Monument': 8.5,
            'Trendy Cafe': 8.5, 'Rooftop Bar': 8.0, 'Cultural District': 8.0
        }).fillna(6.0)
        
        df['golden_hour_appeal'] = df['type'].apply(
            lambda t: 10.0 if any(x in t for x in ['Beach', 'Scenic', 'Waterfront', 'Sea View'])
                     else 8.0 if any(x in t for x in ['Rooftop', 'Hilltop', 'Bridge View'])
                     else 6.0 if 'Historic Monument' in t else 4.0
        )
        
        return df
    
    def _add_heritage_walks_features(self, df, vibe_category):
        """Add features based on heritage walks data"""
        print("Adding heritage walks intelligence...")

        df['heritage_walk_accessibility'] = df.apply(
            lambda row: self._calculate_heritage_walk_accessibility(row['lat'], row['lng']), axis=1
        )
        
        df['tourism_infrastructure_score'] = df.apply(
            lambda row: self._calculate_tourism_infrastructure(row['lat'], row['lng']), axis=1
        )

        df['walking_tour_frequency'] = df.apply(
            lambda row: self._calculate_walking_tour_frequency(row['lat'], row['lng']), axis=1
        )
        
        return df
    
    def _add_hashtag_intelligence_features(self, df, vibe_category):
        """Add features based on trending hashtags data"""
        print(" Adding hashtag intelligence...")
        
        # Map vibe categories to hashtag categories
        vibe_to_hashtag_mapping = {
            "Ganesh Gully Energy": "mumbai_general",
            "Kickin' it old school": "heritage_culture", 
            "Bombay Bhukkad": "food_culture",
            "Chaotic Hustle": "mumbai_general",
            "Do it for the Gram": ["beach_spots", "nightlife_cafes"]
        }
        
        hashtag_categories = vibe_to_hashtag_mapping.get(vibe_category, "mumbai_general")
        
        if isinstance(hashtag_categories, list):
            # Multiple hashtag categories (like for "Do it for the Gram")
            total_hashtags = sum([len(self.trending_hashtags[cat]) for cat in hashtag_categories])
        else:
            total_hashtags = len(self.trending_hashtags.get(hashtag_categories, []))
        
        # Hashtag trend strength (more hashtags = stronger social media presence)
        df['hashtag_trend_strength'] = total_hashtags / 2  # Normalize to reasonable scale
        
        if vibe_category == "Do it for the Gram":
            df['beach_hashtag_potential'] = len(self.trending_hashtags['beach_spots'])
            df['nightlife_hashtag_potential'] = len(self.trending_hashtags['nightlife_cafes'])
            df['food_hashtag_overlap'] = len(self.trending_hashtags['food_culture']) * 0.3  
        elif vibe_category == "Bombay Bhukkad":
            df['food_hashtag_alignment'] = len(self.trending_hashtags['food_culture'])
        elif vibe_category == "Kickin' it old school":
            df['heritage_hashtag_alignment'] = len(self.trending_hashtags['heritage_culture'])
        
        return df
    
    def _add_congestion_intelligence_features(self, df, vibe_category):
        """Add features based on busy areas and congestion data"""
        print(" Adding congestion intelligence...")
        
        # Distance to congestion hotspots
        df['distance_to_congestion_hotspot'] = df.apply(
            lambda row: self._min_distance_to_areas(
                row['lat'], row['lng'], self.mumbai_knowledge['congestion_hotspots']
            ), axis=1
        )
        
        # Congestion impact score (higher for areas closer to hotspots)
        df['congestion_impact_score'] = df['distance_to_congestion_hotspot'].apply(
            lambda dist: max(0, 10 - dist / 200)  # Score decreases with distance
        )
        
        # Infrastructure stress indicator
        df['infrastructure_stress_indicator'] = df.apply(
            lambda row: self._calculate_infrastructure_stress(row['lat'], row['lng'], vibe_category), axis=1
        )
        
        # Peak hour chaos prediction
        df['peak_hour_chaos_prediction'] = df.apply(
            lambda row: self._predict_peak_hour_chaos(row['lat'], row['lng'], vibe_category), axis=1
        )
        
        return df
    
    def _add_smart_temporal_features(self, df, vibe_category):
        print("Adding smart temporal intelligence...")
        
        current_time = datetime.now()
        current_hour = current_time.hour
        current_month = current_time.month
        is_weekend = current_time.weekday() >= 5
        
        # Basic temporal context
        df['is_weekend'] = is_weekend
        df['current_month'] = current_month
        df['is_monsoon'] = current_month in [6, 7, 8, 9]
        df['is_tourist_season'] = current_month in [10, 11, 12, 1, 2]
        
        # Enhanced vibe-specific temporal features
        if vibe_category == "Ganesh Gully Energy":
            df['is_ganesh_season'] = current_month in [8, 9]
            df['festival_temporal_boost'] = np.where(df['is_ganesh_season'], 3.0, 1.0)
            
        elif vibe_category == "Kickin' it old school":
            df['heritage_season_boost'] = np.where(df['is_tourist_season'], 1.8, 0.8)
            df['weekend_heritage_boost'] = np.where(is_weekend, 1.5, 1.0)
            # NEW: Heritage walks timing alignment
            df['heritage_walk_timing_alignment'] = self._calculate_walk_timing_alignment(current_hour)
            
        elif vibe_category == "Bombay Bhukkad":
            df['meal_time_boost'] = self._calculate_meal_time_boost(current_hour)
            
        elif vibe_category == "Chaotic Hustle":
            df['rush_hour_chaos'] = self._calculate_rush_hour_chaos(current_hour, is_weekend)
            # NEW: Enhanced with congestion data
            df['congestion_adjusted_chaos'] = df['rush_hour_chaos'] * (1 + df['congestion_impact_score'] / 10)
            
        elif vibe_category == "Do it for the Gram":
            df['golden_hour_boost'] = self._calculate_golden_hour_boost(current_hour)
            df['social_weekend_boost'] = np.where(is_weekend, 2.0, 1.0)
        
        return df
    
    def _calculate_heritage_walk_accessibility(self, lat, lng):
        """Calculate accessibility via heritage walking tours"""
        
        accessibility_score = 0
        
        for walk_name, walk_data in self.heritage_walk_coordinates.items():
            walk_coords = walk_data['coordinates']
            frequency = walk_data['frequency']
            
            # Check if location is near any walk route
            min_distance_to_walk = min([
                geodesic((lat, lng), coord).meters for coord in walk_coords
            ]) if walk_coords else float('inf')
            
            if min_distance_to_walk < 500:  # Within 500m of walk route
                # Score based on walk frequency and proximity
                walk_score = frequency * (500 - min_distance_to_walk) / 500
                accessibility_score += walk_score
        
        return min(10, accessibility_score)  # Cap at 10
    
    def _calculate_tourism_infrastructure(self, lat, lng):
        """Calculate tourism infrastructure quality"""
        
        # Based on heritage walks density and quality
        infrastructure_score = 0
        
        for walk_name, walk_data in self.heritage_walk_coordinates.items():
            walk_coords = walk_data['coordinates']
            difficulty = walk_data['difficulty']
            
            if walk_coords:
                min_distance = min([geodesic((lat, lng), coord).meters for coord in walk_coords])
                
                if min_distance < 1000:  # Within 1km
                    # Easier walks indicate better infrastructure
                    difficulty_score = 3 if difficulty == 'Easy' else 2 if difficulty == 'Moderate' else 1
                    proximity_score = (1000 - min_distance) / 1000
                    infrastructure_score += difficulty_score * proximity_score
        
        return min(10, infrastructure_score)
    
    def _calculate_walking_tour_frequency(self, lat, lng):
        """Calculate how frequently area is covered by walking tours"""
        
        total_frequency = 0
        
        for walk_name, walk_data in self.heritage_walk_coordinates.items():
            walk_coords = walk_data['coordinates']
            frequency = walk_data['frequency']
            
            if walk_coords:
                min_distance = min([geodesic((lat, lng), coord).meters for coord in walk_coords])
                
                if min_distance < 300:  # Very close to walk route
                    total_frequency += frequency
                elif min_distance < 600:  # Moderately close
                    total_frequency += frequency * 0.5
        
        return total_frequency
    
    def _calculate_infrastructure_stress(self, lat, lng, vibe_category):
        """Calculate infrastructure stress based on congestion data"""
        
        base_stress = 0

        for hotspot_coord in self.mumbai_knowledge['congestion_hotspots']:
            distance = geodesic((lat, lng), hotspot_coord).meters
            if distance < 1000:  # Within 1km of hotspot
                stress_contribution = (1000 - distance) / 1000 * 5 
                base_stress += stress_contribution
  
        if vibe_category == "Chaotic Hustle":
            base_stress *= 1.5 
        elif vibe_category == "Do it for the Gram":
            base_stress *= 0.7 
        
        return min(10, base_stress)
    
    def _predict_peak_hour_chaos(self, lat, lng, vibe_category):

        congestion_chaos = self._calculate_infrastructure_stress(lat, lng, vibe_category)
        current_hour = datetime.now().hour
        if 7 <= current_hour <= 11 or 17 <= current_hour <= 21: 
            time_multiplier = 2.0
        elif 12 <= current_hour <= 14: 
            time_multiplier = 1.5
        else:
            time_multiplier = 1.0
        
        return min(10, congestion_chaos * time_multiplier)
    
    def _calculate_walk_timing_alignment(self, current_hour):
        if 8 <= current_hour <= 11:  # Morning preferred time
            return 2.0
        elif 16 <= current_hour <= 18:  # Evening walk time
            return 1.5
        else:
            return 1.0
    
    def _calculate_meal_time_boost(self, current_hour):
        """Enhanced meal time boost calculation"""
        if 7 <= current_hour <= 11:  # Breakfast
            return 3.0
        elif 12 <= current_hour <= 15:  # Lunch peak
            return 4.0
        elif 19 <= current_hour <= 23:  # Dinner peak
            return 4.5
        elif 23 <= current_hour or current_hour <= 6:  # Late night
            return 2.0
        else:
            return 1.5
    
    def _calculate_rush_hour_chaos(self, current_hour, is_weekend):
        """Enhanced rush hour chaos calculation"""
        if is_weekend:
            return 2.0  # Weekend quieter
        elif 7 <= current_hour <= 11:  # Morning rush
            return 4.0
        elif 17 <= current_hour <= 21:  # Evening rush
            return 4.5
        else:
            return 2.5
    
    def _calculate_golden_hour_boost(self, current_hour):
        """Enhanced golden hour calculation for social media"""
        if 6 <= current_hour <= 8 or 17 <= current_hour <= 19:  # Golden hour
            return 2.5
        elif 19 <= current_hour <= 22:  # Evening social activity
            return 1.8
        else:
            return 1.0
    
        
    def _calculate_contextual_vibe_intensity(self, df, vibe_category):
        """Calculate final vibe intensity using all contextual features - FIXED VERSION"""
        
        base_intensity = df.get('vibe_intensity', 3.0)
        
        # Vibe-specific contextual enhancement
        if vibe_category == "Ganesh Gully Energy":
            # FIXED: Proper distance normalization
            distance_score = np.maximum(0, (2000 - df['distance_to_major_ganesh_area']) / 2000)  # 0-1 scale
            
            contextual_enhancement = (
                (df['festival_infrastructure_score'] / 10) * 0.25 +
                (df['cultural_significance_multiplier']) * 0.20 +
                (df['festival_temporal_boost'] / 3) * 0.15 +
                distance_score * 0.20 + 
                (df['hashtag_trend_strength'] / 10) * 0.10 +
                (df['congestion_impact_score'] / 10) * 0.10
            )
            
        elif vibe_category == "Kickin' it old school":
            contextual_enhancement = (
                (df['heritage_importance_score'] / 10) * 0.30 +
                (df['architectural_era_score'] / 10) * 0.25 +
                (df['heritage_walk_accessibility'] / 10) * 0.15 +
                (df['tourism_infrastructure_score'] / 10) * 0.15 +
                (df['heritage_hashtag_alignment'] / 10) * 0.10 +
                (df['heritage_walk_timing_alignment'] / 2) * 0.05
            )
            
        elif vibe_category == "Bombay Bhukkad":
            # FIXED: Similar distance normalization
            food_distance_score = np.maximum(0, (1500 - df['distance_to_food_hub']) / 1500)
            
            contextual_enhancement = (
                (df['culinary_heritage_score'] / 10) * 0.30 +
                (df['food_authenticity_score'] / 10) * 0.25 +
                (df['meal_time_boost'] / 5) * 0.20 +
                food_distance_score * 0.15 +  # FIXED
                (df['food_hashtag_alignment'] / 10) * 0.10
            )
            
        elif vibe_category == "Chaotic Hustle":
            contextual_enhancement = (
                (df['transport_stress_score'] / 10) * 0.25 +
                (df['peak_chaos_intensity'] / 10) * 0.25 +
                (df['congestion_adjusted_chaos'] / 5) * 0.20 +
                (df['infrastructure_stress_indicator'] / 10) * 0.15 +
                (df['peak_hour_chaos_prediction'] / 10) * 0.15
            )
            
        elif vibe_category == "Do it for the Gram":
            contextual_enhancement = (
                (df['content_creation_score'] / 10) * 0.25 +
                (df['virality_potential'] / 10) * 0.25 +
                (df['golden_hour_appeal'] / 10) * 0.20 +
                (df['beach_hashtag_potential'] / 10) * 0.10 +
                (df['nightlife_hashtag_potential'] / 10) * 0.10 +
                (df['golden_hour_boost'] / 3) * 0.10
            )
        else:
            contextual_enhancement = 1.0
 
        contextual_enhancement = np.maximum(0.1, contextual_enhancement)  # Minimum 0.1
        contextual_enhancement = np.minimum(2.0, contextual_enhancement)  # Maximum 2.0

        df['contextual_vibe_intensity'] = np.minimum(
            base_intensity * contextual_enhancement,
            5.0
        )
    
        df['original_vibe_intensity'] = base_intensity
        
        return df

    # HELPER METHODS
    def _min_distance_to_areas(self, lat, lng, area_list):
        """Calculate minimum distance to a list of important areas"""
        if not area_list:
            return 1000  # Default distance if no areas
        distances = [geodesic((lat, lng), area).meters for area in area_list]
        return min(distances)
    
    def process_all_enhanced_datasets(self, data_folder="data/raw/", output_folder="data/processed/"):
        """Process all vibe datasets with enhanced contextual feature engineering"""
        
        print("Mumbai Vibe Map - Enhanced Contextual Feature Engineering")
        print("Now incorporating heritage walks, hashtags, and congestion data!")
        print("="*70)
        
        vibe_files = {
            "Ganesh Gully Energy": "ganesh_energy_dataset.csv",
            "Kickin' it old school": "old_school_heritage_dataset.csv", 
            "Bombay Bhukkad": "bombay_bhukkad_dataset.csv",
            "Chaotic Hustle": "chaotic_hustle_dataset.csv",
            "Do it for the Gram": "do_it_for_the_gram_dataset.csv"
        }
        
        enhanced_datasets = {}
        
        for vibe_name, filename in vibe_files.items():
            input_path = f"{data_folder}{filename}"
            output_path = f"{output_folder}{filename.replace('.csv', '_enhanced.csv')}"
            
            try:
                print(f"\n{'='*50}")
                print(f"Processing: {vibe_name}")
                print(f"{'='*50}")
                
                # Load dataset
                df = pd.read_csv(input_path)
                print(f"Loaded: {input_path} ({len(df)} locations)")
                
                # Extract enhanced features with contextual data
                enhanced_df = self.extract_enhanced_smart_features(df, vibe_name)
                
                # Save enhanced dataset
                enhanced_df.to_csv(output_path, index=False)
                enhanced_datasets[vibe_name] = enhanced_df
                
                print(f"Saved: {output_path}")
                print(f"Features: {len(enhanced_df.columns)} total ({len(enhanced_df.columns) - len(df)} enhanced features added)")
                print(f"{vibe_name} enhanced successfully!")
                
            except Exception as e:
                print(f"Error processing {vibe_name}: {e}")
        
        # Generate comprehensive enhanced report
        self._generate_enhanced_feature_report(enhanced_datasets, output_folder)
        
        return enhanced_datasets
    
    def _generate_enhanced_feature_report(self, enhanced_datasets, output_folder):
        """Generate comprehensive enhanced feature engineering report"""
        
        report = {
            "enhanced_feature_engineering_summary": {
                "approach": "Contextual intelligence from heritage walks + hashtags + congestion data",
                "data_sources": [
                    "Core vibe datasets (5 vibes)",
                    "Heritage walks data (tourism intelligence)",
                    "Mumbai trending hashtags (social media intelligence)", 
                    "Busy areas data (congestion & infrastructure intelligence)"
                ],
                "total_vibes_processed": len(enhanced_datasets),
                "enhancement_philosophy": "Extract features that leverage ALL available Mumbai data"
            },
            
            "contextual_features_added": {
                "heritage_walks_intelligence": [
                    "heritage_walk_accessibility", "tourism_infrastructure_score", 
                    "walking_tour_frequency", "heritage_walk_timing_alignment"
                ],
                "hashtag_intelligence": [
                    "hashtag_trend_strength", "beach_hashtag_potential", 
                    "nightlife_hashtag_potential", "food_hashtag_alignment", "heritage_hashtag_alignment"
                ],
                "congestion_intelligence": [
                    "distance_to_congestion_hotspot", "congestion_impact_score",
                    "infrastructure_stress_indicator", "peak_hour_chaos_prediction", "congestion_adjusted_chaos"
                ]
            },
            
            "enhanced_vibe_features": {
                "Ganesh Gully Energy": [
                    "festival_infrastructure_score", "cultural_significance_multiplier",
                    "distance_to_visarjan_spot", "festival_temporal_boost",
                    "hashtag_trend_strength", "congestion_impact_score"
                ],
                "Kickin' it old school": [
                    "heritage_importance_score", "architectural_era_score", 
                    "heritage_walk_accessibility", "tourism_infrastructure_score",
                    "heritage_hashtag_alignment", "heritage_walk_timing_alignment"
                ],
                "Bombay Bhukkad": [
                    "culinary_heritage_score", "food_authenticity_score",
                    "distance_to_food_hub", "meal_time_boost", "food_hashtag_alignment"
                ],
                "Chaotic Hustle": [
                    "transport_stress_score", "peak_chaos_intensity",
                    "congestion_adjusted_chaos", "infrastructure_stress_indicator", 
                    "peak_hour_chaos_prediction"
                ],
                "Do it for the Gram": [
                    "virality_potential", "content_creation_score", "golden_hour_appeal",
                    "beach_hashtag_potential", "nightlife_hashtag_potential", "golden_hour_boost"
                ]
            },
            
            "datasets_processed": {},
            "contextual_insights": {}
        }
        
        for vibe_name, df in enhanced_datasets.items():
            # Analyze enhanced features
            contextual_cols = len([col for col in df.columns if any(
                contextual_feature in col for contextual_feature in [
                    'walk_', 'hashtag_', 'congestion_', 'infrastructure_', 'chaos_', 'tourism_'
                ]
            )])
            
            report["datasets_processed"][vibe_name] = {
                "total_locations": len(df),
                "total_features": len(df.columns),
                "contextual_features_added": contextual_cols,
                "avg_original_vibe_intensity": round(df['original_vibe_intensity'].mean(), 2) if 'original_vibe_intensity' in df.columns else None,
                "avg_contextual_vibe_intensity": round(df['contextual_vibe_intensity'].mean(), 2) if 'contextual_vibe_intensity' in df.columns else None,
                "enhancement_factor": round(df['contextual_vibe_intensity'].mean() / df['original_vibe_intensity'].mean(), 2) if all(col in df.columns for col in ['contextual_vibe_intensity', 'original_vibe_intensity']) else None
            }
        
        # Save comprehensive report
        with open(f'{output_folder}enhanced_contextual_report.json', 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"\nEnhanced Contextual Feature Engineering Report:")
        print(f"{'='*70}")
        
        for vibe_name, stats in report["datasets_processed"].items():
            print(f"\n{vibe_name}:")
            print(f"Locations: {stats['total_locations']}")
            print(f"Total features: {stats['total_features']}")
            print(f"Contextual features: {stats['contextual_features_added']}")
            if stats['enhancement_factor']:
                print(f"Vibe enhancement: {stats['avg_original_vibe_intensity']} → {stats['avg_contextual_vibe_intensity']} ({stats['enhancement_factor']}x)")
        
        print(f"\nEnhanced Intelligence Sources:")
        print(f"Heritage Walks: {len(self.heritage_walk_coordinates)} walking tours analyzed")
        print(f"Hashtag Intelligence: {sum(len(tags) for tags in self.trending_hashtags.values())} trending hashtags")
        print(f"Congestion Intelligence: {len(self.busy_areas_data['congestion_hotspots'])} hotspots + infrastructure insights")
        
        print(f"Enhanced report saved: {output_folder}enhanced_contextual_report.json")
        
        return report

def enhance_with_contextual_data(data_folder="data/raw/", output_folder="data/processed/",
                                heritage_walks_path="data/raw/heritage_walks_data.csv",
                                hashtags_path="data/raw/mumbai_trending_hashtags.json",
                                busy_areas_path="data/raw/busy_areas.json"):

    extractor = EnhancedMumbaiVibeFeatureEngineering(
        heritage_walks_path=heritage_walks_path,
        hashtags_path=hashtags_path, 
        busy_areas_path=busy_areas_path
    )
    
    enhanced_datasets = extractor.process_all_enhanced_datasets(data_folder, output_folder)
    
    print(f"ENHANCED CONTEXTUAL FEATURE ENGINEERING COMPLETE!")
    print(f"Enhanced datasets: {output_folder}")
    
    return enhanced_datasets

if __name__ == "__main__":
    import os
    enhanced_datasets = enhance_with_contextual_data()
    
    print(f"\nEnhanced Feature Engineering Results:")
    print(f"{'='*60}")
    
    total_locations = sum([len(df) for df in enhanced_datasets.values()])
    print(f"Enhanced Files Created:")
    for vibe in enhanced_datasets.keys():
        filename = vibe.lower().replace(' ', '_').replace("'", '')
        print(f"   - data/processed/{filename}_dataset_enhanced.csv")
    print(f"   - data/processed/enhanced_contextual_report.json")