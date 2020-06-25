Per clonare lo shuttle sul Web Server (in questo caso su profs di uniVR) devi eseguire i 3 scripts nella presente directory nel seguente ordine (ed alimentarli dei dati richiesti mano a mano).

./startVPN.sh
./clone_shuttle.sh
./stopVPN.sh

Finito questo la cartella shuttle è stata clonata con tutti i temi, ma nessuno (tranne tè che hai tutte le credenziali) potrà ancora accedere ad essi fino a quando non avrai fatto avere le credenziali agli studenti.

## Cancellare file e cartelle da remoto

srm -r rzzrmo30@profs.sci.univr.it:~/public_html/classes/RO/shuttle

Command 'srm' not found, but can be installed with:

sudo apt install secure-delete

