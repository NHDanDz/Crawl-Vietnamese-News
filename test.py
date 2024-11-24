from newspaper import Article
from bs4 import BeautifulSoup
import urllib.request
def crawl_by_url(url, title):
    article = Article(url, language='vi')
    article.download()
    article.parse()
    contents = str(article.text).replace("\n","")
    article.nlp()
    # replace
    char_to_replace = {':': '',
                       '/': '',
                       '\\': '',
                      '*': '',
                      '?': '',
                      '"': '',
                      '<': '',
                      '>': '',
                      '|': ''}
    for key, value in char_to_replace.items():
        # Replace key character with value character in string
        title = title.replace(key, value)

    # write txt
    # https://vnexpress.net
    if(url.find('https://vnexpress.net/') != -1):
        output = "data/text/vnexpress/" + title  + ".txt"
        f = open(output, "w+", encoding='utf-8')
        f.write(str(url)+"\n")
        f.write(title+"\n")
        f.write(contents)
        f.close()
    elif(url.find('https://thanhnien.vn/') != -1):
        output = "data/text/thanhnien/" + title  + ".txt"
        f = open(output, "w+", encoding='utf-8')
        f.write(str(url)+"\n")
        f.write(title+"\n")
        f.write(contents)
    elif(url.find('https://vietnamnet.vn/') != -1):
        output = "data/text/vietnamnet/" + title  + ".txt"
        f = open(output, "w+", encoding='utf-8')
        f.write(str(url)+"\n")
        f.write(title+"\n")
        f.write(contents)
        # VNEXPRESS
def get_links_in_page_vnexpress(url):
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    # <section>
    sections = soup.find_all('section', attrs={'class':'section section_container mt15'})
    # <h3>
    h3_all = []
    for section in sections:
        h3_all.extend(section.find_all('h3', attrs={'class':'title-news'}))
    # <a>
    a_all = []
    results = [[]]
    for h3 in h3_all:
        a_all.extend(h3.find_all('a', attrs={'class':''}))
    for a in a_all:
        title = a.get('title')
        link = a.get('href')
        print('Title: {} - Link: {}'.format(title, link))
        results.append([title,link])
    return results
# VNEXPRESS
def get_page_urls_vnexpress(base_url, quantity):
    news_per_page = 25
    if quantity % news_per_page == 0:
        no_of_pages = quantity // news_per_page
    else:
        no_of_pages = quantity // news_per_page + 1

    extend_url = ['-p{}'.format(page) for page in range(2, no_of_pages + 1)]
    url_list = [base_url + extend_part for extend_part in extend_url]
    url_list.insert(0, base_url)
    return url_list
# THANHNIEN
def get_links_in_page_thanhnien(url):
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    # <div>
    div_all = soup.find_all('div', attrs={'class':'site-content'})
    # div_all
    # <h2>
    h2_all = []
    for div in div_all:
        h2_all.extend(div.find_all('h2', attrs={'class':''}))
    # print(h2_all)
    #<a>
    a_all = []
    results = [[]]
    for h2 in h2_all:
        a_all.extend(h2.find_all('a', attrs={'class':'story__title'}))

    for a in a_all:
        title = a.get('title')
        if(a.get('href').find('video') != -1):
            pass
        else:
            link =  'https://thanhnien.vn/'+ str(a.get('href'))

        print('Title: {} - Link: {}'.format(title, link))
        results.append([title,link])
    return results
# THANHNIEN
def get_page_urls_thanhnien(base_url, quantity):
    news_per_page = 25
    if quantity % news_per_page == 0:
        no_of_pages = quantity // news_per_page
    else:
        no_of_pages = quantity // news_per_page + 1

    extend_url = ['/trang-{}.html'.format(page) for page in range(2, no_of_pages + 1)]
    url_list = [base_url + extend_part for extend_part in extend_url]
    url_list.insert(0, base_url)
    return url_list
# VIETNAMNET
def get_links_in_page_vietnamnet(url):
#     url = 'https://vietnamnet.vn/vn/thoi-su/trang5/'
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    # <div>
    div_all = soup.find_all('div', attrs={'class':'list-content list-content-loadmore lagre m-t-20 clearfix'})
    div_all

    # <h3>
    h3_all = []
    for div in div_all:
        h3_all.extend(div.find_all('h3', attrs={'class':''}))
    #<a>
    a_all = []
    results = [[]]
    for h3 in h3_all:
        a_all.extend(h3.find_all('a'))
    # print(a_all)
    for a in a_all:
        title = a.get('title')
        link =  'https://vietnamnet.vn/vn/thoi-su'+ str(a.get('href'))
        print('Title: {} - Link: {}'.format(title, link))
        results.append([title,link])
    return results
# VIETNAMNET
def get_page_urls_vietnamnet(base_url, quantity):
    news_per_page = 25
    if quantity % news_per_page == 0:
        no_of_pages = quantity // news_per_page
    else:
        no_of_pages = quantity // news_per_page + 1

    extend_url = [f'trang{page}/' for page in range(2, no_of_pages + 1)]
    url_list = [base_url + extend_part for extend_part in extend_url]
    url_list.insert(0, base_url)
    return url_list
def vnexpress(base_url):
    page_urls = get_page_urls_vnexpress(base_url, quantity=40000)
    print(page_urls)
    total_articles = 0
    for page in page_urls:
        arr = get_links_in_page_vnexpress(page)
        for i in range(1,len(arr)-1):
            title = arr[i][0]
            url = arr[i][1]
            crawl_by_url(url,title)
# base_url = 'http://vnexpress.net/thoi-su' ## category = thoi-su
def thanhnien(base_url):
    print(1)
    page_urls = get_page_urls_thanhnien(base_url, quantity=10000)

    total_articles = 0
    for page in page_urls:
        arr = get_links_in_page_thanhnien(page)
        for i in range(1,len(arr)-1):
            title = arr[i][0]
            url = arr[i][1]
            crawl_by_url(url,title)
# base_url = 'http://thanhnien.vn/thoi-su' ## category = thoi-su
def vietnamnet(base_url):
    page_urls = get_page_urls_vietnamnet(base_url, quantity=300)
#     print(page_urls)
    for page in page_urls:
        arr = get_links_in_page_vietnamnet(page)
        for i in range(1,len(arr)-1):
            title = arr[i][0]
            url = arr[i][1]
            crawl_by_url(url,title)

# base_url = 'https://vietnamnet.vn/vn/thoi-su/' ## category = thoi-su