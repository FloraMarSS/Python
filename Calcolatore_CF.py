lista = {}
import csv

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

def compilatore(nome):#inserire il nome della persona a cui fare CF
	
	global CF
	dati_persona = lista[nome]
	if persona == nome:
		for lettere in dati_persona[1]:#itera per lettere del cognome (la 2 stringa nella lista valori del dizionario)
			if lettere not in vocali :#esclusione vocali(case insensitive)
				CF += lettere
			if len(CF)==3:#Quando prende le prime 3 consonanti, si ferma
				break
		for lettere in dati_persona[0]:#itera per le lettere del nome (la 1 stringa nella lista valori del dizionario)
			if lettere not in vocali:#esclusione vocali(case insensitive)
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
		if dati_persona[2] == 'f': #aggiunge 40 se sesso (la 3 stringa nella lista valori del dizionario) è femminile
			giorno = int(dati_persona[3][:2])
			giorno += 40
			CF += str(giorno)
		else:
			CF += dati_persona[3][:2]
		
		with open("./comuni_m.csv",newline="") as comuni_m:
			lettore = csv.reader(comuni_m, delimiter = ";")
			codice_città = str([riga[0] for riga in lettore if riga[1] == dati_persona[4]])
			codice_città = codice_città.strip("[]'")
		CF += codice_città
		return CF
				
				
	

#compilatore('nome') # decommentare e sostituire 'nome' con nome della persona di cui si vuole il CF
#print(CF) #per stampare il CF
			

