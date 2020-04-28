# Scaffold for solution to DIT873 / DAT346, Programming task 3
from operator import itemgetter

def sublist(s_list):
    # Create the sublist function which uses generators in order to
    # identify all sub-lists with ascending order
    # from a given l_list
    # Your code below
    n=s_list[0]
    sublist=[]
    for v in s_list:
        if v>=n:
            sublist.append(v)
            n=v
        else:
            yield sublist
            sublist=[v]
            n=v
    yield sublist
    #return

def longest_common_list(s_list):
    # Create the longest_common_list function which returns the common longest sublist
    # in s_list and the reverse of s_list
    # Please use the list comprehension in this function
    # Your code below
    s_list_rev=[i for i in reversed(s_list)]
    sublists=sublist(s_list)
    sublists_rev=sublist(s_list_rev)
    common_list=[[len(a),a] for a in sublists if a in sublists_rev]
    return sorted(common_list)[-1][1]



# The following is called if you execute the script from the commandline
# e.g. with python Solution.py
if __name__ == "__main__":

    assert longest_common_list([1,1,2,3,0,0,3,4,5,7,1,3,2,1,1,2]) == [1,1, 2, 3]
