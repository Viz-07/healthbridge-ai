import os
import pandas as pd
from dotenv import load_dotenv
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Qdrant, Chroma
from langchain_groq import ChatGroq
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
import time

# 1. Load environment
load_dotenv()
GROQ_API_KEY = os.environ["GROQ_API_KEY"]

# configuration
DATA_PATH = "data"
CHROMA_PATH = "chroma_db"
CSV_FILE = "Diseases_Symptoms.csv"

# --- Qdrant configs (placeholder values, uncomment for deployment) ---
QDRANT_URL = None
QDRANT_API_KEY = None
# QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
# QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", None) or None

# 2. Load CSV manually (combine Symptoms + Treatments into one text field)
start = time.time()
file_path = os.path.join(DATA_PATH, CSV_FILE)
df = pd.read_csv(file_path)
print(f"[Timing] CSV loaded in {time.time() - start:.2f} seconds")

start = time.time()
documents = []
for _, row in df.iterrows():
    text = f"Symptoms: {row['Symptoms']}\nTreatments: {row['Treatments']}"
    metadata = {"disease": row["Name"]}
    documents.append(Document(page_content=text, metadata=metadata))
print(f"[Timing] Documents created in {time.time() - start:.2f} seconds")

# 3. Chunking
start = time.time()
splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=40)
docs = splitter.split_documents(documents)
print(f"[Timing] Chunking done in {time.time() - start:.2f} seconds")

# 4. Embeddings model
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# 5. Store in vector DB (Chroma for prototyping, Qdrant for deployment)
VECTOR_DB = "chroma"
start = time.time()
if VECTOR_DB == "chroma":
    vector_db = Chroma.from_documents(
        docs,
        embeddings,
        persist_directory=CHROMA_PATH
    )
elif VECTOR_DB == "qdrant":
    vector_db = Qdrant.from_documents(
        docs,
        embeddings,
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
        collection_name="healthbridge-docs",
    )
else:
    raise Exception("Unknown vector db backend")
print(f"[Timing] Vector DB built in {time.time() - start:.2f} seconds")

# 6. Retrieval
start = time.time()
retriever = vector_db.as_retriever(search_type="mmr", search_kwargs={"k": 4})
print(f"[Timing] Retriever initialized in {time.time() - start:.2f} seconds")

# 7. LLM setup
llm = ChatGroq(
    temperature=0.3,
    groq_api_key=GROQ_API_KEY,
    model_name="llama-3.1-8b-instant"
)

# --- Stage 1: Classifier prompt ---
classifier_prompt = PromptTemplate(
    input_variables=["query"],
    template="""
You are a classifier. Decide if the following user query is:
- "medical" (talking about symptoms, illness, treatments, or health issues)
- "smalltalk" (greetings, emotions, casual talk, non-medical).

User query: {query}
Answer only with: medical OR smalltalk
"""
)

def detect_closure(user_query: str):
    explicit_endings = ["exit", "end conversation", "quit", "goodbye"]
    soft_endings = ["thanks", "i feel better", "that’s enough", "i got it", "no worries", "appreciate it"]

    q_lower = user_query.lower()

    if any(phrase in q_lower for phrase in explicit_endings):
        return "explicit"
    elif any(phrase in q_lower for phrase in soft_endings):
        return "soft"
    return None

# --- Stage 2: Conversational medical assistant prompt ---
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

rag_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    return_source_documents=True,
    combine_docs_chain_kwargs={"prompt": medical_prompt},
)

# --- Chat state ---
chat_history = []

# 8. Chatbot interaction with 2-stage flow
def chat_with_bot(user_query):
    global chat_history
    if len(user_query.strip()) < 1:
        print("⚠️ Please enter something.")
        return

    # Step 1: Check if user wants to end conversation
    closure_type = detect_closure(user_query)
    if closure_type == "explicit":
        print("\nHealthBridge AI: I'm really glad we could talk today. Remember, I'm always here if you want to chat again. Take care of yourself ❤️\n")
        return "end"
    elif closure_type == "soft":
        print("\nHealthBridge AI: I'm so glad I could help 💙 Do you want to wrap up here, or would you like to keep talking?\n")
        return

    # Step 2: Classify query (smalltalk vs medical)
    classification = llm.invoke(classifier_prompt.format(query=user_query)).content.strip().lower()

    if "smalltalk" in classification:
        # casual smalltalk
        response = llm.invoke(
            f"You are a warm, empathetic companion. Respond naturally to this message: {user_query}"
        )
        answer = response.content
        print("\nHealthBridge AI (casual):", answer)
    else:
        # medical query → use RAG
        start = time.time()
        response = rag_chain.invoke({"question": user_query, "chat_history": chat_history})
        chat_history.append((user_query, response["answer"]))
        print(f"\n\n[Timing] Query answered in {time.time() - start:.2f} seconds \n\n")
        print("HealthBridge AI:", response["answer"])
        print("\nSources:")
        for doc in response["source_documents"]:
            print(" -", doc.metadata.get("disease", "Unknown"))


# Example usage
if __name__ == "__main__":
    print("Type 'exit' to quit.")
    while True:
        q = input("You: ")
        if q.lower() == "exit":
            break
        result = chat_with_bot(q)
        if result == "end":  # user ended naturally
            break

