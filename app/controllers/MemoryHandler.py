class MemoryHandler:
    def __init__(self):
        self.bag = {}

    def set_memory_bag(self, memory):
        self.bag = memory

    def get_memory_bag(self):
        return self.memory_bag

    def del_memory_bag(self, name):
        self.bag[name] = {}

    def clear_memory_bag(self):
        self.bag = {}
