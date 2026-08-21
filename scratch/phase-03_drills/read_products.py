import csv
from pathlib import  Path
from typing import Iterator


CURRENT_FILE_DIR = Path(__file__).resolve().parent

PROJECT_ROOT = CURRENT_FILE_DIR.parents[0]

CSV_PATH = PROJECT_ROOT / "products.csv"





def read_products(path: Path) -> Iterator[dict] :
    '''
    Read a csv of products and yield each row as a dict 

    Must not load the whole file into memory at once 
    '''
    with open(path , newline="", encoding="utf-8") as f :
        reader = csv.DictReader(f)
        
        for row in reader:
            yield row





if __name__ == "__main__":
    
    print(CSV_PATH)
    for product in read_products(Path(CSV_PATH)):
        
        print(product)
