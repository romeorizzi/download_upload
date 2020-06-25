#!/bin/bash
set -e
echo
echo "Sono lo script che crea automaticamente, secondo configurazioni standard, i seguenti file:"
echo "   1. lista_studenti_iscritti.csv"
echo "   2. lista_studenti_iscritti_con_chiavi.csv"
echo " partento dal file ListaStudentiEsameExportExcel.xls degli studenti iscritti all'appello scaricato da esse3."
echo
echo "ATTENZIONE: ricordati di non modificare questi file dopo che hai cominciato ad utilizzarli per non creare inconsistenze tra le varie cose che genererai partendo da essi. Se li modifici riparti da capo dall'esecuzione del presente script."
echo
echo "Creating the file: lista_studenti_iscritti.csv"
xls2csv ListaStudentiEsameExportExcel.xls | cut -d, -f3,4,5,6,13 | sort | grep "^\"VR" > lista_studenti_iscritti.csv
echo "Fatto! The file lista_studenti_iscritti.csv has been created."
echo
echo "Creating the file: lista_studenti_iscritti_con_chiavi.csv"
./add_chiavi_al_csv_file.py -n 6 "" "" 15
echo "Fatto! The file lista_studenti_iscritti_con_chiavi.csv has been created."
echo
echo "Trovi una ToDo list delle prossime cose da fare nel file passi_da_compiere_dopo_aver_generato_il_file_con_chiavi.md"
echo -e "Le prossime cose che devi fare sono:" > passi_da_compiere_dopo_aver_generato_il_file_con_chiavi.md
echo -e "   1. generare i vari testi dei temi per gli studenti, sfruttando il file lista_studenti_iscritti_con_chiavi.csv e collocarli, ciascuno in una sua cartella separata di nome esame_RO-yyyy-mm-dd_ANCORA_ID dentro la cartella shuttle.\n     Quì si assume che:\n        yyyy-mm-dd sia la data dell'appello\n        ANCORA sia la stringa nella colonna 4 del file lista_studenti_iscritti_con_chiavi.csv (esempio: NNCUPAJGiKV2Qsb)\n        ID sia l'id dello studente (esempio: id826yor)\n      Si assume inoltre che il testo del tema, collocato dentro la cartella di cui sopra, sia un archzio compresso in formato 7z e di nome esame_RO-yyyy-mm-dd_ID.7z" >> passi_da_compiere_dopo_aver_generato_il_file_con_chiavi.md
echo -e "   2. lanciare lo script run_after_exam_texts_in_shuttle.sh per predisporre la cartella shuttle in modo che possa essere caricata sul Web Server per gli accessi degli studenti regolati da credenziali." >> passi_da_compiere_dopo_aver_generato_il_file_con_chiavi.md
echo -e "   3. clonare la cartella shuttle sul Web Server agendo dalla cartella VPN_clone_shuttle. (Anche se caricati sul Web Server i temi non saranno ancora accessibili fino a quando non invierai le mail con le credenziali.)" >> passi_da_compiere_dopo_aver_generato_il_file_con_chiavi.md
echo -e "   4. dare avvio all'esame inviando le mail con le credenziali di accesso. Puoi fare questo agendo dalla cartella send_the_mails utilizando gli script che trovi dentro di essa." >> passi_da_compiere_dopo_aver_generato_il_file_con_chiavi.md

