
from pydantic import AfterValidator
from typing import Annotated



def validate_budget(value: int) -> int :

    if value <= 0 :
        raise ValueError(f"Budget must be postive , got {value}")

    return value 

PositiveBudget = Annotated[int , AfterValidator(validate_budget)]