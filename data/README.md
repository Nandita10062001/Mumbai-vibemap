# 📊 Data Collection & Engineering Pipeline

> **Multi-source data collection pipeline for Mumbai vibe prediction using geospatial data, computer vision, and social media analytics.**

#### 🎯 Data Collection Strategy

##### Phase 1: Location Coordinate Mapping
- **Library Used:** `geopy` for precise coordinate extraction
- **Process:** Manually curated 227 authentic Mumbai locations across 5 vibe categories
- **Validation:** Cross-referenced with Google Maps and local knowledge for accuracy

##### Phase 2: Multi-Source Data Integration

#### 🛰️ Satellite Image Analysis

**Data Source:** Google Earth Engine and Manually Annotated High Resolution Satellite Image Dataset of Mumbai for Semantic Segmentation + Mapillary

**Processing Pipeline (Sample: 5 images per vibe only due to constraints):**
- Collected 500m x 500m satellite tiles for representative locations
- Applied **DeepLabV3+** (pre-trained) for semantic segmentation (building/vegetation/road classification)
- Used **ResNet-50** pre-trained on ImageNet for spatial feature extraction
- Applied **U-Net architecture** (pre-trained) for land use classification

**Extracted Features:**
- `urban_density`: Building footprint ratio using **semantic segmentation masks**
- `green_space_ratio`: Vegetation coverage using **NDVI-based CNN classification**
- `road_coverage`: Street network density via **Canny edge detection**
- `building_density_per_hectare`: Structure count using **YOLOv5 object detection**
- `open_space_ratio`: Non-built area percentage from **DeepLabV3+ land use segmentation**

#### 📸 Street-Level Extraction

**Data Source:** Google Street View API

**Processing Pipeline (Sample: 5 images per vibe):**
- Applied pre-trained CNN for scene understanding
- Used **YOLO** for crowd detection and **NIMA (Neural Image Assessment)** for aesthetic scoring

**Extracted Features:**
- `aesthetic_score`: Visual appeal using **NIMA pre-trained aesthetic model**
- `crowd_density_visual`: People count via **YOLOv8 person detection**
- `heritage_photography_score`: Architectural quality
- `natural_lighting_score`: Lighting analysis via **histogram equalization + brightness distribution**
- `noise_level_estimate`: Visual noise using **Laplacian variance texture analysis**

#### 📱 Social Media Image Intelligence

**Data Source:** Instagram Location APIand geotagged images

**Processing Pipeline (Sample: 5 images per vibe):**
- Collected geotagged images within 100m radius of sample locations
- Applied **CLIP (Contrastive Language-Image Pre-training)** for content understanding
- Used **hashtag frequency analysis**

**Extracted Features:**
- `instagram_tags`: Popular hashtags from **NLP hashtag extraction algorithms**
- `posts_per_day`: Social media frequency using **time-series engagement analysis**
- `viral_potential_score`: Engagement prediction using **CLIP visual-semantic similarity**
- `instagrammability_score`: Visual appeal using **Instagram-trained aesthetic CNN**

#### 🗺️ OpenStreetMap (OSM) sample queries 

##### Heritage & Cultural Density
```python
query = """
[out:json][timeout:25];
(
 way["historic"](around:500,{lat},{lng});
 way["heritage"](around:500,{lat},{lng});
 way["building"="historic"](around:500,{lat},{lng});
 way["tourism"="attraction"](around:500,{lat},{lng});
);
out count;
"""
```

##### Religious Infrastructure (Ganesh Energy)
```python
query = """
[out:json][timeout:25];
(
  way["amenity"="place_of_worship"](around:500,{lat},{lng});
  way["building"="temple"](around:500,{lat},{lng});
  way["name"~"[Gg]anesh|[Gg]anpati|[Mm]andal"](around:500,{lat},{lng});
  node["amenity"="place_of_worship"]["religion"="hindu"](around:500,{lat},{lng});
);
out count;
"""
```

#### 🏗 Data Generation Pipeline
###### Step 1: Deep Learning Sample Analysis (5 images per vibe)

- Real feature extraction using pre-trained and already previously created models
- Computer vision pipeline for spatial, aesthetic, and semantic features
- API-based social media analytics for engagement and trend metrics

Due to limited constraints like no billing account, free-tier credits expiration and rate limits I trained it on 5 images per vibe for each of the above sources and with the help of extracted features, generated rule-based features for the rest of the 200 locations!

###### Step 2: Automated Rule-Based Scaling (Remaining 202 locations)

- Statistical pattern modeling based on deep learning sample correlations
- Geospatial interpolation using sample feature distributions
- Mumbai-specific rule synthesis for cultural and temporal patterns

###### Step 3: Contextual Feature Engineering

- 247 contextual features through feature_engineering.py
- Multi-source intelligence fusion (heritage walks + hashtags + congestion)
- Vibe-specific authenticity scoring using cultural domain knowledge

I created a quiet comprehensive list of features, that would scale for other cities like Delhi and Bangalore as well. My main aim was ot research and study every aspect of Mumbai to get all possible estimates. For a dataset as huge as 2000+, this would be the ideal set of features. 
Since I currently trained only on 227 datapoints, I performed further feature selection during ML Modeling and selected top ones to maintain the **10:1** ratio.


#### 🎯 Final Dataset Specifications

227 locations across 5 authentic Mumbai vibe categories
247 engineered features from CV, OSM, social media, and contextual sources
Multi-modal approach: 25 locations with deep learning features + 202 with rule-based scaling
Production-ready pipeline with comprehensive preprocessing and model validation
