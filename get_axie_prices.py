import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from apscheduler.schedulers.blocking import BlockingScheduler

from bs4 import BeautifulSoup
import pandas as pd
import numpy as np 
import datetime


# Create driver
def create_driver(path='C:/Users/srdes/Desktop/Axie_Infinity/chromedriver_win32/chromedriver.exe', url='https://axieinfinity.com/'):
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_argument("--disable-blink-features=AutomationControlled")
	# chrome_options.add_argument('headless')
	# chrome_options.add_argument('window-size=1920x1080')
	# chrome_options.add_argument("disable-gpu")
	
	driver = webdriver.Chrome(executable_path=path, options=chrome_options)  # Optional argument, if not specified will search path.
	# access axie infinity
	driver.set_window_position(-10000,0)
	driver.get(url)

	# time.sleep(5) # Wait for page to load

	return driver

def open_marketplace(driver):

	element = driver.find_element_by_link_text("Marketplace")
	element.click()

	time.sleep(15) # Wait for page to load

	driver.switch_to.window(driver.window_handles[-1])

	return driver

def get_price(driver, url):

	driver.get(url)
	time.sleep(10) # Loading page
	axie_box = driver.find_elements_by_class_name('axie-card')
	price_list = []
	for box in axie_box:
		box_html = box.get_attribute('innerHTML')
		soup = BeautifulSoup(box_html)
		for d in soup.findAll('h6',attrs={'class':'truncate ml-8 text-gray-1 font-medium'}):
			price_list.append(float(d.get_text().replace('$','').replace(',','')))
	median = np.median(price_list)
	max_ = np.max(price_list)
	min_ = np.min(price_list)

	return price_list, min_, max_, median



	return driver

def main():
	print('starting '+ str(datetime.datetime.now()))
	

	driver = create_driver(path='C:/Users/srdes/Desktop/Axie_Infinity/chromedriver_win32/chromedriver.exe', url='https://axieinfinity.com/')
	driver = open_marketplace(driver)

		# Pull filters
	pull_dict = {
	'plant':'https://marketplace.axieinfinity.com/axie?part=tail-carrot&part=mouth-serious&part=horn-cactus&part=back-pumpkin&pureness=6',
	'bird':'https://marketplace.axieinfinity.com/axie?part=back-raven&part=mouth-hungry-bird&part=horn-kestrel&part=tail-post-fight&pureness=6',
	'beast':'https://marketplace.axieinfinity.com/axie?part=back-ronin&part=mouth-goda&part=horn-imp&part=tail-cottontail&pureness=6',
	'aqua':'https://marketplace.axieinfinity.com/axie?part=back-goldfish&part=mouth-risky-fish&part=horn-shoal-star&part=tail-navaga&pureness=6'
	}

	for key in pull_dict:
		url = pull_dict[key]

		price_list, min_, max_, median = get_price(driver, url)

		date_col = [datetime.datetime.now().strftime("%Y%m%d-%H%M")] * len(price_list)
		
		df = {'price':price_list, 'date':date_col, 'min':min_,'max':max_,'median':median}

		df_master = pd.read_csv('data/'+key+'_master.csv')
		df_new = pd.DataFrame(df)
		df_master = df_master.append(df_new, ignore_index=True)
		df_master.to_csv('data/'+key+'_master.csv',index=False)

	driver.quit()
	print('finished')

if __name__ == "__main__":
	main()
	scheduler = BlockingScheduler()
	scheduler.add_job(main, 'interval', hours=.25)
	scheduler.start()

