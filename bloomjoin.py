from typing import List
import math

# Bloom filter size
FILTER_SIZE = 10

class BloomFilter:
    def __init__(self, filter_size: int):
        self.filter_size = filter_size
        self.bit_set = [False] * filter_size

    def add(self, key: str) -> None:
        hash1 = self.hash_function1(key)
        hash2 = self.hash_function2(key)
        hash3 = self.hash_function3(key)
        self.bit_set[hash1] = True
        self.bit_set[hash2] = True
        self.bit_set[hash3] = True

    def contains(self, key: str) -> bool:
        hash1 = self.hash_function1(key)
        hash2 = self.hash_function2(key)
        hash3 = self.hash_function3(key)
        return self.bit_set[hash1] and self.bit_set[hash2] and self.bit_set[hash3]

    def hash_function1(self, key: str) -> int:
        hash_value = 0
        for char in key:
            hash_value = (hash_value * 31 + ord(char)) % self.filter_size
        return hash_value

    def hash_function2(self, key: str) -> int:
        hash_value = 0
        for char in key:
            hash_value = (hash_value * 37 + ord(char)) % (self.filter_size - 1)
        return hash_value

    def hash_function3(self, key: str) -> int:
        hash_value = 0
        for char in key:
            hash_value = (hash_value * 41 + ord(char)) % (self.filter_size - 2)
        return hash_value

def bloom_join(relation1: List[str], relation2: List[str]) -> List[str]:
    # Create Bloom filter for relation 2
    bloom_filter = BloomFilter(FILTER_SIZE)
    for row in relation2:
        parts = row.split(",")
        key = parts[0].strip()
        bloom_filter.add(key)

    # Perform join
    result = []
    for row in relation1:
        parts = row.split(",")
        key = parts[0].strip()
        if bloom_filter.contains(key):
            branch = find_branch(relation2, key)
        else:
            branch = "Branch not found"  # Ensuring every item is processed even if not in Bloom filter
        result.append(row + ", " + branch)

    return result

def find_branch(relation2: List[str], key: str) -> str:
    for row in relation2:
        parts = row.split(",")
        if parts[0].strip() == key.strip():
            return parts[1].strip()  # Return the branch
    return "Branch not found"

if __name__ == "__main__":
    # Define two relations
    relation1 = ["1, Sakshi", "2, Prachi", "3, Shriya", "5, Akash"]
    relation2 = ["1, Finance", "2, HR", "4, Marketing"]

    # Perform the Bloom join
    results = bloom_join(relation1, relation2)

    # Print each result
    for result in results:
        print(result)


