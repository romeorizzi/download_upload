#!/bin/bash
echo -e "SE NON SEI IN UNIVERSITA': Per entrare su profs devi prima attivare la VPN (credenziali GIA, e meccanismo di Dario così non si bloccherà il browser ed altre connessioni correntemente aperte.\n(Invece, una volta attivata la VPN, l'accesso a profs NON mi richiede attualmente le credenziali in quanto profs ha la mia chiave pubblica.)"
read -p "Sei pronto per proseguire? Hai ora attivato la VPN (oppure SEI IN UNI)? (YySs)? " -n 1 -r
if [[ ! $REPLY =~ ^[YySs]$ ]]; then
    echo -e "\nOk, senza la VPN e DA FUORI UNI non si può agire sul web server e facciamo prima ad uscire.\nOperazione abortita!"
    exit 1
fi

start_time=`date +%s`
for f in ../shuttle/esame-RO_????-??-??_???????????????__id?????? ; do
    if ssh rzzrmo30@profs.sci.univr.it 'test -e ~/public_html/classes/RO/shuttle'; then
        scp -r $f  rzzrmo30@profs.sci.univr.it:~/public_html/classes/RO/shuttle/
    fi
done
current_time=`date +%s`
total_time=$((current_time-start_time))
echo 
echo "Questa aggiunta incrementale allo shuttle sul web server ha preso TEMPO TOTALE= $total_time" secondi
exit 0
