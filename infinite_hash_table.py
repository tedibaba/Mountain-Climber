from __future__ import annotations
from typing import Generic, TypeVar

from data_structures.referential_array import ArrayR
from data_structures.linked_stack import LinkedStack
from algorithms.mergesort import mergesort

K = TypeVar("K")
V = TypeVar("V")

class InfiniteHashTable(Generic[K, V]):
    """
    Infinite Hash Table.

    Type Arguments:
        - K:    Key Type. In most cases should be string.
                Otherwise `hash` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    TABLE_SIZE = 27

    def __init__(self, level: int = 0) -> None:
        self.count = 0 
        self.array = ArrayR(self.TABLE_SIZE)
        self.level = level
        self.sub_array_count = 0 #Number of sub hash tables in the current hash table

    def hash(self, key: K) -> int:
        if self.level < len(key):
            return ord(key[self.level]) % (self.TABLE_SIZE-1)
        return self.TABLE_SIZE-1

    def __getitem__(self, key: K) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.
        :complexity: 
            :best case: O(1)
            :worst case: O(len(key))
            Best case occurs when the key is in the original hash table
            
        """
        pos = self.hash(key)
        if self.array[pos] is None:
            raise KeyError(key)
        elif isinstance(self.array[pos][1], InfiniteHashTable): #This elif statement must be above the next elif because it is possible the key matches the entry but there is more recursion to be done
            return self.array[pos][1][key]
        elif self.array[pos][0] == key:
            return self.array[pos][1] 
        
            

    def __setitem__(self, key: K, value: V) -> None:
        """
        Set an (key, value) pair in our hash table.

        :complexity:
            :best case: O(1)
            :worst case: O(A * len(key))
            where A is the size of the hash table
            Best case occurs when the key is in the original hash table
            Worst case occurs two words have matching prefixes and so an infinite hash table is created for each letter in the prefix 
        """
        pos = self.hash(key)
        if self.array[pos] is None: #Base case
            self.array[pos] = (key,value)
            self.count += 1
        else:
            if not isinstance(self.array[pos][1], InfiniteHashTable):
                if self.array[pos][0] == key:#Need to consider reassign
                    self.array[pos] = (key,value)
                    return
                temp = self.array[pos] #We need to reassign this value into the hash table about to be created
                self.array[pos] = (key[:self.level + 1], InfiniteHashTable(self.level + 1))
                self.count -= 1 #We reduce the count because this spot in the table is not holding a base value anymore
                self.sub_array_count += 1
                self.array[pos][1][temp[0]] = temp[1]

            self.array[pos][1][key] = value #Recurse

    def __delitem__(self, key: K) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.
        
        :complexity:
            :best case: O(len(key))
            :worst case: O(len(key) + table_size) 

            Best case occurs when the element to be deleted is in the parent hash table.
            Worst case when the element to be deleted requires a hash table for each letter to be traversed.
        """
        self.del_helper(key, self)

    
    def del_helper(self, key, parent):
        """
        The function `del_helper` is used to delete an element from a hash table and handle the case of
        collapsing sub-arrays.
        
        
        :param key: The `key` parameter represents the key of the element that needs to be deleted from
        the hash table
        :param parent: The "parent" parameter represents the head infinite table
        :raises KeyError: when the key does not exist.

        :complexity: see __delitem__
        """
        pos = self.hash(key)
        if pos is not None:
            
            if self.array[pos][0] == key and not isinstance(self.array[pos][1], InfiniteHashTable):
                self.array[pos] = None
                self.count -= 1
                res1 = [item for item in self.array if item is not None and not isinstance(item[1], InfiniteHashTable)] #Getting all values in this hash table (not any in the sub hash tables)

                return (self, res1[0]) if len(res1) == 1 else None #Only if res1 has only one element, then we might need to collapse this infinite hash table

            elif isinstance(self.array[pos][1], InfiniteHashTable):
                res = self.array[pos][1].del_helper(key, parent)
                if res is not None:
                    if  res[0].count <= 1 and res[0].sub_array_count <= 0: #Checking if only one element is left in the sub hash table
                        # Collapse this hash table and place the single value in the parent hash table
                        self.count += 1
                        self.sub_array_count -= 1
                        self.array[pos] = (res[1][0], res[1][1])
                        return (self, res[1])
                    
                    elif self == parent and res[0].sub_array_count <= 0 and res[0].count <= 1: #If we are at the parent, we cannot go up anymore
                        self.array[pos] = (res[1][0], res[1][1])
                        self.count += 1
                        self.sub_array_count -= 1
                return

        raise KeyError(key) 
            
    def __len__(self) -> int:
        """
        Returns to number of elements in the infinite hash table

        :complexity:
            :best case: O(1)
            :worst case: O(nm)
            where n is the table size and m is the longest element in the hash table.
            The best case occurs when the elements in the hash table do not share any common values and hence are able all be counted in the top level infinite hash table.
            The worst case involves recursing all the way to the bottom of the infinite hash table for every entry in the hash table.
        """
        res = self.count
        for i in self.array:
            if i is not None and isinstance(i[1], InfiniteHashTable):
               res += len(i[1]) 
        return res


    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """
        pass

    def get_location(self, key) -> list[int]:
        """
        Get the sequence of positions required to access this key.

        :param key: The key we are searching for the location to
        :raises KeyError: when the key doesn't exist.

        :complexity: 
            :best case: O(1)
            :worst case: O(n)
            where n is the length of the key
            The best case occurs when the key is in the top level of the hash table.
            The worst case occurs when n recursions must occur to reach where the key is located.
        """

        pos = self.hash(key)
        if not isinstance(self.array[pos][1], InfiniteHashTable): #Base case
            if self.array[pos][0] == key:
                return [pos] 
            else:
                raise KeyError()
        return [pos] + self.array[pos][1].get_location(key)

            

    def __contains__(self, key: K) -> bool:
        """
        Checks to see if the given key is in the Hash Table

        :complexity: See linear probe.
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True

    def sort_keys(self, current=None) -> list[str]:
        """
        Returns all keys currently in the table in lexicographically sorted order.

        :complexity:
            :best case: O(a)
            :worst case: O(nal)
            where a is the table_size, l is the length of the longest key and 
            n is the number of words inserted 
            The best case occurs when there are no sub hash tables

        """

        elems = []
        if self.array[self.TABLE_SIZE - 1] is not None: #At the bottom, there are words with no matter letters so we must add those first
            elems.append(self.array[self.TABLE_SIZE - 1][0])
        for i in range(self.TABLE_SIZE):
            index = (19 + i) % self.TABLE_SIZE #Words starting with a are not at the first index so we must calculate an offset so we can start at a
            if index == self.TABLE_SIZE - 1:
                continue
            if self.array[index] is not None:
                if isinstance(self.array[index][1], InfiniteHashTable):
                    elems += self.array[index][1].sort_keys()
                else:
                    elems.append(self.array[index][0])
        return elems




if __name__ == "__main__":
    inf = InfiniteHashTable()
    
    words = ['on', 'language', 'rough', 'cpython', 'way', 'tribute', 'while', 'perls', 'abc', 'difficult', 'preferably', 'increases', 'fun', 'core', 'program', 'was', 'contrast', 'namea', 'should', 'alex', 'their', 'written', 'interfaces', 'espoused', 'grammar', 'rossums', 'standard', 'building', 'style', 'by', 'functions', 'one', 'made', 'syntax', 'group', 'van', 'speed', 'emphasis', 'easily', 'particularly', 'has', 'reject', 'stemmed', 'software', 'idioms', 'patches', 'moving', 'improved', 'timecritical', 'giving', 'execution', 'sketch', 'and', 'describe', 'would', 'oneand', 'for', 'implementation', 'or', 'examples', 'into', 'neologism', 'frustrations', 'a', 'optimization', 'fluency', 'reference', 'oftenused', 'natural', 'can', 'not', 'programmable', 'related', 'reads', 'rather', 'with', 'show', 'lesscluttered', 'something', 'avoid', 'this', 'british', 'clarity', 'playful', 'minimalist', 'do', 'means', 'materials', 'strive', 'in', 'spam', 'adding', 'functionality', 'be', 'of', 'all', 'vision', 'conform', 'modules', 'it', 'foo', 'via', 'languages', 'meanings', 'compliment', 'pythonand', 'eggs', 'unpythonic', 'methodology', 'applications', 'programming', 'range', 'book', 'popular', 'aim', 'choice', 'author', 'such', 'pypy', 'pythonic', 'interpreter', 'large', 'small', 'wrote', 'using', 'to', 'clever', 'understand', 'readability', 'common', 'called', 'martelli', 'pythons', 'designed', 'transcription', 'compiler', 'other', 'from', 'highly', 'is', 'tutorials', 'noncritical', 'instead', 'modularity', 'community', 'his', 'existing', 'culture', 'more', 'embraces', 'use', 'strives', 'extension', 'the', 'simpler', 'wide', 'approach', 'parts', 'cost', 'reflected', 'than', 'offer', 'fellow', 'well', 'marginal', 'extensible', 'developers', 'bar', 'that', 'which', 'there', 'python', 'may', 'another', 'foundation', 'only', 'motto', 'at', 'like', 'approaches', 'premature', 'terms', 'opposite', 'oneobvious', 'monty', 'occasionally', 'justintime', 'code', 'library', 'philosophy', 'its', 'compact', 'as', 'coding', 'c', 'crosscompiling', 'comedy', 'considered']

    for w in words:
        inf[w] = 'value of '+ w

    assert inf.sort_keys() == sorted(words)
    assert len(inf) == len(words)

    locations = [[7, 6, 26], [4, 19, 6, 25, 13, 19, 25, 23, 26], [10, 7, 13], [21, 8], [15, 19, 17], [12, 10, 1], [15, 0, 1, 4], [8, 23], [19, 20], [22, 1], [8, 10, 23, 24], [1, 6, 21], [24, 13, 6, 26], [21, 7, 10], [8, 10, 7, 25, 10, 19, 5, 26], [15, 19, 11], [21, 7, 6, 12], [6, 19, 5], [11, 0, 7, 13], [19, 4, 23], [12, 0, 23, 1], [15, 10, 1], [1, 6, 12, 23, 10, 24], [23, 11], [25, 10, 19], [10, 7, 11], [11, 12, 19], [20, 13], [11, 12, 17], [20, 17], [24, 13, 6, 21, 12, 1, 7, 6, 11], [7, 6, 23, 26], [5, 19, 22], [11, 17], [25, 10, 7], [14, 19], [11, 8, 23], [23, 5, 8], [23, 19], [8, 19, 10, 12, 1], [0, 19], [10, 23, 2], [11, 12, 23], [11, 7, 24], [1, 22], [8, 19, 12], [5, 7, 14], [1, 5, 8, 10], [12, 1], [25, 1], [23, 16, 23], [11, 3], [19, 6, 22], [22, 23, 11, 21], [15, 7], [7, 6, 23, 19], [24, 7, 10], [1, 5, 8, 4], [7, 10], [23, 16, 19], [1, 6, 12, 7], [6, 23], [24, 10, 13], [19, 26], [7, 8, 12], [24, 4], [10, 23, 24, 23], [7, 24, 12], [6, 19, 12], [21, 19, 6], [6, 7, 12], [8, 10, 7, 25, 10, 19, 5, 5, 19], [10, 23, 4], [10, 23, 19, 22, 11], [10, 19, 12], [15, 1, 12], [11, 0, 7, 15], [4, 23], [11, 7, 5], [19, 14], [12, 0, 1], [20, 10], [21, 4, 19], [8, 4], [5, 1], [22, 7], [5, 23, 19, 6, 11], [5, 19, 12], [11, 12, 10, 1, 14, 23, 26], [1, 6, 26], [11, 8, 19], [19, 22], [24, 13, 6, 21, 12, 1, 7, 6, 19], [20, 23], [7, 24, 26], [19, 4, 4], [14, 1, 11], [21, 7, 6, 24], [5, 7, 22, 13, 4, 23], [1, 12, 26], [24, 7, 7], [14, 1, 19], [4, 19, 6, 25, 13, 19, 25, 23, 11], [5, 23, 19, 6, 1], [21, 7, 5, 8, 4], [8, 17, 12, 0, 7, 6, 19], [23, 25], [13, 6, 8], [5, 23, 12], [19, 8, 8, 4], [8, 10, 7, 25, 10, 19, 5, 5, 1], [10, 19, 6], [20, 7], [8, 7], [19, 1], [21, 0], [19, 13], [11, 13], [8, 17, 8], [8, 17, 12, 0, 7, 6, 1], [1, 6, 12, 23, 10, 8], [4, 19, 10], [11, 5], [15, 10, 7], [13, 11, 1], [12, 7], [21, 4, 23], [13, 6, 22], [10, 23, 19, 22, 19], [21, 7, 5, 5, 7], [21, 19, 4], [5, 19, 10, 12], [8, 17, 12, 0, 7, 6, 11], [22, 23, 11, 1], [12, 10, 19], [21, 7, 5, 8, 1], [7, 12], [24, 10, 7], [0, 1, 25], [1, 11], [12, 13], [6, 7, 6], [1, 6, 11], [5, 7, 22, 13, 4, 19], [21, 7, 5, 5, 13], [0, 1, 11], [23, 16, 1], [21, 13], [5, 7, 10], [23, 5, 20], [13, 11, 23], [11, 12, 10, 1, 14, 23, 11], [23, 16, 12, 23, 6, 11, 1, 7], [12, 0, 23, 26], [11, 1], [15, 1, 22], [19, 8, 8, 10, 7, 19, 21, 0, 26], [8, 19, 10, 12, 11], [21, 7, 11], [10, 23, 24, 4], [12, 0, 19, 6], [7, 24, 24], [24, 23], [15, 23], [5, 19, 10, 25], [23, 16, 12, 23, 6, 11, 1, 20], [22, 23, 14], [20, 19], [12, 0, 19, 12], [15, 0, 1, 21], [12, 0, 23, 10], [8, 17, 12, 0, 7, 6, 26], [5, 19, 17], [19, 6, 7], [24, 7, 13], [7, 6, 4], [5, 7, 12], [19, 12], [4, 1, 3], [19, 8, 8, 10, 7, 19, 21, 0, 23], [8, 10, 23, 5], [12, 23], [7, 8, 8], [7, 6, 23, 7], [5, 7, 6], [7, 21], [2], [21, 7, 22, 23], [4, 1, 20], [8, 0], [1, 12, 11], [21, 7, 5, 8, 19], [19, 11], [21, 7, 22, 1], [21, 26], [21, 10], [21, 7, 5, 23], [21, 7, 6, 11]]
    for w in words:
        assert inf.get_location(w) == locations.pop(0)


    del inf['python']
    assert len(inf) == len(words) - 1
    assert 'python' not in inf

    inf['python'] = 'new value'
    assert inf['python'] == 'new value'

    assert len(inf) == len(words)

    for w in words:
        del inf[w]
    assert len(inf) == 0