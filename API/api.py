
from flask import Flask, request, jsonify
from src.recipe_retrival import cerca_ricette  

app = Flask(__name__)

# Endpoint dell'API (versione 1)
@app.route('/api/v1/search', methods=['POST'])
def search_recipe():
    
    data = request.get_json()
    
    if not data or 'ingredients' not in data:
        return jsonify({"status": "error", "message": "Missing 'ingredients' in request body"}), 400
        
    ingredienti = data.get('ingredients')
    
    try:
        risultati = cerca_ricette(ingredienti)
        return jsonify({
            "status": "success",
            "count": len(risultati),
            "data": risultati
        }), 200
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    #il backend gira sulla porta 8000
    app.run(host='0.0.0.0', port=8000, debug=True)