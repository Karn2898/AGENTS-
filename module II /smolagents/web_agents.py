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
