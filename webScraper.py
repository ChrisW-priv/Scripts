import requests as rq
import csv
from bs4 import BeautifulSoup

url = 'https://www.pw.edu.pl/Rekrutacja/Studia-I-i-II-stopnia/Studia-stacjonarne-I-stopnia-i-jednolite/Progi-punktowe-z-ubieglych-lat'
r = rq.get(url)
soup = BeautifulSoup(r.content, 'html.parser')

table = soup.find('table', class_='renderedtable')

with open('kierunki.csv', 'w', encoding='utf-8') as new:
	writer = csv.writer(new, delimiter='\t')
	for tr in table.find_all_next('tr'):
		text = [str(td.get_text()).replace('\n', '') for td in tr.findChildren('td')]
		print(text)
		writer.writerow(text)
