from flask import Flask
from config import Config
from extensions import db, migrate
from models import Users, ChatHistory

# Import rag and init pipeline objects before routes using them
from rag.data_loader import load_documents
from rag.text_chunker import chunk_documents
from rag.vector_db import get_embeddings, build_vector_db
from rag.prompts import init_llm, init_rag_chain

documents = load_documents()
docs = chunk_documents(documents)
embeddings = get_embeddings()
vector_db = build_vector_db(docs, embeddings)
retriever = vector_db.as_retriever(search_type="mmr", search_kwargs={"k": 4})
llm = init_llm()
rag_chain = init_rag_chain(llm, retriever)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)

    # register Blueprints
    from routes.auth_routes import auth_bp
    from routes.chat_routes import chat_bp
    from routes.user_routes import user_bp
    from routes.doctor_routes import doctor_bp
    from routes.settings_routes import settings_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(doctor_bp)
    app.register_blueprint(settings_bp)

    # Attach shared objects for use in Blueprints
    app.llm = llm
    app.rag_chain = rag_chain

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
