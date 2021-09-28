import telebot
from zipfile import ZipFile
import requests
import os

API_TOKEN = ""
bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['help', 'start','consegna'])
def send_welcome(message):
    bot.reply_to(message, """\
Vuoi consegnare? \nTrascina qui la tua cartella generata dalla mappa (Se hai il mac puoi anche non zipparla ci pensa Telegram) che ha come nome il tuo id e contiene: \n - la mappa \n - la firma anticipata \n - l'esame zippato \
""")

#gestisce messaggi text
@bot.message_handler(func=lambda message: True)
def message(message):
    bot.reply_to(message, "Azione non supportata, carica il file o scrivi uno dei seguenti comandi /consegna /start /help") 
#gestisce documenti
@bot.message_handler(content_types=['document', 'file'])
def check(message):
    if message.document.file_name[:2]!="id": #si potrebbe mettere la lista_studenti e verificare che sia all'interno degli iscritti
        bot.reply_to(message, "ATTENZIONE il nome NON è corretto deve essere il tuo id! Coreggi e rinvia.")
    elif message.document.mime_type[12:]!= "zip": #solo zip perchè lo coprime telegram(non sempre windows no)
        bot.reply_to(message, "Il formato NON è corretto. Correggi e rinvia")
    else:
        file_info = bot.get_file(message.document.file_id)
        file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(API_TOKEN, file_info.file_path))
        open(message.document.file_name, 'wb').write(file.content)
        with ZipFile(message.document.file_name) as zipObj:
            listOfiles = zipObj.infolist()
            #print(listOfiles)
        if len(listOfiles) not in [3,4]: #4 perchè mac crea DS_store devo verificare cosa accade per windows
            bot.reply_to(message, "ATTENZIONE manca uno dei tre elementi richiesti! Sistema e rinvia.")
        else:
            print('Esame di: ', message.from_user.first_name, message.from_user.last_name)
            print('Username Telegram:',message.from_user.username)
            with ZipFile(message.document.file_name, 'r') as zip:
                #zip.printdir()
                zip.extractall() 
                os.remove(message.document.file_name)
            os.chdir(message.document.file_name[:8])
            with ZipFile("esame_RO-"+"2021-06-18_"+message.document.file_name, 'r') as zip:
                zip.extractall() 
            os.remove("esame_RO-"+"2021-06-18_"+message.document.file_name)
            #check allegati



            totalFiles = 0
            tot_im=0

            for base, dirs, files in os.walk(os.getcwd()):
                for Files in files:
                    if (Files.lower().endswith('.png') or Files.lower().endswith('.jpg') or Files.lower().endswith('.jpeg')) and Files.lower()[0]!=".":
                        print(Files.lower())
                        tot_im+=1
                    totalFiles += 1
            
            os.chdir(os.path.normpath(os.getcwd() + os.sep + os.pardir))

            print('Numero allegati  :',tot_im-1)#-1 per la favicon
            print('Esame scaricato!')
            print()
            bot.reply_to(message, f"L'esame è coerente con quanto richiesto. Il numero di allegati che hai aggiunto è {tot_im-1}. Il tuo esame è finito. Ciao! Rimani nel gruppo telegram per avere aggiornamenti su voti ed esame orale")
            



bot.polling()