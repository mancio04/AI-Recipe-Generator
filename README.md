# AI-Recipe-Generator

L'obiettivo di questo progetto è realizzare un sistema di Recipe Retrieval, cioè un sistema in grado di individuare le ricette più adatte a partire da un insieme di ingredienti forniti dall'utente. Le ricette non vengono generate da zero ma vengono ricercate all'interno di un dataset sfruttando tecniche di Information Retrieval.

Durante lo sviluppo del progetto è stato utilizzato il dataset RecipeNLG per implementare il sistema di retrieval, basato sul modello Sentence-BERT (SBERT) e sulla libreria FAISS.

E’ stata sviluppata anche una semplice interfaccia web con Flask che consente all'utente di inserire gli ingredienti che ha a disposizione e ottenere le ricette più indicate.

Nel repository sono presenti due versioni del progetto:

1. una senza limitazione di memoria RAM (ne dovrebbero bastare 16GB)
2. una con limitazione di memoria a 8GB di RAM

La prima versione si trova nelle cartelle ```retrieval/v1``` e ```evaluation/v1```. La seconda nelle cartelle ```retrieval/v2``` e ```evaluation/v2```.

La prima versione può essere usata con docker, la seconda no. Di seguito verrà spiegato come poter usare il sistema per entrambe le versioni.

## Guida all'uso con docker (versione senza limite di memoria)

1.  Clonare il repository ed entrare nella cartella:
    ```bash
    git clone https://github.com/mancio04/AI-Recipe-Generator.git
    cd AI-Recipe-Generator
    ```

2.  Creare le cartelle necessarie:
    ```bash
    mkdir dataset idx
    ```

3.  Installare il dataset [RecipeNLG](https://recipenlg.cs.put.poznan.pl/) e spostarlo nella cartella dataset appena creata:
    ```bash
    unzip ~/Scaricati/dataset.zip -d dataset
    ```
    <p align="center"><b>Nota: assicurarsi che il dataset unzippato abbia nome full_dataset.csv</b></p>

4.  Creare il virtual environment e installare le dipendenze:
    ```bash
    uv venv
    source .venv/bin/activate
    uv pip install -r requirements.txt
    ```

5.  Normalizzare il dataset:
    ```bash
    python3 normalize.py
    ```

6.  Creare l'indice degli embeddings:
    ```bash
    python3 retrieval/v1/embeddings.py
    ```

7.  Creare l'immagine docker:
    ```bash
    sudo docker compose build --no-cache
    ```

8.  Avviare il backend:
    ```bash
    sudo docker run ai-recipe-generator-backend:latest
    ```

9.  Avviare il frontend:
    ```bash
    sudo docker run ai-recipe-generator-frontend:latest
    ```

10. A questo punto l'applicazione può essere usata al seguente [URL](http://localhost:5050)

## Guida all'uso senza docker (versione con limite di memoria)

1.  Clonare il repository ed entrare nella cartella:
    ```bash
    git clone https://github.com/mancio04/AI-Recipe-Generator.git
    cd AI-Recipe-Generator
    ```

2.  Creare le cartelle necessarie:
    ```bash
    mkdir dataset idx
    ```

3.  Installare il dataset [RecipeNLG](https://recipenlg.cs.put.poznan.pl/) e spostarlo nella cartella dataset appena creata:
    ```bash
    unzip ~/Scaricati/dataset.zip -d dataset
    ```
    <p align="center"><b>Nota: assicurarsi che il dataset unzippato abbia nome full_dataset.csv</b></p>

4.  Creare il virtual environment e installare le dipendenze:
    ```bash
    uv venv
    source .venv/bin/activate
    uv pip install -r requirements.txt
    ```

5.  Normalizzare il dataset:
    ```bash
    python3 normalize.py
    ```

6.  Creare l'indice degli embeddings:
    ```bash
    python3 retrieval/v2/embeddings_fragmented.py
    ```

7.  Cambiare la riga 2 del file ```app/backend/api.py``` in ```from src.retrieval_fragmented import search_recipes```

8.  Cambiare la riga 7 del file ```app/frontend/app.py``` in ```BACKEND_API_URL = "http://localhost:8000/api/search"```

9.  Avviare il backend:
    ```bash
    python3 app/backend/api.py
    ```

10. Avviare il frontend:
    ```bash
    python3 app/frontend/app.py
    ```

11. A questo punto l'applicazione può essere usata al seguente [URL](http://localhost:5000)