class Stack:

    def __init__(self, **ls):
        try:
            self.__stack = list(ls['ls'])
        except KeyError:
            self.__stack = []
        except TypeError:
            self.__stack = []
            self.__stack.append(ls['ls'])

    def pop(self):
        del self.__stack[0]

    def push(self, x):
        self.__stack.insert(0, x)

    def empty(self):
        if self.__stack == []:
            return True
        else:
            return False

    def top(self):
        return self.__stack[0]

    def length(self):
        return len(self.__stack)

    def clear(self):
        t = 0
        while t < len(self.__stack):
            del self.__stack[0]

    def swap(self):
        self.__stack[0], self.__stack[1] = self.__stack[1], self.__stack[0]

    def dup(self):
        self.__stack.insert(0, self.__stack[0])
    def get_stack(self):
        return self.__stack


class Queue:

    def __init__(self, **ls):
        try:
            self.__queue = list(ls['ls'])
        except KeyError:
            self.__queue = []
        except TypeError:
            self.__queue = []
            self.__queue.append(ls['ls'])

    def enqueue(self, x):
        self.__queue.append(x)

    def dequeue(self):
        del self.__queue[0]

    def empty(self):
        if self.__queue == []:
            return True
        else:
            return False

    def length(self):
        return len(self.__queue)
    def get_Queue(self):
        return self.__queue
