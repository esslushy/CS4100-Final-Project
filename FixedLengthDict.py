from collections import OrderedDict

class FixedLengthDict:
    def __init__(self, max_size: int, dict: OrderedDict = OrderedDict()) -> None:
        self.max_size = max_size
        self.dict: OrderedDict = dict
        
    def _prune_to_size(self):
        while len(self.dict) > self.max_size:
            # Remove oldest part of dict
            self.dict.popitem(False)

    def append(self, key, value):
        self.dict[key] = value
        self._prune_to_size()
