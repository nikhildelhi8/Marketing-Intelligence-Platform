import json 
from pathlib import Path
from typing import Any
from fk_drill import generate_owners , generate_pets



def save_dataset(data: dict[str , Any] , path: Path) -> None:

    '''
    Persist data as pretty-printed json , creating parents dirs as needed
    '''

    path.parent.mkdir(parents=True , exist_ok=True)
    with open(path , "w" , encoding="utf-8") as f :
        json.dump(data , f , indent=2)


def load_dataset(path: Path) -> dict[str , Any] :
    '''load and return the json file at path as a dict'''

    with open(path , encoding="utf-8") as f:
        return json.load(f)


def verify_integrity(data: dict[str , Any]) -> int:
    '''
    Given a loaded dataset with keys 'owners' and 'pets', return the count of dangling FK references (pet.owner_id is not in owners)
    '''    
    count = 0 

    owners_ids = [ item.get("owner_id" , -1) for item in data["owners"]]

    for pets  in data["pets"]:

        for pet in pets:
            if pet.get("owner_id") not in owners_ids:
                count +=1 

    return count 


if __name__ == "__main__" : 

    owners = generate_owners(5)
    owner_ids = [o["id"] for o in owners]

    pets = generate_pets(20 , owner_ids)

    dataset = {"owners":owners , "pets": pets}


    # serialization( write out to disk)
    output_path = Path("out/dataset.json")
    save_dataset(dataset , output_path)
    print(f"dataset successfully written to {output_path.resolve()}")

    reloaded = load_dataset(output_path)


    dangling = verify_integrity(reloaded)

    print("dangling fk's after round-trip" , dangling)

    assert dangling == 0,(f"Integrity check failed: found {dangling} dangling foreign keys!"
    )
    print("Persistence & integrity verification passed successfully!")












