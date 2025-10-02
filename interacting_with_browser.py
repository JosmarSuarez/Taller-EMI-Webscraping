from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get("https://duckduckgo.com")
# Wait until the elements are found
WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'searchbox_input__rnFzM')))
# Getting the element using find_element
input_element = driver.find_element(By.CLASS_NAME, "searchbox_input__rnFzM")
# Simulating keyboard input using send_keys
input_element.clear()
input_element.send_keys("trabajopolis"+ Keys.ENTER)


# Find with partial text from a link
WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "trabajopolis.bo"))
)
link = driver.find_element(By.PARTIAL_LINK_TEXT, "trabajopolis.bo")
link.click()

time.sleep(10)
driver.quit()