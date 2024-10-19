from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")  # Run Chromium in headless mode
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# No need to specify the driver path; Selenium Manager will handle it.
driver = webdriver.Chrome(options=options)

# Example usage
driver.get("https://www.google.com")
print(driver.title)

driver.quit()