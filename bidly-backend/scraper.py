import sys
import json
import os
from selenium import webdriver
import requests
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from geopy.geocoders import Nominatim
from bs4 import BeautifulSoup
from scrapeghost import SchemaScraper
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
from datetime import date

# Environment variables (OPENAI_API_KEY) should be passed from Node.js
# No need to load from .env file

# Schema definition
schema = {
    "title": "string",
    "url": "url",
    "Date": "string",
    "Status": "string",
}

def is_date_after_today(date_str):
    date_formats = [
        '%m-%d-%Y',
        '%m/%d/%Y'
    ]
    date_obj = None
    date_str = date_str.split(" ")[0]
    
    for date_format in date_formats:
        try:
            date_obj = datetime.strptime(date_str, date_format).date()
            break
        except ValueError as e:
            continue

    if date_obj is None:
        return False  # If no format succeeded, return False

    today = date.today()
    return date_obj > today

def parse_react_table(soup):
    react_table = soup.select_one("div.ReactTable")
    if not react_table:
        sys.stderr.write("ReactTable not found in the HTML\n")
        return []

    data = []
    rows = react_table.find_all("div", class_="rt-tr-group")
    for row in rows:
        row_data = []
        cells = row.find_all("div", class_="rt-td")
        for cell in cells:
            cell_text = cell.get_text(strip=True)
            row_data.append(cell_text)
        if row_data:
            data.append(row_data)

    return data

def is_date_after_today(date_str):
    date_formats = ['%Y-%m-%d', '%d-%m-%Y', '%m/%d/%Y', '%m/%d/%Y %I:%M %p']  # Add any other date formats you want to try
    date_obj = None
    
    for date_format in date_formats:
        try:
            date_obj = datetime.strptime(date_str, date_format)
            break  # If parsing succeeds, exit the loop
        except ValueError:
            continue  # If parsing fails, try the next format

    if date_obj is None:
        return False  # If no format succeeded, return False

    # Get today's date
    today = datetime.now()
    
    # Check if the date is after today
    return date_obj > today
    


def parse_list_group(soup):
    list_groups = soup.find_all('div', class_='listGroupWrapper clearfix')

    if not list_groups:
        sys.stderr.write("List Group Wrapper not found in the HTML\n")
        return []
    
    data = []

    for group in list_groups:
        row_data = []
        anchors = group.find_all("a", class_="mw-75 text-truncate")
        for anchor in anchors:
            cell_text = anchor.get_text(strip=True)
            cell_href = anchor.get('href')
            row_data.append({'text': cell_text, 'url': cell_href})
        if row_data:
            data.append(row_data)

    return data

def parse_planet_bids(soup):
    rows = soup.select('tbody[role="rowgroup"] > tr')
    if not rows:
        sys.stderr.write("Planet Bids Table not found in the HTML\n")
        return []

    data = []
    for row in rows:
        row_data = []
        cells = row.find_all("div", class_="rt-td")
        for cell in cells:
            cell_text = cell.get_text(strip=True)
            row_data.append(cell_text)
        if row_data:
            data.append(row_data)

    return data

def parse_ember_table(soup):
    """Parse Ember.js datatable structures"""
    import re
    data = []

    # Look for Ember table rows
    rows = soup.find_all('tr', class_=re.compile(r'ember|row'))

    if not rows:
        # Try alternative: look for table with pb-datatable class
        table = soup.find('table', class_=re.compile(r'pb-datatable|datatable'))
        if table:
            tbody = table.find('tbody')
            if tbody:
                rows = tbody.find_all('tr')

    for row in rows:
        # Skip header rows
        if row.find('th'):
            continue

        cells = row.find_all('td')
        if cells:
            row_data = {}
            for i, cell in enumerate(cells):
                # Get text content
                cell_text = cell.get_text(strip=True)
                # Get links if any
                link = cell.find('a')
                if link and link.get('href'):
                    row_data[f'column_{i}'] = {'text': cell_text, 'url': link.get('href')}
                else:
                    row_data[f'column_{i}'] = cell_text

            if row_data:
                data.append(row_data)

    return data

def parse_standard_table(soup):
    """Parse standard HTML tables with thead, tbody, tr, td structure"""
    tables = soup.find_all('table')
    all_table_data = []

    for table in tables:
        # Get headers
        headers = []
        thead = table.find('thead')
        if thead:
            header_row = thead.find('tr')
            if header_row:
                headers = [th.get_text(strip=True) for th in header_row.find_all(['th', 'td'])]

        # Get rows
        tbody = table.find('tbody') or table
        rows = tbody.find_all('tr')

        table_data = []
        for row in rows:
            cells = row.find_all(['td', 'th'])
            if cells:
                row_data = {}
                for i, cell in enumerate(cells):
                    # Get cell text
                    cell_text = cell.get_text(strip=True)
                    # Get links if any
                    link = cell.find('a')
                    if link and link.get('href'):
                        cell_text = {'text': cell_text, 'url': link.get('href')}

                    header = headers[i] if i < len(headers) and headers else f"Column_{i}"
                    row_data[header] = cell_text

                if row_data:
                    table_data.append(row_data)

        if table_data:
            all_table_data.extend(table_data)

    return all_table_data

def parse_simple_list(soup):
    """Parse simple unordered lists (ul/li) with links"""
    import re
    data = []
    # Find all ul elements
    lists = soup.find_all('ul')

    for ul in lists:
        items = ul.find_all('li', recursive=False)
        for item in items:
            # Get the first link in the list item
            link = item.find('a')
            if link:
                title = link.get_text(strip=True)
                url = link.get('href', '')

                # Try to find date in the list item text
                item_text = item.get_text()
                date_match = None

                # Look for common date patterns
                date_patterns = [
                    r'Posting Date:\s*(\d{1,2}-\d{1,2}-\d{4})',
                    r'Due Date:\s*(\d{1,2}/\d{1,2}/\d{4})',
                    r'(\d{1,2}/\d{1,2}/\d{4})',
                    r'(\d{1,2}-\d{1,2}-\d{4})'
                ]

                for pattern in date_patterns:
                    match = re.search(pattern, item_text)
                    if match:
                        date_match = match.group(1)
                        break

                if title:  # Only add if there's a title
                    data.append({
                        'text': title,
                        'url': url,
                        'date': date_match if date_match else ''
                    })

    return data

def parse_card_layout(soup):
    """Parse card-based bid listings (like Union City format)"""
    import re
    data = []

    # Find all bid cards - looking for divs with bid-related content
    # Try multiple selectors to find the card containers
    cards = soup.find_all('div', class_=re.compile(r'bid|opportunity|rfp|card', re.IGNORECASE))

    # Also try finding divs that contain both a link and status/date info
    if not cards:
        # Find all divs that might be bid containers
        all_divs = soup.find_all('div')
        cards = [div for div in all_divs if div.find('a') and
                (re.search(r'Status:|Closes:|Bid\s*No', div.get_text(), re.IGNORECASE))]

    for card in cards:
        # Find the main title link
        title_link = card.find('a', href=True)
        if not title_link:
            continue

        title = title_link.get_text(strip=True)
        url = title_link.get('href', '')

        # Skip if title is too short or generic
        if len(title) < 10 or title.lower() in ['read on', 'more', 'details', 'view']:
            continue

        card_text = card.get_text()

        # Look for status
        status_match = re.search(r'Status:\s*(\w+)', card_text, re.IGNORECASE)
        status = status_match.group(1) if status_match else ''

        # Look for closing/due date
        date_match = None
        date_patterns = [
            r'Closes?:\s*(\d{1,2}/\d{1,2}/\d{4}(?:\s+\d{1,2}:\d{2}\s*(?:AM|PM)?)?)',
            r'Due Date:\s*(\d{1,2}/\d{1,2}/\d{4}(?:\s+\d{1,2}:\d{2}\s*(?:AM|PM)?)?)',
            r'Closing Date:\s*(\d{1,2}/\d{1,2}/\d{4}(?:\s+\d{1,2}:\d{2}\s*(?:AM|PM)?)?)',
            r'(\d{1,2}/\d{1,2}/\d{4}\s+\d{1,2}:\d{2}\s*(?:AM|PM))'
        ]

        for pattern in date_patterns:
            match = re.search(pattern, card_text, re.IGNORECASE)
            if match:
                date_match = match.group(1)
                break

        # Look for bid number
        bid_no_match = re.search(r'Bid\s*(?:No\.?|#|Number)[:.]?\s*([\w-]+)', card_text, re.IGNORECASE)

        # Only add if we found meaningful information
        if title and (date_match or status):
            entry = {
                'text': title,
                'url': url,
                'date': date_match if date_match else '',
                'status': status
            }
            if bid_no_match:
                entry['bid_number'] = bid_no_match.group(1)

            # Avoid duplicates
            if entry not in data:
                data.append(entry)

    return data

def parse_generic_bids(soup):
    """Parse generic bid listings by looking for common patterns"""
    import re
    data = []

    # First try card layout
    card_data = parse_card_layout(soup)
    if card_data:
        return card_data

    # Find all links on the page
    links = soup.find_all('a', href=True)

    for link in links:
        # Get parent container (could be div, li, td, etc.)
        parent = link.parent
        if not parent:
            continue

        # Get all text from parent container
        parent_text = parent.get_text(strip=False)
        title = link.get_text(strip=True)

        # Skip if title is too short or generic
        if len(title) < 10 or title.lower() in ['read on', 'more', 'details', 'view']:
            continue

        # Look for status (Open, Closed, etc.)
        status_match = re.search(r'Status:\s*(\w+)', parent_text, re.IGNORECASE)
        status = status_match.group(1) if status_match else ''

        # Look for closing/due date patterns
        date_match = None
        date_patterns = [
            r'Closes?:\s*(\d{1,2}/\d{1,2}/\d{4}(?:\s+\d{1,2}:\d{2}\s*(?:AM|PM)?)?)',
            r'Due Date:\s*(\d{1,2}/\d{1,2}/\d{4}(?:\s+\d{1,2}:\d{2}\s*(?:AM|PM)?)?)',
            r'Closing Date:\s*(\d{1,2}/\d{1,2}/\d{4}(?:\s+\d{1,2}:\d{2}\s*(?:AM|PM)?)?)',
            r'(\d{1,2}/\d{1,2}/\d{4}\s+\d{1,2}:\d{2}\s*(?:AM|PM))'
        ]

        for pattern in date_patterns:
            match = re.search(pattern, parent_text, re.IGNORECASE)
            if match:
                date_match = match.group(1)
                break

        # Look for bid number
        bid_no_match = re.search(r'Bid\s*(?:No\.?|#|Number)[:.]?\s*([\w-]+)', parent_text, re.IGNORECASE)

        # Only add if we found meaningful information
        if title and (date_match or status):
            entry = {
                'text': title,
                'url': link.get('href', ''),
                'date': date_match if date_match else '',
                'status': status
            }
            if bid_no_match:
                entry['bid_number'] = bid_no_match.group(1)

            # Avoid duplicates
            if entry not in data:
                data.append(entry)

    return data

def preprocess_html(html):
    soup = BeautifulSoup(html, "lxml")

    # Collect data from traditional tables
    new_soup = BeautifulSoup("", "lxml")

    # Parse standard HTML tables
    standard_table_data = parse_standard_table(soup)

    # Collect data from React tables
    react_table_data = parse_react_table(soup)
    list_group_data = parse_list_group(soup)
    planet_bids_data = parse_planet_bids(soup)
    ember_table_data = parse_ember_table(soup)
    simple_list_data = parse_simple_list(soup)
    generic_bids_data = parse_generic_bids(soup)

    if react_table_data:
        react_table_str = json.dumps(react_table_data, indent=4)
        new_soup.append(BeautifulSoup(f"<pre>{react_table_str}</pre>", "lxml"))
    elif list_group_data:
        list_group_str = json.dumps(list_group_data, indent=4)
        new_soup.append(BeautifulSoup(f"<pre>{list_group_str}</pre>", "lxml"))
    elif planet_bids_data:
        planet_bids_str = json.dumps(planet_bids_data, indent=4)
        new_soup.append(BeautifulSoup(f"<pre>{planet_bids_str}</pre>", "lxml"))
    elif ember_table_data:
        # Use Ember.js table data
        ember_table_str = json.dumps(ember_table_data, indent=4)
        new_soup.append(BeautifulSoup(f"<pre>{ember_table_str}</pre>", "lxml"))
    elif standard_table_data:
        # Use standard table data if no other format was found
        standard_table_str = json.dumps(standard_table_data, indent=4)
        new_soup.append(BeautifulSoup(f"<pre>{standard_table_str}</pre>", "lxml"))
    elif simple_list_data:
        # Use simple list data as fallback
        simple_list_str = json.dumps(simple_list_data, indent=4)
        new_soup.append(BeautifulSoup(f"<pre>{simple_list_str}</pre>", "lxml"))
    elif generic_bids_data:
        # Use generic bid parser as final fallback
        generic_bids_str = json.dumps(generic_bids_data, indent=4)
        new_soup.append(BeautifulSoup(f"<pre>{generic_bids_str}</pre>", "lxml"))

    return str(new_soup)

def fetch_page_with_selenium(url):
    options = Options()
    options.add_argument("--headless=new")  # Use new headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get(url)
    html = ""
    try:
        # First try to wait for React table
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.ReactTable div.rt-table div.rt-tbody div.rt-tr-group"))
        )
        html = driver.page_source
    except Exception as e:
        # If no React table, try waiting for standard HTML table
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table"))
            )
            # Give it extra time for dynamic content to load
            import time
            time.sleep(2)
            html = driver.page_source
        except Exception as e2:
            sys.stderr.write("Timeout waiting for table to load\n")
            # Still get the page source as last resort
            import time
            time.sleep(3)
            html = driver.page_source
    finally:
        driver.quit()

    return html

def main(url, city):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36 Vivaldi/5.3.2679.70."
    }
    try:
        # First try with simple requests (faster and works for most sites)
        try:
            response_check = requests.get(url, headers=headers, timeout=10)
            if response_check.status_code == 200:
                html = response_check.text
                # Check if the HTML has enough content
                soup_check = BeautifulSoup(html, "lxml")
                # If we find tables, React tables, or iframes, we have content
                if soup_check.find('table') or soup_check.find('div', class_='ReactTable') or soup_check.find('iframe'):
                    # Content found, use this HTML
                    pass
                else:
                    # No content found, might need Selenium for dynamic loading
                    raise Exception("No tables found, trying Selenium")
            else:
                raise Exception(f"Request failed with status {response_check.status_code}")
        except Exception as e:
            sys.stderr.write(f"Requests failed or no content found, trying Selenium: {str(e)}\n")
            html = fetch_page_with_selenium(url)

        # Check for iframes and extract their src URLs
        soup = BeautifulSoup(html, "lxml")
        iframes = soup.find_all('iframe', src=True)

        # Filter iframes - prioritize procurement/bid platforms, skip tracking/storage
        content_iframes = []
        priority_iframes = []
        skip_domains = ['googletagmanager', 'google-analytics', 'analytics', 'doubleclick',
                       'facebook', 'twitter', 'storage.html', 'rlets.com']
        priority_domains = ['procurement', 'opengov', 'planetbids', 'bidnet', 'publicsurplus',
                           'questcdn', 'civicplus', 'demandstar']

        for iframe in iframes:
            iframe_src = iframe.get('src', '')
            # Skip tracking/storage iframes
            if any(domain in iframe_src.lower() for domain in skip_domains):
                continue

            # Prioritize known procurement platforms
            if any(domain in iframe_src.lower() for domain in priority_domains):
                priority_iframes.append(iframe)
            else:
                content_iframes.append(iframe)

        # Use priority iframes first, then other content iframes
        final_iframes = priority_iframes + content_iframes

        # If content iframe found, scrape the iframe content instead
        if final_iframes:
            iframe_src = final_iframes[0].get('src')
            # Convert relative iframe URLs to absolute
            from urllib.parse import urljoin
            iframe_url = urljoin(url, iframe_src)
            sys.stderr.write(f"Found content iframe, scraping from: {iframe_url}\n")

            try:
                html = fetch_page_with_selenium(iframe_url)
            except Exception as e:
                sys.stderr.write(f"Selenium failed for iframe, trying requests...")
                response_check = requests.get(iframe_url, headers=headers)
                if response_check.status_code == 200:
                    html = response_check.text

        cleaned_html = preprocess_html(html)

        geolocator = Nominatim(user_agent="bidly")
        episode_scraper = SchemaScraper(
            schema,
            models=["gpt-4"],
            auto_split_length=3000,
            extra_instructions=[
                "Include any Bid or Request for Proposal that has to do with Civil Engineering or Construction, make sure the bid date/closing date/due date is after today's date. If there are two dates for the same bid choose the latest one. For the URL part, copy the link address directly from the page to construct the full URL.",
            ],
        )

        response = episode_scraper(cleaned_html)

        civil_engineering_topics = [
            'extension', 'design', 'structural', 'roadway', 'pavement', 'asphalt',
            'affordable', 'street', 'cannabis', 'coding', 'recycled',
            'transportation', 'bike', 'bicycle', 'lane', 'sidewalk', 'pedestrian',
            'safety', 'bridge', 'car', 'road', 'traffic', 'avenue', 'route',
            'car-free', 'streets'
        ]
        construction_topics = [
            'construction', 'building', 'contractor', 'subcontractor',
            'infrastructure', 'foundation', 'framework', 'materials', 'renovation',
            'restoration', 'installation', 'fabrication', 'erection', 'commissioning',
            'demolition', 'excavation', 'site development', 'masonry', 'plumbing',
            'electrical', 'hvac', 'finishing', 'landscaping', 'project management',
            'quality control', 'safety management', 'bidding', 'cost estimate',
            'timeline', 'scheduling'
        ]
        structural_topics = [
            'structural', 'loads', 'stress', 'reinforcement', 'concrete', 'steel',
            'timber', 'composites', 'seismic', 'wind', 'foundations', 'walls',
            'dynamics', 'codes', 'modeling', 'simulation', 'monitoring', 'forensics',
            'failure', 'bridges', 'high-rises', 'earthquake', 'trusses', 'beams',
            'columns', 'slabs', 'frames', 'connections'
        ]

        cleaned_response = []
        
        for each in response.data:
            has_date = bool(each['Date'])
            bid_url = each.get('url', '')
            has_url = bool(bid_url) and bid_url.lower() not in ['url', 'undefined', 'null', 'n/a', 'none']
            status = each.get('Status', '').lower()

            # Skip closed bids
            if status == 'closed':
                continue

            # Skip bids without valid URLs
            if not has_url:
                continue

            if has_date and is_date_after_today(each['Date']):
                title_to_check = each['title'].lower()
                contains_civil_engineering_topics = any(topic in title_to_check for topic in civil_engineering_topics)
                contains_construction_topics = any(topic in title_to_check for topic in construction_topics)
                contains_structural_topics = any(topic in title_to_check for topic in structural_topics)

                if contains_civil_engineering_topics or contains_construction_topics:
                    city_and_state = city + " CA"
                    location = geolocator.geocode(city_and_state)
                    if location:
                        each['geo_location'] = (location.latitude, location.longitude)
                        each['city'] = city
                        if contains_construction_topics:
                            each['bid_type'] = "construction"
                        elif contains_civil_engineering_topics:
                            each['bid_type'] = "civil_engineering"
                        else:
                            each['bid_type'] = "structural_engineering"
                    if not location:
                        each['geo_location'] = (39.7886111, -82.6418883)

                    # Convert relative URLs to absolute URLs
                    bid_url = each.get('url', '')
                    if bid_url and 'http' not in bid_url:
                        # Parse the base URL to get the domain
                        from urllib.parse import urljoin
                        each['url'] = urljoin(url, bid_url)
                    elif not bid_url:
                        # If no URL provided, use the base page URL
                        each['url'] = url

                    cleaned_response.append(each)

            # Print only the final processed data as JSON
        print(json.dumps(cleaned_response, indent=4))
    except Exception as e:
        sys.stderr.write(f"Couldn't scrape -> {city}\n")
        sys.stderr.write(f"Error: {e}\n")
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.stderr.write("Usage: python scraper.py <URL> <City>\n")
        sys.exit(1)
    url = sys.argv[1]
    city = sys.argv[2]
    main(url, city)