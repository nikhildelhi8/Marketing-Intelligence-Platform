import csv 
from pathlib import Path 


def read_rows(path: Path) : 
    with open(path , newline="" , encoding = "utf-8") as f :
        reader = csv.DictReader(f)
        for row in reader:
            print(row)