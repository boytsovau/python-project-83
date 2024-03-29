from urllib.parse import urlparse
from bs4 import BeautifulSoup


def get_normalized_url(url):
    if url:
        parsed_name = urlparse(url)
        normalize_url = "{0}://{1}".format(
            parsed_name.scheme,
            parsed_name.netloc
        )
    else:
        normalize_url = ''
    return normalize_url


def collect_page_data(id, http_response):
    html_content = http_response.text
    code = http_response.status_code
    soup = BeautifulSoup(html_content, 'html.parser')
    header_title = soup.find('h1').text.strip() if soup.find('h1') else ''
    title = soup.find('title').text.strip() if soup.find('title') else ''
    description = soup.find(attrs={"name": "description"})['content'].strip()\
        if soup.find(attrs={"name": "description"}) else ''
    check_record = {'url_id': id,
                    'status_code': code,
                    'h1': header_title,
                    'title': title,
                    'description': description,
                    }
    return check_record
