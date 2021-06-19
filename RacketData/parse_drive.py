# Generate dictionary of websites and corresponding URLs

import requests
from urllib.parse import urlparse

URL = 	"https://www.tenniswarehouse-europe.com/catpage-WILSONRACS-EN.html"
page = requests.get(URL)


URL_parsed = urlparse(URL)
base_url = URL_parsed[0]+"://"+URL_parsed[1]

from bs4 import BeautifulSoup,Tag
soup = BeautifulSoup(page.content, 'html.parser')


list_of_urls =[]
rak = soup.find_all(class_='product_wrapper cf rac')





for t in rak:
	urlls=t.find_all('a',href=True)
	if not "Junior" in urlls[0]['href']:
		list_of_urls.append(urlls[0]['href'])
	

from parseTW import GetRacketSpecs


rak_info = {}
import pandas as pd 

for p in list_of_urls: 
	
	specs=GetRacketSpecs(p,base_url)
	# sf = pd.Series(specs)
	# print(sf)
	# input()
	if specs != None:
		rak_info[specs["Racket Name"]] = specs
	# if name is not None and specs is not None:
	# 	specs["URL"] = p
	# 	# rak_info[name] = {"url":p,"specs":sf}
	# 	rak_info[name] = specs
	# print(rak_info)
	# input()



df = pd.DataFrame.from_dict(rak_info)	
dff = df.T
dff.to_csv("./wilson_data.csv")
# print(dff.to_string())
exit()