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

found_folder_with_long_name = False
for name in lista_cartelle:
   if os.path.isdir(SHUTTLE_FOLDER+'/'+name):
      if len(name)>29:
         print(f"Considering the subdirectory {name} of the shuttle.") 
         if found_folder_with_long_name:
             if name[9:19] != DATE:
                 print(f"Errore: non tutti i floder in {SHUTTLE_FOLDER} si riferiscono alla data {DATE}. Controlla e, dopo aver ripulito, start me again.")
                 exit(1)
         else:
             found_folder_with_long_name = True
             DATE = name[9:19]
             print(f"Shuttle del {DATE} accende i motori per la partenza. Ultimi controlli in corso ...")
if not found_folder_with_long_name: 
    print(f"ERROR: the SHUTTLE_FOLDER directory {SHUTTLE_FOLDER} does not contain any folder whose name is sufficiently long (at least 30 characters) that we consider it the folder of an assignment to a student. Fill up the shuttle properly and start me again.")
    exit(1)
    
with open(f"{CSV_FILE_WITH_STUDENTS}") as input_file:
    for row in list(csv.reader(input_file)):
        DEST_STUDENT_CODE = row[0]
        DEST_MAIL_ADDRESS = row[0]+"@studenti.univr.it"
        DEST_ANCHOR = row[2]
        DEST_PWD = row[3]
        DEST_ID = row[4]
        DEST_NAME = row[5]
        DEST_SURNAME = row[6]

        # POTREBBE ESSERE OPPORTUNO PREVEDERE QUI' UN CHECK CHE LA CARTELLA CORRISPONDENTE ESISTA IN lista_cartelle  PRIMA DI PROVARE AD INVIARE LA MAIL. 

        print(f"procedo ad inviare la mail allo studente {DEST_STUDENT_CODE} {DEST_ID} {DEST_NAME} {DEST_SURNAME}:")
        risp = os.system(f"./send_one_mail.py {argv[1]} {DEST_STUDENT_CODE} {DATE}")
