import random as rd

def clear_screan():
	import os
	try:
		os.system('cls')
	except:
		os.system('clear')


class Ask_or_Dare:
	def __init__(self):
		with open('Zadania.txt', encoding='utf-8') as file:
			zadania = file.read()
		with open('Pytania.txt', encoding='utf-8') as file:
			pytania = file.read()

		self.zadania = zadania.split('\n') 
		self.pytania = pytania.split('\n') 

	def ask_or_dare(self, user_input):
		if user_input == "w":
			choice = rd.randrange(len(self.zadania))
			print('Zadanie:', self.zadania[choice])
		elif user_input == "p":
			choice = rd.randrange(len(self.pytania))
			print('Pytanie:', self.pytania[choice])

	def play(self):
		while True:
			ask_ok = False
			while not ask_ok:
				user_input = input('Pytanie czy Wyzwanie?\n > ').lower()
				try:
					assert user_input in ['w', 'p']
					clear_screan()
					self.ask_or_dare(user_input)
					ask_ok=True
				except AssertionError:
					print('Nie równe "w" lub "p"')
				except KeyboardInterrupt:
					print('Wyszedłeś(łaś) z gry')


if __name__=="__main__":
	try:
		clear_screan()
		game = Ask_or_Dare()
		game.play()
	except KeyboardInterrupt:
		clear_screan()
		print('Wyszedłeś(łaś) z gry')
