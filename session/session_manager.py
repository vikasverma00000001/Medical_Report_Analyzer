import uuid

from rag.rag_pipeline import MedicalRAGPipeline


class SessionManager:

    def __init__(self):

        self.sessions = {}

    def create_session(self):

        session_id = str(uuid.uuid4())

        self.sessions[session_id] = (MedicalRAGPipeline())

        print("=" * 60)
        print("SESSION CREATED")
        print("Session ID :", session_id)
        print("Pipeline Object ID :", id(self.sessions[session_id]))
        print("=" * 60)

        return session_id

    def get_pipeline(self,session_id):
        pipeline = self.sessions.get(session_id)

        print("=" * 60)
        print("GET PIPELINE")
        print(session_id)
        print(id(pipeline))
        print("=" * 60)

        return pipeline

    def delete_session(self,session_id):

        if session_id in self.sessions:

            del self.sessions[session_id]