#!/usr/bin/python3
from sys import argv, exit, stderr
import os
from shutil import copyfile
import csv
import re

CSV_FILE_WITH_STUDENTS_GROUP = "../lista_studenti_iscritti_con_chiavi.csv"
SHUTTLE_FOLDER = "."
GEN_EXAM_VERSION = "template_testo_esame_dummy"


# script che, per ogni studente che appaia nel file CSV_FILE_WITH_STUDENTS_GROUP genera un testo di tema dummy dal template e lo pone in shuttle.

def usage(onstream):
    print("\nSono lo script che genera tanti temi nominativi quanti sono gli studenti ma per semplice copia da un'unico template di tema.\n\nUsage: os.path.basename(argv[0])  yyyy-mm-dd  [ GEN_EXAM_VERSION [ SHUTTLE_FOLDER [ CSV_FILE_WITH_STUDENTS_GROUP ] ] ]\n\n   The first parameter is the date of the exam.\n   I tre parametri opzionali che vanno semmai precisati nell'ordine sono:\n   GEN_EXAM_VERSION (default {GEN_EXAM_VERSION}\n   SHUTTLE_FOLDER (default {SHUTTLE_FOLDER}\n   CSV_FILE_WITH_STUDENTS_GROUP (default {CSV_FILE_WITH_STUDENTS_GROUP})", file=onstream)

# THE MAIN PROGRAM:
if len(argv) > 5:
    print("ERROR: Hai fornito troppi parametri (più di 4)!", file=stderr)
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
    GEN_EXAM_VERSION = argv[2]
if len(argv) > 3:
    SHUTTLE_FOLDER = argv[3]
if len(argv) > 4:
    CSV_FILE_WITH_STUDENTS_GROUP = argv[4]

if not os.path.exists(GEN_EXAM_VERSION):
    print(f"Questo script ({argv[0]}) opera a partire dalla cartella GEN_EXAM_VERSION che contiene il testo del tema unico da distribuire a tutto il gruppo di studenti listati nel file CSV_FILE_WITH_STUDENTS_GROUP={CSV_FILE_WITH_STUDENTS_GROUP}.\n\nESECUZIONE INTERROTTA: File GEN_EXAM_VERSION={GEN_EXAM_VERSION} non trovato.", file=stderr)
    exit(1)
    
if not os.path.exists(SHUTTLE_FOLDER):
    print(f"Questo script ({argv[0]}) ripone nel folder SHUTTLE_FOLDER il testo del tema di esame che si trova nella cartella GEN_EXAM_VERSION.\n\nESECUZIONE INTERROTTA: File SHUTTLE_FOLDER={SHUTTLE_FOLDER} non trovato.", file=stderr)
    exit(1)
    
if not os.path.exists(CSV_FILE_WITH_STUDENTS_GROUP):
    print(f"Questo script ({argv[0]}) opera a partire dal file CSV_FILE_WITH_STUDENTS_GROUP che contiene i dati degli studenti necessari all'invio delle mail che forniscano loro i punti di accesso e le credenziali personali.\n\nESECUZIONE INTERROTTA: File CSV_FILE_WITH_STUDENTS_GROUP={CSV_FILE_WITH_STUDENTS_GROUP} non trovato.", file=stderr)
    exit(1)
    
    
with open(f"{CSV_FILE_WITH_STUDENTS_GROUP}") as input_file:
    for row in list(csv.reader(input_file)):
        DEST_STUDENT_CODE = row[1]
        DEST_ANCHOR = row[3]
        DEST_PWD = row[4]
        DEST_MAIL_ADDRESS = row[5]
        DEST_ID = DEST_MAIL_ADDRESS.split("@")[0]
        DEST_NAME = row[6]
        DEST_SURNAME = row[7]

        print(f"genero la cartella del testo d'esame per lo studente {DEST_STUDENT_CODE} {DEST_ID} {DEST_NAME} {DEST_SURNAME}:")
        risp = os.system(f"cp -r {GEN_EXAM_VERSION} esame_RO-{DATE}_{DEST_ID}")
        risp = os.system(f"tar -cvzf esame_RO-{DATE}_{DEST_ID}.tgz esame_RO-{DATE}_{DEST_ID}")
        risp = os.system(f"zip -r esame_RO-{DATE}_{DEST_ID} esame_RO-{DATE}_{DEST_ID}")
        risp = os.system(f"mkdir {SHUTTLE_FOLDER}/esame_RO-{DATE}_{DEST_ANCHOR}_{DEST_ID}")
        risp = os.system(f"mv esame_RO-{DATE}_{DEST_ID}.tgz {SHUTTLE_FOLDER}/esame_RO-{DATE}_{DEST_ANCHOR}_{DEST_ID}")
        risp = os.system(f"mv esame_RO-{DATE}_{DEST_ID}.zip {SHUTTLE_FOLDER}/esame_RO-{DATE}_{DEST_ANCHOR}_{DEST_ID}")
        risp = os.system(f"rm -rf esame_RO-{DATE}_{DEST_ID}")
