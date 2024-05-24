from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd


driver = webdriver.Edge()

driver.get("https://onebite.app/reviews/dave")

# Lists to store the scraped data
names = []
timestamps = []
scores = []
locations = []

def scrape_page():
    try:
        # Find the elements containing the data
        review_cards = driver.find_elements(By.CSS_SELECTOR, "div.jsx-2655995184.reviewCard.reviewCard--feedItem")
        
        print(f"Found {len(review_cards)} review cards on this page.")

        for card in review_cards:
            try:
                name_element = card.find_element(By.CLASS_NAME, "reviewCard__title")
                timestamp_element = card.find_element(By.CLASS_NAME, "userMeta__timestamp")
                location_element = card.find_element(By.CLASS_NAME, "reviewCard__location")
                score_element = card.find_element(By.CLASS_NAME, "rating__score")

                
                name = name_element.text
                timestamp = timestamp_element.text
                location = location_element.text
                score = score_element.text

                names.append(name)
                timestamps.append(timestamp)
                locations.append(location)
                scores.append(score)

                print(f"Extracted: {name}, {timestamp}, {location}")
            except Exception as e:
                print(f"Error extracting data: {e}")
                print(card.get_attribute('innerHTML'))  # Print the inner HTML of the problematic element for debugging
    except Exception as e:
        print(f"Error finding review cards: {e}")

scrape_page()

# Close the web driver
driver.quit()

# Create a DataFrame to store the scraped data
data = pd.DataFrame({
    'Name': names,
    'Timestamp': timestamps,
    'Location': locations,
    'Score': scores
})

# Save the data to a CSV file
data.to_csv('scraped_data_test.csv', index=False)

print("Scraping completed and data saved to 'scraped_data.csv'")
