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
    driver.get("https://cnn.com")

    element = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME,"header__search-icon"))
    )

    element.clear()
    element.send_keys(QUERY + Keys.ENTER)

    link = wait.until(EC.presence_of_element_located((
        By.PARTIAL_LINK_TEXT,"google"
    )))
    link.click()
    # wait.until(EC.title_contains("Headphone Zone"))
finally:
    driver.quit()