# chat-room-python
Simple Chat Room with Client-Server model using TCP protocol and socket module in Python

L'applicativo permette di chattare contemporaneamente con più utenti collegati ad un server. Ciascun utente prima di entrare nella chat-room è invitato ad 
inserire il proprio nickname in modo tale da poter essere riconosciuto. Ogni volta che un nuovo utente si collega al server la sua paretcipazione viene notificata 
all'intera chat-room. L'applicativo è composto da due elementi principali: un Server ed un Client. 
Il server rimane in costante ascolto per fornire la connessione ad eventuali client che si vogliono collegare.

Il funzionamento è realizzato in Python attraverso l'utilizzo del modulo socket e il protocollo TCP.
L'interfaccia utente è stata realizzata con la libreria grafica di python: Tkinter

