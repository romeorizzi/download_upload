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

import mail_template_only_zip as chosen_mail_template
#import mail_template_zip_and_tgz as chosen_mail_template
#import mail_template_only_zip_on_Telegram as chosen_mail_template
#import mail_template_only_zip_on_both_Telegram_and_web_server as chosen_mail_template

CONFIG_MAIL_SERVER_FILE = "../../../credenziali_per_scripts_in_repo_pubblici/send_mail_config.yaml"
CSV_FILE_WITH_STUDENTS = "../lista_studenti_iscritti_con_chiavi.csv"
SHUTTLE_FOLDER_HERE = "../shuttle"
SHUTTLE_FOLDER_ON_WEB_SERVER = "http://profs.sci.univr.it/~rrizzi/classes/RO/shuttle"

STANZA_ZOOM="https://univr.zoom.us/j/3518684000"
GRUPPO_TELEGRAM="https://t.me/RicercaOperativa2021"

MYADDRESS = "romeo.rizzi@univr.it"
#CCLIST = ["romeo.rizzi@univr.it","alice.raffaele@univr.it"]
CCLIST = ["romeo.rizzi@univr.it","aurora.rossi@studenti.univr.it"]
CCLIST_FOR_ME_EXPERIMENTS = ["romeo.rizzi@univr.it", "romeorizzi05@gmail.com"]
BCCLIST = []
ATTACHMENTLIST=[]

EXT_COMPRESSION = "zip"


def usage(onstream):
    print(f"\nUsage: ./{os.path.basename(argv[0])}  {{ SUDO | ME | SAY }} code_of_the_recipient_student (VR??????) data_esame (yyyy-mm-dd\n\n)   where the three alternative options are:\n   * SUDO: really act! Send the mail to the person.\n   * ME: send the mail but to myself. In this way I can have a look at a few mails before sending a ton of them.\n   * SAY: only tell the action in the gun but do not really take it.\n\n   In my case in UniVR the code of the student has the form VR??????\n   The third and last parameter is the date of the exam and has the form yyyy-mm-dd.", file=onstream)

# student's code = matricola of the form VR?????? where each ? is a digit.
    

# THE MAIN PROGRAM:
if len(argv) != 4:
    print(f"You gave this script {len(argv)-1} parameters. Expecting 3.")
    usage(stderr)
    exit(1)

if argv[1] not in {"SUDO","ME","SAY"}:
    print(f"Your first parameter (namely, {argv[1]}) was neither 'SUDO', nor 'ME' nor 'SAY'.")
    usage(stderr)
    exit(1)

DATE=argv[3]
pattern = re.compile("^[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]$")
if not pattern.match(DATE):
    print(f"Your third parameter (namely, {DATE}) should rather be a date of the form yyyy-mm-dd (like e.g. 2020-06-30).")
    usage(stderr)
    exit(1)

DEST_STUDENT_CODE = argv[2]

# NOW WE GET THE STUDENT DATA:

if not os.path.exists(CSV_FILE_WITH_STUDENTS):
    print(f"Questo script ({argv[0]}) opera a partire dal file {CSV_FILE_WITH_STUDENTS}. Tale file contiene i dati degli studenti necessari all'invio delle mail che forniscano loro i punti di accesso e le credenziali personali. Il file .csv contiene una riga per ogni studente, suddivisa nei campi necessari affinche questo ed altri script della nostra architettura possano svolgere la loro funzione. Lo scritp si attende che tale file od un link ad esso sia presente nella cartella padre di quella dove lo script viene lanciato (che assumiamo essere .../student_download/send_the_mails/).\n\nESECUZIONE INTERROTTA: File {CSV_FILE_WITH_STUDENTS} con i dati degli studenti necessari all'invio delle mail non trovato.", file=stderr)
    exit(1)

with open(f"{CSV_FILE_WITH_STUDENTS}") as csv_file:
    found = False
    for row in list(csv.reader(csv_file)):
       if found and row[0]==DEST_STUDENT_CODE:
          print(f"WARNING: the student with code ={DEST_STUDENT_CODE} occurs twice in your file {CSV_FILE_WITH_STUDENTS}\nIn these case we take take the first occurrence as the good one.",file=stderr)
       if not found and row[0]==DEST_STUDENT_CODE:
          found=True
          DEST_ANCHOR = row[2]
          DEST_PWD = row[3]
          DEST_ID = row[4]
          DEST_NAME = row[5]
          DEST_SURNAME = row[6]
          DEST_MAIL_ADDRESS = row[7]

if not found:
   print(f"CRITICAL ERROR: DEST_STUDENT_CODE={DEST_STUDENT_CODE} not found in the file {CSV_FILE_WITH_STUDENTS}\nNo action has been taken.",file=stderr)
   exit(1)

# FINISHED GETTING IN THE STUDENT'S DATA

# NOW WE CHECK THAT THE FILES WITH THE FILENAMES AS IN THE ANNOUNCEMENT MAIL WE ARE GOING TO SEND INDEED EXIST (AT LEAST IN THE SHUTTLE FOLDER):

rel_path_ZIP_file_for_student = f"esame_RO-{DATE}_{DEST_ANCHOR}_{DEST_ID}/esame_RO-{DATE}_{DEST_ID}.zip"

rel_path_TGZ_file_for_student = f"esame_RO-{DATE}_{DEST_ANCHOR}_{DEST_ID}/esame_RO-{DATE}_{DEST_ID}.tgz"

def confirm_to_continue():
    answ=input("Do you want to continue with this student (yY), or skip this one student (kK), or abort the whole send_all_mails process that might have triggered this single send_one_mail process? ")
    if answ.upper() == 'Y':
        print(f"Ok, we go ahead and complete the intended action ({argv[1]}) with this one student ({DEST_ID})")
    elif answ.upper() == 'K':
        print(f"\nOk, we just skip this one student ({DEST_ID})")
        exit(1)
    else:
        print("Ok. The (possibly inner) script for the sending of one single mail is aborted with error and termination signal!")
        exit(2)    

if not os.path.exists(SHUTTLE_FOLDER_HERE+'/'+rel_path_ZIP_file_for_student):
    print(f"\nWARNING: could not find the file:\n   {rel_path_ZIP_file_for_student}\nin the shuttle folder:\n   {SHUTTLE_FOLDER_HERE}\nHowever, the mail we were going to send offers a link to such a file on the remote web server shuttle folder:\n   {SHUTTLE_FOLDER_ON_WEB_SERVER}\n")
    confirm_to_continue()

#if not os.path.exists(SHUTTLE_FOLDER_HERE+'/'+rel_path_TGZ_file_for_student):
#    print(f"\nWARNING: could not find the file:\n   {rel_path_TGZ_file_for_student}\nin the shuttle folder:\n   {SHUTTLE_FOLDER_HERE}\nHowever, the mail we were going to send offers a link to such a file on the remote web server shuttle folder:\n   {SHUTTLE_FOLDER_ON_WEB_SERVER}\n")
#    confirm_to_continue()
    
# FINISHED CHECKING EXISTENCE OF THE ANNOUNCED FILES  

# NOW DECIDING WHETHER AND WHERE TO ACTUALLY SEND THE MAIL:

if argv[1] != "SUDO":
    print("If you had called this script with the SUDO option, then I would be performing the following action:")
print("Sending a mail to the following people:")
print(f"   DEST_MAIL_ADDRESS={DEST_MAIL_ADDRESS}")
print(f"   CCLIST={CCLIST}")
print(f"   BCCLIST={BCCLIST}")
print(f"   student ID={DEST_ID}")
print(f"   Name of the recipient student: {DEST_NAME}")
print(f"   Surname of the recipient student: {DEST_SURNAME}")
if argv[1] == "SAY":
    print("However, you called me with the SAY option. Therefore, no true action has been undertaken.\n")
    exit(0)
if argv[1] == "ME":
    DEST_MAIL_ADDRESS=MYADDRESS
    CCLIST = CCLIST_FOR_ME_EXPERIMENTS
    BCCLIST = []
    print(f"However, you called me with the ME option. Therefore, that mail has actually been sent to you ({MYADDRESS}) so that you can have a look at it before proceeding in the sconsiderate act of sending tons of these mails.")


# NOW WE GET THE MAIL SERVER DATA:
    
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


mail([DEST_MAIL_ADDRESS], CCLIST, BCCLIST,
     chosen_mail_template.subject(),
     chosen_mail_template.body_as_text(DEST_NAME, DEST_SURNAME, DEST_PWD, SHUTTLE_FOLDER_ON_WEB_SERVER, rel_path_ZIP_file_for_student, rel_path_TGZ_file_for_student, GRUPPO_TELEGRAM, STANZA_ZOOM),
     chosen_mail_template.body_as_html(DEST_NAME, DEST_SURNAME, DEST_PWD, SHUTTLE_FOLDER_ON_WEB_SERVER, rel_path_ZIP_file_for_student, rel_path_TGZ_file_for_student, GRUPPO_TELEGRAM, STANZA_ZOOM),
     ATTACHMENTLIST)

print("Ok. The (possibly inner) script for the sending of one single mail (virtually to {STUD}) has successfully terminated!\n")
