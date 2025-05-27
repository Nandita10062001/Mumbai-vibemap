import pandas as pd
import numpy as np

def ml_ready_clean_mumbai_data():
    
    print("ML-READY DATA CLEANING")
    print("="*35)
    
    # Load master dataset
    df = pd.read_csv('data/processed/mumbai_vibe_master_raw.csv')
    print(f"{df.shape}")
    
    # 1. Analyze missing value patterns
    print(f"MISSING VALUE ANALYSIS:")
    
    missing_analysis = df.isnull().sum().sort_values(ascending=False)
    missing_cols = missing_analysis[missing_analysis > 0]
    
    print(f"   Total missing values: {missing_analysis.sum()}")
    print(f"   Columns with missing values: {len(missing_cols)}")

    vibe_categories = df['vibe_category'].unique()
    print(f"Missing Value Patterns by Vibe:")
    
    for vibe in vibe_categories:
        vibe_data = df[df['vibe_category'] == vibe]
        vibe_missing = vibe_data.isnull().sum().sum()
        total_cells = len(vibe_data) * len(vibe_data.columns)
        print(f"{vibe}: {vibe_missing/total_cells*100:.1f}% missing")
    
    #Identify truly irrelevant features (set to 0)
    vibe_feature_mapping = {
        'Ganesh Energy': {
            'relevant_keywords': ['ganesh', 'festival', 'religious', 'cultural', 'visarjan'],
            'irrelevant_keywords': ['heritage', 'food', 'transport', 'instagram', 'viral']
        },
        'Old School Heritage': {
            'relevant_keywords': ['heritage', 'historic', 'conservation', 'architectural', 'built_year'],
            'irrelevant_keywords': ['ganesh', 'festival', 'food', 'transport', 'instagram']
        },
        'Bombay Bhukkad': {
            'relevant_keywords': ['food', 'culinary', 'restaurant', 'meal', 'cuisine'],
            'irrelevant_keywords': ['ganesh', 'heritage', 'transport', 'instagram', 'viral']
        },
        'Chaotic Hustle': {
            'relevant_keywords': ['transport', 'traffic', 'footfall', 'chaos', 'rush'],
            'irrelevant_keywords': ['ganesh', 'heritage', 'food', 'instagram', 'viral']
        },
        'Do It For The Gram': {
            'relevant_keywords': ['instagram', 'viral', 'social', 'aesthetic', 'posts'],
            'irrelevant_keywords': ['ganesh', 'heritage', 'food', 'transport', 'chaos']
        }
    }
    for vibe_name, keywords in vibe_feature_mapping.items():
        vibe_mask = df['vibe_category'] == vibe_name
        vibe_count = vibe_mask.sum()
        
        print(f"\n   Processing {vibe_name} ({vibe_count} locations):")
        
        # Find irrelevant features for this vibe
        irrelevant_features = []
        for col in df.columns:
            if any(keyword in col.lower() for keyword in keywords['irrelevant_keywords']):
                if df[col].dtype in ['int64', 'float64']:
                    irrelevant_features.append(col)
        
        # Set irrelevant features to 0 (meaning "not applicable")
        for col in irrelevant_features:
            if col in df.columns:
                missing_count = df.loc[vibe_mask, col].isnull().sum()
                if missing_count > 0:
                    df.loc[vibe_mask, col] = df.loc[vibe_mask, col].fillna(0)
        
        print(f"      Set {len(irrelevant_features)} irrelevant features to 0")
        
        # Find relevant features for this vibe
        relevant_features = []
        for col in df.columns:
            if any(keyword in col.lower() for keyword in keywords['relevant_keywords']):
                if df[col].dtype in ['int64', 'float64']:
                    relevant_features.append(col)
        
        # Fill relevant missing features with vibe-specific median
        filled_relevant = 0
        for col in relevant_features:
            if col in df.columns:
                vibe_data = df.loc[vibe_mask, col]
                if vibe_data.isnull().any() and len(vibe_data.dropna()) > 0:
                    median_val = vibe_data.median()
                    df.loc[vibe_mask, col] = vibe_data.fillna(median_val)
                    filled_relevant += 1
        
        print(f"Filled {filled_relevant} relevant features with vibe median")
    
    # Common features that all vibes should have
    common_keywords = ['lat', 'lng', 'vibe_intensity', 'heritage_walk', 'tourism', 'congestion']
    common_features = []
    
    for col in df.columns:
        if any(keyword in col.lower() for keyword in common_keywords):
            if df[col].dtype in ['int64', 'float64']:
                common_features.append(col)
    
    # Fill common features with overall median by vibe category
    for col in common_features:
        if col in df.columns and df[col].isnull().any():
            df[col] = df.groupby('vibe_category')[col].transform(
                lambda x: x.fillna(x.median()) if len(x.dropna()) > 0 else x.fillna(0)
            )
    
    print(f"Processed {len(common_features)} common features") 
    # 4. Final missing value cleanup for ML
    # Fill any remaining missing numerical values with 0
    numerical_cols = df.select_dtypes(include=[np.number]).columns
    for col in numerical_cols:
        if df[col].isnull().any():
            df[col].fillna(0, inplace=True)
    
    # Fill categorical missing values
    categorical_cols = df.select_dtypes(include=['object']).columns
    categorical_cols = [col for col in categorical_cols if col not in ['vibe_category']]
    
    for col in categorical_cols:
        if df[col].isnull().any():
            df[col].fillna('Unknown', inplace=True)
    print(f"ML DATA VALIDATION:")
    before_dedup = len(df)
    df = df.drop_duplicates(subset=['location_id'], keep='first')
    after_dedup = len(df)
    print(f"   Duplicates removed: {before_dedup - after_dedup}")
    intensity_cols = [col for col in df.columns if 'intensity' in col.lower()]
    for col in intensity_cols:
        if col in df.columns:
            df[col] = df[col].clip(0, 5)
    distance_cols = [col for col in df.columns if 'distance' in col.lower()]
    for col in distance_cols:
        if col in df.columns and df[col].max() > 1000:
            df[col] = df[col] / 1000  # Convert to km
    print(f"ML FEATURE PREPARATION:")
    
    # Exclude metadata
    exclude_cols = [
        'location_id', 'name', 'lat', 'lng', 'vibe_category', 'vibe_source',
        'area', 'type', 'specialty', 'heritage_status', 'cuisine_type',
        'peak_dining_hours', 'peak_visiting_hours', 'peak_posting_hours'
    ]
    
    feature_cols = [col for col in df.columns if col not in exclude_cols and 
                   df[col].dtype in ['int64', 'float64', 'bool']]

    bool_cols = df[feature_cols].select_dtypes(include=['bool']).columns
    for col in bool_cols:
        df[col] = df[col].astype(int)
    
    print(f"   Total feature columns: {len(feature_cols)}")
    print(f"   Boolean columns converted: {len(bool_cols)}")
    print(f"Feature Availability by Vibe:")
    for vibe in df['vibe_category'].unique():
        vibe_data = df[df['vibe_category'] == vibe]
        non_zero_features = (vibe_data[feature_cols] != 0).sum(axis=1).mean()
        print(f"   {vibe}: avg {non_zero_features:.1f}/{len(feature_cols)} active features")
    output_path = 'data/processed/mumbai_vibe_master_ml_ready.csv'
    df.to_csv(output_path, index=False)
    
    return df, feature_cols

if __name__ == "__main__":
    clean_df, features = ml_ready_clean_mumbai_data()
    
    print(f"\nML-Ready Summary:")
    print(f"   Dataset: {clean_df.shape}")
    print(f"   Features: {len(features)}")
    print(f"   Perfect for multi-class vibe classification!")