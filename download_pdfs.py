import requests as rq 
import os


class CS_MaturaPdfsDowloader:
	def __init__(self, lvl='Rozszerzony', mth='maj'):
		self.lvl = lvl
		self.mth = mth
		self.path_to_folder_on_desktop = os.path.join(os.path.expanduser("~/Desktop"), f'Informatyka Matury Poziom {lvl}', mth.title())
		os.makedirs(self.path_to_folder_on_desktop, exist_ok=True)

	def __del__(self):
		for subdir, dirs, files in os.walk(self.path_to_folder_on_desktop):
			if not files and not dirs:
				os.rmdir(subdir);print('Removed:', subdir)
			for file in files:
				if file.endswith('.zip'):
					os.remove(os.path.join(subdir, file))

	def unzip_folder(self, folder):
		from zipfile import ZipFile
		*path, folder_to =  os.path.split(folder)
		path_to_folder = os.path.join(*path)
		with ZipFile(folder, 'r') as zipObj:
			zipObj.extractall(path_to_folder);print('Unzipped', folder, 'to', path_to_folder)

	def dowload_matura_files_by_year(self, year):
		os.makedirs(os.path.join(self.path_to_folder_on_desktop, str(year)), exist_ok=True)
		print('Folder created, year:', year)
		for url in self.urls_to_pdfs(year):      
			self.download_pdf_using_its_url(url, folder=os.path.join(self.path_to_folder_on_desktop,str(year)))

	def urls_to_pdfs(self, year):
		from bs4 import BeautifulSoup
		url = f'https://arkusze.pl/matura-matematyka-{year}-{self.mth}-poziom-{(self.lvl).lower()}'
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
		file = os.path.join(folder,name)
		with open(file, 'wb') as new:
			new.write(r.content);print('Downolading:', name)
		if url.endswith('.zip'):
			self.unzip_folder(file)


if __name__ == '__main__':
	import threading
	lvls = ['Podstawowy', 'Rozszerzony'] 
	mths = ['maj','czerwiec'] 
	for lvl in lvls:
		for mth in mths:
			dowloader = CS_MaturaPdfsDowloader(lvl=lvl, mth=mth)
			threads = []
			for year in range(2002,2020+1):
				t = threading.Thread(target=dowloader.dowload_matura_files_by_year, args=[year])
				t.start()
				threads.append(t)
			for t in threads:
				t.join()
