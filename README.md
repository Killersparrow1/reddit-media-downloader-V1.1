# Reddit Media Downloader V1.1 

A browser-based tool to download media from Reddit users with a modern, responsive interface.

![Reddit](https://img.shields.io/badge/Reddit-Media%2520Downloader-orange)
![Python](https://img.shields.io/badge/Python-3.8%252B-blue)
![Flask](https://img.shields.io/badge/Flask-2.0%252B-lightgrey)

## Screenshot

[![light-Edit-Edit.png](https://i.postimg.cc/KjXRnLkF/light-Edit-Edit.png)](https://postimg.cc/9Rpm2DYN)
[![dark-Edit-Edit.png](https://i.postimg.cc/14h5qZdz/dark-Edit-Edit.png)](https://postimg.cc/wR2dCngK)
"The application includes functionality to filter and handle NSFW (Not Safe For Work) content, with appropriate user controls and warnings. Screenshots demonstrating this capability are included solely for the purpose of showcasing the application's complete feature set in a technical context."

## 📋 Overview
Reddit Media Downloader is a Python Flask application that allows users to download images and videos from any Reddit user's posts. It features a modern glass-morphism UI with dark mode support, bulk downloading capabilities, and filtering options.

**Disclaimer:** This project was created by an enthusiastic developer without formal coding education. It's a learning project that may contain imperfections but has been crafted with care and attention to detail.

## ✨ Features
- 🔍 Fetch media from any Reddit user
- 🖼️ Filter by content type (images, videos, or all)
- ⚠️ NSFW content filtering with clear warnings
- 💾 Bulk download media as ZIP files
- 🌙 Dark/Light mode toggle
- 📱 Responsive design for all devices
- 🎨 Modern glass-morphism UI with SVG icons
- 📊 Media statistics and previews

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone the Repository
```bash
git clone https://github.com/your-username/reddit-media-downloader.git
cd reddit-media-downloader
```

### Step 2: Set Up a Virtual Environment (Recommended)
**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```
**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```
If you don't have a `requirements.txt` file, install manually:
```bash
pip install flask flask-cors praw requests
```

### Step 4: Set Up Reddit API Credentials
- Go to [Reddit Apps](https://www.reddit.com/prefs/apps)
- Click "Create another app..." or "Create App"
- Fill in the form:
  - Name: RedditMediaDownloader
  - App type: Script
  - Redirect URI: http://localhost:5000
- Click "Create app"
- Note the client ID (under the app name) and client secret

Update `app.py` with your credentials:
```python
REDDIT_CLIENT_ID = "your_actual_client_id"
REDDIT_CLIENT_SECRET = "your_actual_client_secret"
REDDIT_USER_AGENT = "RedditMediaDownloader/1.0 by YourRedditUsername"
```

### Step 5: Run the Application
```bash
python app.py
```
Access at [http://localhost:5000](http://localhost:5000)

## 🚀 Usage
1. Open your browser and navigate to [http://localhost:5000](http://localhost:5000)  
2. Enter a Reddit username (without `u/`)  
3. Set the number of posts to check (max 1000)  
4. Select content type (all, images, or videos)  
5. Choose whether to include NSFW content  
6. Click "Fetch Media"  
7. Preview the media and click "Download All" to get a ZIP file

## 📁 Project Structure
```
reddit-media-downloader/
├── app.py                 # Main Flask application
├── templates/
│   └── index.html         # Main HTML template
├── downloads/             # Directory for downloaded files
├── README.md              # This file
└── requirements.txt       # Python dependencies
```

## ⚠️ Legal Notice
This tool is for personal use only. Respect copyright laws and Reddit's terms of service.  
Do not download or distribute content without proper authorization.  
Reddit is a trademark of Reddit, Inc. This application is not affiliated with or endorsed by Reddit, Inc.

## 🤝 Contributing
As this is a learning project, contributions and suggestions are welcome! Submit issues or pull requests.

## 🙏 Acknowledgments
- DeepSeek AI for guidance  
- Reddit API for access to Reddit content  
- Python and Flask communities for documentation  
- Google Fonts for Pixelify Sans and Inter fonts  
- All open-source projects that inspired this tool

## 📄 License
MIT License. See the [LICENSE file](https://github.com/Killersparrow1/reddit-media-downloader-V1.1/blob/main/LICENSE) for details.

## AI Assistance Notice

This project was created with significant assistance from DeepSeek AI. 
While the implementation and customization were done by [Killersparrow1](https://github.com/Killersparrow1),
the core structure and code patterns were generated with AI assistance.

## 🐛 Troubleshooting
**API Connection Errors:** Verify credentials and `app.py` placeholders  
**Module Not Found Errors:** Install requirements and activate virtual environment  
**Download Failures:** Check console for error messages; some media hosts may require additional handling

## 📞 Support
Open an issue on the GitHub repository for questions or issues.

**Note:** Developed by an enthusiastic learner without formal coding education. Feedback and contributions are welcome!

Enjoy using the Reddit Media Downloader V1.1!
