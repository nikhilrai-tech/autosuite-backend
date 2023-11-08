from selenium import webdriver

# Create ChromeOptions and add arguments as needed
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')  # Run in headless mode to avoid opening a visible browser window

# Initialize the Chrome WebDriver with the specified options
driver = webdriver.Chrome(options=chrome_options)

# Get the path to the ChromeDriver executable
driver_path = driver.service.process.pid

# Print the path to ChromeDriver
print("Path to ChromeDriver executable:", driver_path)

# Quit the WebDriver
driver.quit()
