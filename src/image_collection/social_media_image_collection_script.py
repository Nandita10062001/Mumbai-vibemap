
import requests
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json

class SocialMediaImageCollector:
    def __init__(self):
        self.driver = None
        self.setup_driver()
        
    def setup_driver(self):
        """Setup Chrome driver for web scraping"""
        from selenium.webdriver.chrome.options import Options
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=chrome_options)
    
    def collect_instagram_style_images(self, locations_df):
        """Collect Instagram-style images for social media locations"""
        api_key = "YOUR_GOOGLE_STREETVIEW_API_KEY"
        base_url = "https://maps.googleapis.com/maps/api/streetview"
        
        for idx, location in locations_df.iterrows():
            # Multiple times of day for different moods
            times = ['morning', 'afternoon', 'golden_hour', 'night']
            
            for time_period in times:
                # Adjust parameters based on time
                if time_period == 'golden_hour':
                    pitch = -10  # Slightly downward for sunset
                    fov = 75    # Narrower for dramatic effect
                elif time_period == 'night':
                    pitch = 5
                    fov = 90
                else:
                    pitch = 0
                    fov = 85
                
                params = {
                    'size': '640x640',
                    'location': f"{location['lat']},{location['lng']}",
                    'heading': '0',  
                    'pitch': pitch,
                    'key': api_key,
                    'fov': fov
                }
                
                response = requests.get(base_url, params=params)
                
                if response.status_code == 200:
                    filename = f"social_media_images/{location['location_id']}_{time_period}.jpg"
                    os.makedirs("social_media_images", exist_ok=True)
                    with open(filename, 'wb') as f:
                        f.write(response.content)
                    print(f"Saved social media image: {filename}")
                
                time.sleep(0.5)
    
    def collect_trending_content_images(self, location_name, location_type):
        """Collect trending content style images"""
        search_terms = [
            f"{location_name} instagram mumbai",
            f"{location_name} photography mumbai",
            f"{location_type} aesthetic mumbai",
            f"{location_name} influencer photos",
            f"mumbai {location_type} viral"
        ]
        
        collected_images = []
        for term in search_terms:
            images = self.collect_google_images(term, 4)
            collected_images.extend(images)
            time.sleep(2)
        
        return collected_images
    
    def collect_aesthetic_references(self, aesthetic_score, location_type):
        """Collect aesthetic reference images by style"""
        if aesthetic_score > 8.5:
            aesthetic_terms = [
                f"mumbai {location_type} aesthetic",
                f"mumbai {location_type} pinterest",
                f"mumbai instagram spots"
            ]
        else:
            aesthetic_terms = [
                f"mumbai {location_type} photography",
                f"mumbai {location_type} travel"
            ]
        
        collected_images = []
        for term in aesthetic_terms:
            images = self.collect_google_images(term, 5)
            collected_images.extend(images)
            time.sleep(2)
        
        return collected_images
    
    def collect_influencer_content_samples(self, location_name, instagram_tags):
        """Collect influencer content style samples"""
        # Higher Instagram tags = more influencer content
        if instagram_tags > 200000:
            search_terms = [
                f"{location_name} mumbai influencer",
                f"{location_name} blog mumbai",
                f"{location_name} photo shoot mumbai"
            ]
        else:
            search_terms = [
                f"{location_name} mumbai travel",
                f"{location_name} visit mumbai"
            ]
        
        collected_images = []
        for term in search_terms:
            images = self.collect_google_images(term, 3)
            collected_images.extend(images)
            time.sleep(2)
        
        return collected_images
    
    def collect_seasonal_content(self, location_name, location_type):
        """Collect seasonal content variations"""
        seasons = ['monsoon', 'winter', 'summer']
        
        collected_by_season = {}
        for season in seasons:
            search_term = f"{location_name} {season} mumbai"
            images = self.collect_google_images(search_term, 3)
            collected_by_season[season] = images
            time.sleep(2)
        
        return collected_by_season
    
    def collect_google_images(self, search_term, num_images=10):
        """Collect social media style images from Google Images"""
        search_url = f"https://www.google.com/search?q={search_term}&tbm=isch&tbs=itp:photo"
        
        self.driver.get(search_url)
        time.sleep(2)
        
        for i in range(2):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
        
        images = self.driver.find_elements(By.CSS_SELECTOR, "img[alt]")
        print(f"Found {len(images)} social media images for {search_term}")
        
        return [img.get_attribute('src') for img in images[:num_images]]

collector = SocialMediaImageCollector()
