class Dictionary():
    def __init__(self, dict={}):
        self.dict = dict
    
    def get(self, key=None):
        if not key:
            return self.dict
        if key in self.dict:
            return self.dict[key]
        return None
    
    def set(self, key, value):
        self.dict[key] = value
        return value
        
    def setUnique(self, key, value):
        if key in self.dict:
            return self.get(key)
        return self.set(key, value)
    
    def delete(self, key):
        if key in self.dict:
            del self.dict[key]
    
    def setMultiple(self, list, prefix, separator='_', start=0):
        cntr = start
        for ii in list:
            self.set('{0}{1}{2}'.format(prefix, separator, str(cntr)), ii)
            cntr = cntr + 1