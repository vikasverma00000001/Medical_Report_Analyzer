from utils.chunking import create_chunks
from utils.vector_store import VectorStore
from utils.retriever import MedicalRetriever
from utils.prompts import build_prompt
from utils.llm import MedicalLLM
from memory.chat_memory import ChatMemory


class MedicalRAGPipeline:

    def __init__(self):

        self.vector_store = VectorStore()

        self.llm = MedicalLLM()

        self.memory = ChatMemory()

        self.db = None

    def build_vector_database(self,text):

        chunks = create_chunks(text)

        self.db = self.vector_store.create_vector_store(chunks)

        print("=" * 60)
        print("SELF BUILD :", id(self))
        print("DB :", self.db)
        print("=" * 60)

        return len(chunks)


    def ask(self,question,history,top_k=3):

        retriever = MedicalRetriever(self.db)

        documents = retriever.retrieve(question,k=top_k)

        context = "\n\n".join(

            doc.page_content

            for doc in documents

        )

        prompt = build_prompt(context,history,question)

        answer = self.llm.generate_answer(prompt)

        return {

            "question": question,

            "context": context,

            "answer": answer

        }

    def summarize(self):
        print("=" * 50)
        print("SELF ID SUMMARY :", id(self))
        print("DB :", self.db)
        print("=" * 50)

        if self.db is None:
            raise Exception("DB is None inside summarize()")

        retriever = MedicalRetriever(self.db)

        documents = retriever.retrieve("Generate report summary",k=8)

        context = "\n\n".join(

            doc.page_content

            for doc in documents

        )

        summary = self.llm.generate_summary(context)

        return summary

    def generate_insights(self):
        retriever = MedicalRetriever(self.db)

        documents = retriever.retrieve("Generate medical insights",k=8)

        context = "\n\n".join(

            doc.page_content

            for doc in documents

        )

        insights = self.llm.generate_insights(context)

        return insights

    def chat(self, question):
        if self.db is None:
            return {

                "error": "Please upload a medical report first."

            }

        history = self.memory.get_history()

        result = self.ask(question, history)

        self.memory.add_user_message(question)

        self.memory.add_ai_message(result["answer"])

        return result