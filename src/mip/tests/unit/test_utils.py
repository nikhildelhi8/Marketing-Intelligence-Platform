from mip.utils.formatting import safe_float , safe_int  , parse_percentage
from mip.utils.transforms import chunked
import pytest



@pytest.mark.parametrize("raw_value , expected" , [

    ("abc" , None) , 
    (123 , None ) , 
    (None , None),
])

def test_safe_int_bad_input_returns_default(raw_value , expected) :
    assert safe_int(raw_value) == expected


# def test_safe_int_logs_warning_on_bad_string(caplog):
#     safe_int("not a number")
#     assert "safe_int failed" in caplog.text


# def test_chunked_splits_correctly():
#     result = list(chunked([1,2,3,4,5] , 2))
#     assert result == [[1,2] , [3,4] ,[5]]


# def test_chunked_raises_on_zero_size():
#     with pytest.raises(ValueError):
#         list(chunked([1,2,3,4]  , 0))



# Test for safe_float()
@pytest.mark.parametrize("raw_value , default , expected" ,   [

    ("abc" , 0.0   , 0.0) ,
    ("++" ,  None  , None)
])


def test_safe_float_returns_custom_default( raw_value , default , expected):
    assert safe_float(raw_value , default) == expected

def test_safe_float_returns_warning_on_bad_input(caplog):
    safe_float("not a relevant float number")
    assert "safe_float failed due to" in caplog.text.lower()



# Test for safe_int()

@pytest.mark.parametrize("raw_value , expected" , [

    ("12.5" , None) ,
    ("abc" , None) , 
    (123 , None ) , 
    (None , None),
])

def test_safe_int_bad_input_returns_default(raw_value , expected) :
    assert safe_int(raw_value) == expected


# Test for parse_percentage

@pytest.mark.parametrize("raw_value , default , expected" , [

    ("45%" , None , 0.45) ,
    ("0%" , None , 0.0) , 
    ("ab%" ,None , None)
])


def test_parse_percentage_test(raw_value , default , expected) :

    assert parse_percentage(raw_value , default)  == expected



