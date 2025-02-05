import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from packages.selenium_setup import *

class BookingScraper:
    def __init__(self, driver):
        self.driver = driver

    def reject_cookies(self):
        '''
        Rejects the cookies notification.
        '''
        path_cookies='//button[@id="onetrust-reject-all-handler"]'
        cookies= self.driver.find_elements('xpath',path_cookies)
        cookies[0].click()

    def reject_google_cookies(self):
        '''
        Rejects the Google cookies notification.
        '''
        try:
            iframe_google = self.driver.find_elements(By.TAG_NAME,'iframe')[0] #we find the iframe object
            self.driver.switch_to.frame(iframe_google) #switch to acces the iframe
            close_log_in = self.driver.find_element(By.CSS_SELECTOR, '#close') # find the close button element
            close_log_in.click() #click on it to close the pop-up
        except Exception:
            print('No Google LogIn found')
        self.driver.switch_to.default_content() 

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
        '''
        Clicks on the search button at the bottom of the page.
        '''
        my_xpath="/html/body/div[3]/div[2]/div/form/div/div[4]/button/span"
        check_obscures(self.driver, my_xpath , type='xpath')
        check_and_click(self.driver,my_xpath , type='xpath')

    def close_genius(self):
        '''
        Wait for content to load around 5 seconds and close the Genius Banner.
        In case there is no genius banner we will perform no action
        '''
        try:
            time.sleep(5)  
            path_close_genius='//div[@class="abcc616ec7 cc1b961f14 c180176d40 f11eccb5e8 ff74db973c"]'
            close_genius= self.driver.find_elements('xpath',path_close_genius)
            close_genius[0].click()
        except Exception as e:
            print("No Genius Banner")

    def scroll_and_click(self):
        '''
        Scroll to the bottom of the page and click the button to load more hotels.
        We define some time.sleep() to wait for the content to load.
        '''
        try:
            # Scroll to the bottom of the page to load new content
            self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)  
            time.sleep(3)  # Wait for content to load
            
            # Wait for the "load more" button to be clickable
            wait = WebDriverWait(self.driver, 7)
            
            while True:
                try:
                    # Look for the "load more" button
                    button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@class = "a83ed08757 c21c56c305 bf0537ecb5 f671049264 af7297d90d c0e0affd09"]')))
                    button.click() 
                    time.sleep(1) 
                    
                    # Scroll again to check if there's more content
                    self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)  
                    time.sleep(1) 
                    
                except Exception:
                    print("No more hotels to load or button is not clickable.")
                    break
        except Exception as e:
            print('No button found or other issue:', e)

    def run_pipeline(self, place, target_month, target_year, from_date, to_date):
        """ Ejecute all the steps in one pipeline """
        self.reject_cookies()
        self.reject_google_cookies()
        self.search_destination(place)
        self.select_month(target_month, target_year)
        self.select_dates(from_date, to_date)
        self.search_bottom()
        self.close_genius()
        self.scroll_and_click()
