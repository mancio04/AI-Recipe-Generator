from flask import Flask, render_template, request
from ml.src.recipe_retrival import cerca_ricette
app = Flask(__name__)

#rendering to the homepage
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/input', methods=['POST'])
def generate():
    if request.method == 'POST':
        
        ingredienti_utente = request.form['ingredienti']
        
        ricette_trovate = cerca_ricette(ingredienti_utente)
        
        # Passa la lista di dizionari alla pagina dei risultati
        return render_template('result.html', recipes=ricette_trovate, query=ingredienti_utente)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)