from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select as select
import logging
import os
import datetime
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (NoSuchElementException, TimeoutException, ElementClickInterceptedException,
ElementNotInteractableException, ElementNotVisibleException, ElementNotSelectableException, InvalidElementStateException)



#NOTE this has been abandoned :(  I'm keeping it around for spare parts in the future

#TODO add encapsulation to everything
#TODO add logging
#TODO add error handling
#TODO add docstrings
#TODO add central algorithm for finding elements
#TODO add central algorithm for comparing the info screens

#CONSTANTS
#NOTE dotenv was straight up not working at all on this machine, so I'm hardcoding the values in the interest of time :(
#NOTE I know this is really bad practice, but it's *a* real solution :)
HEADER_TEXT = "Support services contacts consumer selection"
FOOTHOLD_USERNAME= 'username'
FOOTHOLD_PASSWORD = 'password'
EDGE_DRIVER_PATH = 'msedgedriver.exe'
FOOTHOLD_HOME_URL = 'https://depaul.footholdtechnology.com/awards/home'
FOOTHOLD_LOGIN_URL = 'https://depaul.footholdtechnology.com/zf2/login'
LOGIN_XPATH = '//*[@id="handle"]'
PASSWORD_XPATH = '//*[@id="password"]'
AUTH_CODE_XPATH = '//*[@id="auth_code"]'
DROPDOWN_XPATH = '//*[@id="clientid_INT"]'
#DROPDOWN_FULL_XPATH = '/html/body/form/center/table/tbody/tr/td/table/tbody/tr[2]/td/div/label/select'

CHART_SIDEBAR_XPATH = '//*[@id="q-app"]/div/div[1]/aside/div/div/div[1]/div/div/div[1]/div[2]/a[3]'
SUBMIT_BUTTON_XPATH = '//input[@name="submitbtn" and @type="submit"]'
SUBMIT_BUTTON_NAME = 'submitbtn'
SUPPORT_BUTTON_XPATH = '//*[@id="sidebar-flyout-charts"]/div[3]/div/div[5]/div[2]/div/div[11]/div/div[2]/a/div[2]'
MEDICAL_BUTTON_XPATH ='//*[@id="sidebar-flyout-charts"]/div[3]/div/div[5]/div[1]/div[2]/a'

SEARCH_BOX_XPATH = "//input[@class='q-field__input q-placeholder col']"
SEARCH_BOX_XPATH_WITH_TYPE = '//input[@class="q-field__input q-placeholder col" and @type="search"]'
# '//input[contains(@class, "q-field__input") and @type="search"]') #NOTE this uses contains
SEARCH_BOX_CSS = "input.q-field__input.q-placeholder.col"
# SEARCH_BOX_CSS = "input.q-field__input.q-placeholder.col"
# 'input.q-field__input.q-placeholder.col[type="search"]'
INNER_BOX = '.q-input__inner'

#NOTE dont need these frame paths to be constants but its good practice to not use magic strings
PARENT_FRAME_XPATH = "//*[contains(@id, 'ng-app')]"
CHILD_FRAME_XPATH = "//*[contains(@id, 'awards_classic_iframe')]"
# Print all environment variables
load_dotenv(
    dotenv_path='C:\\Users\\jmancuso\\Repos\\RepoDocs\\migration_end_dates\\vars.env'
)  #NOTE cannot get to work



def exception_handler(self, exception):
        '''This method handles exceptions'''
        current_exception = exception
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        error_message = f'{timestamp} - Exception: {current_exception}'
        logging.error(error_message)
class Navigate:
        
    class NavigateHelpers:
        def __init__(self, outer_instance) -> None:
            self.outer_instance = outer_instance
            self.driver =  self.outer_instance.driver
            self.wait = self.outer_instance.wait
            self.select = self.outer_instance.select
            self.iteration = self.outer_instance.iteration

        def detect_home_page(self, url):
            '''Detects if the current page is the home page
            url is to be the URL of the home page'''
            try:
                wait(self.driver, 10).until(EC.url_to_be(url))
                if self.driver.current_url == FOOTHOLD_HOME_URL:
                    logging.info('home page detected')
                    return True
                else:
                    logging.info('home page not detected')
            except TimeoutException as e:
                logging.error(f"Timeout error: {e}")
                

        def click_selected_element(self, identifier_type, identifier, clear=False):
            #NOTE feels like I reinvented the wheel here, something to consider
            by_map = {
                'class': By.CLASS_NAME,
                'css': By.CSS_SELECTOR,
                'id': By.ID,
                'link_text': By.LINK_TEXT,
                'name': By.NAME,
                'partial_link_text': By.PARTIAL_LINK_TEXT,
                'tag': By.TAG_NAME,
                'xpath': By.XPATH,
            }
            try:
                # Get the By attribute from the map
                by_attribute = by_map.get(identifier_type.lower())
                if by_attribute is None:
                    raise ValueError(f"Invalid identifier_type: {identifier_type}")
                locator = (by_attribute, identifier)
                self.wait(self.driver, 4).until(EC.presence_of_element_located(locator))
                element = self.driver.find_element(*locator)
                if clear is False or None:
                    element.click()
                    logging.info(f'clicked element by {identifier_type} clear: {clear}')
                elif clear is True:
                    element.click()
                    element.clear()  # Clear the element's value
                    logging.info(f'clicked element by {identifier_type} and cleared: {clear}')
                else:
                    raise ValueError("Invalid value for clear parameter")
            except NoSuchElementException as e:
                logging.error(f'No such element: {e.msg}')
            except TypeError as e:
                logging.error(f"Type error: {str(e)}")
            except AttributeError as e:
                logging.error(f"Attribute error: {str(e)}")
            except TimeoutException as e:
                logging.exception(f'Timeout error: {e.msg}')
                      

        class DataOperations:
            def __init__(self, outer_instance) -> None:
                self.outer_instance = outer_instance
                self.driver =  self.outer_instance.driver
                self.wait = self.outer_instance.wait
                self.select = self.outer_instance.select
                self.iteration = self.outer_instance.iteration

            def get_range_of_dropdown(self) -> int:
                #TODO move to navigate helpers
                '''This method gets the range of the dropdown element and returns it to the caller
                to be used as the range of the loop'''
                dropdown_range = len(self.select(self.driver.find_element(By.XPATH, DROPDOWN_XPATH)).options)
                logging.info(f'got range of dropdown: {dropdown_range}')
                return dropdown_range

            def select_dropdown_option(self, iteration=None):
                '''This method selects a dropdown element and selects the option by index. If no 
                index is passed, it selects the first option with the 0 index. logs the selection'''
                self.select(self.driver.find_element(By.XPATH, DROPDOWN_XPATH)).select_by_index(iteration or 0)
                logging.info(f'selected dropdown option by {"iteration" if iteration else "default"}')                      
    
    
    def __init__(self,driver,wait,select,iteration = None):
       '''This class contains methods for navigating the Foothold application.
       The iteration parameter is used to select the correct dropdown option based on the current i in range of the loop'''
       self.driver = driver
       self.wait = wait
       self.select = select
       self.iteration = iteration
       self.current_support_prog_return_url = None
       self.navHelper = self.NavigateHelpers(self)

        
    def input_program_name_into_search(self, program_input=None):
        #NOTE 'q-input__inner' is the search box css element
        # search_box_find = self.driver.find_element(By.CSS_SELECTOR, SEARCH_BOX_CSS)
        
        if program_input is None:
            program_input = input("Enter program input: ")  # Wait for user input
        if not program_input:
            raise ValueError("Invalid program input")
        try:
            # self.wait(self.driver,5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '\
            #     input.q-field__input.q-placeholder.col\
            #     [type="search"]')))
            # search_box = self.wait(self.driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, SEARCH_BOX_CSS)))
            search_box = self.driver.find_element(By.CSS_SELECTOR, SEARCH_BOX_CSS)
            self.wait(self.driver,3).until(EC.element_to_be_clickable((search_box)))
            self.navHelper.click_selected_element('css', INNER_BOX, clear = True) 
            search_box.click()
            search_box.clear()
            search_box.send_keys(program_input)
            logging.info('program input entered into search box')
        except NoSuchElementException as e:
            exception_handler(self,e)
            logging.error(f'No such element @ search input: {e.msg}')
        except TimeoutException as e:
            exception_handler(self,e)
            logging.exception(f'Timeout error @ search input: {e.msg}')
        except AttributeError as e:
            exception_handler(self,e)
            logging.error(f'Attribute error @ search input: {str(e)}')


    def navigate_side_bar(self):
        '''This method clicks the charts sidebar link and then the medical records link, takes input
        from the user, and then selects the first item in the dropdown list'''
        #NOTE the hardcoding is not great, but it is consistent
        #TODO if cleaning up, break this into 4 methods
        #NOTE '.q-menu' is the list, '.q-item' is the item. maybe add these to constants or vars
        try:
            #click charts link
            self.navHelper.click_selected_element('xpath', CHART_SIDEBAR_XPATH, clear = False)
            logging.info('clicked charts link')

            #enter program input into search box
            self.input_program_name_into_search()
            
            #TODO if cleaning up, refactor this chunk with the helper select method
            # Select the first item in the dropdown list, q-menu is the list, q-item is the item
            self.wait(self.driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.q-menu ')))
            first_item = self.driver.find_element(By.CSS_SELECTOR,('.q-menu .q-item'))
            self.wait(self.driver, 3).until(EC.presence_of_element_located(first_item))
            first_item.click()
            logging.info('clicked first item in dropdown list')

            #click medical records link
            self.navHelper.click_selected_element('xpath', MEDICAL_BUTTON_XPATH)
            logging.info('clicked medical records link')
            
            #NOTE this is the old way of doing it
            # self.wait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH,MEDICAL_BUTTON_XPATH)))
            # medical_records_element = driver.find_element(By.XPATH, MEDICAL_BUTTON_XPATH)
            # medical_records_element.click()
            # logging.info('clicked medical records link')

            #select support button
            self.navHelper.click_selected_element('xpath', SUPPORT_BUTTON_XPATH)
            logging.info('clicked support contacts button')
            #old way of doing it
            # self.wait(self.driver, 8).until(EC.presence_of_element_located((By.XPATH, SUPPORT_BUTTON_XPATH)))
            # self.wait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, SUPPORT_BUTTON_XPATH)))
            # support_button_element = driver.find_element(By.XPATH, SUPPORT_BUTTON_XPATH)
            # support_button_element.click()

        except NoSuchElementException as e:
            logging.error(f'No such element: {e.msg}')
        except TimeoutException as e:
            logging.error(f'Timeout error: {e.msg}')

    def detect_support_contact_selection_page(self):
        '''Detects if the current page is the support contact selection page'''
        try:

            # Switch to iframe
            self.driver.switch_to.frame(self.wait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@id, 'ng-app')]"))))
            self.driver.switch_to.frame(self.wait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@id, 'awards_classic_iframe')]"))))

            dropdown_element = self.wait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, DROPDOWN_XPATH)))
            if dropdown_element:
                self.current_support_prog_return_url = self.driver.current_url
                logging.info('support page detected')
                     
            logging.info('end of support page detection chain')

        except NoSuchElementException as e:
            logging.exception(f'No such element: detect support contact selection page {e.msg}')
            raise NoSuchElementException(f"No such element: {e.msg}")
        except TimeoutException as e:
            logging.exception(f'Timeout error: {e.msg}')
            # raise TimeoutException(f"Timeout error: {e.msg}") from e
        except TypeError as e:
            logging.exception(f'Type error: {e}')
            raise TypeError(f"Type error: {e}") from e
            # raise TypeError(f"Type error: {e.msg}") from e

    def get_range_of_dropdown(self) -> int:
        #TODO move to navigate helpers
        '''This method gets the range of the dropdown element and returns it to the caller
        to be used as the range of the loop'''
        dropdown_range = len(self.select(self.driver.find_element(By.XPATH, DROPDOWN_XPATH)).options)
        logging.info(f'got range of dropdown: {dropdown_range}')
        return dropdown_range

    def select_dropdown_option(self, driver, select, iteration=None):

        '''This method selects a dropdown element and selects the option by index. If no 
        index is passed, it selects the first option with the 0 index. logs the selection'''
        self.select(self.driver.find_element(By.XPATH, DROPDOWN_XPATH)).select_by_index(iteration or 0)
        logging.info(f'selected dropdown option by {"iteration" if iteration else "default"}')


    
    #not sure where this was or how it got here 
    # driver = driver
    #     self.wait = wait
    #     select = select
    #     iteration = iteration
    #     drange = drange
    #     self.navigate = Navigate(driver, wait, select, iteration)
class Authentication:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def send_username(self, username_handle_XPATH, username=None):
        try:
            username_element = self.driver.find_element(By.XPATH, username_handle_XPATH)
            username_element.send_keys(username)
        except NoSuchElementException as e:
            # raise NoSuchElementException from e
            logging.error(f'No such element: {e.msg}')

    def send_password(self, password_handle_XPATH, password=None):
        #TODO add password masking
        #TODO TEST to see if this works with the password parameter
        try:
            password_element = self.driver.find_element(By.XPATH, password_handle_XPATH)
            password_element.send_keys(password)
        except NoSuchElementException as e:
            # raise NoSuchElementException
            logging.error(f'No such element: {e.msg}')

    def wait_for_auth_code(self):
        try:
            self.wait(self.driver, 120).until_not(
                EC.presence_of_element_located((By.XPATH, AUTH_CODE_XPATH))
            )
        except NoSuchElementException as e:
            # raise NoSuchElementExceptio
            logging.error(f'No such element: {e.msg}')
        except TimeoutException as e:
            # raise TimeoutException
            logging.exception(f'Timeout error: {e.msg}')
        


def main():
    load_dotenv(os.path.join(os.path.dirname(__file__), 'vars.env'))
    logging.basicConfig(filename='dirty_end_dates.log', level=logging.INFO)
    logging.info('Started')

    path = os.getenv('EDGE_DRIVER_PATH') # this doesn't work currently

    # username_handle_id = '//*[@id="handle"]'
    # password_handle_id = '//*[@id="password"]'
    # auth_code_id = '//*[@id="auth_code"]'
    # chart_xpath = '//*[@id="q-app"]/div/div[1]/aside/div/\
    #     div/div[1]/div/div/div[1]/div[2]/a[3]'
    # username = os.getenv('FOOTHOLD_USERNAME')
    # username = 'jmancuso'
    # logging.info(os.getenv('FOOTHOLD_USERNAME'))

    #config
    options = webdriver.EdgeOptions()
    options.add_argument(r"--user-data-dir=C:\\Users\\jmancuso\\AppData\\Local\\Microsoft\\Edge\\User Data\\Profile 1")
    options.add_argument(r"--profile-directory=Profile 1")
    service = Service('C:\\Users\\jmancuso\\Repos\\RepoDocs\\migration_end_dates\\msedgedriver.exe')
    driver = webdriver.Edge(options=options, service=service)
    driver.implicitly_wait(3)
    auth = Authentication(driver,wait)
    nav = Navigate(driver, wait, select)

    driver.get('https://depaul.footholdtechnology.com')
    logging.info('got foothold')
    #TODO add control flow to login stuff
    
    if  nav.driver.current_url == FOOTHOLD_LOGIN_URL:
        auth.send_username(LOGIN_XPATH, FOOTHOLD_USERNAME)
        auth.send_password(PASSWORD_XPATH, FOOTHOLD_PASSWORD)
    # nav.navHelper.click_submit_button(driver)
        nav.navHelper.click_selected_element('xpath', SUBMIT_BUTTON_XPATH, clear = False)
        # nav.wait(driver, 20).until_not(EC.presence_of_element_detected((By.XPATH, AUTH_CODE_XPATH)))
        auth.wait_for_auth_code()
    
    # nav.navHelper.detect_home_page(FOOTHOLD_HOME_URL)
    nav.wait(driver, 20).until(EC.url_to_be(FOOTHOLD_HOME_URL))
        # program = input("Enter the program name: ")
    if nav.driver.current_url == (FOOTHOLD_HOME_URL):
        # nav.navHelper.click_selected_element('xpath', CHART_SIDEBAR_XPATH, clear = False)
        # nav.navHelper.click_selected_element('xpath', MEDICAL_BUTTON_XPATH, clear = False)
        # nav.navHelper.click_selected_element('xpath', SUPPORT_BUTTON_XPATH, clear = False)
        # nav.navHelper.click_selected_element('xpath', DROPDOWN_XPATH, clear = False)
        # nav.navHelper.click_selected_element('xpath', SUBMIT_BUTTON_XPATH, clear = False)
        # nav.navHelper.click_selected_element('xpath', SEARCH_BOX_XPATH, clear = True)
        # nav.input_program_name_into_search()
        # nav.navHelper.click_selected_element('xpath', DROPDOWN_XPATH, clear = False)
        # nav.navHelper.click_selected_element('xpath', SUBMIT_BUTTON_XPATH, clear = False)
        # nav.navHelper.click_selected_element('xpath', SUPPORT_BUTTON_XPATH, clear = False)
        # nav.navHelper.click_selected_element('xpath', DROPDOWN_XPATH, clear = False)
        # nav.navHelper.click_selected_element('xpath', SUBMIT_BUTTON_XPATH, clear = False)
        # nav.navHelper.click_selected_element('xpath', SEARCH_BOX_XPATH, clear = True)
        # nav.input_program_name_into_search()
        # nav.navHelper.click_selected_element('xpath', DROPDOWN_XPATH, clear = False)
        # nav.navHelper.click_selected_element('xpath', SUBMIT_BUTTON_XPATH, clear = False)
        # nav.navHelper.click_selected_element('xpath', SUPPORT_BUTTON_XPATH, clear = False)
        # nav.navHelper.click_selected_element('xpath', DROPDOWN_XPATH, clear = False)
        # nav.navHelper.click_selected_element('xpath', SUBMIT_BUTTON_XPATH, clear = False)
        # nav.navHelper.click_selected_element('xpath', SEARCH_BOX_XPATH, clear = True)
        # nav.input_program_name_into_search()
        # nav.navHelper.click_selected_element('xpath', DROPDOWN_XPATH, clear = False)
        # nav.navHelper.click_selected_element('xpath', SUBMIT_BUTTON_XPATH, clear = False)
        # nav.navHelper.click_selected_element('xpath', SUPPORT_BUTTON_XPATH, clear = False)
        # nav.navHelper.click_selected_element('xpath', DROPDOWN_XPATH, clear = False)
        # nav.navHelper.click_selected_element('xpath', SUBMIT_BUTTON_XPATH, clear = False)
        # nav.navHelper.click_selected_element('xpath', SEARCH_BOX_XPATH, clear =
        nav.navigate_side_bar()
        nav.detect_support_contact_selection_page()


    # auth.sign_in(username_handle_XPATH=username_handle_id, password_handle_XPATH=password_handle_id,auth_code_XPATH=auth_code_id)


if __name__ == '__main__':
    main()





    #wait until support contacts pages
    #identify dropdown page
    #get the range of the dropdown
    #click the two buttons to get to the info page
    #collect data in the tables as key values
    #go to history page
    #collect data in the tables as key values
    #see what does not have and end date
    #optionally ignore if discontinued

    #compare the values in the dictionary
    #if they are the same, continue
    #if they are different, update the