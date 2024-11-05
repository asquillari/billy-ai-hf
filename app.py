from flask import Flask, request, jsonify
from transformers import pipeline
import os

app = Flask(__name__)

model_name = "facebook/bart-large-mnli"
classifier = pipeline("zero-shot-classification", model=model_name)

def classify_text(text, categories):
    result = classifier(text, candidate_labels=categories)
    return result["labels"][0]

@app.route('/categorize', methods=['POST'])
def categorize():
    data = request.get_json()
    description = data.get('description')
    categories = data.get('categories')

    category = classify_text(description, categories)
    return jsonify({"category": category})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 80)))  # Cambiado a puerto 80