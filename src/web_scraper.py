import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json
import random

# Define a list of user agents to randomly choose from
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
    # Add more user agents if needed
]


def get_random_headers():
    """Get random headers for the request."""
    return {'User-Agent': random.choice(USER_AGENTS)}


def save_html(content, domain):
    """Save raw HTML content to a file named after the domain."""
    filename = f"{domain}_page.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)


def is_valid_product_container(tag):
    """Determine if a tag is a valid product container."""
    return tag.name == 'div' and 'grid-product' in tag.get('class', [])


def extract_product_info(product_container, base_url):
    """Extract product information from a product container."""
    product_link_tag = product_container.select_one('.grid-product__link')
    product_name_tag = product_container.select_one('.grid-product__title--body')
    product_price_tag = product_container.select_one('.grid-product__price')

    if not product_link_tag or not product_name_tag:
        return None  # Skip if essential information is missing

    product_name = product_name_tag.get_text(strip=True)
    product_url = urljoin(base_url, product_link_tag['href'])
    product_price = product_price_tag.get_text(strip=True) if product_price_tag else "N/A"

    return {
        'name': product_name,
        'url': product_url,
        'price': product_price
    }


def scrape_products(url):
    """Scrape products from a given URL."""
    session = requests.Session()
    session.headers.update(get_random_headers())

    response = session.get(url)
    response.raise_for_status()  # Will raise an exception for HTTP errors

    soup = BeautifulSoup(response.text, 'html.parser')
    product_containers = soup.find_all('div', class_='grid-product')

    products = []
    product_html_list = []
    for container in product_containers:
        product_info = extract_product_info(container, url)
        if product_info:  # Make sure it's not None
            products.append(product_info)
            product_html_list.append(str(container))

    domain = get_domain_from_url(url)
    save_product_html(product_html_list, domain)

    return products


def save_product_html(product_html_list, domain):
    """Save the HTML content for all products to a single file."""
    html_content = '<html><body>'
    for product_html in product_html_list:
        html_content += product_html
    html_content += '</body></html>'

    filename = f"web/{domain}_products.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)


def save_to_json(data, filename):
    """Save data to a JSON file, updating the file if it already exists."""
    try:
        with open(filename, 'r+', encoding='utf-8') as f:
            existing_data = json.load(f)
            existing_data.update(data)
            f.seek(0)
            f.truncate()
            json.dump(existing_data, f, ensure_ascii=False, indent=4)
    except FileNotFoundError:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except json.JSONDecodeError:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


def get_domain_from_url(url):
    """Extract the domain name from the given URL."""
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    if domain.startswith('www.'):
        domain = domain[4:]
    return domain


def scrape_site(url, json_filename):
    """Scrape products from a single URL and update the JSON file."""
    domain = get_domain_from_url(url)
    print(f"Scraping products from {domain}")
    products = scrape_products(url)
    if products:
        print(f"Found {len(products)} products.")
        save_to_json({domain: products}, json_filename)
        print(f"Updated {json_filename} with products from {domain}.")
    else:
        print(f"No products found at {url}.")


# List of URLs to scrape
urls_to_scrape = [
    f'https://mlreng.com/collections/all?limit=200'
    # ...add more URLs as needed
]

# File to save the product information
json_filename = 'web/all_products.json'

# Scrape each site and save the results
for url in urls_to_scrape:
    scrape_site(url, json_filename)

