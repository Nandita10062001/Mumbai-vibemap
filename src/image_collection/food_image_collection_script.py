
import requests
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json

class FoodImageCollector:
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
    
    def collect_food_street_view(self, locations_df):
        """Collect street view images for food locations"""
        api_key = "YOUR_GOOGLE_STREETVIEW_API_KEY"
        base_url = "https://maps.googleapis.com/maps/api/streetview"
        
        for idx, location in locations_df.iterrows():
            # Multiple angles for food establishments
            for heading in [0, 90, 180, 270]:
                params = {
                    'size': '640x640',
                    'location': f"{location['lat']},{location['lng']}",
                    'heading': heading,
                    'pitch': '0',
                    'key': api_key,
                    'fov': '90'
                }
                
                response = requests.get(base_url, params=params)
                
                if response.status_code == 200:
                    filename = f"food_images/{location['location_id']}_street_{heading}.jpg"
                    os.makedirs("food_images", exist_ok=True)
                    with open(filename, 'wb') as f:
                        f.write(response.content)
                    print(f"Saved food street image: {filename}")
                
                time.sleep(0.5)
    
    def collect_food_dish_images(self, location_name, specialty):
        """Collect food dish images"""
        search_terms = [
            f"{specialty} mumbai food",
            f"{location_name} mumbai restaurant",
            f"{specialty} street food mumbai",
            f"mumbai {specialty} authentic",
            f"{location_name} food photos"
        ]
        
        collected_images = []
        for term in search_terms:
            images = self.collect_google_images(term, 6)
            collected_images.extend(images)
            time.sleep(2)
        
        return collected_images
    
    def collect_instagram_food_posts(self, location_name, area):
        """Collect Instagram food posts (placeholder - requires Instagram API)"""
        hashtags = [
            f"#{location_name.replace(' ', '').lower()}",
            f"#{area.lower()}food",
            "#mumbaifood",
            "#streetfoodmumbai",
            "#bombaybhukkad",
            "#mumbaieats"
        ]
        
        print(f"Instagram hashtags for {location_name}: {hashtags}")
        #Instagram Basic Display API implementation
        
    def collect_zomato_images(self, restaurant_name):
        """Collect food images from Zomato (requires Zomato API)"""
        # Zomato API integration
        print(f"Collecting Zomato images for {restaurant_name}")
        
    def collect_google_images(self, search_term, num_images=10):
        """Collect food images from Google Images"""
        search_url = f"https://www.google.com/search?q={search_term}&tbm=isch"
        
        self.driver.get(search_url)
        time.sleep(2)
        
        for i in range(2):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
        
        images = self.driver.find_elements(By.CSS_SELECTOR, "img[alt]")
        print(f"Found {len(images)} food images for {search_term}")
        
        return [img.get_attribute('src') for img in images[:num_images]]

collector = FoodImageCollector()
