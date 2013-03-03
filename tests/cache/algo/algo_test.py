from cache.test import StoreEverytingStorage
from mock import patch, MagicMock
import cache.algo as cut
from unittest.case import TestCase
from twisted.web.http_headers import Headers

def test_BaseCacheLogicShouldForwardMethods():
    with patch('cache.CacheStorage') as mock:
        # Given
        instance = mock.return_value
        header = object()
        
        cl = cut.CacheLogic(instance)
        
        # When
        cl.get("someKey", header)
        cl.items()
        cl.remove("someKey2")
        cl.store("x", header, "abc")
        
        
        # Then
        instance.get.assert_called_once_with("someKey", headers=header)
        instance.items.assert_called_once_with()
        instance.remove.assert_called_once_with("someKey2")
        instance.store.assert_called_once_with("x", header, "abc")
        
class TestFifoLogic(TestCase):
    
    def test_FifoLogic(self):
        # Given
        mock = StoreEverytingStorage()
        
        cl = cut.Fifo(mock, 2)
        cl.store("key1", Headers(), "value1")
        cl.store("key2", Headers(), "value2")
        len(cl.items()).should.equal(2)
        
        # When
        cl.store("key3", Headers(), "value3")
        
        # Then
        items = cl.items()
        len(items).should.equal(2)
        items[0].key.should.equal("key2")
        items[1].key.should.equal("key3")
        
