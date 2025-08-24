from langchain.prompts import PromptTemplate
from langchain.chains import ConversationalRetrievalChain
from langchain_groq import ChatGroq
from rag.config import GROQ_API_KEY

classifier_prompt = PromptTemplate(
    input_variables=["query"],
    template="""You are a classifier. Decide if the following user query is:
    - "medical" (talking about symptoms, illness, treatments, or health issues)
    - "smalltalk" (greetings, emotions, casual talk, non-medical).
    User query: {query}
    Answer only with: medical OR smalltalk
    """
)

medical_prompt = PromptTemplate(
    input_variables=["context", "question", "chat_history"],
    template="""
    You are HealthBridge AI, a friendly medical assistant who talks like a supportive therapist.

    The user will describe their symptoms in conversation.
    Your goals:
    1. Understand their symptoms empathetically.
    2. Use the retrieved medical context to identify possible diseases.
    3. Provide recommended treatments clearly.
    4. Continue the conversation naturally, asking follow-up questions if needed.

    Never list symptoms as treatments. If unsure, ask clarifying questions or suggest visiting a doctor.

    Conversation so far: {chat_history}

    Context: {context}

    User: {question}
    AI:"""
)

def init_llm():
    return ChatGroq(temperature=0.3, groq_api_key=GROQ_API_KEY, model_name="llama-3.1-8b-instant")

def init_rag_chain(llm, retriever):
    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        return_source_documents=True,
        combine_docs_chain_kwargs={"prompt": medical_prompt},
    )
