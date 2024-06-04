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
