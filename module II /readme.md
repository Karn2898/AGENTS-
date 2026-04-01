**smolagents**

Code agents are the default agent type in smolagents. They generate Python tool calls to perform actions, achieving action representations that are efficient, expressive, and accurate.
here is the agent code : https://github.com/Karn2898/AGENTS-/blob/main/module%20II%20/alfred.py

________________________________________________________________________________
module II /tools here is how you use tools in smolagents
To interact with a tool, the LLM needs an interface description with these key components:

Name: What the tool is called

Tool description: What the tool does

Input types and descriptions: What arguments the tool accepts

Output type: What the tool returns

For instance, while preparing for a party at Wayne Manor, Alfred needs various tools to
gather information - from searching for catering services to finding party theme ideas.
---------------------------------------------------------------------------------
Here’s how a simple search tool interface might look:

Name: web_search

Tool description: Searches the web for specific queries

Input: query (string) - The search term to look up

Output: String containing the search results
____________________________________________________________________________________
smolagents comes with a set of pre-built tools that can be directly injected into your agent. The default toolbox includes:

PythonInterpreterTool
FinalAnswerTool
UserInputTool
DuckDuckGoSearchTool
GoogleSearchTool
VisitWebpageTool
______________________________________________________________________________________

**Retrieval Agents**: Agentic RAG (Retrieval-Augmented Generation) extends traditional RAG systems by combining autonomous agents with dynamic knowledge retrieval.

While traditional RAG systems use an LLM to answer queries based on retrieved data, agentic RAG enables intelligent control of both retrieval and generation processes, improving efficiency and accuracy.

enhanced agent can:

1.First check the documentation for relevant information
2.Combine insights from the knowledge base
3.Maintain conversation context in memory
_______________________________________________________________________________________
[module II /smolagents/multi_agent_systems.py Multi-agent systems] :
A typical setup might include:

A Manager Agent for task delegation
A Code Interpreter Agent for code execution
A Web Search Agent for information retrieval

For example, a Multi-Agent RAG system can integrate:

A Web Agent for browsing the internet.
A Retriever Agent for fetching information from knowledge bases.
An Image Generation Agent for producing visuals.

______________________________________________________________________________________
**LangGrph**  [module II /LangGraph/Blocks_of_langGraph.py] To build applications with LangGraph, you need to understand its core components.An application in LangGraph starts from an entrypoint, and depending on the execution, the flow may go to one function or another until it reaches the END.
<img width="1505" height="672" alt="application" src="https://github.com/user-attachments/assets/1a8e3cd9-f54b-4360-bd83-efe3f13f99dd" />
_______________________________________________________________________________________
<img width="1175" height="639" alt="first_graph" src="https://github.com/user-attachments/assets/df732f13-8844-4dd7-bc16-1d72ccec2c65" />
building my first langgraph
