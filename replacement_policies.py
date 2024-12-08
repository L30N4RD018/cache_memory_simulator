from math import log2

class Block:
    def __init__(self, tag: int = None, index: int = None, valid: bool = False, size: int = 16):
        self.tag = tag
        self.index = index
        self.valid = valid
        self.size = size
        self.data = [None]*size        
    
    def __repr__(self):
        return f"Block(tag={self.tag}, index={self.index}, valid={self.valid}, size={self.size})"
    
class Set:
    def __init__(self, blocks: list[Block] = None, index: int = 0):
        self.blocks = blocks
        self.index = index
    
    def __repr__(self):
        return f"Set(blocks={self.blocks}, index={self.index})"

class TwoWaySetAssociativeCache:

    def __init__(self, blocks: int = 4, block_size: int = 16):                
        self.blocks = blocks
        self.block_size = block_size
        self.tag_bits = int(log2(blocks))
        self._capacity = blocks * block_size
        self._sets = (self._capacity) // (block_size*2)
        blocks_aux = [Block(index=_) for _ in range(blocks)]
        self.cache = [Set(blocks=[blocks_aux.pop(0), blocks_aux.pop(0)], index=i) for i in range(self._sets)]        

    def calculate_tag(self, address: int = 0):
        tag = bin(address)[2:][:-self.tag_bits]
        if len(tag) < self.tag_bits:
            tag = '0' * (self.tag_bits - len(tag)) + tag
        return tag
    
    def calculate_set_index(self, address: int = 0):        
        return address % self._sets
    
    def calculate_block_index(self, address: int = 0):
        return address % self.block_size        

def LruReplacementPolicy(addresses: list, cache: TwoWaySetAssociativeCache):
    for address in addresses:
        set_index = cache.calculate_set_index(address)
        tag = cache.calculate_tag(address)
        block_index = cache.calculate_block_index(address)
        set = cache.cache[set_index]
        
        found = False
        for block in set.blocks:
            if block.valid and block.tag == tag:
                found = True
                break
        
        if not found:
            lru_block = min(set.blocks, key=lambda x: x.index)
            lru_block.tag = tag
            lru_block.valid = True
            start = (address // lru_block.size) * lru_block.size
            lru_block.data = [i for i in range(start, start + lru_block.size)]
            lru_block.index = block_index

cache = TwoWaySetAssociativeCache(blocks=4)
print(cache.cache)
addresses = list(map(int, input("Lista De Direcciones [x-x-x-x-x...]: ").split("-")))
LruReplacementPolicy(addresses, cache)
print(cache.cache)