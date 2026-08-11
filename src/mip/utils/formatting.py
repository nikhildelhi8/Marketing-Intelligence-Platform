'''Defensive parsing and formatting helpers for messy CSV/CLI input'''

'''
Every function here follows the same contract: never raise on malformed input , log a warning describing what was dropped and return a safe fallback( usually None)
 instead'''


import logging

logger = logging.getLogger(__name__)

def safe_float(value: str , default: float | None = None) -> float | None :

    '''
    Parse 'value' into a float, tolerating currency-style strings 
    like "$1,234.56" or "12.5%"

    Args:
        value : Raw string to parse.
        default: Value to return if parsing fails
    '''
    if not isinstance(value , str) :
        logger.warning(
              f"safe_float expected str , got {type(value).__name__}"
        )
        return default

    

    try:
        parsed_float_value = value.strip().strip('$%').strip().replace("," , "")
        return float(parsed_float_value)
    
    except ValueError  as e :
        logger.warning(f"Safe_float failed due to  {value}  : {e} ")
        return default 




def safe_int(value: str, default: int | None = None) -> int | None:
    """
    Parse `value` into an int, tolerating whitespace and thousands
    separators like "1,234".

    Args:
        value: Raw string to parse.
        default: Value to return if parsing fails.

    Returns:
        The parsed int, or `default` if parsing fails.
    """
    if not isinstance(value , str) :
        logger.warning(
            f"safe_int expected str , got {type(value).__name__}"
        )
        return default

    try:
        parsed_int_value = value.strip().strip('$%').replace("," , "")
        return int(parsed_int_value)
    
    except ValueError as e :
        logger.warning(f"safe_int failed due to {value}  : {e}")
        return default 


def parse_percentage(value: str, default: float | None = None) -> float | None:
    """
    Parse a percentage string like "45%" or "45.5%" into a decimal
    fraction (e.g. "45%" -> 0.45).

    Args:
        value: Raw percentage string to parse.
        default: Value to return if parsing fails.

    Returns:
        The parsed fraction as a float, or `default` if parsing fails.
    """


    float_percentage  = safe_float(value)

    if float_percentage is None:
        logger.warning("parse_percentage has failed to parse the percentage value")
        return default
    
    return float_percentage /100


    


def format_currency(value: float) -> str:
    """
    Format a numeric value as a currency string, e.g. 1234.5 -> "$1,234.50".

    Args:
        value: The numeric amount to format.

    Returns:
        A formatted currency string.

    """

    if value is None or value == "":
        logger.warning(
            f"Could not format the currency value {value} , returning $0.00"
        )
        return "$0.00"

    try:
        numeric_value = float(value)
        return f"${numeric_value:,.2f}"
    except (ValueError, TypeError) as e:
        logger.warning(
            f"Could not format currency for value '{value}': {e}"
        )
        return "$0.00"




    