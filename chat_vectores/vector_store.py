from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os
import pickle


"""
Carga un modelo de SentenceTransformer (all-MiniLM-L6-v2) para convertir textos en vectores (embeddings) de 384 dimensiones
"""
model = SentenceTransformer('all-MiniLM-L6-v2')

"""
Genera rutas para dos archivos: un índice FAISS (.index) y un archivo de metadatos (.pkl) para la IA llamada ia_name.
"""
def get_index_paths(ia_name):
    return f"memory/{ia_name}.index", f"memory/{ia_name}.meta.pkl)"

"""
Carga o crea Indices
- Si existen archivos previos, carga el índice FAISS y los metadatos.
- Si no, crea un nuevo índice FAISS (IndexFlatL2) para buscar por distancia euclidiana y una lista vacía de metadatos.
- dim=384 corresponde a la dimensión de los embeddings del modelo.
"""
def load_or_create_index(ia_name, dim=384):
    index_path, meta_path = get_index_paths(ia_name)

    if os.path.exists(index_path) and os.path.exists(meta_path):
        index = faiss.read_index(index_path)
        with open(meta_path, "rb") as f:
            metadata = pickle.load(f)
    elif os.path.exists(index_path) and not os.path.exists(meta_path):
        index = faiss.read_index(index_path)
        metadata = []  # Añadir metadatos vacíos
    else:
        index = faiss.IndexFlatL2(dim)
        metadata = []
    return index, metadata

"""
Guarda indices y metadatos
- Guarda el índice FAISS en un archivo .index y los metadatos en otro .pkl.
"""
def save_index(index, metadata, ia_name):
    index_path, meta_path = get_index_paths(ia_name)
    faiss.write_index(index, index_path)
    with open(meta_path, "wb") as f:
        pickle.dump(metadata, f)

"""
Agrega memoria
- Convierte el texto en un mbedding usando el modelo
- Agrega el mbedding al índice FAISS y el texto a los metadatos
- Guarda los cambios en los archivos correspondientes
"""
def add_memory(ia_name, text):
     index, metadata = load_or_create_index(ia_name)
     embedding = model.encode([text])
     index.add(np.array(embedding).astype('float32'))
     metadata.append(text)
     save_index(index, metadata, ia_name)

"""
Buscar memorias
- Convierte la consulta en un mbedding usando el modelo
- Busca los k embeddings más cercanos al indice FAISS (devuelve índices I y distancias D)
- Rotorna los textos correspondientes a los metadatos de esos índices
"""
def search_memory(ia_name, query, k=3):
    index, metadata = load_or_create_index(ia_name)
    embedding = model.encode([query])
    D, I = index.search(np.array(embedding).astype('float32'), k)
    results = [metadata[i] for i in I[0] if i < len(metadata)]
    return results