from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import csv
import re
import time
from bs4 import BeautifulSoup
import requests

req_headers = {
	'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	'accept-encoding': 'gzip, deflate, br',
	'accept-language': 'en-US,en;q=0.8',
	'upgrade-insecure-requests': '1',
	'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}


prefs = {'profile.default_content_setting_values': {'cookies': 2, 'images': 2, 'javascript': 2, 
                            'plugins': 2, 'popups': 2, 'geolocation': 2, 
                            'notifications': 2, 'auto_select_certificate': 2, 'fullscreen': 2, 
                            'mouselock': 2, 'mixed_script': 2, 'media_stream': 2, 
                            'media_stream_mic': 2, 'media_stream_camera': 2, 'protocol_handlers': 2, 
                            'ppapi_broker': 2, 'automatic_downloads': 2, 'midi_sysex': 2, 
                            'push_messaging': 2, 'ssl_cert_decisions': 2, 'metro_switch_to_desktop': 2, 
                            'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement': 2, 
                            'durable_storage': 2}}

chrome_options = Options()
chrome_options.add_argument("--headless")
#chrome_options.add_experimental_option('prefs', prefs)
#chrome_options.add_argument("start-maximized")
#chrome_options.add_argument("disable-infobars")
#chrome_options.add_argument("--disable-extensions")
#chrome_options.add_argument("--no-sandbox")
#chrome_options.add_argument("--disable-dev-shm-usage")
#chrome_options.add_argument("--disable-gpu")


### the following function is for ask search engine and can be swapped out if necessary

def get_ask(name,url):
	name_split = name.split('+')
	name = name_split[0]
	print(name)
	links = []
	counter = 0
	with requests.Session() as sess:
		res = sess.get(url,headers=req_headers)
		soup = BeautifulSoup(res.content, 'lxml')
		comp = soup.find_all('a',{'class':'result-link'})
		for co in comp:
			try:
				href_text = co.text
				if 'Supply' in href_text or 'Supplies' in href_text: 
					href = co['href']
					links.append(href)

					print(href_text)
			except:
				print('did not load')
	if len(links) < 3:
		while len(links) < 3:
			links.append('unable to find additional link')
	return links


### the following function scrapes Google

domains_to_avoid = ['school-supply-list', 'teacherlists', 'supplylist', 'myschoolsupplylists']

def get_goog(url):
	links = []
	service = Service(executable_path="chromedriver.exe")
	mydriver = webdriver.Chrome(service=service)

	mydriver.get(url)
	time.sleep(8)

	divs = mydriver.find_elements(By.XPATH,"//div[@id='search']//div[starts-with(@class, 'g ')]")
	for div in divs:
		h3 = div.find_element(By.XPATH, '//h3')
		h3_text = h3.text
		if 'Supply' in h3_text or 'Supplies' in h3_text:
			div_class = div.get_attribute('data-hveid')
			a_link = mydriver.find_element(By.XPATH, f"//div[@data-hveid='{div_class}']//a")
			href = a_link.get_attribute('href')
			print(href)
			list_check = 'yes'
			for domain in domains_to_avoid:
				if domain in href:
					list_check = 'no'
			if list_check == 'yes':
				links.append(h3_text)
				links.append(href)
	mydriver.close()
	return links



def cycle(file_name,output_name):
	headers = []
	schools = []
	return_array = []
	with open(file_name, 'r') as read:
		reader = csv.reader(read)
		headers = next(reader)
		for row in reader:
			schools.append(row)
	for school in schools:
		school_name = school[3]
		name = school_name.replace(' ','+').replace('-','').replace('.','').replace('/','').replace('&','')
#		link = "https://www.ask.com/web?o=0&l=dir&qo=serpSearchTopBox&q={0}+supply+list".format(name)
#		supply_urls = get_ask(name,link)
		link = "https://www.google.com/search?q={0}+supply+list".format(name)
		supply_urls = get_goog(link)
		school += supply_urls
		return_array.append(school)
	with open('{0}.csv'.format(output_name), 'w') as write:
		writer = csv.writer(write)
		writer.writerow(headers)
		for i in return_array:
			try:
				writer.writerow(i)
			except:
				writer.writerow([i])


### the following calls the function to run the scraper
### scraper is currently set up to use Google


cycle('test.csv', "output")


