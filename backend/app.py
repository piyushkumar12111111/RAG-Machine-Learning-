
from flask import Flask, request, jsonify
from flask_cors import CORS
import fitz  
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

app = Flask(__name__)
CORS(app)  


def extract_text_from_pdf(pdf_path):
    pdf_document = fitz.open(pdf_path)
    text = ""
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    return text


def split_text_into_chunks(text, chunk_size=1000):
    words = text.split()
    chunks = [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
    return chunks


pdf_paths = [
    r'C:/Users/hp/Downloads/NCERT-Solutions-for-Class-12-March-30-Biology-Chapter-5-Principles-of-Inheritance-and-Variation.pdf',
    r'C:/Users/hp/Downloads/updated_resume-4-1.pdf'
]

all_chunks = []
pdf_chunks = {}
for pdf_path in pdf_paths:
    pdf_text = extract_text_from_pdf(pdf_path)
    chunks = split_text_into_chunks(pdf_text)
    pdf_chunks[pdf_path] = chunks
    all_chunks.extend([(chunk, pdf_path) for chunk in chunks])


all_texts = [chunk[0] for chunk in all_chunks]
vectorizer = TfidfVectorizer().fit(all_texts)
vectors = vectorizer.transform(all_texts).toarray()

@app.route('/query', methods=['POST'])
def query_pdf():
    query = request.json['query']
    query_vec = vectorizer.transform([query]).toarray()
    cosine_similarities = cosine_similarity(query_vec, vectors).flatten()

   
    most_similar_chunk_idx = cosine_similarities.argmax()
    most_relevant_chunk, most_relevant_pdf = all_chunks[most_similar_chunk_idx]

    
    relevant_chunks = pdf_chunks[most_relevant_pdf]
    relevant_vectors = vectorizer.transform(relevant_chunks).toarray()
    cosine_similarities_in_pdf = cosine_similarity(query_vec, relevant_vectors).flatten()
    most_relevant_chunk_idx_in_pdf = cosine_similarities_in_pdf.argmax()
    best_chunk = relevant_chunks[most_relevant_chunk_idx_in_pdf]

    response = {
        'document': os.path.basename(most_relevant_pdf),
        'text': best_chunk
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)