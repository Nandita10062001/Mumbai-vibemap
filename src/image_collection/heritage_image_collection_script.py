
import requests
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json

class HeritageImageCollector:
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
    
    def collect_google_street_view_heritage(self, locations_df):
        """Collect Google Street View images for heritage locations"""
        api_key = "YOUR_GOOGLE_STREETVIEW_API_KEY"
        base_url = "https://maps.googleapis.com/maps/api/streetview"
        
        for idx, location in locations_df.iterrows():
            # Multiple angles for architectural documentation
            for heading in [0, 45, 90, 135, 180, 225, 270, 315]:
                params = {
                    'size': '640x640',
                    'location': f"{location['lat']},{location['lng']}",
                    'heading': heading,
                    'pitch': '10',  # Slight upward angle for buildings
                    'key': api_key,
                    'fov': '75'  # Narrower field of view for architectural details
                }
                
                response = requests.get(base_url, params=params)
                
                if response.status_code == 200:
                    filename = f"heritage_images/{location['location_id']}_angle_{heading}.jpg"
                    os.makedirs("heritage_images", exist_ok=True)
                    with open(filename, 'wb') as f:
                        f.write(response.content)
                    print(f"Saved heritage image: {filename}")
                
                time.sleep(0.5)  # Rate limiting
    
    def collect_architectural_details(self, location_name, built_year):
        """Collect detailed architectural images"""
        search_terms = [
            f"{location_name} architecture details mumbai",
            f"{location_name} facade mumbai heritage",
            f"{location_name} colonial architecture mumbai",
            f"{location_name} art deco mumbai" if built_year > 1920 else f"{location_name} colonial mumbai",
            f"{location_name} historical photos mumbai"
        ]
        
        collected_images = []
        for term in search_terms:
            images = self.collect_google_images(term, 5)
            collected_images.extend(images)
            time.sleep(2) 
        
        return collected_images
    
    def collect_heritage_documentation(self, heritage_status, location_type):
        """Collect heritage documentation images"""
        if heritage_status == "UNESCO World Heritage":
            search_term = f"mumbai unesco world heritage {location_type}"
        elif "Grade I" in heritage_status:
            search_term = f"mumbai grade 1 heritage {location_type}"
        else:
            search_term = f"mumbai heritage {location_type}"
        
        return self.collect_google_images(search_term, 8)
    
    def collect_google_images(self, search_term, num_images=10):
        """Collect images from Google Images for heritage documentation"""
        search_url = f"https://www.google.com/search?q={search_term}&tbm=isch&tbs=sur:fmc"  # Commercial use filter
        
        self.driver.get(search_url)
        time.sleep(2)
        

        for i in range(3):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
        
        images = self.driver.find_elements(By.CSS_SELECTOR, "img[alt]")
        print(f"Found {len(images)} heritage images for {search_term}")
        
        return [img.get_attribute('src') for img in images[:num_images]]

collector = HeritageImageCollector()
