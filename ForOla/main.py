from MainWindow import MainWindow
from SortPhotos import ImageSorter

class Controler:
	def __init__(self):
		self.main = MainWindow()
		self.main.show()
		
		self.path_to_folder=''

		# actions
		self.main.Sort.clicked.connect(self.start_sorting)
		self.main.chooseFolder.clicked.connect(self.chooseFolder)
		self.createCopy = self.main.CreateCopy
		self.Unit = str( self.main.Unit.currentText() )
		self.Interval = str( self.main.Interval.value() )

	def chooseFolder(self):
		from PyQt5.QtWidgets import QFileDialog
		self.path_to_folder = str(QFileDialog.getExistingDirectory(caption="Choose Folder"))

	def start_sorting(self):
		try:
			assert self.path_to_folder!=''
			sorter = ImageSorter(self.path_to_folder, self.createCopy.isChecked())
			sorter.sort()
		except AssertionError:
			self.show_popup('You have not any folder', 'Please select folder using dedicated button')
		except IndexError:
			self.show_popup('Have you chosen correct folder?', 'Most probably you have not chosen folder where there are Photos,'\
				'\nIf you did please contact the KW')
		# except Exception:
		# 	self.show_popup('Sth Unexpected Happened!', 'Please contact the KW and describe what u did to get this message')
		else:
			if self.createCopy.isChecked():
				self.show_popup('Sorting Ended', 'Program finished and sorted all your Photos and copied it to "Sorted" Folder in same directory')
			else:
				self.show_popup('Sorting Ended', 'Program finished and sorted all your Photos in original directory')


	def show_popup(self, title, msg):
		from PyQt5.QtWidgets import QMessageBox

		popup = QMessageBox()
		popup.setWindowTitle(title)
		popup.setText(msg)
		popup.setIcon(QMessageBox.Information)		
		x = popup.exec_()

if __name__ == '__main__':
	from PyQt5.QtWidgets import QApplication
	import sys

	app = QApplication(sys.argv)
	controller = Controler()
	sys.exit(app.exec_())
