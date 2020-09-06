import requests as rq 
from bs4 import BeautifulSoup

def urls_to_pdfs(year):
	url = f'https://arkusze.pl/matura-informatyka-{year}-maj-poziom-rozszerzony/'
	r = rq.get(url)
	soup = BeautifulSoup(r.content, 'html.parser')

	div_pdf = soup.find_all('div', class_='msgbox msgbox-arkusz')
	for i in div_pdf:
		a = i.find_next('a')
		yield a['href']

def download_pdf_using_its_url(url):
	r = rq.get(url)
	*_, name = url.split("/") 
	with open(name, 'wb') as new:
		new.write(r.content)

for year in range(2005,2019+1):
	for url in urls_to_pdfs(year):
		download_pdf_using_its_url(url)
	
