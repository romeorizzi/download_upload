#!/usr/bin/python3
from sys import argv, exit, stderr
import os
import csv
import sys
import ro
from passlib.apache import HtpasswdFile

CSV_FILE_WITH_STUDENTS = "lista_studenti_iscritti_con_chiavi.csv"
SHUTTLE_FOLDER = "shuttle"

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


filenames= os.listdir(SHUTTLE_FOLDER) #get all files' and folders' names in the indicated directory
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
        csv_dict.update({lines[1]:{'name':None,'surname':None,'psw':None,'anchor':None,'id_mail_address':None,'id':None}})
        csv_dict[lines[1]].update({'name':lines[6]})
        csv_dict[lines[1]].update({'surname':lines[7]})
        csv_dict[lines[1]].update({'psw':lines[4]})
        csv_dict[lines[1]].update({'anchor':lines[3]})
        csv_dict[lines[1]].update({'id_mail_address':lines[5]})
        csv_dict[lines[1]].update({'id':lines[5].split("@")[0]})

#uncomment to create all empty student dirs {SHUTTLE_FOLDER}/esameRO-{DATE}_anchor_matricola
"""
for key in csv_dict:
    os.mkdir(f"{SHUTTLE_FOLDER}/esameRO-{DATE}_{csv_dict[key]['anchor']}_{csv_dict[key]['id']}/")
"""

#create .htaccess and .htpasswd (user:matricola)
def create_ht(key,filename,htaccess,csv_dict):
    user_htaccess = htaccess.replace('auth_name','"'+key+'"').replace('psw_path',SHUTTLE_FOLDER+'/'+filename+'/.htpasswd')
    ht = HtpasswdFile(SHUTTLE_FOLDER+'/'+filename+'/.htpasswd', new=True)
    ht.set_password(key,csv_dict[key]['psw'])
    ht.set_password("rizzi_admin","rizzi_admin")
    ht.save()
    with open(SHUTTLE_FOLDER+'/'+filename+'/.htaccess','w') as f:
        f.write(user_htaccess)
		
#get all dir in shuttle			
for filename in filenames: # loop through all  folders
    if os.path.isdir(os.path.join(os.path.abspath(SHUTTLE_FOLDER), filename)): # check whether the current object is a folder or not
        key = filename[-8:]
        create_ht(key,filename,htaccess,csv_dict)


		
