# # # vector_db/db_manager.py
# # import pinecone
# # import numpy as np

# # # Initialize Pinecone environment and index
# # def init_db(api_key, index_name, dimension=512, environment='us-west1-gcp'):
# #     pinecone.init(api_key=api_key, environment=environment)
# #     # Check if the index exists, if not, create it
# #     if index_name not in pinecone.list_indexes():
# #         pinecone.create_index(index_name, dimension=dimension)
# #     return pinecone.Index(index_name)

# # # Function to convert text to a vector (this is a placeholder)
# # def text_to_vector(text):
# #     # Ideally, you'll replace this with an actual model's embedding process
# #     # Example: using a pretrained model from Hugging Face's Sentence Transformers
# #     return np.random.rand(512)  # Example: random vector, replace with actual model output

# # # Insert or update an item in the database
# # def upsert_vector(index, item_id, text):
# #     vector = text_to_vector(text)
# #     index.upsert(vectors={item_id: vector})

# # # Query the database to find similar items
# # def query_vectors(index, query_text, top_k=5):
# #     query_vector = text_to_vector(query_text)
# #     return index.query(query_vector, top_k=top_k)

# # # Optional: Delete an item in the database
# # def delete_vector(index, item_id):
# #     index.delete(item_ids=[item_id])

# # # Optional: Clear the index
# # def clear_index(index):
# #     index.delete_all()









# # vector_db/db_manager.py






# # import pinecone
# # import numpy as np

# # def init_db():
# #     pinecone.init(api_key='your_api_key')
# #     index = pinecone.Index('vector_db')
# #     return index

# # def upsert_vector(index, id, vector):
# #     index.upsert({id: vector})

# # def query_vectors(index, vector):
# #     return index.query(vector, top_k=5)


# import os
# from pinecone import Pinecone, ServerlessSpec
# def init_db(api_key='your_api_key', index_name='my_index', dimension=512):
#     # Initialize Pinecone client with your API key
#     pc = Pinecone(api_key=api_key)

#     # Check if the index exists, create if not
#     if index_name not in pc.list_indexes().names():
#         pc.create_index(
#             name=index_name,
#             dimension=dimension,
#             metric='euclidean',
#             spec=ServerlessSpec(
#                 cloud='aws',
#                 region='us-west-2'
#             )
#         )
#     return pc.index(name=index_name)





# # Import necessary libraries
# import sqlite3
# from random import randint  # Example for generating mock vectors

# # Define a class to simulate a simple in-memory 'database'
# class LocalDB:
#     def __init__(self):
#         self.data = {}  # Simple dict to store data indexed by ID

#     def upsert(self, id, vector):
#         self.data[id] = vector

#     def query(self, query_vector, top_k=5):
#         # Simplified query: Return items sorted by simple criterion (e.g., vector length)
#         return sorted(self.data.items(), key=lambda x: -len(x[1]))[:top_k]

# # Create an instance of LocalDB
# db = LocalDB()

# # Function to insert or update vectors in the LocalDB or SQLite
# def upsert_vector(id, vector):
#     db.upsert(id, vector)  # Using LocalDB for demonstration

# # Function to query vectors in the LocalDB or SQLite
# def query_vectors(query_vector, top_k=5):
#     return db.query(query_vector, top_k)

# # SQLite setup for a more robust local testing environment
# conn = sqlite3.connect('local_vectors.db')  # Local SQLite DB file

# def setup_database():
#     with conn:
#         conn.execute('''
#             CREATE TABLE IF NOT EXISTS vectors
#             (id TEXT PRIMARY KEY, vector TEXT)
#         ''')

# def text_to_vector(text):
#     # Convert text to a simplistic numerical vector based on word lengths
#     return [len(word) for word in text.split()]

# # Integrate SQLite functions with upsert and query functions if required
# def sqlite_upsert_vector(id, vector):
#     with conn:
#         conn.execute('REPLACE INTO vectors (id, vector) VALUES (?, ?)', (id, str(vector)))

# def sqlite_query_vectors(query_vector, top_k=5):
#     cursor = conn.cursor()
#     cursor.execute('SELECT * FROM vectors ORDER BY RANDOM() LIMIT ?', (top_k,))  # Random selection for example
#     return cursor.fetchall()

# # Ensure the SQLite database is set up
# setup_database()
##########################################################


# # Import necessary libraries
# import sqlite3
# from random import randint  # Example for generating mock vectors

# # Define a class to simulate a simple in-memory 'database'
# class LocalDB:
#     def __init__(self):
#         self.data = {}  # Simple dict to store data indexed by ID

#     def upsert(self, id, content):
#         self.data[id] = content

#     def query(self, query_text, top_k=5):
#         # Simplified query: Return items sorted by simple criterion (e.g., content similarity)
#         # This is placeholder logic; you might need a more complex comparison based on the actual text
#         return sorted(self.data.items(), key=lambda x: x[1].count(query_text), reverse=True)[:top_k]

# # Create an instance of LocalDB
# db = LocalDB()

# # SQLite setup for a more robust local testing environment
# conn = sqlite3.connect('local_vectors.db')

# def setup_database():
#     with conn:
#         # Modify the table to include a 'text' column
#         conn.execute('''
#             CREATE TABLE IF NOT EXISTS vectors
#             (id TEXT PRIMARY KEY, vector TEXT, text TEXT)
#         ''')
#         conn.commit()

# def insert_data(id, vector, text):
#     with conn:
#         # Insert or replace the data including text
#         conn.execute('REPLACE INTO vectors (id, vector, text) VALUES (?, ?, ?)', (id, str(vector), text))
#         conn.commit()

# def query_text_data(query_text, top_k=5):
#     cursor = conn.cursor()
#     # Modify the query to fetch based on text content
#     cursor.execute('SELECT text FROM vectors WHERE text LIKE ? ORDER BY RANDOM() LIMIT ?', ('%' + query_text + '%', top_k))
#     results = cursor.fetchall()
#     return [result[0] for result in results]  # Return a list of texts

# # Ensure the SQLite database is set up
# setup_database()




# # vector_db/db_manager.py
# import sqlite3
# import json
# import re
# from collections import Counter

# conn = sqlite3.connect('vectors.db')

# def setup_database():
#     """Set up the SQLite database to store vectors and URLs."""
#     with conn:
#         conn.execute('''
#             CREATE TABLE IF NOT EXISTS vectors
#             (url TEXT PRIMARY KEY, vector TEXT)
#         ''')
#         conn.commit()

# def text_to_vector(text):
#     """Convert text to a simple vector representation."""
#     words = re.findall(r'\w+', text.lower())
#     return Counter(words)

# def insert_vector(url, vector):
#     """Insert or update the vector in the database."""
#     with conn:
#         vector_serialized = json.dumps(dict(vector))  # Serialize the Counter object to a string using JSON
#         conn.execute('REPLACE INTO vectors (url, vector) VALUES (?, ?)', (url, vector_serialized))
#         conn.commit()

# setup_database()
# ################################### good


import sqlite3
import json
import re
from collections import Counter

conn = sqlite3.connect('vectors.db')

def setup_database():
    """Set up the SQLite database with full-text search capabilities."""
    with conn:
        conn.execute('''
            CREATE VIRTUAL TABLE IF NOT EXISTS vector_fts USING fts5(url, vector);
        ''')
        conn.commit()

def text_to_vector(text):
    """Convert text to a simple vector representation based on word frequency."""
    words = re.findall(r'\w+', text.lower())
    return Counter(words)

def insert_vector(url, vector):
    """Insert or update the vector in the FTS table."""
    with conn:
        vector_serialized = json.dumps(dict(vector))  # Serialize the Counter object to a string using JSON
        conn.execute('REPLACE INTO vector_fts (url, vector) VALUES (?, ?)', (url, vector_serialized))
        conn.commit()


setup_database()
