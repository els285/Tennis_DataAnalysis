import requests
from urllib.parse import urlparse

URL = 'https://www.tenniswarehouse-europe.com/Babolat_Pure_Strike_16x19_Racket/descpageRCQBA-PS1619-EN.html'

# o = urlparse(URL)
# print(o)
# exit()

from bs4 import BeautifulSoup,Tag


def SplitNConvert(txt):

	import re

	t = txt.split("/")
	t0b = t[0].replace(",",".")
	t0f = re.findall(r"[-+]?\d*\.\d+|\d+",t0b)
	t1b = t[1].replace(",",".")
	t1f = re.findall(r"[-+]?\d*\.\d+|\d+",t1b)
	return float(t0f[0]),float(t1f[0])

	# return (float(re.sub(r"^\d*[.,]*$", "",t[0]))   ,  float(re.sub(r"^\d*[.,]*$", "",t[1]))) 





def TW_Review(URL):

	page = requests.get(URL)

	soup = BeautifulSoup(page.content, 'html.parser')

	score_dict = {}

	overall_score = soup.find(class_="total_score fr")
	if overall_score:
		overall_score_value = int(overall_score.get_text()) 
		score_dict["Overall"] = overall_score_value

	score_table = soup.find(class_='scores')
	if score_table:
		table_iter=score_table.find_all("tr")

		for row in table_iter:
			param_name = row.find("th").get_text()
			score      = int(row.find("td").get_text())
			score_dict[param_name] = score

		return score_dict
	else:
		return None


# def RacketSpecs(new_specs)



def GetRacketSpecs(URL,base_url):
	page = requests.get(URL)

	soup = BeautifulSoup(page.content, 'html.parser')

	RacketName = soup.find(class_="name").get_text()
	print(RacketName)
	specs_dict = {}
	specs_dict["Racket Name"] = RacketName



	## This gets the TW Review scores

	tw_review = soup.find(class_="product_links review_links cf")
	fitz=tw_review.find_all('a',href=True)
	cust_review   = fitz[0].attrs['href']
	twr_bool = False
	if len(fitz) == 2:
		# This gives a relative path, we need to attach the base url to generate the full path
		tw_review_url = base_url+fitz[1].attrs['href']
		twR_score_dict =TW_Review(tw_review_url)
		if not twR_score_dict==None:
			twr_bool = True


	"""
	Gettign racket specifications by parsing table
	"""
	specs = soup.find(class_="rac_specs")

	new_specs = specs.find(class_="new_specs")

	if new_specs:

		specs1 = new_specs.find_all(class_="SpecsLt")
		specs2 = new_specs.find_all(class_="SpecsDk")


		for x in specs1+specs2:
			s = x.get_text()
			s2 =s.replace("\n","").split(":")
			# Data is in s2[1]
			# Generalised 
			# if any(x in s2[0] for x in ["Head Size","Strung Weight","Length","Unstrung Weight"]):
			# 	s3 = SplitNConvert(s2[1])
			# else:
			# 	s3 = s2[1]

			# Specific
			# print(s2[0])

			if "Head Size" in s2[0]:
				s3 = SplitNConvert(s2[1])
				specs_dict["Head Size (in^2)"] = s3[0]
				specs_dict["Head Size (cm^2)"] = s3[1]
			elif "Length" in s2[0]:
				s3 = SplitNConvert(s2[1])
				specs_dict["Length (in)"] = s3[0]
				specs_dict["Length (cm)"] = s3[1]
			elif "Unstrung Weight" in s2[0]:
				s3 =SplitNConvert(s2[1])
				specs_dict["Unstrung weight (g)" ] = s3[0]
				specs_dict["Unstrung weight (oz)"] = s3[1]
			elif "Strung Weight" in s2[0]:
				s3 = SplitNConvert(s2[1])
				specs_dict["Strung weight (g)" ] = s3[0]
				specs_dict["Strung weight (oz)"] = s3[1]
			else:
				specs_dict[s2[0]] = s2[1]

		specs_bool = True
		# return RacketName,specs_dict

	else:
		specs_bool = False
		# return None,None

	if specs_bool and twr_bool:
		specs_dict["TW Review"] = True
		return {**specs_dict, **twR_score_dict}
	elif specs_bool and not twr_bool:
		specs_dict["TW Review"] = False
		return specs_dict
	elif not specs_bool and twr_bool:
		specs_dict["TW Review"] = True
		return twR_score_dict
	else:
		return None



# for x in specs2:
# 	print(x.get_text())

