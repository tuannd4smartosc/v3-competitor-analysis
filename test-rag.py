import os
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from dotenv import load_dotenv

load_dotenv()

from crews.promotion_campaigns import generate_promotion_campaign_user_query

# Load your .txt file
loader = TextLoader("context.txt", encoding='utf-8')
documents = loader.load()

# Split the text into manageable chunks
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
docs = text_splitter.split_documents(documents)

# Embed and index with FAISS
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(docs, embeddings)

# Create retriever
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# Use OpenAI's GPT-4 model
llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

# Create the Retrieval-QA chain
qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, return_source_documents=True)

# Ask your question
query = "List all Asics promotion campaigns"

result = qa({"query": query})

# Show the result
print("Answer:", result["result"])
print("\nSources:")
print("Top relevant chunks:\n")
for i, doc in enumerate(result["source_documents"], 1):
    print(f"--- Chunk {i} ---")
    print(doc.page_content.strip())
    print("\n--- End of Chunk ---\n")
