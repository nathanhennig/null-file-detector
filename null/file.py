import os


class File:

    def __init__(self, name):
        self.name = name
        self.null_count = 0

        _, self.suffix = os.path.splitext(self.name)
        if self.suffix and len(self.suffix) > 0 and self.suffix[0] == '.':
            self.suffix = self.suffix[1:]

        self.size = os.stat(self.name).st_size
