import pandas as pd
import requests
import numpy as np
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import os
#TODO lav min egen urlparser
#TODO undersøg hvilke hjemmesider som reqs ikke kan fange


def scrape_url(start_url, website_depth = 2):
	# Purpose:
	# Scraper which will find the external urls on the website.
	#
	# Input:
	# Start_url, string, The url wich should be scraped
	# webstie_depth, int, the depth the scaper should
	#
	# Output:
	# external_urls, list, Contains the external urls
	# external_domain, list, Contain the domains from the external urls

	# Vi laver nogle lister, som skal bruges senere
	internal_urls = [start_url]
	external_urls = []
	external_domain = []
	internal_urls_checked = []
	session = requests.Session()
	session.max_redirects = 60
	filetype = ['.jpg',".png",".pdf"] # Vi behøver ikke scrape billeder for links
	start_url_domain = urlparse(start_url).netloc

	while len(internal_urls_checked) < len(internal_urls): # vi forsætter while, så længer der er interne urls af kigge på
		print(len(internal_urls_checked))
		for url in internal_urls:
			if (url not in internal_urls_checked) & (url.count('/') <= website_depth+2): # vi tjekker kun de urls som ikke har kigget på i nu
				print(url)
				reqs = session.get(url,allow_redirects=False) # vi scraper siden
				if reqs.status_code < 300  : # Vi vil ikke tjekkek urls der ikke fungere
					soup = BeautifulSoup(reqs.text, 'html.parser')
					urls = []
					for link in soup.find_all('a', href=True):
						urls = urls + [(link.get('href'))]
					urls = [x for x in urls if len(x)>0]
					for link in urls: # vi opdeler urls i interne og eksterne urls
						if (link[0] == '/') & ('?f' not in link):
						#if (link[0] == '/') & (not link[-1].isdigit()):  # Vi kigge ikke på urls som ender på et tal
							full_link = start_url + link
							if (full_link not in internal_urls):
								internal_urls = internal_urls + [full_link]
						elif ('https' in link) & (link not in external_urls):
							url_domain = urlparse(link).netloc
							# Hvis vi får en fuld url til dens egen hjemmeside skal vi huske af gemme dem som en intern url
							if (start_url_domain == url_domain) & (link not in internal_urls):
								internal_urls = internal_urls + [link]
							elif url_domain not in external_domain:
								external_urls = external_urls + [link]
								external_domain = external_domain + [url_domain]
			internal_urls_checked = internal_urls_checked + [url]

	return external_urls, external_domain


def scrape_multi(start_url, website_depth = 2,max_order = 2):
	# Purpose:
	# Scraper which will scrabe multiple website for their urls.
	# start_url will be the first url to be scrabe, down to the depth defined in website_depth.
	# Then the external urls are scaped like the start_url and this continues until the max_order is reached
	#
	# Input:
	# Start_url, string, The url which should be scraped first
	# website_depth, int, the depth the scraper should
	# max_order, int, den maximale order som bestemme hvor mange hjemmesider vi vil tjekke
	#
	# Output:
	# website_dataframe, pandas dataframe,
	#

	# Vi starter med af scrape den første url.
	external_urls, external_domain = scrape_url(start_url, website_depth)
	external_urls_checked = [start_url]
	start_url_domain = urlparse(start_url).netloc
	# Den gemmer vi i et dataframe med dens order og hvilke eksterne urls den indeholdte
	website_dataframe = pd.DataFrame({'Website':start_url_domain,'url': start_url, 'Order':0, 'Connected websites':[external_domain]})
	domain_checked = [start_url_domain]
	# Der er vise hjemmesider vi undgår som sociale medier
	banned_words = ['facebook','twitter','instagram','google','linkedin','politi','apple']
	external_urls = [x for x in external_urls if not len([y for y in banned_words if y in x]) > 0]

	i=0 # vi forsætter indtil vi når max orden
	while(i< max_order):
		i = i+1
		external_urls_keep = []

		for url in external_urls:
			url_domain = urlparse(url).netloc
			if (url not in external_urls_checked) & (url_domain not in domain_checked):
				external_urls_temp, external_domain_temp = scrape_url(url, website_depth)
				external_urls_keep = external_urls_keep + external_urls_temp
				dataframe_temp = pd.DataFrame({'Website': url_domain,'url': url, 'Order': i, 'Connected websites': [external_domain_temp]})
				domain_checked = domain_checked + [url_domain]
				website_dataframe = website_dataframe._append(dataframe_temp)
		external_urls_keep = np.unique(external_urls_keep)
		external_urls = external_urls_keep.tolist()
		external_urls = [x for x in external_urls if not len([y for y in banned_words if y in x]) > 0]
		if i == max_order:
			for url in external_urls:
				url_domain = urlparse(url).netloc
				if url not in external_urls_checked:
					dataframe_temp = pd.DataFrame({'Website': url_domain,'url': url, 'Order': max_order+1, 'Connected websites': []})
					website_dataframe = website_dataframe._append(dataframe_temp)
		external_urls_checked = external_urls_checked + external_urls

	# Vi laver en liste af alle de hjemmesider scraperen har besøgt
	website_series = website_dataframe['Connected websites'].explode().dropna()
	website_series = website_series.unique()
	website_list = website_series.tolist()
	website_list = [x for x in website_list if x in website_dataframe['Website'].explode().dropna().tolist()]
	website_dataframe.index = range(0,len(website_dataframe))
	# Nu bytter vi lister ud med en søjle for hver hjemmeside
	for domain in website_list:
		temp_list = []
		for i in range(0, len(website_dataframe['Connected websites'])):
			if domain in website_dataframe['Connected websites'][i]:
				temp_list = temp_list + [1]
			else:
				temp_list = temp_list + [0]
		website_dataframe[domain] = temp_list
	website_dataframe = website_dataframe.drop(columns=['Connected websites'])
	website_dataframe.to_csv(os.getcwd() + '\\website_dataframe.csv', index=False)
	#dataframe_expanded = dataframe["Connected websites"].apply(pd.Series)
	#dataframe_expanded.to_csv(index=False)

	return website_dataframe

# Da vi vil undersøge sik.dk , er det også vores star_url
test_url = 'https://www.sik.dk'

test_data = scrape_multi(test_url, website_depth = 3,max_order = 3)
print(test_data)