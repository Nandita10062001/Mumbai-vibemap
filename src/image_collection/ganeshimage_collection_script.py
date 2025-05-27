
import requests
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json

class GaneshImageCollector:
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
    
    def collect_google_street_view_images(self, locations_df):
        """Collect Google Street View images for each location"""
        api_key = "YOUR_GOOGLE_STREETVIEW_API_KEY"
        base_url = "https://maps.googleapis.com/maps/api/streetview"
        
        for idx, location in locations_df.iterrows():
            params = {
                'size': '640x640',
                'location': f"{location['lat']},{location['lng']}",
                'heading': '0',
                'pitch': '0',
                'key': api_key,
                'fov': '90'
            }
            
            # Multiple angles for better coverage
            for heading in [0, 90, 180, 270]:
                params['heading'] = heading
                response = requests.get(base_url, params=params)
                
                if response.status_code == 200:
                    filename = f"images/{location['location_id']}_heading_{heading}.jpg"
                    os.makedirs("images", exist_ok=True)
                    with open(filename, 'wb') as f:
                        f.write(response.content)
                    print(f"Saved: {filename}")
                
                time.sleep(0.5)  # Rate limiting
    
    def collect_social_media_images(self, location_name, area):
        """Collect images from social media (Instagram, Twitter)"""
        # Using Instagram Basic Display API
        
        search_tags = [
            f"#{location_name.replace(' ', '').lower()}",
            f"#{area.lower()}ganpati",
            "#lalbaugcharaja" if "Lalbaug" in location_name else f"#{area.lower()}raja",
            "#ganeshchaturthi",
            "#ganpatibappamorya"
        ]
        
        print(f"Search tags for {location_name}: {search_tags}")
       
    def collect_google_images(self, search_term, num_images=10):
        """Collect images from Google Images (for reference only)"""
        search_url = f"https://www.google.com/search?q={search_term}&tbm=isch"
        
        self.driver.get(search_url)
        time.sleep(2)
  
        for i in range(3):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

        images = self.driver.find_elements(By.CSS_SELECTOR, "img[alt]")
        print(f"Found {len(images)} images for {search_term}")
        
        return [img.get_attribute('src') for img in images[:num_images]]

collector = GaneshImageCollector()
