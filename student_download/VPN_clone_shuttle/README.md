Per clonare lo shuttle sul Web Server (in questo caso su profs di uniVR) devi eseguire 3 passi:

1. se richiesto per accedere al server, attivare una VPN.

   A seconda della tua situazione, puoi predisporti degli scrip per automatizzare o semi-automatizzare questa operazione.
   Ad esempio, quando ancora la VPN a VR seguiva standard parcchio suoi io mi ero fatto i segunti script (ora del tutto superati anche in termino di qualità del servizio):  

   ./startVPN.sh   (per aprire la VPN)
   ./stopVPN.sh   (per poi chiudere la VPN una volta terminato il cloning)

2. lancio (cloning) della cartella shuttle:

   Per fare questo lancia lo script:
     ./clone_shuttle.sh

   Al termine di questo script (progredirà lentamente perchè stà copiando file in remoto via ssh) la cartella shuttle è stata clonata con tutti i temi, ma nessuno (tranne tè che hai tutte le credenziali) potrà ancora accedere ad essi fino a quando non avrai fatto avere le credenziali agli studenti.

3. chiudere la VPN

## Cancellare file e cartelle da remoto

srm -r rzzrmo30@profs.sci.univr.it:~/public_html/classes/RO/shuttle

Command 'srm' not found, but can be installed with:

sudo apt install secure-delete

