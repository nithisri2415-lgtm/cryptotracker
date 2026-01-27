from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
from datetime import datetime

# Chrome options
options = Options()
options.add_argument("--start-maximized")  # maximize browser window

# Chrome browser open
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

# CoinMarketCap page open
driver.get("https://coinmarketcap.com/")
time.sleep(5)  # wait page load

# Scrape top 10 crypto coins
rows = driver.find_elements("xpath", "//table/tbody/tr")
crypto_data = []

for row in rows[:10]:
    try:
        name = row.find_element("xpath", ".//p[contains(@class,'coin-item-symbol')]").text
        price = row.find_element("xpath", ".//td[4]").text
        change = row.find_element("xpath", ".//td[5]").text
        market_cap = row.find_element("xpath", ".//td[7]").text
        crypto_data.append([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), name, price, change, market_cap])
    except:
        continue

# Save data to CSV
df = pd.DataFrame(crypto_data, columns=["Time", "Coin", "Price", "24h Change", "Market Cap"])
df.to_csv("crypto_prices.csv", index=False)

# Close browser
driver.quit()
print("CSV file created successfully")