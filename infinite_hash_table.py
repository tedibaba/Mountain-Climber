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
        self.sub_array_count = 0
        self.elems = [] #Keeping track if the pairs in the hash table 

    def hash(self, key: K) -> int:
        if self.level < len(key):
            return ord(key[self.level]) % (self.TABLE_SIZE-1)
        return self.TABLE_SIZE-1

    def __getitem__(self, key: K) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.
        """
        pos = self.hash(key)
        if isinstance(self.array[pos][1], InfiniteHashTable):
            return self.array[pos][1][key]
        elif self.array[pos][0] == key:
            return self.array[pos][1] 
        else:
            raise KeyError(key)

    def __setitem__(self, key: K, value: V) -> None:
        """
        Set an (key, value) pair in our hash table.
        """
        pos = self.hash(key)
        if self.array[pos] is None: #Base case
            self.array[pos] = (key,value)
            self.elems.append((key,value))
            self.count += 1
        else:
            if not isinstance(self.array[pos][1], InfiniteHashTable):
                temp = self.array[pos]
                self.array[pos] = (key[:self.level + 1], InfiniteHashTable(self.level + 1))
                self.array[pos][1][temp[0]] = temp[1]
                self.count -= 1 #We reduce the count because this spot in the table is not holding a base value anymore
                self.sub_array_count += 1
            self.array[pos][1][key] = value #Recurse

    def __delitem__(self, key: K) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.
        """
        self.del_helper(key, self)

    
    def del_helper(self, key, parent):
        pos = self.hash(key)

        if pos is not None:
            if self.array[pos][0] == key and not isinstance(self.array[pos][1], InfiniteHashTable):
                self.elems.remove(self.array[pos])
                self.array[pos] = None
                self.count -= 1
                res1 = [item for item in self.array if item is not None and not isinstance(item[1], InfiniteHashTable)]

                return (self, res1[0]) if res1 != [] else None

            elif isinstance(self.array[pos][1], InfiniteHashTable):
                res = self.array[pos][1].del_helper(key, self)
                if res is not None:
                    # if not single_value_left[0] and self.count > 1:
                    #     #curr deal with

                    if  res[0].count <= 1 and res[0].sub_array_count <= 0:
                        #collapse
                        self.count += 1
                        self.sub_array_count -= 1
                        self.array[pos] = (res[1][0], res[1][1])
                        self.elems.append(res[1])
                        return (self, res[1])
                    elif self == parent and res[0].sub_array_count <= 1:
                        self.array[pos] = (res[1][0], res[1][1])
                        self.count += 1
                        self.sub_array_count -= 1
                        self.elems.append(res[1])
                return



        raise KeyError(key)
            
    def __len__(self) -> int:
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
        result = ''
        for item in self.array:
            if item is not None:
                result += "↳ "
                result += item[0]

                if item[0][-1] == "*":
                    result += f"({len(item[1])})" # size of the table
                    result += "\n"
                    result += str(item[1])
                else:
                    result += f" = {item[1]}"
                    result += "\n"

        indented_result = ""
        for line in result.split("\n"):
            if line != "":
                indented_result += "|   " + line + "\n"

        return indented_result

    def get_location(self, key) -> list[int]:
        """
        Get the sequence of positions required to access this key.

        :raises KeyError: when the key doesn't exist.
        """

        pos = self.hash(key)
        if not isinstance(self.array[pos][1], InfiniteHashTable):
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
        """
        #Get all the keys 
        keys = self.get_keys()
        return mergesort(keys)

       
    def get_keys(self):
        elems = []
        for elem in self.array:
            if elem is not None:
                if isinstance(elem[1], InfiniteHashTable):
                    elems += elem[1].get_keys()
                else:
                    elems.append(elem[0])
        return elems


