import os
import pandas as pd
from langchain.schema import Document
from rag.config import DATA_PATH, CSV_FILE

# Load CSV manually (combine Symptoms + Treatments into one text field)
def load_documents():
    file_path = os.path.join(DATA_PATH, CSV_FILE)
    df = pd.read_csv(file_path)
    
    documents = []
    for _, row in df.iterrows():
        text = f"Symptoms: {row['Symptoms']}\nTreatments: {row['Treatments']}"
        metadata = {"disease": row["Name"]}
        documents.append(Document(page_content=text, metadata=metadata))
    return documents
