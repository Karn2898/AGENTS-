import os
from typing import Any, Dict

from google import genai
from google.genai import types
from poke_env.player import Player


def normalize_name(name: str) -> str:
    return name.lower().replace(" ", "").replace("-", "")


TOOL_SCHEMA = {
    "choose_move": {
        "name": "choose_move",
        "description": "Selects and executes an available attacking or status move.",
        "parameters": {
            "type": "object",
            "properties": {
                "move_name": {
                    "type": "string",
                    "description": "The exact name or ID (e.g., 'thunderbolt', 'swordsdance') of the move to use. Must be one of the available moves.",
                }
            },
            "required": ["move_name"],
        },
    },
    "choose_switch": {
        "name": "choose_switch",
        "description": "Selects and switches to a different Pokemon.",
        "parameters": {
            "type": "object",
            "properties": {
                "pokemon_name": {
                    "type": "string",
                    "description": "The exact name of the Pokemon to switch to. Must be one of the available Pokemon in the player's party that is not currently active.",
                }
            },
            "required": ["pokemon_name"],
        },
    },
}


class LLMAgentBase(Player):
    """Base player that exposes function-calling tool declarations."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.standard_tools = TOOL_SCHEMA

    async def _get_llm_decision(self, battle_state: str) -> Dict[str, Any]:
        raise NotImplementedError


class GeminiAgent(LLMAgentBase):
    """Uses Google Gemini API for battle decisions."""

    def __init__(
        self,
        api_key: str = None,
        model: str = "gemini-2.5-pro-preview-03-25",
        avatar: str = "steven",
        *args,
        **kwargs,
    ):
        kwargs["avatar"] = avatar
        kwargs["start_timer_on_battle_start"] = True
        super().__init__(*args, **kwargs)

        self.model_name = model
        used_api_key = api_key or os.environ.get("GOOGLE_API_KEY")
        if not used_api_key:
            raise ValueError("Google API key not provided or found in GOOGLE_API_KEY env var.")

        self.genai_client = genai.Client(api_key=used_api_key)
        self.function_declarations = list(self.standard_tools.values())

    async def _get_llm_decision(self, battle_state: str) -> Dict[str, Any]:
        """Sends state to Gemini and returns a function-call decision."""
        prompt = (
            "Based on the current battle state, decide the best action: either use an available move or switch to an available Pokemon. "
            "Consider type matchups, HP, status conditions, field effects, entry hazards, and potential opponent actions. "
            "Only choose actions listed as available using their exact ID (for moves) or species name (for switches). "
            "Use the provided functions to indicate your choice.\n\n"
            f"Current Battle State:\n{battle_state}\n\n"
            "Choose the best action by calling the appropriate function ('choose_move' or 'choose_switch')."
        )

        try:
            tools = [types.Tool(function_declarations=self.function_declarations)]
            config = types.GenerateContentConfig(
                tools=tools,
                automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
            )
            response = self.genai_client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=config,
            )

            function_calls = response.function_calls or []
            if not function_calls:
                return {"error": "Gemini did not return a function call."}

            function_name = function_calls[0].name
            arguments = function_calls[0].args or {}
            if function_name not in self.standard_tools:
                return {"error": f"Model called unknown function '{function_name}'."}

            return {"decision": {"name": function_name, "arguments": arguments}}
        except Exception as exc:
            return {"error": f"Unexpected error: {exc}"}
        