import pandas as pd
import os

def combine_mumbai_datasets():  
    print("Combining Mumbai Vibe Datasets")
    print("="*50)
    
    dataset_files = {
        'Ganesh Energy': 'data/processed/ganesh_energy_dataset_enhanced.csv',
        'Old School Heritage': 'data/processed/old_school_heritage_dataset_enhanced.csv', 
        'Bombay Bhukkad': 'data/processed/bombay_bhukkad_dataset_enhanced.csv',
        'Chaotic Hustle': 'data/processed/chaotic_hustle_dataset_enhanced.csv',
        'Do It For The Gram': 'data/processed/do_it_for_the_gram_dataset_enhanced.csv'
    }
    
    combined_dfs = []

    for vibe_name, file_path in dataset_files.items():
        try:
            print(f"Loading {vibe_name}...")
            df = pd.read_csv(file_path)
            df['vibe_category'] = vibe_name
            df['vibe_source'] = vibe_name.lower().replace(' ', '_')
            
            combined_dfs.append(df)
            print(f"{len(df)} locations, {len(df.columns)} features")
            
        except Exception as e:
            print(f"Failed to load {vibe_name}: {e}")
    print(f"Combining all datasets...")
    master_df = pd.concat(combined_dfs, ignore_index=True, sort=False)
    
    # Summary
    print(f"MASTER DATASET CREATED:")
    print(f"Total locations: {len(master_df)}")
    print(f"Total columns: {len(master_df.columns)}")
    print(f"Vibe categories: {master_df['vibe_category'].nunique()}")
    
    print(f"\nVibe Distribution:")
    vibe_counts = master_df['vibe_category'].value_counts()
    for vibe, count in vibe_counts.items():
        print(f"{vibe}: {count} locations")
    output_path = 'data/processed/mumbai_vibe_master_raw.csv'
    master_df.to_csv(output_path, index=False)
    print(f"Master dataset saved: {output_path}")

    print(f"Run data cleaning and preprocessing")
    
    return master_df

if __name__ == "__main__":
    master_dataset = combine_mumbai_datasets()
    
    print(f"Summary:")
    print(f"Shape: {master_dataset.shape}")
    print(f"Memory: {master_dataset.memory_usage(deep=True).sum() / 1024**2:.1f} MB")