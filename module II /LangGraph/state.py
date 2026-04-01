import os
from typing import TypedDict, List, Dict, Any, Optional
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
#state 
class State(TypedDict):
    email:Dict[str ,Any]
    email_category: Optional[str]
    spam_reson:Optional[str]
    is_spam:Optional[bool]
    email_draft:Optional[str]
    messages:List[Dict[str, Any]]
    
#nodes

