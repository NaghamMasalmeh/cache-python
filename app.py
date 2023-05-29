#The main goal of the below application is to design a Cache Model
#The used replacement algorithm is Least Recently Used (LRU)
#To implement this, a combination of double linked list and a hash map (dictionary) is used
#Linked list is used to store the items/elements/key-value pairs while the hash map is used
#as a cache to store the key for each item, so when user insert new item, it will check if the
#map contains the key and if it doesn't then it will add it to our list.

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

    while (True):
        new_data = input('Enter Your Key-value Pair separated by ",":\n')
        temp_data = new_data.split(',')
        cache.addNewItem(int(temp_data[0]), temp_data[1])
        print()
        cacheList.printList()

if __name__ == "__main__":
    main()