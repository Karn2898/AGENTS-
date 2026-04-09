#%pip install langgraph langchain_openai langchain_core


import base64
from typing import List, TypedDict, Annotated, Optional
from langchain_openai import ChatOpenAI
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage
from langgraph.graph.message import add_messages
from langgraph.graph import START, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from IPython.display import Image, display

class AgentState(TypeDict):
  input_file: Optional[str]
  messages:Annonated[list[AnyMessage], add_messages]

#preparing tools
vision_llms=ChatOpenAI(model="gpt-4o")

def extract_text(img_path: str)->str:
      """
    Extract text from an image file using a multimodal model.
    
    Master Wayne often leaves notes with his training regimen or meal plans.
    This allows me to properly analyze the contents.
    """

  all_text=""
try:
  with open(img_path,"rb")as image_file:
    image_bytes=image_file.read()
image_base64=base64.b64encode(image_bytes).decode("utf-8")

message=[
  HumanMessage(
    content=[
      { "type": "text",
                        "text": (
                            "Extract all the text from this image. "
                            "Return only the extracted text, no explanations."
                        ),
                    },
      {"type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{image_base64}"
                        },
                    },
                ]
            )
        ]

response=vision_llm.invoke(message)
all_text+=response.content + "\n\n"

return all_text.strip()

except Exception as e :
error_msg = f "Error extracting text : {str(e)}"
print(error_msg)
return ""

def divide(a: int , b: int)-> float:
   """Divide a and b - for Master Wayne's occasional calculations."""
    return a / b
#equip buttler with tools

tools=[
  divide,
  extract_text
]

llm=ChatOpenAI(model="gpt-4o")
llm_with_tools = llm.bind_tools(tools, parallel_tool_calls=False)
