import collections
from concurrent.futures import ThreadPoolExecutor
import os
import time
from pprint import pprint


def get_age(scientist):
    time.sleep(1)
    print(f"Process {os.getpid()} working record {scientist.name}")
    name_and_age = {
        "name": scientist.name,
        "age": int(time.strftime("%Y")) - scientist.born,
    }
    print(f"Process {os.getpid()} done processing record {scientist.name}")

    return name_and_age


if __name__ == "__main__":
    Scientist = collections.namedtuple("Scientist", ["name", "field", "born", "nobel",])

    scientists = (
        Scientist(name="Ada Lovelace", field="math", born=1815, nobel=False),
        Scientist(name="Emmy Noether", field="math", born=1882, nobel=False),
        Scientist(name="Marie Curie", field="physics", born=1867, nobel=True),
        Scientist(name="Tu Youyou", field="chemistry", born=1930, nobel=True),
        Scientist(name="Ada Yonath", field="chemistry", born=1939, nobel=True),
        Scientist(name="Vera Rubin", field="astronomy", born=1928, nobel=False),
        Scientist(name="Sally Ride", field="physics", born=1951, nobel=False),
    )
    
    print("\nSerial execution")
    start = time.time()
    result = tuple(map(get_age, scientists))
    end = time.time()
    pprint(result)
    print(f"\nTime to complete: {end - start:.2f}s\n")
    

    print("\nParallel execution")
    start = time.time()
    with ThreadPoolExecutor() as executor:
        result = executor.map(get_age, scientists)
    end = time.time()
    pprint(tuple(result))
    print(f"\nTime to complete: {end - start:.2f}s\n")
    
