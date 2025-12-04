# ServerWebSocketSSL
## Protocollo
Per gestire le comunicazioni tra client e server è previsto l'utilizzo dei seguenti codici
|Comando|Client|Server|
|----|----|----|
|Accessso|A:-*username*:-*password*|U:-*Risultato*|
|Invio Messaggio|M:-*username*:-*SecureC*:-*command*|R:-*Feedback*|

Per ogni comando il server potrebbe rispondere in vari modi.
|Comando   |Stato       |Risposta       |
|---|---|---|
|Accesso    |Successo / Fallimentare   |U:-OK:-*SecureC* / U:-E0   |
|Invio Messaggio|Scritto bene / Scritto male|R:-*Feedback* / R:-E1|

Nelle tabelle, sono utilizzati gli asterrsichi * per rappresentare il nome di una variabile che assumerà un valore preciso. Nello specifico i significati delle parole sono:
1. *Feedback*: indica il dato restituito a seguito all'esecuzione del comando dato;
2. *SecureC*: per essere sicuri che la persona non si stia fingendo un'altra, viene attribuito a ciascun utente un numero di 5 cifre casuale il SecureC;
3. *username*: il nome dell'utente che vuole eseguire il log in;
4. *password*: la password dell'utente;
5. *command*: il comando che si vuole eseguire.
