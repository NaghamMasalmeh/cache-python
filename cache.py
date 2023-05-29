#node of the linked list / key-value pair
class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None
        self.prev = None
    
    #setters and getters

#double linked list to store items
class CacheLinkedList:
    def __init__(self):
        self.head = None
    
    #add node to the head of the list
    def addNode(self, key, value):
        new_node = Node(key = key, value = value)
        new_node.next = self.head
        new_node.prev = None

        #link the previous head to the new head
        if self.head is not None:
            self.head.prev = new_node

        self.head = new_node


    #remove node from the end of the list
    def deleteLastNode(self):
        current = self.head
        prev_curr = None

        if current == None:
            print('List has no elements to delete')
            return
        
        #check for the last node
        while current.next != None:
            prev_curr = current
            current = current.next
        
        #free last node
        prev_curr.next = None


    #move most recently used node to the head of the list
    def moveNodeToStart(self, key):
        current = self.head
        prev_curr = None

        #if the list is empty or contains only one node or the required node is already in the head
        if current == None or current.next == None or current.key == key:
            return

        #check for the required node, and keep the previous node of the current one inside prev_curr
        while current.key != key:
            prev_curr = current
            current = current.next

        temp = current
        #free the required node:
        #if it is the last node
        if current.next == None:
            prev_curr.next = None
        #if it is in the middle
        else:
            prev_curr.next = current.next
            current.next.prev = prev_curr

        #move node to head
        temp.next = self.head
        temp.prev = None
        self.head = temp

    
    #print all list items
    def printList(self):
        current = self.head
        if current == None:
            print('List is Empty')
        else:
            while current != None:
                print('{', current.key, ',', current.value, '}') 
                current = current.next
        print()


#Map/dictionary used as a cache with LRU algorithm
class Cache:
    def __init__(self, currentSize, capacity, hashMap, cacheList):
        self.currentSize = currentSize
        self.capacity = capacity
        self.hashMap = hashMap
        self.cacheList = cacheList
    
    def incrementCurrentSize(self):
        self.currentSize += 1

    def decrementCurrentSize(self):
        self.currentSize -= 1


    #Most recently used item will be always stored in the front of the list, while LRU one will be at the end of the list
    #when user add new item, it will check if the key of this item already exists in the cache or not

    def addNewItem(self, key, value):
        #if item exists, it will move it to the head of list to indicate that it is most recently used
        if key in self.hashMap:
            self.cacheList.moveNodeToStart(key)
        else:
            #if the item does not exist and the current size of items exceeds the max capacity of the cache
            #LRU item which is the last item will be removed from the cache and then the new item will be added
            if self.currentSize >= self.capacity:
                self.cacheList.deleteLastNode()
                self.decrementCurrentSize()
            self.cacheList.addNode(key, value)
            self.hashMap[key] = value
            self.incrementCurrentSize()

            