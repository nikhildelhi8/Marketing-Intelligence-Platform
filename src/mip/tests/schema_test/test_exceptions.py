# test_exceptions.py

# isinstance(ValidationError(...), MIPError) is True — same for RepositoryError, NotFoundError.
# except MIPError catches an instance of each subclass when raised — proves the broad-catch use case actually works, not just the type hierarchy in isolation.


import pytest 
from  mip.exceptions import MIPError , ValidationError , NotFoundError , RepositoryError


def test_custom_validation():

    assert isinstance(ValidationError() , MIPError)
    assert isinstance(NotFoundError() , MIPError)
    assert isinstance(RepositoryError() , MIPError)



