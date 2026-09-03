from faker import Faker
from typing import Any
from pprint import pprint

def generate_fake_companies(n: int , seed: int = 42) -> list[dict[str , Any]] :

    '''
    Genereate n fake companies as dicts with keys : name , industry , budget.
    Must be determinisic for a given seed.
    '''

    fake = Faker()
    
    # Faker.seed(seed) # this sets the seed in class level gloval seed , but for big project it can alter other instance where we use it 
    fake.seed_instance(42) # it will lock the state to that specific fake instance

   

    return [
       
       {
            "company_name": fake.company(),
            "full_name": fake.name(),
            "user_id": fake.uuid4(),
            "moto": fake.bs(),
            "budget": fake.random_int(min=42_000, max=1_000_000),
        }
        for _ in range(n)
    ]


if __name__ == "__main__" : 
    
    batch1 = generate_fake_companies(5 , seed=42)
    batch2 = generate_fake_companies(5 , seed=42)
    pprint(batch1)
    assert batch1 == batch2 , "Not determinstic" 
    print("Deterministic OK")



