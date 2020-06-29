Lo shuttle è quella cartella che verrà clonata identica sul Web Server, da dove i subfolder dello shuttle saranno accessibili agli studenti con le credenziali di accesso per quel subfolder. L'idea è di prevedere una sottocartella per ogni fila del testo d'esame. Chiamiamo quì file le diverse versioni di un testo d'esame come predisposte per non indurre gli studenti a copiare. Possiamo prevedere fino ad una fila per ogni studente, e di fatto negli esami in telematico è consigliabile assegnare agli studenti dei testi d'esame tutti diversi, ossia l'uso di file d'esame private. Di fatto il numero delle sottocartelle eccederà poi il numero degli studenti effettivi per la presenza di utenti e file di prova.
Il nome di ciascuna sottocartella contiene una lunga stringa casuale detta ancora, chi non conosce l'ancora non potrà accedere alla sottocartella.
La cartella folder deve pertento contenere il file .htaccess che serve per oscurare i nomi di tutte le sue sottocartelle, così che esse non siano accessibili se non da chi ne conosce le ancore. Ogni studente potrà accedere solo alla sua fila, o comunque esclusivamente all'insieme di cartelle stabilito da noi. 
Il file .htaccess è in tutto caratterizzato da:
shuttle$ cat .htaccess 
Options -Indexes
shuttle$ ls -l  .htaccess 
-rw-r--r--  .htaccess
