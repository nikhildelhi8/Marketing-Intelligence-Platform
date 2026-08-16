import timeit 
from mip.utils.formatting import safe_float



import random

# Base pool of realistic raw CSV entries
clean_numeric = [
    "0",
    "1",
    "42",
    "100.5",
    "0.0034",
    "-15.2",
    "1299.99",
    "3.14159",
    "99999",
    "0.50",
    "250",
    "-0.01",
    "18.75",
    "4000.0",
    "72.1",
]

formatted_numeric = [
    "$1,200.50",
    "$45.00",
    "€99.99",
    "£150.00",
    "50%",
    "12.5%",
    "1,000,000",
    "  45.67  ",
    "\t12.8\n",
    "- $50.00",
    "100.00 USD",
    "2.5k",
]

missing_and_nulls = [
    "",
    " ",
    "   ",
    "N/A",
    "n/a",
    "NA",
    "NaN",
    "nan",
    "None",
    "null",
    "NULL",
    "-",
    "--",
    "?",
    "undefined",
]

garbage_strings = [
    "pending",
    "free",
    "error",
    "unknown",
    "TBD",
    "missing",
    "two hundred",
    "O",  # letter O instead of zero
    "l",  # lowercase L instead of one
    "12.34.56",
    "#VALUE!",
    "#REF!",
    "inf",
    "-inf",
]

# Generate a 1,000-item realistic dataset:
# ~60% valid/clean numeric, ~15% formatted, ~15% missing/nulls, ~10% garbage
raw_values = (
    random.choices(clean_numeric, k=600)
    + random.choices(formatted_numeric, k=150)
    + random.choices(missing_and_nulls, k=150)
    + random.choices(garbage_strings, k=100)
)

# Shuffle to simulate a real dirty column
random.seed(42)
random.shuffle(raw_values)





def run_comprehension(raw_values: list) -> float:

    number_of_runs = 250

    total_time_comprehension = timeit.repeat(
          lambda : list(map(safe_float , raw_values)) , 
          repeat = 5 , 
          number = 1000
    )

    # Average time per run in milliseconds

    avg_time_ms = (total_time_comprehension / number_of_runs) * 1000

    return avg_time_ms





def run_map(raw_values :list) ->  float :

    number_of_runs = 250
    # total_time_map = timeit.timeit(
    #     lambda : list(map(safe_float , raw_values)) , 
    #     number= number_of_runs
    # )

    total_time_map = timeit.repeat(
        lambda : list(map(safe_float , raw_values)) , 
        repeat = 5 , 
        number = 1000
    )
    #print(total_time_map)

    avg_time_ms = (total_time_map / number_of_runs) * 1000

    return avg_time_ms



comp_time = run_comprehension(raw_values)
map_time = run_map(raw_values)



print(f"average time of execution for comprehension is {comp_time}")

print(f"average time of execution for map is {map_time}")






