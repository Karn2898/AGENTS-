#use images from Wikipedia to keep the example minimal, but imagine the possible use-case
from PIL import Image
import requests
from io import BytesI0

image_urls=[
      "https://upload.wikimedia.org/wikipedia/commons/e/e8/The_Joker_at_Wax_Museum_Plus.jpg", # Joker image
    "https://upload.wikimedia.org/wikipedia/en/9/98/Joker_%28DC_Comics_character%29.jpg" # Joker image
]

images=[]
for url in image_urls:
  headers={
    "user-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
  }

response=requests.get(url ,headers=headers)
image=Image.open(BytesI0(response.content)).convert("RGB")
images.append(image)
#now the agent will tell us wheather one guest is actually a superhero
from smolagents import CodeAgent ,OpenAIServerModel

model=OpenAIServiceModel(model_id="gpt-4o")

#instantiate the agent
agent=CodeAgent(
      tools=[],
      model=model,
      max_steps=20,
      verbosity_level=2
)

response=agent.run(
       """
    Describe the costume and makeup that the comic character in these photos is wearing and return the description.
    Tell me if the guest is The Joker or Wonder Woman.
    """,
      images=images
)
