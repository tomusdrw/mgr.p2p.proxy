from twisted.web.http_headers import Headers

class CacheStorage:
    def __init__(self):
        pass
    
    def get(self, key, headers=Headers()):
        pass
    
    def items(self):
        return []
    
    def remove(self, key):
        pass
    
    def store(self, key, headers, value):
        pass
    
class CacheObject:
    key = None
    headers = None
    _content = None
    hits = 0

    def __init__(self, key, content, headers=None):
        self.key = key
        self.content = content
        self.headers = headers or {}
    def applyHeaders(self, headerObject):
        for key, value in self.headers.items():
            headerObject.setRawHeaders(key, value)
    @property
    def content(self):
        return self._content
    def hit(self):
        self.hits += 1
