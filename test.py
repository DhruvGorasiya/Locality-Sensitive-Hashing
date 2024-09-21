import random
import os
import glob

class LSH:
    def __init__(self, vocabs: set):
        """
        Initializes the LSH class with a set of vocabulary.

        Parameters:
        - vocabs (set): A set to store unique vocabulary elements encountered in the shingles.
        """
        self.vocabs = vocabs

    def reset_vocabs(self):
        """
        Resets the vocabulary set to an empty set.
        """
        self.vocabs = set()

    def shingles(self, text: str, k: int) -> set:
        """
        Generates a set of k-shingles (substrings of length k) from the given text.

        Parameters:
        - text (str): The input text from which shingles are generated.
        - k (int): The length of each shingle.

        Returns:
        - set: A set of unique k-shingles from the text.
        """
        if k > len(text):
            k = len(text)
        text = text.lower()
        _set = set([text[i:i+k] for i in range(len(text) - k + 1)])
        self.vocabs = self.vocabs.union(_set)
        return _set
    
    def _1_hot(self, vocab: list) -> list:
        """
        Converts a list of vocabulary into a 1-hot vector based on the current vocabulary set.

        Parameters:
        - vocab (list): A list of shingles to be converted into a 1-hot vector.

        Returns:
        - list: A 1-hot vector representing the presence of shingles in the vocab list.
        """
        return [1 if i in vocab else 0 for i in self.vocabs]
        
    def _randomize(self) -> list:
        """
        Generates a random permutation of indices for the vocabulary set.

        Returns:
        - list: A list of random indices corresponding to the vocabulary set.
        """
        _random = list(range(1, len(self.vocabs) + 1))
        random.shuffle(_random)
        return _random
    
    def _randomHashes(self, n: int) -> list:
        """
        Generates a list of n random hash functions (permutations).

        Parameters:
        - n (int): The number of random hash functions to generate.

        Returns:
        - list: A list containing n lists of random indices (hash functions).
        """
        _hashes = []
        for i in range(n):
            _hashes.append(self._randomize())
        return _hashes
    
    def signatures(self, _hashLists: list, _1_hot_vector: list) -> list:
        """
        Generates a signature for the given 1-hot vector using a specified number of hash functions.

        Parameters:
        - signature_size (int): The number of hash functions to use for generating the signature.
        - _1_hot_vector (list): The 1-hot vector for which the signature is generated.

        Returns:
        - list: The signature vector generated using the hash functions.
        """
        signature = []
        # _hashLists = self._randomHashes(signature_size)

        for i in _hashLists:
            for j in range(1, len(self.vocabs) + 1):
                ind = i.index(j)
                signature_val = _1_hot_vector[ind]
                if signature_val == 1:
                    signature.append(ind)
                    break
        return signature
    
    def split_vector(self, signature: list, b: int) -> list:
        """
        Splits a signature vector into b bands.

        Parameters:
        - signature (list): The signature vector to be split.
        - b (int): The number of bands to split the signature into.

        Returns:
        - list: A list of sub-vectors (bands) from the signature vector.
        """
        assert len(signature) % b == 0, "choose a different number for band"
        r = int(len(signature) / b)
        sub_vectors = []
        for i in range(0, len(signature), r):
            sub_vectors.append(signature[i:i+r])
        return sub_vectors
    
    def find_candidate(self, sub_vec_a: list, sub_vec_b: list):
        """
        Finds candidate pairs by comparing two lists of sub-vectors (bands).

        Parameters:
        - sub_vec_a (list): The list of sub-vectors (bands) for the first item.
        - sub_vec_b (list): The list of sub-vectors (bands) for the second item.

        This function prints the candidate pair if a matching band is found.
        """
        for a, b in zip(sub_vec_a, sub_vec_b):
            if a == b:
                return(f"{a} == {b}")
            
        return "There is no candidate pair"
            
    def jaccard_set_containment(self, x: set, y: set) -> float:
        """
        Computes the Jaccard set containment of set x within set y.

        Parameters:
        - x (set): The first set.
        - y (set): The second set.

        Returns:
        - float: The Jaccard set containment ratio.
        """
        return len(x.intersection(y)) / len(x)                
            
    def jaccard_similarity(self, x: set, y: set) -> float:
        """
        Computes the Jaccard similarity between two sets.

        Parameters:
        - x (set): The first set.
        - y (set): The second set.

        Returns:
        - float: The Jaccard similarity coefficient.
        """
        return len(x.intersection(y)) / len(x.union(y))
    
    def load_data(self) -> dict:
        """
        Loads data from CSV files in the specified directory and organizes it into a dictionary.

        Returns:
        - dict: A dictionary where keys are table names and values are dictionaries containing column data.
        """
        dict = {}
        directory = '/Users/dhruvgorasiya/Documents/Drive 1/university/sem 8/327/LSH/data'
        csv_files = glob.glob(os.path.join(directory, '*.csv'))
        table_name = [os.path.basename(file).replace(".csv", "") for file in csv_files]
        
        for k in table_name:
            dict[k] = {}
            for j in range(len(open(f"data/{k}.csv",'r').readline().split(','))):
                temp = open(f"data/{k}.csv",'r').readline().split(',')[j]
                dict[k][temp] = []
                for i in open(f"data/{k}.csv",'r'):
                    dict[k][temp].append(i.split(",")[j])
        return dict

if __name__ == "__main__":
    o = LSH(set())
                
    def solve(T: str):
        """
        Main function to solve the problem by finding similar items in different tables.

        Parameters:
        - T (str): The name of the target table to find similar items in other tables.

        This function processes the target table and compares it with other tables to find pairs
        with high Jaccard set containment or similarity. It prints the pairs found and their similarities.
        """
        table_data = o.load_data()
        target = table_data.pop(T)

        target_table_column_name_shingles = {i: o.shingles(i, 2) for i in target}
    

        pairs = []
        scores = []
        for i in target_table_column_name_shingles:
            print(i)
            for k in table_data:
                for j in table_data[k]:
                    shingle_j = o.shingles(j, 2)
                    if (o.jaccard_set_containment(target_table_column_name_shingles[i], shingle_j) > 0.5) or (o.jaccard_set_containment(shingle_j, target_table_column_name_shingles[i]) > 0.5):
                        scores.append(max(o.jaccard_set_containment(target_table_column_name_shingles[i], shingle_j),(o.jaccard_set_containment(shingle_j, target_table_column_name_shingles[i]))))
                        pairs.append((i, j, k))
        print(pairs)

        for i in pairs:
            
            # if i[0] != i[1]:
            #     continue
            
            shingles_pair_target = set()
            shingles_pair_table2 = set()
            

            for j in target[i[0]]:
                shingles_pair_target = shingles_pair_target.union(o.shingles(j, 4))
                
            for k in table_data[i[2]][i[1]]:
                shingles_pair_table2 = shingles_pair_table2.union(o.shingles(k, 4))
                
            
            signature_size = 200
            _hashLists = o._randomHashes(signature_size)
            
            _1_hot_pair_target = o._1_hot(list(shingles_pair_target))
            signature_target = o.signatures(_hashLists, _1_hot_pair_target)
            
            split_vectors_pair1_target = o.split_vector(signature_target, len(signature_target) // 2)
            
            _1_hot_pair_table2 = o._1_hot(list(shingles_pair_table2))
            signature_table2 = o.signatures(_hashLists, _1_hot_pair_table2)
            split_vectors_pair1_table2 = o.split_vector(signature_table2, len(signature_target) // 2)
            
        
            
            print(f"""The similar columns are:
                    column name of Target Table: {i[0]}
                    column name of Table with similarity: {i[1]}
                    similar table name: {i[2]}
                    The similarity between the columns is: {o.jaccard_similarity(set(signature_target), set(signature_table2))}
                    The candidate pairs are: {o.find_candidate(split_vectors_pair1_target, split_vectors_pair1_table2)}
                    """)

            
            # print(i,o.jaccard_similarity(set(signature_target), set(signature_table2)),o.find_candidate(split_vectors_pair1_target,split_vectors_pair1_table2))
            
            o.reset_vocabs()
            
    print(solve('patientdb'))
