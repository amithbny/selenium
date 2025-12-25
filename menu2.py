from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

START_URL = "https://developer.mozilla.org/en-US/"
WAIT_TIME = 5
MAX_LINKS = 2

service = Service("chromedriver.exe")
driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver, WAIT_TIME)

def open_menu(driver):
    menu_selectors = [
        "button[aria-label*='menu']",
        "button[class*='menu']",
        "div[class*='menu']",
        "a[class*='menu']"
    ]

    for selector in menu_selectors:
        try:
            menu_button = driver.find_element(By.CSS_SELECTOR, selector)
            if menu_button.is_displayed():
                menu_button.click()
                time.sleep(1)
                break
        except:
            pass 

def get_nav_links(driver, domain):
    links = driver.find_elements(By.TAG_NAME, "a")
    nav_links = []

    for link in links:
        text = link.text.strip()
        href = link.get_attribute("href")

        if text and href and domain in href:
            nav_links.append((text, href))

        if len(nav_links) == MAX_LINKS:
            break

    return nav_links


try:
    driver.get(START_URL)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    open_menu(driver)

    domain = START_URL.replace("https://", "").replace("http://", "")

    nav_links = get_nav_links(driver, domain)

    print("Navigation options found:")
    for text, _ in nav_links:
        print("-", text)

    for text, url in nav_links:
        print(f"\nOpening: {text}")
        driver.get(url)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        time.sleep(2)   

    print("Returning to home")
    driver.get(START_URL)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    input("")
finally:
    driver.quit()
