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
        self.top_level_sizes = self.TABLE_SIZES
        self.internal_level_sizes = self.TABLE_SIZES
        if sizes is not None:
            self.top_level_sizes = sizes
        if internal_sizes is not None:
            self.internal_level_sizes = internal_sizes

        self.top_size_index = 0
        self.internal_size_index = 0
        self.count = 0 
        self.internal_sizes = ArrayR(self.TABLE_SIZES[self.top_size_index]) #Keeping track of the size of each internal hash table for the iterator

        self.array = ArrayR[ArrayR](self.TABLE_SIZES[self.top_size_index])
        for i in self.array: #More optimal way? 
            self.array[i] = ArrayR(self.TABLE_SIZES[self.internal_level_sizes])
            
        

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
        internal_level_position = self.hash2(key2, self.array[top_level_position])

        for _ in range(len(self.array[top_level_position])):
            if self.array[top_level_position][internal_level_position] is not None:
                if is_insert:
                    return (top_level_position, internal_level_position)
                else:
                    raise KeyError(key1, key2)
            elif self.array[top_level_position][internal_level_position][:2] == (key1, key2):
                return (top_level_position, internal_level_position)
            else:
                internal_level_position = (internal_level_position + 1) % len(self.array[top_level_position])
        
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
        if key is not None:
            pass
        else:
            pass


    def keys(self, key:K1|None=None) -> list[K1|K2]:
        """
        key = None: returns all top-level keys in the table.
        key = x: returns all bottom-level keys for top-level key x.
        """
        if key is None:
            pass

    def iter_values(self, key:K1|None=None) -> Iterator[V]:
        """
        key = None:
            Returns an iterator of all values in hash table
        key = k:
            Returns an iterator of all values in the bottom-hash-table for k.
        """
        raise NotImplementedError()

    def values(self, key:K1|None=None) -> list[V]:
        """
        key = None: returns all values in the table.
        key = x: returns all values for top-level key x.
        """
        raise NotImplementedError()

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
        pos1, pos2 = self._linear_probe(key[0], key[2], False)
        return self.array[pos1][pos2]


    def __setitem__(self, key: tuple[K1, K2], data: V) -> None:
        """
        Set an (key, value) pair in our hash table.
        """

        pos1, pos2 = self._linear_probe(key[0], key[2], True)
        if self.array[pos1][pos2] is None:
            self.count += 1
            self.internal_level_sizes[pos1] += 1

        self.array[pos1][pos2] = (pos1, pos2, data)
        
        if len(self.array[pos1]) > self.internal_level_sizes[self.internal_size_index] / 2:
            self._rehash(); 


    def __delitem__(self, key: tuple[K1, K2]) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.
        """
        pos1, pos2 = self._linear_probe(key[0], key[2], False)
        self.array[pos1][pos2] = None
        self.count -= 1
        self.internal_level_sizes[pos1] -= 1

        pos2 = (pos2 + 1) % len(self.array[pos1])

        while self.array[pos1][pos2] is not None:
            key1, key2, value = self.array[pos1][pos2]
            self.array[pos1][pos2] = None

            newpos1, newpos2 = self._linear_probe(key1, key2, True)
            self.array[newpos1][newpos2] = (newpos1, newpos2, value)
            pos2 = (pos2 + 1) % len(self.array[pos1])


    def _rehash(self) -> None:
        """
        Need to resize table and reinsert all values

        :complexity best: O(N*hash(K)) No probing.
        :complexity worst: O(N*hash(K) + N^2*comp(K)) Lots of probing.
        Where N is len(self)
        """
        self.top_size_index += 1
        self.internal_size_index += 1
        old_array = self.array
        if self.top_size_index == len(self.TABLE_SIZES): #We cannot resize anymore
            return
        
        self.array = ArrayR(self.TABLE_SIZES[self.top_size_index])
        self.count = 0
        for i in range(len(old_array)):
            old_sub_array = old_array[i]
            self.array[i] = ArrayR(self.TABLE_SIZES[self.internal_size_index])
            for elem in old_sub_array:
                if elem is not None:
                    key1, key2, val = elem
                    self[key1][key2] = val


       

    def table_size(self) -> int:
        """
        Return the current size of the table (different from the length)
        """
        return self.top_level_sizes[self.top_size_index]

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

class TopLevelKeyIterator():
    def __init__(self, hash_table: DoubleKeyTable) -> None:
        self.hash_table = hash_table
        self.index = 0        
        # self.current = hash_table.array[self.index]

        
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.index < len(self.hash_table) - 1:
            item = self.hash_table.array[self.index]
            self.index += 1
            return item
        else:
            raise StopIteration
      
       
class BottomLevelIterator():

    def __init__(self, hash_table: DoubleKeyTable, key=None) -> None:
        self.hash_table = hash_table
        self.index = 0
        self.given_key = key is not None
        if key is not None: #We only want to traverse a certain index in the hash table
            self.position = hash_table.hash1(key)
            # self.current = hash_table.array[self.position][self.index]
        else: #We want to traverse every value in the table
            while hash_table.internal_sizes[self.index] == 0:
                self.index += 1
            self.internal_index = 0

    def __iter__(self):
        return self
    
    def __next__(self):
        if self.given_key:
            if self.index < len(self.hash_table[self.position]):
                item = self.hash_table[self.position][self.index]
                self.index += 1
                return item
            else:
                raise StopIteration
        else:
            item = self.hash_table[self.index][self.internal_index]
            self.internal_index += 1
            if self.internal_index >= self.hash_table.TABLE_SIZES[self.hash_table.internal_size_index] or self.hash_table[self.index][self.internal_index] == None:
                if self.index >= len(self.hash_table) - 1:
                    raise StopIteration
                self.index += 1
                self.internal_index = 0
            return item