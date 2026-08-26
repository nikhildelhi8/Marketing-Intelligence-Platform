'''
csv_loader.py 

Streams the raw kaggle influencer/social-post CSV as parsed , typed dicts.

This module is the ONLY place in the project that reads the raw CSV.
Everything downstream (seed_data.py and every later phase) consumes the already-parsed output of this module , 
never the raw file again.
'''

import csv 
from pathlib import Path 
from typing import Iterator , Any , Callable

from mip.utils.formatting import safe_float , safe_int , safe_bool , safe_datetime , safe_string

from mip import PROJECT_ROOT





CSV_PATH = PROJECT_ROOT / "data"/"raw"/"influencer_marketing.csv"



COLUMN_PARSERS : dict[str , Callable[[str] , Any]] = {

    "Post_ID"               : safe_string,
    "Timestamp"             : safe_datetime,
    "Platform"              : safe_string,
    "Content_Type"          : safe_string,
    "Category"              : safe_string,
    "Likes"                 : safe_int,
    "Comments"              : safe_int,
    "Shares"                :  safe_int,
    "Views"                 :  safe_int,
    "Saves"                 :  safe_int,
    "Follower_Count"        :  safe_int,
    "Engagement_Rate"       : safe_float,
    "Hour_of_Day"           : safe_int,
    "Day_of_Week"           : safe_string,
    "Hashtag_Count"         : safe_int,
    "Content_Length"        : safe_int,
    "Sentiment"             : safe_string,
    "Influencer_Tier"       : safe_string,
    "Has_Media"             : safe_bool,
    "Is_Verified"           : safe_bool,
}



def load_influencer_csv(path: Path) -> Iterator[dict] : 

    """
    Stream rows from the raw influencer/social-post CSV, applying
    COLUMN_PARSERS to each column so callers receive typed, cleaned values
    instead of raw strings.

    Must NOT materialize the full file into memory — yield row by row.

    Args:
        path: filesystem path to the raw CSV file.

    Yields:
        One dict per CSV row, with values converted per COLUMN_PARSERS
        (or left as-is / cleaned, per your Step 3 decision on unmapped columns).
    """
    def identity(value: Any) -> Any :
        return value




    with open(path , newline="" , encoding="utf-8") as f:

        reader = csv.DictReader(f)

        for row in reader :
            yield { k : COLUMN_PARSERS.get(k ,identity)(v) for k , v in row.items()}



if __name__ == "__main__" :

    for i , row in enumerate(load_influencer_csv(CSV_PATH) , start= 1) :

        print(f"row {i}" , row)

        if i >=5:
            break







    
        

            



    


