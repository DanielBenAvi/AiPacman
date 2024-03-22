from dataclasses import dataclass
from Objects.Node import Node


@dataclass
class PriorityQueue(object):

    queue: list[Node]

    def __init__(self):
        self.queue = []

    def __str__(self):
        return ' '.join([str(i) for i in self.queue])

    # for checking if the queue is empty
    def isEmpty(self):
        return len(self.queue) == 0

    # for inserting an element in the queue
    def insert(self, data):
        self.queue.append(data)

    # for popping an element based on Priority
    def delete(self):
        try:
            tmp_max = 0
            for i in range(len(self.queue)):
                if self.queue[i].f < self.queue[tmp_max].f:
                    tmp_max = i
            item = self.queue[tmp_max]
            del self.queue[tmp_max]
            return item
        except IndexError:
            print()
            exit()
