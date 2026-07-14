from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# URL dell'API del backend
BACKEND_API_URL = "http://localhost:8000/api/search"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/input", methods=["POST"])
def input():
    if request.method == "POST":
        # prelevo gli ingredienti inseriti dall'utente nel form HTML
        ingredienti_utente = request.form["ingredients"]
        
        try:
            # invio i dati all'API facendo una richiesta POST JSON
            response = requests.post(BACKEND_API_URL,  json={"ingredients": ingredienti_utente}, timeout=30)
            
            # verifica della risposta dell'API (200 OK)
            if response.status_code == 200:
                risposta_json = response.json()
                ricette_trovate = risposta_json.get("data", [])
            else:
                ricette_trovate = []
                print(f"Errore del backend: {response.status_code}")

        except requests.exceptions.RequestException as e:
            ricette_trovate = []
            print(f"Impossibile connettersi al backend: {e}")
        
        # rendering alla pagina del result
        return render_template("result.html", recipes=ricette_trovate, query=ingredienti_utente)

if __name__ == "__main__":
    # facciamo girare l'app sulla port 5000
    app.run(host="0.0.0.0", port=5000, debug=True)