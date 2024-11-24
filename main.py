from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from flask_cors import cross_origin
from scraper import NewsScraper
import os

# Initialize Flask app
app = Flask(__name__) 

# News sources and topics
news_sources = [
    {"id": 1, "name": "VnExpress", "url": "https://vnexpress.net"},
    {"id": 2, "name": "Thanh Niên", "url": "https://thanhnien.vn"},
    {"id": 3, "name": "VietnamNet", "url": "https://vietnamnet.vn"},
    {"id": 4, "name": "Người Đưa Tin", "url": "https://nguoiduatin.vn"},
    {"id": 5, "name": "Dân Trí", "url": "https://dantri.com.vn"},
    {"id": 6, "name": "Tiền Phong", "url": "https://tienphong.vn"}
]

topics = [
    "Thời sự", "Kinh doanh", "Thể thao", "Giải trí", 
    "Giáo dục", "Sức khỏe"
]

@app.route('/')
def home(): 
    return render_template('home.html', sources=news_sources, topics=topics)
@app.route('/collect', methods=['POST'])
def collect_news():
    try:
        data = request.get_json()
        if not data or 'sources' not in data or 'topics' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required data'
            }), 400

        # Extract timestamps if provided
        fromdate = data.get('fromdate')
        todate = data.get('todate')

        scraper = NewsScraper()
        all_articles = []
        failed_sources = []
        
        for source in data['sources']:
            for topic in data['topics']:
                try:
                    # Pass timestamps to scraper
                    articles = scraper.scrape_news(
                        source, 
                        topic, 
                        quantity=25,
                        fromdate=fromdate,
                        todate=todate
                    )
                    
                    for article in articles:
                        formatted_article = {
                            'title': article.get('title', ''),
                            'description': article.get('description', ''),
                            'link': article.get('link', ''),
                            'date': article.get('date', ''),
                            'source': article.get('source', source),
                            'topic': topic
                        }
                        all_articles.append(formatted_article)
                except Exception as e:
                    print(f"Error processing {source} - {topic}: {str(e)}")
                    failed_sources.append({
                        'source': source,
                        'topic': topic,
                        'error': str(e)
                    })
                    continue

        return jsonify({
            'success': True,
            'data': all_articles,
            'total': len(all_articles),
            'failed_sources': failed_sources if failed_sources else None
        })

    except Exception as e:
        print(f"Error in collect_news: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/search', methods=['POST'])
def search_news():
    try:
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing search query'
            }), 400
            
        query = data['query'].lower()
        sources = data.get('sources', [s["name"] for s in news_sources])
        topics = data.get('topics', topics)
        
        scraper = NewsScraper()
        search_results = []
        
        for source in sources:
            for topic in topics:
                try:
                    articles = scraper.scrape_news(source, topic, quantity=50)
                    
                    # Filter articles based on search query
                    for article in articles:
                        if query in article.get('title', '').lower() or \
                           query in article.get('description', '').lower():
                            formatted_article = {
                                'title': article.get('title', ''),
                                'description': article.get('description', ''),
                                'link': article.get('link', ''),
                                'date': article.get('date', ''),
                                'source': article.get('source', source),
                                'topic': topic
                            }
                            search_results.append(formatted_article)
                            
                except Exception as e:
                    print(f"Error searching {source} - {topic}: {str(e)}")
                    continue
        
        return jsonify({
            'success': True,
            'data': search_results,
            'total': len(search_results)
        })
        
    except Exception as e:
        print(f"Error in search_news: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Add this helper method to check for XHR requests
@app.before_request
def before_request():
    if not hasattr(request, 'is_xhr'):
        request.is_xhr = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

if __name__ == "__main__": 
    # Run app in debug mode
    app.run(debug=True)