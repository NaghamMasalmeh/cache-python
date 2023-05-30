#The main goal of the below application is to design a Cache Model
#The used replacement algorithm is Least Recently Used (LRU)
#To implement this, a combination of double linked list and a hash map (dictionary) is used
#hash map will be used to store the items, while the double linked list is used to manage the LRU algorithm
#by keeping the most recently used at the head of list while the LRU at the tail

#The idea behind using the hash map is that the complexity of search inside map is O(1)
#while inside the linked list is O(n)


from cache import CacheLinkedList, Cache

def main():
    currentSize = 0
    capacity = 3
    hashMap = {}
    cacheList = CacheLinkedList()
    cache = Cache(currentSize, capacity, hashMap, cacheList)

    print('Cache System Design\n')

    cache.set_item(4,3)
    cache.set_item(5,6)
    cache.set_item(6,8)
    print(cache.hashMap)
    cache.cacheList.print_list()

    #hashMap: {4: 3, 5: 6, 6: 8}
    #LinkedList: {{6:8}, {5,6}, {4,3}}

    cache.set_item(5,7)
    print(cache.hashMap)
    cache.cacheList.print_list()

    #hashMap: {4: 3, 5: 7, 6: 8}
    #LinkedList: {{5,7}, {6:8}, {4,3}}

    cache.set_item(1,2)
    print(cache.hashMap)
    cache.cacheList.print_list()

    #hashMap: {5: 7, 6: 8, 1: 2}
    #LinkedList: {{1,2}, {5,7}, {6,8}}

    print(cache.get_item(6))  #8
    print(cache.get_item(0))  #None

if __name__ == "__main__":
    main()