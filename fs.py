import os
import sys
import pickle
from math import ceil
from fnt import * 
from abpt import * 

class FileSystem:

    def __init__(self, n_blocks):
        self.__block_size = 256
        self.n_blocks = n_blocks
        self.n_blocks_free = n_blocks
        self.data_bitmap = [0b0 for n in range(n_blocks)]
        self.files = []
        self.n_files = 0
        self.formatted = False

    def fmt(self, n_names, n_abpt):
        '''Create FNT and ABPT
        Mark their blocks used 
        '''

        self.fnt = FilenameTable(n_names)
        self.abpt = ABPTable(self.n_blocks)
        fnt_abpt_size = ceil((sys.getsizeof(self.fnt) + sys.getsizeof(self.abpt)) / self.__block_size)
        self.n_blocks_free -= fnt_abpt_size
        del self.files[:]
        self.n_files = 0

        # Reserve blocks at end of file
        for i in range(1, fnt_abpt_size + 1):
            self.data_bitmap[self.n_blocks - i] = 0b1 # you're my only hope

        self.formatted = True

    def next_free_block(self):
        for i in range(self.n_blocks):
            if self.data_bitmap[i] == 0b0:
                return i
        return None
        

    def next_free_abp(self):
        for i in range(len(self.inode_bitmap)):
            if self.inode_bitmap[i] == 0b0:
                return i
        return None

    def ls(self, l=False):
        # TODO: make "long" version that prints ABP info
        for k in self.fnt.files.keys():
            print(k)

    def savefs(self, name):
        if self.formatted:
            self.disk = name
            f = open(name, 'wb')
            pickle.dump(self, f) # find out if this moves file pos

            if sys.getsizeof(self) < self.n_blocks * 256:
                f.truncate(self.n_blocks * 256)

            f.close()
        else:
            print('Error: must format before saving.')

    def remove(self, name):
        '''Decrement reference count in ABPT
        Reclaim blocks
        Delete the directory entry
        '''

        index = self.fnt.get_abp(name)
        self.n_blocks_free += self.abpt.get_size(index)

        for i in self.abpt.get_blocks(index):
            self.data_bitmap[i] = 0b0

        self.abpt.dec_ref(index)
        self.fnt.delete(name)

    def put(self, extern_file):
        '''Read in binary data from extern_file
        write to first available block(s) on disk
        '''
        #import pdb; pdb.set_trace()

        if extern_file in self.fnt.files.keys():
            return

        if not os.path.isfile(extern_file):
            print('No such file: %s.' % extern_file)
            return

        f = open(extern_file, 'rb')
        data = f.read()
        f.close()

        size = ceil(sys.getsizeof(data) / self.__block_size)
        if size > self.n_blocks_free:
            print('Disk out of storage!')
            return
        else:
            # Limit filenames to 56 char
            if '/' in extern_file:
                tokens = extern_file.split('/')
                fname = tokens[-1] if len(tokens[-1]) <= 56 else tokens[-1][-56]
            else:
                fname = extern_file

            self.n_blocks_free -= size
            self.files.append(data)
            self.fnt.addfile(fname, self.n_files)

            b = self.next_free_block()

            count = 0
            blocks_used = []
            for i in range(b, self.n_blocks):
                if self.data_bitmap[i] == 0b0:
                    self.data_bitmap[i] = 0b1
                    blocks_used.append(i)
                    count += 1
                if count == size:
                    break
                    
            self.abpt.new_entry(self.n_files, blocks_used)
            self.n_files += 1

    def get(self, fname):
        '''Look up fname in FNT
        Locate on disk via ABPT
        Write data to file in CWD 
        '''
        #import pdb; pdb.set_trace()
        if fname not in self.fnt.files.keys():
            return

        data = self.files[self.abpt.get_pointer(self.fnt.get_abp(fname))]
        f = open(fname, 'wb')
        f.write(data)
        f.close()

    def link(self, new, existing):
        '''Add FNT entry which
        points to an existing ABP
        '''
        self.fnt.addfile(new, self.fnt.get_abp(existing))
        self.abpt.inc_ref(self.fnt.get_abp(existing))

    def unlink(self, link):
        '''Remove FNT link entry
        '''

        self.remove(link)

    def disk_name(self):
        return self.disk

