'''Defensive parsing and formatting helpers for messy CSV/CLI input'''

'''
Every function here follows the same contract: never raise on malformed input , log a warning describing what was dropped and return a safe fallback( usually None)
 instead'''

from datetime import datetime
from typing import Any
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
              f"safe_float expected str , got for {value} {type(value).__name__}"
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



DEFAULT_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def safe_datetime(value: str , fmt: str = DEFAULT_DATETIME_FORMAT , default: datetime | None=None ) -> datetime | None :

    """Safely parse a string into a datetime object using an explicit format.

    - Returns `value` if it is already a datetime instance.
    - Returns `default` (None) if the input is None or empty.
    - Catches parsing errors, logs a warning with the offending value,
      and returns `default` instead of raising an unhandled exception.
    """


    if value is None :
        return default

    if isinstance(value , datetime) :
        return value

    if not isinstance(value , str) :

        logger.warning(
            "Expected string value got different valuetype for %s which is of type %r", 
            value , 
            type(value).__name__  , 
        )
        return default

    cleaned_value = value.strip()

    if not cleaned_value:
        return default 


    try:
        return datetime.strptime(cleaned_value , fmt)
    
    except(ValueError , TypeError) as exc :
        
        logger.warning("failed to parse datetime string %r with format %r: %s" , 
                       cleaned_value, 
                       fmt , 
                       exc
        )
        return default



BOOLEAN_MAP = {

    "true"  : True , 
    "1" : True , 
    "yes" : True , 
    "t" : True , 
    "false" : False , 
    "0" : False , 
    "no" : False , 
    "f" : False 
}



def safe_bool(value: str , default = None) -> bool :

    """Safely parse a string into a bool object.
        - Returns `default` (None) if the input is None or empty.
        - Catches parsing errors, logs a warning with the offending value,
          and returns `default` instead of raising an unhandled exception.
    """



    if value is None :
        return default 

    if not isinstance(value , str) :
    
            logger.warning(
                "Expected string value got different valuetype for %s which is of type %r", 
                value , 
                type(value).__name__  , 
            )
            return default


    try:
        clean_value = value.strip().lower()
        return  BOOLEAN_MAP.get(clean_value , default)
    

    except (ValueError , TypeError) as exc :

        logger.warning("falied to parse bool string %r : %s", 
            value ,
            exc
        )
        return default


def safe_string(value: str , default: str = "") -> str :

    '''
      Perform default cleanup on a string value: strip leading/trailing
    whitespace. Used for columns that don't need type conversion but
    still need basic hygiene applied (raw CSV text often carries
    incidental whitespace regardless of the column's semantic type).

    Args:
        value: Raw string to clean.
        default: Value to return if input is missing/invalid.

    Returns:
        The stripped string, or `default` if input is None or not a string.
    
    '''

    if value is None:
        return default

    if not isinstance(value , str) :

        logger.warning(
            "Expected string value got different valuetype for %s which is of type %r", 
            value , 
            type(value).__name__
        )
        return default

    try:
        return  value.strip()
    
    except (ValueError , TypeError) as exc :
        logger.warning("failed to parse string value due to  %s" , 
            exc , 

        )
        return default



    
    


    
        

    







    