#!/usr/bin/python3

def subject(DATE):
    return f"ESAME di Ricerca Operativa {DATE}: ecco le tue credenziali per scaricarti il testo per l'esame"

def body_as_text(DEST_NAME, DEST_SURNAME, DEST_PWD, DEST_ANCHOR, with_tgz, with_zip, with_encrypted_tgz, with_encrypted_zip, with_tgz_attached, with_zip_attached, SHUTTLE_FOLDER_ON_WEB_SERVER=None, rel_path_ZIP_file_for_student=None, rel_path_TGZ_file_for_student=None, GRUPPO_TELEGRAM=None, STANZA_ZOOM=None):
    added_txt_when_exam_in_attachment=""
    if with_tgz_attached and with_zip_attached:
        added_txt_when_exam_in_attachment=f"Per altro, trovi gli archivi .zip e .tgz col tuo testo per l'esame di Ricerca Operativa in attachment alla presente mail.\n\n"
    elif with_zip_attached:
        added_txt_when_exam_in_attachment=f"Per altro, trovi l'archivio .zip col tuo testo per l'esame di Ricerca Operativa in attachment alla presente mail.\n\n"
    elif with_tgz_attached:
        added_txt_when_exam_in_attachment=f"Per altro, trovi l'archivio .tgz col tuo testo per l'esame di Ricerca Operativa in attachment alla presente mail.\n\n"
        
    body=f"""
Caro/a {DEST_NAME} {DEST_SURNAME},
puoi ora scaricarti (consigliamo sul Desktop/Scrivania) il file compresso col tuo testo per l'esame di Ricerca Operativa dal seguente URL:

   {SHUTTLE_FOLDER_ON_WEB_SERVER}/{rel_path_ZIP_file_for_student}

Se cliccando sullo URL non succede nulla (dipende dalla configurazione del tuo mailer) allora copia ed incolla lo URL in un browser.\n"""
    if with_tgz:
        body += f"Se preferisci un archivio .tgz utilizza allora lo URL:\n   {SHUTTLE_FOLDER_ON_WEB_SERVER}/{rel_path_TGZ_file_for_student}\n"
    body += f"""In ogni caso, per accedere dovrai immettere la tua matricola nella forma VR?????? come username e la seguente password:

   Password: {DEST_PWD}

Se disponi di un terminale (con shell bash o equivalenti) un modo alternativo per ottenere il file è avvalersi del comando wget, ad esempio:

   wget --user <VR??????> --password <vedi sopra> {SHUTTLE_FOLDER_ON_WEB_SERVER}/{rel_path_ZIP_file_for_student}

In questo modo non solo scaricherai il testo d'esame direttamente dove vorrai lavorare al tuo elaborato ma potrai anche beneficiare di tutta la robustezza di wget in caso di connessione instabile.\n"""
    if with_encrypted_zip:
        body += f"""Abbiamo inoltre inviato un'archivio .zip con lo stesso materiale sul gruppo Telegram del corso. E' uno .zip criptato che potrai aprire con la tua chiave segreta tramite il seguente comando:

   unzip -P {DEST_ANCHOR} {rel_path_ZIP_file_for_student.split('/')[-1]}\n\n"""   
    body += f"""{added_txt_when_exam_in_attachment}Qualunque sia stato il tuo percorso il risultato finale sarà in tutto equivalente. All'interno dell'archivio trovi un file README.txt che spiega come dare avvio all'esame.

Buon Esame!

P.S. In caso incontrassi difficoltà non mancare di segnalarcele subito chiedendo aiuto. 

La stanza Zoom di riferimento è:
    {STANZA_ZOOM}

Il gruppo Telegram di riferimento è quello del corso:
    {GRUPPO_TELEGRAM}
"""
    return body

def body_as_html(DEST_NAME, DEST_SURNAME, DEST_PWD, DEST_ANCHOR, with_tgz, with_zip, with_encrypted_tgz, with_encrypted_zip, with_tgz_attached, with_zip_attached, SHUTTLE_FOLDER_ON_WEB_SERVER=None, rel_path_ZIP_file_for_student=None, rel_path_TGZ_file_for_student=None, GRUPPO_TELEGRAM=None, STANZA_ZOOM=None):
    added_html_when_exam_in_attachment=""
    if with_tgz_attached and with_zip_attached:
        added_html_when_exam_in_attachment=f"<p>Per altro, trovi gli archivi .zip e .tgz col tuo testo per l'esame di Ricerca Operativa in attachment alla presente mail.</p><p></p>"
    elif with_zip_attached:
        added_html_when_exam_in_attachment=f"<p>Per altro, trovi l'archivio .zip col tuo testo per l'esame di Ricerca Operativa in attachment alla presente mail.</p><p></p>"
    elif with_tgz_attached:
        added_html_when_exam_in_attachment=f"<p>Per altro, trovi l'archivio .tgz col tuo testo per l'esame di Ricerca Operativa in attachment alla presente mail.</p><p></p>"
    
    body=f"""
<html><body>
<p>Caro/a {DEST_NAME} {DEST_SURNAME},</p>
<p>puoi ora scaricarti (consigliamo sul Desktop/Scrivania) il file compresso col tuo testo per l'esame di Ricerca Operativa dal seguente URL:</p>
<p></p>
<p><a href="{SHUTTLE_FOLDER_ON_WEB_SERVER}/{rel_path_ZIP_file_for_student}">{SHUTTLE_FOLDER_ON_WEB_SERVER}/{rel_path_ZIP_file_for_student}</a></p>
<p></p>
<p>Se cliccando sullo URL da te scelto non succede nulla (dipende dalla configurazione del tuo mailer) allora copia ed incolla lo URL in un browser.</p>"""
    if with_tgz:
        body += f"""<p>Se preferisci un archivio .tgz utilizza allora lo URL:</p><p><a href="{SHUTTLE_FOLDER_ON_WEB_SERVER}/{rel_path_TGZ_file_for_student}">{SHUTTLE_FOLDER_ON_WEB_SERVER}/{rel_path_TGZ_file_for_student}</a></p><p></p>"""
    body += f"""<p>In ogni caso, per accedere dovrai immettere la tua matricola nella forma VR?????? come username e la seguente password:</p>
<p></p>
<p>Password: {DEST_PWD}</p>
<p></p>
<p></p>
<p>Se disponi di un terminale (con shell bash o equivalenti) un modo alternativo per ottenere il file è avvalersi del comando wget, ad esempio:</p>
<p></p>
<p>wget --user VR?????? --password quella_specificata_sopra {SHUTTLE_FOLDER_ON_WEB_SERVER}/{rel_path_ZIP_file_for_student}</p>
<p></p>
<p>In questo modo non solo scaricherai il testo d'esame direttamente dove vorrai lavorare al tuo elaborato ma potrai anche beneficiare di tutta la robustezza di wget in caso di connessione instabile.</p>
<p></p>"""
    if with_encrypted_zip:
        body += f"""<p></p><p>Abbiamo inoltre inviato un'archivio .zip con lo stesso materiale sul gruppo Telegram del corso. E' uno .zip criptato che potrai aprire con la tua chiave segreta tramite il seguente comando:</p><p></p><p>unzip -P {DEST_ANCHOR} {rel_path_ZIP_file_for_student.split('/')[-1]}</p><p></p>"""
    body += f"""<p></p>
{added_html_when_exam_in_attachment}<p>Qualunque sia stato il tuo percorso il risultato finale sarà in tutto equivalente. All'interno dell'archivio trovi un file README.txt che spiega come dare avvio all'esame.</p>
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
    return body

