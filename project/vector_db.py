from chromadb import Client, Collection
from sentence_transformers import SentenceTransformer
import pickle

model = SentenceTransformer("intfloat/multilingual-e5-large-instruct")


def create_vector_db(texts, db_name="russian_text_db"):
    """
    Creates a vector database from a list of Russian texts.

    Args:
        texts (list): List of Russian texts to embed and store.
        db_name (str): Name of the vector database collection.

    Returns:
        Collection: A ChromaDB collection containing embedded texts.
    """
    # Initialize ChromaDB client
    client = Client()

    # Load pre-trained model for Russian embeddings


    # Create a collection in ChromaDB
    collection = client.get_or_create_collection(db_name)

    # Generate embeddings for each text
    embeddings = model.encode(list(texts.keys()), convert_to_tensor=True, normalize_embeddings=True)

    # Add embeddings and texts to the collection
    for i, embedding in enumerate(embeddings):
        collection.add(ids=[str(i)], embeddings=[embedding.tolist()], documents=[texts[list(texts.keys())[i]]])

    print(f"Database '{db_name}' created with {len(texts)} entries.")
    return collection


def query_vector_db(query_text, collection, model, top_k=5):
    """
    Queries the vector database to find the top_k most similar texts to the given query.

    Args:
        query_text (str): The text to search for.
        collection (Collection): The ChromaDB collection to query.
        model (SentenceTransformer): The model to create embeddings.
        top_k (int): The number of top results to return.

    Returns:
        list of dict: A list of the top_k most similar documents with their similarity scores.
    """
    # Embed the query text
    query_embedding = model.encode([query_text], convert_to_tensor=True, normalize_embeddings=True)[0]

    # Search for similar embeddings in the collection
    results = collection.query(query_embeddings=[query_embedding.tolist()], n_results=top_k)



    return results['documents']


def load_vector_db():
    # Example usage
    with open('project/dict_db_2.pkl', 'rb') as f:
        d = pickle.load(f)
    vector_db = create_vector_db(d)
    return vector_db


if __name__ == '__main__':
    v = load_vector_db()
    while True:
        # Example usage
        query_text = input("Query: ")
        results = query_vector_db(query_text, v, model)
        for i, result in enumerate(results):
            print(result)

