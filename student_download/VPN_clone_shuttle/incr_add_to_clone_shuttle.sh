#!/bin/bash
echo "Per entrare su profs devi prima attivare la VPN (credenziali GIA, e meccanismo di Dario così non si bloccherà il browser ed altre connessioni correntemente aperte."
echo "Attivata la VPN, l'accesso a profs NON mi richiede attualmente le credenziali in quanto profs ha la mia chiave pubblica."
scp -r ../shuttle/esame_* rzzrmo30@profs.sci.univr.it:~/public_html/classes/RO/shuttle
current_time=`date +%s`
total_time=$((current_time-start_time))
echo 
echo "Questa aggiunta incrementale allo shuttle sul web server ha preso TEMPO TOTALE= $total_time"
exit 0
