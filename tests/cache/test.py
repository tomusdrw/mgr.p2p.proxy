# pylint: disable=W0611
from cache.test import StoreEverytingStorage
from twisted.web.http_headers import Headers
from unittest.case import TestCase
import sure
from cache import CacheObject

class Deferred(object):
    def callback(self):
        pass

class TestStoreEverythingCache(TestCase):
    
    cut = None
    
    def setUp(self):
        self.cut = StoreEverytingStorage()

    def test_StoringItems(self):
        # Given
        len(self.cut.items()).should.be.equal(0)
        
        # When
        self.cut.put("Something", Headers(), "value")
        
        # Then
        len(self.cut.items()).should.be.equal(1)
        self.cut.items()[0].key.should.be.equal("Something")
        
    def test_retrievingItems(self):
        # Given
        self.cut.put("Something", Headers(), "value")
        
        # When
        obj = self.cut.get("Something")
        
        # Then
        isinstance(obj, CacheObject).should.be.true
        
    def test_shouldUpdateExistingEntry(self):
        # Given
        self.cut.put("Abc", Headers(), "xyz")
        
        # When
        self.cut.put("Abc", Headers(), "asd", "123123")
        
        # Then
        items = self.cut.items()
        len(items).should.equal(1)
        items[0].content.should.equal("asd")
        items[0].metadata.should.equal("123123")
        
    def test_retrievingNonExistingItems(self):
        # Given
        len(self.cut.items()).should.equal(0)
        
        # When
        item = self.cut.get("Something")
        
        # Then
        item.should.be.none
        
    def test_removingItems(self):
        # Given
        self.cut.put("a", Headers(), "xyz")
        self.cut.put("b", Headers(), "xyz")
        len(self.cut.items()).should.equal(2)
            
        # When
        self.cut.remove("a")
        
        # Then
        len(self.cut.items()).should.equal(1)
        self.cut.items()[0].key.should.equal("b")
