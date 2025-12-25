from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("https://google.com")
link = WebDriverWait(driver,25).until(
    EC.presence_of_element_located((By.CLASS_NAME,"gLFyf"))
)
link.clear()
link.send_keys("amith benny" + Keys.ENTER)

im = WebDriverWait(driver,25).until(
    EC.presence_of_element_located((By.PARTIAL_LINK_TEXT,"Amith Benny"))
)
im.click()
WebDriverWait(driver,10).until(EC.title_contains("Instagram"))
driver.quit()