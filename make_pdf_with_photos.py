class PDF_from_zipped_folder:
	def __init__(self, folder, new_file='Odpowiedzi.pdf'):
		self.folder = folder
		self.pdfs = []
		self.temp_file='temp_photo.png'
		self.new_file = new_file

	def __del__(self):
		# clean up
		import os
		for file in self.pdfs:
			os.remove(file)
		os.remove(self.temp_file)

		# move fie to desktop
		path_to_desktop = os.path.expanduser("~/Desktop")
		os.rename(self.new_file, os.path.join(path_to_desktop, self.new_file))

	def get_photos_from_zip(self):
		import os
		import zipfile

		with zipfile.ZipFile(self.folder) as z:
		    for filename in z.namelist():
		        if not os.path.isdir(filename):
		            # read the file
		            with z.open(filename) as f:
		                yield f

	def make_photos(self):
		from PIL import Image
		all_photos_in_bytes = self.get_photos_from_zip()
		for i, file in enumerate(all_photos_in_bytes, start=1):
			with open(self.temp_file, 'wb') as new:
				for line in file:
					new.write(line) 
			image = Image.open(self.temp_file)
			new_file = f'pdf_img{i}.pdf'
			image.save(new_file)
			self.pdfs.append( new_file )

	def merge(self):
		from PyPDF2 import PdfFileMerger

		merger = PdfFileMerger()
		for pdf in self.pdfs:
		    merger.append(pdf)

		merger.write(self.new_file)
		merger.close()

	def make_file(self):
		self.make_photos()
		self.merge()


if __name__ == '__main__':
	FOLDER = ""
	PDF_from_zipped_folder(FOLDER).make_file()
