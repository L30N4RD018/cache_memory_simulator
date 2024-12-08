'''
Large and Fast: Exploiting Memory Hierarchy
'''

from math import log2

class Block(object):
    def __init__(self, num_words: int = 1, word_size: int = 16, index: str = None, tag: str = None, 
                 valid: bool = False, data: list[str] = None):
        self.num_words = num_words
        self.word_size = word_size
        self.index = index
        self.tag = tag
        self.valid = valid
        self.data = [None] * num_words

    def __str__(self):
        return f"Index: {self.index}, Tag: {self.tag}, Valid: {self.valid}, Data: {self.data}"

    def __repr__(self):
        return f"Block(index={self.index}, tag={self.tag}, valid={self.valid}, data={self.data})"                

class Cache(object):
    def __init__(self, num_blocks: int = 8, word_size: int = 16, num_words: int = 1):
        self.num_blocks = num_blocks
        self.word_size = word_size
        self.num_words = num_words
        self.blocks = [Block(num_words=self.num_words, word_size=self.word_size,
                             index=bin(_)[2:].zfill(int(log2(self.num_blocks)))) for _ in range(self.num_blocks)]

    def read(self, address: int):
        tag, index, offset = self.get_address_parts(address)
        print(f"Reading from address {address} (Binary={bin(address)[2:]},Tag={tag}, Index={index}, Offset={offset})")
        block = self.blocks[int(index,2)]    
        if block.valid and block.tag == tag:
            return True
        else:
            block.tag = tag
            block.valid = True
            block.data[int(offset,2)] = bin(address)[2:]
            return False

    def get_address_parts(self, address: int):
        binary = bin(address)[2:].zfill(self.word_size)
        if self.num_words == 1:
            tag = binary[:-int(log2(self.num_blocks))]
            index = binary[-int(log2(self.num_blocks)):]
            offset = '0'
        else:
            offset_bits = int(log2(self.num_words))
            index_bits = int(log2(self.num_blocks))
            tag = binary[:-(offset_bits + index_bits)]
            index = binary[-(offset_bits + index_bits):-offset_bits]
            offset = binary[-offset_bits:]
        return tag, index, offset

def integer_input(prompt: str) -> int:
    try:
        return int(prompt)
    except ValueError:
        try:
            return int(prompt, 16)
        except ValueError:
            ValueError("The addresses is not a valid - need to be integer or HEX numbers.")            

if __name__ == "__main__":
    # Exercise 5.2    
    WORD_SIZE = 64        
    while True:
        ADDRESSES = list(map(integer_input, input("Enter the addresses (separated by comma): ").split(",")))
        if ADDRESSES[0] == None:
            print("The separator is not a valid - need to be comma.")
        else:
            break

    # Solution 5.2.1
    cache = Cache(num_blocks=16, word_size=WORD_SIZE, num_words=1) 
    print ("Solution 5.2.1 \n")
    hitsMisses = [{addr: "Hit"} if cache.read(addr) else {addr:"Miss"} for addr in ADDRESSES]
    hits = sum(1 for hit in hitsMisses if "Hit" in hit.values())
    missRate = (len(ADDRESSES) - hits) / len(ADDRESSES)
    print(hitsMisses, "\n")
    print(f"Total hits: {hits}, Total misses: {len(ADDRESSES) - hits}, Miss Rate: {missRate*100}%\n")
       
    # Solution 5.2.2
    cache = Cache(num_blocks=8, word_size=WORD_SIZE, num_words=2)
    print ("Solution 5.2.2 \n")
    hitsMisses = [{addr: "Hit"} if cache.read(addr) else {addr:"Miss"} for addr in ADDRESSES]
    hits = sum(1 for hit in hitsMisses if "Hit" in hit.values())
    missRate = (len(ADDRESSES) - hits) / len(ADDRESSES)
    print(hitsMisses, "\n")
    print(f"Total hits: {hits}, Total misses: {len(ADDRESSES) - hits}, Miss Rate: {missRate*100}%\n")

    # Solution 5.2.3
    TOTAL_WORDS = 8
    CACHES = [Cache(num_blocks=(int(TOTAL_WORDS/1)), word_size=WORD_SIZE, num_words=1), 
              Cache(num_blocks=(int(TOTAL_WORDS/2)), word_size=WORD_SIZE, num_words=2),
              Cache(num_blocks=(int(TOTAL_WORDS/4)), word_size=WORD_SIZE, num_words=4)]
    best_cache = {}

    print ("Solution 5.2.3 \n")
    for cache in CACHES:
        print(f"Cache {CACHES.index(cache)+1}")
        hitsMisses = [{addr: "Hit"} if cache.read(addr) else {addr:"Miss"} for addr in ADDRESSES]
        hits = sum(1 for hit in hitsMisses if "Hit" in hit.values())
        missRate = round(((len(ADDRESSES) - hits) / len(ADDRESSES))*100,2)
        best_cache[f"Cache {CACHES.index(cache)+1}"] = missRate
        print('\n',hitsMisses, "\n")
        print(f"Total hits: {hits}, Total misses: {len(ADDRESSES) - hits}, Miss Rate: {missRate}%\n")

    smallest_missrate = min(best_cache.values())
    best_cache = {k: v for k, v in best_cache.items() if v == smallest_missrate}
    if len(best_cache) > 1:
        print(f"The best caches are {best_cache} with a missrate of {smallest_missrate}% that is the smallest missrate (this means that we have more hits).\n")
    else:
        print(f"The best cache is {min(best_cache, key=best_cache.get)} with a missrate of {best_cache[min(best_cache, key=best_cache.get)]}% that is the smallest missrate (this means that we have more hits).\n")
