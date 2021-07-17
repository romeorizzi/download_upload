#!/usr/bin/python3
def subject():
    return "ESAME di Ricerca Operativa: ecco l'ancora privata e le tue credenziali per scaricarti il testo per l'esame di Ricerca Operativa"

def body_as_text(DEST_NAME, DEST_SURNAME, DEST_PWD, SHUTTLE_FOLDER_ON_WEB_SERVER=None, rel_path_ZIP_file_for_student=None, rel_path_TGZ_file_for_student=None, GRUPPO_TELEGRAM=None, STANZA_ZOOM=None):
    return f"""
Caro/a {DEST_NAME} {DEST_SURNAME},
puoi ora scaricarti (consigliamo sul Desktop/Scrivania) il file compresso col tuo testo per l'esame di Ricerca Operativa dal seguente URL:

   {SHUTTLE_FOLDER_ON_WEB_SERVER}/{rel_path_ZIP_file_for_student}

Se cliccando sullo URL non succede nulla (dipende dalla configurazione del tuo mailer) allora copia ed incolla lo URL in un browser.
In ogni caso, per accedere dovrai immettere la tua matricola nella forma VR?????? come username e la seguente password:

Password: {DEST_PWD}


In realtà, come sempre, se disponi di un terminale (con shell bash o equivalenti) un modo alternativo, più diretto ed efficace, per ottenere il file è immettere da terminale il comando:

wget --user <VR??????> --password <vedi sopra> {SHUTTLE_FOLDER_ON_WEB_SERVER}/{rel_path_ZIP_file_for_student}

In questo modo non solo scaricherai il testo d'esame direttamente dove vorrai lavorare al tuo elaborato ma potrai anche beneficiare di tutta la robustezza di wget in caso di connessione instabile.

All'interno dell'archivio trovi un file README.txt che spiega come dare avvio all'esame.

Buon Esame!

P.S. In caso incontrassi difficoltà non mancare di segnalarcele subito chiedendo aiuto. 

La stanza Zoom di riferimento è:
{STANZA_ZOOM}

Il gruppo Telegram di riferimento è quello del corso:
{GRUPPO_TELEGRAM}

"""

def body_as_html(DEST_NAME, DEST_SURNAME, DEST_PWD, SHUTTLE_FOLDER_ON_WEB_SERVER=None, rel_path_ZIP_file_for_student=None, rel_path_TGZ_file_for_student=None, GRUPPO_TELEGRAM=None, STANZA_ZOOM=None):
    return f"""
<html><body>
<p>Caro/a {DEST_NAME} {DEST_SURNAME},</p>
<p>puoi ora scaricarti (consigliamo sul Desktop/Scrivania) il file compresso col tuo testo per l'esame di Ricerca Operativa dal seguente URL:</p>
<p></p>
<p><a href="{SHUTTLE_FOLDER_ON_WEB_SERVER}/{rel_path_ZIP_file_for_student}">{SHUTTLE_FOLDER_ON_WEB_SERVER}/{rel_path_ZIP_file_for_student}</a></p>
<p></p>
<p>Se cliccando sullo URL da te scelto non succede nulla (dipende dalla configurazione del tuo mailer) allora copia ed incolla lo URL in un browser. In ogni caso, per accedere dovrai immettere la tua matricola nella forma VR?????? come username e la seguente password:</p>
<p></p>
<p>Password: {DEST_PWD}</p>
<p></p>
<p></p>
<p>In realtà, come sempre, se disponi di un terminale (con shell bash o equivalenti) un modo alternativo, più diretto ed efficace, per ottenere il file è immettere da terminale il comando:</p>
<p></p>
<p>wget --user VR?????? --password quella_specificata_sopra {SHUTTLE_FOLDER_ON_WEB_SERVER}/{rel_path_ZIP_file_for_student}</p>
<p></p>
<p>In questo modo non solo scaricherai il testo d'esame direttamente dove vorrai lavorare al tuo elaborato ma potrai anche beneficiare di tutta la robustezza di wget in caso di connessione instabile.</p>
<p></p>
<p></p>
<p>Buon Esame!</p>
<p></p>
<p></p>
<p>P.S. In caso incontrassi difficoltà non mancare di segnalarcele subito e di chiedere aiuto.</p><p></p>
<p>La stanza Zoom di riferimento è:</p>
<p>{STANZA_ZOOM}</p><p></p>

<p>Il gruppo Telegram di riferimento è quello del corso:</p>
<p>{GRUPPO_TELEGRAM}</p>
</body></html>
"""

