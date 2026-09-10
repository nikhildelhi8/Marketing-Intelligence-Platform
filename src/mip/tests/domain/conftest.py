import pytest
import json
from mip import PROJECT_ROOT


file_name = PROJECT_ROOT/'data'/'seed'/'seeded_dataset.json'



@pytest.fixture(scope="session")
def seeded_dataset():

    with open(file_name  , 'r') as file :

        data = json.load(file)

    return data





