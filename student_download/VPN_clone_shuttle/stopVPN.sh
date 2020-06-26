#!/bin/bash
OCPID=$(pgrep -x lt-openconnect)
echo Processo OpenConnect $OCPID
echo Per terminare la connessione VPN dare la password per sudo
echo '(se gia` data proseguira` automaticamente)'
sudo kill -HUP $OCPID
echo ''
