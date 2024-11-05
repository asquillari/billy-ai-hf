from flask import Flask, request, jsonify
from transformers import pipeline
import os

app = Flask(__name__)

# Cargar el modelo de clasificación de Hugging Face
model_name = "facebook/bart-large-mnli"
classifier = pipeline("zero-shot-classification", model=model_name)

# Ruta principal que muestra "Hello, World!"
@app.route('/', methods=['GET'])
def hello_world():
    return jsonify({"message": "Hello, World!"})

# Ruta de verificación de salud (Health Check)
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

# Ruta para clasificar texto en categorías
@app.route('/categorize', methods=['POST'])
def categorize():
    data = request.get_json()
    description = data.get('description')
    categories = data.get('categories')

    if not description or not categories:
        return jsonify({"error": "Missing description or categories"}), 400

    try:
        # Clasificación del texto con el modelo de Hugging Face
        result = classifier(description, candidate_labels=categories)
        category = result["labels"][0]  # Tomar la primera categoría como resultado
        return jsonify({"category": category})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Ejecutar la aplicación en el puerto 80 para producción
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 80)))