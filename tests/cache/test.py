# pylint: disable=W0611
from cache.test import respond, StoreEverytingStorage
from mock import MagicMock, patch
from tests.utils import matchers
from twisted.internet import defer, reactor
from twisted.web.http_headers import Headers
import sure
from cache import CacheObject
from unittest.case import TestCase

class Deferred(object):
    def callback(self):
        pass

def test_respondShouldCallReactor():
    # given
    deferred = Deferred()
    reactor.callLater = MagicMock()
    
    # when
    respond(deferred)
    
    # then
    dict2 = {
        'success' : False,
        'result' : None
    }
    reactor.callLater.assert_called_once_with(0, deferred.callback, dict2) 

class TestStoreEverythingCache(TestCase):
    
    respondPatch = None
    respondMock = None
    cut = None
    
    def setUp(self):
        self.cut = StoreEverytingStorage()
        self.respondPatch = patch('cache.test.respond')
        self.respondMock = self.respondPatch.start()
        
    def tearDown(self):
        self.respondPatch.stop() 

    def test_StoringItems(self):
        # Given
        len(self.cut.items()).should.be.equal(0)
        
        # When
        self.cut.store("Something", Headers(), "value")
        
        # Then
        len(self.cut.items()).should.be.equal(1)
        self.cut.items()[0].key.should.be.equal("Something")
        
    def test_retrievingItems(self):
        # Given
        self.cut.store("Something", Headers(), "value")
        
        # When
        self.cut.get("Something")
        
        # Then
        self.respondMock.assert_called_once_with(
                matchers.instanceOf(defer.Deferred),
                success=True,
                result=matchers.instanceOf(CacheObject))
        
    def test_shouldUpdateExistingEntry(self):
        # Given
        self.cut.store("Abc", Headers(), "xyz")
        
        # When
        self.cut.store("Abc", Headers(), "asd")
        
        # Then
        len(self.cut.items()).should.equal(1)
        self.cut.items()[0].content.should.equal("asd")
        
    def test_retrievingNonExistingItems(self):
        # Given
        len(self.cut.items()).should.equal(0)
        
        # When
        self.cut.get("Something")
        
        self.respondMock.assert_called_once_with(
                matchers.instanceOf(defer.Deferred))
        
            
            
            
