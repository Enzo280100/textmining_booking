from selenium import webdriver
from selenium.webdriver.common.by import By
from packages.selenium_setup import *

class BookingScraper:
    def __init__(self, driver):
        self.driver = driver

    def search_destination(self, place):
        '''
        Searches for the destination in the search box.
        Only the user has to enter the correct name of the place.
        '''
        self.driver.find_element(By.XPATH, '//div[@data-testid="destination-container"]').click()
        search_box = self.driver.find_element(By.NAME, 'ss')
        search_box.send_keys(place)
        css_selector = 'button.ebbedaf8ac:nth-child(2) > span:nth-child(1)'
        self.driver.find_element(By.CSS_SELECTOR, css_selector).click()

    def select_month(self, target_month, target_year):
        '''
        Selects the month and year in the calendar. 
        Advance to next month.
        The user has to enter the month in and the year in numbers (i.e. 'marzo' and '2025').
        '''
        months_path = '//h3[@class="e1eebb6a1e ee7ec6b631"]'
        
        while True:
            months = self.driver.find_elements(By.XPATH, months_path)
            
            for month in months:
                text = month.text.lower()
                if target_month.lower() in text and str(target_year) in text:
                    return
            
            next_month_path = '//button[contains(@class, "f073249358")]'
            next_month_buttons = self.driver.find_elements(By.XPATH, next_month_path)
            if next_month_buttons:
                next_month_buttons[0].click()
            else:
                print("The button to move to the next month was not found.")
                break
    
    def select_dates(self, from_date, to_date):
        '''
        Selects the dates in the calendar.
        The user has to enter the dates in the format 'mm-dd'.
        '''
        calendar_id = "calendar-searchboxdatepicker"
        span_class = "cf06f772fa ef091eb985"
        path = f'//div[@id="{calendar_id}"]//table[@class="eb03f3f27f"]//tbody//td[@class="b80d5adb18"]//span[@class="{span_class}"]'
        dates = self.driver.find_elements(By.XPATH, path)
        
        for date in dates:
            if date.get_attribute("data-date") == f"2025-{from_date}":
                date.click()
            if date.get_attribute("data-date") == f"2025-{to_date}":
                date.click()
                break

    def search_bottom(self):
        my_xpath="/html/body/div[3]/div[2]/div/form/div/div[4]/button/span"
        check_obscures(self.driver, my_xpath , type='xpath')
        check_and_click(self.driver,my_xpath , type='xpath')

    def run_pipeline(self, place, target_month, target_year, from_date, to_date):
        """ Ejecuta todo el pipeline con los datos ingresados """
        self.search_destination(place)
        self.select_month(target_month, target_year)
        self.select_dates(from_date, to_date)
        self.search_bottom()
