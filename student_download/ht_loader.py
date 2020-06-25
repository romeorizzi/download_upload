import os
import csv
import sys
from passlib.apache import HtpasswdFile

CSV_FILE_WITH_STUDENTS = "../lista_studenti_iscritti_con_chiavi.csv"
SHUTTLE_FOLDER = "../shuttle/"

def usage(onstream):
    print(f"\nUsage: ./{os.path.basename(argv[0])}  [ shuttle_folder [ csv_students_file [ {{ md5 | clear }} ] ] ]\n\n   where the first optional parameter shuttle_folder è il percorso della cartella shuttle (default {SHUTTLE_FOLDER})\n   the second optional parameter csv_students_file è il percorso del csv file con le credenziali degli studenti (default {CSV_FILE_WITH_STUDENTS})\n   the third optional parameter is either literally 'md5' when present) se si vuole l'encryption di tipo md5 oppure 'clear' se si vuole che le credenziali siano gestite in chiaro da htpasswd.\n\nSi presume che in shuttle ci siano già le cartelle degli studenti così nominate '22-06-30_anchor_matricola'.\nLo script va a creare in ogni cartella i due file .htaccess e .htpasswd (user è la matricola, la password è quella del csv file).", file=onstream)
 
# THE MAIN PROGRAM:
if len(argv) > 4:
    print(f"You gave this script {len(argv)-1} parameters. Expecting at most 3 (all optionals).")
    usage(stderr)
    exit(1)

if len(argv) > 1:    
    SHUTTLE_FOLDER = sys.argv[1]
if len(argv) > 2:    
    CSV_FILE_WITH_STUDENTS = sys.argv[2]
if len(argv) == 4 and argv[3] != "md5" and argv[3] != "clear":
    print(f"You gave this script a third parameter {argv[3]}. However, when the third parameter is present it should be either 'md5' or 'clear'.")
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
        csv_dict.update({lines[1]:{'name':None,'surname':None,'psw':None,'anchor':None}})
        csv_dict[lines[1]].update({'name':lines[6]})
        csv_dict[lines[1]].update({'surname':lines[7]})
        csv_dict[lines[1]].update({'psw':lines[4]})
        csv_dict[lines[1]].update({'anchor':lines[3]})

#uncomment to create all empty student dirs 2020-06-30_anchor_matricola
"""
for key in csv_dict:
    os.mkdir(SHUTTLE_FOLDER+'/2020-06-30_'+csv_dict[key]['anchor']+'_'+key+'/')
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


		
