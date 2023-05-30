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
    
    def add_node(self, key, value):
        """
        Add node to the head of the list

        Parameters:
        key: int
        value: any
        """

        new_node = Node(key = key, value = value)
        new_node.next = self.head
        new_node.prev = None

        #link the previous head to the new head
        if self.head is not None:
            self.head.prev = new_node

        self.head = new_node


    def delete_last_node_and_return_key(self):
        """
        Search for the last node of linked list, remove it from the list and return it is key
        """

        current = self.head
        prev_curr = None

        if current == None:
            print('List has no elements')
            return
        
        #check for the last node
        while current.next != None:
            prev_curr = current
            current = current.next
        
        #free last node
        prev_curr.next = None
        return current.key


    def move_node_to_start(self, key, newValue):
        """
        Move most recently used node to the head of the list and update the value of the item

        Parameters:
        key: int
        newValue: any
        """
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

    
    def print_list(self):
        """
        Print the linked list
        """
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
    
    def increment_current_size(self):
        """
        Increment the current size / number of items
        """
        self.currentSize += 1

    def decrement_current_size(self):
        """
        Decrement the current size / number of items
        """
        self.currentSize -= 1


    def set_item(self, key, value):
        """
        Set the new item to the map and list based on it is key existance and manage the cache based on LRU algorithm

        Parameters:
        key: int
        value: any
        """
        #if the key already exists, update the value in both map and linked list and move the node to head of linked list
        if key in self.hashMap:
            self.hashMap[key] = value
            self.cacheList.move_node_to_start(key, value)
            return
        
        #if number of items exceeds the max size (capacity), remove the LRU at end of list from the list and map
        if self.currentSize == self.capacity:
            lastNodeKey = self.cacheList.delete_last_node_and_return_key()
            self.hashMap.pop(lastNodeKey)
            self.decrement_current_size()

        #add the new node to the list and map
        self.cacheList.add_node(key, value)
        self.hashMap[key] = value
        self.increment_current_size()

    
    def get_item(self, key):
        """
        Search for the key in the cache and return it is value if it exists

        Parameters:
        key: int

        Returns:
        None || value: any
        """
        if key in self.hashMap:
            self.cacheList.move_node_to_start(key, self.hashMap[key])
            return self.hashMap[key]
        else:
            return None


            