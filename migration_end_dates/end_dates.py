import logging
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
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select


#todo: add a way to compare the data from the two screens
#todo: verify that it works up to the dropdown point
#add a way, maybe regex, to select the role, and then the following value for the role
#todo: add a wway to collect what's been done for an audit
#todo: add an entry logic
#todo: come up with corner cases
#todo: add a way to check for the end date, and if it's not there, add it
#todo, maybe add a click path for each program, or a way to input the program, or just have it wait till i select one


validation_structure = []
contacts_dict = {}  # checked on the info screen
check_dict = {}  # checked on the history screen
role_list = ['Dentist', 'Psychiatrist', 'Physician', 'Surgery', 'Therapist'] #maybe make this a dictionary with the role as the key and the value as the index, or regex the roles


class JoeDriver(webdriver.Edge):
    '''This class is a wrapper for the selenium webdriver.Edge class. It adds some additional functionality to the webdriver.Edge class.'''
    #could probably break this up a bit, but IT'S FIIIINE
    def __init__(self, wait, dropdown_index=None, EdgeOptions=None, EdgeService=None,
                  expected_conditions=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._default_implicit_wait = 10
        self._default_page_load_wait = 10
        self._default_script_timeout = 10
        self._default_element_wait = 10
        self.driver_path = 'msedgedriver.exe'
        self.options = Options()
        self.service = Service(self.driver_path)
        self._username = os.environ.get('FOOTHOLD_USERNAME')
        self._password = os.environ.get('FOOTHOLD_PASSWORD')

      
    # Getter and setter for driver_path
    def get_driver_path(self):
        return self.driver_path

    def set_driver_path(self, driver_path):
        self.driver_path = driver_path

    # Getter and setter for username
    def get_username(self):
        return self._username

    def set_username(self, username):
        self._username = username

    # Getter and setter for password
    def get_password(self):
        return self._password

    def set_password(self, password):
        self._password = password

    def sign_in(self):
        # Find the username and password input fields

        if EC.presence_of_element_located((By.ID, 'handle')):
            print("found the username input")
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
        else:
            pass
    
    def get_dropdown_length(self, dropdown_locator=None):
        dropdown = self.find_element(By.ID, 'clientid_INT')
        select = Select(dropdown)
        dropdown_length = len(select.options)
        return dropdown_length

    def submit_button_click(self, dropdown_index=None):
        first_button = self.find_element(By.CSS_SELECTOR, "input[type='submit']")
        first_button.click()

    def config_driver_default_instance_(self):
        #configures for either default browser or exsisting
        pass

    def find_duplicate(self):
        pass
    def compare_duplicates(self):
        pass
    def end_record(self):
        pass
    
    def dropdown_select(self, dropdown_index=None, dropdown_locator=None, dropdown_length=None, validation_structure=None): 
        '''Selects a dropdown option by index and adds the name to a data structure for validation later'''
        try:
            dropdown = self.find_element(By.ID, 'clientid_INT')
            wait(self,49).until.EC.presence_of_element_located(By.ID, 'clientid_INT')
            select = Select(dropdown)  # Create an instance of Select using the dropdown element
            continue_btn = self.find_element(By.CSS_SELECTOR, "input[type='submit']")
            # If a dropdown index is specified, select the option at that index, then click continue button
            if dropdown_index is not None:
                select.select_by_index(dropdown_index)  # Use the select_by_index method on the Select instance
                dropdown_name = select.first_selected_option.get_attribute("text")  # Get the name from the selected option
                continue_btn.click()  # Click the continue button
            else:
                select.select_by_index(0)  # Use the select_by_index method on the Select instance
                dropdown_name = select.first_selected_option.get_attribute("text")  # Get the name from the default option
                  # Return the name from the dropdown option
                continue_btn.click()  # Click the continue button
                
        except WebDriverException:
            current_address = self.current_url
            print(f"Failed to reach the specified address. Current address: {current_address}")
            manual_url = input("Failed to reach the specified address. Enter URL manually and press enter")
            self.get(manual_url)
        except Exception as e:
            print(f"An error occurred while selecting the dropdown option: {e}")
            print(Exception.__traceback__)
            logging.error(f"An error occurred while selecting the dropdown option: {e}")     
   
   
    def open_browser_to_site(self):
        # Add your code here

    # Navigate to the desired URL
    # Specify the path to the Edge driver executable
    #If there's an element from their login, sign in
    # If there's an element from their 2fa, wait for action 
        try:

            if 'depaul.footholdtechnology.com' in self.current_url:


            self.get('https://depaul.footholdtechnology.com') 
            if EC.presence_of_element_located((By.ID, 'handle')):
                    self.sign_in()
            else:pass
                #if 2fa, wait for action
            if EC.presence_of_element_located((By.ID, 'auth-code')):
                print("waiting for 2fa")
                wait(self,60).until_not(EC.presence_of_element_located((By.ID, 'auth-code'))) 
            self.get('https://depaul.footholdtechnology.com/awards/charts/medical/support_services_contacts')
            wait(self,45).until(method=EC.presence_of_element_located((By.ID, 'clientid_INT')))
            JoeDriver.dropdown_select(self)   
            JoeDriver.dropdown_select(self, 1)
            
    
        except WebDriverException:
            # If the specified address cannot be reached, get the current address from the open active instance
            current_address = self.current_url
            print(f"Failed to reach the specified address. Current address: {current_address}")
    
            manual_url = input("Failed to reach the specified address. enter url manually and press enter")
            self.get(manual_url)
        except Exception:
            print(Exception.__traceback__)
    
    


# Usually don't use globals, but this is a quick and dirty script.
# Specify the path to the Edge driver executable
# driver_path = 'msedgedriver.exe'
# options = Options()
# options.add_argument('--remote-debugging-port=9222')
# service = Service(driver_path)
#driver = webdriver.Edge(service=service, options=options)

def main():
    load_dotenv() 
    driver = JoeDriver(wait)
    driver.open_browser_to_site()
    driver.sign_in()
    # go to contact screen
   


    



info_dict = {} #checked on the info screen
history_dict = {} #chwcked on the history screen
role_list = ['Dentist','Psychiatrist','Physician','Surgery','Therapist']
done_list = []
dropdown_index= 0

# Rest of your code...

#end record decision logic 
# decision



# Close the browser window.

if __name__ == '__main__':
    main()
    print('Done.')




#compare logic

#if end date, ignore
#if not on the info screen that matches the title on the right screen, 
#if <i>discontinued</i> in the table
# if no end date, and box is available, fill in end date
    #find the role as the key value in the history screen, add the key and value to the dictionary
    #find the role as the key value in the info screen, add the key and value to the dictionary
    #compare the two dictionaries:
        #if they're the same/ fuzzy matches, do nothing
        #if they're different, add the end date to the info screen on the 



#scs/ssc?fs=L3BhcnNlci5waHA%2FcHJvdmlkZXJzX3BocF9SVU49JnByb2duYW1lX2NoYXI9VXBwZXIrRmFsbHMmcGdyb3VwX2ludD0wJmdsY29faW50PTAmZ2xkaXZfaW50PTAmcHJvZ3NldF9sb2dpPXllcyZ1bj0yMDc3NzYwMDgmdGltZT0xNzA0MjI4Nzg1NTE5')