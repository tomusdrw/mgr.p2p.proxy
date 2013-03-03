
class InstanceOfMatcher(object):
    def __init__(self, clazz):
        self.clazz = clazz
    def __eq__(self, other):
        return isinstance(other, self.clazz)
    
class AnyMatcher(object):
    def __eq__(self, other):
        return True

    
def anyObj():
    return AnyMatcher()

def instanceOf(clazz):
    return InstanceOfMatcher(clazz)
