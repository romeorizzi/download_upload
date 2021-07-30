#!/usr/bin/python3
from sys import argv, exit, stderr
import os
from shutil import copyfile
import csv
import time
import argparse

import send_one_mail

CSV_FILE_WITH_STUDENTS = "../lista_studenti_iscritti_con_chiavi.csv"
SHUTTLE_FOLDER = "../shuttle"

usage=f"""\nSono lo script che invia tutte le mail agli studenti coi link e le credenziali per dare avvio all\'esame.

Usage: {os.path.basename(argv[0])}  {{ SUDO | ME | SAY }}

   where the three alternative options for the 'mode' compulsory parameter are:
   * SUDO: really act! Send all the mails to the person.
   * ME: send all the mails but just to myself. In this way, I can have a look at a few mails before sending a ton of them.
   * SAY: only tell the action in the gun but do not really take it.

Devo essere lanciato dalla cartella dove mi trovo:
   ~/corsi/RO/jupyther/download_upload/student_download/send_the_mails/
dopo che la cartella shuttle con tutte le sue sottocartelle con ancora privata (ciascuna sottocartella rivolta al rispettivo studente, con dentro il file compresso con il suo tema d'esame) è stata ricopiata sul Web Server. Invece in locale, se non specificato altrimenti, si assume che:
   + lo shuttle sia collocato in {SHUTTLE_FOLDER}
   + il .csv file coi dati degli studenti in {CSV_FILE_WITH_STUDENTS}"""


def press_RETURN_to_continue():
    answ = input(f"\n{CBOLD}{CYELLOW}Continuare?{CEND} (Premi {CBOLD}{CBEIGE}<RETURN/Enter>{CEND} per proseguire. Se vuoi abortire immetti '{CBOLD}{CBEIGE}stop{CEND}' o premi {CBOLD}{CBEIGE}Ctrl-C{CEND})\n >>> ")
    if answ.upper() != "STOP":
        print("Ok. Proseguiamo ...")
    else:
        print("Ok. Script abortito")
        exit(1)

CEND      = '\33[0m'
CBOLD     = '\33[1m'
CITALIC   = '\33[3m'
CURL      = '\33[4m'
CBLINK    = '\33[5m'
CRED    = '\33[31m'
CGREEN  = '\33[32m'
CYELLOW = '\33[33m'
CBLUE   = '\33[34m'
CVIOLET = '\33[35m'
CBEIGE  = '\33[36m'
CWHITE  = '\33[37m'


def main():
    global CSV_FILE_WITH_STUDENTS, SHUTTLE_FOLDER

    parser=argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=usage,
    epilog="""-------------------""")
    parser.add_argument('mode', type=str, choices=['SUDO', 'ME', 'SAY'], help='choose one option in the set { SUDO | ME | SAY }', default='SAY')
    parser.add_argument('--shuttle', type=str, help=f'use this optional argument to specify a different name/location for the shuttle folder (the default is SHUTTLE_FOLDER={SHUTTLE_FOLDER}, that is, "shuttle" in the parent directory)', default=SHUTTLE_FOLDER)
    parser.add_argument('--csv_file', type=str, help=f'use this optional argument to specify a different name for the csv_file offering the list of the subscribed students with their keys (the default is CSV_FILE_WITH_STUDENTS={CSV_FILE_WITH_STUDENTS}, that is, "lista_studenti_iscritti_con_chiavi.csv" in the parent directory)', default=CSV_FILE_WITH_STUDENTS)
    parser.add_argument('--filtered_csv_file', help=f'you can use this optional argument when the .csv file has an extra last column where you specify with an "X" those students to which you want to send the mail', action="store_true")
    parser.add_argument("--with_tgz", help="please, give ALSO the link to the .tgz archive (the one that ends up in the anchored folder)",
                    action="store_true")
    parser.add_argument("--without_zip", help="please, do NOT give the link to the unencrypted zip archive (the one without password protection that ends up in the anchored folder)",
                    action="store_true")
    parser.add_argument("--with_encrypted_tgz", help="please, mention ALSO and place on Telegram the encrypted tgz archive (the one with password protection contained in the unanchored folder with no anchor in the folder name)",
                    action="store_true")
    parser.add_argument("--without_encrypted_zip", help="please, do NOT  mention NOR place on Telegram the encrypted zip archive (the one with password protection contained in the unanchored folder with no anchor in the folder name)",
                    action="store_true")
    parser.add_argument("--with_tgz_attached", help="please, put in attachment of the mail the .tgz archive (the one that ends up in the anchored folder)",
                    action="store_true")
    parser.add_argument("--with_zip_attached", help="please, put in attachment of the mail the unencrypted zip archive (the one without password protection that ends up in the anchored folder)",
                    action="store_true")
    args = parser.parse_args()

    with_web_server_download = args.with_tgz or not args.without_zip
    with_encrypted_download = args.with_encrypted_tgz or not args.without_encrypted_zip
    with_attachment_download = args.with_tgz_attached or args.with_zip_attached
    
    if args.shuttle:
        SHUTTLE_FOLDER=args.shuttle
    if args.csv_file:
        CSV_FILE_WITH_STUDENTS=args.csv_file

    if not os.path.exists(CSV_FILE_WITH_STUDENTS):
        print(f"Questo script ({argv[0]}) opera a partire dal file {CSV_FILE_WITH_STUDENTS}. Tale file contiene i dati degli studenti necessari all'invio delle mail che forniscano loro i punti di accesso e le credenziali personali. Il file .csv contiene una riga per ogni studente, suddivisa nei campi necessari affinche questo ed altri script della nostra architettura possano svolgere la loro funzione. Lo scritp si attende che tale file od un link ad esso sia presente nella cartella padre di quella dove lo script viene lanciato (che assumiamo essere .../student_download/send_the_mails/).\n\nESECUZIONE INTERROTTA: File {CSV_FILE_WITH_STUDENTS} con i dati degli studenti necessari all'invio delle mail non trovato.", file=stderr)
        exit(1)

    if not os.path.exists(SHUTTLE_FOLDER):    
        print(f"ERROR: the SHUTTLE_FOLDER directory {SHUTTLE_FOLDER} does not exist. Create it and fill it up properly, then you can start me again.")
        exit(1)
        
        
    print(f"\n{CBOLD}QUADRO DI COSA ANDIAMO A INVIARE:{CEND}\n")
    if args.filtered_csv_file:
        print(f" For each X-filtered-out student, the message will contain:")
    else:
        print(" For each student the sent message will contain:")
    if with_web_server_download:
        print(f"\n  + {CBOLD}URLs (with access credentials){CEND} where to get the NOT encrypted materials:")
        print(f'    namely, the anchored URL (plus access credentials) where to get the NOT encrypted archives ({CGREEN}{CBOLD}{".tgz " if args.with_tgz else ""}{".zip" if not args.without_zip else ""}{CEND}) contained within the ANCHORED folder in the shuttle.')
    if with_encrypted_download:
        print(f"\n  + {CBOLD}Passwords to open the encrypted materials{CEND} made available on a pulic channel (Telegram)):")
        print(f'    namely, the password for the encrypted archives ({CGREEN}{CBOLD}{".tgz " if args.with_encrypted_tgz else ""}{".zip" if not args.without_encrypted_zip else ""}{CEND}) made available on Telegram.')
    if with_attachment_download:
        print(f"\n  + {CBOLD}Materials in attachment{CEND} to the mail itself:")
        print(f'     namely, the NOT encrypted archives ({CGREEN}{CBOLD}{".tgz " if args.with_tgz_attached else ""}{".zip" if args.with_zip_attached else ""}{CEND}).')
            
    press_RETURN_to_continue()
    start_time = time.time()

    lista_cartelle = os.listdir(SHUTTLE_FOLDER)
    #print(f"lista_cartelle={lista_cartelle}")
    
    IDs_in_shuttle = {} 
    found_folder_with_proper_name_structure = False
    for name in lista_cartelle:
       if os.path.isdir(SHUTTLE_FOLDER+'/'+name):
          if len(name)>20 and name[8]=='_' and name[13]=='-' and name[16]=='-' and name[19]=='_':
             if name[-8:] not in IDs_in_shuttle.keys():
                 IDs_in_shuttle[name[-8:]] = {'anchored': False, 'unanchored': False }
             if name[20]=='_':
                 IDs_in_shuttle[name[-8:]]['unanchored'] = True
             else:
                 IDs_in_shuttle[name[-8:]]['anchored'] = True
             if found_folder_with_proper_name_structure:
                 if name[9:19] != DATE:
                     print(f"Errore: non tutti i folder in {SHUTTLE_FOLDER} si riferiscono alla data {DATE}. Controlla e, dopo aver ripulito, start me again.")
                     exit(1)
             else:
                 print(f"Pick up of the exam's date info: Considering the subdirectory {name} of the shuttle.")
                 found_folder_with_proper_name_structure = True
                 DATE = name[9:19]
                 print(f"Shuttle del {CBOLD}{CYELLOW}{DATE}{CEND} accende i motori per la partenza. Primi controlli in corso ...")
    if not found_folder_with_proper_name_structure: 
        print(f"\nERROR: the SHUTTLE_FOLDER directory {SHUTTLE_FOLDER} does not contain any folder whose name has the proper format for an exam folder of some student. Fill up the shuttle properly and start me again.")
        exit(1)

    dict_mittenti = {}
    with open(f"{CSV_FILE_WITH_STUDENTS}") as input_file:
        for row in list(csv.reader(input_file)):
            DEST_STUDENT_CODE = row[0]
            DEST_ANCHOR = row[2]
            DEST_PWD = row[3]
            ID_STUDENT = row[4]
            DEST_NAME = row[5]
            DEST_SURNAME = row[6]
            DEST_MAIL_ADDRESS = row[7]
            if (not args.filtered_csv_file) or row[8].upper()=='X':
                if ID_STUDENT in dict_mittenti.keys():
                    print(f"\nERROR: the ID_student {ID_STUDENT} occurs twice (into two different rows) of the file {CSV_FILE_WITH_STUDENTS}.\n Here is the whole data of the second occurrence:\n   matricola: {DEST_STUDENT_CODE},\n   name: {DEST_NAME},\n   name: {DEST_SURNAME},\n   ID: {ID_STUDENT},\n   ancora: {DEST_ANCHOR}")
                    exit(1)
                if (ID_STUDENT not in IDs_in_shuttle.keys() or IDs_in_shuttle[ID_STUDENT]['anchored'] == False) and with_web_server_download:
                    print(f"\nERROR: no folder with anchor is present in the shuttle for the ID_student {ID_STUDENT}\n Here is the whole data of the student:\n   matricola: {DEST_STUDENT_CODE},\n   name: {DEST_NAME},\n   name: {DEST_SURNAME},\n   ID: {ID_STUDENT},\n   ancora: {DEST_ANCHOR}")
                    print(f"I folder CON ancora rilevati sono i seguenti:")
                    for idS in IDs_in_shuttle.keys():
                        if IDs_in_shuttle[idS]['anchored']:
                            print(f"   {idS}")
                    exit(1)
                if (ID_STUDENT not in IDs_in_shuttle.keys() or IDs_in_shuttle[ID_STUDENT]['unanchored'] == False) and with_encrypted_download:
                    print(f"\nERROR: no folder without anchor is present in the shuttle for the ID_student {ID_STUDENT}\n Here is the whole data of the student:\n   matricola: {DEST_STUDENT_CODE},\n   name: {DEST_NAME},\n   name: {DEST_SURNAME},\n   ID: {ID_STUDENT},\n   ancora: {DEST_ANCHOR}")
                    print(f"I folder SENZA ancora rilevati sono i seguenti:")
                    for idS in IDs_in_shuttle.keys():
                        if IDs_in_shuttle[idS]['unanchored']:
                            print(f"   {idS}")
                    exit(1)
                dict_mittenti[ID_STUDENT] = { 'matricola': DEST_STUDENT_CODE, 'mail': DEST_MAIL_ADDRESS, 'name': DEST_NAME, 'surname': DEST_SURNAME, 'anchor': DEST_ANCHOR, 'pwd': DEST_PWD }

    print("Ultimo controllo: per ogni folder in shuttle abbiamo il mittente")
    if (with_encrypted_download and len(dict_mittenti) < len([idS for idS in IDs_in_shuttle.keys() if IDs_in_shuttle[idS]['unanchored']])) or (with_web_server_download and len(dict_mittenti) < len([idS for idS in IDs_in_shuttle.keys() if IDs_in_shuttle[idS]['anchored']])):
        print(f"\n{CRED}{CBOLD}WARNING:{CEND} nello shuttle sono presenti delle cartelle pasibili di utilizzo per le quali non troviamo i dati del destinatario nel file {CSV_FILE_WITH_STUDENTS}\nGli ID-students di queste cartelle sono:")
        num_missing = 0
        for idS in IDs_in_shuttle.keys():
            if idS not in dict_mittenti and (((not IDs_in_shuttle[idS]['unanchored']) and with_encrypted_download) or ((not IDs_in_shuttle[idS]['anchored']) and with_web_server_download)):
                num_missing += 1
                print(f"   {num_missing}. {idS}")
        print("Reputi di voler comunque proseguire con l'invio di tutte le altre mail?")
        press_RETURN_to_continue()
    else:
        print(f"{CGREEN}{CBOLD}Ok:{CEND} {CGREEN}Le cartelle in shuttle ed i destinatari nel file {CSV_FILE_WITH_STUDENTS} corrispondono.{CEND}\n\nSiamo pronti per inviare le seguenti {CBOLD}{len(dict_mittenti)}{CEND} mails:")
    print("{CBOLD}LISTA STUDENTI CHE VERRANNO GESTITI:{CEND}")
    for idS, i in zip(dict_mittenti.keys(),range(len(dict_mittenti))):
        print(f"{i+1}. {CBOLD}{idS}{CEND}: {dict_mittenti[idS]}")
    print(f"Vuoi procedere con la gestione dei {CBOLD}{len(dict_mittenti)}{CEND} studenti elencati quì sopra?")
    press_RETURN_to_continue()
    mail_inviate = 0
    for idS in dict_mittenti.keys():
        print(f"procedo ad inviare la mail per lo studente {CYELLOW}{CBOLD}{idS}{CEND}:  {dict_mittenti[idS]['matricola']} {dict_mittenti[idS]['name']} {dict_mittenti[idS]['surname']} all'indirizzo {CYELLOW}{dict_mittenti[idS]['mail']}{CEND}")
        risp = send_one_mail.send_one_mail(args.mode, DATE, idS, dict_mittenti[idS]['mail'], dict_mittenti[idS]['anchor'], dict_mittenti[idS]['pwd'], dict_mittenti[idS]['surname'], dict_mittenti[idS]['name'], SHUTTLE_FOLDER, args.with_tgz, args.without_zip, args.with_encrypted_tgz, args.without_encrypted_zip, args.with_tgz_attached, args.with_zip_attached)
        if risp=="skip":
            print(f"\n{CRED}{CBOLD}Student {idS} has been skipped!{CEND}\n")
        elif risp=="stop":
            break
        else:
            mail_inviate += 1
    print(f"{CGREEN}{CBOLD}Mail {'pseudo-' if args.mode=='SAY' else ''}inviate: {mail_inviate}/{len(dict_mittenti)}{CEND}. Tempo totale impiegato: {CBOLD}{time.time() - start_time}{CEND} secondi")

    
if __name__ == "__main__":
    main()

