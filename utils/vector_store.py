from langchain_community.vectorstores import FAISS

from langchain_core.documents import Document

from langchain_community.embeddings import HuggingFaceEmbeddings


class VectorStore:

    def __init__(self):

        self.embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        self.db = None

    def create_vector_store(self, chunks):

        documents = []

        for i, chunk in enumerate(chunks):

            documents.append(

                Document(

                    page_content=chunk,

                    metadata={

                        "chunk_id": i

                    }

                )

            )

        self.db = FAISS.from_documents(

            documents,

            self.embedding_model

        )
        print("Chunks :", len(chunks))

        print("Documents :", len(documents))

        return self.db