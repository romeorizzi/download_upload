#!/usr/bin/python3
from sys import argv, exit, stderr
import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import yaml
import csv
import re
import argparse

import mail_templates

CONFIG_FOLDER_WITH_SECRET_CREDENTIALS = "../../../../credenziali_per_scripts_in_repo_pubblici/"
CONFIG_MAIL_SERVER_FILE = CONFIG_FOLDER_WITH_SECRET_CREDENTIALS + "send_mail_config.yaml"
CONFIG_TELEGRAM_SEND_RO_GROUP_FILE = CONFIG_FOLDER_WITH_SECRET_CREDENTIALS + "ro.conf"
CSV_FILE_WITH_STUDENTS = "../lista_studenti_iscritti_con_chiavi.csv"
SHUTTLE_FOLDER = "../shuttle"
SHUTTLE_FOLDER_ON_WEB_SERVER = "http://profs.sci.univr.it/~rrizzi/classes/RO/shuttle"

STANZA_ZOOM="https://univr.zoom.us/j/3518684000"
GRUPPO_TELEGRAM="https://t.me/RicercaOperativa2021"
CONFIG_TELEGRAM="ro.conf"

MYADDRESS = "romeo.rizzi@univr.it"
CCLIST = ["romeo.rizzi@univr.it","aurora.rossi@studenti.univr.it"]
#CCLIST = ["romeo.rizzi@univr.it"]
#CCLIST = ["romeo.rizzi@univr.it","alice.raffaele@univr.it"]
CCLIST_FOR_ME_EXPERIMENTS = ["romeo.rizzi@univr.it", "romeorizzi05@gmail.com"]
BCCLIST = []


usage=f"""\nUsage: This script can be used both stand-alone and as a library.
Stand-alone Usage: ./{os.path.basename(argv[0])}  {{ SUDO | ME | SAY }} ID-code of the recipient student (id??????)\n\n    where the three alternative options are:
   * SUDO: really act! Send the mail to the person.
   * ME: send the mail but to myself. In this way I can have a look at a few mails before sending a ton of them.
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


# GETTING THE MAIL SERVER DATA:
    
if not os.path.exists(CONFIG_MAIL_SERVER_FILE):
    print(f"Questo script ({argv[0]}) opera a partire dal file {CONFIG_MAIL_SERVER_FILE}. Tale file contiene le credenziali di accesso al server mail ed è pertanto stato disposto esternamente alla repo git pubblica.\nTrovi un file d'esempio entro il quale puoi riporre le tue credenziali per il tuo mail server nella cartella del presente script. Dopo averne riempito i campi richiesti collocalo dove credi opportuno ed aggiusta di conseguenza la variabile CONFIG_MAIL_SERVER_FILE che compare all'inizio del presente script.\n\nESECUZIONE INTERROTTA: File {CONFIG_MAIL_SERVER_FILE} con le credenziali di accesso al server di posta non trovato.", file=stderr)
    exit(1)

with open(CONFIG_MAIL_SERVER_FILE,"r") as f:  
    data = yaml.load(f, Loader=yaml.SafeLoader)
    # Note: using 'FullLoader' would be nicer and if you get the error "AttributeError: module 'yaml' has no attribute 'FullLoader'" then do as follows:
    # If you are managing packages with pip, you can upgrade to the current release by running:
    #   pip install -U PyYAML
    # If you are managing packages with conda, you can upgrade to the current release by running:
    #   conda install PyYAML
    #print(data)

user = data["user"]
pwd = data["pwd"]
server = data["server"]
port = data["port"]

#print(f"Here is your private data:\n   user = {user}\n   pwd = {pwd}\n   server = {server}\n   port = {port}")

# FINISHED GETTING THE SERVER'S DATA

def mail(toAddrsList, ccList, bccList, subject, text, html, attachmentsList):
    msg = MIMEMultipart("alternative", None, [MIMEText(text), MIMEText(html,'html')])
    msg['From'] = MYADDRESS
    msg['Subject'] = subject
    msg['To'] = ",".join(toAddrsList)
    msg['CC'] = ",".join(ccList)
    msg['BCC'] = ",".join(bccList)
    msg.attach(MIMEText(text))

    #managing the attachmentsList
    for attach in attachmentsList:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(attach, 'rb').read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        'attachment; filename="%s"' % os.path.basename(attach))
        msg.attach(part)

    mailServer = smtplib.SMTP(server, port)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.login(user, pwd)
    recipientsList = toAddrsList + ccList + bccList
    print("sending message to: " + ",".join(recipientsList))
    mailServer.sendmail(MYADDRESS, recipientsList, msg.as_string())
    mailServer.quit()
    mailServer.close()


    
def send_one_mail(MODE, DATE, ID_STUDENT, DEST_MAIL_ADDRESS, DEST_ANCHOR, DEST_PWD, DEST_SURNAME, DEST_NAME, SHUTTLE_FOLDER, with_tgz, without_zip, with_encrypted_tgz, without_encrypted_zip, with_tgz_attached, with_zip_attached):
    global CCLIST, BCCLIST
    with_web_server_download = with_tgz or not without_zip
    with_encrypted_download = with_encrypted_tgz or not without_encrypted_zip
    with_attachment_download = with_tgz_attached or with_zip_attached
    
    # ELABORATIONS ON THE STUDENT'S DATA:

    rel_path_ZIP_file_for_student = f"esame-RO_{DATE}_{DEST_ANCHOR}__{ID_STUDENT}/esame-RO_{DATE}_{ID_STUDENT}.zip"

    rel_path_TGZ_file_for_student = f"esame-RO_{DATE}_{DEST_ANCHOR}__{ID_STUDENT}/esame-RO_{DATE}_{ID_STUDENT}.tgz"

    rel_path_ENCRYPTED_ZIP_file_for_student = f"esame-RO_{DATE}__{ID_STUDENT}/esame-RO_{DATE}_{ID_STUDENT}.zip"

    rel_path_ENCRYPTED_TGZ_file_for_student = f"esame-RO_{DATE}__{ID_STUDENT}/esame-RO_{DATE}_{ID_STUDENT}.tgz"

    # NOW WE CHECK THAT THE FILES WITH THE FILENAMES AS IN THE ANNOUNCEMENT MAIL WE ARE GOING TO SEND INDEED EXIST (AT LEAST IN THE SHUTTLE FOLDER):

    def confirm_to_continue():
        answ=input("Do you want to continue with this student (yY), or skip this one student (kK), or abort (just RETURN) the whole send_all_mails process that might have triggered this single send_one_mail process? ")
        if answ.upper() == 'Y':
            print(f"Ok, we go ahead and anyhow complete the intended action ({argv[1]}) with this one student ({ID_STUDENT})")
            return "continue"
        elif answ.upper() == 'K':
            print(f"\nOk, we just skip this one student ({ID_STUDENT})")
            return "skip"
        else:
            print("Ok. The (possibly inner) script for the sending of one single mail is aborted with error and termination signal!")
            return "stop"

    if not without_zip:
        if not os.path.exists(SHUTTLE_FOLDER+'/'+rel_path_ZIP_file_for_student):
            print(f"\n{CRED}{CBOLD}WARNING:{CEND} could not find the file:\n   {rel_path_ZIP_file_for_student}\nin the shuttle folder:\n   {SHUTTLE_FOLDER}\n")
            answ=confirm_to_continue()
            if answ!="continue":
                return answ
            print("Ok, REMOVED any mention to the anchored URL for the download also from the mail. We proceed.\n")
            press_RETURN_to_continue()
            without_zip=True
            with_web_server_download = with_tgz or not without_zip

    if with_tgz:
        if not os.path.exists(SHUTTLE_FOLDER+'/'+rel_path_TGZ_file_for_student):
            print(f"\n{CRED}{CBOLD}WARNING:{CEND} could not find the file:\n   {rel_path_TGZ_file_for_student}\nin the shuttle folder:\n   {SHUTTLE_FOLDER}\n")
            answ=confirm_to_continue()
            if answ!="continue":
                return answ
            print("Ok, REMOVED any mention to the anchored URL for the download also from the mail. We proceed.\n")
            press_RETURN_to_continue()
            with_tgz=False
            with_web_server_download = with_tgz or not without_zip

    ATTACHMENTLIST=[]
    if with_zip_attached:
        if not os.path.exists(SHUTTLE_FOLDER+'/'+rel_path_ZIP_file_for_student):
            print(f"\n{CRED}{CBOLD}WARNING:{CEND} could not find the file:\n   {rel_path_ZIP_file_for_student}\nin the shuttle folder:\n   {SHUTTLE_FOLDER}\n")
            answ=confirm_to_continue()
            if answ!="continue":
                return answ
            print("Ok, REMOVED this last attachment from the attachments' list of the mail. We proceed.\n")
            press_RETURN_to_continue()
            with_zip_attached=False
            with_attachment_download = with_tgz_attached or with_zip_attached
        else:
            ATTACHMENTLIST.append(SHUTTLE_FOLDER + '/' + rel_path_ZIP_file_for_student)

    if with_tgz_attached:
        if not os.path.exists(SHUTTLE_FOLDER+'/'+rel_path_TGZ_file_for_student):
            print(f"\n{CRED}{CBOLD}WARNING:{CEND} could not find the file:\n   {rel_path_TGZ_file_for_student}\nin the shuttle folder:\n   {SHUTTLE_FOLDER}\n")
            answ=confirm_to_continue()
            if answ!="continue":
                return answ
            print("Ok, REMOVED this last attachment from the attachments' list of the mail. We proceed.\n")
            press_RETURN_to_continue()
            with_tgz_attached=False
            with_attachment_download = with_tgz_attached or with_zip_attached
        else:
            ATTACHMENTLIST.append(SHUTTLE_FOLDER + '/' + rel_path_TGZ_file_for_student)
            
    if not without_encrypted_zip:
        if not os.path.exists(SHUTTLE_FOLDER+'/'+rel_path_ENCRYPTED_ZIP_file_for_student):
            print(f"\n{CRED}{CBOLD}WARNING:{CEND} could not find the file:\n   {rel_path_ENCRYPTED_ZIP_file_for_student}\nin the shuttle folder:\n   {SHUTTLE_FOLDER}\n")
            answ=confirm_to_continue()
            if answ!="continue":
                return answ
            print("Ok, CANCELED the sending of the missing zip on Telegram.\n")
            press_RETURN_to_continue()
            without_encrypted_zip=True
            with_encrypted_download = with_encrypted_tgz or not without_encrypted_zip

    if with_encrypted_tgz:
        if not os.path.exists(SHUTTLE_FOLDER+'/'+rel_path_ENCRYPTED_TGZ_file_for_student):
            print(f"\n{CRED}{CBOLD}WARNING:{CEND} could not find the file:\n   {rel_path_ENCRYPTED_TGZ_file_for_student}\nin the shuttle folder:\n   {SHUTTLE_FOLDER}\n")
            answ=confirm_to_continue()
            if answ!="continue":
                return answ
            print("Ok, CANCELED the sending of the missing tgz on Telegram.\n")
            press_RETURN_to_continue()
            with_encrypted_tgz=False
            with_encrypted_download = with_encrypted_tgz or not without_encrypted_zip
            
    # FINISHED CHECKING EXISTENCE OF THE ANNOUNCED FILES  

    # NOW DECIDING WHETHER AND WHERE TO ACTUALLY SEND THE MAIL:

    if argv[1] != "SUDO":
        print("If you had called this script with the SUDO option, then I would be performing the following action:")
    print("Sending a mail to the following people:")
    print(f"   DEST_MAIL_ADDRESS={DEST_MAIL_ADDRESS}")
    print(f"   CCLIST={CCLIST}")
    print(f"   BCCLIST={BCCLIST}")
    print(f"   student ID={ID_STUDENT}")
    print(f"   Name of the recipient student: {DEST_NAME}")
    print(f"   Surname of the recipient student: {DEST_SURNAME}")
    if argv[1] == "SAY":
        print("However, you called me with the SAY option. Therefore, no true action has been undertaken.\n")
        return "only say"
    if argv[1] == "ME":
        DEST_MAIL_ADDRESS=MYADDRESS
        CCLIST = CCLIST_FOR_ME_EXPERIMENTS
        BCCLIST = []
        print(f"However, you called me with the ME option. Therefore, that mail has actually been sent to you ({MYADDRESS}) so that you can have a look at it before proceeding in the sconsiderate act of sending tons of these mails.")

    mail([DEST_MAIL_ADDRESS], CCLIST, BCCLIST,
         mail_templates.subject(DATE),
         mail_templates.body_as_text(DEST_NAME, DEST_SURNAME, DEST_PWD, DEST_ANCHOR, with_tgz, not without_zip, with_encrypted_tgz, not without_encrypted_zip, with_tgz_attached, with_zip_attached, SHUTTLE_FOLDER_ON_WEB_SERVER, rel_path_ZIP_file_for_student, rel_path_TGZ_file_for_student, GRUPPO_TELEGRAM=GRUPPO_TELEGRAM, STANZA_ZOOM=STANZA_ZOOM),
         mail_templates.body_as_html(DEST_NAME, DEST_SURNAME, DEST_PWD, DEST_ANCHOR, with_tgz, not without_zip, with_encrypted_tgz, not without_encrypted_zip, with_tgz_attached, with_zip_attached, SHUTTLE_FOLDER_ON_WEB_SERVER, rel_path_ZIP_file_for_student, rel_path_TGZ_file_for_student, GRUPPO_TELEGRAM=GRUPPO_TELEGRAM, STANZA_ZOOM=STANZA_ZOOM),
         ATTACHMENTLIST)

    if not without_encrypted_zip:
        if MODE == "SUDO":
            os.system(f'telegram-send --config {CONFIG_TELEGRAM_SEND_RO_GROUP_FILE} --file {SHUTTLE_FOLDER}/{rel_path_ENCRYPTED_ZIP_file_for_student}   --caption "Exam for student {DEST_NAME} {DEST_SURNAME}"')
            print("Sent on Telegram a .zip archive accessible to {ID_STUDENT}.")
        else:
            print("If you had called this script with the SUDO option, then we would also be adding the encrypted zip file over the Telegram Group.")



def main():
    global CSV_FILE_WITH_STUDENTS, SHUTTLE_FOLDER

    parser=argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=usage,
    epilog="""-------------------""")
    parser.add_argument('mode', type=str, choices=['SUDO', 'ME', 'SAY'], help='choose one option in the set { SUDO | ME | SAY }', default='SAY')
    parser.add_argument('ID_student', type=str, help='the ID of the recipient student (has the form id??????)}', default='id123456')
    parser.add_argument('--shuttle', type=str, help=f'use this optional argument to specify a different name/location for the shuttle folder (the default is SHUTTLE_FOLDER={SHUTTLE_FOLDER}, that is, "shuttle" in the parent directory)', default=SHUTTLE_FOLDER)
    parser.add_argument('--csv_file', type=str, help=f'use this optional argument to specify a different name for the csv_file offering the list of the subscribed students with their keys (the default is CSV_FILE_WITH_STUDENTS={CSV_FILE_WITH_STUDENTS}, that is, "lista_studenti_iscritti_con_chiavi.csv" in the parent directory)', default=CSV_FILE_WITH_STUDENTS)
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

    with open(f"{CSV_FILE_WITH_STUDENTS}") as csv_file:
        found = False
        for row in list(csv.reader(csv_file)):
           if found and row[4]==args.ID_student:
              print(f"{CRED}{CBOLD}WARNING:{CEND} the student with code ={args.ID_student} occurs twice in your file {CSV_FILE_WITH_STUDENTS}\nIn these case we take take the first occurrence as the good one.",file=stderr)
              press_RETURN_to_continue()
           if not found and row[4]==args.ID_student:
              found=True
              DEST_MATRICOLA = row[0]
              DEST_ANCHOR = row[2]
              DEST_PWD = row[3]
              DEST_NAME = row[5]
              DEST_SURNAME = row[6]
              DEST_MAIL_ADDRESS = row[7]

    if not found:
       print(f"{CRED}{CBOLD}CRITICAL ERROR:{CEND} ID_student={args.ID_student} not found in the file {CSV_FILE_WITH_STUDENTS}\nNo action has been taken.",file=stderr)
       exit(1)

    lista_cartelle = os.listdir(SHUTTLE_FOLDER)
    DATE = None
    for name in lista_cartelle:
       if os.path.isdir(SHUTTLE_FOLDER+'/'+name):
          if len(name)>20 and name[8]=='_' and name[13]=='-' and name[16]=='-' and name[19]=='_' and name[-8:] == args.ID_student:
             DATE = name[9:19]
             print(f"A folder for student {CBOLD}{args.ID_student}{CEND} has been found with exam date {CBOLD}{CYELLOW}{DATE}{CEND}. Possiamo proseguire ...")
             break
    if DATE == None: 
        print(f"\nERROR: the SHUTTLE_FOLDER directory {SHUTTLE_FOLDER} does not contain any folder whose name has the proper format for an exam folder for student {CBOLD}{args.ID_student}{CEND}. Fill up the shuttle properly and start me again.")
        exit(1)
        
    
    send_one_mail(args.mode, DATE, args.ID_student, DEST_MAIL_ADDRESS, DEST_ANCHOR, DEST_PWD, DEST_SURNAME, DEST_NAME, SHUTTLE_FOLDER, args.with_tgz, args.without_zip, args.with_encrypted_tgz, args.without_encrypted_zip, args.with_tgz_attached, args.with_zip_attached)

    
    print(f"Ok. The (possibly inner) script for the sending of one single mail (virtually to {args.ID_student}) has successfully terminated!\n")
    exit(0)

if __name__ == "__main__":
    main()
