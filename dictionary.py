class Dictionary():
    _dict = {}
    
    def get(self, key=None):
        if not key:
            return self._dict
        if key in self._dict:
            return self._dict[key]
        return None
    
    def set(self, key, value):
        self._dict[key] = value
    
    def delete(self, key):
        if key in self._dict:
            del self._dict[key]
    
    def setMultiple(self, list, prefix, separator='_', start=0):
        cntr = start
        for ii in list:
            self.set('{0}{1}{2}'.format(prefix, separator, str(cntr)), ii)
            cntr = cntr + 1