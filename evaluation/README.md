# Evaluation

La valutazione del modello è stata fatta prendendo in esame la metrica **Recall@N**. Questa tecnica consiste nel trovare la proporzione fra il numero di documenti rilevanti recuperati e il numero di tutti i documenti rilevanti disponibili nella collezione considerata.

Per implementare la valutazione è stato preso un campione casuale di ricette dal dataset. Poi, per ogni ricetta di questo campione, è stato preso un sottoinsieme di ingredienti e dato come input al modello, che ritornerà le N ricette più simili. Il risultato ottenuto viene così confrontato con la ricetta originale per capire se questa è stata trovata e restituita dal modello.

Tradotta al nostro caso d'uso la Recall@N è quindi espressa dalla seguente formula:
<br>
$$Recall@N = (correct) / (tested)$$
<br>
dove:

- *correct* è il numero di volte che una ricetta è stata trovata fra le prime *N*
- *tested* è il numero di volte che è stato effettuato l'esperimento

## Interpretazione Grafica

Il seguente grafico mostra come si comporta il modello al variare del parametro *N* e della percentuale di ingredienti presa da una ricetta.

![evaluation](./img/evaluation.png)

Come ci aspettiamo, il grafico si comporta come segue:

- più ingredienti vengono forniti, maggiore è la facilità con cui si recupera una ricetta
- se N aumenta, la probabilità di trovare la ricetta aumenta

Le prestazioni peggiori si hanno ovviamente per il 30% degli ingredienti. Prendendone circa un terzo infatti il modello tende a dare priorità a quelle ricette che hanno numero di ingredienti e ingredienti simili a quel terzo.

Osservando la crescita delle curve ci accorgiamo che:

- se teniamo la percentuale fissa e aumentiamo N, le prestazioni aumentano in media del 15% circa
- se teniamo N fisso e aumentiamo la percentuale, le prestazioni aumentano in media del 68% circa

Quindi in generale è meglio fornire una lista di ingredienti più specifica in quanto il modello si comporta meglio di conseguenza.