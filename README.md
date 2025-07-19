**MyAnimeList Complete Database Scraper**

Python script that automatically scrapes the entire MyAnimeList top anime ranking database via the Jikan API, collecting 29,000+ anime entries with comprehensive details including rankings, scores, genres, studios, and metadata. Outputs both CSV and JSON formats for easy data analysis and visualization.

**Features**

- **Complete Dataset:** Scrapes all anime from MyAnimeList's top ranking (1,000+ pages)
- **Comprehensive Data:** Extracts 20+ fields per anime including rank, score, genres, studios, episodes, etc.
- **Multiple Formats:** Outputs both CSV and JSON files
- **Rate Limiting:** Built-in delays to respect API guidelines
- **Progress Tracking:** Real-time updates showing scraping progress
- **Error Handling:** Robust error handling for network issues

**Data Fields Extracted**

- **Basic Info:** mal_id, title, title_english, title_japanese
- **Rankings:** rank, score, scored_by, popularity, members, favorites
- **Details:** type, episodes, status, duration, rating
- **Dates:** aired_from, aired_to
- **Categories:** genres, themes, demographics, studios
- **Additional:** synopsis, url, image_url
