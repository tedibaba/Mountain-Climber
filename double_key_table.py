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
        self.internal_sizes = internal_sizes
        self.count = 0
        self.top_level_count = 0
        self.top_size_index = 0

        self.array = ArrayR(self.TABLE_SIZES[self.top_size_index])
            

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
        pos1 = self.find_top_position(key1, is_insert)
        
        return (pos1, self.array[pos1][1]._linear_probe(key2, is_insert))

    def find_top_position(self, key1, is_insert):
        pos1 = self.hash1(key1)

        for _ in range(self.top_level_count + 1):
            #We have to linear probe until we can find a spot for the first key
            if self.array[pos1] is None or self.array[pos1][0] is None:
                if is_insert:
                    self.array[pos1] = (None, LinearProbeTable(self.internal_sizes))
                    self.array[pos1][1].hash = lambda k: self.hash2(k, self.array[pos1][1])
                    break
                else:
                    raise KeyError(key1)
            elif self.array[pos1][0] == key1:
                break     
            pos1 = (pos1 + 1) % self.table_size
        else:
            if is_insert:
                raise FullError
            else:
                raise KeyError(key1)
        return pos1

    def iter_keys(self, key:K1|None=None) -> Iterator[K1|K2]:
        """
        key = None:
            Returns an iterator of all top-level keys in hash table
        key = k:
            Returns an iterator of all keys in the bottom-hash-table for k.
        """
        return TopLevelIterator(self, key)


    def keys(self, key:K1|None=None) -> list[K1|K2]:
        """
        key = None: returns all top-level keys in the table.
        key = x: returns all bottom-level keys for top-level key x.
        """
        return [x for x in TopLevelIterator(self, key)]
    
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
        return self.array[pos1][1][key[1]][2]

    def __setitem__(self, key: tuple[K1, K2], data: V) -> None:
        """
        Set an (key, value) pair in our hash table.
        """

        pos1, pos2 = self._linear_probe(key[0], key[1], True)
        if self.array[pos1][1].array[pos2] is None:
            self.count += 1
        if len(self.array[pos1][1]) <= 0:
            self.top_level_count += 1
            self.array[pos1] = (key[0], self.array[pos1][1])
        
        inner_hash_table = self.array[pos1][1]
        inner_hash_table[key[1]] = (key[0], key[1], data)

        if self.top_level_count > self.table_size / 2:
            self._rehash()


    def __delitem__(self, key: tuple[K1, K2]) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.
        """
        pos1, pos2 = self._linear_probe(key[0], key[1], False)

        self.array[pos1][1].__delitem__(key[1])

        if len(self.array[pos1][1]) <= 0:
            self.array[pos1] = (None, LinearProbeTable(self.internal_sizes))

    def _rehash(self) -> None:
        """
        Need to resize table and reinsert all values

        :complexity best: O(N*hash(K)) No probing.
        :complexity worst: O(N*hash(K) + N^2*comp(K)) Lots of probing.
        Where N is len(self)
        """
        if self.top_size_index >= len(self.TABLE_SIZES) - 1:
            return
        self.top_size_index += 1
        old_array = self.array
        self.count = 0
        self.array = ArrayR(self.TABLE_SIZES[self.top_size_index])

        for i in range(self.TABLE_SIZES[self.top_size_index]):
            self.array[i] = (None,LinearProbeTable(self.internal_sizes))

        for i in range(len(old_array)):
            if old_array[i] is not None:
                for elem in old_array[i][1].array:
                    if elem is not None:
                        temp, (key1, key2, val) = elem
                        self[key1, key2] = val

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
        return self.count

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """
        pass
        raise NotImplementedError()
    

class TopLevelIterator():
    def __init__(self, hash_table: DoubleKeyTable, key=None) -> None:
        self.hash_table = hash_table
        self.index = 0        

        self.given_key = key is not None #If key is not None, then we want to return the secondary keys for the given key

        if self.given_key:
            self.pos1 = self.hash_table.find_top_position(key, False)


    def __iter__(self):
        return self
    
    def __next__(self):
        if self.given_key:
            while True:
                if self.index < self.hash_table.array[self.pos1][1].table_size:
                    if self.hash_table.array[self.pos1][1].array[self.index] is not None:
                        item = self.hash_table.array[self.pos1][1].array[self.index][0]
                        self.index+= 1
                        break
                    self.index += 1
                else:
                    raise StopIteration
                
        else:
            while True:
                if self.index < self.hash_table.table_size:
                    if self.hash_table.array[self.index] is not None and self.hash_table.array[self.index][0] is not None:
                        item = self.hash_table.array[self.index][0]
                        self.index += 1
                        break
                    self.index += 1
                else:
                    raise StopIteration
                
            
        return item

class BottomLevelIterator():

    def __init__(self, hash_table: DoubleKeyTable, key=None) -> None:
        self.hash_table = hash_table
        self.index = 0        

        self.given_key = key is not None 

        if self.given_key:
            self.pos1 = self.hash_table.find_top_position(key, False)
        else:
            self.internal_index = 0


    def __iter__(self):
        return self
    
    def __next__(self):
        if self.given_key:
            while True:
                if self.index < self.hash_table.array[self.pos1][1].table_size:
                    if self.hash_table.array[self.pos1][1].array[self.index] is not None:
                        item = self.hash_table.array[self.pos1][1].array[self.index][1][2]
                        self.index+= 1
                        break
                    self.index += 1
                else:
                    raise StopIteration
        else:
            while True:
                if self.index < self.hash_table.table_size - 1 and self.hash_table.array[self.index] is None:
                    self.index += 1
                    continue
                elif self.index >= self.hash_table.table_size - 1:
                    raise StopIteration

                if self.internal_index < self.hash_table.array[self.index][1].table_size:
                    if self.hash_table.array[self.index][1].array[self.internal_index] is not None:
                        item = self.hash_table.array[self.index][1].array[self.internal_index][1][2]
                        self.internal_index += 1
                        break
                    self.internal_index += 1
                    
                else:
                    if self.index < self.hash_table.table_size - 1:
                        self.index += 1
                        self.internal_index = 0
                        
        return item
