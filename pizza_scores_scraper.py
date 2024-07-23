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
url = 'https://onebite.app/reviews/dave?page='

# Open the URL using Selenium
driver.get(url+str(1))

# Allow some time for the JavaScript to load
import time
time.sleep(5)

# Lists to store the scraped data
names = []
timestamps = []
scores = []
locations = []
urls = []

def scrape_page():
    try:
        # Find the elements containing the data
        review_cards = driver.find_elements(By.CSS_SELECTOR, "div.jsx-2994838533.col.col--review")
        #review_cards= driver.find_elements(By.CSS_SELECTOR, "div.jsx-2655995184.reviewCard.reviewCard--feedItem")

        
        print(f"Found {len(review_cards)} review cards on this page.")

        for card in review_cards:
            try:
                url_element = card.find_element(By.CLASS_NAME, 'jsx-2655995184').get_attribute("href")

                name_element = card.find_element(By.CLASS_NAME, "reviewCard__title")
                timestamp_element = card.find_element(By.CLASS_NAME, "userMeta__timestamp")
                location_element = card.find_element(By.CLASS_NAME, "reviewCard__location")
                score_element = card.find_element(By.CLASS_NAME, "rating__score")

                    
                name = name_element.text
                timestamp = timestamp_element.text
                location = location_element.text
                score = score_element.text
                url = url_element

                names.append(name)
                timestamps.append(timestamp)
                locations.append(location)
                scores.append(score)
                urls.append(url)

                print(f"Extracted: {name}, {timestamp}, {location}, {score}, {url}")
            except Exception as e:
                print(f"Error extracting data: {e}")
                print(card.get_attribute('innerHTML'))  # Print the inner HTML of the problematic element for debugging
                
    except Exception as e:
        print(f"Error finding review cards: {e}")


for i in range(1,60):
    driver.get(url + str(i))
    driver.implicitly_wait(3)

    scrape_page()

    
# Close the web driver
driver.quit()

# Create a DataFrame to store the scraped data
data = pd.DataFrame({
    'Name': names,
    'Date': timestamps,
    'Location': locations,
    'Score:': scores,
    'Url': urls,
})

# Save the data to a CSV file
data.to_csv('dave_pizza_data_final.csv', index=False)

print("Scraping completed and data saved to 'dave_pizza_data_final.csv'")
