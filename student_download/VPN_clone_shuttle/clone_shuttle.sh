#!/bin/bash
BOLD='\e[1m'
RED='\033[0;31m'
CYAN='\033[0;36m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo -e "SE NON SEI IN UNIVERSITA': Per entrare su profs devi prima attivare la VPN (credenziali GIA, e meccanismo di Dario così non si bloccherà il browser ed altre connessioni correntemente aperte.\n(Invece, una volta attivata la VPN, l'accesso a profs NON mi richiede attualmente le credenziali in quanto profs ha la mia chiave pubblica.)"
read -p "Sei pronto per proseguire? Hai ora attivato la VPN (oppure SEI IN UNI)? (YySs)? " -n 1 -r
if [[ ! $REPLY =~ ^[YySs]$ ]]; then
    echo -e "\nOk, senza la VPN e DA FUORI UNI non si può agire sul web server e facciamo prima ad uscire.\nOperazione abortita!"
    exit 1
fi

if ssh rzzrmo30@profs.sci.univr.it 'test -e ~/public_html/classes/RO/shuttle'; then
    num_students=$(ssh rzzrmo30@profs.sci.univr.it 'ls -d ~/public_html/classes/RO/shuttle/esame-RO_????-??-??_???????????????__id?????? | wc -l')
    echo -e "\n${BOLD}${CYAN}WARNING!!!${NC}  Uno shuttle folder è già presente sul web server (e contiene ${BOLD}${GREEN}$num_students${NC} student's subfolders)."
    echo -e "Sei sicuro di voler ricostruire da zero lo shuttle sul web server in remoto?\n(Considera anche la possibilità di utilizzare lo script per l'aggiunta incrementale di cartelle allo shuttle)"
    read -p "Proseguire sovrascrivendo interamenete lo shuttle sul web server in remoto? (YySs)? " -n 1 -r
    if [[ ! $REPLY =~ ^[YySs]$ ]]; then
        echo -e "\nOk, script abortito!"
        exit 1
    else
        ./remove_shuttle_from_WebServer.sh
    fi
fi
start_time=`date +%s`
ssh rzzrmo30@profs.sci.univr.it 'mkdir ~/public_html/classes/RO/shuttle'
scp -r ../shuttle/esame-RO_????-??-??_???????????????__id??????   rzzrmo30@profs.sci.univr.it:~/public_html/classes/RO/shuttle/
current_time=`date +%s`
total_time=$((current_time-start_time))
echo 
echo "Clonare lo shuttle sul web server ha preso TEMPO TOTALE= $total_time secondi"
exit 0
