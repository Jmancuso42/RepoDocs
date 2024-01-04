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




# Usually don't use globals, but this is a quick and dirty script.
# Specify the path to the Edge driver executable
driver_path = 'msedgedriver.exe'
options = Options()
options.add_argument('--remote-debugging-port=9222')
service = Service(driver_path)
#driver = webdriver.Edge(service=service, options=options)



def sign_in():
    

     # Enter the predefined username and password
    username = "jmancuso"
    password = "Epsilon8279898!"
    
    # Find the username and password input fields
    username_input = wait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'handle'))
    )
    password_input = wait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'password'))
    )
    
    # Clear the input fields (optional)
    username_input.clear()
    password_input.clear()
    
    # Enter the username and password
    username_input.send_keys(username)
    password_input.send_keys(password)
    
    # Find and click the sign in button
    sign_in_button = wait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit'][name='submitbtn']"))
    )
    sign_in_button.click()

def first_form_click(driver): 
    dropdown = Select(driver.EC.presence_of_element_located((By.ID, 'clientid_INT')))


# Wait until the dropdown is available to interact with.
   wait(driver, 10).until(EC.presence_of_element_located((By.ID, 'clientid_INT'))
        
    
    dropdown.select_by_index()
    

# Select an option from the dropdown.

# Click the first button.
    first_button = wait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit']"))
    )
    first_button.click()

def config_driver_default_instance_():
    


# # Wait for the second button to be clickable, then click it.
# second_button = wait(driver, 10).until(
#     EC.element_to_be_clickable((By.ID, 'SECOND_BUTTON_ID_OR_NAME'))
# )
# second_button.click()



# Check if the browser is already open
try:
    # Try to connect to an existing instance of the browser
    driver = webdriver.Remote(command_executor='http://localhost:9222', options=options)
except WebDriverException:
    # If the browser is not already open, open a new instance
    driver = webdriver.Edge(service=service, options=options)
except Exception:
    driver = webdriver.Edge(service=service, options=options)

# Navigate to the desired URL
# Specify the path to the Edge driver executable

# Navigate to the desired URL

#If there's an element from their login, sign in
# If there's an element from their 2fa, wait for action 
try:
    driver.get('https://depaul.footholdtechnology.com') 
    if EC.presence_of_element_located((By.ID, 'handle')):
        sign_in()
        #if 2fa, wait for action
    if EC.presence_of_element_located((By.ID, 'auth-code')):
        print("waiting for 2fa")
        wait(driver,60).until_not(EC.presence_of_element_located((By.ID, 'auth-code'))) 

    driver.get('https://depaul.footholdtechnology.com/awards/charts/medical/support_services_contacts')
    wait(driver,45).until(method=EC.presence_of_element_located((By.ID, 'clientid_INT')))
    first_form_click()
except WebDriverException:
    # If the specified address cannot be reached, get the current address from the open active instance
    current_address = driver.current_url
    print(f"Failed to reach the specified address. Current address: {current_address}")

    manual_url = input("Failed to reach the specified address. enter url manually and press enter")
    driver.get(manual_url)
except Exception:
    driver.get('https://depaul.footholdtechnology.com')
    sign_in()

first_form_click()

done_list = []
list_index = 0

# Rest of your code...

# wait(driver, 65)


# Close the browser window.
print('Done.')








#scs/ssc?fs=L3BhcnNlci5waHA%2FcHJvdmlkZXJzX3BocF9SVU49JnByb2duYW1lX2NoYXI9VXBwZXIrRmFsbHMmcGdyb3VwX2ludD0wJmdsY29faW50PTAmZ2xkaXZfaW50PTAmcHJvZ3NldF9sb2dpPXllcyZ1bj0yMDc3NzYwMDgmdGltZT0xNzA0MjI4Nzg1NTE5')