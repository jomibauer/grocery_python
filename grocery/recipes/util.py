import bs4
import requests
import re


def find_domain(url):
	supported_domains = ['allrecipes']
	try:
		found = re.search(r'\.(.+?)\.', url).group(1)
		if found in supported_domains:
			return found
		else:
			return "unsupported"
	except AttributeError:
		return "unsupported"


def get_from_all_recipes(url):
	res = requests.get(url)
	soup_res = bs4.BeautifulSoup(res.text, features="html.parser")
	ingredients = soup_res.select('.ingredients-item-name')
	steps = soup_res.select('.paragraph')

	ingr_list = [ingredient.getText().strip() for ingredient in ingredients]
	step_list = [str(i) + '. ' + step.getText().strip() for i, step in enumerate(steps, start=1)]

	return ingr_list, step_list