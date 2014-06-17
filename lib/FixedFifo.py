#!/usr/bin/env python
# pylint: disable=missing-docstring
'''
A fixed-length FIFO class, which operates pretty much how you'd expect.

Size is set at instantiation.  Items are emplaced using push(), and removed
using pop().  It can only hold the number of items set during instantiation,
so attempting to push when it is full will result in an item being popped to
stay under the limit.

usage:

# create an instance with size = 3
>>> demo = FixedFifo(3)

# push three items into the FIFO and confirm its length
>>> demo.push('a')
>>> demo.push('b')
>>> demo.push('c')
>>> len(demo)
3

# check if item is in the FIFO
>>> 'a' in demo
True

# push a fourth item.  since size = 3, should displace first item ('a')
>>> demo.push('d')
'a'

# pop the last item.  'a' is already gone, next should be 'b'
>>> demo.pop()
'b'
    '''

class FixedFifo(object):
    def __init__(self, max_size):
        self.max_size = max_size
        self.contents = []

    def __contains__(self, key):
        return key in self.contents

    def __len__(self):
        return len(self.contents)

    def pop(self):
        return self.contents.pop()

    def push(self, key):
        self.contents.insert(0, key)
        return self.pop() if len(self.contents) > self.max_size else None

    def size(self):
        return self.max_size

    def resize(self, newsize):
        self.contents = self.contents[:newsize]
        self.max_size = newsize

if __name__ == "__main__":
    import doctest
    doctest.testmod()
