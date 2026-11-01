from utils.pdf_reader import extract_text_from_pdf
from utils.ocr import extract_text_from_image
import os
from utils.pdf_reader import extract_text_from_pdf
from utils.text_cleaner import clean_text
from utils.chunking import create_chunks
from utils.embeddings import EmbeddingModel
from utils.vector_store import VectorStore
from utils.retriever import MedicalRetriever
from utils.llm import MedicalLLM
from rag.rag_pipeline import MedicalRAGPipeline
from session.session_manager import SessionManager
from dotenv import load_dotenv

load_dotenv()


from utils.prompts import (
    SYSTEM_PROMPT,
    build_prompt
)

from utils.ocr import (
    extract_text_from_image,
    extract_text_from_scanned_pdf
)

from flask import (
    Flask,
    render_template,
    request,
    jsonify
)

from werkzeug.utils import secure_filename

from config import (
    UPLOAD_FOLDER,
    ALLOWED_EXTENSIONS,
    MAX_CONTENT_LENGTH
)

embedding_model = EmbeddingModel()
vector_store = VectorStore()
medical_llm = MedicalLLM()
session_manager = SessionManager()

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):

    if "." not in filename:
        return False

    extension = filename.rsplit(".", 1)[1].lower()

    return extension in ALLOWED_EXTENSIONS


@app.route("/")
def home():

    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():

    if "report" not in request.files:

        return jsonify({

            "success": False,
            "message": "No File Found"

        }), 400

    file = request.files["report"]

    if file.filename == "":

        return jsonify({

            "success": False,
            "message": "No File Selected"

        }), 400

    if not allowed_file(file.filename):

        return jsonify({

            "success": False,
            "message": "Only PDF/JPG/PNG Allowed"

        }), 400


    filename = secure_filename(file.filename)

    save_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    file.save(save_path)

    text = ""

    extension = filename.rsplit(".", 1)[1].lower()

    if extension == "pdf":

        text = extract_text_from_pdf(save_path)

        if text.strip() == "":
            text = extract_text_from_scanned_pdf(save_path)

    elif extension in ["jpg", "jpeg", "png"]:

        text = extract_text_from_image(save_path)

        print("TEXT LENGTH :", len(text))
        print(text[:300])

    session_id = request.form.get("session_id")

    print("SESSION ID FROM UPLOAD :", session_id)

    pipeline = session_manager.get_pipeline(session_id)

    print("UPLOAD PIPELINE :", id(pipeline))


    pipeline.build_vector_database(text)

    return jsonify({
        "success": True,
        "session_id": session_id,
        "filename": filename,
        "message": "Upload Successful",
        "text": text
    })


@app.route("/summary")
def summary():

    session_id = request.args.get("session_id")
    print("SESSION ID FROM SUMMARY :", session_id)

    pipeline = session_manager.get_pipeline(session_id)
    print("SUMMARY PIPELINE :", id(pipeline))

    summary = pipeline.summarize()

    return jsonify({
        "summary": summary
    })

@app.route("/insights")
def insights():

    session_id = request.args.get("session_id")

    pipeline = session_manager.get_pipeline(session_id)

    result = pipeline.generate_insights()

    return jsonify({
        "insights": result
    })

@app.route("/chat", methods=["POST"])

def chat():

    data = request.json

    question = data.get("question")

    session_id = request.json.get("session_id")

    pipeline = session_manager.get_pipeline(session_id)

    result = pipeline.chat(question)

    return jsonify(result)

@app.route("/clear")
def clear_chat():

    session_id = request.args.get("session_id")

    pipeline = session_manager.get_pipeline(session_id)

    pipeline.memory.clear()

    return jsonify({
        "message":"Chat cleared."
    })

@app.route("/session")

def create_session():

    session_id = (

        session_manager.create_session()

    )

    return jsonify({

        "session_id":session_id

    })

# Delete Session

@app.route("/delete_session")

def delete_session():

    session_id = request.args.get(

        "session_id"

    )

    session_manager.delete_session(

        session_id

    )

    return jsonify({

        "message":"Deleted"

    })


if __name__ == "__main__":

    app.run(debug=True)