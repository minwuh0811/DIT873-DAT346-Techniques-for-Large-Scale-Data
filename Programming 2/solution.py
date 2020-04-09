# Scaffold for solution to DIT873 / DAT346, Programming task 2
from mrjob.job import MRJob

def encode_list(s_list):
    # Identify the run-length encoding for each data value [data value, count]
    # from a given s_list of integers or a given s_list of characters.
    # You should use generators for implementing this function and do not use groupby
    # Generators: See https://docs.python.org/3/howto/functional.html#generator-expressions-and-list-comprehensions
    # Your code below
    chr=s_list[0]
    n=0
    for c in s_list:
        if c==chr:
            n+=1
        else:
            yield [chr,n]
            n=1
            chr=c
    yield[chr,n]

    #return


def create_list (s_list):
    # returns the run-length encoded list
    encoded_list=[]
    # Your code below
    encodes=encode_list(s_list)
    for encode in encodes:
        encoded_list.append(encode)
    return encoded_list


# The following is called if you execute the script from the commandline
# e.g. with python solution.py
if __name__ == "__main__":
    assert create_list([1, 1, 1, 2, 3, 3, 4, 4, 5, 1,1,7,5]) == [[1, 3], [2, 1], [3, 2], [4, 2], [5, 1], [1, 2], [7, 1], [5, 1]]

