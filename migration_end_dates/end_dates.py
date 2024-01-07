import time
import datetime
import os
import sys
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait as wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select  import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    WebDriverException,
    TimeoutException,
    ElementNotInteractableException,
)
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.options import Options as EdgeOptions  # noqa
from selenium.webdriver import EdgeService as EdgeService  # noqa

class JoeDriver(webdriver.Edge, EdgeOptions = None, EdgeService = None):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._default_implicit_wait = 10
        self._default_page_load_wait = 10
        self._default_script_timeout = 10
        self._default_element_wait = 10
        self.driver_path = 'msedgedriver.exe'
        self.options = Options()
        self.service = Service(self.driver_path)


    #getter for driver_path
    def get_driver_path(self):
        return self.driver_path
    def set_driver_path(self, driver_path):
        self.driver_path = driver_path
    # Getter for username
    def get_username(self):
        return self._username

    # Setter for username
    def set_username(self, username):
        self._username = username

    # Getter for password
    def get_password(self):
        return self._password

    # Setter for password
    def set_password(self, password):
        self._password = password

    def sign_in(self):
        # Find the username and password input fields
        username_input = wait(self, 10).until(
            EC.element_to_be_clickable((By.ID, 'handle'))
        )
        password_input = wait(self, 10).until(
            EC.element_to_be_clickable((By.ID, 'password'))
        )

        # Clear the input fields (optional)
        username_input.clear()
        password_input.clear()

        # Enter the username and password
        username_input.send_keys(self._username)
        password_input.send_keys(self._password)

        # Find and click the sign in button
        sign_in_button = wait(self, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit'][name='submitbtn']"))
        )
        sign_in_button.click()

        

        
        





# Usually don't use globals, but this is a quick and dirty script.
# Specify the path to the Edge driver executable
# driver_path = 'msedgedriver.exe'
# options = Options()
# options.add_argument('--remote-debugging-port=9222')
# service = Service(driver_path)
#driver = webdriver.Edge(service=service, options=options)

def main():
    driver = JoeDriver()
    open_browser_to_site(driver)
    driver.sign_in()
   

def dropdown_select(driver, dropdown_index=None, dropdown_locatorza=None, dropdown_length=None ): 
#    dropdown_length = len(dropdown.options)
    #dropdown index would be the iteration number of the loop
    dropdown = Select(driver.EC.find_element((By.ID, 'clientid_INT')))
    if dropdown_index is not None:
        dropdown.select_by_index(dropdown_index)
        dropdown_name = dropdown.options[dropdown_index].text  # Get the name from the selected option

    else:
        dropdown.select_by_index(0)
        dropdown_name = dropdown.options[0].text  # Get the name from the default option
    return dropdown_name  # Return the name from the dropdown option
    
def end_record():
    pass

def submit_button_click(driver, dropdown_index=None):
# Duplicate the tab, select the correct person from the drop down, go to new tab, Click the history button in the new duplicated tab, click the continue button,  go back to the other tab,    hit the update button at the bottom of history 
    
    first_button = (driver.find_element((By.CSS_SELECTOR, "input[type='submit']")))
    first_button.click()

def config_driver_default_instance_():
    pass
    

 
def compare_data(driver):
    pass
def open_browser_to_site(driver):


    # Navigate to the desired URL
    # Specify the path to the Edge driver executable
    #If there's an element from their login, sign in
    # If there's an element from their 2fa, wait for action 
    try:
        driver.get('https://depaul.footholdtechnology.com') 
        if EC.presence_of_element_located((By.ID, 'handle')):
                driver.sign_in()
            #if 2fa, wait for action
        if EC.presence_of_element_located((By.ID, 'auth-code')):
            print("waiting for 2fa")
            wait(driver,60).until_not(EC.presence_of_element_located((By.ID, 'auth-code'))) 
        driver.get('https://depaul.footholdtechnology.com/awards/charts/medical/support_services_contacts')
        wait(driver,45).until(method=EC.presence_of_element_located((By.ID, 'clientid_INT')))
        dropdown_select(driver)    
        submit_button_click(driver)

    except WebDriverException:
        # If the specified address cannot be reached, get the current address from the open active instance
        current_address = driver.current_url
        print(f"Failed to reach the specified address. Current address: {current_address}")

        manual_url = input("Failed to reach the specified address. enter url manually and press enter")
        driver.get(manual_url)
    except Exception:
        print(Exception.__traceback__)
        


contacts_dict = {} #checked on the info screen
check_dict = {} #chwcked on the history screen
title_list = ['Dentist','Psychiatrist','Physician','Surgery','Therapist']
done_list = []
dropdown_index= 0

# Rest of your code...

#end record decision logic 
# decision
#if end date, ignore
#if not on the info screen that matches the title on the right screen, and has a cherck box, and has no end date
#if 
# if no end date, and box is available, fill in end date

# Close the browser window.
print('Done.')








#scs/ssc?fs=L3BhcnNlci5waHA%2FcHJvdmlkZXJzX3BocF9SVU49JnByb2duYW1lX2NoYXI9VXBwZXIrRmFsbHMmcGdyb3VwX2ludD0wJmdsY29faW50PTAmZ2xkaXZfaW50PTAmcHJvZ3NldF9sb2dpPXllcyZ1bj0yMDc3NzYwMDgmdGltZT0xNzA0MjI4Nzg1NTE5')