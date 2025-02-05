import pandas as pd
import re
from selenium import webdriver
from packages.selenium_setup import *
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
    
class DataCollection:
    def __init__(self, driver):
        self.driver = driver
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
    
    def get_hotel_information(self):
        '''Collects the information of the hotels in the search results.'''
        property_xpath = '//div[@data-testid="property-card-container"]'
        name_xpath = './/div[@class="f6431b446c a15b38c233"]'
        rating_xpath = './/div[@class="a3b8729ab1 d86cee9b25"]'
        price_xpath = './/span[@class="f6431b446c fbfd7c1165 e84eb96b1f"]'
        location_xpath = './/span[@class="aee5343fdb def9bc142a" and @data-testid="address"]'
        center_xpath = './/span[@data-testid="distance"]'
        stars_xpath = './/span[@class="f419a93f12"]//div[@class="b3f3c831be"]'
        link_xpath = './/a[@data-testid="title-link"]'

        properties = self.driver.find_elements(By.XPATH, property_xpath)

        data = []

        for property in properties:
            try:
                name = property.find_element(By.XPATH, name_xpath).text
            except:
                name = pd.NA

            try:
                rating_text = property.find_element(By.XPATH, rating_xpath).text
                rating_num = re.findall(r'\n(\d+,\d+)', rating_text)
                rating = rating_num[0] if rating_num else pd.NA
            except:
                rating = pd.NA

            try:
                star_text = property.find_element(By.XPATH, stars_xpath).get_attribute("aria-label")
                star_num = re.findall(r'(\d+)\sde', star_text)
                stars = star_num[0] if star_num else pd.NA
            except:
                stars = pd.NA

            try:
                price_text = property.find_element(By.XPATH, price_xpath).text
                price_num = re.findall(r'\s(\d+\.?\d+)', price_text)
                price = price_num[0] if price_num else pd.NA
            except:
                price = pd.NA

            try:
                location = property.find_element(By.XPATH, location_xpath).text
            except:
                location = pd.NA

            try:
                center_text = property.find_element(By.XPATH, center_xpath).text
                distance = re.findall(r'a\s(.*)\sk?m', center_text)
                distance = float(distance[0].replace(",", ".")) if distance else pd.NA
                if distance >= 50:
                    distance = distance / 1000 
            except:
                distance = pd.NA

            try:
                link = property.find_element(By.XPATH, link_xpath).get_attribute("href")
            except:
                link = pd.NA

            data.append({
                'name': name,
                'rating': rating,
                'stars': stars,
                'price': price,
                'location': location,
                'distance': distance,
                'link': link
            })

        df = pd.DataFrame(data, columns=['name', 'rating', 'stars', 'price', 'location', 'distance', 'link'])
        return df
    
    def fetch_description(self, link):
        """Fetches the hotel description from its webpage."""
        if not link or pd.isna(link):
            return "No link available"

        try:
            response = requests.get(link, headers=self.headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                element = soup.find(attrs={"data-testid": "property-description"})
                return element.text if element else "Description not found"
            return f"Error {response.status_code}"
        except requests.Timeout:
            return "Request timed out"
        except requests.RequestException:
            return "Request failed"

    def get_all_hotel_data(self):
        """Runs the full process: scrapes hotel info and descriptions."""
        df = self.get_hotel_information()

        if 'link' in df and not df['link'].isnull().all():
            valid_links = df['link'].dropna().astype(str)
            with ThreadPoolExecutor(max_workers=10) as executor:
                descriptions = list(executor.map(self.fetch_description, valid_links))
            
            # Assign descriptions back to DataFrame
            df.loc[df['link'].notna(), 'description'] = descriptions
        else:
            df['description'] = "No link available"

        return df
    