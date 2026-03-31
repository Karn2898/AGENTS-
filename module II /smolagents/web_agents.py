#pip install "smolagents[all]" helium selenium python-dotenv

#We’ll need a set of agent tools specifically designed for browsing, such as search_item_ctrl_f, go_back, and close_popups. These tools allow the agent to act like a person navigating the web.
@tool
def search_item_ctrl_f(text: str , nth_result:int=1) -> str:
     """
    Searches for text on the current page via Ctrl + F and jumps to the nth occurrence.
    Args:
        text: The text to search for
        nth_result: Which occurrence to jump to (default: 1)
    """
  elements=driver.find_elements(By.XPATH, f"//*[contains(text() , '{text}')]")

  if nth_result > len(elements):
        raise Exception(f"Match n°{nth_result} not found (only {len(elements)} matches found)")
    result = f"Found {len(elements)} matches for '{text}'."
    elem = elements[nth_result - 1]
    driver.execute_script("arguments[0].scrollIntoView(true);", elem)
    result += f"Focused on element {nth_result} of {len(elements)}"
    return result

@tool 
def go_back()-> None:
  ""goes back to previous page."""

  driver.back()

  @tool
  def close_popups()->str:
"""
   Closes any visible modal or pop-up on the page. Use this to dismiss pop-up windows! This does not work on cookie consent banners.
"""
webdriver.ActionChains(driver).send_keys(keys.ESCAPE).perform()

#We also need functionality for saving screenshots, as this will be an essential part of what our VLM agent uses to complete the task. This functionality captures the screenshot and saves it in step_log.observations_images = [image.copy()], allowing the agent to store and process the images dynamically as it navigates
def save_screenshot(step_log: ActionStep, agent: CodeAgent) -> None:
sleep(1.0)
driver=helium.get_driver()
current_step=step_log.step_number
if driver is not None:
     if isinstance(step_log, ActionStep) and step_log.step_number <= current_step - 2:
                step_logs.observations_images = None
        png_bytes = driver.get_screenshot_as_png()
        image = Image.open(BytesIO(png_bytes))
        print(f"Captured a browser screenshot: {image.size} pixels")
        step_log.observations_images = [image.copy()]  
  # Update observations with current URL
url_info = f"Current url: {driver.current_url}"
step_log.observations = url_info if step_logs.observations is None else step_log.observations + "\n" + url_info
return

#This function is passed to the agent as step_callback, as it’s triggered at the end of each step during the agent’s execution. This allows the agent to dynamically capture and store screenshots throughout its process

#Now, we can generate our vision agent for browsing the web, providing it with the tools we created, along with the DuckDuckGoSearchTool to explore the web. This tool will help the agent retrieve necessary information for verifying guests’ identities based on visual cues.

from smolagents import CodeAgent, OpenAIServerModel, DuckDuckGoSearchTool
model = OpenAIServerModel(model_id="gpt-4o")

agent = CodeAgent(
    tools=[DuckDuckGoSearchTool(), go_back, close_popups, search_item_ctrl_f],
    model=model,
    additional_authorized_imports=["helium"],
    step_callbacks=[save_screenshot],
    max_steps=20,
    verbosity_level=2,
)

agent.run("""
I am Alfred, the butler of Wayne Manor, responsible for verifying the identity of guests at party. A superhero has arrived at the entrance claiming to be Wonder Woman, but I need to confirm if she is who she says she is.

Please search for images of Wonder Woman and generate a detailed visual description based on those images. Additionally, navigate to Wikipedia to gather key details about her appearance. With this information, I can determine whether to grant her access to the event.
""" + helium_instructions)
