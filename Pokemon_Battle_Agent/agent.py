import os
import json
import asyncio
import random

from google import genai
from google.genai import types

from poke_env.player import Player
from typing import Optional,Dict,Any,Union

def normalize_name(name:str)->str:
    return name.lower().replace(" ","").replace("-","")

TOOL_SCHEME={
    "choose_move": {
        "name":"choose_move",
        "description":"Selects and executes an available attacking or status move.",
    "parameters":{
        "type":"object",
        "properties":{
            "move_name":{
                "type":"string",
                "description":"The exact name or ID (e.g., 'thunderbolt', 'swordsdance') of the move to use. Must be one of the available moves."
            
            },
            "required":["move_name"]
        },
        
    },
    "choose_switch":{
        "name":"choose_switch",
        "description":"Selects and switches to a different Pokémon.",
        "parameters":{
            "type":"object",
            "properties":{
                "pokemon_name":{
                    "type":"string",
                    "description":"The exact name of the Pokémon to switch to. Must be one of the available Pokémon in the player's party that is not currently active."
                },
            },
            "required":["pokemon_name"]
        },
    } ,
        
    }
}

class LLMAgentBase(Player):
    super().__init__(self, *args , **kwargs):
    self.tools=TOOLS_SCHEMA
    self.battle_history=[]
    
def _format_battle_state(self,battle)->str:
    actie_pkmn=battle.active_pokemon
    f"HP: {active_pkmn.current_hp_fraction * 100:.1f}% " \
    f"Status: {active_pkmn.status.name if active_pkmn.status else 'None'} " \
    f"Boosts: {active_pkmn.boosts}"active_pkmn_info= f"Your active Pokemon: {active_pkmn.species}"\
        
opponent_pkmn=battle.opponent_active_pokemon
opp_info_str="unknown"
if opponent_pkmn:
    oppo_info_str=  f"{opponent_pkmn.species} " \
                    f"(Type: {'/'.join(map(str, opponent_pkmn.types))}) " \
                    f"HP: {opponent_pkmn.current_hp_fraction * 100:.1f}% " \
                    f"Status: {opponent_pkmn.status.name if opponent_pkmn.status else 'None'} " \
                    f"Boosts: {opponent_pkmn.boosts}"  
                    
opponent_pkmn_info= f"Opponent's active Pokemon: {opp_info_str}"             
                      