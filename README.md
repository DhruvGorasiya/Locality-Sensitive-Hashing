## Locality Sensitive Hashing (LSH) for Efficient Column Similarity Detection

This project implements a Python-based Locality Sensitive Hashing (LSH) algorithm designed to efficiently detect similarities between columns in large datasets. LSH is particularly valuable for high-dimensional data where traditional similarity detection methods can be computationally expensive.

### Key Features

- **Shingle Generation**: Breaks text data into `k`-shingles (substrings of length `k`) to capture unique patterns within columns.
- **1-Hot Vector Encoding**: Converts shingles into binary vectors (1-hot encoding) for hash-based signature generation.
- **Random Hash Functions**: Generates random permutations to create hash functions for LSH signatures.
- **Jaccard Similarity Calculation**: Measures the similarity between columns using the Jaccard index.
- **Banding and Candidate Detection**: Utilizes banding techniques to efficiently find similar columns in large datasets by comparing LSH signatures.

### How It Works

1. **Shingling**: Text from database columns is divided into `k`-shingles (substrings) of a fixed size `k`, capturing patterns and uniqueness in the data.
2. **Signature Generation**: Using random hash functions, LSH signatures are created based on 1-hot encoded vectors of the shingles.
3. **Similarity Calculation**: LSH signatures are split into bands, and the similarity is calculated using the Jaccard similarity metric to detect similar columns.
4. **Candidate Detection**: Bands from the LSH signatures are compared to detect potential column matches and return candidate pairs.

### Usage

1. Initialize the LSH object:
    ```python
    lsh = LSH(vocabs=set())
    ```

2. Generate `k`-shingles from column text:
    ```python
    shingles_set = lsh.shingles(text='column_text', k=4)
    ```

3. Create LSH signatures using random hash functions:
    ```python
    hash_list = lsh._randomHashes(n=200)
    one_hot_vector = lsh._1_hot(list(shingles_set))
    signature = lsh.signatures(hash_list, one_hot_vector)
    ```

4. Calculate Jaccard similarity between columns:
    ```python
    similarity = lsh.jaccard_similarity(set1=signature1, set2=signature2)
    print(f"Jaccard Similarity: {similarity}")
    ```

5. Find candidate column pairs:
    ```python
    candidates = lsh.find_candidate(band1=split_vector1, band2=split_vector2)
    print(f"Candidate Pairs: {candidates}")
    ```

### Example

The included script also demonstrates how to analyze column similarities in a table. You can run the `solve()` function to apply this process to a table such as `'people'`.

```python
solve('people')
```

### Requirements

- Python 3.x
- Libraries: `random`, `os`, `glob`