import os
from typing import Optional

from smolagents import CodeAgent, DuckDuckGoSearchTool, FinalAnswerTool, InferenceClientModel, VisitWebpageTool, tool


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
    return agent.run(task)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run the Project agent")
    parser.add_argument("task", help="The task for the agent to solve")
    args = parser.parse_args()

    result = run_agent(args.task)
    print(result)
