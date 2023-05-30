#node of the linked list / key-value Pair
class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None
        self.prev = None
    
    #setters and getters

#double linked list to manage the LRU 
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

    #delete last node of linked list
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

    def getLastNode(self):
        current = self.head
        if current == None:
            print('Empty list')

        while current.next != None:
            current = current.next
        return current

    #move most recently used node to the head of the list and update the value of the item
    def moveNodeToStart(self, key, newValue):
        current = self.head
        prev_curr = None

        #if the list is empty or contains only one node or the required node is already in the head
        if current == None or current.next == None or current.key == key:
            if current.value != newValue:
                current.value = newValue
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
        temp.value = newValue
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


#LRU Cache 
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


    def setItem(self, key, value):
        #if the key already exists, update the value in both map and linked list
        if key in self.hashMap:
            self.hashMap[key] = value
            self.cacheList.moveNodeToStart(key, value)
            return
        
        if self.currentSize == self.capacity:
            lastNode = self.cacheList.getLastNode()
            self.cacheList.deleteLastNode()
            self.hashMap.pop(lastNode.key)
            self.decrementCurrentSize()

        self.cacheList.addNode(key, value)
        self.hashMap[key] = value
        self.incrementCurrentSize()

    
    def getItem(self, key):
        if key in self.hashMap:
            self.cacheList.moveNodeToStart(key, self.hashMap[key])
            return self.hashMap[key]
        else:
            return None


            