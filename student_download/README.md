# Come far accedere ogni studente al suo tema d'esame

Nota: i temi d'esame assegnati agli studenti non sono necessariamente tutti uguali, possono essere organizzati in file per non comportare la tentazione a copiare (ed i temi possono anche essere tutti diversi, ossia le file possono essere di un solo studente ciascuna. Di fatto questo è quanto facciamo noi col tema di Ricerca Operativa). Nel seguito vedremo come il gestire questa complessità in modo robusto possa essere di fatto semplice.
Nel seguito assumiamo che il docente abbia già predisposto uno script `generaTemaEsame` che, data in input la matricola dello studente (nella forma VR??????, dove ciascun ? è una cifra) e la data dell'appello (nella forma 2020-06-30), genera, entro la directory shuttle:

1. shuttle/esame_RO-2020-06-30_NNCUPAJGiKV2Qsb_id826yor/  una sottodirectory specifica per lo studente con quella matricola ed ID ad esempio id826yor
2. shuttle/esame_RO-2020-06-30_NNCUPAJGiKV2Qsb_id826yor/esame_RO-2020-06-30_id826yor/ una sottodirectory collocata entro essa nella quale si trova l'intero testo d'esame.

Utilizzando un'utility di compressione, lo script genera_gli_archivi_compressi.sh genera quindi il file compresso:

shuttle/esame_RO-2020-06-30_NNCUPAJGiKV2Qsb_id826yor/esame_RO-2020-06-30_id826yor.7z

Questo file compresso, omonimo alla cartella che contiene (eccetto l'estensione) contiene tutti i file del testo d'esame per quello specifico studente a quel specifico appello. 

## PUNTO DI PARTENZA

La prima cosa da fare per allestire (sul solo piano tecnico) un appello è procurarsi o generare un file `.csv` (che in seguito chiameremo `lista_studenti_iscritti.csv`) dove ogni riga contenga i dati di un diverso studente iscritto all'appello.
Senza una tale file non ti è nemmeno possibile gestire la generazioni di temi diversi a seconda dello studente.
A seconda degli atenei o dei sistemi, un tale file potrebbe ad esempio avere il seguente formato:

<matricola>,<anno accademico di frequenza>,<cognome>,<nome>,<indirizzo>

Eccone due possibili righe (la seconda è per l'utente di test, e le comunicazioni a lui sono quindi redirette come comunicazioni a mè):
```
VR431431,2018/2019,id948bch,ROSSI,MARIO,id431rossim@studenti.univr.it
VR123456,2001/2002,id123456,MY,TEST,romeo.rizzi@univr.it
```

Più sotto viene spiegato come ottenere un tale file `lista_studenti_iscritti.csv`. Hai più modi per farlo, anche in modo indipendente da quelli da noi suggeriti, ma è anche molto plausibile tu abbia già generato il file `lista_studenti_iscritti.csv` quando hai generato gli esami e magari hai anche generato, con procedimento automatico che parte da esso, il file `lista_studenti_iscritti_con_chiavi.csv`. E' questo un file `.csv` più ricco, con ulteriori colonne che offrono codici segreti che servono per rendere privato l'accesso dello studente all'esame che gli pertiene. Esso viene utilizzato da tutti quegli script di questa parte del repo `download_upload/student_download/` che si preoccupano di rendere accessibile ad ogni studente il suo tema d'esame da un sito internet.
Questi script assumono che il file `lista_studenti_iscritti_con_chiavi.csv` sia presente nella cartella `download_upload/student_download/` del presente repo.
Questo secondo file si chiama `lista_studenti_iscritti_con_chiavi.csv` e gli script di cui sopra assumono esso sia collocato nella stessa cartella del presente `README.txt`.
Ora entreremo nei dettagli di questi due file e della loro generazione, ma puoi saltare tutta questa szion se hai già un file `lista_studenti_iscritti_con_chiavi.csv` e ti assicuri di collocarlo nella stessa cartella del presente `README.txt`.  

Nota 1 [Criteri di preferenza sugli indirizzi mail da utilizzare] nel caso di Verona (più in generale dove ogni studente abbia sia una matricola che un id) l'indirizzo mail può essere ottenuto (anche automaticamente) come:

MODO PREFERITO (utilizzando lo student id):
   id963bch@studenti.univr.it
MODO ACCETTABILE1 (utilizzando la matricola dello studente):
   VR422428@studenti.univr.it
MODO ACCETTABILE2 (indirizzo specifico, eventualmente anche privato):
   mario.rossi_07@studenti.univr.it 
MODO PROBLEMATICO:
   nome.cognome@studenti.univr.it offre poche garanzie di funzionare dati i numerosi casi di omonimia (che verrebbero gestiti come da ultimo esempio sopra: mario.rossi_07@studenti.univr.it) 

Pertanto: in generale ci piace lavorare con gli indirizzi mail basati sull'id studente piuttosto che con quelli ottenibili automaticamente dalla matricola perchè la matricola cambia col passaggio da triennale a magistrale mentre l'id offre una maggiore stabilità.

Nota 2: per quanto non necessario avremo piacere di lavorare con un file dove le righe sono lessicograficamente ordinate (ossia per matricola).

## struttura del file `lista_studenti_iscritti_con_chiavi.csv`

Ove fosse presente, l'intestazione delle colonne per il file `lista_studenti_iscritti_con_chiavi.csv` sarebbe qualcosa tipo:

<matricola>,<anno accademico di frequenza>,<ancora>,<password>,<id_student>,<cognome>,<nome>,<indirizzo_mail>

Ecco due righe d'esempio:
```
VR422428,2019/2020,odTIqAkFIIq5l9r,283993,id963bch,MARIO,ROSSI,id431,USE_ID
VR123456,2001/2002,Dlh2IuCRbRWgNBn,233924,id123456,MY,TEST,romeo.rizzi@univr.it
```

dove per l'utente di test ho preferito impostare il mio indirizzo (docente che opera gli script e che così riceve un feedback ulteriore sul buon funzionamento del tutto) mentre per lo studente, piuttosto che fornire un indirizzo di mail specifico, ho preferito impiegare una keyword (`USE_ID`) che dice di utilizzare il campo `id_student` per l'ottenimento dell'indirizzo. L'altra keyword attualmente prevista è `USE_MATRICOLA`. 


## COME OTTENERE DIRETTAMENTE IL FILE `lista_studenti_iscritti_con_chiavi.csv` 

Se lo hai, colloca il file `ListaStudentiEsameExport.xls` nella cartella `download_upload/student_download` del presente repo, posizionati nella stessa cartella, e lancia lo script:

```
`./start_from_esse3_xls_students_file.sh
```

Se non hai dei prerequisiti che abbiamo assuno o se incontri malfunzionamenti prosegui nella lettura per suddividere l'operazione di intereesse (produzione del file `lista_studenti_iscritti_con_chiavi.csv`) in più passi e raccogliere le informazioni che ti consentono anche di prendere evntuali tue deviazioni.

## COME OTTENERE IL FILE `lista_studenti_iscritti.csv`

Per ottenere un tale file puoi partire da un `.csv` più ricco, oppure da un `.xls` come faremo noi quì sotto, oppure da un `.txt` che potrai ottenere per copia-incolla (ad esempio tramite `Ctrl-C Ctrl-V`) prendendo i pezzi di dati di interesse da un qualsiasi documento (anche un `.pdf` ben formato può prestarsi a copia ed incolla) contenente la lista degli iscritti all'appello.

Nel nostro caso (il nostro ateneo utilizza `Esse3`), per produrre il file `lista_studenti_iscritti.csv` partiamo dal file `ListaStudentiEsameExportExcel.xls` che è possibile scaricare cliccando un simbolo in alto quando si visualizza la "Lista degli Iscritti" all'appello e successivamente cliccando direttamente il tasto "Esporta" senza bisogno di riconfigurare nulla delle opzioni di default su cosa si vuole appaia nel file.

Una volta scaricato in locale il file `ListaStudentiEsameExportExcel.xls` o file ad esso analogo, ti converrà organizzarti in modo che il file `lista_studenti_iscritti.csv` possa essere automaticamente prodotto dal file `ListaStudentiEsameExport.xls` utilizzando il comando `xls2csv`. Pr farlo dovrai forse installarti `xls2csv` sul tuo sistema. Inoltre, se il tuo foglio elettronico di partenza differisce in formato dal nostro dovrai forse chiamare tale comando in modo diverso da come lo facciamo noi.

Quindi, da terminale, esegui il comando:

```
xls2csv ListaStudentiEsameExportExcel.xls | cut -d, -f3,4,5,6,14 | sort | grep "^\"VR" > lista_studenti_iscritti.csv
```

Questo sopra è solo un esempio di come potresti avvalerti del comando `xls2csv`, ma andrà probabilmente adattato al tuo uso e sistema (o anche solo per via dei continui aggiornamenti di Esse3 al proprio formato, purtroppo il concetto di API è estraneo a esse3).
Inoltre il file che produci con un comando così semplice andrebbe poi rettificato (ad esmpio aggiungndo uno studente di test e controllando non siano presenti caratteri strani od altre sporcizie).

Noi abbiamo messo a disposizione uno script (`start_from_esse3_xls_students_file.sh`) che fà tutto questo, con ambizione di produrre in modo del tutto automatizzato un file pulito, ed anche il file `lista_studenti_iscritti_con_chiavi.csv`. Lo script và però adattatato se tu parti da un altro tipo di file che non `ListaStudentiEsameExportExcel.xls` o anche quando Esse3 cambia i suoi formati. 

## COME OTTENERE IL FILE `lista_studenti_iscritti_con_chiavi.csv` PARTENDO DAL FILE FILE `lista_studenti_iscritti.csv`

Collocato il file `lista_studenti_iscritti.csv` nella cartella `download_upload/student_download` del presente repo e posizionati nella stessa cartella si lanci lo script:

```
`./add_chiavi_al_csv_file.py -n 6 "" "" 15
```

Dopo averlo eseguito senza errori, ora nella stessa cartella dovresti trovare anche il file `lista_studenti_iscritti_con_chiavi.csv` che in fasi successive ti servirà per (1) la generazione dei testi d'esame da assegnare a ciascun studente e (2) per garantire l'accesso, privato e regolato da credenziali, di ciascun studente al proprio esame.
Esso è stato generato automaticamente partendo dal file `lista_studenti_iscritti.csv` arricchendolo però con l'introduzione di una stringa di ancoraggio privata per ogni studente e di una password di accesso. Questi dati verranno utilizzati per consentire ad ogni singolo studente l'accesso al suo testo d'esame ed il download dello stesso.

Nota: il comportamento di `add_chiavi_al_csv_file.py` non vuole essere riproducibie nè prevedibile nel senso che ogni volta che lo rilanci verranno generate password ed ancore diverse. Questo è necessario per proteggere l'esame dato che questi codici sono pubblici.

Se vuoi conoscere di più sullo script e su come personalizzare la generazione, e assumendo tu sia nella cartella dovi si trova lo script (dentro `esami-RO-private/students_lists` di questo repo), lancia:

```
./add_chiavi_al_csv_file.py -h
```

Se vuoi saperne ancora di più o adattare ulteriormente, lo script è scritto per essere leggibile e non dovrebbe esserti difficile personalizzarlo. Se apporti delle integrazioni non distruttive (generalizzando o aggiungendo features) considera l'opportunità di fare una pull request in modo che il tuo branch possa rimanere centrale nel progetto. 
