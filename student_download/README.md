# Come far accedere ogni studente al suo tema d'esame

Nota: i temi d'esame assegnati agli studenti non sono necessariamente tutti uguali, possono essere organizzati in file per non comportare la tentazione a copiare (ed i temi possono anche essere tutti diversi, ossia le file possono essere di un solo studente ciascuna. Di fatto questo è quanto facciamo noi col tema di Ricerca Operativa). Nel seguito vedremo come il gestire questa complessità in modo robusto possa essere di fatto semplice.
Nel seguito assumiamo che il docente abbia già predisposto uno script `generaTemaEsame` che, data in input la matricola dello studente e la data dell'appello, genera un file compresso omonimo (eccetto l'estensione) di una cartella (di nome MATRICOLA_2020-06-30) contenente tutti i file del testo d'esame per quello studente a quell'appello. 

## PUNTO DI PARTENZA

La prima cosa da fare per allestire (sul solo piano tecnico) un appello è procurarsi o generare un file `.csv` dove ogni riga ha il sequente formato:

<matricola>,<cognome>,<nome>,<anno accademico di frequenza><indirizzo>

A seconda degli atenei o dei sitemi potrebbe essere tipo:
"VR431431","ROSSI","MARIO","2018/2019","id431rossim@studenti.univr.it"

Nota 1: in generale ci piace lavorare con questi indirizzi mail basati sull'id studente piuttosto che con quelli ottenibili automaticamente dalla matricola perchè la matricola cambia col passaggio da triennale a magistrale mentre l'id offre una maggiore stabilità.

Nota 2: per quanto non necessario avremo piacere di lavorare con un file dove le righe sono lessicograficamente ordinate (per matricola).

Assumeremo che tale file si chiami lista_studenti_iscritti.csv e sia collocato nella stessa cartella del presente `README.txt`

## COME OTTENERE IL FILE `lista_studenti_iscritti.csv`

Per ottenere un tale file puoi partire da un `.csv` più ricco, oppure da un `.xls` come faremo noi quì sotto, oppure da un `.txt` che potrai ottenere per copia-incolla (ad esempio tramite `Ctrl-C Ctrl-V`) prendendo i pezzi di dati di interesse da un qualsiasi documento (anche un `.pdf` ben formato può prestarsi a copia ed incolla) contenente la lista degli iscritti all'appello.


Nel nostro caso (il nostro ateneo utilizza `esse3`), per produrre il file `lista_studenti_iscritti.csv` partiamo dal file `ListaStudentiEsameExportExcel.xls` che è possibile scaricare pigiando un simbolo in alto quando si visualizzi la "Lista degli Iscritti" all'appello e successivamente pigiando direttamente il tasto "Esporta" senza bisogno di riconfigurare nulla delle opzioni di default su cosa si vuole appaia nel file.

Quindi, da terminale, eseguiamo il comando:

```
xls2csv ListaStudentiEsameExportExcel.xls | cut -d, -f3,4,5,6,13 | sort | grep "^\"VR" > lista_studenti_iscritti.csv
```

## COME OTTENERE IL FILE `lista_studenti_iscritti_con_chiavi.csv`

Dalla cartella dove si trova il file `lista_studenti_iscritti.csv` lancia lo script:

```
./add_chiavi_al_csv_file.py -n 6 "" "" 15
```

Se vuoi conoscere di più sullo script e su come personalizzare la generazione, e sempre assumendo tu sia nella cartella dovi si trova lo script, lancia:

```
./add_chiavi_al_csv_file.py -h
```

Il file `lista_studenti_iscritti_con_chiavi.csv` che in fasi successive ti servirà per (1) la generazione dei testi d'esame da assegnare a ciascun studente e (2) per garantire l'accesso, privato e regolato da credenziali, di ciascun studente al proprio esame, sarà generato automaticamente partendo dal file `lista_studenti_iscritti.csv` che però viene arricchito con l'introduzione di una stringa di ancoraggio privata per ogni studente e di una password di accesso. Questi dati verranno utilizzati per consentire ad ogni singolo studente l'accesso al suo testo d'esame ed il download dello stesso.
