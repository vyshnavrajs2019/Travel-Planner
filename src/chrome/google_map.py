import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

GOOGLE_URL = 'https://www.google.com/maps/'
DELAY_TIME = 20

def create_driver():
	chrome_options = webdriver.ChromeOptions()
	prefs = {"profile.managed_default_content_settings.images": 2}
	chrome_options.add_experimental_option("prefs", {})
	driver = webdriver.Chrome(chrome_options=chrome_options)
	driver.set_page_load_timeout(DELAY_TIME)
	driver.implicitly_wait(DELAY_TIME)
	return driver

def get_url(driver, path):
	driver.get(GOOGLE_URL + path)
	time.sleep(2)
