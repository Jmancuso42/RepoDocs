from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
import logging
import os
from dotenv import load_dotenv
from end_dates import Authenticator







def main():
    # load_dotenv()
    logging.basicConfig(filename='dirty_end_dates.log', level=logging.INFO)
    logging.info('Started')
    options = webdriver.EdgeOptions()
    # path = os.getenv('EDGE_DRIVER_PATH')
    service = Service('C:\\Users\\jmancuso\\Repos\\RepoDocs\\migration_end_dates\\msedgedriver.exe')
    driver = webdriver.Edge(options=options, service=service)
    username_handle_id = 'handle'
    password_handle_id = 'password'
    auth = Authenticator(driver)

    
    driver.get('https://depaul.footholdtechnology.com')
    wait(driver, 60).until(
        EC.title_contains('Foothold Technology')
    )
    auth.sign_in(username_handle_id=username_handle_id, password_handle_id=password_handle_id,auth_code_id='auth_code')



if __name__ == '__main__':
    main()