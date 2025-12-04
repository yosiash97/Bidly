

from bs4 import BeautifulSoup
from website_analysis.dom_analysis import HtmlLoader, UrlHtmlLoader

# Create HtmlLoader or UrlHtmlLoader based on the source type
def create_html_loader(source, source_type):
    if source_type == 'url':
        return UrlHtmlLoader(source)
    else:  # source_type == 'file'
        return HtmlLoader(source)

html_loader = create_html_loader("https://procurement.opengov.com/portal/palo-alto-ca?departmentId=4697&status=all", "url")
response = html_loader.load()

html_soup = BeautifulSoup(response, 'html.parser')
    
# Continue from your code

# Find divs that contains the required information
info_divs = html_soup.find_all('div', class_="rt-td _1lNEVuDlslMqIiKuxGxMFQ")

data = []

# Extract the required information
for div in info_divs:
    info = {}
    info['title'] = div.find('a', class_="HVdDLVUy-wCXAPUhHi0bc").text
    info['status'] = div.find('span', class_="_24r-rpb07lKxiE5O2a6ub5 label label-primary").text
    data.append(info)

# Print the information in JSON format
import json
print(json.dumps(data, indent=4))
        