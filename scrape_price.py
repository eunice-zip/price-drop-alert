import csv
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


#chromedriver path
service = Service("chromedriver.exe")

options = Options()
options.add_argument("--headless")

driver = webdriver.Chrome(service=service, options=options)

def get_price(url):
    driver = webdriver.Chrome()
    driver.get(url)

    try:
        
        price = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".h-currency.h-currency-red"))
        ).text
    except TimeoutException:
        try:
            # no discount, find original price
            price = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".origin-price .h-currency"))
            ).text
        except TimeoutException:
            price = "can't find price tag"

    
    return price

def save_to_csv(price, file_path):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(file_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        
        if f.tell() == 0:
            writer.writerow(["Time", "Current Price"])
        writer.writerow([now, price])

# input item url
url = "https://www.uniqlo.com/tw/zh_TW/"
price = get_price(url)
#print("current price is:", price)


save_to_csv(price, "price_history.csv")
driver.quit()