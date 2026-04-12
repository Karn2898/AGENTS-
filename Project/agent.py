import os
from typing import Optional

from smolagents import CodeAgent, DuckDuckGoSearchTool, FinalAnswerTool, InferenceClientModel, VisitWebpageTool, tool


DEFAULT_WEB_SEARCH_TASK = (
    "Search the web for the latest reliable information on a topic, "
    "open the most relevant sources, and return a concise summary with source names."
)

WEB_SEARCH_BRIEF = (
    "Use web search and page visits to answer the task. Prefer reliable sources, "
    "compare conflicting claims when needed, and include source names in the final answer."
)


@tool
def summarize_goal(goal: str, context: Optional[str] = None) -> str:
    """Turn a user goal into a short execution brief for the agent."""
    context_text = f" Context: {context}." if context else ""
    return f"Goal: {goal}.{context_text} Focus on the clearest actionable answer."


def build_agent() -> CodeAgent:
    model_id = os.getenv("SMOLAGENTS_MODEL_ID", "Qwen/Qwen2.5-Coder-32B-Instruct")
    provider = os.getenv("SMOLAGENTS_PROVIDER", "together")

    model = InferenceClientModel(
        model_id=model_id,
        provider=provider,
        max_tokens=int(os.getenv("SMOLAGENTS_MAX_TOKENS", "4096")),
    )

    return CodeAgent(
        model=model,
        tools=[
            DuckDuckGoSearchTool(),
            VisitWebpageTool(),
            summarize_goal,
            FinalAnswerTool(),
        ],
        additional_authorized_imports=["json", "re", "math"],
        max_steps=int(os.getenv("SMOLAGENTS_MAX_STEPS", "10")),
        verbosity_level=int(os.getenv("SMOLAGENTS_VERBOSITY", "2")),
    )


def run_agent(task: str) -> str:
    agent = build_agent()
    return agent.run(f"{WEB_SEARCH_BRIEF}\n\nTask: {task}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run the Project web search agent")
    parser.add_argument(
        "task",
        nargs="?",
        default=DEFAULT_WEB_SEARCH_TASK,
        help="The research task for the agent to solve",
    )
    parser.add_argument(
        "--context",
        default=None,
        help="Extra context to guide the web research task",
    )
    args = parser.parse_args()

    task = args.task
    if args.context:
        task = f"{task}\n\nContext: {args.context}"

    result = run_agent(task)
    print(result)
