import requests
import json
import csv
import time
from datetime import datetime

# Configuration
BASE_URL = 'https://api.jikan.moe/v4/top/anime'
DELAY_SECONDS = 1  # Rate limiting - 1 request per second
OUTPUT_JSON = 'top_anime_list.json'
OUTPUT_CSV = 'top_anime_list.csv'

def fetch_anime_data(page=1):
    """Fetch anime data from a specific page"""
    try:
        url = f"{BASE_URL}?page={page}"
        print(f"Fetching page {page}...")
        
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching page {page}: {e}")
        return None

def process_anime_data(anime_data):
    """Process and clean anime data"""
    return {
        'mal_id': anime_data.get('mal_id', 'N/A'),
        'title': anime_data.get('title', 'N/A'),
        'title_english': anime_data.get('title_english') or anime_data.get('title', 'N/A'),
        'title_japanese': anime_data.get('title_japanese', 'N/A'),
        'rank': anime_data.get('rank', 'N/A'),
        'score': anime_data.get('score', 'N/A'),
        'scored_by': anime_data.get('scored_by', 'N/A'),
        'popularity': anime_data.get('popularity', 'N/A'),
        'members': anime_data.get('members', 'N/A'),
        'favorites': anime_data.get('favorites', 'N/A'),
        'type': anime_data.get('type', 'N/A'),
        'episodes': anime_data.get('episodes', 'N/A'),
        'status': anime_data.get('status', 'N/A'),
        'aired_from': anime_data.get('aired', {}).get('from', 'N/A')[:10] if anime_data.get('aired', {}).get('from') else 'N/A',
        'aired_to': anime_data.get('aired', {}).get('to', 'N/A')[:10] if anime_data.get('aired', {}).get('to') else 'N/A',
        'duration': anime_data.get('duration', 'N/A'),
        'rating': anime_data.get('rating', 'N/A'),
        'studios': ', '.join([studio['name'] for studio in anime_data.get('studios', [])]) or 'N/A',
        'genres': ', '.join([genre['name'] for genre in anime_data.get('genres', [])]) or 'N/A',
        'themes': ', '.join([theme['name'] for theme in anime_data.get('themes', [])]) or 'N/A',
        'demographics': ', '.join([demo['name'] for demo in anime_data.get('demographics', [])]) or 'N/A',
        'synopsis': anime_data.get('synopsis', 'N/A').replace('\n', ' ').replace(',', ';') if anime_data.get('synopsis') else 'N/A',
        'url': anime_data.get('url', 'N/A'),
        'image_url': anime_data.get('images', {}).get('jpg', {}).get('large_image_url') or 
                    anime_data.get('images', {}).get('jpg', {}).get('image_url', 'N/A')
    }

def save_to_json(anime_list, filename):
    """Save anime list to JSON file"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(anime_list, f, indent=2, ensure_ascii=False)
        print(f"Successfully saved {len(anime_list)} anime entries to {filename}")
    except Exception as e:
        print(f"Error saving JSON file: {e}")

def save_to_csv(anime_list, filename):
    """Save anime list to CSV file"""
    try:
        if not anime_list:
            return
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=anime_list[0].keys())
            writer.writeheader()
            writer.writerows(anime_list)
        print(f"Successfully saved {len(anime_list)} anime entries to {filename}")
    except Exception as e:
        print(f"Error saving CSV file: {e}")

def scrape_top_anime():
    """Main function to scrape all anime data"""
    print('Starting to scrape top anime data from MyAnimeList via Jikan API...')
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    all_anime = []
    current_page = 1
    has_more_pages = True
    
    while has_more_pages:
        data = fetch_anime_data(current_page)
        
        if not data or 'data' not in data or not data['data']:
            print('No more data available or reached the end.')
            has_more_pages = False
            break
        
        # Process the anime data from current page
        processed_anime = [process_anime_data(anime) for anime in data['data']]
        all_anime.extend(processed_anime)
        
        print(f"Page {current_page} completed. Total anime collected: {len(all_anime)}")
        
        # Check if there are more pages
        pagination = data.get('pagination', {})
        if not pagination.get('has_next_page', False):
            has_more_pages = False
            print('Reached the last page.')
        else:
            current_page += 1
            # Add delay to respect rate limits
            time.sleep(DELAY_SECONDS)
    
    # Save data to files
    save_to_json(all_anime, OUTPUT_JSON)
    save_to_csv(all_anime, OUTPUT_CSV)
    
    print(f"\nScraping completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total anime collected: {len(all_anime)}")
    
    # Display sample data
    if all_anime:
        print('\nSample data (first 3 entries):')
        for i, anime in enumerate(all_anime[:3], 1):
            print(f"\n{i}. {anime['title']} (Rank: {anime['rank']})")
            print(f"   Score: {anime['score']}, Type: {anime['type']}, Episodes: {anime['episodes']}")
    
    return all_anime

if __name__ == "__main__":
    try:
        scrape_top_anime()
    except KeyboardInterrupt:
        print("\nScript interrupted by user.")
    except Exception as e:
        print(f"Script failed: {e}")