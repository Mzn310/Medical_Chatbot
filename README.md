# 🩺 Medical Chatbot — RAG with LangChain, Pinecone & Groq

A conversational AI chatbot that answers medical questions using **Retrieval-Augmented Generation (RAG)**. It embeds a medical knowledge base into a Pinecone vector store and uses a Groq-hosted LLM (Llama 3.3 70B) to generate grounded, context-aware answers.

## Features

- **RAG pipeline** built with LangChain — retrieves relevant context before generating an answer, reducing hallucinations
- **Vector search** powered by [Pinecone](https://www.pinecone.io/) serverless index
- **Fast inference** via [Groq](https://groq.com/) running Llama 3.3 70B Versatile
- **HuggingFace sentence-transformer embeddings** for semantic search
- **Flask web UI** with a simple chat interface
- **Dockerized** for easy deployment
- **CI/CD ready** — GitHub Actions + AWS (EC2/ECR) deployment workflow included

## Architecture

```
PDF documents (data/)
        │
        ▼
  Text splitting & chunking
        │
        ▼
  HuggingFace embeddings ──► Pinecone index (medical-chatbot)
                                     │
User question ──► Flask app ──► Retriever (top-k similarity search)
                                     │
                                     ▼
                        Groq LLM (Llama 3.3 70B) + retrieved context
                                     │
                                     ▼
                              Answer returned to user
```

## Project Structure

```
.
├── app.py                 # Flask app — serves the chatbot UI and handles chat requests
├── store_index.py         # One-off script to embed PDFs and populate the Pinecone index
├── src/
│   ├── helper.py           # PDF loading, chunking, embeddings download
│   └── prompt.py           # System prompt template for the LLM
├── templates/
│   └── index.html          # Chat UI
├── data/                   # Source PDF documents (not tracked in git)
├── requirements.txt
├── setup.py
├── Dockerfile
└── .github/workflows/      # CI/CD pipeline (GitHub Actions → AWS)
```

## Prerequisites

- Python 3.10+
- A [Pinecone](https://www.pinecone.io/) account and API key
- A [Groq](https://console.groq.com/) account and API key

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
```

### 2. Create a virtual environment and install dependencies

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### . Set up environment variables

Create a `.env` file in the project root:

```env
PINECONE_API_KEY=your_pinecone_api_key
GROQ_API_KEY=your_groq_api_key
```

> Never commit your `.env` file. It's already excluded via `.gitignore`.

### 4. Add your source documents

Place your medical reference PDFs inside a `data/` folder at the project root.

### 5. Build the vector index

This chunks your PDFs, generates embeddings, and upserts them into Pinecone:

```bash
python store_index.py
```

### 6. Run the app

```bash
python app.py
```

Visit **http://localhost:8080** in your browser to start chatting.

## Running with Docker

```bash
docker build -t medical-chatbot .
docker run -p 8080:8080 --env-file .env medical-chatbot
```

## Deployment (AWS EC2 + ECR via GitHub Actions)

This project includes a reference CI/CD setup for deploying to AWS:

1. **Create an IAM user** with programmatic access for deployment.
2. **Create an ECR repository** to store the Docker image.
3. **Launch an EC2 instance** (Ubuntu) and install Docker on it:
   ```bash
   sudo apt-get update -y
   sudo apt-get upgrade -y
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   sudo usermod -aG docker ubuntu
   newgrp docker
   ```
4. **Register the EC2 instance as a self-hosted GitHub Actions runner** (Settings → Actions → Runners → New self-hosted runner).
5. **Add the following GitHub repository secrets:**

   | Secret                  | Description         |
   | ----------------------- | ------------------- |
   | `AWS_ACCESS_KEY_ID`     | IAM user access key |
   | `AWS_SECRET_ACCESS_KEY` | IAM user secret key |
   | `AWS_DEFAULT_REGION`    | e.g. `us-east-1`    |
   | `ECR_REPO`              | ECR repository URI  |
   | `PINECONE_API_KEY`      | Pinecone API key    |
   | `GROQ_API_KEY`          | Groq API key        |

   Required IAM policies: `AmazonEC2ContainerRegistryFullAccess`, `AmazonEC2FullAccess`

On push, the workflow builds the Docker image, pushes it to ECR, pulls it on the EC2 instance, and runs the container.

## Tech Stack

| Component         | Tool                                |
| ----------------- | ----------------------------------- |
| Web framework     | Flask                               |
| LLM orchestration | LangChain                           |
| LLM inference     | Groq (Llama 3.3 70B Versatile)      |
| Vector database   | Pinecone                            |
| Embeddings        | HuggingFace `sentence-transformers` |
| Deployment        | Docker, GitHub Actions, AWS EC2/ECR |

## Notes

- The Pinecone index is created with a fixed embedding dimension of `384` — this must match the sentence-transformer model used in `src/helper.py`.
- `test.py` is a scratch script used for verifying environment variables and is not part of the app's runtime.

## License

This project is open source and available under the [MIT License](LICENSE).

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to check the [issues page](../../issues).

---

**Disclaimer:** This chatbot is intended for educational and informational purposes only. It is **not** a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider.
