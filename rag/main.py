from rag.data_loader import load_documents
from rag.text_chunker import chunk_documents
from rag.vector_db import get_embeddings, build_vector_db
from rag.prompts import init_llm, init_rag_chain, classifier_prompt
from rag.utils import detect_closure

def get_rag_answer(user_query, chat_history, llm, rag_chain):
    """
    Process the user query, return a dict with answer, classification, closure type, and sources.
    """
    if len(user_query.strip()) < 2:
        return {"error": "Please enter something."}
    
    # Step 1: Check if user wants to end conversation
    closure_type = detect_closure(user_query)
    if closure_type == "explicit":
        return {"answer": "I'm really glad we could talk today. Take care of yourself ❤️", "closure": "explicit"}
    elif closure_type == "soft":
        return {"answer": "I'm so glad I could help 💙 Do you want to wrap up here, or would you like to keep talking?", "closure": "soft"}
    
    # Step 2: Classify query (smalltalk vs medical)
    classification = llm.invoke(classifier_prompt.format(query=user_query)).content.strip().lower()
    
    if "smalltalk" in classification:
        response = llm.invoke(f"You are a warm, empathetic companion. Respond naturally to this message: {user_query}")
        chat_history.append((user_query, response.content))  # append the message-response pair!
        return {"answer": response.content, "classification": "smalltalk"}
    else:
        response = rag_chain.invoke({"question": user_query, "chat_history": chat_history})
        chat_history.append((user_query, response["answer"]))
        sources = [doc.metadata.get("disease", "Unknown") for doc in response.get("source_documents",[])]
        return {
            "answer": response["answer"],
            "classification": "medical",
            "sources": sources,
            "closure": None
        }
