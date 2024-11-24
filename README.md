# 🗞️ Vietnamese News Scraper

[![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/flask-v2.0.1-green.svg)](https://flask.palletsprojects.com/)
[![BeautifulSoup](https://img.shields.io/badge/beautifulsoup4-v4.9.3-orange.svg)](https://www.crummy.com/software/BeautifulSoup/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> A powerful Flask-based web application for collecting and analyzing news from Vietnam's leading digital newspapers. Support multiple date formats, pagination handling, and advanced SSL certificate management.

## 📋 Features

### 📰 Supported News Sources
- [VnExpress](https://vnexpress.net/) - Full support with date range filtering
- [VietnamNet](https://vietnamnet.vn/) - Advanced pagination with date filtering
- [Báo Quốc Tế](https://baoquocte.vn/) - Dynamic pagination with 15 articles per page
- [Thông Tấn Xã Việt Nam](https://baotintuc.vn/) - Legacy SSL support with date-based scraping
- [Thanh Niên](https://thanhnien.vn/) - Basic scraping support
- [Người Đưa Tin](https://www.nguoiduatin.vn/) - Basic scraping support
- [Dân Trí](https://dantri.com.vn/) - Basic scraping support
- [Tiền Phong](https://tienphong.vn/) - Basic scraping support

### 📑 News Categories
Each news source supports the following categories with source-specific URLs:
- Current Affairs (Thời sự)
- Business (Kinh doanh)
- Sports (Thể thao)
- Entertainment (Giải trí)
- Education (Giáo dục)
- Health (Sức khỏe)

### 🛠️ Advanced Features

#### Date Handling
- **Multiple Date Formats Support**
  - DD/MM/YYYY HH:MM
  - HH:MM DD/MM/YYYY
  - DD/MM/YYYY
  - YYYY-MM-DD

#### Pagination Mechanisms
- **VnExpress**: 
  - Current day: `-p{page_number}` (e.g., `-p2`, `-p3`)
  - Date range: `/page/{page_number}`
  - Category-based filtering with IDs

- **VietnamNet**:
  - Current day: `-page{page_number}`
  - Date range: `-p{page_number}?bydate=DD/MM/YYYY`
  - Category ID support

- **Báo Quốc Tế**:
  - BRSR-based pagination: `&BRSR={offset}`
  - 15 articles per page
  - Date filtering with `&fv=YYYY-MM-DD`

- **Thông Tấn Xã**:
  - Day-based URLs: `/d{DD-MM-YYYY}`
  - Category prefix support
  - Legacy SSL handling

#### Security Features
- Custom SSL certificate handling
- Legacy protocol support
- Secure request adapters
- Certificate verification options

### 🔧 Technical Improvements

#### Error Handling
- Comprehensive exception catching
- Detailed error logging
- Fallback mechanisms for failed requests
- Rate limiting protection

#### Performance Optimizations
- 1-second delay between requests
- Memory-efficient article processing
- Batch processing for date ranges
- Custom HTTP adapters

## 💻 URL Formats and Examples

### VnExpress
```plaintext
Current Day: https://vnexpress.net/thoi-su-p2
Date Range: /category/day/cateid/1001005/fromdate/{timestamp}/todate/{timestamp}
```

### VietnamNet
```plaintext
Current Day: https://vietnamnet.vn/thoi-su-page1
Date Range: https://vietnamnet.vn/tin-tuc-24h-p2?bydate=05/11/2024-13/11/2024&cate=000002
```

### Báo Quốc Tế
```plaintext
Current Day: https://baoquocte.vn/thoi-su&s_cond=&BRSR=15
Date Range: https://baoquocte.vn/kinh-te&fv=2024-11-15&s_cond=&BRSR=15
```

### Thông Tấn Xã
```plaintext
Current Day: https://baotintuc.vn/thoi-su-472ct0.htm
Date Range: https://baotintuc.vn/thoi-su-472ct0/d10-10-2024.htm
```

## 📁 Enhanced Project Structure
```
vietnamese-news-scraper/
├── main.py                # Main Flask application
├── scraper.py             # Core scraping logic
├── fetch_url.py           # URL fetching with SSL handling
├── requirements.txt       # Project dependencies
├── templates/             # HTML templates
│   ├── home.html         # Main interface
│   ├── 404.html          # Error page
│   └── 500.html          # Server error page
└── static/               # Static assets
```

## ⚠️ Important Considerations

### SSL Handling
- Custom SSL adapters for legacy sites
- Security level adjustments for older servers
- Certificate verification options

### Rate Limiting
- 1-second delay between requests
- Source-specific timing adjustments
- Error handling for rate limits

### Memory Management
- Default limit: 1000 articles per collection
- Batch processing for large date ranges
- Memory-efficient article storage

### Date Processing
- Multi-format date parsing
- Timezone handling
- Date range validation

## 🔍 Advanced Usage Examples

### Date Range Scraping
```python
scraper = NewsScraper()

# VnExpress with date range
articles = scraper.scrape_news(
    'VnExpress',
    'Thời sự',
    quantity=100,
    fromdate='2024-11-20',
    todate='2024-11-24'
)

# Báo Quốc Tế with pagination
articles = scraper.scrape_news(
    'Thế giới và Việt Nam',
    'Kinh doanh',
    quantity=100,
    fromdate='2024-11-15'
)

# TTXVN with date filtering
articles = scraper.scrape_news(
    'Thông tấn xã Việt Nam',
    'Thời sự',
    quantity=50,
    fromdate='2024-10-10',
    todate='2024-10-15'
) 

## 🔧 Troubleshooting Guide

### Common Issues and Solutions

#### SSL Certificate Errors
```bash
Error: [SSL: UNSAFE_LEGACY_RENEGOTIATION_DISABLED] unsafe legacy renegotiation disabled
```
**Solution:** The scraper includes custom SSL adapters. If you encounter this error:
1. Check your Python version supports legacy SSL
2. Use the provided `fetch_url.py` helper
3. Configure security level in SSL context

#### Rate Limiting Detection
```bash
Error: HTTP Error 429: Too Many Requests
```
**Solution:**
1. Increase delay between requests (default: 1 second)
2. Use proxy rotation
3. Implement exponential backoff

#### Memory Issues with Large Date Ranges
**Solution:**
1. Use batch processing with smaller date ranges
2. Implement pagination with smaller quantity per request
3. Enable garbage collection for large scrapes

### Source-Specific Issues

#### VnExpress
- Category ID mismatch
- Timestamp conversion errors
- Pagination format changes

**Solutions:**
```python
# Custom category ID mapping
self.vnexpress_categories = {
    'Thời sự': '1001005',
    'Kinh doanh': '1003159',
    # ...
}

# Timestamp handling
def _convert_date_to_timestamp(self, date_str):
    dt = datetime.strptime(date_str, '%Y-%m-%d')
    return int(dt.timestamp())
```

#### Báo Quốc Tế
- BRSR pagination errors
- Date format mismatches
- Article container changes

**Solutions:**
```python
# Correct BRSR calculation
current_url = f"{base_url}&s_cond=&BRSR={page * 15}"

# Date format standardization
formatted_date = date.strftime('%Y-%m-%d')
```

## 📈 Performance Optimization

### Memory Usage
```python
# Batch processing example
def process_in_batches(self, date_range, batch_size=100):
    for i in range(0, len(date_range), batch_size):
        batch = date_range[i:i + batch_size]
        yield self.process_batch(batch)
```

### Request Optimization
```python
# Custom session with retries
session = requests.Session()
retries = Retry(total=5, backoff_factor=1)
session.mount('https://', HTTPAdapter(max_retries=retries))
```

### Caching Strategy
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def fetch_cached_content(url):
    return requests.get(url).content
```

## 🛣️ Development Roadmap

### Version 1.1 (Current)
- ✅ Multi-source support
- ✅ Date range filtering
- ✅ Basic error handling
- ✅ SSL certificate management

### Version 1.2 (Planned)
- 🔄 Proxy support
- 🔄 Advanced caching
- 🔄 Async scraping
- 🔄 Database integration

### Version 1.3 (Future)
- 📋 Content analysis
- 📋 Sentiment detection
- 📋 Topic clustering
- 📋 API rate limiting

## 🤝 Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📮 Contact

Nguyễn Hải Đăng - [@NHDanDz] - nhdandz@gmail.com

Project Link: [https://github.com/NHDanDz/Crawl-Vietnamese-News](https://github.com/NHDanDz/Crawl-Vietnamese-News)

## 🙏 Acknowledgments

* [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) for web scraping capabilities
* [Flask](https://flask.palletsprojects.com/) for the web framework
* All news sources for providing content
