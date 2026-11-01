class MedicalRetriever:

    def __init__(self, vector_db):

        if vector_db is None:
            raise Exception(
                "Vector Database Not Found"
            )

        self.vector_db = vector_db

    def retrieve(self, question, k=3):

        documents = self.vector_db.similarity_search(
            query=question,
            k=k
        )

        return documents

    def retrieve_with_score(self, question, k=3):

        results = self.vector_db.similarity_search_with_score(
            query=question,
            k=k
        )

        return results