from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


QUERY = "wikipedia"
WAIT_TIME = 5

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver,WAIT_TIME)

try:
    driver.get("https://www.cnn.com/search?q=wikipedia")

    search_io = wait.until(
        EC.element_to_be_clickable((By.NAME,"q"))
    )
    
    search_io.send_keys(QUERY + Keys.ENTER)

    wait.until(EC.title_contains("Search"))

finally:
    driver.quit()