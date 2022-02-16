Cose da avere:

1. il file lista_studenti_iscritti_con_chiavi.csv
   ottienilo con:
   download_upload/student_download$ cp ../../../esami-RO-private/students_lists/20yy-mm-dd/* .
2. lo shuttle folder con i temi
   ottienilo con:
   download_upload/student_download$ cp -r -d ../../../esami-RO-private/shuttle .

3. colloca dentro la cartella shuttle il file nascosto .htaccess   (NECESSARIO se vuoi che scarichino da WebServer)
   ottienilo con:
        download_upload/student_download$ cp htaccess_files/.htaccess shuttle/
   oppure sappi che il file .htaccess è in tutto caratterizzato da:
      1. shuttle$ cat .htaccess 
         Options -Indexes
	 
      2. shuttle$ ls -l  .htaccess
         -rw-r--r--  .htaccess
   e pertanto lo puoi produrre con:
      1. student_download$ echo -e "Options -Indexes\n" > shuttle/.htaccess
      2. student_download$ chmod u=rw,g=r,o=r shuttle/.htaccess
          oppure:
	 student_download$ chmod 644 shuttle/.htaccess

   Nota: per sapere di più sul ruolo di questo file .htaccess vedere le note nel file getby.htaccess, se rimangono dubbi cerca poi in rete, 

Cose da fare a quel punto:
1. clonare lo shuttle sul server che rende accessibili i temi e materiali privati (e spesso individuali) ai singoli studenti.

  Come farlo: entra nella cartella VPN_clone_shuttle ed esegui in sequenza:
      1. attiva la VPN (nel mio caso: entra con la username rzzrmo30 pigiando "Connext", ma forse prima devi aver pigato "Login"? (e forse "Login" senza 30?) )

2. inviare le mail con le credenziali di accesso ed istruzioni agli studenti

  Come farlo: entra nella cartella send_the_mails ed esegui quanto spiegato lì (gli script offrono help contestuale auto-esplicativo).
  E' quì molto importante che testi le cose per gradi:
    dimensione 1: prima SAY, poi ME, poi SUDO su ogni azione di invio mail.
    dimensione 2: prima usare lo script per inviare una singola mail (quella all'utente di prova VR123456), poi usare lo scrip per inviare la mail to all.

