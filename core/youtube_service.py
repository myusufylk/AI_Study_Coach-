import os
import requests
import logging
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
load_dotenv()

def get_youtube_videos(query, max_results=3):
    """
    YouTube Data API v3 kullanarak verilen query (Ders + Konu) için en popüler videoları getirir.
    Eğer API anahtarı yoksa veya hata oluşursa boş liste döner.
    """
    api_key = os.getenv('YOUTUBE_API_KEY')
    if not api_key:
        logger.warning("YOUTUBE_API_KEY bulunamadı. Lütfen .env dosyasına ekleyin.")
        return []

    # API uç noktası ve parametreleri
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        'part': 'snippet',
        'q': f"{query} konu anlatımı -shorts", # Shorts'ları elemek için -shorts ekledik
        'type': 'video',
        'videoDuration': 'any', # Tüm süreleri kabul et (uzun videolar dahil)
        'maxResults': max_results,
        'key': api_key,
        'relevanceLanguage': 'tr',
        'order': 'relevance'
    }

    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        videos = []
        for item in data.get('items', []):
            snippet = item.get('snippet', {})
            title = snippet.get('title', '')
            video_id = item.get('id', {}).get('videoId')
            
            # Başlıkta #shorts veya parodi geçiyorsa atla
            if video_id and "#shorts" not in title.lower() and "parodi" not in title.lower():
                videos.append({
                    'video_id': video_id,
                    'title': title,
                    'channel_title': snippet.get('channelTitle'),
                    'thumbnail_url': snippet.get('thumbnails', {}).get('medium', {}).get('url'),
                    'video_url': f"https://www.youtube.com/watch?v={video_id}",
                    'embed_url': f"https://www.youtube.com/embed/{video_id}"
                })
        return videos[:max_results] # Filtreleme sonrası gerekirse sınırlat
    except Exception as e:
        logger.error(f"YouTube API çağrısında hata oluştu: {e}")
        return []
