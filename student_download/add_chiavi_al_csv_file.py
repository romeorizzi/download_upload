#!/usr/bin/python3
import smtplib
from sys import argv, exit, stderr
import os
import random
import string
import re

INPUT_FILE = "lista_studenti_iscritti.csv"
OUTPUT_FILE = "lista_studenti_iscritti_con_chiavi.csv"

def usage():
    print(f"""Usage: {os.path.basename(argv[0])} [-h] [-n] [length_pwd (int, default = 6) [PWD_PREFIX (string, "") [PWD_SUFFIX (string, "") [lenght_anchor (int, -1)] ] ] ]\n\n   dove un flag che inizi per h condurrebbe a visualizzare questo aiuto ed il flag n chiede che la password generata sia un codice numerico\n\n   il primo parametro opzionale (length_pwd) è un numero intero che indica la lunghezza della sezione randomica della password di accesso (default 6, può essere 0 se non vogliamo alcuna password).\n\n   il secondo parametro opzionale (PWD_PREFIX) e' un'eventuale stringa di prefisso uguale per tutte le password (default la stringa vuota).\n     Nota: alcuni valori particolari di PWD_PREFIX vengono serviti in modo speciale, si veda il codice.\n\n   il terzo parametro opzionale (PWD_SUFFIX) e' un'eventuale stringa di suffisso uguale per tutte le password (default la stringa vuota).\n     Nota: alcuni valori particolari di PWD_SUFFIX possono essere gestiti in modo speciale.\n\n   il quarto parametro opzionale (lenght_anchor) è la lunghezza dell'ancora nell'indirizzo a cui lo studente reperisce i propri file col tema assegnato (consigliato 10, possibile 0 che implica che tutte le ancore siano la stringa vuota, ma il default è -1 nel qual caso il file .csv generato non conterrà la colonna per le ancore generate randomicamente e specifiche al singolo studente).""", file=stderr)
    exit(1)

# THE MAIN PROGRAM:    
# Usage: command_name  [-h] [-n] [length_pwd (int, default = 6) [PWD_PREFIX (string, "") [PWD_SUFFIX (string, "") [lenght_anchor (int, -1)] ] ] ]
if len(argv) > 1 and argv[1][:2] == "-h":
    print("Serviamo la tua RICHIESTA DI AIUTO:", file=stderr)
    usage()
    exit(1)

numeric_pwd = False    
if len(argv) > 1 and argv[1][:2] == "-n":
    numeric_pwd = True
    argv = argv[1:]

if len(argv) > 5:
    print("ERROR: Hai fornito troppi parametri (più di 4)!", file=stderr)
    usage()
    exit(1)

if len(argv) > 1:
  try:
    length_pwd = int(argv[1])
  except ValueError:
    print(f"ERROR: The first optional argument is present but it is not an int (ha valore {argv[1]})!", file=stderr)
    usage()
else:
    length_pwd = 6

if len(argv) > 4:
  try:
    length_anchor = int(argv[4])
  except ValueError:
    print(f"ERROR: The fourth optional argument is present but it is not an int (ha valore {argv[4]})!", file=stderr)
    usage()
else:
    length_anchor = -1

PWD_PREFIX = PWD_SUFFIX = ""
if len(argv) > 2:
    PWD_PREFIX = argv[2]
if len(argv) > 3:
    PWD_SUFFIX = argv[3]

def PWD_prefix(MATRICOLA,SURNAME,NAME,YEAR,MAILADR_ID):
    if PWD_PREFIX == "MATRICOLA":
        return MATRICOLA
    elif PWD_PREFIX == "NAME":
        return re.sub('[ ]', '', NAME)
    elif PWD_PREFIX == "SURNAME":
        return re.sub('[ ]', '', SURNAME)
    else:
        return PWD_PREFIX  

def PWD_suffix(MATRICOLA,SURNAME,NAME,YEAR,MAILADR_ID):
    if PWD_SUFFIX == "MATRICOLA":
        return MATRICOLA
    elif PWD_SUFFIX == "NAME":
        return re.sub('[ ]', '', NAME)
    elif PWD_SUFFIX == "SURNAME":
        return re.sub('[ ]', '', SURNAME)
    else:
        return PWD_SUFFIX  

        
if not os.path.exists(INPUT_FILE):
    print(f"Questo script ({argv[0]}) opera a partire dal file {INPUT_FILE} che assume esistere nella sua stessa cartella.\nESECUZIONE INTERROTTA: File non trovato.", file=stderr)
    exit(1)

if os.path.exists(OUTPUT_FILE):
    print(f"Questo script ({argv[0]}) genera un file di nome {OUTPUT_FILE} nella sua stessa cartella.\nESECUZIONE INTERROTTA: File esiste già. Cancellalo o spostalo prima di richiederne una nuova generazione.", file=stderr)
    exit(1)
    

# Esempio di utilizzo di tabella di conversione:
#intab = "$"
#outtab = " "
# Ma per ora non sono emerse situazioni dove sia stato necessario disinfettare dei caratteri e quindi, teniamo presente lo strumento (un filtro di depurazione), ma lasciamolo girare a vuoto:
intab = ""
outtab = ""
trantab = str.maketrans(intab, outtab)    

fout = open(OUTPUT_FILE,"w")
with open(INPUT_FILE,"r") as fin:
    i = 0
    for line in fin:
       i+=1 
       MATRICOLA, SURNAME, NAME, YEAR, MAILADR_ID = line.strip().split(',')
       MATRICOLA = re.sub('["]', '', MATRICOLA).translate(trantab)
       SURNAME = re.sub('["]', '', SURNAME).translate(trantab)
       NAME = re.sub('["]', '', NAME).translate(trantab)
       YEAR = re.sub('["]', '', YEAR).translate(trantab)
       MAILADR_ID = re.sub('["]', '', MAILADR_ID).translate(trantab)
       MAILADR_MAT = MATRICOLA + "@studenti.univr.it"
       #print(f"MATRICOLA={MATRICOLA}, SURNAME={SURNAME}, NAME={NAME}, YEAR={YEAR}, MAILADR_ID={MAILADR_ID}, MAILADR_MAT={MAILADR_MAT}")
       palette = string.ascii_letters + string.digits
       if numeric_pwd:
           palette = string.digits
       PASSWORD = PWD_prefix(MATRICOLA,SURNAME,NAME,YEAR,MAILADR_ID) + \
                  ''.join([random.choice(palette) for n in range(length_pwd)]) + \
                  PWD_suffix(MATRICOLA,SURNAME,NAME,YEAR,MAILADR_ID)
       # USERNAME = MATRICOLA
       if length_anchor < 0:
           fout.write(MAILADR_MAT + "," + MATRICOLA + "," + YEAR + "," + PASSWORD + "," + MAILADR_ID + "," + NAME + "," + SURNAME + "\n")
       else:
           ANCHOR = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(length_anchor)])
           fout.write(MAILADR_MAT + "," + MATRICOLA + "," + YEAR + "," + ANCHOR + "," + PASSWORD + "," + MAILADR_ID + "," + NAME + "," + SURNAME + "\n")
print(f"Fatto! Il file {OUTPUT_FILE} è stato costruito e contiene {i} records.")
