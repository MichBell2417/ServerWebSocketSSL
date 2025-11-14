# ServerWebSocketSSL
## Protocollo
Per gestire le comunicazioni tra client e server è previsto l'utilizzo dei seguenti codici
|Comando|Client|Server|
|----|----|----|
|Accessso|A:-*username*:-*password*|U:-*Risultato*|
|Invio Messaggio|M:-*username*:-*message*|R:-*Feedback*|

Per ogni comando il server potrebbe rispondere in vari modi.
|Comando   |Stato       |Risposta       |
|---|---|---|
|Accesso    |Successo / Fallimentare   |U:-success / U:-E0   |
|Invio Messaggio|Scritto bene / Scritto male|R:-*Feedback* / R:-E1|
