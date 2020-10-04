import requests as rq 
from bs4 import BeautifulSoup
import os


class CS_MaturaPdfsDowloader:
    def __init__(self, lvl='Rozszerzony', mth='maj'):
        self.lvl = lvl
        self.mth = mth
        self.path_to_folder_on_desktop = os.path.join(os.path.expanduser("~/Desktop"), f'Informatyka Matury Poziom {lvl}')
        os.makedirs(self.path_to_folder_on_desktop, exist_ok=True)

    def dowload_matura_files_by_year(self, year):
        os.makedirs(os.path.join(self.path_to_folder_on_desktop, str(year)), exist_ok=True)
        print('Folder created, year:', year)
        for url in self.urls_to_pdfs(year):      
            self.download_pdf_using_its_url(url, folder=os.path.join(self.path_to_folder_on_desktop,str(year)))

    def urls_to_pdfs(self, year):
        url = f'https://arkusze.pl/matura-informatyka-{year}-{self.mth}-poziom-{(self.lvl).lower()}'
        print('Folowing URL:', url)
        r = rq.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')

        div_to_file = soup.find_all('div', class_='msgbox msgbox-arkusz')
        print('Found', len(div_to_file), 'files')
        for i in div_to_file:
            a = i.find_next('a')
            yield a['href']

    def download_pdf_using_its_url(self, url, folder):
        r = rq.get(url)
        *_, name = url.split('/')
        with open(os.path.join(folder,name), 'wb') as new:
            new.write(r.content)
            print('Downolading:', name)


dowloader = CS_MaturaPdfsDowloader(lvl='Podstawowy')
for year in range(2005,2019+1):
    dowloader.dowload_matura_files_by_year(year)
