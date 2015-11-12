class Dictionary():
    _dict = {}
    
    def get(key=None):
        if not key:
            return _dict
        if key in self._dict:
            return self._dict[key]
        return None
    
    def set(key, value):
        self._dict[key] = value
    
    def delete(key):
        if key in self._dict:
            del self._dict[key]