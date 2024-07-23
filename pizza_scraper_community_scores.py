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
url = 'https://onebite.app/restaurant/fan-favorites?page='


names = []
locations = []
community_scores = []
dave_scores = []
review_numbers = []
score_differences = []
urls = []


def scrape_page():
    try:
        venue_list_items = driver.find_elements(By.CSS_SELECTOR, "div.jsx-1243063083.venue") #__details
        for item in venue_list_items:
            try:
                url_element = item.find_element(By.CLASS_NAME, 'jsx-1243063083').get_attribute("href")
                score_elements = item.find_elements(By.CLASS_NAME, "rating__score")
                name_element = item.find_element(By.CLASS_NAME, "venue__title")
                location_element = item.find_element(By.CLASS_NAME, "venue__address")
                number_of_review_elements = item.find_elements(By.CLASS_NAME, "venue__meta")
                
                
                if len(score_elements) != 2:
                    continue


                name = name_element.text
                location = location_element.text
                number_of_reviews = number_of_review_elements[0].text
                dave_score = score_elements[0].text
                community_score = score_elements[1].text
                score_difference = float(community_score) - float(dave_score)
                url = url_element

    
 
                names.append(name)
                locations.append(location)
                dave_scores.append(dave_score)
                community_scores.append(community_score)
                review_numbers.append(number_of_reviews)
                score_differences.append(score_difference)
                urls.append(url)


                print(f"Extracted: {name}, {location}, {dave_score}, {community_score}, {score_difference}, {url}")
                      
            except Exception as e:
                print(f"Error extracting data: {e}")
                print(item.get_attribute('innerHTML'))  # Print the inner HTML of the problematic element for debugging
    except Exception as e:
        print(f"Error finding venue list items: {e}")

#range(1,500)
for i in range(502,1001):
    driver.get(url + str(i))
    driver.implicitly_wait(4)
    scrape_page()
    
# Close the web driver
driver.quit()

# Create a DataFrame to store the scraped data
data = pd.DataFrame({
    'Name': names,
    #'Date': timestamps,
    'Location': locations,
    'Dave Score':dave_scores,
    'Community Score':community_scores,
    'Number of Reviews':review_numbers,
    'Score Diffrence':score_differences,
    'Url': urls,
})

# Save the data to a CSV file
data.to_csv('pizza_community_scores_final_2.csv', index=False)

print("Scraping completed and data saved to 'pizza_community_scores_final.csv'")
