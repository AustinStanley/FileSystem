import fs
import fnt
import time

class ABPTEntry:
    
    def __init__(self):
        self.filesize = 0
        self.filetype = None
        self.fileno = -1
        self.last_modified = None
        self.references = 0
        self.pointers = []

class ABPTable:
    """Attribute/Block Pointer Table"""

    def __init__(self, n_blocks):
        self.entries = [ABPTEntry() for n in range(n_blocks)]
        self.max_entries = n_blocks * 2

    def new_entry(self, index, blocks):
        self.entries[index].filesize = len(blocks) * 256
        self.entries[index].last_modified = time.time()
        self.entries[index].references = 1
        self.entries[index].pointers.extend(blocks)
        self.entries[index].fileno = index

    def get_pointer(self, index):
        return self.entries[index].fileno

    def inc_ref(self, index):
        self.entries[index].references += 1

    def dec_ref(self, index):
        self.entries[index].references -= 1

    def get_ref(self, index):
        return self.entries[index].references

    def get_size(self, index):
        return self.entries[index].filesize / 256

    def get_blocks(self, index):
        return self.entries[index].pointers
