import random 
from faker import Faker
from typing import Any


fake = Faker()
fake.seed_instance(42)


def generate_owners(n : int) -> list[dict[str , Any]] : 
    '''
    Generate n 'owner' parent records with unique ids like 'owner_0'
    '''
    return [{"id" : f"owner_{i}" , "name" : f"{fake.name()}"} for i in range(n)]




def generate_pets(n: int, owner_ids: list[str]) -> list[dict[str, Any]]:
    """
    Generate n 'pet' child records, each with an 'owner_id'
    sampled ONLY from owner_ids (never invented).
    """
    return [
        {"id" : f"pets_{i}" , "owner_id" : random.choice(owner_ids)  , "pet_name" : f"{fake.first_name()}"}
        for i in range(n)
    ]

def check_dangling_fks(pets: list[dict], owner_ids: list[str]) -> int:
    """
    Return the COUNT of pets whose owner_id does NOT exist in owner_ids.
    Should always be 0 if generate_pets was implemented correctly.
    """

    count = 0

    for pet in pets:
        if pet.get("owner_id") not in owner_ids:
            count += 1

    return count 


if __name__ == "__main__":

    owners = generate_owners(3)
    owner_ids = [o["id"] for o in owners]

    pets = generate_pets(10 , owner_ids) 

    dangling = check_dangling_fks(pets , owner_ids)

    print(f"Dangling fks: {dangling}")

    assert dangling == 0
    print("Referential integrity check passed successfully!")

    


