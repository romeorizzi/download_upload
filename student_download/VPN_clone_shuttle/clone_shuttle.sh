#!/bin/bash
echo "per entrare su profs devi prima attivare la VPN. Lei ti bloccherà il browser."
echo "l'accesso a profs NON mi richiede attualmente le credenziali in quanto profs ha la mia chiave prubblica."
scp -r ../shuttle rzzrmo30@profs.sci.univr.it:~/public_html/classes/RO/shuttle
