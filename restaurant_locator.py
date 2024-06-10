import pandas as pd
import requests
import googlemaps
import os


api_key = os.environ.get("GOOGLE_MAP_API_KEY")
# Load your CSV
df = pd.read_csv("C:/Users/ncare/pizza/scraped_data_may24.csv")

# Initialize Google Maps API client
gmaps = googlemaps.Client(key=api_key)

# Function to get the address
def get_address(name, city, state):
    geocode_result = gmaps.geocode(f"{name}, {city}, {state}")
    if geocode_result:
        return geocode_result[0]['formatted_address']
    return None

# Apply the function to get addresses
df['Address'] = df.apply(lambda row: get_address(row['Name'], row['City'], row['State']), axis=1)


# Save the updated DataFrame to a new CSV
df.to_csv('all_pizza_restaurants_with_addresses.csv', index=False)
