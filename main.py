import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from langchain_openai import ChatOpenAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import CharacterTextSplitter


load_dotenv()


if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY not found in .env file")
if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("GOOGLE_API_KEY not found in .env file")


loader = TextLoader("knowledge.txt")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
docs = text_splitter.split_documents(documents)

print(f"Document split into {len(docs)} chunks.")

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

vectorstore = FAISS.from_documents(docs, embeddings)
print("Vector store created successfully using Google's embeddings.")

retriever = vectorstore.as_retriever()

template = """
You are an expert on AI Fitness Coach that combines workout planning, nutrition guidance, and progress tracking with RAG-based knowledge retrieval through a simple chat interface.

.
Answer the following question based ONLY on the provided context.
If the answer is not in the context, say "I don't have that information".

CONTEXT:
{context}

QUESTION:
{question}
"""
prompt = ChatPromptTemplate.from_template(template)

llm = ChatOpenAI(model="gpt-4.1-nano")

rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()

)
question = input("Enter your question: ")
print("\n--- Streaming RAG Response ---")
for chunk in rag_chain.stream(question):
    print(chunk, end="", flush=True)
print("\n" + "-" * 30)