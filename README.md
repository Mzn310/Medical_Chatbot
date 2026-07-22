In Pinecone, an index is the main container where your vector embeddings are stored and searched. You can think of it as being similar to a database table, but instead of storing rows of text or numbers, it stores high-dimensional vectors.

What an index contains

A Pinecone index stores:

Vector embeddings (numerical representations of text, images, etc.)
Unique IDs for each vector
Metadata (optional information like source, page number, category)
The configuration needed to perform fast similarity searches
