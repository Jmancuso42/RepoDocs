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
from fuzzywuzzy import fuzz

#todo: add a way to compare the data from the two screens
#todo: verify that it works up to the dropdown point
#add a way, maybe regex, to select the role, and then the following value for the role
#todo: add a wway to collect what's been done for an audit
#todo: add an entry logic
#todo: come up with corner cases
#todo: add a way to check for the end date, and if it's not there, add it
#todo, maybe add a click path for each program, or a way to input the program, or just have it wait till i select one




  #key ideas right now:
    #from home page, select and click on charts
        #select/ interact wirth the search bar input with the placeholder elemnt attributes of "search program/ id = "530"
        #enter the right program name in the search bar by getting input from user or waiting , hit enter
        #navigate to and click on the anchor link with the text of "support services contacts" in the div 
        #get the URL of the consumer selection page, store into a variable to use as a return point for each iteration
        # get the length of the drop down element and store into a variable to use as a range
        # select the dropdown element according to the iteration number
        #click the continue button
            #good idea to have locked record handling if it gets that far
        # go through the table
class Navigator:
    '''This class wraps the driver, but adds some additional functionality to the webdriver.Edge class and is mostly use to navigate to pages, routing, and browser config'''
    def __init__(self, driver, Authenticator, Navigator, ClickHandler):
        self.driver = driver
        self.Authenticator = Authenticator
        self.Navigator = Navigator
        self.ClickHandler = ClickHandler
    
  
    def init_browser_to_page(self, site_url, login_handle_id, password_handle_id, auth_code_id, search_term=None):
        '''This method initializes the browser to the site, and then signs in, and handles 2fa, if necessary. 
        the site_url is the url of the site you want to go to\
        the login_handle_id is the html id of the login handle
        the password_handle_id is the html id of the password handle
        the auth_code_id is the html id of the auth code handle'''

        try:
            self.navigate_to_site(site_url)
            self.Authenticator.sign_in(login_handle_id, password_handle_id)
            self.Authenticator.handle_2fa(auth_code_id)
            # self.navigate_to_support_page(page_url)
        except self.Authenticator.is_logged_in():
            logging.info("Already logged in")
        except:
            logging.error("Incorrect username or password")
        finally:
            if 
            logging.info("Sign in successful")

    def navigate_to_site(self, site_url):
        self.driver.get(site_url)

    def wait_for_search(self, search_term):
        
    pass
    
class Authenticator:
    '''This class handles authentication, and is mostly used to sign in and 2fa'''
    def __init__(self, driver):
        self.driver = driver
        self._username = os.getenv('USERNAME')
        self._password = os.getenv('PASSWORD')
        
    def clear_login_fields(self):
        '''Clears the username and password fields'''
        username_input = self.driver.find_element(By.ID, 'handle')
        password_input = self.driver.find_element(By.ID, 'password')
        username_input.clear()
        password_input.clear()

    #getters and setteres in case the default doesn't work
    def get_username(self):
        return self._username

    def set_username(self, username):
        self._username = username

    # Getter and setter for password
    def get_password(self):
        return self._password

    def set_password(self, password):
        self._password = password


    def sign_in(self, username_handle_id, password_handle_id):
        try:
            # Check if the username and password fields are present
            if EC.presence_of_element_located((By.ID, username_handle_id)) and EC.presence_of_element_located((By.ID, password_handle_id)):
                # Find the username and password input fields
                username_input = self.driver.find_element(By.ID, username_handle_id)
                password_input = self.driver.find_element(By.ID, password_handle_id)
                
                self.clear_login_fields()

                # Send keys to the username and password input fields
                username_input.send_keys(self._username)
                password_input.send_keys(self._password)

                # Find and click the sign in button
                sign_in_button = wait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//input[@type='submit'][@name='submitbtn']"))
                )
                sign_in_button.click()               
            else:
                pass
        except NoSuchElementException:
            logging.error("Username or password fields not found")
        except TimeoutException:
            logging.error("Sign in button not found")
        except Exception as e:
            logging.error(f"An exception occurred during sign in: {str(e)}")

    def is_logged_in(self):
        '''Check if the user is logged in'''
        current_url = self.driver.current_url
        if current_url == 'https://depaul.footholdtechnology.com/awards/home':
            logging.info("Already logged in")
            return True
        try:
            sign_in_button = self.driver.find_element(By.XPATH, "//input[@type='submit'][@name='submitbtn']")
            auth_code_input = self.driver.find_element(By.ID, "auth-id")
            if sign_in_button.is_displayed() and auth_code_input.is_displayed():
                return False
        except NoSuchElementException:
            logging.exception("No such element")
            
    def handle_2fa(self, auth_code_id):
        '''Sometimes you have to do 2fa, so this waits until the user has handled it, because it's not automated'''
        if EC.presence_of_element_located((By.ID, auth_code_id)):
            logging.log(logging.INFO, "Found the 2fa input")
        wait(self.driver, 60).until_not(EC.presence_of_element_located((By.ID, auth_code_id)))

class DataOperator:
    '''This class handles data operations, like comparing data, and adding data to a data structure, '''

    def __init__(self, driver, ClickHandler, RecordUpdater):
        self.driver = driver
        self.ClickHandler = ClickHandler
        self.RecordUpdater = RecordUpdater
    pass
    
    def compare_and_update(self):
        pass
    def search_info_screen(self):
        pass
    def search_history_screen(self):
        pass

    def add_to_dict(self, dict, key, value):
        dict[key] = value    
    # def add_to_dict(self, dict, key, value):
    #     dict[key] = value
    # if  dropdown_index is not None:
    #     driver.select.select_by_index(dropdown_index)  # Use the select_by_index method on the Select instance
    #     dropdown_name = select.first_selected_option.get_attribute("text")  # Get the name from the selected option
    #     continue_btn.click()  # Click the continue button
    #  if = is not None:
    #      =.append(dropdown_name)
    #  else:
    #     select.select_by_index(0)  # Use the select_by_index method on the Select instance
class InteractionHandler:
    '''This class handles tasks like clicking, dropdowns, and things that's not navigation or authentication. Keystrokes and the like'''
    def __init__(self, driver, select, wait, dropdown_index=None):
        self.driver = driver
        self.select = select
        self.wait = wait
        self.dropdown_index = dropdown_index

        
    def submit_button_click(self):
        submit_button = self.driver.find_element(By.XPATH, "//input[@type='submit']")
        submit_button.click()
    
        #NOTE this might not even be necessary because of being able to get the URL, but it's here untiil that is the case
    def click_charts_sidebar_link(self):
        link_element = self.driver.find_element(By.XPATH, "//a[@aria-label='Charts']")
        link_element.click()


    def click_selected_element(self, identifier_type, identifier):
        '''This method clicks an element by id, type, or xpath, CSS, or aria-label. It's a bit of a catch all'''
        #NOTE this honestly might not be good practice, but it's here for now
        element = None
        try:
            if identifier_type == "id":
                element = self.driver.find_element(By.ID, identifier)
            elif identifier_type == "name":
                element = self.driver.find_element(By.NAME, identifier)
            elif identifier_type == "xpath":
                element = self.driver.find_element(By.XPATH, identifier)
            elif identifier_type == "css":
                element = self.driver.find_element(By.CSS_SELECTOR, identifier)
            if element is not None:          
                element.click()
        except NoSuchElementException:
            logging.exception(f"No such element: {identifier, identifier_type}")

    def get_dropdown_length(self, dropdown_id):
        dropdown = self.driver.find_element(By.ID, dropdown_id)
        select = Select(dropdown)
        dropdown_length = len(select.options)
        return dropdown_length
        
    def dropdown_select(self, dropdown_id, dropdown_index=None): 
        #NOTE the htmll id for dropdown_ID = "clientid_INT", html name tag is the same as the id
        # dropdown index is going to be the integer that is iterator to be used in the for loop
        try:
            dropdown = self.driver.find_element(By.ID, dropdown_id)
            wait(self.driver, 49).until(EC.presence_of_element_located((By.ID, dropdown_id)))
            select = Select(dropdown)
            if dropdown_index is not None:
                dropdown_element = select.select_by_index(dropdown_index)
            else:
                dropdown_element = select.select_by_index(0)
            dropdown_element.click()
        except NoSuchElementException:
            logging.exception(f"No such element: {dropdown_id}")

    def find_and_click(self,element_id = None, element_type = None, element_xpath = None):
        '''This method finds and clicks an element by id, type, or xpath'''
        pass
class RecordUpdater:
    '''This class handles updating the records, and is mostly used to update the end date'''
    def __init__(self, driver):
        self.driver = driver
    def update_record(self):
        pass
    def update_end_date(self):
        pass
    
    
    
class JoeDriver(webdriver.Edge):
    '''This class is a wrapper for the selenium webdriver.Edge class. it has some additional functiolnality because it felt more organized to have it contain the driver features, but with my own configuration'''
    #could probably break this up a bit, but IT'S FIIIINE
    def __init__(self, wait = None, select = None,iterator=None, EdgeOptions=None,
                  EdgeService=None,expected_conditions=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._default_implicit_wait = 10
        self._default_page_load_wait = 10
        self._default_script_timeout = 10
        self._default_element_wait = 10
        self.driver_path = 'msedgedriver.exe'
        self.options = Options()
        self.service = Service(self.driver_path)
       


    # Getter and setter for driver_path incase the default doesn't work
    def get_driver_path(self):
        return self.driver_path

    def set_driver_path(self, driver_path):
        self.driver_path = driver_path

    
    def set_config_driver_default_instance_(self,config_variable):
        #configures for either default browser, with the idea of beinjg able to use a browser that'sa already signed in, or a local instance 
        pass



        # Specify the path to the Edge driver executable    
        # driver_path = 'msedgedriver.exe'
        # options = Options()
        #options.add_argument('--remote-debugging-port=9222')
        # service = Service(driver_path)
        #driver = webdriver.Edge(service=service, options=options)

def main(iterator = None, info_dict = None, history_dict = None, done_list = None):

    load_dotenv() 
    #set variables
    login_handle_id = 'handle'
    password_handle_id = 'password'
    auth_code_id = 'auth-id'


    driver = JoeDriver(wait,Select,iterator,EdgeOptions,EdgeService,EC)
    auth = Authenticator(driver)
    handler = InteractionHandler(driver,Select,iterator)
    rupdater = RecordUpdater(driver)
    navigator = Navigator(driver, Authenticator, Navigator, InteractionHandler)
    data = DataOperator(driver, InteractionHandler, RecordUpdater)

    #try to go to 
    navigator.init_browser_to_page('https://depaul.footholdtechnology.com/awards/home', login_handle_id, password_handle_id, auth_code_id)

   
role_list = ['Dentist','Psychiatrist','Physician','Surgery','Therapist'] #maybe make this a dictionary with the role as the key and the value as the index, or regex the roles
iterator= 0


if __name__ == '__main__':
    iterator = 0
    done_list = []
    info_dict = {} #checked on the info screen
    history_dict = {} #checked on the history screen

    main(iterator, info_dict, history_dict, done_list)
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



#URL scs/ssc?fs=L3BhcnNlci5waHA%2FcHJvdmlkZXJzX3BocF9SVU49JnByb2duYW1lX2NoYXI9VXBwZXIrRmFsbHMmcGdyb3VwX2ludD0wJmdsY29faW50PTAmZ2xkaXZfaW50PTAmcHJvZ3NldF9sb2dpPXllcyZ1bj0yMDc3NzYwMDgmdGltZT0xNzA0MjI4Nzg1NTE5')