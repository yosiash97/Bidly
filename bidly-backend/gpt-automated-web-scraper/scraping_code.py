

from bs4 import BeautifulSoup
from website_analysis.dom_analysis import HtmlLoader, UrlHtmlLoader

# Create HtmlLoader or UrlHtmlLoader based on the source type
def create_html_loader(source, source_type):
    if source_type == 'url':
        return UrlHtmlLoader(source)
    else:  # source_type == 'file'
        return HtmlLoader(source)

html_loader = create_html_loader("https://www.cityofsancarlos.org/business/bids_and_proposals/call_for_bids_rfpsrfqs.php", "url")
response = html_loader.load()

html_soup = BeautifulSoup(response, 'html.parser')
    
# Find all table rows
table_rows = html_soup.find_all('tr')

# Initialize an empty list to store the data
data = []

# List of keywords to search for
keywords = ['safety', 'transportation', 'bridge', 'bike lane', 'pedestrian', 'safe', 'crossings', 'railroad', 'car']

# Loop through each table row
for row in table_rows:
    # Find all anchor tags in the row
    anchors = row.find_all('a')
    # Loop through each anchor tag
    for anchor in anchors:
        # Check if the anchor tag's text contains any of the keywords
        if any(keyword in anchor.text.lower() for keyword in keywords):
            # If so, append the anchor tag's href attribute to the data list
            data.append({
                'name': anchor.text,
                'link': anchor['href']
            })

# Print the data as a JSON string
import json
print(json.dumps(data, indent=4))
        