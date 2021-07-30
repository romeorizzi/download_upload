#!/bin/bash
#!/bin/bash
echo -e "SE NON SEI IN UNIVERSITA': Per entrare su profs devi prima attivare la VPN (credenziali GIA, e meccanismo di Dario così non si bloccherà il browser ed altre connessioni correntemente aperte.\n(Invece, una volta attivata la VPN, l'accesso a profs NON mi richiede attualmente le credenziali in quanto profs ha la mia chiave pubblica.)"

ssh rzzrmo30@profs.sci.univr.it 'rm -rf ~/public_html/classes/RO/shuttle'
