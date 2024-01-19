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
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (NoSuchElementException, TimeoutException, ElementClickInterceptedException,
ElementNotInteractableException, ElementNotVisibleException, ElementNotSelectableException, InvalidElementStateException)





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
FOOTHOLD_USERNAME= 'jmancuso'
FOOTHOLD_PASSWORD = 'Epsilon8279898!'
EDGE_DRIVER_PATH = 'C:\\Users\\jmancuso\\Repos\\migration_end_dates\\msedgedriver.exe'
FOOTHOLD_HOME_URL = 'https://depaul.footholdtechnology.com/awards/home'

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
# '//input[contains(@class, "q-field__input") and @type="search"]')   #NOTE this uses contains
SEARCH_BOX_CSS = "input.q-field__input.q-placeholder.col"
# SEARCH_BOX_CSS = "input.q-field__input.q-placeholder.col"
# 'input.q-field__input.q-placeholder.col[type="search"]'

#NOTE dont need these frame paths to be constants but its good practice to not use magic strings
PARENT_FRAME_XPATH = "//*[contains(@id, 'ng-app')]"
CHILD_FRAME_XPATH = "//*[contains(@id, 'awards_classic_iframe')]"
# Print all environment variables
load_dotenv(
    dotenv_path='C:\\Users\\jmancuso\\Repos\\RepoDocs\\migration_end_dates\\vars.env'
)  #NOTE cannot get to work

class Navigate:
    def __init__(self,driver,wait,select,NavigateHelpers, iteration = None):
        '''This class contains methods for navigating the Foothold application.
        The iteration parameter is used to select the correct dropdown option based on the current i in range of the loop'''
        driver = driver
        wait = wait
        select = select
        iteration = iteration
        self.current_support_prog_return_url = None
        self.navHelper = NavigateHelpers(self, Navigate)
        # self.select = select

    class NavigateHelpers:
        def __init__(self,outer_instance) -> None:
            self.outer_instance = outer_instance
            self.driver = self.outer_instance.driver
            self.wait = self.outer_instance.wait
            self.select = self.outer_instance.select
            self.iteration = self.outer_instance.iteration



    def get_return_url(self):
        return self.return_url
    def set_return_url(self, url):
        self.return_url = url

    def detect_home_page(self, driver,url):
        '''Detects if the current page is the home page
        url is to be the URL of the home page'''
        #NOTE this might not be needed at because this will be semi automated
        wait(driver, 20).until(EC.url_to_be(url))
        if driver.current_url == FOOTHOLD_HOME_URL:
            logging.info('home page detected')
            return True
        else:
            logging.info('home page not detected')
            return False
    def click_submit_button(self, driver):
        try:
            submit_button = driver.find_element(By.NAME, SUBMIT_BUTTON_NAME)
            if submit_button:
                logging.info('submit button found')
                submit_button.click()
        except NoSuchElementException as e:
            #  NoSuchElementException(f"No such element: {e.msg}") from e
            logging.error(f'No such element: {e.msg}')
        except TypeError as e:
            logging.exception(f'Type error: {str(e)}')
        except TimeoutException as e:
            logging.error(f'Timeout error: {str(e)}')

    def input_program_name_into_search(self, wait, driver, program_input=None):
        #NOTE 'q-input__inner' is the search box css element
        # search_box_find = driver.find_element(By.CSS_SELECTOR, SEARCH_BOX_CSS)
        
        inner_box = '.q-input__inner'
        search_box = wait(driver,5).until(EC.presence_of_element_located((By.CSS_SELECTOR, SEARCH_BOX_CSS)))
        
        if program_input is None:
            program_input = input("Enter program input: ")  # Wait for user input
        try:
            # wait(driver,5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '\
            #     input.q-field__input.q-placeholder.col\
            #     [type="search"]')))
            wait(driver,6).until(EC.element_to_be_clickable((search_box)))
            self.clear_selected_element(driver, 'css',inner_box)
            self.click_selected_element(driver, 'css', inner_box)
            search_box.send_keys(program_input)
            logging.info('program input entered into search box')

        except NoSuchElementException as e:
            logging.error(f'No such element @ search input: {e.msg}')
        except TimeoutException as e:
            logging.exception(f'Timeout error @ search input: {e.msg}')
        except AttributeError as e:
            logging.error(f'Attribute error @ search input: {str(e)}')

    def navigate_side_bar(self, wait, driver, program_input=None):
        '''This method clicks the charts sidebar link and then the medical records link, takes input
        from the user, and then selects the first item in the dropdown list'''
        #NOTE the hardcoding is not great, but it is consistent
        #TODO if cleaning up, break this into 4 methods
        #NOTE '.q-menu' is the list, '.q-item' is the item. maybe add these to constants or vars
        try:
            #click charts link
            self.click_selected_element(driver, 'xpath', CHART_SIDEBAR_XPATH)
            logging.info('clicked charts link')


            #enter program input into search box
            self.input_program_name_into_search(wait, driver, program_input)
            
            #TODO if cleaning up, refactor this chunk with the helper select method
            # Select the first item in the dropdown list, q-menu is the list, q-item is the item
            wait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.q-menu')))
            first_item = driver.find_element(By.CSS_SELECTOR,('.q-menu .q-item'))
            wait(driver, 15).until(EC.element_to_be_clickable(first_item))
            first_item.click()
            logging.info('clicked first item in dropdown list')

            #click medical records link
            self.click_selected_element(driver, 'xpath', MEDICAL_BUTTON_XPATH)
            logging.info('clicked medical records link')
            
            #NOTE this is the old way of doing it
            # wait(driver, 5).until(EC.element_to_be_clickable((By.XPATH,MEDICAL_CHART_XPATH)))
            # medical_records_element = driver.find_element(By.XPATH, MEDICAL_CHART_XPATH)
            # medical_records_element.click()
            # logging.info('clicked medical records link')

            #select support button
            self.click_selected_element(driver, 'xpath', SUPPORT_BUTTON_XPATH)
            logging.info('clicked support button')
            #old way of doing it
            # wait(driver, 8).until(EC.presence_of_element_located((By.XPATH, support_button_xpath)))
            # wait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, SUPPORT_BUTTON_XPATH)))
            # support_button_element = driver.find_element(By.XPATH, SUPPORT_BUTTON_XPATH)
            # support_button_element.click()

        except NoSuchElementException as e:
            logging.error(f'No such element: {e.msg}')
        except TimeoutException as e:
            logging.error(f'Timeout error: {e.msg}')

    def detect_support_contact_selection_page(self, driver, wait):
        '''Detects if the current page is the support contact selection page'''
        try:

            # Switch to iframe
            driver.switch_to.frame(wait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@id, 'ng-app')]"))))
            driver.switch_to.frame(wait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@id, 'awards_classic_iframe')]"))))

            dropdown_element = wait(driver, 5).until(EC.presence_of_element_located((By.XPATH, DROPDOWN_XPATH)))
            if dropdown_element:
                self.current_support_prog_return_url = driver.current_url()
                logging.info('support page detected')
                return True            
            logging.info('end of support page detection chain')
            return False
        except NoSuchElementException as e:
            logging.exception(f'No such element: detect support contact selection page {e.msg}')
            raise NoSuchElementException(f"No such element: {e.msg}")
        except TimeoutException as e:
            logging.exception(f'Timeout error: {e.msg}')
            # raise TimeoutException(f"Timeout error: {e.msg}") from e


    def get_range_of_dropdown(self, driver, select) -> int:
        #TODO move to navigate helpers
        '''This method gets the range of the dropdown element and returns it to the caller
        to be used as the range of the loop'''
        dropdown_range = len(select(driver.find_element(By.XPATH, DROPDOWN_XPATH)).options)
        logging.info(f'got range of dropdown: {dropdown_range}')
        return dropdown_range

    def select_dropdown_option(self, driver, select, iteration=None):
        #TODO move to navigate helpers
        '''This method selects a dropdown element and selects the option by index. If no 
        index is passed, it selects the first option with the 0 index. logs the selection'''
        select(driver.find_element(By.XPATH, DROPDOWN_XPATH)).select_by_index(iteration or 0)
        logging.info(f'selected dropdown option by {"iteration" if iteration else "default"}')

    def click_selected_element(self, driver, identifier_type, identifier):
        #TODO move to navigate helpers
        '''This helper method clicks an element by id, type, or xpath'''
        element = None
        identifier_type = identifier_type.lower()
        try:
            locator = (getattr(By, identifier_type.upper()), identifier)
            wait(driver, 10).until(EC.presence_of_element_located(locator))
            element = driver.find_element(*locator)
            if element:
                element.click()
        except NoSuchElementException as e:
            # raise NoSuchElementException(f"No such element: {e.msg}") from e
            logging.error(f'No such element: {e.msg}')
        except TypeError as e:
            logging.error(f"Type error: {str(e)}")
        except AttributeError as e:
            logging.error(f"Attribute error: {str(e)}")

    def clear_selected_element(self, driver, identifier_type, identifier):
        #TODO move to navigate helpers
        '''This helper method clears an element by id, type, or xpath'''
        element = None
        identifier_type = identifier_type.lower()
        try:
            locator = (getattr(By, identifier_type.upper()), identifier)
            wait(driver, 10).until(EC.presence_of_element_located(locator))
            element = driver.find_element(*locator)
            if element:
                element.click()
                element.clear()  # Clear the element's value
        except NoSuchElementException as e:
            # raise NoSuchElementException(f"No such element: {e.msg}") from e
            logging.error(f'No such element: {e.msg}')
        except TypeError as e:
            logging.error(f"Type error: {str(e)}")
        except AttributeError as e:
            logging.error(f"Attribute error: {str(e)}")

    
class Authentication:
    def __init__(self, driver, wait):
        driver = driver
        wait = wait

    def send_username(self, driver, username_handle_XPATH, username=None):
        try:
            username_element = driver.find_element(By.XPATH, username_handle_XPATH)
            username_element.send_keys(username)
        except NoSuchElementException as e:
            # raise NoSuchElementException from e
            logging.error(f'No such element: {e.msg}')

    def send_password(self, driver, password_handle_XPATH, password=None):
        #TODO add password masking
        #TODO TEST to see if this works with the password parameter
        try:
            password_element = driver.find_element(By.XPATH, password_handle_XPATH)
            password_element.send_keys(password)
        except NoSuchElementException as e:
            # raise NoSuchElementException
            logging.error(f'No such element: {e.msg}')

    def wait_for_auth_code(self, driver):
        try:
            wait(driver, 120).until_not(
                EC.presence_of_element_located((By.XPATH, AUTH_CODE_XPATH))
            )
        except NoSuchElementException as e:
            # raise NoSuchElementExceptio
            logging.error(f'No such element: {e.msg}')
class CleanUp:
    def __init__(self, driver, wait, select, iteration = None, drange = None,history_dict = None, info_dict = None):
        driver = driver
        wait = wait
        select = select
        iteration = iteration
        drange = drange
        self.navigate = Navigate(driver, wait, select, iteration)


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
    auth = Authentication(driver,wait)
    nav = Navigate(driver, wait, select, NavigateHelpers)
    # driver.implicitly_wait(1)

    driver.get('https://depaul.footholdtechnology.com')
    logging.info('got foothold')
    #TODO add control flow to login stuff
    auth.send_username(driver, LOGIN_XPATH, FOOTHOLD_USERNAME)
    auth.send_password(driver, PASSWORD_XPATH, FOOTHOLD_PASSWORD)
    nav.click_submit_button(driver)
    auth.wait_for_auth_code(driver)
    if nav.detect_home_page(driver, FOOTHOLD_HOME_URL) is True:

        # program = input("Enter the program name: ")
        nav.navigate_side_bar(wait, driver)

        nav.detect_support_contact_selection_page(driver, wait)


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