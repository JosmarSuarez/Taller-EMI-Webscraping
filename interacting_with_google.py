from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get("https://google.com")
# Wait until the elements are found
WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'gLFyf')))
# Getting the element using find_element
input_element = driver.find_element(By.CLASS_NAME, "gLFyf")
# Simulating keyboard input using send_keys
input_element.clear()
input_element.send_keys("Escribiendo desde selenium"+ Keys.ENTER)




time.sleep(10)

driver.quit()