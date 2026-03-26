from smolagents import CodeAgent, DuckDuckGoSearchTool, HfApiModel, load_tool, tool as tooldef
import datetime
import requests
import pytz
import yaml
from tools.final_answer import FinalAnswerTool
import base64
import random
from Gradio_UI import GradioUI



@tooldef
def my_custom_tool(arg1: str, arg2: str) -> str:
    """A text transformer tool that transforms input text in various ways.

    Args:
        arg1: The text to transform.
        arg2: The transformation mode -- one of: 'reverse', 'encode', 'scramble'.
    """
    text = arg1
    mode = arg2.strip().lower()

    if mode == "reverse":
        return text[::-1]

    elif mode == "encode":
        encoded = base64.b64encode(text.encode()).decode()
        return f"Base64: {encoded}"

    elif mode == "scramble":
        words = text.split()
        scrambled = []
        for word in words:
            if len(word) <= 2:
                scrambled.append(word)
            else:
                middle = list(word[1:-1])
                random.shuffle(middle)
                scrambled.append(word[0] + "".join(middle) + word[-1])
        return " ".join(scrambled)

    else:
        return f"Unknown mode '{mode}'. Choose from: reverse, encode, scramble"


@tooldef
def get_current_time_in_timezone(timezone: str) -> str:
    """A tool that fetches the current local time in a specified timezone.

    Args:
        timezone: A string representing a valid timezone (e.g., 'America/New_York').
    """
    try:
        tz = pytz.timezone(timezone)
        local_time = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        return f"The current local time in {timezone} is: {local_time}"
    except Exception as e:
        return f"Error fetching time for timezone '{timezone}': {str(e)}"



final_answer = FinalAnswerTool()

model = HfApiModel(
    max_tokens=2096,
    temperature=0.5,
    model_id='Qwen/Qwen2.5-Coder-32B-Instruct',
    custom_role_conversions=None,
)

image_generation_tool = load_tool("agents-course/text-to-image", trust_remote_code=True)

with open("prompts.yaml", 'r') as stream:
    prompt_templates = yaml.safe_load(stream)

agent = CodeAgent(
    model=model,
    tools=[final_answer, my_custom_tool, get_current_time_in_timezone, image_generation_tool],
    max_steps=6,
    verbosity_level=1,
    grammar=None,
    planning_interval=None,
    name=None,
    description=None,
    prompt_templates=prompt_templates
)

GradioUI(agent).launch()
