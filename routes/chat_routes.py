from flask import Blueprint, render_template, request, session, redirect, url_for, flash, current_app
from extensions import db
from models import Users, ChatHistory
from rag.main import get_rag_answer

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/chat', methods=["GET", "POST"])
def chat():
    if "user" not in session:
        flash("Please log in to access the chat feature!")
        return redirect(url_for("auth.login"))
    user = Users.query.filter_by(name=session["user"]).first()
    if not user:
        flash("User not found.")
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        user_message = request.form.get('message', '').strip()
        # Save user's message
        db.session.add(ChatHistory(user_id=user.id, sender='user', message=user_message))
        db.session.commit()

        # Build chat_history for RAG (from DB)
        history_objs = ChatHistory.query.filter_by(user_id=user.id).order_by(ChatHistory.timestamp).all()
        chat_history = [
            (history_objs[i].message, history_objs[i+1].message)
            for i in range(0, len(history_objs)-1, 2)
            if history_objs[i].sender == 'user' and history_objs[i+1].sender == 'bot'
        ]

        # Get LLM response
        llm = current_app.llm
        rag_chain = current_app.rag_chain
        result = get_rag_answer(user_message, chat_history, llm, rag_chain)
        bot_response = result.get("answer", "")
        sources = result.get("sources", [])
        
        # Save bot's reply
        db.session.add(ChatHistory(user_id=user.id, sender='bot', message=bot_response))
        db.session.commit()

    # Always fetch chat history for display
    history_objs = ChatHistory.query.filter_by(user_id=user.id).order_by(ChatHistory.timestamp).all()
    chat_history = [
        (history_objs[i].message, history_objs[i+1].message)
        for i in range(0, len(history_objs)-1, 2)
        if history_objs[i].sender == 'user' and history_objs[i+1].sender == 'bot'
    ]

    return render_template("chat.html", chat_history=chat_history)
