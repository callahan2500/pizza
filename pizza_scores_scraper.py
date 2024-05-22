from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Path to your Edge WebDriver (adjust the path as necessary)
driver_path = 'C:/Users/ncare/edgedriver_win64/msedgedriver.exe'

# Initialize the web driver
service = Service(driver_path)
options = webdriver.EdgeOptions()
options.add_argument('--headless')  # Run in headless mode for efficiency
driver = webdriver.Edge(service=service, options=options)

# URL of the website to scrape
url = 'https://onebite.app/reviews/dave'

# Open the URL using Selenium
driver.get(url)

# Allow some time for the JavaScript to load
import time
time.sleep(5)

# Lists to store the scraped data
names = []
timestamps = []
scores = []

# Function to scrape data from the current page
def scrape_page():
    # Find the elements containing the data
    review_cards = driver.find_elements(By.CSS_SELECTOR, 'div.jsx-2655995184.reviewCard__details')

    for card in review_cards:
        try:
            name = card.find_element(By.CSS_SELECTOR, 'h2.jsx-2655995184.reviewCard__title').text
            timestamp = card.find_element(By.CSS_SELECTOR, 'p.jsx-107e6328b2507bd6.userMeta__timestamp').text
            score = card.find_element(By.CSS_SELECTOR, 'p.jsx-407081529.rating__score').text

            names.append(name)
            timestamps.append(timestamp)
            scores.append(score)
        except Exception as e:
            print(f"Error extracting data: {e}")

# Scrape data from the first page
scrape_page()

# Handle pagination (example: clicking 'Next' button and scraping subsequent pages)
while True:
    try:
        # Find the 'Next' button
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.jsx-1581628325.btn.btn--next'))
        )
        
        # Click the 'Next' button
        next_button.click()
        
        # Wait for the next page to load
        time.sleep(5)
        
        # Scrape data from the new page
        scrape_page()
    except Exception as e:
        print("No more pages or error in pagination:", e)
        break

# Close the web driver
driver.quit()

# Create a DataFrame to store the scraped data
data = pd.DataFrame({
    'Name': names,
    'Timestamp': timestamps,
    'Score': scores
})

# Save the data to a CSV file
data.to_csv('portnoy_scores_overtime.csv', index=False)

print("Scraping completed and data saved to 'scraped_data.csv'")
