import sys
import json
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

def preprocess_html(html):
    soup = BeautifulSoup(html, "lxml")
    tables = soup.find_all('table')
    
    # Collect data from traditional tables
    new_soup = BeautifulSoup("", "lxml")
    for table in tables:
        new_soup.append(table)

    # Collect data from React tables
    react_table_data = parse_react_table(soup)
    list_group_data = parse_list_group(soup)
    planet_bids_data = parse_planet_bids(soup)
    if react_table_data:
        react_table_str = json.dumps(react_table_data, indent=4)
        new_soup.append(BeautifulSoup(f"<pre>{react_table_str}</pre>", "lxml"))
    elif not react_table_data and list_group_data:
        list_group_str = json.dumps(list_group_data, indent=4)
        new_soup.append(BeautifulSoup(f"<pre>{list_group_str}</pre>", "lxml"))
    elif not react_table_data and not list_group_data and planet_bids_data:
        planet_bids_str = json.dumps(planet_bids_data, indent=4)
        new_soup.append(BeautifulSoup(f"<pre>{planet_bids_str}</pre>", "lxml"))


    return str(new_soup)

def fetch_page_with_selenium(url):
    options = Options()
    options.headless = True
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    driver.get(url)
    html = ""
    try:
        # Wait for the React table to be present
        WebDriverWait(driver, 45).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.ReactTable div.rt-table div.rt-tbody div.rt-tr-group"))
        )
        html = driver.page_source
    except Exception as e:
        sys.stderr.write("Timeout waiting for ReactTable to load\n")
        driver.save_screenshot("screenshot.png")  # Save a screenshot for debugging
        html = driver.page_source  # Get the page source even if there's an error
    finally:
        driver.quit()
    
    return html

def main(url, city):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36 Vivaldi/5.3.2679.70."
    }
    try:
        try: 
            html = fetch_page_with_selenium(url)
        except Exception as e:
            sys.stderr.write(f"Tried to scrape with selenium, no react table.... doing html scrape now.")
            response_check = requests.get(url, headers=headers)
        
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
            has_url = bool(each['url'])

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
                    if has_url and 'http' not in url:
                        each['url'] = url
                    if not has_url:
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