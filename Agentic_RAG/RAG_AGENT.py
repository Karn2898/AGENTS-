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
#step 3: Integration
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage, HumanMessage, AIMessage
from langgraph.prebuilt import ToolNode
from langgraph.graph import START, StateGraph
from langgraph.prebuilt import tools_condition
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
llm=HuggingFaceEndpoint(
    repo_id="Qwen/Qwen2.5-Coder-32B-Instruct",
    huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN,
)

chat=ChatHuggingFace(llm=llm,verbose=True)
tools=[guest_info_tool]
chat_with_tools=chat.bind_tools(tools)

class AgentState(TypeDict):
  messages:Annonated[list[AnyMessage] , add_messages]

def assistant (state: AgentState):
  return {
    "messages":[chat_with_tools.invoke(state["messages"])],
  }
#graph
builder=StateGraph(AgentState)

builder.add_node("assistant",assistant)
builder.add_node("tools", ToolNode(tools))

# Define edges: these determine how the control flow moves
builder.add_edge(START, "assistant")
builder.add_conditional_edges(
    "assistant",
    # If the latest message requires a tool, route to tools
    # Otherwise, provide a direct response
    tools_condition,
)
builder.add_edge("tools", "assistant")
alfred = builder.compile()

messages=[HumanMessage(content="Tell me about our guest named 'Lady Ada Lovelace'.")]
print("Alfred's response :")
print(response['messages][-1].content)

