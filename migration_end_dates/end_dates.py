import logging
import time
import datetime
import os
import sys
import re
from selenium import webdriver as webdriver
from selenium.webdriver.edge.service import Service
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
 # noqa
from selenium.webdriver import EdgeService as EdgeService  # noqa
from dotenv import load_dotenv
from fuzzywuzzy import fuzz

#TODO: add a way to compare the data from the two screens
#TODO: verify that it works up to the dropdown point
#add a way, maybe regex, to select the role, and then the following value for the role
#TODO: add a wway to collect what's been done for an audit
#TODO: add an entry logic
#TODO: come up with corner cases
#TODO: add a way to check for the end date, and if it's not there, add it
#TODO, maybe add a click path for each program, or a way to input the program, or just have it wait till i select one




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
from selenium.webdriver.support.select import Select
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
from selenium.webdriver import EdgeService as EdgeService
from dotenv import load_dotenv
from fuzzywuzzy import fuzz

from dotenv import load_dotenv
from fuzzywuzzy import fuzz
from selenium.webdriver import EdgeService as EdgeService
from dotenv import load_dotenv
from fuzzywuzzy import fuzz

#TODO: add a way to compare the data from the two screens
#TODO: verify that it works up to the dropdown point
#add a way, maybe regex, to select the role, and then the following value for the role
#TODO: add a wway to collect what's been done for an audit
#TODO: add an entry logic
#TODO: come up with corner cases
#TODO: add a way to check for the end date, and if it's not there, add it
#TODO, maybe add a click path for each program, or a way to input the program, or just have it wait till i select one




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
    def __init__(self, driver, Authenticator, Navigator, wait):
        self.driver = driver
        self.Authenticator = Authenticator
        self.Navigator = Navigator
        self.wait = wait(self.driver, 60)
    
  
    def init_browser_to_page(self, site_url, login_handle_id, password_handle_id, auth_code_id, search_term=None):
        '''This method initializes the browser to the site, and then signs in, and handles 2fa, if necessary. 
        the site_url is the url of the site you want to go to\
        the login_handle_id is the html id of the login handle
        the password_handle_id is the html id of the password handle
        the auth_code_id is the html id of the auth code handle'''

        self.navigate_to_site(site_url)
        try:
            self.Authenticator.sign_in(login_handle_id, password_handle_id)
            self.Authenticator.handle_2fa(auth_code_id)
            # self.navigate_to_support_page(page_url)
            if self.Authenticator.is_logged_in():
                logging.info("Already logged in")
            else:
                logging.info("Not logged in")
        except WebDriverException as e :
            logging.error(f"Incorrect username or password", str(e))
   

    def navigate_to_site(self, site_url):
        self.driver.get(site_url)

    def wait_for_search(self, search_term):
        search_input = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search Program']")))
        search_input.send_keys(search_term)
    
    def click_charts_sidebar_link(self):
        link_element = self.driver.find_element(By.XPATH, "//a[@aria-label='Charts']")
        link_element.click()
    
    def save_return_url(self):
        '''This method saves the current url as a return point for the program to return to after it's done with a task'''
        support_return_url = self.driver.current_url

        return support_return_url

class Navigator:
    '''This class wraps the driver, but adds some additional functionality to the webdriver.Edge class and is mostly use to navigate to pages, routing, and browser config'''
    def __init__(self, driver, Authenticator, Navigator, wait):
        self.driver = driver
        self.Authenticator = Authenticator
        self.Navigator = Navigator
        self.wait = wait(self.driver, 60)
    
    def init_browser_to_page(self, site_url, login_handle_id, password_handle_id, auth_code_id, search_term=None):
        '''This method initializes the browser to the site, signs in, and handles 2fa, if necessary. 
        site_url: the url of the site you want to go to
        login_handle_id: the html id of the login handle
        password_handle_id: the html id of the password handle
        auth_code_id: the html id of the auth code handle'''

        self.navigate_to_site(site_url)
        try:
            self.Authenticator.sign_in(login_handle_id, password_handle_id)
            self.Authenticator.handle_2fa(auth_code_id)
            if self.Authenticator.is_logged_in():
                logging.info("Already logged in")
        
        except WebDriverException as e:
            logging.error("Incorrect username or password", str(e))
   
    def navigate_to_site(self, site_url):
        self.driver.get(site_url)

    def wait_for_search(self, search_term):
        search_input = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search Program']")))
        search_input.send_keys(search_term)
    
    def click_charts_sidebar_link(self):
        link_element = self.driver.find_element(By.XPATH, "//a[@aria-label='Charts']")
        link_element.click()
    
    def save_return_url(self):
        '''This method saves the current url as a return point for the program to return to after it's done with a task'''
        support_return_url = self.driver.current_url
        return support_return_url

    def submit_button_click(self):
        submit_button = self.driver.find_element(By.XPATH, "//input[@type='submit']")
        submit_button.click()
    
    def click_selected_element(self, identifier_type, identifier):
        '''This method clicks an element by id, type, or xpath'''
        element = None
        try:
            if identifier_type == "id":
                element = self.driver.find_element(By.ID, identifier)
            elif identifier_type == "name":
                element = self.driver.find_element(By.NAME, identifier)
            elif identifier_type == "xpath":
                element = self.driver.find_element(By.XPATH, identifier)
            if element:
                element.click()
        except NoSuchElementException as e:
            logging.error("Element not found", str(e))


class DataOperator:
    '''This class handles data operations, like comparing data, and adding data to a data structure, '''

    def __init__(self, driver, ClickHandler):
        self.driver = driver
        self.ClickHandler = ClickHandler
    pass
    
    def update_end_date(self):
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



class Authenticator:
    '''This class handles authentication, and is mostly used to sign in and 2fa'''

        #NOTE it would be better to move the creation of the WebDriverWait instance (wait(self.driver, 60)) to the initialization of the class and reuse it 

    def __init__(self, driver):
        self.driver = driver
        self._username = os.getenv('FOOTHOLD_USERNAME')
        self._password = os.getenv('FOOTHOLD_PASSWORD')
        # self.driver.EC.wait = wait(self.driver, 60)
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


    def sign_in(self, username_handle_id, password_handle_id, auth_code_id):
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
                self.handle_2fa(auth_code_id)        
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
        try:
            if EC.presence_of_element_located((By.ID, auth_code_id)):
                logging.info("Found the 2fa input")
            wait(self.driver, 60).until_not(EC.presence_of_element_located((By.ID, auth_code_id)))
        except NoSuchElementException:
            logging.error("No such element: 2fa input not found")
        except TimeoutException:
            logging.error("Timeout: 2fa input not found")



def main(iterator = None, info_dict = None, history_dict = None, done_list = None):

    load_dotenv() 
    #set variables
    login_handle_id = 'handle'
    password_handle_id = 'password'
    auth_code_id = 'auth-id'


    driver = webdriver.Edge()
    auth = Authenticator(driver)
  
    navigator = Navigator(driver, Authenticator, Navigator)
    data = DataOperator(driver, Navigator)

    
    navigator.init_browser_to_page('https://depaul.footholdtechnology.com', login_handle_id, password_handle_id, auth_code_id)

   



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