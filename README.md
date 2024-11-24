# 🗞️ Vietnamese News Scraper

[![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/flask-v2.0.1-green.svg)](https://flask.palletsprojects.com/)
[![BeautifulSoup](https://img.shields.io/badge/beautifulsoup4-v4.9.3-orange.svg)](https://www.crummy.com/software/BeautifulSoup/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> A powerful Flask-based web application for collecting and analyzing news from Vietnam's leading digital newspapers.

## 📋 Features

### 📰 Supported News Sources
- [VnExpress](https://vnexpress.net/)
- [Thanh Niên](https://thanhnien.vn/)
- [VietnamNet](https://vietnamnet.vn/)
- [Người Đưa Tin](https://www.nguoiduatin.vn/)
- [Dân Trí](https://dantri.com.vn/)
- [Tiền Phong](https://tienphong.vn/)

### 📑 News Categories
- Current Affairs (Thời sự)
- Business (Kinh doanh)
- Sports (Thể thao)
- Entertainment (Giải trí)
- Education (Giáo dục)
- Health (Sức khỏe)

### 🛠️ Core Functions
- Collect news by date range
- Keyword-based news search
- News data analysis
- Pagination support
- Article quantity limit options

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/vietnamese-news-scraper.git
cd vietnamese-news-scraper
```

2. **Set up virtual environment**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# For Windows
venv\Scripts\activate
# For macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

### Dependencies
```plaintext
flask==2.0.1
flask-sqlalchemy==2.5.1
flask-cors==3.0.10
beautifulsoup4==4.9.3
requests==2.26.0
```

## 💻 Usage

### Starting the Server
```bash
python main.py
```
The server will run at `http://localhost:5000`

### API Documentation

#### 1. Collect News
```http
POST /collect
```

Request Body:
```json
{
    "sources": ["VnExpress", "Thanh Niên"],
    "topics": ["Thời sự", "Kinh doanh"],
    "fromdate": "2024-11-20",
    "todate": "2024-11-24"
}
```

Response:
```json
{
    "success": true,
    "data": [
        {
            "title": "Article Title",
            "description": "Article Description",
            "link": "Article URL",
            "date": "Publication Date",
            "source": "News Source",
            "topic": "Category"
        }
    ],
    "total": 100
}
```

#### 2. Search News
```http
POST /search
```

Request Body:
```json
{
    "query": "search keyword",
    "sources": ["VnExpress"],
    "topics": ["Thời sự"]
}
```

#### 3. Analyze News
```http
POST /analytics
```

Request Body:
```json
{
    "articles": [
        {
            "title": "Article Title",
            "description": "Description",
            "link": "URL",
            "date": "Date",
            "source": "Source",
            "topic": "Category"
        }
    ]
}
```

## 🔍 Source-Specific Handling

### VnExpress
- **Current Day:** Regular URL with pagination (`-p2`, `-p3`,...)
- **Date Range:** URL format: `/category/day/cateid/{id}/fromdate/{timestamp}/todate/{timestamp}`

### VietnamNet
- **Current Day:** URL format: `thoi-su-page1`, `thoi-su-page2`,...
- **Date Range:** URL format: `tin-tuc-24h-p2?bydate=05/11/2024-13/11/2024&cate=000002`

## 📁 Project Structure
```
vietnamese-news-scraper/
├── main.py           # Main Flask application
├── scraper.py        # News scraping module
├── requirements.txt  # Project dependencies
├── templates/        # HTML templates
│   ├── home.html
│   ├── 404.html
│   └── 500.html
└── static/          # Static files
```

## ⚠️ Important Notes

### Rate Limiting
- 1-second delay between requests
- Consider implementing additional rate limiting for production

### Memory Management
- Default limit: 1000 articles per collection
- Adjustable via `quantity` parameter

### Time Handling
- Date format: YYYY-MM-DD
- Timezone consideration required

## 🤝 Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📮 Contact

Your Name - [@yourusername](https://twitter.com/yourusername) - email@example.com

Project Link: [https://github.com/yourusername/vietnamese-news-scraper](https://github.com/yourusername/vietnamese-news-scraper)

## 🙏 Acknowledgments

* [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) for web scraping capabilities
* [Flask](https://flask.palletsprojects.com/) for the web framework
* All news sources for providing content
