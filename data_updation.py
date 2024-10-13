from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_all_elements_located
from selenium.webdriver.chrome.options import Options

options = Options()
# options.add_argument("--headless")  # Run in headless mode (no GUI)
options.add_argument("--no-sandbox")  # Prevent issues with sandboxing in Linux environments
options.add_argument("--disable-dev-shm-usage")  # Use /tmp instead of /dev/shm to avoid memory issues
options.add_argument("--remote-debugging-port=9222")  # Required for headless Chrome to avoid DevToolsActivePort error
options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration


driver = webdriver.Chrome(options=options)

# Configure the webdriver to use Chrome
#driver = webdriver.Chrome()

# Navigate to the match page
driver.get("https://www.iplt20.com/match/2024/1439")

# Wait for the ball-by-ball co
# mmentary to load
wait = WebDriverWait(driver, 5)
ball_elements = wait.until(presence_of_all_elements_located((By.CSS_SELECTOR, "p.cmdOver.mcBall")))
commentary_start = wait.until(presence_of_all_elements_located((By.CSS_SELECTOR, "div.commentaryStartText.ng-binding.ng-scope")))
commentary_text = wait.until(presence_of_all_elements_located((By.CSS_SELECTOR, "div.commentaryText.ng-binding")))

# Get the text of the ball-by-ball commentary and commentary start and text
ball_values = []
for i in range(len(ball_elements)):
    ball_number = ball_elements[i].text.split('\n')[0]
    ball_value = ball_elements[i].text.split('\n')[1]
    start = commentary_start[i].text
    text = commentary_text[i].text
    ball_values.append([ball_number,ball_value, start, text])

# Print the ball values
for ball in ball_values:
    print(ball)

# Close the webdriver
driver.quit()