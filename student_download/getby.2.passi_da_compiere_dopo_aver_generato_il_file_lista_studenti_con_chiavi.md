Le prossime cose che devi fare sono:
   1. generare i vari testi dei temi per gli studenti, sfruttando il file lista_studenti_iscritti_con_chiavi.csv e collocarli, ciascuno in una sua cartella separata di nome esame_RO-yyyy-mm-dd_ANCORA_ID dentro la cartella shuttle.
     Quì si assume che:
        yyyy-mm-dd sia la data dell'appello
        ANCORA sia la stringa nella colonna 4 del file lista_studenti_iscritti_con_chiavi.csv (esempio: NNCUPAJGiKV2Qsb)
        ID sia l'id dello studente (esempio: id826yor)
      Si assume inoltre che il testo del tema, collocato dentro la cartella di cui sopra, sia un archivio compresso in formato 7z e di nome esame_RO-yyyy-mm-dd_ID.7z
   2. lanciare lo script ht_loader.py per predisporre la cartella shuttle in modo che possa essere caricata sul Web Server per gli accessi degli studenti regolati da credenziali.
      Va lanciato attraverso python:
       > python ht_loader.py yyyy-mm-dd
   3. clonare la cartella shuttle sul Web Server agendo dalla cartella VPN_clone_shuttle. (Anche se caricati sul Web Server i temi non saranno ancora accessibili fino a quando non invierai le mail con le credenziali.)
   4. dare avvio all'esame inviando le mail con le credenziali di accesso. Puoi fare questo agendo dalla cartella send_the_mails utilizando gli script che trovi dentro di essa.
