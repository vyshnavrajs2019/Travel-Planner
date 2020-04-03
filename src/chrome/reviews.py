import time, json
from .google_map import create_driver, get_url
from collections import defaultdict

CONFIG_FILE = 'chrome/config.json'
USER_DB_FILE = 'chrome/user_db.json'

user_reviews = defaultdict(dict)
config = {}

def load_data():
	global user_reviews
	global config
	with open(CONFIG_FILE) as conf:
		config = json.loads(conf.read())
	with open(USER_DB_FILE) as user_db:
		user_reviews = json.loads(user_db.read())
	return config['INDEX']

def get_place(driver, place):
	base_path = 'search/'
	path = base_path + place + "/"
	get_url(driver, path)

def get_user_id(url):
	parts = url.split("https://www.google.com/maps/contrib/")[1]
	parts = parts.split("?")[0]
	return parts

def click_on_all_reviews(driver):
	count = 0
	button = None
	while count < 5:
		try:
			time.sleep(2)
			button = driver.find_elements_by_css_selector("button.jqnFjrOWMVU__button")[0]
			break
		except:
			count += 1
			if count == 5:
				return False
	button.click()
	return True
	
def collect_all_reviews(driver, place, index):
	config['INDEX'] = index
	try:
		time.sleep(5)
		prev = None
		length = 0
		while prev != length:
			driver.execute_script("let svrDiv = document.querySelector('div.section-layout.section-scrollbox.scrollable-y.scrollable-show');svrDiv.scrollTo(0, svrDiv.scrollHeight);")
			reviews = driver.find_elements_by_css_selector("div.section-review")
			prev = length
			length = len(reviews)
			time.sleep(5)

		reviews = driver.find_elements_by_css_selector("div.section-review")
		for review in reviews:
			user_url = review.find_elements_by_css_selector("a.section-review-link")[0].get_attribute('href')
			user_id = get_user_id(user_url)
			ratings = review.find_elements_by_css_selector("span.section-review-stars")[0]
			rating = len(ratings.find_elements_by_css_selector("span.section-review-star-active"))
			if user_reviews.get(user_id):
				user_reviews[user_id][place] = rating
			else:
				user_reviews[user_id] = {}
				user_reviews[user_id][place] = rating
		print(len(reviews), 'reviews collected from', place)
	except Exception as e:
		print("EXCEPTION")
		print(e)
	
	with open(USER_DB_FILE, 'w') as user_db:
		user_db.write(json.dumps(user_reviews))

	with open(CONFIG_FILE, 'w') as conf:
		conf.write(json.dumps(config))