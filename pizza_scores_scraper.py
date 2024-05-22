import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the website to scrape
url = 'https://www.onebitepizzarankings.com/'

# Send a GET request to the website
response = requests.get(url)
if response.status_code != 200:
    raise Exception(f"Failed to load page {url}")

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find the elements that contain the pizza rankings
# Note: You need to update the following line based on the actual structure of the website
rankings = soup.find_all('div', class_='ranking-item')

# Lists to store the scraped data
names = []
scores = []
addresses = []

# Loop through the ranking elements and extract the required data
for ranking in rankings:
    name = ranking.find('h2').text
    score = ranking.find('span', class_='score').text
    address = ranking.find('div', class_='address').text.strip()
    
    names.append(name)
    scores.append(score)
    addresses.append(address)

# Create a DataFrame to store the scraped data
data = pd.DataFrame({
    'Name': names,
    'Score': scores,
    'Address': addresses
})

# Save the data to a CSV file
data.to_csv('pizza_rankings.csv', index=False)

print("Scraping completed and data saved to 'pizza_rankings.csv'")
