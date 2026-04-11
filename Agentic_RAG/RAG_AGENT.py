import datasets
from langchain_core.documents import Document

guest_dataset=datasets.load_dataset("agents-course/unit3-invitees", split="train")
#convert into document objects
docs=[
  Document(
    page_content="\n".join([
      f"Name: {guest['name']}",
            f"Relation: {guest['relation']}",
            f"Description: {guest['description']}",
            f"Email: {guest['email']}"
        ]),
   meadata={"name":guest["name"]} 
  )
  for guest in guest_dataset
]

#create retrieval tool
from langchain_community.retrievers import BM25Retriever
from langchain_core.tools import tool

bm25_retriever=BM25Retriever.from_documents(docs)

def extract_text(query:str)->str:
  results=bm25_retriever.invoke(query)
 if results:
   return "\n\n".join([doc.page_content for doc in results[:3]])
 else:
   return "no matching"

guest_info_tool=Tool(
  name="guest_info_retriever",
  func=extract_text,
  description="Retrieves detailed information about gala guests based on their name or relation."
)
