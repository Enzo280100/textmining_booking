import pandas as pd
import re
from selenium import webdriver
from packages.selenium_setup import *

# class DataCollection:
#     def __init__(self, driver):
#         self.driver = driver

#     def get_hotel_information(self):
#         '''
#         Collects the information of the hotels in the search results.
#         '''
#         rating = '//div[@class="a3b8729ab1 d86cee9b25"]'
#         name = '//div[@class="f6431b446c a15b38c233"]'
#         price = '//span[@class="f6431b446c fbfd7c1165 e84eb96b1f"]'
#         location = '//span[@class="aee5343fdb def9bc142a" and @data-testid="address"]'
#         center = '//span[@data-testid="distance"]'
#         stars = '//span[@class="f419a93f12"]//div[@class="b3f3c831be"]'

#         ratings = self.driver.find_elements('xpath', rating)
#         names = self.driver.find_elements('xpath', name)
#         prices = self.driver.find_elements('xpath', price)
#         locations = self.driver.find_elements('xpath', location)
#         centers = self.driver.find_elements('xpath', center)
#         stars = self.driver.find_elements('xpath', stars)

#         link_elements = self.driver.find_elements(By.CSS_SELECTOR, 'a[data-testid="title-link"]')
#         links = [element.get_attribute("href") for element in link_elements]

#         data = []
#         for i in range(len(name)):
#             data.append({
#                 'name': names[i].text, 
#                 'rating': ratings[i].text, 
#                 'price': prices[i].text, 
#                 'location': locations[i].text, 
#                 'link': links[i]
#             })

#         df = pd.DataFrame(data, columns=['name', 'rating', 'price', 'location', 'link'])
        
#         return df
    
class DataCollection:
    def __init__(self, driver):
        self.driver = driver

    def get_hotel_information(self):
        '''
        Collects the information of the hotels in the search results.
        '''
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