def WAT_PKT():
	import pandas as pd

	df = pd.read_csv('WAT.csv')
	df.set_index('Wynik', inplace=True)

	możliwości = [['MatP','InfR','AngP','PolP'],['MatR','InfR','AngP','PolP'],['MatP','InfR','AngR','PolP'],['MatR','InfR','AngR','PolP']]

	Wyniki = {
		'MatP':90,
		'MatR':50,
		'InfR':60,
		'AngP':90,
		'AngR':80,
		'PolP':30,
	}

	for przedmioty in (możliwości):
		punkty = 0
		for przedmiot in przedmioty:
			pkt = Wyniki[przedmiot]

			punkty += int(df.at[pkt,przedmiot])
		print(punkty, przedmioty)
		
