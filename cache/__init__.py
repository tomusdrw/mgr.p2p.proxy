class CacheStorage:
    def __init__(self):
        pass
    
    def get(self, key, headers=None):
        pass
    
    def store(self, key, value):
        pass
    
class CacheObject:
    headers = None
    content = None
    hits = 0

    def __init__(self, content, headers=None):
        self.content = content
        self.headers = headers
    def applyHeaders(self, headerObject):
        if self.headers is not None:
            for key, value in self.headers.items():
                headerObject.addRawHeader(key, value)
    def hit(self):
        self.hits += 1
