import requests
from bs4 import BeautifulSoup


url = 'https://www.sik.dk'
reqs = requests.get(url)
soup = BeautifulSoup(reqs.text, 'html.parser')

urls = []
for link in soup.find_all('a'):
	print(link.get('href'))

#
# from urllib.parse import urlparse
#
#
# urls = []
# internal_urls = []
# external_urls = []
# external_domain = []
# internal_urls_checked = []
#
# url = 'https://www.sik.dk'
# #url = 'https://www.google.dk/search?q=%22sik.dk%22&sxsrf=APwXEdfE4F2pxv52AlAIIKAnaLR-IVdYtQ%3A1681841054164&ei=nts-ZNLLCZeHxc8Pyv6l6AE&ved=0ahUKEwjSkuiUgrT-AhWXQ_EDHUp_CR0Q4dUDCA8&uact=5&oq=%22sik.dk%22&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIFCAAQgAQyCAgAEAcQHhAPMggIABAHEB4QDzIFCAAQgAQyBAgAEB4yBAgAEB4yBggAEB4QDzIICAAQCBAeEA8yAggmOggIABCABBCwAzoLCAAQBxAeEA8QsAM6BwgAEB4QsAM6CQgAEB4QDxCwAzoICAAQBRAeEA9KBAhBGAFQ0wlY2BFg9xZoAHAAeACAAaECiAH6BJIBBTAuMi4xmAEAoAEByAEKwAEB&sclient=gws-wiz-serp#ip=1'
# reqs = requests.get(url)
# soup = BeautifulSoup(reqs.text, 'html.parser')
#
# for link in soup.find_all('a',href=True):
# 	urls = urls +[(link.get('href'))]
#
# for link in urls:
# 	if (link[0] == '/') & (link not in internal_urls) :
# 		internal_urls = internal_urls + [url + link]
# 	elif ('https' in link) & (link not in external_urls):
# 		url_domain = urlparse(link).netloc
# 		if url_domain not in external_domain:
# 			external_urls = external_urls + [link]
# 			external_domain = external_domain + [url_domain]