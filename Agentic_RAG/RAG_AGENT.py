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
