import requests
import os
import time
import json
from urllib.parse import quote

def download_wikimedia_api():
    
    sample_locations = [
    "Lalbaugcha Raja",
    "Ganesh Galli Ka Raja",
    "GSB Seva Mandal (King of Kings)",
    "Tejukayacha Raja",
    "Khetwadi Cha Ganraj",
    "Mumbai Cha Raja (Ganesh Galli)",
    "Andheri Cha Raja",
    "Chinchpokli Cha Chintamani",
    "Girgaon Cha Raja",
    "Sarvajanik Ganeshotsav Mandal, Fort",
    "Girgaon Chowpatty",
    "Dadar Chowpatty",
    "Juhu Beach",
    "Versova Beach",
    "Mahim Beach",
    "Powai Lake",
    "Bandra Bandstand",
    "Lalbaug to Girgaon Route",
    "Ganesh Galli to Dadar Route",
    "Khetwadi to Girgaon Route",
    "Andheri to Versova Route",
    "Siddhivinayak Temple",
    "Mumbadevi Ganesh Temple",
    "Ganpati Bappa Morya Mandir, Wadala",
    "Shree Ganesh Mandir, Matunga",
    "Kumartuli (Murti Makers Hub)",
    "Chinchpokli Murti Market",
    "Pen Murti Market",
    "Sarvajanik Mandal, Byculla",
    "Sarvajanik Mandal, Worli",
    "Sarvajanik Mandal, Malad",
    "Sarvajanik Mandal, Borivali",
    "Crawford Market (Festival Items)",
    "Zaveri Bazaar (Decorations)",
    "Bhuleshwar Market",
    "Shivaji Park Ganesh Mandal",
    "Chembur Ganesh Mandal",
    "Ghatkopar Ganesh Mandal",
    "Fortcha Raja",
    "Tulsiwadi Cha Raja",
    "Kandivali Cha Raja",
    "Mulund Cha Raja",
    "Thane Cha Raja"
    ]
    
    os.makedirs("data/images/ganesh_energy", exist_ok=True)
    
    successful_downloads = 0
    failed_downloads = []
    
    print("Downloading Mumbai images using Wikimedia Commons API")
    print(f"Total locations: {len(sample_locations)}")
    print("="*60)
    
    for idx, location in enumerate(sample_locations):
        print(f"\n{idx+1}/{len(sample_locations)}: {location}")
        
        try:
            search_terms = [
                f"{location} Mumbai",
                f"{location}",
                f"Mumbai {location}"
            ]
            
            image_found = False
            
            for search_term in search_terms:
                if image_found:
                    break
                
                # Wikimedia Commons API search
                api_url = "https://commons.wikimedia.org/w/api.php"
                params = {
                    'action': 'query',
                    'format': 'json',
                    'list': 'search',
                    'srsearch': search_term,
                    'srnamespace': 6,  # File namespace
                    'srlimit': 10,
                    'srprop': 'title'
                }
                
                response = requests.get(api_url, params=params, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if 'query' in data and 'search' in data['query']:
                        search_results = data['query']['search']

                        for result in search_results:
                            filename = result['title'] 
                            if not any(ext in filename.lower() for ext in ['.jpg', '.jpeg', '.png', '.webp']):
                                continue
                            
                            print(f"Found: {filename}")

                            image_params = {
                                'action': 'query',
                                'format': 'json',
                                'titles': filename,
                                'prop': 'imageinfo',
                                'iiprop': 'url',
                                'iiurlwidth': 800  # Get 800px wide version
                            }
                            
                            img_response = requests.get(api_url, params=image_params, timeout=10)
                            
                            if img_response.status_code == 200:
                                img_data = img_response.json()
                                
                                pages = img_data.get('query', {}).get('pages', {})
                                for page_id, page_data in pages.items():
                                    imageinfo = page_data.get('imageinfo', [])
                                    
                                    if imageinfo:
                                        img_url = imageinfo[0].get('thumburl') or imageinfo[0].get('url')
                                        
                                        if img_url:
                                            try:
                                                headers = {
                                                    'User-Agent': 'Mumbai Vibe Map'
                                                }
                                                
                                                download_response = requests.get(img_url, headers=headers, timeout=20)
                                                
                                                if download_response.status_code == 200 and len(download_response.content) > 10000:
                                                    # Save the image
                                                    clean_location = location.replace(' ', '_').replace('-', '_')
                                                    filename_save = f"data/images/ganesh_energy/{idx+1:02d}_{clean_location}.jpg"
                                                    
                                                    with open(filename_save, 'wb') as f:
                                                        f.write(download_response.content)
                                                    
                                                    file_size = len(download_response.content)
                                                    
                                                    successful_downloads += 1
                                                    image_found = True
                                                    break
                                                    
                                            except Exception as e:
                                                print(f"Download failed: {e}")
                                                continue
                            
                            time.sleep(1)  # Rate limiting 
                            
                            if image_found:
                                break
                
                time.sleep(1) 
            
            if not image_found:
                print(f"No suitable images found for {location}")
                failed_downloads.append(location)
        
        except Exception as e:
            print(f"Error processing {location}: {e}")
            failed_downloads.append(location)
        time.sleep(2)
    
    # Summary
    print("\n" + "="*60)
    print("WIKIMEDIA API DOWNLOAD COMPLETE!")
    print(f"Successful: {successful_downloads}/{len(sample_locations)} images")

    
    if failed_downloads:
        print(f"\nFailed locations:")
        for location in failed_downloads:
            print(f"{location}")
    
    summary = {
        'total_locations': len(sample_locations),
        'successful_downloads': successful_downloads,
        'failed_downloads': len(failed_downloads),
        'failed_locations': failed_downloads,
        'source': 'Wikimedia Commons API',
        'license': 'Public Domain / Creative Commons',
        'method': 'Official API (not scraping)'
    }
    
    with open('data/images/ganesh_energy/wikimedia_api_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    return summary

if __name__ == "__main__":
    print("Wikimedia Commons API Downloader")
    print("Uses official API (not scraping)")
    
    results = download_wikimedia_api()
    
    print(f"\nPerfect for your interactive Mumbai vibe map!")

