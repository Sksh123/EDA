import os
from collections import Counter
import math

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read() 

def tokenize(text):
    # Tokenization logic can be customized based on requirements
    return text.split()

def calculate_tf_idf_vector(tokens, document_tokens_list):
    tf_idf_vector = {}
    num_documents = len(document_tokens_list)
    term_freq = Counter(tokens)

    for term in set(tokens):
        term_freq_in_document = sum(1 for doc_tokens in document_tokens_list if term in doc_tokens)
        idf = math.log(num_documents / (1 + term_freq_in_document))
        tf_idf_vector[term] = term_freq[term] * idf

    return tf_idf_vector

def cosine_similarity(v1, v2):
    dot_product = sum(v1.get(term, 0) * v2.get(term, 0) for term in set(v1) | set(v2))
    magnitude_v1 = math.sqrt(sum(v1[term] ** 2 for term in v1))
    magnitude_v2 = math.sqrt(sum(v2[term] ** 2 for term in v2))
    return dot_product / (magnitude_v1 * magnitude_v2)

def document_similarity(query_vector, document_vectors):
    similarities = []
    for i, doc_vector in enumerate(document_vectors):
        similarity = cosine_similarity(query_vector, doc_vector)
        similarities.append((i+1, similarity))
    return sorted(similarities, key=lambda x: x[1], reverse=True)

def main():
    # Input for query file
    query_file_path = input("Enter the query file path: ")

    # Input for document files
    document_file_paths = []
    for i in range(2):
        document_file_paths.append(input(f"Enter the file path for document {i+1}: "))

    try:
        # Read query text
        query_text = read_file(query_file_path)

        # Read document texts
        document_texts = [read_file(file_path) for file_path in document_file_paths]

        # Tokenize query and documents
        query_tokens = tokenize(query_text)
        document_tokens_list = [tokenize(doc_text) for doc_text in document_texts]

        # Calculate TF-IDF vectors for query and documents
        query_vector = calculate_tf_idf_vector(query_tokens, document_tokens_list)
        document_vectors = [calculate_tf_idf_vector(tokens, document_tokens_list) for tokens in document_tokens_list]

        # Calculate similarity
        similarities = document_similarity(query_vector, document_vectors)

        # Print results
        for doc_num, similarity in similarities:
            print(f"Document {doc_num}: Similarity Score = {similarity:.2f}")

    except FileNotFoundError as e:
        print(f"Error: {e.filename} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
