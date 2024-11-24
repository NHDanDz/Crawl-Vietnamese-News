
import time
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import urllib.request
import subprocess

class NewsScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.vnexpress_categories = {
            'Thời sự': '1001005',
            'Kinh doanh': '1003159',
            'Thể thao': '1002565',
            'Giải trí': '1002691',
            'Giáo dục': '1003497',
            'Sức khỏe': '1003750'
        }

    def _convert_date_to_timestamp(self, date_str):
        """Convert date string to Unix timestamp"""
        try:
            # Assuming date_str is in format 'YYYY-MM-DD'
            dt = datetime.strptime(date_str, '%Y-%m-%d')
            return int(dt.timestamp())
        except Exception as e:
            print(f"Error converting date: {e}")
            return None

    def _is_date_in_range(self, article_date, start_date, end_date):
        """Check if article date is within the specified range"""
        try:
            # Convert article date string to datetime object
            # Handle different date formats from different news sources
            date_formats = [
                '%d/%m/%Y %H:%M',  # Example: 24/11/2023 15:30
                '%H:%M %d/%m/%Y',  # Example: 15:30 24/11/2023
                '%d/%m/%Y',        # Example: 24/11/2023
                '%Y-%m-%d',        # Example: 2023-11-24
            ]
            
            article_dt = None
            for fmt in date_formats:
                try:
                    article_dt = datetime.strptime(article_date.split(' GMT')[0].strip(), fmt)
                    break
                except:
                    continue
            
            if not article_dt:
                return True  # If we can't parse the date, include the article
            
            start_dt = datetime.strptime(start_date, '%Y-%m-%d')
            end_dt = datetime.strptime(end_date, '%Y-%m-%d')
            
            return start_dt <= article_dt <= end_dt
        except Exception as e:
            print(f"Error checking date range: {e}")
            return True  # If there's an error, include the article

    def scrape_news(self, source: str, topic: str, quantity: int = 1000, fromdate=None, todate=None):
        """Main method to scrape news based on source"""
        base_url = self._get_base_url(source, topic)
        if not base_url:
            print(f"No base URL found for {source} - {topic}")
            return []

        try:
            articles = []
            if source == 'VnExpress':
                # Check if dates are provided and if todate is today
                if fromdate and todate:
                    today = datetime.now().strftime('%Y-%m-%d')
                    if todate == today:
                        # If todate is today, don't apply date filter
                        print("Today's date detected - scraping without date filter") 
                    else:
                        # Apply date filter for historical dates
                        from_timestamp = self._convert_date_to_timestamp(fromdate)
                        to_timestamp = self._convert_date_to_timestamp(todate)
                        if from_timestamp and to_timestamp:
                            category_id = self.vnexpress_categories.get(topic)
                            if category_id:
                                base_url = f"https://vnexpress.net/category/day/cateid/{category_id}/fromdate/{from_timestamp}/todate/{to_timestamp}/allcate/{category_id}"
                print(f"Using URL: {base_url}")
                articles = self._scrape_vnexpress(base_url, quantity)
                
            elif source == 'VietnamNet':
                    articles = self._scrape_vietnamnet(base_url, quantity, fromdate, todate)
            elif source == 'VietnamNet':
                articles = self._scrape_vietnamnet(base_url, quantity)
            elif source == 'Người Đưa Tin':
                articles = self._scrape_nguoiduatin(base_url, quantity)
            elif source == 'Dân Trí':
                articles = self._scrape_dantri(base_url, quantity)
            elif source == 'Tiền Phong':
                articles = self._scrape_tienphong(base_url, quantity)
            elif source == 'Thế giới và Việt Nam':
                return self._scrape_baoquocte(base_url, quantity)
            elif source == 'Thông tấn xã Việt Nam':
                return self._scrape_baotintuc(base_url, quantity)

            # Filter articles by date range for non-VnExpress sources
            # if fromdate and todate and source != 'VnExpress':
            #     filtered_articles = []
            #     for article in articles:
            #         if article.get('date') and self._is_date_in_range(article['date'], fromdate, todate):
            #             filtered_articles.append(article)
            #     articles = filtered_articles[:quantity]
            
            return articles

        except Exception as e:
            print(f"Error scraping {source}: {str(e)}")
            return []

    def _parse_vnexpress_date(self, date_str):
        """Parse VnExpress date string to datetime object"""
        try:
            # Remove timezone info and trim
            date_str = date_str.split('GMT')[0].strip()
            return datetime.strptime(date_str, '%d/%m/%Y %H:%M')
        except Exception as e:
            print(f"Error parsing VnExpress date: {e}")
            return None

    def _scrape_vnexpress(self, base_url, quantity):
        articles = []
        page = 1
        
        try:
            while len(articles) < quantity:
                # Construct URL with pagination
                if "fromdate" in base_url and "todate" in base_url:
                    # URL format for date-filtered pages
                    current_url = f"{base_url}/page/{page}" if page > 1 else base_url
                else:
                    # URL format for regular pages
                    current_url = f"{base_url}-p{page}" if page > 1 else base_url
                
                print(f"Scraping page {page}: {current_url}")
                
                response = requests.get(current_url, headers=self.headers)
                if response.status_code != 200:
                    break
                    
                soup = BeautifulSoup(response.content, 'html.parser')
                article_containers = [
                    '.width_common.list-news-subfolder',
                    '.container-fluid .sidebar-1',
                    '.width_common.list_news',
                    '.col-left-top'
                ]
                
                found_articles = False
                for container_selector in article_containers:
                    containers = soup.select(container_selector)
                    for container in containers:
                        articles_elements = container.find_all(['article', 'div'], class_=['item-news', 'article-item'])
                        
                        if articles_elements:
                            found_articles = True
                            
                        for article in articles_elements:
                            if len(articles) >= quantity:
                                return articles
                                
                            try:
                                title_elem = (
                                    article.find('a', class_='title-news') or 
                                    article.find('h3', class_='title-news').find('a') if article.find('h3', class_='title-news') else None or
                                    article.find('a', class_='art-title')
                                )
                                
                                desc_elem = (
                                    article.find('p', class_='description') or
                                    article.find('p', class_='news-item__description') or
                                    article.find('p', class_='article-item__summary')
                                )
                                
                                date_elem = (
                                    article.find('span', class_='time-publish') or
                                    article.find('span', class_='time') or
                                    article.find('span', class_='article-item__publish')
                                )
                                
                                if title_elem and desc_elem:
                                    articles.append({
                                        'title': title_elem.text.strip(),
                                        'description': desc_elem.text.strip(),
                                        'link': title_elem.get('href', ''),
                                        'date': date_elem.text.strip() if date_elem else '',
                                        'source': 'VnExpress'
                                    })
                                
                            except Exception as e:
                                print(f"Error parsing individual VnExpress article: {e}")
                                continue
                
                # Break if no articles found on current page
                if not found_articles:
                    break
                    
                page += 1
                
                # Add a small delay between requests to be polite
                time.sleep(1)
                
        except Exception as e:
            print(f"Error fetching VnExpress: {e}")
            
        return articles[:quantity]
    # def scrape_news(self, source: str, topic: str, quantity: int = 25):
    #     """Main method to scrape news based on source"""
    #     base_url = self._get_base_url(source, topic)
    #     if not base_url:
    #         print(f"No base URL found for {source} - {topic}")
    #         return []

    #     try:
    #         if source == 'VnExpress':
    #             return self._scrape_vnexpress(base_url, quantity)
    #         elif source == 'Thanh Niên':
    #             return self._scrape_thanhnien(base_url, quantity)
    #     except Exception as e:
    #         print(f"Error scraping {source}: {str(e)}")
    #         return []

    # def _scrape_vnexpress(self, url, quantity):
    #     # VnExpress scraping code remains the same...
    #     pass

    def _scrape_thanhnien(self, url, quantity): 
        # print(url)
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, 'html.parser')
        # <div>
        div_all = soup.find_all('div', attrs={'class':'main'})
        # div_all
        # <h2>
        h3_all = []
        for div in div_all:
            h3_all.extend(div.find_all('h3', attrs={'class':'box-title-text', 'data-vr-headline':""})) 
        a_all = [] 
        articles = [] 
        for h3 in h3_all: 
            if len(articles) >= quantity:
                break
            try:
                link_elem = h3.find('a', attrs={'class':'box-category-link-title'}) 
                if not link_elem:
                    continue 
                title = link_elem.get('title')
                link = link_elem.get('href')
                # print(title, link)
                
                if link and not link.startswith('http'):
                    link = 'https://thanhnien.vn' + link
                    
                article_container = h3.find_parent('article') or h3.find_parent('div')
                desc_elem = article_container.find('p', class_='box-content-text') if article_container else None
                description = desc_elem.text.strip() if desc_elem else ''
                
                date_elem = article_container.find('span', class_='box-pub-time') if article_container else None  
                date = date_elem.text.strip() if date_elem else ''
                
                if title and link:
                    articles.append({
                        'title': title,
                        'description': description, 
                        'link': link,
                        'date': date,
                        'source': 'Thanh Niên'
                    })
                    
            except Exception as e:
                print(f"Error parsing article: {str(e)}")
                continue 
        return articles
    def _scrape_vietnamnet(self, url, quantity, fromdate=None, todate=None):
        articles = []
        page = 1
        
        # Map topics to category IDs for date filtering
        topic_mapping = {
            'thoi-su': {'name': 'Thời sự', 'id': '000002'},
            'kinh-doanh': {'name': 'Kinh doanh', 'id': '000003'},
            'the-thao': {'name': 'Thể thao', 'id': '000008'},
            'giai-tri': {'name': 'Giải trí', 'id': '000012'},
            'giao-duc': {'name': 'Giáo dục', 'id': '000006'},
            'suc-khoe': {'name': 'Sức khỏe', 'id': '000005'}
        }
        
        try:
            while len(articles) < quantity:
                current_url = ""
                
                if fromdate and todate and not self._is_today(todate):
                    # Format dates for URL
                    from_date_str = datetime.strptime(fromdate, '%Y-%m-%d').strftime('%d/%m/%Y')
                    to_date_str = datetime.strptime(todate, '%Y-%m-%d').strftime('%d/%m/%Y')
                    
                    # Extract topic from URL
                    topic_key = url.split('vietnamnet.vn/')[1].split('/')[0] if 'vietnamnet.vn/' in url else ''
                    category_id = topic_mapping.get(topic_key, {}).get('id', '000002')  # Default to Thời sự if not found
                    
                    # Construct URL for date range
                    if page == 1:
                        current_url = f"https://vietnamnet.vn/tin-tuc-24h?bydate={from_date_str}-{to_date_str}&cate={category_id}"
                    else:
                        current_url = f"https://vietnamnet.vn/tin-tuc-24h-p{page}?bydate={from_date_str}-{to_date_str}&cate={category_id}"
                else:
                    # URL for current day (default pagination)
                    base_url = url.rstrip('/')
                    current_url = f"{base_url}-page{page}" if page > 1 else base_url
                
                print(f"Scraping page {page}: {current_url}")
                
                try:
                    response = requests.get(current_url, headers=self.headers)
                    if response.status_code != 200:
                        print(f"Failed to fetch page {page}: Status code {response.status_code}")
                        break
                        
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Find all article containers
                    article_containers = soup.find_all('div', attrs={'class': 'verticalPost__main'}) + \
                                    soup.find_all('div', attrs={'class':'horizontalPost__main'})
                    
                    if not article_containers:
                        print(f"No articles found on page {page}")
                        break
                    
                    found_new_articles = False
                    for container in article_containers:
                        try:
                            # Find title and link
                            title_elem = container.find(['h3', 'h2']).find('a')
                            if not title_elem:
                                continue

                            title = title_elem.get('title')
                            link = title_elem.get('href')

                            if link and not link.startswith('http'):
                                link = 'https://vietnamnet.vn' + link

                            # Find description
                            desc_elem = container.find('p')
                            description = desc_elem.text.strip() if desc_elem else ''

                            # Find date
                            date_elem = container.find('span', class_='time')
                            date = date_elem.text.strip() if date_elem else ''

                            if title and link:
                                found_new_articles = True
                                articles.append({
                                    'title': title,
                                    'description': description,
                                    'link': link,
                                    'date': date,
                                    'source': 'VietnamNet'
                                })
                                
                                if len(articles) >= quantity:
                                    return articles[:quantity]
                                    
                        except Exception as e:
                            print(f"Error parsing article in container: {str(e)}")
                            continue
                    
                    if not found_new_articles:
                        print("No new articles found on this page")
                        break
                    
                    page += 1
                    time.sleep(1)  # Be nice to the server
                    
                except Exception as e:
                    print(f"Error processing page {page}: {str(e)}")
                    break
                    
        except Exception as e:
            print(f"Error in _scrape_vietnamnet: {str(e)}")
        
        return articles[:quantity]

    def _is_today(self, date_str):
        """Check if given date is today"""
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            return date == datetime.now().date()
        except Exception:
            return False

    def _scrape_nguoiduatin(self, url, quantity):
    
        # Mở và phân tích trang web
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, 'html.parser')

        # Tìm tất cả các thẻ <div> chứa bài viết
        div_all = soup.find_all('div', attrs={'class': 'list__tc'})+ \
                  soup.find_all('div', attrs={'class':'list__news-up cate'})
        # print(div_all)
        # Lấy các thẻ <h3> trong các <div> này
        h3_all = []
        for div in div_all:
            h3_all.extend(div.find_all('div', attrs={'class': 'box-category-content'}))

        articles = []  # Danh sách kết quả bài viết
        for h3 in h3_all:
            if len(articles) >= quantity:  # Dừng nếu đạt số lượng yêu cầu
                break

            try:
                # Tìm thẻ <a> chứa tiêu đề và liên kết
                link_elem = h3.find('a')
                if not link_elem:
                    continue

                title = link_elem.get('title')
                link = link_elem.get('href')

                # Chuyển liên kết sang dạng đầy đủ
                if link and not link.startswith('http'):
                    link = 'https://nguoiduatin.vn' + link

                # Tìm phần mô tả (nếu có)
                desc_elem = h3.find('p')  # Giả sử mô tả là thẻ <p> tiếp theo
                description = desc_elem.text.strip() if desc_elem else ''

                # Tìm ngày đăng (nếu có)
                date_elem = h3.find_next('span', class_='time')  # Giả sử ngày trong thẻ <span class="time">
                date = date_elem.text.strip() if date_elem else ''

                # Lưu bài viết vào danh sách
                if title and link:
                    articles.append({
                        'title': title,
                        'description': description,
                        'link': link,
                        'date': date,
                        'source': 'Người Đưa Tin'
                    })

            except Exception as e:
                print(f"Error parsing article: {str(e)}")
                continue

        return articles
    
    def _scrape_dantri(self, url, quantity):
    
        # Mở và phân tích trang web
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, 'html.parser')

        # Tìm tất cả các thẻ <div> chứa bài viết
        div_all = soup.find_all('div', attrs={'class': 'grid list'})+ \
                  soup.find_all('div', attrs={'class': 'grid highlight' })+ \
                  soup.find_all('div', attrs={'class': 'grid row three'})
        # Lấy các thẻ <h3> trong các <div> này
        h3_all = []
        for div in div_all:
            h3_all.extend(div.find_all('article', attrs={'class': 'article-item'}))

        articles = []  # Danh sách kết quả bài viết
        for h3 in h3_all:
            if len(articles) >= quantity:  # Dừng nếu đạt số lượng yêu cầu
                break

            try:
                # Tìm thẻ <a> chứa tiêu đề và liên kết
                link_elem = h3.find('h3').find('a')
                if not link_elem:
                    continue

                title = link_elem.text.strip()
                link = link_elem.get('href')

                # Chuyển liên kết sang dạng đầy đủ
                if link and not link.startswith('http'):
                    link = 'https://dantri.com.vn' + link

                # Tìm phần mô tả (nếu có)
                desc_elem = h3.find_next_sibling('p')  # Giả sử mô tả là thẻ <p> tiếp theo
                # desc_elem = h3.find('div', attrs={'class': 'article-excerpt'}).find('a') 
                description = desc_elem.text.strip() if desc_elem else ''

                # Tìm ngày đăng (nếu có)
                date_elem = h3.find_next('span', class_='time')  # Giả sử ngày trong thẻ <span class="time">
                date = date_elem.text.strip() if date_elem else ''

                # Lưu bài viết vào danh sách
                if title and link:
                    articles.append({
                        'title': title,
                        'description': description,
                        'link': link,
                        'date': date,
                        'source': 'Dân Trí'
                    })

            except Exception as e:
                print(f"Error parsing article: {str(e)}")
                continue

        return articles
    
    def _scrape_tienphong(self, url, quantity):
    
        # Mở và phân tích trang web
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, 'html.parser')

        # Tìm tất cả các thẻ <div> chứa bài viết
        div_all = soup.find_all('div', attrs={'class': 'site-body'})
        # Lấy các thẻ <h3> trong các <div> này
        h3_all = []
        for div in div_all:
            h3_all.extend(div.find_all('article', attrs={'class': 'story'}))

        articles = []  # Danh sách kết quả bài viết
        for h3 in h3_all:
            if len(articles) >= quantity:  # Dừng nếu đạt số lượng yêu cầu
                break

            try:
                # Tìm thẻ <a> chứa tiêu đề và liên kết
                link_elem = h3.find('a')
                if not link_elem:
                    continue

                title = link_elem.get('title')
                link = link_elem.get('href')

                # Chuyển liên kết sang dạng đầy đủ
                if link and not link.startswith('http'):
                    link = 'https://tienphong.vn' + link

                # Tìm phần mô tả (nếu có)
                desc_elem = h3.find('div', attrs={'class': 'story__summary'})  # Giả sử mô tả là thẻ <p> tiếp theo
                description = desc_elem.text.strip() if desc_elem else ''

                # Tìm ngày đăng (nếu có)
                date_elem = h3.find_next('span', class_='time')  # Giả sử ngày trong thẻ <span class="time">
                date = date_elem.text.strip() if date_elem else ''

                # Lưu bài viết vào danh sách
                if title and link:
                    articles.append({
                        'title': title,
                        'description': description,
                        'link': link,
                        'date': date,
                        'source': 'Tiền Phong'
                    })

            except Exception as e:
                print(f"Error parsing article: {str(e)}")
                continue

        return articles
    
    def _scrape_baoquocte(self, url, quantity):
    
        # Mở và phân tích trang web
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, 'html.parser')

        # Tìm tất cả các thẻ <div> chứa bài viết
        div_all = soup.find_all('div', attrs={'class': 'bx-list-left lt'})
        # print(div_all)
        # Lấy các thẻ <h3> trong các <div> này
        h3_all = []
        for div in div_all:
            h3_all.extend(div.find_all('div', attrs={'class': 'article'}))
        print(h3_all)

        articles = []  # Danh sách kết quả bài viết
        for h3 in h3_all:
            if len(articles) >= quantity:  # Dừng nếu đạt số lượng yêu cầu
                break

            try:
                # Tìm thẻ <a> chứa tiêu đề và liên kết
                link_elem = h3.find('a')
                if not link_elem:
                    continue

                title = link_elem.get('title')
                link = link_elem.get('href')

                # Chuyển liên kết sang dạng đầy đủ
                if link and not link.startswith('http'):
                    link = 'https://baoquocte.vn' + link

                # Tìm phần mô tả (nếu có)
                desc_elem = h3.find('div', attrs={'class': 'article-desc'})  # Giả sử mô tả là thẻ <p> tiếp theo
                description = desc_elem.text.strip() if desc_elem else ''

                # Tìm ngày đăng (nếu có)
                date_elem = h3.find_next('span', class_='time')  # Giả sử ngày trong thẻ <span class="time">
                date = date_elem.text.strip() if date_elem else ''

                # Lưu bài viết vào danh sách
                if title and link:
                    articles.append({
                        'title': title,
                        'description': description,
                        'link': link,
                        'date': date,
                        'source': 'Thế giới và Việt Nam'
                    })

            except Exception as e:
                print(f"Error parsing article: {str(e)}")
                continue

        return articles
    
    def _scrape_baotintuc(self, url, quantity):
    
        # Mở và phân tích trang web
        result = subprocess.run(
            ["curl", "-k", url], capture_output=True
        )
        
        # Kiểm tra xem lệnh có chạy thành công không
        if result.returncode != 0:
            print(f"Error fetching page: {result.stderr.decode('utf-8', errors='ignore')}")
            return []

        # Giải mã dữ liệu đầu ra thành chuỗi, bỏ qua các ký tự không hợp lệ
        output = result.stdout.decode('utf-8', errors='ignore')

        # Phân tích nội dung trang với BeautifulSoup
        soup = BeautifulSoup(output, 'html.parser')

        # Tìm tất cả các thẻ <div> chứa bài viết
        div_all = soup.find_all('div', attrs={'class': 'list-content w1040'})
        # print(div_all)
        # Lấy các thẻ <h3> trong các <div> này
        h3_all = []
        for div in div_all:
            h3_all.extend(div.find_all('div', attrs={'id': 'plhMain_ctl00_divFocus'}))
            h3_all.extend(div.find_all('li', attrs={'class': 'item'}))
            h3_all.extend(div.find_all('li', attrs={'class': 'boxnews-item'}))
        print(h3_all)

        articles = []  # Danh sách kết quả bài viết
        for h3 in h3_all:
            if len(articles) >= quantity:  # Dừng nếu đạt số lượng yêu cầu
                break

            try:
                # Tìm thẻ <a> chứa tiêu đề và liên kết
                link_elem = h3.find('a')
                if not link_elem:
                    continue

                title = link_elem.get('title')
                link = link_elem.get('href')

                # Chuyển liên kết sang dạng đầy đủ
                if link and not link.startswith('http'):
                    link = 'https://baotintuc.vn' + link

                # Tìm phần mô tả (nếu có)
                desc_elem = h3.find('p', attrs={'class': 'des'})  # Giả sử mô tả là thẻ <p> tiếp theo
                description = desc_elem.text.strip() if desc_elem else ''

                # Tìm ngày đăng (nếu có)
                date_elem = h3.find_next('span', class_='time')  # Giả sử ngày trong thẻ <span class="time">
                date = date_elem.text.strip() if date_elem else ''

                # Lưu bài viết vào danh sách
                if title and link:
                    articles.append({
                        'title': title,
                        'description': description,
                        'link': link,
                        'date': date,
                        'source': 'Thông tấn xã Việt Nam'
                    })

            except Exception as e:
                print(f"Error parsing article: {str(e)}")
                continue

        return articles

    def _get_base_url(self, source: str, topic: str):  
        """Get base URL for given source and topic"""
        urls = {
            'VnExpress': {
                'Thời sự': 'https://vnexpress.net/thoi-su',
                'Kinh doanh': 'https://vnexpress.net/kinh-doanh',
                'Thể thao': 'https://vnexpress.net/the-thao',
                'Giải trí': 'https://vnexpress.net/giai-tri',
                'Giáo dục': 'https://vnexpress.net/giao-duc',
                'Sức khỏe': 'https://vnexpress.net/suc-khoe'
            },
            'Thanh Niên': {
                'Thời sự': 'https://thanhnien.vn/thoi-su.htm',
                'Kinh doanh': 'https://thanhnien.vn/kinh-te.htm',
                'Thể thao': 'https://thanhnien.vn/the-thao.htm',
                'Giải trí': 'https://thanhnien.vn/giai-tri.htm', 
                'Giáo dục': 'https://thanhnien.vn/giao-duc.htm',
                'Sức khỏe': 'https://thanhnien.vn/suc-khoe.htm'
            },
            'VietnamNet': {
                'Thời sự': 'https://vietnamnet.vn/thoi-su',
                'Kinh doanh': 'https://vietnamnet.vn/kinh-doanh',
                'Thể thao': 'https://vietnamnet.vn/the-thao',
                'Giải trí': 'https://vietnamnet.vn/giai-tri', 
                'Giáo dục': 'https://vietnamnet.vn/giao-duc',
                'Sức khỏe': 'https://vietnamnet.vn/suc-khoe'
            },
            'Người Đưa Tin': {
                'Thời sự': 'https://www.nguoiduatin.vn/toan-canh.htm',
                'Kinh doanh': 'https://nguoiduatin.vn/kinh-te.htm',
                'Thể thao': 'https://www.nguoiduatin.vn/van-hoa/the-thao.htm',
                'Giải trí': 'https://www.nguoiduatin.vn/van-hoa/giai-tri.htm', 
                'Giáo dục': 'https://nguoiduatin.vn/xa-hoi/giao-duc.htm',
                'Sức khỏe': 'https://nguoiduatin.vn/doi-song/suc-khoe.htm'
            },
            'Dân Trí': {
                'Thời sự': 'https://dantri.com.vn/xa-hoi.htm',
                'Kinh doanh': 'https://dantri.com.vn/kinh-doanh.htm',
                'Thể thao': 'https://dantri.com.vn/the-thao.htm',
                'Giải trí': 'https://dantri.com.vn/giai-tri.htm', 
                'Giáo dục': 'https://dantri.com.vn/giao-duc.htm',
                'Sức khỏe': 'https://dantri.com.vn/suc-khoe.htm'
            },
            'Tiền Phong': {
                'Thời sự': 'https://tienphong.vn/xa-hoi/',
                'Kinh doanh': 'https://tienphong.vn/kinh-te/',
                'Thể thao': 'https://tienphong.vn/the-thao/',
                'Giải trí': 'https://tienphong.vn/giai-tri/', 
                'Giáo dục': 'https://tienphong.vn/giao-duc/',
                'Sức khỏe': 'https://tienphong.vn/suc-khoe/'
            },
            'Thế giới và Việt Nam': {
                'Thời sự': 'https://baoquocte.vn/thoi-su',
                'Kinh doanh': 'https://baoquocte.vn/kinh-te',
                'Thể thao': 'https://baoquocte.vn/the-thao',
                'Giải trí': 'https://baoquocte.vn/giai-tri', 
                'Giáo dục': 'https://baoquocte.vn/xa-hoi/giao-duc',
                'Sức khỏe': 'https://baoquocte.vn/xa-hoi/y-te'
            },
            'Thông tấn xã Việt Nam': {
                'Thời sự': 'https://baotintuc.vn/thoi-su-472ct0.htm',
                'Kinh doanh': 'https://baotintuc.vn/kinh-te-128ct0.htm',
                'Thể thao': 'https://baotintuc.vn/the-thao-273ct0.htm',
                'Giải trí': 'https://baotintuc.vn/giai-tri-sao-274ct158.htm', 
                'Giáo dục': 'https://baotintuc.vn/giao-duc-135ct0.htm',
                'Sức khỏe': 'https://baotintuc.vn/suc-khoe-564ct0.htm'
            }
        }
        return urls.get(source, {}).get(topic, '')



if __name__ == "__main__":
    scraper = NewsScraper()
    articles = scraper.scrape_news('Tiền Phong', 'Thời sự', quantity=50)
    i = 1
    for article in articles:
        print(i)
        print(f"Title: {article['title']}")
        print(f"Link: {article['link']}")
        print(f"description: {article['description']}")
        print("---")
        i += 1