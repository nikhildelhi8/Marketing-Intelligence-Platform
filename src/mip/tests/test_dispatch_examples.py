# Dispatch equivalence test — write a tests/unit/test_dispatch_examples.py that calls both dispatch_command("create", {...}) directly and manually replicates the naive if/elif version inline in the test,
# asserting they produce identical output. This is what "proving both paths behave identically" means — not a general test, a comparison test.

from mip.utils.dispatch_examples import (
    dispatch , handle_update , handle_delete , handle_create
)
import pytest



def naive_dispatch(command: str , payload: dict) -> str : 

    if command == "create":
        return handle_create(payload)

    elif command == "delete":
        return handle_delete(payload)

    elif command == "update" :
        return handle_update(payload)

    else :
        raise ValueError(f"Unknown command: {command}")



@pytest.mark.parametrize("command, payload", [
    ("create", {"name": "nikhil"}),
    ("update", {"name": "nikhil"}),
    ("delete", {"name": "nikhil"}),
])


def test_dispatch_tests(command , payload) : 
    assert dispatch(command , payload) == naive_dispatch(command , payload)


def test_dispatch_and_naive_both_raise_on_unknown_command():
    with pytest.raises(ValueError):
        dispatch("unknown" , {"name" : "nikhil"})

    with pytest.raises(ValueError):
        naive_dispatch("unknown" , {"name": "nikhil"})