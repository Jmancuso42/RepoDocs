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
from end_dates import Authenticator
from end_dates import Navigator
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

#TODO add encapsulation to everything
#TODO add logging
#TODO add error handling
#TODO add docstrings
#TODO add central algorithm for finding elements
#TODO add central algorithm for comparing the info screens

#CONSTANTS
#NOTE env vars was straight up not working at all on this machine, so I'm hardcoding the values in the interest of time :(
HEADER_TEXT = "Support services contacts consumer selection"
DROPDOWN_XPATH = '//*[@id="clientid_INT"]'
FOOTHOLD_USERNAME= 'jmancuso'
FOOTHOLD_PASSWORD = 'Epsilon8279898!'
EDGE_DRIVER_PATH = 'C:\\Users\\jmancuso\\Repos\\migration_end_dates\\msedgedriver.exe'
FOOTHOLD_HOME_URL = 'https://depaul.footholdtechnology.com/awards/home'
AUTH_CODE_ID = 'auth_id'
CHART_XPATH = '//*[@id="q-app"]/div/div[1]/aside/div/div/div[1]/div/div/div[1]/div[2]/a[3]'
LOGIN_XPATH = '//*[@id="handle"]'
PASSWORD_XPATH = '//*[@id="password"]'

# Print all environment variables
load_dotenv(
    dotenv_path='C:\\Users\\jmancuso\\Repos\\RepoDocs\\migration_end_dates\\vars.env'
    
) 
for key, value in os.environ.items():
    print(f"{key}: {value}")


class Navigate:

    def __init__(self, driver,wait, select) -> None:
        self.driver = driver
        self.wait = wait
        self.select = select

    def click_selected_element(self, identifier_type, identifier):
        '''This method clicks an element by id, type, or xpath'''
        element = None
        identifier_type = identifier_type.lower()
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
            logging.error(f"Element not found: {str(e)}")

    def wait_for_detect_support_contact_selection_page(self, driver):

    def detect_support_contact_selection_page(self, driver, wait) -> bool:
        '''Detects if the current page is the support contact selection page'''
        # NOTE Doesn't feel good to hardcode any values ever, but they are constant
        # NOTE dropdown seems to be the most solid way to do this, not many unique IDs on the page
        try:
            header_text_element_hard_xpath = f"//header[text()='{HEADER_TEXT}']"
            # if driver.wait.until(By.XPATH, DROPDOWN_XPATH):
            if self.wait.until(EC.presence_of_element_located((By.XPATH, DROPDOWN_XPATH))):
                logging.info('support page detected on dropdown')
                return True
            elif driver.find_element(By.XPATH, header_text_element_hard_xpath):
                logging.info('support page detected on header text')
                return True
            else:
                logging.info('end of support page detection chain')
                return False
        except NoSuchElementException as e:
            logging.exception(f'No such element ON detect_support page: {str(e)}')
            return False


    def stored_support_page_url(self, driver):
        '''Saves the current support page url and returns it to the caller.
        This is used to return to the support page after data operations are complete'''
        if self.detect_support_contact_selection_page(driver) is True:
            logging.info('saved_support_page_url and returned it to the caller')
            current_support_program_url = driver.current_url()
            return current_support_program_url

        elif self.detect_support_contact_selection_page(driver) is False:
            logging.info('saved_support_page_url returned is false')


    def return_to_support_page(self, driver):
        '''Uses stored_support URL to return to the support page after data operations are complete'''
        support_page_url = self.stored_support_page_url(driver)
        if support_page_url is not None:
            self.driver.get(support_page_url)
            logging.info('returned to support page')


    def click_charts_sidebar_link(self, driver, chart_xpath):
        link_element = driver.find_element(By.XPATH, chart_xpath)
        link_element.click()


    def click_submit_button(self, driver, submit_button_XPATH):
        try:
            submit_button = driver.find_element(By.XPATH, submit_button_XPATH)
            submit_button.click()
        except NoSuchElementException as e:
            logging.exception(f'No such element: {str(e)}')

class Authentication:
        def __init__(self, driver):
            self.driver = driver
    
        def send_username(self, driver, username_handle_XPATH, username = None):
            try:
                username_element = driver.find_element(By.XPATH, username_handle_XPATH)
                username_element.send_keys(username)
            except NoSuchElementException as e:
                logging.exception(f'No such element at username: {str(e)}')    
        def send_password(self, driver, password_handle_XPATH, password = None):
            #TODO add password masking
            #TODO TEST to see if this works with the password parameter
            try:
                password_element = driver.find_element(By.XPATH, password_handle_XPATH)
                password_element.send_keys(password)
            except NoSuchElementException as e:
                logging.exception(f'No such element at password: {str(e)}')
        def wait_for_auth_code(self, driver, auth_code_id):
            try:
                wait(driver, 180).until_not(
                    EC.presence_of_element_located((By.ID, auth_code_id))
                )
            except NoSuchElementException as e:
                logging.exception(f'No such element at auth: {str(e)}')

class DataOperations:
    def __init__(self,driver) -> None:
        self.driver = driver


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
    logging.info(os.getenv('FOOTHOLD_USERNAME'))
    
    #config
    options = webdriver.EdgeOptions()
    options.add_argument(r"--user-data-dir=C:\\Users\\jmancuso\\AppData\\Local\\Microsoft\\Edge\\User Data\\Profile 1")
    options.add_argument(r"--profile-directory=Profile 1")
    service = Service('C:\\Users\\jmancuso\\Repos\\RepoDocs\\migration_end_dates\\msedgedriver.exe')
    driver = webdriver.Edge(options=options, service=service)
    auth = Authentication(driver)

    
    driver.get('https://depaul.footholdtechnology.com')
    logging.info('got foothold')
    auth.send_username(driver, LOGIN_XPATH, FOOTHOLD_USERNAME)
    auth.send_password(driver, PASSWORD_XPATH, FOOTHOLD_PASSWORD)
\
        

    




    wait(driver, 90).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="q-app"]/div/div[2]/main/div/div/div[1]/div[1]/h1'))
    )
    click_charts_sidebar_link(driver, chart_xpath)






    # auth.sign_in(username_handle_XPATH=username_handle_id, password_handle_XPATH=password_handle_id,auth_code_XPATH=auth_code_id)


if __name__ == '__main__':
    main()