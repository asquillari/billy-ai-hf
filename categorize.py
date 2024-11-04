from flask import Flask, request, jsonify
from transformers import pipeline

# Inicializar Flask
app = Flask(__name__)

# Cargar el modelo de clasificación
model_name = "facebook/bart-large-mnli"
classifier = pipeline("zero-shot-classification", model=model_name)

def classify_text(text, categories):
    """
    Clasifica un texto dado en las categorías proporcionadas.

    :param text: Texto a clasificar.
    :param categories: Lista de categorías posibles.
    :return: La categoría más alta asignada al texto.
    """
    result = classifier(text, candidate_labels=categories)
    print("Texto:", text)
    print("Categoría:", result["labels"][0])
    return result["labels"][0]

@app.route('/categorize', methods=['POST'])
def categorize():
    data = request.get_json()
    description = data.get('description')
    categories = data.get('categories')

    category = classify_text(description, categories)
    return jsonify({ "category": category })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)  # Asegúrate de que esté escuchando en el puerto correcto
