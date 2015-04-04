import fs
import abpt

class FilenameTable:

    def __init__(self, n_files):
        self.n_files = int(n_files)
        self.files = {}

    def addfile(self, name, abpt_pointer):
        if len(self.files) < self.n_files:
            self.files[name] = abpt_pointer
        else:
            raise Exception

    def get_abp(self, fname):
        return self.files[fname]

    def delete(self, fname):
        del self.files[fname]
