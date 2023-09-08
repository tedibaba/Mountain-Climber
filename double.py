from __future__ import annotations

from typing import Generic, TypeVar, Iterator
from data_structures.hash_table import LinearProbeTable, FullError
from data_structures.referential_array import ArrayR

K1 = TypeVar('K1')
K2 = TypeVar('K2')
V = TypeVar('V')

class DoubleKeyTable(Generic[K1, K2, V]):
    """
    Double Hash Table.

    Type Arguments:
        - K1:   1st Key Type. In most cases should be string.
                Otherwise `hash1` should be overwritten.
        - K2:   2nd Key Type. In most cases should be string.
                Otherwise `hash2` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    # No test case should exceed 1 million entries.
    TABLE_SIZES = [5, 13, 29, 53, 97, 193, 389, 769, 1543, 3079, 6151, 12289, 24593, 49157, 98317, 196613, 393241, 786433, 1572869]

    HASH_BASE = 31

    def __init__(self, sizes:list|None=None, internal_sizes:list|None=None) -> None:
        if sizes is not None:
            self.TABLE_SIZES = sizes
        
        if internal_sizes is not None:
            self.internal_sizes = internal_sizes
        else:
            self.internal_sizes = self.TABLE_SIZES

        self.top_size_index = 0
        self.total_count = 0 
        self.top_level_count = 0

        self.array = ArrayR(self.TABLE_SIZES[self.top_size_index])
        # for i in range(len(self.array)): #More optimal way? 
        #     self.array[i] = (None , LinearProbeTable(internal_sizes)) 
            
        

    def hash1(self, key: K1) -> int:
        """
        Hash the 1st key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """

        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % self.table_size
            a = a * self.HASH_BASE % (self.table_size - 1)
        return value

    def hash2(self, key: K2, sub_table: LinearProbeTable[K2, V]) -> int:
        """
        Hash the 2nd key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """

        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % sub_table.table_size
            a = a * self.HASH_BASE % (sub_table.table_size - 1)
        return value

    def _linear_probe(self, key1: K1, key2: K2, is_insert: bool) -> tuple[int, int]:
        """
        Find the correct position for this key in the hash table using linear probing.

        :raises KeyError: When the key pair is not in the table, but is_insert is False.
        :raises FullError: When a table is full and cannot be inserted.
        """
        top_level_position = self.hash1(key1)

        for _ in range(self.top_level_count + 1):
            #We have to linear probe until we can find a spot for the first key
            if (self.array[top_level_position][0] is None and is_insert) or (self.array[top_level_position][0] == key1):
                if self.array[top_level_position] is None:
                    self.array[top_level_position] = (None, LinearProbeTable(self.internal_sizes))
                    self.array[top_level_position][1].hash = lambda k: self.hash2(k, self.array[top_level_position][1])
                return top_level_position
            top_level_position = (top_level_position + 1) % self.table_size
        
        # internal_level_position = self.hash2(key2, self.array[top_level_position][1])

        # for _ in range(self.array[top_level_position][1].table_size):
        #     if self.array[top_level_position][1].array[internal_level_position] is None:
        #         if is_insert:
        #             return (top_level_position, internal_level_position)
        #         else:
        #             raise KeyError(key1, key2)
        #     elif self.array[top_level_position][1].array[internal_level_position][:2] == (key1, key2):
        #         return (top_level_position, internal_level_position)
        #     else:
        #         internal_level_position = (internal_level_position + 1) % self.array[top_level_position][1].table_size
        
        if is_insert:
            raise FullError(f"Hash table for {key1} is full")
        else:
            raise KeyError(key1,key2)

    def iter_keys(self, key:K1|None=None) -> Iterator[K1|K2]:
        """
        key = None:
            Returns an iterator of all top-level keys in hash table
        key = k:
            Returns an iterator of all keys in the bottom-hash-table for k.
        """
        return TopLevelKeyIterator(self, key)


    def keys(self, key:K1|None=None) -> list[K1|K2]:
        """
        key = None: returns all top-level keys in the table.
        key = x: returns all bottom-level keys for top-level key x.
        """
        for x in TopLevelKeyIterator(self,key):
            print(x)
        return [x for x in TopLevelKeyIterator(self, key)]
    
    def iter_values(self, key:K1|None=None) -> Iterator[V]:
        """
        key = None:
            Returns an iterator of all values in hash table
        key = k:
            Returns an iterator of all values in the bottom-hash-table for k.
        """
        return BottomLevelIterator(self, key)

    def values(self, key:K1|None=None) -> list[V]:
        """
        key = None: returns all values in the table.
        key = x: returns all values for top-level key x.
        """
        return [x for x in BottomLevelIterator(self, key)]

    def __contains__(self, key: tuple[K1, K2]) -> bool:
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

    def __getitem__(self, key: tuple[K1, K2]) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.
        """
        pos1, pos2 = self._linear_probe(key[0], key[1], False)
        return self.array[pos1][1].array[pos2]


    def __setitem__(self, key: tuple[K1, K2], data: V) -> None:
        """
        Set an (key, value) pair in our hash table.
        """

        pos1, pos2 = self._linear_probe(key[0], key[1], True)
        
        if self.array[pos1][1].array[pos2] is None:
            self.total_count += 1
        if len(self.array[pos1][1]) <= 0: #This hash table was empty
            self.array[pos1] = (key[0], self.array[pos1][1])
            self.top_level_count += 1

        self.array[pos1][1].array[pos2] = (key[0], key[1], data)
        self.array[pos1][1].count += 1

        if len(self.array[pos1][1]) > self.array[pos1][1].table_size / 2:
            self.array[pos1][1]._rehash()

        if self.top_level_count > self.table_size / 2:
            self._rehash()


    def __delitem__(self, key: tuple[K1, K2]) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.
        """
        pos1, pos2 = self._linear_probe(key[0], key[1], False)

        self.array[pos1][1].__delitem__(key[1])
        # self.array[pos1][1].array[pos2] = None
        # self.total_count -= 1
        # if len(self.array[pos1][1]) <= 0:
        #     self.top_level_count -= 1
        #     self.array[pos1] =(None, LinearProbeTable())

        # pos2 = (pos2 + 1) % self.array[pos1][1].table_size

        # while self.array[pos1][1].array[pos2] is not None:
        #     key1, key2, value = self.array[pos1][1].array[pos2]
        #     self.array[pos1][1].array[pos2] = None

        #     newpos1, newpos2 = self._linear_probe(key1, key2, True)
        #     self.array[newpos1][1].array[newpos2] = (key1, key2, value)
        #     pos2 = (pos2 + 1) % self.array[pos1][1].table_size


    def _rehash(self) -> None:
        """
        Need to resize table and reinsert all values

        :complexity best: O(N*hash(K)) No probing.
        :complexity worst: O(N*hash(K) + N^2*comp(K)) Lots of probing.
        Where N is len(self)
        """
        
        old_array = self.array
        if self.top_size_index >= len(self.TABLE_SIZES) - 1: #We cannot resize anymore
            return
        self.top_size_index += 1
        
        self.array = ArrayR(self.TABLE_SIZES[self.top_size_index])
        self.total_count = 0

        for i in range(self.TABLE_SIZES[self.top_size_index]):
            self.array[i] = (None,LinearProbeTable(self.internal_sizes))

        for i in range(len(old_array)):

            old_sub_array = old_array[i][1]
            self.array[i][1]
            # print(old_sub_array.values())
          
            for elem in old_sub_array.array:
                if elem is not None:
                    key1, key2, val = elem
                    self[key1,key2] = val
            
    @property
    def table_size(self) -> int:
        """
        Return the current size of the table (different from the length)
        """
        return self.TABLE_SIZES[self.top_size_index]

    def __len__(self) -> int:
        """
        Returns number of elements in the hash table
        """
        return self.total_count

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """
        pass
        # for elem in len(self.array):


class TopLevelKeyIterator():
    def __init__(self, hash_table: DoubleKeyTable, key=None) -> None:
        self.hash_table = hash_table
        self.index = 0        
        self.given_key = key is not None #If key is not None, then we want to return the secondary keys for the given key
        if key is None:
            self.keys = list(filter(lambda x: x is not None, sum([[x for x in self.hash_table.array[y][1].array] for y in range(self.hash_table.table_size)], [])))
        else:
            position = self.hash_table.hash1(key)
            self.keys = list(filter(lambda x: x is not None,[x for x in self.hash_table.array[position][1].array]))

    def __iter__(self):
        return self
    
    def __next__(self):
        if self.index < len(self.keys) - 1:
            item = self.keys[self.index]
            self.index+= 1
            return item
        raise StopIteration


       
class BottomLevelIterator():

    def __init__(self, hash_table: DoubleKeyTable, key=None) -> None:
        self.hash_table = hash_table
        self.index = 0
        if key is not None: #We only want to traverse a certain index in the hash table
            position = self.hash_table.hash1(key)
            self.values = [x[2] for x in self.hash_table.array[position][1].array]
        else: #We want to traverse every value in the table
            self.values = list(filter(lambda x: x is not None, sum([[x for x in self.hash_table.array[y][1].array] for y in range(self.hash_table.table_size)], [])))


    def __iter__(self):
        return self
    
    def __next__(self):
        if self.index < len(self.values) - 1:
            item = self.values[self.index]
            self.index += 1
            return item
        raise StopIteration
   

        

dt = DoubleKeyTable(sizes=[12], internal_sizes=[5])
dt.hash1 = lambda k: ord(k[0]) % 12
dt.hash2 = lambda k, sub_table: ord(k[-1]) % 5

dt["Tim", "Jen"] = 1
dt["Amy", "Ben"] = 2
dt["Tim", "Kat"] = 3


del dt["Tim", "Jen"]
# We can't do this as it would create the table.
# self.assertEqual(dt._linear_probe("Het", "Bob", True), (1, 3))
del dt["Tim", "Kat"]
# Deleting again should make space for Het.
dt["Het", "Bob"] = 4
print(dt._linear_probe("Het", "Bob", False), (0, 3))