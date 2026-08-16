"""
Scratch module: demostrate dict[str , Callable] dispatch vs if/else chains.
Supressed by real command dispatch in cli/commands / ( Phase 11)
"""


from collections.abc import Callable


def handle_create(payload: dict) -> str:

    return f"created : {payload}"



def handle_delete(payload: dict) -> str: 

    return f"deleted : {payload}"


def handle_update(payload: dict) -> str:

    return f"updated : {payload}"



COMMAND_HANDLERS : dict[str , Callable[[dict] , str]] =  {

    "create" : handle_create , 
    "delete" : handle_delete ,
    "update" : handle_update

}


def dispatch(command: str , payload: dict) -> str:

    handler = COMMAND_HANDLERS.get(command) 

    if handler is None:
        raise ValueError(f"Unknown command: {command}")

    return handler(payload) 




print(dispatch("create" , {"name": "Acme"}))