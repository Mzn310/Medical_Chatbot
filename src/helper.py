from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.embeddings import Embeddings
from huggingface_hub import InferenceClient
from langchain_core.documents import Document
from typing import List
import os


# Extract Data From the PDF File
def load_pdf_file(data):
    loader = DirectoryLoader(
        data,
        glob="*.pdf",
        loader_cls=PyPDFLoader
    )

    documents = loader.load()

    return documents

class HFRouterEmbeddings(Embeddings):
    def __init__(self, model_name: str, api_key: str):
        self.client = InferenceClient(model=model_name, token=api_key)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [self.client.feature_extraction(text).tolist() for text in texts]

    def embed_query(self, text: str) -> List[float]:
        return self.client.feature_extraction(text).tolist()


def filter_to_minimal_docs(docs: List[Document]) -> List[Document]:
    """
    Given a list of Document objects, return a new list of Document objects
    containing only 'source' in metadata and the original page_content.
    """

    minimal_docs = []

    for doc in docs:
        src = doc.metadata.get("source")

        minimal_docs.append(
            Document(
                page_content=doc.page_content,
                metadata={"source": src}
            )
        )

    return minimal_docs



# Split the Data into Text Chunks
def text_split(extracted_data):

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=20
    )

    text_chunks = text_splitter.split_documents(extracted_data)

    return text_chunks



# Download the Embeddings from HuggingFace
def download_hugging_face_embeddings():

    embeddings = HFRouterEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        api_key=os.environ.get("HF_TOKEN")
    )

    return embeddings