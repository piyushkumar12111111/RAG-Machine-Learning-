# backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import fitz  # PyMuPDF
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

app = Flask(__name__)
CORS(app)  # Enable CORS

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_path):
    pdf_document = fitz.open(pdf_path)
    text = ""
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    return text

# Load and process the specified PDF
pdf_path = r'C:\Users\hp\Downloads\updated_resume-4-1.pdf'
pdf_text = extract_text_from_pdf(pdf_path)
documents = [pdf_text]

# TF-IDF Vectorization
vectorizer = TfidfVectorizer()
vectorizer.fit(documents)
vectors = vectorizer.transform(documents).toarray()

@app.route('/query', methods=['POST'])
def query_pdf():
    query = request.json['query']
    query_vec = vectorizer.transform([query]).toarray()
    cosine_similarities = cosine_similarity(query_vec, vectors).flatten()
    most_similar_doc_idx = cosine_similarities.argmax()
    response = {
        'document': os.path.basename(pdf_path),
        'text': pdf_text
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
