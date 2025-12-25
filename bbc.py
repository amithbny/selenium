from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from model import summarize

WAIT_TIME = 8
ARTICLE_URL = "https://www.bbc.com/"
MAX_LINKS = 3

service = Service("chromedriver.exe")
driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver, WAIT_TIME)

def get_first_300_words(driver):
    paragraphs = driver.find_elements(By.TAG_NAME, "p")
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
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service)

    driver.get("https://bbc.com/news")

    wait = WebDriverWait(driver,15)

    links = wait.until(
        EC.presence_of_all_elements_located(
            (By.XPATH,"//a[contains(@href,'/news/') and not(@data-testid='subNavigationLink')]")
        )
    )

    link = []
    for a in links:
        href = a.get_attribute("href")
        if href and href not in links:
            link.append(href)

    articles = []
    for a in link[:5]:
        driver.get(a)
        heading = wait.until(
            EC.presence_of_element_located(
                (By.XPATH,"//div[@data-component='headline-block']//h1")
            )
        )
        all_text = wait.until(
            EC.presence_of_all_elements_located(
                (By.XPATH,"//div[@data-component='text-block']//p")
            )
        ) 
        full = heading.text + "\n"
        for i in all_text:
            full = full +  i.text + "\n"
        articles.append(full)
        time.sleep(2)

finally:
    driver.quit()
