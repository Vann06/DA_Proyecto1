# carga y arma de delta

import json
from dataclasses import dataclass
from typing import Dict, Tuple

TransitionKey = Tuple[str,str]
TransitionVal = Tuple[str,str,str] #write, move, next

@dataclass
class MachineDef:
    name:str
    blank:str
    start_state:str
    accept_states: set[str]
    reject_states: set[str]
    delta: Dict[TransitionKey, TransitionVal]

def load_machine(path: str) -> MachineDef:
    with open(path, "r", encoding="utf-8-sig") as f:
        data = json.load(f)
    
    blank = data.get("blank", "_")
    start_state = data["start_state"]
    accept_states = set(data.get("accept_states" ,[]))
    reject_states = set(data.get("reject_states", []))
    name = data.get("name", path)

    delta: Dict[TransitionKey, TransitionVal] ={}
    for t in data["transitions"]:
        key = (t["state"], t["read"])
        val = (t["write"], t["move"], t["next"])
        if key in delta : 
            raise ValueError(f"Transicion Duplicada {key}")
        delta[key] = val 

    return MachineDef(
        name=name,
        blank=blank,
        start_state=start_state,
        accept_states=accept_states,
        reject_states=reject_states,
        delta=delta,
    )