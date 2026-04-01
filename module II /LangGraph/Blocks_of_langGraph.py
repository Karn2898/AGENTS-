#1.State :  It represents all the information that flows through your application.
from typing_extentions import TypeDict

class State(TypeDict):
  graph_state:str
#state is user defined

#2. Nodes: takes state as input , performs some operation , returns updates to the state

def node_1(state):
  return{"graph_state": state['graph_state]+ "I am" }


def node_2(state):
    return{"graph_state": state['grpah_state']+ "happy!"}

def node_3(state):
   return {"graph_state": state['graph_state]+ "sad !}

"""
nodes can contain ,
LLM calls: Generate text or make decisions
Tool calls: Interact with external systems
Conditional logic: Determine next steps
Human intervention: Get input from user"""


#3. Edges: connects nodes and define the possible paths through your graph

import random
from typing import Literal

def decide_mood(state)-> Literal ["node_2","node_3"]

    user_input=state['graph_state']




    if random.random() <0.5:

         return "node_2"

    return "node_3"
""" Edges can be:

Direct: Always go from node A to node B
Conditional: Choose the next node based on the current state"""


#4. StateGraph: The container that holds your entire agent workflow

from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END
#build graph
builder =StateGrpah(state)
builder.add_note("node_1", node_1)
builder.add_note("node_2", node_2)
builder.add_note("node_3", node_3)

#logic

builder.add_edge(START ,"node_1")
builder.add_conditional_edges("node_1",decide_mood)
builder.add_edge("node_2",END)
builder.add_edge("node_3",END)

graph=builder.compile()

#view
display(Imagr(grpah.get_grpah().draw_mermaid_png()))
graph.invoke({"graph_state" : "Hi, this is Lance."})

