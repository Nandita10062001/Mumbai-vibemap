
import requests
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json

class UrbanEnergyImageCollector:
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
    
    def collect_urban_street_view(self, locations_df):
        """Collect street view images for urban energy locations"""
        api_key = "YOUR_GOOGLE_STREETVIEW_API_KEY"
        base_url = "https://maps.googleapis.com/maps/api/streetview"
        
        for idx, location in locations_df.iterrows():
            for heading in [0, 90, 180, 270]:
                params = {
                    'size': '640x640',
                    'location': f"{location['lat']},{location['lng']}",
                    'heading': heading,
                    'pitch': '10', 
                    'key': api_key,
                    'fov': '90'
                }
                
                response = requests.get(base_url, params=params)
                
                if response.status_code == 200:
                    filename = f"urban_energy_images/{location['location_id']}_angle_{heading}.jpg"
                    os.makedirs("urban_energy_images", exist_ok=True)
                    with open(filename, 'wb') as f:
                        f.write(response.content)
                    print(f"Saved urban energy image: {filename}")
                
                time.sleep(0.5)
    
    def collect_crowd_flow_images(self, location_name, location_type):
        """Collect images showing crowd flow and urban energy"""
        search_terms = [
            f"{location_name} mumbai rush hour",
            f"{location_name} crowd mumbai",
            f"{location_type} mumbai traffic",
            f"mumbai {location_type} busy",
            f"{location_name} peak hours mumbai"
        ]
        
        collected_images = []
        for term in search_terms:
            images = self.collect_google_images(term, 5)
            collected_images.extend(images)
            time.sleep(2)
        
        return collected_images
    
    def collect_infrastructure_images(self, location_type):
        """Collect infrastructure images by type"""
        if "Station" in location_type:
            search_terms = [
                "mumbai railway station platform",
                "mumbai train station crowd",
                "mumbai local train rush"
            ]
        elif "Junction" in location_type:
            search_terms = [
                "mumbai traffic junction",
                "mumbai road intersection busy",
                "mumbai traffic signal"
            ]
        elif "Business District" in location_type:
            search_terms = [
                "mumbai business district skyline",
                "mumbai office buildings",
                "mumbai corporate area"
            ]
        else:
            search_terms = [f"mumbai {location_type}"]
        
        collected_images = []
        for term in search_terms:
            images = self.collect_google_images(term, 4)
            collected_images.extend(images)
            time.sleep(2)
        
        return collected_images
    
    def collect_time_lapse_references(self, location_name):
        """Collect time-lapse reference images"""
        search_terms = [
            f"{location_name} mumbai timelapse",
            f"{location_name} day to night mumbai",
            f"{location_name} mumbai 24 hours"
        ]
        
        collected_images = []
        for term in search_terms:
            images = self.collect_google_images(term, 3)
            collected_images.extend(images)
            time.sleep(2)
        
        return collected_images
    
    def collect_google_images(self, search_term, num_images=10):
        """Collect urban energy images from Google Images"""
        search_url = f"https://www.google.com/search?q={search_term}&tbm=isch"
        
        self.driver.get(search_url)
        time.sleep(2)
        
        for i in range(2):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
        
        images = self.driver.find_elements(By.CSS_SELECTOR, "img[alt]")
        print(f"Found {len(images)} urban energy images for {search_term}")
        
        return [img.get_attribute('src') for img in images[:num_images]]

collector = UrbanEnergyImageCollector()
