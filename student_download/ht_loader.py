#!/usr/bin/python3
# quando avevo problemi con le troppe installazioni di python, questo script lo laciavo da terminale con python3. Ora ho installasto passlib su conda e posso così trattarlo come uno script.

from sys import argv, exit, stderr
import os
import csv
import sys
import re
from passlib.apache import HtpasswdFile

CSV_FILE_WITH_STUDENTS = "lista_studenti_iscritti_con_chiavi.csv"
SHUTTLE_FOLDER = "shuttle"
SHUTTLE_TEMPLATES_FOLDER = "shuttle_templates"
ABSOLUTE_PATH_TO_HTPASSWD_ON_WEB_SERVER = "/home/accounts/personale/rzzrmo30/public_html/classes/RO/shuttle"
FILE_PWD_ADMIN_ESAMI = "../../credenziali_per_scripts_in_repo_pubblici/pwd_admin_passwd_esami_download.yaml"


def usage(onstream):
    print(f"\nUsage: ./{os.path.basename(argv[0])}  yyyy-mm-dd  [ shuttle_folder [ csv_students_file [ {{ md5 | clear }} ] ] ]\n\n   The first parameter is the date of the exam.\n   I tre parametri opzionali che vanno semmai precisati nell'ordine sono:\n   shuttle_folder (default {SHUTTLE_FOLDER}) che specifica il percorso della cartella shuttle\n   csv_students_file (default {CSV_FILE_WITH_STUDENTS}) che specifica il percorso del csv file con le credenziali degli studenti\n   the third optional parameter is either literally 'md5' when present) se si vuole l'encryption di tipo md5 oppure 'clear' se si vuole che le credenziali siano gestite in chiaro da htpasswd.\n\nSi presume che in shuttle ci siano gi le cartelle degli studenti cos nominate '22-06-30_anchor_matricola'.\nLo script va a creare in ogni cartella i due file .htaccess e .htpasswd (user  la matricola, la password  quella del csv file).", file=onstream)
 
# THE MAIN PROGRAM:
if len(argv) > 5:
    print(f"You gave this script {len(argv)-1} parameters. Expecting at most 4 (all optionals).")
    usage(stderr)
    exit(1)

if len(argv) == 1:
    print(f"You gave this script no parameter but at least the date of the exam is mandatory.")
    usage(stderr)
    exit(1)

if not os.path.exists(FILE_PWD_ADMIN_ESAMI):
    print(f"Questo script ({argv[0]}) opera a partire dal file {FILE_PWD_ADMIN_ESAMI}. Tale file contiene le credenziali di accesso htpasswd riservate ai supervisori di un esame ed è pertanto stato disposto esternamente alla repo git pubblica.\nQuesto file contiene esclusivamente una stringa cheè la password di tali amministratori scritta in chiaro.\n\nESECUZIONE INTERROTTA: File {FILE_PWD_ADMIN_ESAMI} con le credenziali di accesso al server di posta non trovato.", file=stderr)
    exit(1)

with open(FILE_PWD_ADMIN_ESAMI,"r") as f:
    pwd_admin = f.read().strip().replace("\n", "")
    #print(f"pwd_admin = {pwd_admin}")

    
DATE=argv[1]
pattern = re.compile("^[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]$")
if not pattern.match(DATE):
    print(f"Your third parameter (namely, {DATE}) should rather be a date of the form yyyy-mm-dd (like e.g. 2020-06-30).")
    usage(stderr)
    exit(1)
    
if len(argv) > 2:    
    SHUTTLE_FOLDER = sys.argv[2]
if len(argv) > 3:    
    CSV_FILE_WITH_STUDENTS = sys.argv[3]
if len(argv) == 5 and argv[4] != "md5" and argv[4] != "clear":
    print(f"You gave this script a third parameter {argv[4]}. However, when the third parameter is present it should be either 'md5' or 'clear'.")
    usage(stderr)
    exit(1)


csv_dict = {}

htaccess = """AuthName auth_name
AuthType Basic
AuthUserFile psw_path
Require valid-user
"""

#csv parsing 
with open(f"{CSV_FILE_WITH_STUDENTS}", "r") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for lines in csv_reader:
        id=lines[5].split("@")[0]
        csv_dict.update({id:{'name':None,'surname':None,'psw':None,'anchor':None,'id_mail_address':None,'matricola':None}})
        csv_dict[id].update({'name':lines[6]})
        csv_dict[id].update({'surname':lines[7]})
        csv_dict[id].update({'psw':lines[4]})
        csv_dict[id].update({'anchor':lines[3]})
        csv_dict[id].update({'id_mail_address':lines[5]})
        csv_dict[id].update({'matricola':lines[1]})

#uncomment to create all empty student dirs {SHUTTLE_FOLDER}/esameRO-{DATE}_anchor_matricola
"""
for key in csv_dict:
    os.mkdir(f"{SHUTTLE_FOLDER}/esameRO-{DATE}_{csv_dict[key]['anchor']}_{key}/")
"""
README = """Questa cartella è lo shuttle che da quì verrà clonato identico sul Web Server da dove i suoi subfolder saranno accessibili agli studenti con le credenziali di accesso per quel subfolder. L'idea è che il folder shuttle abbia una sottocartella er ogni fila del testo d'esame, dove le file (=versioni diverse del testo) possono essere fino ad una per ogni studente (più altri utenti di prova).
Il nome di ciascuna sottocartella contiene una lunga stringa casuale detta ancora, chi non conosce l'ancora non potrà accedere alla sottocartella.
La cartella folder deve pertento contenere il file .htaccess che serve per oscurare tutte le sue sottocartelle, così che esse non siano accessibili se non da chi ne conosce le ancore. Ogni studente potrà accedere solo alla sua fila (o comunque all'insieme di cartelle deciso da noi). 
Il file .htaccess è in tutto caratterizzato da:
shuttle$ cat .htaccess 
Options -Indexes
shuttle$ ls -l  .htaccess 
-rw-r--r--  .htaccess
"""
risp = os.system(f"cat {README} {SHUTTLE_FOLDER}/README.txt")
risp = os.system(f"cp {SHUTTLE_TEMPLATES_FOLDER}/.htaccess {SHUTTLE_FOLDER}/") # come prima cosa ci assicuriamo di oscurare il listing della cartelle per il dopo atterraggio dello shuttle
#create .htaccess and .htpasswd (user:matricola) for every subfolder
def create_ht(key,folder,htaccess,csv_dict):
    user_htaccess = htaccess.replace('auth_name','"'+csv_dict[key]['matricola']+'"').replace('psw_path',ABSOLUTE_PATH_TO_HTPASSWD_ON_WEB_SERVER+'/'+folder+'/.htpasswd')
    ht = HtpasswdFile(SHUTTLE_FOLDER+'/'+folder+'/.htpasswd', new=True)
    ht.set_password(csv_dict[key]['matricola'],csv_dict[key]['psw'])
    ht.set_password("admin",pwd_admin)
    ht.save()
    with open(SHUTTLE_FOLDER+'/'+folder+'/.htaccess','w') as f:
        f.write(user_htaccess)

folders = os.listdir(SHUTTLE_FOLDER)        
for name in folders:
   if os.path.isdir(SHUTTLE_FOLDER+'/'+name):
      if len(name)>29:
         if name[9:19] == DATE:
             print(f"Adding .htaccess file to folder {name} of the shuttle.") 
             key = name[-8:]
             create_ht(key,name,htaccess,csv_dict)

        
		
