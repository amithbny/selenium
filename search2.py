from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from model import summarize

WAIT_TIME = 5
ARTICLE_URL = "https://en.wikipedia.org/wiki/Lionel_Messi"
MAX_LINKS = 50

service = Service("chromedriver.exe")
driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver, WAIT_TIME)

def get_first_300_words(driver):
    paragraphs = driver.find_elements(By.CSS_SELECTOR, "#bodyContent p")

    words = []
    for p in paragraphs:
        text = p.text.strip()
        if text:
            words.extend(text.split())

        if len(words) >= 300:
            break

    return " ".join(words[:300])

try:
    driver.get(ARTICLE_URL)

    wait.until(
        EC.presence_of_element_located((By.ID, "bodyContent"))
    )

    links = driver.find_elements(
        By.CSS_SELECTOR,
        "#bodyContent a[href]"
    )
    
    visited = []
    for i in range(MAX_LINKS):
        visited.append(links[i].get_attribute("href"))

    for i in visited:
        driver.get(i)
        wait.until(EC.presence_of_element_located((By.ID, "bodyContent")))

        text = get_first_300_words(driver)
        summary = summarize(text)

        with open("summary.txt", "a", encoding="utf-8") as f:
            f.write(f"Source URL: {i}\n")
            f.write(summary + "\n\n")

        time.sleep(1)

        driver.get(ARTICLE_URL)
        wait.until(EC.presence_of_element_located((By.ID, "bodyContent")))

finally:
    driver.quit()

