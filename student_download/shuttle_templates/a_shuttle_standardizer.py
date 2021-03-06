#!/usr/bin/python3
from sys import argv, exit, stderr
import os
from shutil import copyfile
import csv
import re

CSV_FILE_WITH_STUDENTS = "/home/romeo/corsi/RO/download_upload/student_download/lista_studenti_iscritti_con_chiavi.csv"
SHUTTLE_FOLDER = "/home/romeo/corsi/RO/download_upload/student_download/shuttle"
SHUTTLE_TEMPLATES_FOLDER = "/home/romeo/corsi/RO/download_upload/student_download/shuttle_templates"


# script che ricostruisce correttamente i file compressi da un formato sballato. Conviene tenerlo perchè potrebbe venire comodo anche in futuro nello ristandardizzare i subfolders nello shuttle.

def usage(onstream):
    print("\nSono uno script che ristandardizza i nomi e la strutturazione dei file presenti nei subfolders dello shuttle.\n\nUsage: os.path.basename(argv[0])  yyyy-mm-dd  [ SHUTTLE_FOLDER [ CSV_FILE_WITH_STUDENTS ] ]\n\n   The first parameter is the date of the exam.\n   I due parametri opzionali che vanno semmai precisati nell'ordine sono:\n   SHUTTLE_FOLDER (default {SHUTTLE_FOLDER}\n   CSV_FILE_WITH_STUDENTS (default {CSV_FILE_WITH_STUDENTS})", file=onstream)

# THE MAIN PROGRAM:
if len(argv) > 4:
    print("ERROR: Hai fornito troppi parametri (più di 3)!", file=stderr)
    usage()
    exit(1)
    
if len(argv) == 1:
    print(f"You gave this script no parameter but at least the date of the exam is mandatory.")
    usage(stderr)
    exit(1)

DATE=argv[1]
pattern = re.compile("^[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]$")
if not pattern.match(DATE):
    print(f"Your third parameter (namely, {DATE}) should rather be a date of the form yyyy-mm-dd (like e.g. 2020-06-30).")
    usage(stderr)
    exit(1)    
if len(argv) > 2:
    SHUTTLE_FOLDER = argv[2]
if len(argv) > 3:
    CSV_FILE_WITH_STUDENTS = argv[3]

if not os.path.exists(SHUTTLE_FOLDER):
    print(f"Questo script ({argv[0]}) ristruttura i subfolder presenti nel folder SHUTTLE_FOLDER.\n\nESECUZIONE INTERROTTA: File SHUTTLE_FOLDER={SHUTTLE_FOLDER} non trovato.", file=stderr)
    exit(1)
    
if not os.path.exists(CSV_FILE_WITH_STUDENTS):
    print(f"Questo script ({argv[0]}) fà riferimento al file CSV_FILE_WITH_STUDENTS che contiene i dati degli studenti necessari all'invio delle mail che forniscano loro i punti di accesso e le credenziali personali.\n\nESECUZIONE INTERROTTA: File CSV_FILE_WITH_STUDENTS={CSV_FILE_WITH_STUDENTS} non trovato.", file=stderr)
    exit(1)

def clean_name(first_name_of_a_person):
    only_alphanum_part = re.sub(r'[^A-Za-z0-9 ]+', '', first_name_of_a_person)
    return only_alphanum_part[0].upper()+only_alphanum_part[1:].lower()


current = os.getcwd()
risp = os.chdir({SHUTTLE_FOLDER}) # per prima cosa ci portiamo dentro lo shuttle in allestimento (e poi ci torneremo sistematicamente ad ogni subfolder)
#risp = os.system(f"cd {SHUTTLE_FOLDER}") # per prima cosa ci portiamo dentro lo shuttle in allestimento (e poi ci torneremo sistematicamente ad ogni subfolder)
risp = os.system(f"cp {SHUTTLE_TEMPLATES_FOLDER}/.htaccess {SHUTTLE_FOLDER}/") # quindi si oscura il listing della cartelle per il dopo atterraggio dello shuttle
risp = os.system(f"cp {SHUTTLE_TEMPLATES_FOLDER}/README.txt {SHUTTLE_FOLDER}/")
with open(f"{CSV_FILE_WITH_STUDENTS}") as input_file:
    for row in list(csv.reader(input_file)):
        DEST_STUDENT_CODE = row[0]
        DEST_ANCHOR = row[2]
        DEST_PWD = row[3]
        DEST_ID = row[4]
        DEST_MAIL_ADDRESS = DEST_ID+"@studenti.univr.it"
        DEST_NAME = row[5]
        DEST_SURNAME = row[6]

        print(f"rigenero la cartella del testo d'esame per lo studente {DEST_STUDENT_CODE} {DEST_ID} {DEST_NAME} {DEST_SURNAME}:")
        risp = os.system(f"mkdir {SHUTTLE_FOLDER}/esame_RO-{DATE}_{DEST_ID}")
#        risp = os.system(f"mv {SHUTTLE_FOLDER}/esameRO_{DATE}_{DEST_ANCHOR}_{DEST_ID}/esameRO_{DATE}_{DEST_ANCHOR}_{DEST_ID}.zip {SHUTTLE_FOLDER}/esame_RO-{DATE}_{DEST_ID}/")
#        risp = os.system(f"cp {SHUTTLE_FOLDER}/esameRO_{DATE}_{DEST_ANCHOR}_{DEST_ID}/esameRO_{DATE}_{DEST_ANCHOR}_{DEST_ID}.zip {SHUTTLE_FOLDER}/esame_RO-{DATE}_{DEST_ID}/")
        risp = os.system(f"cp {SHUTTLE_FOLDER}/esameRO_{DATE}_{DEST_ANCHOR}_{DEST_ID}/esameRO_{DATE}_{DEST_ANCHOR}_{DEST_ID}.tar.gz {SHUTTLE_FOLDER}/esame_RO-{DATE}_{DEST_ID}/")
        risp = os.chdir({SHUTTLE_FOLDER} + "/esame_RO-{DATE}_{DEST_ID}")
#        risp = os.system(f"unzip {SHUTTLE_FOLDER}/esame_RO-{DATE}_{DEST_ID}/esameRO_{DATE}_{DEST_ANCHOR}_{DEST_ID}.zip")
        risp = os.system(f"tar -xvzf esame_RO-{DATE}_{DEST_ID}/esameRO_{DATE}_{DEST_ANCHOR}_{DEST_ID}.tar.gz")
        risp = os.system(f"mkdir {SHUTTLE_FOLDER}/esame_RO-{DATE}_{DEST_ID}/istruzioni")
        risp = os.system(f"mv {SHUTTLE_FOLDER}/esame_RO-{DATE}_{DEST_ID}/*.pdf {SHUTTLE_FOLDER}/esame_RO-{DATE}_{DEST_ID}/istruzioni/")
        risp = os.system(f"rm -f {SHUTTLE_FOLDER}/esame_RO-{DATE}_{DEST_ID}/esameRO_{DATE}_{DEST_ANCHOR}_{DEST_ID}.tar.gz")
        risp = os.system(f"echo Benvenuto {clean_name(DEST_NAME)} nel folder dove elaborerai il tuo esame e che infine, dopo aver trasformato in un file compresso, ci consegnerai alla fine. Trovi istruzioni su come gestire la consegna nella cartella istruzioni. Nella stessa cartella trovi anche indicazioni su come partire ora e un terzo file .pdf di risoluzione di difficoltà tipicamente riscontrate. In bocca al lupo per il tuo esame! > {SHUTTLE_FOLDER}/esame_RO-{DATE}_{DEST_ID}/BENVENUTO.md")
        risp = os.chdir({SHUTTLE_FOLDER})
        risp = os.system(f"tar -cvzf esame_RO-{DATE}_{DEST_ID}.tgz {SHUTTLE_FOLDER}/esame_RO-{DATE}_{DEST_ID}")
        risp = os.system(f"zip -r {SHUTTLE_FOLDER}/esame_RO-{DATE}_{DEST_ID} esame_RO-{DATE}_{DEST_ID}")
        risp = os.system(f"mkdir {SHUTTLE_FOLDER}/esame_RO-{DATE}_{DEST_ANCHOR}_{DEST_ID}")
        risp = os.system(f"mv {SHUTTLE_FOLDER}/esame_RO-{DATE}_{DEST_ID}.tgz {SHUTTLE_FOLDER}/esame_RO-{DATE}_{DEST_ANCHOR}_{DEST_ID}")
        risp = os.system(f"mv {SHUTTLE_FOLDER}/esame_RO-{DATE}_{DEST_ID}.zip {SHUTTLE_FOLDER}/esame_RO-{DATE}_{DEST_ANCHOR}_{DEST_ID}")
        risp = os.system(f"rm -rf esame_RO-{DATE}_{DEST_ID}")
#        risp = os.system(f"rm -rf esameRO_{DATE}_{DEST_ANCHOR}_{DEST_ID}")
os.chdir(current)
