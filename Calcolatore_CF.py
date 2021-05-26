lista = {}
import csv
import math
import requests

while True:
	nome = input("Inserire il nome: ").upper()
	persona = nome.lower()
	if len(nome) == 0:
	    break
	else:
	    cognome = str(input("Inserire il cognome: ")).upper()
	    sesso = str(input("Inserire il sesso biologico di appartenenza(f/ m): ")).upper()
	    data = str(input("Inserire la data di nascita(gg/mm/aaaa): ")).upper()
	    luogo = str(input("Inserire il luogo di nascita: ")).upper()
	    lista[persona]= [nome,cognome,sesso,data,luogo]
  
print(lista)

CF = "" #è la stringa che conterrà il nostro codice fiscale
vocali = 'AEIOU'
mese_lettera = {
	'01':'A','02':'B','03':'C','04':'D','05':'E',
	'06':'H','07':'L','08':'M','09':'P',
	'10':'R','11':'S','12':'T'
	}
comuni_URL = "https://raw.githubusercontent.com/FloraMarSS/Python/main/comuni_m.csv"
last_url = "https://raw.githubusercontent.com/FloraMarSS/Python/Codice_completo_NoWorking/ultima_lettera.csv"

def compilatore(nome):#inserire il nome della persona a cui fare CF
	
	global CF
	dati_persona = lista[nome]

	for lettere in dati_persona[1]:#itera per lettere del cognome (la 2 stringa nella lista valori del dizionario)
		if lettere not in vocali:#esclusione vocali
			CF += lettere
		if len(CF)==3:#Quando prende le prime 3 consonanti, si ferma
			break
		
	for lettere in dati_persona[0]:#itera per le lettere del nome (la 1 stringa nella lista valori del dizionario)
		if lettere not in vocali:#esclusione vocali
			CF += lettere
		if len(CF)==7: #dovendo prendere la prima, la terza e la 4, lo fermo a 7 consonanti
			CF = CF[:4] + CF[5:] #per eliminare la seconda consonante
			break
			return CF
	anno = dati_persona[3][-2:] #le ultime 2 cifre dell'anno di nascita (la 4 stringa nella lista valori del dizionario)
	CF += anno
	for mesi in mese_lettera.keys():#cerca nel dizionario delle corrispondenze mese_lettera, il mese di nascita indicato
		if mesi == dati_persona[3][3:5]:
			CF += mese_lettera[mesi]
	if dati_persona[2] == 'F': #aggiunge 40 se sesso (la 3 stringa nella lista valori del dizionario) è femminile
		giorno = int(dati_persona[3][:2])
		giorno += 40
		CF += str(giorno)
	else:
		CF += dati_persona[3][:2]
	with requests.Session() as s:
		download = s.get(comuni_URL)
		comuni_m = [line.decode('utf-8') for line in download.iter_lines() if line]
		lettore = csv.reader(comuni_m, delimiter = ";")
		for row in lettore:
			codice_città = str([riga[0] for riga in lettore if riga[1] == dati_persona[4]]) #cerca tra le colonne la riga corrispondente a luogo inserito
			codice_città = codice_città.strip("[]'") #toglie parentesi quadre e apici dal codice
	CF += codice_città
	with requests.Session() as t:
		 downloads = t.get(last_url)
		 last = [line.decode('utf-8') for line in downloads.iter_lines() if line]
		 lettore = csv.reader(last,delimiter =";")
		 lettore = [riga for riga in lettore]#lettore è iterativo adesso
	somma = 0
	CF_p = CF[::2]
	CF_d = CF[1::2]
	for lettere in CF_p:
		for riga in lettore:
			if riga[2] == lettere:
				valore = int(riga[3])
	somma += valore
	for lettere in CF_d:
		for riga in lettore:
			if riga[0] == lettere:
				valore = int(riga[1])
	somma += valore
	resto = int(math.remainder(somma,26))
	for riga in lettore:
		if riga[4] == str(resto):
			CIN = str(riga[5])
	CF += CIN
	return CF
#print(compilatore(nome))#NB: il nome va' inserito con tutti i caratteri minuscoli!!!!
