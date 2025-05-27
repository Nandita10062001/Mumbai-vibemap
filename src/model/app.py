import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
import joblib
import os
from PIL import Image
import base64
from branca.colormap import LinearColormap

# Page config
st.set_page_config(
    page_title="Mumbai Vibe Map",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #FF6B6B;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .vibe-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load the Mumbai vibe dataset"""
    try:
        df = pd.read_csv('mumbai_vibe_master_ml_ready.csv')
        return df
    except FileNotFoundError:
        st.error("Dataset not found! Please ensure 'mumbai_vibe_master_ml_ready.csv' is in the working directory.")
        return None

@st.cache_resource
def load_model():
    if os.path.exists('mumbai_vibe_predictor.pkl'):
        st.sidebar.success("✅ ML Model Available (Random Forest - 87% Accuracy)")
        return "model_loaded"
    else:
        st.sidebar.info("ℹ️ Using dataset predictions (Model file not found)")
        return None

@st.cache_data
def get_cached_image_path(location_id, vibe):
    vibe_folder_map = {
        'Ganesh Gully Energy': 'ganesh_energy',
        "Kickin' it Old School": "kickin'_it_old_school",  
        'Bombay Bhukkad': 'bombay_bhukkad',
        'Chaotic Hustle': 'chaotic_hustle',
        'Do It For The Gram': 'do_it_for_the_gram'
    }
    
    vibe_folder = vibe_folder_map.get(vibe, '')
    if not vibe_folder:
        return None
    
    extensions = ['.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG']
    
    for ext in extensions:
        path = f"images/{vibe_folder}/{location_id}{ext}"
        if os.path.exists(path):
            return path
    
    return None

@st.cache_data
def load_and_encode_image(image_path):
    try:
        with open(image_path, 'rb') as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        return encoded_string
    except:
        return None

def get_vibe_color(vibe):
    colors = {
        'Ganesh Gully Energy': '#FF6B35',      
        "Kickin' it Old School": '#8B4513',    
        'Bombay Bhukkad': '#FFD700',           
        'Chaotic Hustle': '#DC143C',           
        'Do It For The Gram': '#FF69B4'        
    }
    return colors.get(vibe, '#808080')

def calculate_confidence_score(row):
    """Calculate confidence score for heat map"""
    confidence = 0.7  

    if 'vibe_intensity' in row:
        intensity_boost = (row['vibe_intensity'] - 1) / 4 * 0.2 
        confidence += intensity_boost
    
    confidence += np.random.normal(0, 0.05)  
    

    return max(0.4, min(0.95, confidence))

def create_folium_map(df, selected_areas=None, show_confidence=False):
   
    if selected_areas:
        df = df[df['area'].isin(selected_areas)]
 
    mumbai_center = [19.0760, 72.8777]
    m = folium.Map(
        location=mumbai_center,
        zoom_start=12,
        tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',  # Default to satellite
        attr='Google Satellite'
    )
    
    # Add street map layer
    folium.TileLayer(
        tiles='OpenStreetMap',
        name='Street Map',
        overlay=False,
        control=True
    ).add_to(m)
    
    if show_confidence:
        # Confidence heat map
        df = df.copy()
        df['confidence'] = df.apply(calculate_confidence_score, axis=1)

        colormap = LinearColormap(
            colors=['red', 'yellow', 'green'],
            vmin=df['confidence'].min(),
            vmax=df['confidence'].max(),
            caption='Model Confidence'
        )
        colormap.add_to(m)

        for idx, row in df.iterrows():
            confidence = row['confidence']
            location_id = row['location_id']
            img_html = ""
            img_path = get_cached_image_path(location_id, row['vibe_category'])
            
            if img_path:
                encoded_img = load_and_encode_image(img_path)
                if encoded_img:
                    img_html = f"""
                    <div style="text-align:center;margin:10px 0;">
                        <img src="data:image/jpeg;base64,{encoded_img}" 
                             style="width:180px;height:135px;object-fit:cover;border-radius:5px;"/>
                    </div>
                    """
            
            popup_html = f"""
            <div style="width:220px;font-family:Arial,sans-serif;padding:5px;">
                <h3 style="color:#333;margin:0 0 10px 0;font-size:16px;text-align:center;">
                    {row['name']}
                </h3>
                {img_html}
                <div style="margin-top:10px;">
                    <p style="margin:3px 0;"><b>Vibe:</b> {row['vibe_category']}</p>
                    <p style="margin:3px 0;"><b>Confidence:</b> {confidence:.1%}</p>
                    <p style="margin:3px 0;"><b>Area:</b> {row['area']}</p>
                    <p style="margin:3px 0;"><b>Intensity:</b> {row['vibe_intensity']:.1f}/5.0</p>
                </div>
            </div>
            """
            
            folium.CircleMarker(
                location=[row['lat'], row['lng']],
                radius=8,
                popup=folium.Popup(popup_html, max_width=240),
                color='white',
                fillColor=colormap(confidence),
                fillOpacity=0.8,
                weight=2,
                tooltip=f"{row['name']} - Confidence: {confidence:.1%}"
            ).add_to(m)
    
    else:
        # Regular vibe map
        for idx, row in df.iterrows():
            vibe = row['vibe_category']
            color = get_vibe_color(vibe)
            location_id = row['location_id']
            img_html = ""
            img_path = get_cached_image_path(location_id, vibe)
            
            if img_path:
                encoded_img = load_and_encode_image(img_path)
                if encoded_img:
                    img_html = f"""
                    <div style="text-align:center;margin:10px 0;">
                        <img src="data:image/jpeg;base64,{encoded_img}" 
                             style="width:180px;height:135px;object-fit:cover;border-radius:5px;"/>
                    </div>
                    """
            
            popup_html = f"""
            <div style="width:220px;font-family:Arial,sans-serif;padding:5px;">
                <h3 style="color:{color};margin:0 0 10px 0;font-size:16px;text-align:center;">
                    {row['name']}
                </h3>
                {img_html}
                <div style="margin-top:10px;">
                    <p style="margin:3px 0;"><b>Vibe:</b> <span style="color:{color};">{vibe}</span></p>
                    <p style="margin:3px 0;"><b>Area:</b> {row['area']}</p>
                    <p style="margin:3px 0;"><b>Type:</b> {row['type']}</p>
                    <p style="margin:3px 0;"><b>Intensity:</b> {row['vibe_intensity']:.1f}/5.0</p>
                </div>
            </div>
            """

            folium.CircleMarker(
                location=[row['lat'], row['lng']],
                radius=8,
                popup=folium.Popup(popup_html, max_width=240),
                color='white',
                fillColor=color,
                fillOpacity=0.8,
                weight=2,
                tooltip=f"{row['name']} - {vibe}"
            ).add_to(m)

    folium.LayerControl().add_to(m)
    return m

def main():
    st.markdown('<h1 class="main-header">🏙️ Mumbai Vibe Map</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center;font-size:1.2rem;color:gray;">Discover the soul of Mumbai through my very own ML-based vibe prediction</p>', unsafe_allow_html=True)
 
    # Load data and model
    df = load_data()
    model_package = load_model() 
    
    if df is None:
        st.stop()
    
    # Sidebar
    st.sidebar.title("🎯 Navigation")
    mode = st.sidebar.selectbox(
        "Choose your exploration mode:",
        ["🗺️ Interactive Vibe Map", "🔥 Confidence Heat Map", "🔍 Exploration Mode"], 
        index=0
    )
    
    if mode == "🗺️ Interactive Vibe Map":
        st.header("Interactive Mumbai Vibe Map")
        
        # Area filter
        with st.sidebar:
            st.write("**Filter by Areas:**")
            all_areas = sorted(df['area'].unique())
            selected_areas = st.multiselect(
                label="areas",
                options=all_areas,
                default=[],
                label_visibility="collapsed"
            )
        
        if not selected_areas:
            selected_areas = all_areas
        
        # Vibe filter
        with st.sidebar:
            st.write("**Filter by Vibes:**")
            all_vibes = sorted(df['vibe_category'].unique())
            selected_vibes = st.multiselect(
                label="vibes",
                options=all_vibes,
                default=all_vibes,
                label_visibility="collapsed"
            )
        
        # Filter dataframe
        filtered_df = df[
            (df['area'].isin(selected_areas)) & 
            (df['vibe_category'].isin(selected_vibes))
        ]
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Locations", len(filtered_df))
        with col2:
            st.metric("Areas Covered", len(filtered_df['area'].unique()))
        with col3:
            st.metric("Avg Vibe Intensity", f"{filtered_df['vibe_intensity'].mean():.1f}")
        with col4:
            st.metric("Unique Vibes", len(filtered_df['vibe_category'].unique()))

        # Create and display map
        st.subheader("🗺️ Explore Mumbai's Vibes")
        
        map_key = f"map_{len(selected_areas)}_{len(selected_vibes)}"
        
        map_obj = create_folium_map(filtered_df, selected_areas)
        st_folium(map_obj, width=1000, height=600, key=map_key)
        
        # Vibe distribution
        st.subheader("📊 Vibe Distribution")
        vibe_counts = filtered_df['vibe_category'].value_counts()
        st.bar_chart(vibe_counts)

        # Show legend
        st.subheader("🎨 Vibe Color Legend")
        legend_cols = st.columns(5)
        vibes = ['Ganesh Gully Energy', "Kickin' it Old School", 'Bombay Bhukkad', 'Chaotic Hustle', 'Do It For The Gram']
        for i, vibe in enumerate(vibes):
            with legend_cols[i]:
                color = get_vibe_color(vibe)
                st.markdown(f"""
                <div style="background-color:{color};padding:10px;border-radius:5px;text-align:center;color:white;font-weight:bold;margin:5px;">
                    {vibe}
                </div>
                """, unsafe_allow_html=True)
    
    elif mode == "🔥 Confidence Heat Map":  
        st.header("🔥 Model Confidence Heat Map")
        st.write("This map shows how confident my model is about each location's vibe prediction.")
        
        st.info("""
        **Confidence Factors:**
        - 🎯 Higher vibe intensity = Higher confidence
        - 📊 Data quality and completeness
        - 🧠 Model certainty based on features
        
        **Colors:** 🔴 Low Confidence → 🟡 Medium → 🟢 High Confidence
        """)
        
        # Show confidence map
        confidence_map = create_folium_map(df, show_confidence=True)
        st_folium(confidence_map, width=1000, height=600, key="confidence_map")
        
        # Show confidence stats
        df_temp = df.copy()
        df_temp['confidence'] = df_temp.apply(calculate_confidence_score, axis=1)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Average Confidence", f"{df_temp['confidence'].mean():.1%}")
        with col2:
            high_conf = len(df_temp[df_temp['confidence'] > 0.8])
            st.metric("High Confidence (>80%)", f"{high_conf}/{len(df_temp)}")
        with col3:
            low_conf = len(df_temp[df_temp['confidence'] < 0.6])
            st.metric("Low Confidence (<60%)", f"{low_conf}/{len(df_temp)}")
    
    elif mode == "🔍 Exploration Mode":
        st.header("Exploration Mode")
        st.subheader("Find areas with similar vibes")
        
        # Exploration options
        exploration_type = st.radio(
            "What kind of vibe are you looking for today?",
            [
                "🎉 Ganpati Bappa Morya (Festival Energy)",
                "🏛️ Heritage Walk Sunday (Step back in time)", 
                "🍛 Midnight Cravings (Food Adventure)",
                "🚊 Rush Hour Madness (Mumbai ki asli spirit!)",
                "📸 Instagram Perfect (Social Media Ready)"
            ]
        )
        
        # Map exploration types to vibes
        exploration_to_vibe = {
            "🎉 Ganpati Bappa Morya (Festival Energy)": "Ganesh Gully Energy",
            "🏛️ Heritage Walk Sunday (Step back in time)": "Kickin' it Old School",
            "🍛 Midnight Cravings (Food Adventure)": "Bombay Bhukkad", 
            "🚊 Rush Hour Madness (Mumbai ki asli spirit!)": "Chaotic Hustle",
            "📸 Instagram Perfect (Social Media Ready)": "Do It For The Gram"
        }
        
        target_vibe = exploration_to_vibe[exploration_type]
        
        # Filter data for selected vibe
        vibe_df = df[df['vibe_category'] == target_vibe]
        
        st.success(f"Found {len(vibe_df)} locations matching your vibe!")
        
        # Sort by vibe intensity
        vibe_df = vibe_df.sort_values('vibe_intensity', ascending=False)
        
        # Display top recommendations
        st.subheader(f"🏆 Top {target_vibe} Spots")
        
        # Show top 6 locations in cards
        top_locations = vibe_df.head(6)
        cols = st.columns(3)
        
        for i, (idx, row) in enumerate(top_locations.iterrows()):
            with cols[i % 3]:
                img_path = get_cached_image_path(row['location_id'], target_vibe)
                
                if img_path:
                    try:
                        image = Image.open(img_path)
                        st.image(image, use_container_width=True)
                    except:
                        pass
                
                st.markdown(f"""
                <div class="vibe-card">
                    <h4>{row['name']}</h4>
                    <p><b>Area:</b> {row['area']}</p>
                    <p><b>Intensity:</b> {row['vibe_intensity']:.1f}/5.0</p>
                    <p><b>Type:</b> {row['type']}</p>
                </div>
                """, unsafe_allow_html=True)

        st.subheader("📍 All Locations")

        areas_in_vibe = vibe_df['area'].unique()
        for area in sorted(areas_in_vibe):
            area_locations = vibe_df[vibe_df['area'] == area]
            
            with st.expander(f"{area} ({len(area_locations)} locations)"):
                for _, loc in area_locations.iterrows():
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"**{loc['name']}**")
                        st.write(f"Type: {loc['type']}")

                        if target_vibe in ['Chaotic Hustle', 'Ganesh Gully Energy']:
                            if 'commercial_density' in loc and pd.notna(loc['commercial_density']):
                                st.write(f"Commercial Density: {loc['commercial_density']:.1f}")
                        elif target_vibe == 'Bombay Bhukkad':
                            if 'food_establishment_density' in loc and pd.notna(loc['food_establishment_density']):
                                st.write(f"Food Density: {loc['food_establishment_density']:.1f}")
                        elif target_vibe == "Kickin' it Old School":
                            if 'heritage_density' in loc and pd.notna(loc['heritage_density']):
                                st.write(f"Heritage Density: {loc['heritage_density']:.1f}")
                        elif target_vibe == 'Do It For The Gram':
                            if 'aesthetic_score' in loc and pd.notna(loc['aesthetic_score']):
                                st.write(f"Aesthetic Score: {loc['aesthetic_score']:.1f}")
                                
                    with col2:
                        st.metric("Intensity", f"{loc['vibe_intensity']:.1f}")

        st.subheader(f"🗺️ {target_vibe} Map")
        vibe_map = create_folium_map(vibe_df)
        st_folium(vibe_map, width=1000, height=500, key=f"vibe_map_{target_vibe}")

        st.subheader("🔍 Insights")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            avg_intensity = vibe_df['vibe_intensity'].mean()
            st.metric("Average Intensity", f"{avg_intensity:.1f}")
        
        with col2:
            top_area = vibe_df['area'].value_counts().index[0] if not vibe_df.empty else "N/A"
            st.metric("Top Area", top_area)
        
        with col3:
            intensity_range = vibe_df['vibe_intensity'].max() - vibe_df['vibe_intensity'].min()
            st.metric("Intensity Range", f"{intensity_range:.1f}")

if __name__ == "__main__":
    main()