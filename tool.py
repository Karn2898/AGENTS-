from smolagents import CodeAgent,DuckDuckGoSearchTool, HfApiModel,load_tool,tool
import datetime
import requests
import pytz
import yaml
from tools.final_answer import FinalAnswerTool
import base64
import random
from Gradio_UI import GradioUI

# Below is an example of a tool that does nothing. Amaze us with your creativity !
@tool
def my_custom_tool(arg1:str, arg2:int)-> str: 
    
    """A text transformer tool that transforms iput text in various ways."""
    
    
    Args:
        arg1: The text to transform 
        arg2: The transform mode -one of : 'reverse','encode','scramble'

    text=arg1model=arg2.strip().lower()

    if mode == "reverse":
        return text[::-1]

    elif mode == "encode":
        encoded= base64.b64encode(text.encode()).decode()
        return f"base64: {encoded}  "      
  
    elif mode == "scramble":
        eords=text.split()
        scrambled=[]
        for words in words :
            if len(word) <= 2:
                scrambled.append(word)
            else:
                middle=list(word[1:-1])
                random.shuffle(middle)
                scrambled.append(word[0]+ "".join(middle) +word[-1])
            return "".join(scrambled)
        else:
            return f"unknow mode '{mode}'. choose from : reverse , encode ,scramble"
@tool
def get_current_time_in_timezone(timezone: str) -> str:
      """A tool that fetches the current local time in a specified timezone.
"""
    
    Args:
        timezone: A string representing a valid timezone (e.g., 'America/New_York').
    
    try:

        tz = pytz.timezone(timezone)
        
        local_time = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        return f"The current local time in {timezone} is: {local_time}"
    except Exception as e:
        return f"Error fetching time for timezone '{timezone}': {str(e)}"


final_answer = FinalAnswerTool()

# If the agent does not answer, the model is overloaded, please use another model or the following Hugging Face Endpoint that also contains qwen2.5 coder:
# model_id='https://pflgm2locj2t89co.us-east-1.aws.endpoints.huggingface.cloud' 

model = HfApiModel(
max_tokens=2096,
temperature=0.5,
model_id='Qwen/Qwen2.5-Coder-32B-Instruct',# it is possible that this model may be overloaded
custom_role_conversions=None,
)


# Import tool from Hub
image_generation_tool = load_tool("agents-course/text-to-image", trust_remote_code=True)

with open("prompts.yaml", 'r') as stream:
    prompt_templates = yaml.safe_load(stream)
    
agent = CodeAgent(
    model=model,
    tools=[final_answer], ## add your tools here (don't remove final answer)
    max_steps=6,
    verbosity_level=1,
    grammar=None,
    planning_interval=None,
    name=None,
    description=None,
    prompt_templates=prompt_templates
)


GradioUI(agent).launch()
