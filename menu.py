from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

WAIT_TIME = 2
MAX_LINKS = 8
# START_URL = "https://w3schools.com"  
START_URL = "https://selenium-python.readthedocs.io/navigating.html#interacting-with-the-page"  

service = Service("chromedriver.exe")
driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver, WAIT_TIME)

def open_menu_if_present(driver):
    selectors = [
        "button[aria-label*='menu']",
        "button[aria-label*='Menu']",
        "button[class*='menu']",
        "button[class*='nav']",
        "div[class*='menu']",
        "a[class*='menu']",
    ]

    for sel in selectors:
        try:
            btn = driver.find_element(By.CSS_SELECTOR, sel)
            if btn.is_displayed():
                driver.execute_script("arguments[0].click();", btn)
                time.sleep(1)
                return
        except:
            pass


def collect_nav_links(driver, base_url, limit):
    links = driver.find_elements(By.TAG_NAME, "a")
    nav_links = []

    for link in links:
        try:
            text = link.text.strip()
            href = link.get_attribute("href")

            if (
                href
                and href.startswith("http")
                and base_url in href
                and len(text) > 1
                and len(text.split()) <= 4   
            ):
                nav_links.append((text, href))
        except:
            continue

        if len(nav_links) == limit:
            break
    print(nav_links)
    return list(dict.fromkeys(nav_links))

try:
    driver.get(START_URL)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    open_menu_if_present(driver)

    base_domain = START_URL.split("//")[1].split("/")[0]

    nav_links = collect_nav_links(driver, base_domain, MAX_LINKS)

    print("Navigation options found:")
    for text, _ in nav_links:
        print("-", text)

    for text, url in nav_links:
        print(f"\nVisiting: {text}")
        driver.get(url)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        time.sleep(2)

        # print("⬅️ Returning to home")
        # driver.get(START_URL)
        # wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

finally:
    driver.quit()
