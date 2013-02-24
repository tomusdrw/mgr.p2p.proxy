from twisted.web.http_headers import Headers

class CacheStorage:
    def __init__(self):
        pass
    
    def get(self, key, headers=Headers()):
        pass
    
    def store(self, key, headers, value):
        pass
    
class CacheObject:
    headers = None
    content = None
    hits = 0

    def __init__(self, content, headers=None):
        self.content = content
        self.headers = headers or {}
    def applyHeaders(self, headerObject):
        for key, value in self.headers.items():
            headerObject.setRawHeaders(key, value)
    def hit(self):
        self.hits += 1
