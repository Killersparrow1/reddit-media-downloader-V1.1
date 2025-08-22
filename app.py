import os
import requests
import praw
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import json
from datetime import datetime
import urllib.parse
import mimetypes
from pathlib import Path
import zipfile
import io
import time

app = Flask(__name__)
CORS(app)

# Configuration
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Reddit API configuration (you'll need to get these from https://www.reddit.com/prefs/apps)
REDDIT_CLIENT_ID = "V_-2uWSGNG2dVUxCnxNkag"
REDDIT_CLIENT_SECRET = "TEFKG83C-tHPj6jr0Vh6shPNIY59MQ"
REDDIT_USER_AGENT = "RedditMediaDownloader/1.0 by Jeonmission"

# Initialize Reddit instance
try:
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT
    )
    # Test the connection
    reddit.user.me()
except Exception as e:
    print(f"Error connecting to Reddit API: {e}")
    print("Please check your API credentials")
    reddit = None

def get_media_urls(username, limit=100, content_type='all', include_nsfw=False):
    """
    Fetch media URLs from a Reddit user's posts
    """
    media_urls = []
    
    if not reddit:
        return media_urls
    
    try:
        user = reddit.redditor(username)
        
        for submission in user.submissions.new(limit=limit):
            # Skip NSFW content if not allowed
            if submission.over_18 and not include_nsfw:
                continue
            
            # Skip posts that don't match the content type filter
            if content_type != 'all':
                if content_type == 'images' and not (submission.is_reddit_media_domain or 
                                                   submission.url.endswith(('.jpg', '.jpeg', '.png', '.gif'))):
                    continue
                if content_type == 'videos' and not (getattr(submission, 'is_video', False) or 
                                                    submission.url.endswith(('.mp4', '.gifv'))):
                    continue
            
            url = submission.url
            media_data = {
                'url': url,
                'title': submission.title,
                'id': submission.id,
                'created_utc': submission.created_utc,
                'type': 'unknown',
                'nsfw': submission.over_18,
                'permalink': f"https://reddit.com{submission.permalink}"
            }
            
            # Handle different types of media
            if submission.is_reddit_media_domain:
                # Reddit hosted images
                if hasattr(submission, 'preview') and 'images' in submission.preview:
                    media_data['url'] = submission.preview['images'][0]['source']['url']
                    media_data['type'] = 'image'
                # Reddit hosted videos
                elif getattr(submission, 'is_video', False) and submission.media:
                    media_data['url'] = submission.media['reddit_video']['fallback_url']
                    media_data['type'] = 'video'
            # Handle direct image links (imgur, etc.)
            elif url.endswith(('.jpg', '.jpeg', '.png')):
                media_data['type'] = 'image'
            elif url.endswith('.gif') or url.endswith('.gifv'):
                media_data['type'] = 'gif'
                if url.endswith('.gifv'):
                    media_data['url'] = url.replace('.gifv', '.mp4')
                    media_data['type'] = 'video'
            elif 'imgur.com' in url and '/a/' in url:
                # Imgur album - we'll skip these for simplicity
                continue
            elif 'v.redd.it' in url:
                # Reddit video
                media_data['type'] = 'video'
            else:
                # Unsupported content type
                continue
            
            media_urls.append(media_data)
            # Be respectful to Reddit's API
            time.sleep(0.1)
    
    except Exception as e:
        print(f"Error fetching media for {username}: {e}")
    
    return media_urls

def download_media(media_url, username, folder_path):
    """
    Download a single media file
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(media_url['url'], headers=headers, stream=True, timeout=30)
        if response.status_code == 200:
            # Determine file extension
            content_type = response.headers.get('content-type')
            if content_type:
                ext = mimetypes.guess_extension(content_type.split(';')[0])
            else:
                # Guess from URL
                ext = os.path.splitext(urllib.parse.urlparse(media_url['url']).path)[1]
                if not ext:
                    ext = '.jpg'  # Default extension
            
            # Clean filename
            clean_title = "".join(c for c in media_url['title'] if c.isalnum() or c in (' ', '-', '_')).rstrip()
            if not clean_title:
                clean_title = media_url['id']
            filename = f"{clean_title}_{media_url['id']}{ext}"
            filepath = os.path.join(folder_path, filename)
            
            # Download file
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            return filepath
    except Exception as e:
        print(f"Error downloading {media_url['url']}: {e}")
    
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch_media', methods=['POST'])
def fetch_media():
    if not reddit:
        return jsonify({'error': 'Reddit API not configured. Please check your credentials.'}), 500
        
    data = request.json
    username = data.get('username')
    limit = min(int(data.get('limit', 100)), 1000)  # Cap at 1000 for safety
    content_type = data.get('content_type', 'all')
    include_nsfw = data.get('include_nsfw', False)
    
    if not username:
        return jsonify({'error': 'Username is required'}), 400
    
    media_urls = get_media_urls(username, limit, content_type, include_nsfw)
    
    return jsonify({
        'username': username,
        'media_count': len(media_urls),
        'media_urls': media_urls
    })

@app.route('/download_media', methods=['POST'])
def download_media_endpoint():
    data = request.json
    username = data.get('username')
    media_urls = data.get('media_urls', [])
    
    if not username or not media_urls:
        return jsonify({'error': 'Username and media URLs are required'}), 400
    
    # Create user folder
    user_folder = os.path.join(DOWNLOAD_FOLDER, username)
    os.makedirs(user_folder, exist_ok=True)
    
    # Download each media file
    downloaded_files = []
    for i, media_url in enumerate(media_urls):
        filepath = download_media(media_url, username, user_folder)
        if filepath:
            downloaded_files.append(filepath)
        
        # Update progress (this would be better with websockets, but for simplicity...)
    
    # Create zip file
    zip_filename = f"{username}_media_{int(datetime.now().timestamp())}.zip"
    zip_path = os.path.join(DOWNLOAD_FOLDER, zip_filename)
    
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for file in downloaded_files:
            zipf.write(file, os.path.basename(file))
    
    return jsonify({
        'username': username,
        'downloaded_count': len(downloaded_files),
        'zip_file': zip_filename
    })

@app.route('/download_zip/<filename>')
def download_zip(filename):
    zip_path = os.path.join(DOWNLOAD_FOLDER, filename)
    if os.path.exists(zip_path):
        return send_file(zip_path, as_attachment=True)
    return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
