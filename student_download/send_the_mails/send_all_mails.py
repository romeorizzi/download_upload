#!/usr/bin/python3
from sys import argv, exit, stderr
import os
from shutil import copyfile
import csv

CSV_FILE_WITH_STUDENTS = "../lista_studenti_iscritti_con_chiavi.csv"
SHUTTLE_FOLDER = "../shuttle"

# script che invia tutte le mail (prevedendo le te modalità "SUDO","ME","SAY").
# Ogni studente riceverà la mail con l'ancora e le credenziali per potersi scaricare il suo testo di esame.
# script da lanciare dalla cartella:
# ~/corsi/RO/jupyther/download_upload/student_download/send_the_mails/
# dopo che la cartella shuttle con tutti le sottocartelle, ciascuna con ancora privata per il rispettivo sudente e con dentro il file compresso per il suo tema d'esame è stata ricopiata sul Web Server.


def usage(onstream):
    print(f"\nSono lo script che invia tutte le mail agli studenti per dare avvio all'esame.\n\nUsage: os.path.basename(argv[0])  {{ SUDO | ME | SAY }}\n\n   where the three alternative options are:\n   * SUDO: really act! Send all the mails to the person.\n   * ME: send all the mails but just to myself. In this way, I can have a look at a few mails before sending a ton of them.\n   * SAY: only tell the action in the gun but do not really take it.", file=onstream)

# THE MAIN PROGRAM:
if len(argv) != 2 or argv[1] not in {"SUDO","ME","SAY"}:
    usage(stderr)
    exit(1)


if not os.path.exists(CSV_FILE_WITH_STUDENTS):
    print(f"Questo script ({argv[0]}) opera a partire dal file {CSV_FILE_WITH_STUDENTS}. Tale file contiene i dati degli studenti necessari all'invio delle mail che forniscano loro i punti di accesso e le credenziali personali. Il file .csv contiene una riga per ogni studente, suddivisa nei campi necessari affinche questo ed altri script della nostra architettura possano svolgere la loro funzione. Lo scritp si attende che tale file od un link ad esso sia presente nella cartella padre di quella dove lo script viene lanciato (che assumiamo essere .../student_download/send_the_mails/).\n\nESECUZIONE INTERROTTA: File {CSV_FILE_WITH_STUDENTS} con i dati degli studenti necessari all'invio delle mail non trovato.", file=stderr)
    exit(1)

if not os.path.exists(SHUTTLE_FOLDER):    
    print(f"ERROR: the SHUTTLE_FOLDER directory {SHUTTLE_FOLDER} does not exist. Create and fill it up properly and start me again.")
    exit(1)
lista_cartelle = os.listdir(SHUTTLE_FOLDER)
#print(f"lista_cartelle={lista_cartelle}")

list_IDs = []
found_folder_with_long_name = False
for name in lista_cartelle:
   if os.path.isdir(SHUTTLE_FOLDER+'/'+name):
      if len(name)>29:
         print(f"Considering the subdirectory {name} of the shuttle.")
         list_IDs.append(name[-8:])
         if found_folder_with_long_name:
             if name[9:19] != DATE:
                 print(f"Errore: non tutti i floder in {SHUTTLE_FOLDER} si riferiscono alla data {DATE}. Controlla e, dopo aver ripulito, start me again.")
                 exit(1)
         else:
             found_folder_with_long_name = True
             DATE = name[9:19]
             print(f"Shuttle del {DATE} accende i motori per la partenza. Ultimi controlli in corso ...")
if not found_folder_with_long_name: 
    print(f"\nERROR: the SHUTTLE_FOLDER directory {SHUTTLE_FOLDER} does not contain any folder whose name is sufficiently long (at least 30 characters) that we consider it the folder of an assignment to a student. Fill up the shuttle properly and start me again.")
    exit(1)

dict_mittenti = {}
with open(f"{CSV_FILE_WITH_STUDENTS}") as input_file:
    for row in list(csv.reader(input_file)):
        DEST_STUDENT_CODE = row[0]
        DEST_ANCHOR = row[2]
        DEST_PWD = row[3]
        DEST_ID = row[4]
        DEST_MAIL_ADDRESS = DEST_ID+"@studenti.univr.it"
        DEST_NAME = row[5]
        DEST_SURNAME = row[6]
        if DEST_ID in dict_mittenti:
            print(f"\nERROR: the ID_student {DEST_ID} occurs twice (into two different rows) of the file {CSV_FILE_WITH_STUDENTS}.\n Here is the whole data of the second occurrence:\n   matricola: {DEST_STUDENT_CODE},\n   name: {DEST_NAME},\n   name: {DEST_SURNAME},\n   ID: {DEST_ID},\n   ancora: {DEST_ANCHOR}")
            exit(1)
        if DEST_ID not in list_IDs:
            print(f"\nERROR: no folder is present in the shuttle for the ID_student {DEST_ID}\n Here is the whole data of the student:\n   matricola: {DEST_STUDENT_CODE},\n   name: {DEST_NAME},\n   name: {DEST_SURNAME},\n   ID: {DEST_ID},\n   ancora: {DEST_ANCHOR}")
            print(f"I folder presenti sono relativi agli IDs list_IDs={list_IDs}")
            exit(1)
        dict_mittenti[DEST_ID] = "with folder ready"

print("Ultimo controllo: per ogni folder in shuttle abbiamo il mittente")
assert len(dict_mittenti) <= len(list_IDs)        
if len(dict_mittenti) < len(list_IDs):
    print(f"\nWARNING: nello shuttle sono presenti delle cartelle per le quali non troviamo i dati del destinatario nel file {CSV_FILE_WITH_STUDENTS}\nGli ID-students di queste cartelle sono:")
    num_missing = 0
    for dest in list_IDs:
        if dest not in dict_mittenti:
            num_missing += 1
            print(f"   {num_missing}. {dest}")
    print("Reputi di voler comunque proseguire con l'invio di tutte le altre mail? (s/S)")
    risp = input()
    if risp not in {"s","S"}:
        exit(1)
else:
    print(f"Le cartelle in shuttle ed i destinatari nel file {CSV_FILE_WITH_STUDENTS} corrispondono.\nSiamo pronti per inviare le seguenti {len(list_IDs)} mails")
mail_inviate = 0
with open(f"{CSV_FILE_WITH_STUDENTS}") as input_file:
    for row in list(csv.reader(input_file)):
        DEST_STUDENT_CODE = row[0]
        DEST_ANCHOR = row[2]
        DEST_PWD = row[3]
        DEST_ID = row[4]
        DEST_NAME = row[5]
        DEST_SURNAME = row[6]
        DEST_MAIL_ADDRESS = row[7]
        print(f"procedo ad inviare la mail allo studente {DEST_STUDENT_CODE} {DEST_ID} {DEST_NAME} {DEST_SURNAME}:")
        risp = os.system(f"./send_one_mail.py {argv[1]} {DEST_STUDENT_CODE} {DATE}")
        mail_inviate += 1
print(f"Mail inviate: {mail_inviate}/{len(list_IDs)}.")
