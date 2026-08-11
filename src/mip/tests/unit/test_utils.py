from mip.utils.formatting import safe_float , safe_int  , parse_percentage  , format_currency
from mip.utils.transforms import chunked , flatten , apply_pipeline
import pytest









# def test_chunked_raises_on_zero_size():
#     with pytest.raises(ValueError):
#         list(chunked([1,2,3,4]  , 0))



# Test for safe_float()
@pytest.mark.parametrize("raw_value , default , expected" ,   [

    ("abc" , 0.0   , 0.0) ,
    ("$1,234.56" , None , 1234.56) , 
    ("12.5%" , None , 12.5),
    (123, None , None)  , 
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

def test_safe_int_logs_warning_on_bad_string(caplog):
    safe_int("not a number")
    assert "safe_int failed" in caplog.text




#parse_percentage

@pytest.mark.parametrize("raw_value , default , expected" , [

    ("45%" , None , 0.45) ,
    ("0%" , None , 0.0) , 
    ("ab%" ,None , None) ,
    ("ab%" , 99.0 , 99.0)
])


def test_parse_percentage_test(raw_value , default , expected) :

    assert parse_percentage(raw_value , default)  == expected



# Format currency 

@pytest.mark.parametrize(
    "val, expected",
    [
        (1234.5, "$1,234.50"),
        (0.0, "$0.00"),
        (None , "$0.00"),
        ("" , "$0.00") ,
        (1000000, "$1,000,000.00"),
    ],
)
def test_format_currency_valid_floats(val, expected):
    assert format_currency(val) == expected




# chunked 

@pytest.mark.parametrize(
    "iterable, size, expected",
    [
        ([], 2, []),  # Empty iterable yields no chunks
        ([1,2,3,4,5] , 2 , [[1,2] , [3,4] , [5]]) ,
        ([1], 5, [[1]]),  # Fewer elements than chunk size
    ],
)
def test_chunked_edge_cases(iterable, size, expected):
    assert list(chunked(iterable, size)) == expected

def test_chunked_raises_on_zero_size():
    with pytest.raises(ValueError):
        list(chunked([1,2,3,4] , 0))

# flatten 

def test_flatten_basic_nested_list():
    nested = [[1, 2], [3, 4], [5]]
    assert list(flatten(nested)) == [1, 2, 3, 4, 5]


def test_flatten_handles_mixed_flat_and_nested_items():
    # Proves the isinstance guard handles primitive elements alongside iterables
    mixed = [1, [2, 3], 4, [5]]
    assert list(flatten(mixed)) == [1, 2, 3, 4, 5]



#apply_pipeline

def test_apply_pipeline_preserves_strict_execution_order():
    add_one = lambda x: x + 1
    double = lambda x: x * 2
    square = lambda x: x**2

    pipeline = [add_one, double, square]

    # Pipeline applies left-to-right: square(double(add_one(3))) = 64
    assert apply_pipeline(3, *pipeline) == 64