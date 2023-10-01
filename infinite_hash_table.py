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
        """
        pos = self.hash(key)
        if self.array[pos] is None:
            raise KeyError(key)
        elif isinstance(self.array[pos][1], InfiniteHashTable):
            return self.array[pos][1][key]
        elif self.array[pos][0] == key:
            return self.array[pos][1] 
        
            

    def __setitem__(self, key: K, value: V) -> None:
        """
        Set an (key, value) pair in our hash table.
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

        :complexity:
            :best case: O(len(key))
            :worst case: O(len(key) + table_size)
            Best case occurs when the element to be deleted is in the parent hash table.
            Worst case
        """
        pos = self.hash(key)
        print(self.array[pos])
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
            :best case: O(n+ klog(k))
            :worst case: O(nm + klog(k))
            where n is the table size, m is the length of the keys, and k is the number of keys

        """
        #Get all the keys 
        keys = self.get_keys()
        return mergesort(keys)

       
    def get_keys(self) -> list[str]:
        """
        The function recursively retrieves all keys from an InfiniteHashTable object and returns them as
        a list.
        :return: a list of keys from the given `InfiniteHashTable` object.

        :complexity:
            :best case: O(n)
            :worst case: O(nm)
            where n is the table_size and m is the length of the keys
            The best case occurs when there are no sub hash tables

        """

        elems = []
        for elem in self.array:
            if elem is not None:
                if isinstance(elem[1], InfiniteHashTable):
                    elems += elem[1].get_keys()
                else:
                    elems.append(elem[0])
        return elems


